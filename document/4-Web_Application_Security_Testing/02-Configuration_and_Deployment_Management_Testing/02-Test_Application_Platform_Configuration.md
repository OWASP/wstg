# Test Application Platform Configuration

|ID          |
|------------|
|WSTG-CONF-02|

## Summary

Proper configuration of the single elements that make up an application architecture is important in order to prevent mistakes that might compromise the security of the whole architecture.

Reviewing and testing configurations are critical tasks in creating and maintaining an architecture. This is because various systems often come with generic configurations, which may not align well with the tasks they're supposed to perform on the specific sites where they're installed.

While the typical web and application server installation will contain a lot of functionality (like application examples, documentation, test pages), what is not essential should be removed before deployment to avoid post-install exploitation.

## Test Objectives

- Ensure that default and known files have been removed.
- Validate that no debugging code or extensions are left in the production environments.
- Review the logging mechanisms set in place for the application.

## How to Test

### Black-Box Testing

#### Sample and Known Files and Directories

In a default installation, many web servers and application servers provide sample applications and files for the benefit of the developer, in order to test if the server is working properly right after installation. However, many default web server applications have later been known to be vulnerable. This was the case, for example, for CVE-1999-0449 (Denial of Service in IIS when the Exair sample site had been installed), CAN-2002-1744 (Directory traversal vulnerability in CodeBrws.asp in Microsoft IIS 5.0), CAN-2002-1630 (Use of sendmail.jsp in Oracle 9iAS), or CAN-2003-1172 (Directory traversal in the view-source sample in Apache’s Cocoon).

CGI scanners, which include a detailed list of known files and directory samples provided by different web or application servers, might be a fast way to determine if these files are present. However, the only way to be really sure is to do a full review of the contents of the web server or application server, and determine whether they are related to the application itself or not.

#### Comment Review

It is very common for programmers to add comments when developing large web-based applications. However, comments included inline in HTML code might reveal internal information that should not be available to an attacker. Sometimes, a part of the source code is commented out when a functionality is no longer required, but this comment is unintentionally leaked out to the HTML pages returned to the users.

Comment review should be done in order to determine if any information is being leaked through comments. This review can only be thoroughly done through an analysis of the web server's static and dynamic content, and through file searches. It can be useful to browse the site in an automatic or guided fashion, and store all the retrieved content. This retrieved content can then be searched in order to analyse any HTML comments available in the code.

#### System Configuration

Various tools, documents, or checklists can be used to give IT and security professionals a detailed assessment of the target systems' conformance to various configuration baselines or benchmarks. Such tools include, but are not limited to, the following:

- [CIS-CAT Lite](https://www.cisecurity.org/blog/introducing-cis-cat-lite/)
- [Microsoft's Attack Surface Analyzer](https://github.com/microsoft/AttackSurfaceAnalyzer)
- [NIST's National Checklist Program](https://nvd.nist.gov/ncp/repository)

### Gray-Box Testing

#### Configuration Review

The web server or application server configuration takes an important role in protecting the contents of the site and it must be carefully reviewed in order to spot common configuration mistakes. Obviously, the recommended configuration varies depending on the site policy, and the functionality that should be provided by the server software. In most cases, however, configuration guidelines (either provided by the software vendor or external parties) should be followed to determine if the server has been properly secured.

It is impossible to generically say how a server should be configured, however, some common guidelines should be taken into account:

- Only enable server modules (ISAPI extensions in the case of IIS) that are needed for the application. This reduces the attack surface since the server is reduced in size and complexity as software modules are disabled. It also prevents vulnerabilities that might appear in the vendor software from affecting the site if they are only present in modules that have been already disabled.
- Handle server errors (40x or 50x) with custom-made pages instead of with the default web server pages. Specifically make sure that any application errors will not be returned to the end user and that no code is leaked through these errors since it will help an attacker. It is actually very common to forget this point since developers do need this information in pre-production environments.
- Make sure that the server software runs with minimized privileges in the operating system. This prevents an error in the server software from directly compromising the whole system, although an attacker could elevate privileges once running code as the web server.
- Make sure the server software properly logs both legitimate access and errors.
- Make sure that the server is configured to properly handle overloads and prevent Denial of Service attacks. Ensure that the server has been performance-tuned properly.
- Never grant non-administrative identities (with the exception of `NT SERVICE\WMSvc`) access to applicationHost.config, redirection.config, and administration.config (either Read or Write access).
- Never share out applicationHost.config, redirection.config, and administration.config on the network.
- Do not store sensitive information in readable configuration files.
- Encrypt sensitive configuration data where required.
- Restrict access to shared configuration and protect it appropriately.

#### Logging

Logging is an important part of application security. It supports monitoring, incident response, and investigations. Review both platform and application logging to determine whether security-relevant events are recorded, whether the records are useful, and whether the logging process introduces additional risk.

During the review, verify the following:

- Security-relevant events are logged.
- Log entries contain enough context to support investigation.
- Logs do not store secrets or unnecessary sensitive data.
- Logged data is handled safely before storage and display.
- Access to logs is restricted to authorized personnel.
- Logs are protected against tampering and retained appropriately.
- Logging failures do not expose sensitive debugging information.
- Logs can be centralized or correlated in distributed environments.

Testing should confirm that logs are usable, consistent, and effectively support detection and response activities.

## References

- Apache
    - Apache Security, by Ivan Ristic, O’reilly, March 2005.
    - [Apache Security Secrets: Revealed (Again), Mark Cox, November 2003](https://awe.com/mark/talks/apachecon2003us.html)
    - [Apache Security Secrets: Revealed, ApacheCon 2002, Las Vegas, Mark J Cox, October 2002](https://awe.com/mark/talks/apachecon2002us.html)
    - [Performance Tuning](https://httpd.apache.org/docs/current/misc/perf-tuning.html)
- Lotus Domino
    - Lotus Security Handbook, William Tworek et al., April 2004, available in the IBM Redbooks collection
    - Lotus Domino Security, an X-force white-paper, Internet Security Systems, December 2002
    - Hackproofing Lotus Domino Web Server, David Litchfield, October 2001
- Microsoft IIS
    - [Security Best Practices for IIS 8](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/jj635855(v=ws.11))
    - [CIS Microsoft IIS Benchmarks](https://www.cisecurity.org/benchmark/microsoft_iis/)
    - Securing Your Web Server (Patterns and Practices), Microsoft Corporation, January 2004
    - IIS Security and Programming Countermeasures, by Jason Coombs
    - From Blueprint to Fortress: A Guide to Securing IIS 5.0, by John Davis, Microsoft Corporation, June 2001
    - Secure IIS 5 Checklist, by Michael Howard, Microsoft Corporation, June 2000
- Red Hat’s (formerly Netscape’s) iPlanet
    - Guide to the Secure Configuration and Administration of iPlanet Web Server, Enterprise Edition 4.1, by James M Hayes, The Network Applications Team of the Systems and Network Attack Center (SNAC), NSA, January 2001
- WebSphere
    - IBM WebSphere V5.0 Security, WebSphere Handbook Series, by Peter Kovari et al., IBM, December 2002.
    - IBM WebSphere V4.0 Advanced Edition Security, by Peter Kovari et al., IBM, March 2002.
- General
    - [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), OWASP
    - [SP 800-92](https://csrc.nist.gov/publications/detail/sp/800-92/final) Guide to Computer Security Log Management, NIST
    - [PCI DSS v3.2.1](https://www.pcisecuritystandards.org/document_library) Requirement 10 and PA-DSS v3.2 Requirement 4, PCI Security Standards Council

- Generic:
    - [CERT Security Improvement Modules: Securing Public Web Servers](https://resources.sei.cmu.edu/asset_files/SecurityImprovementModule/2000_006_001_13637.pdf)
