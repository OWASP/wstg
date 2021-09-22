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

- Detecting via DNS
- Usually caches content
- May include IPS/WAF functionality
- Identifying backend servers

### Security Components

#### Network Firewall

Most web servers will be protected by a packet filtering or stateful inspection firewall, which blocks any network traffic that is not required. To detect this, perform a port scan of the server and examine the results.

If the majority of the ports are shown as "closed" (i.e, they return a `RST` packet in response to the initial `SYN` packet) then this suggests that the server may not be protected by a firewall. If the ports are shown as "filtered" (i.e, no response is received when sending a `SYN` packet to an unused port) then a firewall is most likely to be in place.

Additionally, if inappropriate services are exposed to the world (such as SMTP, IMAP, MySQL, etc), this suggests that either there is not firewall in place, or that the firewall is badly configured.

#### Network Intrusion Detection and Prevention System

- Blocks traffic at network level (port scanning)
- How to bypass

#### Local Web Application Firewall (WAF)

- Error pages/messages may reveal
- Add test params: `index.php?madeup=<script>alert(1)</script>`

#### Cloud Web Application Firewall (WAF)

- Detect from DNS
- Similar functionality to local WAF, but hosted in cloud
- How to detect backend server addresses
