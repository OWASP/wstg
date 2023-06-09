# Test Network Infrastructure Configuration

|ID          |
|------------|
|WSTG-CONF-01|

## Summary

The intrinsic complexity of interconnected and heterogeneous web server infrastructure, which can include hundreds of web applications, makes configuration management and review a fundamental step in testing and deploying every single application. It takes only a single vulnerability to undermine the security of the entire infrastructure, and even small and seemingly unimportant problems may evolve into severe risks for another application on the same server. In order to address these problems, it is of utmost importance to perform an in-depth review of configuration and known security issues, after having mapped the entire architecture.

Proper configuration management of the web server infrastructure is very important in order to preserve the security of the application itself. If elements such as the web server software, the backend database servers, or the authentication servers are not properly reviewed and secured, they might introduce undesired risks or introduce new vulnerabilities that might compromise the application itself.

For example, a web server vulnerability that would allow a remote attacker to disclose the source code of the application itself (a vulnerability that has arisen a number of times in both web servers and application servers) could compromise the application, as anonymous users could use the information disclosed in the source code to leverage attacks against the application or its users.

The following steps need to be taken to test the configuration management infrastructure:

- The different elements that make up the infrastructure need to be determined in order to understand how they interact with a web application and how they affect its security.
- All the elements of the infrastructure need to be reviewed in order to make sure that they don't contain any known vulnerabilities.
- A review needs to be made of the administrative tools used to maintain all the different elements.
- The authentication systems need to reviewed in order to assure that they serve the needs of the application and that they cannot be manipulated by external users to leverage access.
- A list of defined ports which are required for the application should be maintained and kept under change control.

After having mapped the different elements that make up the infrastructure (see [Map Network and Application Architecture](../01-Information_Gathering/10-Map_Application_Architecture.md)), it is possible to review the configuration of each element founded and test for any known vulnerabilities.

## Test Objectives

- Review the applications' configurations set across the network and validate that they are not vulnerable.
- Validate that used frameworks and systems are secure and not susceptible to known vulnerabilities due to unmaintained software or default settings and credentials.

## How to Test

### Known Server Vulnerabilities

Vulnerabilities in various areas of the application architecture, whether in the web server or the backend database, can severely compromise the application. For example, consider a server vulnerability that allows a remote, unauthenticated user to upload files to the web server or even replace existing files. This vulnerability could compromise the application, since a rogue user may be able to replace the application itself or introduce code that would affect the backend servers, as its application code would be run just like any other application.

Reviewing server vulnerabilities can be hard to do if the test needs to be done through a blind penetration test. In these cases, vulnerabilities need to be tested from a remote site, typically using an automated tool. However, testing for some vulnerabilities can have unpredictable results on the web server, and testing for others (like those directly involved in denial of service attacks) might not be possible due to the service downtime involved if the test was successful.

Some automated tools will flag vulnerabilities depending on the version of the web server they retrieve. This leads to both false positives and false negatives. On one hand, if the web server version has been removed or obscured by the local site administrator the scan tool will not flag the server as vulnerable even if it is. On the other hand, if the vendor providing the software does not update the web server version when vulnerabilities are fixed, the scan tool will flag vulnerabilities that do not exist. The latter case is actually very common as some operating system vendors back port patches of security vulnerabilities to the software they provide in the operating system, but do not do a full upload to the latest software version. This happens in most GNU/Linux distributions such as Debian, Red Hat, and SuSE. In most cases, vulnerability scanning of an application architecture will only find vulnerabilities associated with the "exposed" elements of the architecture (such as the web server) and will usually be unable to find vulnerabilities associated to elements which are not directly exposed, such as the authentication backend, the backend database, or reverse proxies [1] in use.

Finally, not all software vendors publicly disclose vulnerabilities, which means these weaknesses may not be registered within known vulnerability databases [2]. This information is only disclosed to customers or published through fixes that do not have accompanying advisories. This reduces the effectiveness of vulnerability scanning tools. Typically, vulnerability coverage of these tools will be very good for common products (such as the Apache web server, Microsoft IIS, or IBM's Lotus Domino) but will be lacking for lesser known products.

This is why reviewing vulnerabilities is best done when the tester is provided with internal information about the software, including versions, releases, and patches applied. With this information, the tester can retrieve data from the vendor and analyze potential vulnerabilities in the architecture, as well as their potential impact on the application. When possible, these vulnerabilities can be tested to determine their real effects and to detect if there might be any external elements (such as intrusion detection or prevention systems) that might reduce or negate the possibility of successful exploitation. Testers might even determine through a configuration review that the vulnerability is not actually present since it affects a software component that is not in use.

It is also worthwhile to note that vendors will sometimes silently fix vulnerabilities and make the fixes available with new software releases. Different vendors have varying release cycles that determine the support they may provide for older releases. A tester with detailed information about the software versions used by the architecture can analyse the risk associated with the use of old software releases that might be unsupported in the short term or are already unsupported. This is critical because if a vulnerability emerges in an unsupported older software version, the systems personnel may not be directly aware of it. No patches will be ever made available for it and advisories might not list that version as vulnerable as it is no longer supported. Even if they are aware of the vulnerability and the associated system risks, a full upgrade to a new software release will be necessary, potentially introducing significant downtime in the application architecture or necessitating application re-coding due to incompatibilities with the latest software version.

### Administrative Tools

Any web server infrastructure requires the existence of administrative tools to maintain and update the information used by the application. This information includes static content (web pages, graphic files), application source code, user authentication databases, etc. The type of administrative tools used can vary depending on the specific site, technology, or software in use. For example, some web servers will be managed using administrative interfaces which are themselves web servers (such as the iPlanet web server) or will be administrated by plain text configuration files (such as in the Apache case [3]) or use operating-system GUI tools (such as when using Microsoft's IIS server or ASP.Net).

In most cases, the server configuration is managed with various file maintenance tools, administered through FTP servers, WebDAV, network file systems (NFS, CIFS), or other mechanisms. Obviously, the operating system of the elements that make up the application architecture will also be managed using other tools. Applications may also contain embedded administrative interfaces for managing application data (users, content, etc.).

After mapping the administrative interfaces used to manage different parts of the architecture, it is important to review them. If an attacker gains access to any of these interfaces, they could potentially compromise or damage the application architecture. To accomplish this, it's important to:

- Determine the mechanisms that control access to these interfaces and their associated susceptibilities. This information may be available online.
- Ensure that the default username and password are changed.

Some companies choose not to manage all aspects of their web server applications and may delegate content management to other parties. This external company might provide only certain parts of the content (such as news updates or promotions), or it might completely manage the web server (including content and code). It is common to find administrative interfaces available from the internet in these situations, since using the internet is cheaper than providing a dedicated line that will connect the external company to the application infrastructure through a management-only interface. In such situations, it's crucial to test whether the administrative interfaces are vulnerable to attacks.

## References

- [1] WebSEAL, also known as Tivoli Authentication Manager, is a reverse proxy from IBM which is part of the Tivoli framework.
- [2] Such as Symantec's Bugtraq, ISS' X-Force, or NIST's National Vulnerability Database (NVD).
- [3] There are some GUI-based administration tools for Apache (like NetLoony) but they are not in widespread use yet.
