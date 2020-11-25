# Test RIA Cross Domain Policy

|ID          |
|------------|
|WSTG-CONF-08|

## Summary

Rich Internet Applications (RIA) have adopted Adobe's crossdomain.xml policy files to allow for controlled cross domain access to data and service consumption using technologies such as Oracle Java, Silverlight, and Adobe Flash. Therefore, a domain can grant remote access to its services from a different domain. However, often the policy files that describe the access restrictions are poorly configured. Poor configuration of the policy files enables Cross-site Request Forgery attacks, and may allow third parties to access sensitive data meant for the user.

### What are cross-domain policy files?

A cross-domain policy file specifies the permissions that a web client such as Java, Adobe Flash, Adobe Reader, etc. use to access data across different domains. For Silverlight, Microsoft adopted a subset of the Adobe's crossdomain.xml, and additionally created it's own cross-domain policy file: clientaccesspolicy.xml.

Whenever a web client detects that a resource has to be requested from other domain, it will first look for a policy file in the target domain to determine if performing cross-domain requests, including headers, and socket-based connections are allowed.

Master policy files are located at the domain's root. A client may be instructed to load a different policy file but it will always check the master policy file first to ensure that the master policy file permits the requested policy file.

#### Crossdomain.xml vs. Clientaccesspolicy.xml

Most RIA applications support crossdomain.xml. However in the case of Silverlight, it will only work if the crossdomain.xml specifies that access is allowed from any domain. For more granular control with Silverlight, clientaccesspolicy.xml must be used.

Policy files grant several types of permissions:

- Accepted policy files (Master policy files can disable or restrict specific policy files)
- Sockets permissions
- Header permissions
- HTTP/HTTPS access permissions
- Allowing access based on cryptographic credentials

An example of an overly permissive policy file:

```xml
<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM
"http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
    <site-control permitted-cross-domain-policies="all"/>
    <allow-access-from domain="*" secure="false"/>
    <allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>
```

### How can cross domain policy files can be abused?

- Overly permissive cross-domain policies.
- Generating server responses that may be treated as cross-domain policy files.
- Using file upload functionality to upload files that may be treated as cross-domain policy files.

### Impact of Abusing Cross-Domain Access

- Defeat CSRF protections.
- Read data restricted or otherwise protected by cross-origin policies.

## Test Objectives

- Review and validate the policy files.

## How to Test

### Testing for RIA Policy Files Weakness

To test for RIA policy file weakness the tester should try to retrieve the policy files crossdomain.xml and clientaccesspolicy.xml from the application's root, and from every folder found.

For example, if the application's URL is `http://www.owasp.org`, the tester should try to download the files `http://www.owasp.org/crossdomain.xml` and `http://www.owasp.org/clientaccesspolicy.xml`.

After retrieving all the policy files, the permissions allowed should be be checked under the least privilege principle. Requests should only come from the domains, ports, or protocols that are necessary. Overly permissive policies should be avoided. Policies with `*` in them should be closely examined.

#### Example

```xml
<cross-domain-policy>
    <allow-access-from domain="*" />
</cross-domain-policy>
```

##### Result Expected

- A list of policy files found.
- A list of weak settings in the policies.

## Tools

- Nikto
- OWASP Zed Attack Proxy Project
- W3af

## References

- Adobe: ["Cross-domain policy file specification"](http://www.adobe.com/devnet/articles/crossdomain_policy_file_spec.html)
- Adobe: ["Cross-domain policy file usage recommendations for Flash Player"](http://www.adobe.com/devnet/flashplayer/articles/cross_domain_policy.html)
- Oracle: ["Cross-Domain XML Support"](http://www.oracle.com/technetwork/java/javase/plugin2-142482.html#CROSSDOMAINXML)
- MSDN: ["Making a Service Available Across Domain Boundaries"](http://msdn.microsoft.com/en-us/library/cc197955(v=vs.95).aspx)
- MSDN: ["Network Security Access Restrictions in Silverlight"](http://msdn.microsoft.com/en-us/library/cc645032(v=vs.95).aspx)
- Stefan Esser: ["Poking new holes with Flash Crossdomain Policy Files"](http://www.hardened-php.net/library/poking_new_holes_with_flash_crossdomain_policy_files.html)
- Jeremiah Grossman: ["Crossdomain.xml Invites Cross-site Mayhem"](http://jeremiahgrossman.blogspot.com/2008/05/crossdomainxml-invites-cross-site.html)
- Google Doctype: ["Introduction to Flash security"](http://code.google.com/p/doctype-mirror/wiki/ArticleFlashSecurity)
- UCSD: [Analyzing the Crossdomain Policies of Flash Applications](http://cseweb.ucsd.edu/~hovav/dist/crossdomain.pdf)
