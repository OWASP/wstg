# Test Application Platform Configuration

|ID          |
|------------|
|WSTG-CONF-02|

## Summary

Proper configuration of the single elements that make up an application architecture is important in order to prevent mistakes that might compromise the security of the whole architecture.

Configuration review and testing is a critical task in creating and maintaining an architecture. This is because many different systems will be usually provided with generic configurations that might not be suited to the task they will perform on the specific site they're installed on.

While the typical web and application server installation will contain a lot of functionality (like application examples, documentation, test pages) what is not essential should be removed before deployment to avoid post-install exploitation.

## Test Objectives

- Ensure that defaults and known files have been removed.
- Validate that no debugging code or extensions are left in the production environments.
- Review the logging mechanisms set in place for the application.

## How to Test

### Black-Box Testing

#### Sample and Known Files and Directories

Many web servers and application servers provide, in a default installation, sample applications and files for the benefit of the developer and in order to test that the server is working properly right after installation. However, many default web server applications have been later known to be vulnerable. This was the case, for example, for CVE-1999-0449 (Denial of Service in IIS when the Exair sample site had been installed), CAN-2002-1744 (Directory traversal vulnerability in CodeBrws.asp in Microsoft IIS 5.0), CAN-2002-1630 (Use of sendmail.jsp in Oracle 9iAS), or CAN-2003-1172 (Directory traversal in the view-source sample in Apache’s Cocoon).

CGI scanners include a detailed list of known files and directory samples that are provided by different web or application servers and might be a fast way to determine if these files are present. However, the only way to be really sure is to do a full review of the contents of the web server or application server and determine of whether they are related to the application itself or not.

#### Comment Review

It is very common for programmers to add comments when developing large web-based applications. However, comments included inline in HTML code might reveal internal information that should not be available to an attacker. Sometimes, even source code is commented out since a functionality is no longer required, but this comment is leaked out to the HTML pages returned to the users unintentionally.

Comment review should be done in order to determine if any information is being leaked through comments. This review can only be thoroughly done through an analysis of the web server static and dynamic content and through file searches. It can be useful to browse the site either in an automatic or guided fashion and store all the content retrieved. This retrieved content can then be searched in order to analyse any HTML comments available in the code.

#### System Configuration

Various tools, documents, or checklists can be used to give IT and security professionals a detailed assessment of target systems' conformance to various configuration baselines or benchmarks. Such tools include (but are not limited to):

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
- Never grant non-administrative identities (with the exception of `NT SERVICE\WMSvc`) access to applicationHost.config, redirection.config, and administration.config (either Read or Write access). This includes `Network Service`, `IIS_IUSRS`, `IUSR`, or any custom identity used by IIS application pools. IIS worker processes are not meant to access any of these files directly.
- Never share out applicationHost.config, redirection.config, and administration.config on the network. When using Shared Configuration, prefer to export applicationHost.config to another location (see the section titled "Setting Permissions for Shared Configuration).
- Keep in mind that all users can read .NET Framework `machine.config` and root `web.config` files by default. Do not store sensitive information in these files if it should be for administrator eyes only.
- Encrypt sensitive information that should be read by the IIS worker processes only and not by other users on the machine.
- Do not grant Write access to the identity that the Web server uses to access the shared `applicationHost.config`. This identity should have only Read access.
- Use a separate identity to publish applicationHost.config to the share. Do not use this identity for configuring access to the shared configuration on the Web servers.
- Use a strong password when exporting the encryption keys for use with shared -configuration.
- Maintain restricted access to the share containing the shared configuration and encryption keys. If this share is compromised, an attacker will be able to read and write any IIS configuration for your Web servers, redirect traffic from your Web site to malicious sources, and in some cases gain control of all web servers by loading arbitrary code into IIS worker processes.
- Consider protecting this share with firewall rules and IPsec policies to allow only the member web servers to connect.

#### Logging

Logging is an important asset of the security of an application architecture, since it can be used to detect flaws in applications (users constantly trying to retrieve a file that does not really exist) as well as sustained attacks from rogue users. Logs are typically properly generated by web and other server software. It is not common to find applications that properly log their actions to a log and, when they do, the main intention of the application logs is to produce debugging output that could be used by the programmer to analyze a particular error.

In both cases (server and application logs) several issues should be tested and analyzed based on the log contents:

1. Do the logs contain sensitive information?
2. Are the logs stored in a dedicated server?
3. Can log usage generate a Denial of Service condition?
4. How are they rotated? Are logs kept for the sufficient time?
5. How are logs reviewed? Can administrators use these reviews to detect targeted attacks?
6. How are log backups preserved?
7. Is the data being logged data validated (min/max length, chars etc) prior to being logged?

##### Sensitive Information in Logs

Some applications might, for example, use GET requests to forward form data which will be seen in the server logs. This means that server logs might contain sensitive information (such as usernames as passwords, or bank account details). This sensitive information can be misused by an attacker if they obtained the logs, for example, through administrative interfaces or known web server vulnerabilities or misconfiguration (like the well-known `server-status` misconfiguration in Apache-based HTTP servers).

Event logs will often contain data that is useful to an attacker (information leakage) or can be used directly in exploits:

- Debug information
- Stack traces
- Usernames
- System component names
- Internal IP addresses
- Less sensitive personal data (e.g. email addresses, postal addresses and telephone numbers associated with named individuals)
- Business data

Also, in some jurisdictions, storing some sensitive information in log files, such as personal data, might oblige the enterprise to apply the data protection laws that they would apply to their back-end databases to log files too. And failure to do so, even unknowingly, might carry penalties under the data protection laws that apply.

A wider list of sensitive information is:

- Application source code
- Session identification values
- Access tokens
- Sensitive personal data and some forms of personally identifiable information (PII)
- Authentication passwords
- Database connection strings
- Encryption keys
- Bank account or payment card holder data
- Data of a higher security classification than the logging system is allowed to store
- Commercially-sensitive information
- Information it is illegal to collect in the relevant jurisdiction
- Information a user has opted out of collection, or not consented to e.g. use of do not track, or where consent to collect has expired

#### Log Location

Typically servers will generate local logs of their actions and errors, consuming the disk of the system the server is running on. However, if the server is compromised its logs can be wiped out by the intruder to clean up all the traces of its attack and methods. If this were to happen the system administrator would have no knowledge of how the attack occurred or where the attack source was located. Actually, most attacker tool kits include a ''log zapper '' that is capable of cleaning up any logs that hold given information (like the IP address of the attacker) and are routinely used in attacker’s system-level root kits.

Consequently, it is wiser to keep logs in a separate location and not in the web server itself. This also makes it easier to aggregate logs from different sources that refer to the same application (such as those of a web server farm) and it also makes it easier to do log analysis (which can be CPU intensive) without affecting the server itself.

#### Log Storage

Logs can introduce a Denial of Service condition if they are not properly stored. Any attacker with sufficient resources could be able to produce a sufficient number of requests that would fill up the allocated space to log files, if they are not specifically prevented from doing so. However, if the server is not properly configured, the log files will be stored in the same disk partition as the one used for the operating system software or the application itself. This means that if the disk were to be filled up the operating system or the application might fail because it is unable to write on disk.

Typically in UNIX systems logs will be located in /var (although some server installations might reside in /opt or /usr/local) and it is important to make sure that the directories in which logs are stored are in a separate partition. In some cases, and in order to prevent the system logs from being affected, the log directory of the server software itself (such as /var/log/apache in the Apache web server) should be stored in a dedicated partition.

This is not to say that logs should be allowed to grow to fill up the file system they reside in. Growth of server logs should be monitored in order to detect this condition since it may be indicative of an attack.

Testing this condition is as easy, and as dangerous in production environments, as firing off a sufficient and sustained number of requests to see if these requests are logged and if there is a possibility to fill up the log partition through these requests. In some environments where QUERY_STRING parameters are also logged regardless of whether they are produced through GET or POST requests, big queries can be simulated that will fill up the logs faster since, typically, a single request will cause only a small amount of data to be logged, such as date and time, source IP address, URI request, and server result.

#### Log Rotation

Most servers (but few custom applications) will rotate logs in order to prevent them from filling up the file system they reside on. The assumption when rotating logs is that the information in them is only necessary for a limited amount of time.

This feature should be tested in order to ensure that:

- Logs are kept for the time defined in the security policy, not more and not less.
- Logs are compressed once rotated (this is a convenience, since it will mean that more logs will be stored for the same available disk space).
- File system permission of rotated log files are the same (or stricter) that those of the log files itself. For example, web servers will need to write to the logs they use but they don’t actually need to write to rotated logs, which means that the permissions of the files can be changed upon rotation to prevent the web server process from modifying these.

Some servers might rotate logs when they reach a given size. If this happens, it must be ensured that an attacker cannot force logs to rotate in order to hide his tracks.

#### Log Access Control

Event log information should never be visible to end users. Even web administrators should not be able to see such logs since it breaks separation of duty controls. Ensure that any access control schema that is used to protect access to raw logs and any applications providing capabilities to view or search the logs is not linked with access control schemas for other application user roles. Neither should any log data be viewable by unauthenticated users.

#### Log Review

Review of logs can be used for more than extraction of usage statistics of files in the web servers (which is typically what most log-based application will focus on), but also to determine if attacks take place at the web server.

In order to analyze web server attacks the error log files of the server need to be analyzed. Review should concentrate on:

- 40x (not found) error messages. A large amount of these from the same source might be indicative of a CGI scanner tool being used against the web server
- 50x (server error) messages. These can be an indication of an attacker abusing parts of the application which fail unexpectedly. For example, the first phases of a SQL injection attack will produce these error message when the SQL query is not properly constructed and its execution fails on the back end database.

Log statistics or analysis should not be generated, nor stored, in the same server that produces the logs. Otherwise, an attacker might, through a web server vulnerability or improper configuration, gain access to them and retrieve similar information as would be disclosed by log files themselves.

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
    - Secure Internet Information Services 5 Checklist, by Michael Howard, Microsoft Corporation, June 2000
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
