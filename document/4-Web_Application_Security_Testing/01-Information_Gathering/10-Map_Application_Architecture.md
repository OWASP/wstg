# Map Application Architecture

|ID          |
|------------|
|WSTG-INFO-10|

## Summary

In order to effectively test an application, and to be able to provide meaningful recommendations on how to address any of the issues identified, it is important to understand what you are actually testing. Additionally, it can help determine whether specific components should be considered out of scope for testing.

Modern web applications can vary significantly in complexity, from a simple script running on a single server to a highly complex application spread across dozens of different systems, languages and components. There may also be additional network-level components such as firewalls or intrusion protection systems that can have a significant impact on testing.

## Test Objectives

- Understand the architecture of the application and the technologies in use.

## How to Test

When testing from a black box perspective, it is important to try and build up a clear picture of how the application works, and which technologies and components are in place. In some cases it is possible to test for specific components (such as a web application firewall), while others can be identified by inspecting the behaviour of the application.

The sections below provide a high-level overview of common architectural components, along with details of how they can be identified.

### Application Components

#### Web Server

Simple applications may run on a single server, which can be identified using the steps discussed in the [Fingerprint Web Server](02-Fingerprint_Web_Server.md) section of the guide.

#### Platform-as-a-Service (PaaS)

In a Platform-as-a-Service (PaaS) model, the web server and underlying infrastructure are managed by the service provider, and the customer is only responsible for the application that this deployed on them. From a testing perspective, there are two main differences:

- The application owner has no access to the underlying infrastructure, so will be unable to directly remediate any issues.
- Infrastructure testing is likely to be out of scope for any engagements.

In some cases it is possible to identify the use of PaaS, as the application may use a specific domain name (for example, applications deployed on Azure App Services will have a `*.azurewebsites.net` domain - although they may also use custom domains). However, in other cases it is difficult to determine whether PaaS is in use.

#### Serverless

In a Serverless model, the developers provide code which is directly run on a hosting platform as individual functions, rather than as an traditional larger web application deployed in a webroot. This makes it well suited to microservice-based architectures. As with a PaaS environment, infrastructure testing is likely to be out of scope.

In some cases the use of Serverless code may be indicated by the presence of specific HTTP headers. For example, AWS Lambda functions will typically return the following headers:

```http
X-Amz-Invocation-Type
X-Amz-Log-Type
X-Amz-Client-Context
```

Azure Functions are less obvious. They typically return the `Server: Kestrel` header - but this on its own is not enough to be confident that it is an Azure App function, rather than some other code running on Kestrel.

#### Microservices

In a microservice-based architecture, the application API is made up of multiple discrete services, rather than running as a monolithic application. The services themselves often run inside containers (usually with Kubernetes), and can use a variety of different operating systems and languages. Although they are typically behind a single API gateway and domain, the use of multiple languages (often indicated in detailed error messages) can suggest that microservices are in use.

#### Static Storage

Many applications store static content on dedicated storage platforms, rather than hosting it directly on the main web server. The two most common platforms are Amazon's S3 Buckets, and Azure's Storage Accounts, and can be easily identified by the domain names:

- Amazon S3 Buckets are either `BUCKET.s3.amazonaws.com` or `s3.REGION.amazonaws.com/BUCKET`
- Azure Storage Accounts are `ACCOUNT.blob.core.windows.net`

These storage accounts can often exposes sensitive files, as discussed in the [Testing Cloud Storage Guide](../02-Configuration_and_Deployment_Management_Testing/11-Test_Cloud_Storage.md) section.

#### Database

Most non-trivial web applications use some kind of database to store dynamic content. In some cases it's possible to determine the database, although it usually relies on other issues in the application. This can often be done by:

- Port scanning the server and looking for any open ports associated with specific databases.
- Triggering SQL (or NoSQL) related error messages (or finding existing errors from a [search engine](../01-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage.md).

Where it's not possible to conclusively determine the database, you can often make an educated guess based on other aspects of the application:

- Windows, IIS and ASP.NET often use Microsoft SQL server.
- Embedded systems often use SQLite.
- PHP often uses MySQL or PostgreSQL.
- APEX often uses Oracle.

These are not hard rules, but can certainly give you a reasonable starting point if no better information is available.

#### Authentication

Most applications have some form of authentication for users. There are multiple authentication back ends that can be used, such as:

- Web server configuration (including `.htaccess` files) or hard-coding passwords in scripts.
    - Usually shows up as HTTP Basic authentication, indicated by a pop-up in the browser and a `WWW-Authenticate: Basic` HTTP header.
- Local user accounts in a database.
    - Usually integrated into a form or API endpoint on the application.
- An existing central authentication source such as Active Directory or an LDAP server.
    - May use NTLM authentication, indicated by a `WWW-Authenticate: NTLM` HTTP header.
    - May be integrated into the web application in a form.
    - May require the username to be entered in the "DOMAIN\username" format, or may give a dropdown of available domains.
- Single Sign-On (SSO) with either an internal or external provider.
    - Typically uses OAuth, OpenID Connect, or SAML.

Applications may provide multiple options for the user to authenticate (such as registering a local account, or using their existing Facebook account), and may use different mechanisms for normal users and administrators.

#### Third Party Services and APIs

Almost all web applications include third party resources that are loaded or interacted with by the client. These can include:

- [Active content](https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content#mixed_active_content) (such as scripts, style sheets, fonts, and iframes).
- [Passive content](https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content#mixed_passivedisplay_content) (such as images and videos).
- External APIs.
- Social media buttons.
- Advertising networks.
- Payment gateways.

These resources are requested directly by the user's browser, so can easily be identified using the developer tools, or an intercepting proxy. While it is important to identify them (as they can impact the security of the application), remember that *they are usually out of scope for testing*, as they belong to third parties.

### Network Components

#### Reverse Proxy

A reverse proxy sits in front of one or more back end servers and redirects requests to the appropriate destination. They can implement various functionality, such as:

- Acting as a [load balancer](#load-balancer) or [web application firewall](#web-application-firewall-waf).
- Allowing multiple applications to be hosted on a single IP address or domain (in subfolders).
- Implementing IP filtering or other restrictions.
- Caching content from the back end to improve performance.

It is not always possible to detect a reverse proxy (especially if there is only a application behind it), but you can often sometimes identify it by:

- A mismatch between the front end server and the back end application (such as a `Server: nginx` header with an ASP.NET application).
    - This can sometimes lead to [request smuggling vulnerabilities](https://portswigger.net/web-security/request-smuggling).
- Duplicate headers (especially the `Server` header).
- Multiple applications hosted on the same IP address or domain (especially if they use different languages).

#### Load Balancer

A load balancer sits in front of multiple back end servers and allocates requests between them in order to provide greater redundancy and processing capacity for the application.

Load balancers can be difficult to detect, but can sometimes be identified by making multiple requests and examining the responses for differences, such as:

- Inconsistent system times.
- Different internal IP addresses or hostnames in detailed error messages.
- Different addresses returned from [Server-Side Request Forgery (SSRF)](../07-Input_Validation_Testing/19-Testing_for_Server-Side_Request_Forgery.md).

They may also be indicated by the presence of specific cookies (for example, F5 BIG-IP load balancers will create a cookie called `BIGipServer`.

#### Content Delivery Network (CDN)

A Content Delivery Network (CDN) is a geographically distributed set of caching proxy servers, designed to improve website performance to provide additional resilience for a website.

It is typically configured by pointing the publicly facing domain to the CDN's servers, and then configuring the CDN to connect to the correct back end servers (sometimes known as the "origin").

The easiest way to detect a CDN is to perform a WHOIS lookup for the IP addresses that the domain resolves to. If they belong to a CDN company (such as Akamai, Cloudflare or Fastly - see [Wikipedia](https://en.wikipedia.org/wiki/Content_delivery_network#Notable_content_delivery_service_providers) for a more complete list) then it's like that a CDN is in use.

When testing a site behind a CDN, you should bear in mind the following points:

- The IPs and servers belong to the CDN provider, and are likely to be out of scope for infrastructure testing.
- Many CDNs also include features like bot detection, rate limiting, and web application firewalls.
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

Additionally, if inappropriate services are exposed to the world (such as SMTP, IMAP, MySQL, etc), this suggests that either there is no firewall in place, or that the firewall is badly configured.

#### Network Intrusion Detection and Prevention System

A network Intrusion Detection System (IDS) detects suspicious or malicious network-level activity (such as port or vulnerability scanning) and raises alerts. An Intrusion Prevention System (IPS) is similar, but also takes action to prevent the activity - usually by blocking the source IP address.

An IPS can usually be detected by running automated scanning tools (such as a port scanner) against the target, and seeing if the source IP is blocked. However, many application-level tools may not be detected by an IPS (especially if it doesn't decrypt TLS).

#### Web Application Firewall (WAF)

A Web Application Firewall (WAF) inspects the contents of HTTP requests and blocks those that appear to be suspicious or malicious, or dynamically apply other controls such as CAPTCHA or rate limiting. They are usually based on a set of known bad signatures and regular expressions, such as the [OWASP Core Rule Set](https://owasp.org/www-project-modsecurity-core-rule-set/).  WAFs can be effective at protecting against some types of attacks (such as SQL injection or cross-site scripting), but are less effective against other types (such as access control or business logic related issues).

A WAF can be deployed in multiple locations, including:

- On the web server itself.
- On a separate virtual machine or hardware appliance.
- In the cloud in front of the back end server.

Because a WAF blocks malicious requests, it can be detected by adding common attack strings to parameters and observing whether or not they are blocked. For example, try adding a parameter called `foo` with a value such as `' UNION SELECT 1` or `><script>alert(1)</script>`. If these requests are blocked then it suggests that there may be a WAF in place. Additionally, the contents of the block pages may provide information about the specific technology that is in use. Finally, some WAFs may add cookies or HTTP headers to responses that can reveal their presence.

If a cloud-based WAF is in use, then it may be possible to bypass it by directly accessing the back end server, using the same methods discussed in the [Content Delivery Network](#content-delivery-network-cdn) section.
