# Map Application Architecture

|ID          |
|------------|
|WSTG-INFO-10|

## Summary

The complexity of interconnected and heterogeneous web infrastructure can include hundreds of web applications and makes configuration management and review a fundamental step in testing and deploying every single application. In fact it takes only a single vulnerability to undermine the security of the entire infrastructure, and even small and seemingly unimportant problems may evolve into severe risks for another application in the same infrastructure.

To address these problems, it is of utmost importance to perform an in-depth review of configuration and known security issues. Before performing an in-depth review it is necessary to map the network and application architecture. The different elements that make up the infrastructure need to be determined to understand how they interact with a web application and how they affect security.

## Test Objectives

- Generate a map of the application at hand based on the research conducted.

## How to Test

- Various common components listed below with steps on how to identify them
- Note that a single device/system may provide functionality from multiple areas (such as a combined reverse proxy/firewall/IPS/WAF)

### Application Components

#### Web Server

Simple applications may run on a single server, which can be identified using the steps discussed in [Fingerprint Web Server](02-Fingerprint_Web_Server.md) section of the guide.

#### Platform-as-a-Service (PaaS)

- Azure App Services
*.azurewebsites.net - although may have custom domain
- Infrastructure testing unlikely to be successful + out of scope

#### Serverless

- Azure Functions

```http
Server: Kestrel - Not a guarantee
```

- AWS Lambdas

```http
X-Amz-Invocation-Type
X-Amz-Log-Type
X-Amz-Client-Context
```

#### Static Storage

- AWS S3 buckets and Azure Storage accounts

#### Database

- Usually present in complex applications (although may not be directly queried)
- SQL error messages (XREF SQL Injection)
- Guess based on language
    - .NET -> SQL Server
    - APEX -> Oracle
    - PHP -> MySQL or PostgreSQL

#### Authentication

- LDAP domain might be displayed on login page. LDAP injection might work.
- SAML/SSO is obvious from login process

#### Third Party Services and APIs

- Embedded content (videos, maps, etc)
- Iframes
- Third party APIs (may expose keys)

### Network Components

#### Reverse Proxy

- Nginx is almost always used as a reverse proxy
- Redis as cache
- Multiple sites on same IP (although could be vhosts)
- Multiple languages/frameworks in use
- Mismatch between headers (ASP.NET + Nginx)
- Different folders/paths/files may go to different servers

Detecting a reverse proxy in front of the web server can be done by analysis of the web server banner, which might directly disclose the existence of a reverse proxy. It can also be determined by obtaining the answers given by the web server to requests and comparing them to the expected answers. For example, some reverse proxies act as Intrusion Prevention Systems (IPS) by blocking known attacks targeted at the web server. If the web server is known to answer with a 404 message to a request that targets an unavailable page and returns a different error message for some common web attacks like those done by vulnerability scanners, it might be an indication of a reverse proxy (or an application-level firewall) which is filtering the requests and returning a different error page than the one expected. Another example: if the web server returns a set of available HTTP methods (including TRACE) but the expected methods return errors then there is probably something in between blocking them.

Reverse proxies can also be introduced as proxy-caches to accelerate the performance of back-end application servers. Detecting these proxies can be done based on the server header. They can also be detected by timing requests that should be cached by the server and comparing the time taken to server the first request with subsequent requests.

#### Load Balancer

Another element that can be detected is network load balancers. Typically, these systems will balance a given TCP/IP port to multiple servers based on different algorithms (round-robin, web server load, number of requests, etc.). Thus, the detection of this architecture element needs to be done by examining multiple requests and comparing results to determine if the requests are going to the same or different web servers. For example, based on the Date header if the server clocks are not synchronized. In some cases, the network load balance process might inject new information in the headers that will make it stand out distinctly, like the `BIGipServer` prefixed cookie introduced by F5 BIG-IP load balancers.

#### Content Delivery Network (CDN)

A Content Delivery Network (CDN) is a geographically distributed set of caching proxy servers, designed to improve website performance to to provide additional resilience for a website.

It is typically configured by pointing the publicly facing domain to the CDN's servers, and then configuring the CDN to connect to the correct back end servers (sometimes known as the "origin").

The easiest way to detect a CDN is to perform a WHOIS lookup for the IP addresses that the domain resolves to. If they belong to a CDN company (such as Akami, Cloudflare or Fastly - see [Wikipedia](https://en.wikipedia.org/wiki/Content_delivery_network#Notable_content_delivery_service_providers) for a more complete list) then it's like that a CDN is in use.

When testing a site behind a CDN, you should bear in mind the following points:

- The IPs and servers belong to the CDN provider, and are likely to be out of scope for infrastructure testing.
- Many CDNs also include features like bot detection, rate limiting and web application firewalls.
- CDNs usually cache content, so any changes made to the back end website may not appear immediately.

If the site is behind a CDN, then it can be useful to identify the back end servers. If they don't have proper access control enforced, then you may be able to bypass the CDN (and any protections it offers) by directly accessing the back end servers. There are a variety of different methods that may allow you to identify the back end system:

- Emails sent by the application may come direct from the back end server, which could reveal it's IP address.
- DNS grinding, zone transfers or certificate transparency lists for domain may reveal it on a subdomain.
- Scanning the IP ranges known to be used by the company may find the back end server.
- Exploiting [Server-Side Request Forgery (SSRF)](../07-Input_Validation_Testing/19-Testing_for_Server-Side_Request_Forgery.md) may reveal the IP address.
- Detailed error messages from the application may expose IP addresses or hostnames.

### Security Components

#### Network Firewall

Most web servers will be protected by a packet filtering or stateful inspection firewall, which blocks any network traffic that is not required. To detect this, perform a port scan of the server and examine the results.

If the majority of the ports are shown as "closed" (i.e, they return a `RST` packet in response to the initial `SYN` packet) then this suggests that the server may not be protected by a firewall. If the ports are shown as "filtered" (i.e, no response is received when sending a `SYN` packet to an unused port) then a firewall is most likely to be in place.

Additionally, if inappropriate services are exposed to the world (such as SMTP, IMAP, MySQL, etc), this suggests that either there is not firewall in place, or that the firewall is badly configured.

#### Network Intrusion Detection and Prevention System

An Network Intrusion Detection System (IPS) detects suspicious or malicious network-level activity (such as port or vulnerability scanning) and raises alerts. An Intrusion Prevention System (IPS) is similar, but also takes action to prevent the activity - usually by blocking the source IP address.

An IPS can usually be detected by running automated scanning tools (such as a port scanner) against the target, and seeing if the source IP is blocked. However, many application-level tools may not be detected by an IPS (especially if it doesn't decrypt TLS).

#### Local Web Application Firewall (WAF)

- Error pages/messages may reveal
- Add test params: `index.php?madeup=<script>alert(1)</script>`

#### Cloud Web Application Firewall (WAF)

- Detect from DNS
- Similar functionality to local WAF, but hosted in cloud
- How to detect backend server addresses
