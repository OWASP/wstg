# Test HTTP Methods

|ID          |
|------------|
|WSTG-CONF-06|

## Summary

HTTP offers a number of methods that can be used to perform actions on the web server (the HTTP 1.1 standard refers to them as `methods` but they are also commonly described as `verbs`). Many of theses methods are designed to aid developers in deploying and testing HTTP applications. These HTTP methods can be used for nefarious purposes if the web server is misconfigured. Additionally, Cross Site Tracing (XST), a form of cross site scripting using the server's HTTP TRACE method, is examined.
While GET and POST are by far the most common methods that are used to access information provided by a web server, the Hypertext Transfer Protocol (HTTP) allows several other (and somewhat less known) methods.

The full [HTTP 1.1 specification](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) defines the following valid HTTP request methods, or verbs:

- [`OPTIONS`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.2)
- [`GET`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.3)
- [`HEAD`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.4)
- [`POST`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.5)
- [`PUT`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.6)
- [`DELETE`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7)
- [`TRACE`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.8)
- [`CONNECT`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.9)

If enabled, the Web Distributed Authoring and Version [(WebDAV)](http://www.webdav.org/specs/rfc2518.html) [extensions](https://tools.ietf.org/html/rfc4918) permit several more HTTP methods:

- [`PROPFIND`](http://www.webdav.org/specs/rfc2518.html#METHOD_PROPFIND)
- [`PROPPATCH`](http://www.webdav.org/specs/rfc2518.html#METHOD_PROPPATCH)
- [`MKCOL`](http://www.webdav.org/specs/rfc2518.html#METHOD_MKCOL)
- [`COPY`](http://www.webdav.org/specs/rfc2518.html#METHOD_COPY)
- [`MOVE`](http://www.webdav.org/specs/rfc2518.html#METHOD_MOVE)
- [`LOCK`](http://www.webdav.org/specs/rfc2518.html#METHOD_LOCK)
- [`UNLOCK`](http://www.webdav.org/specs/rfc2518.html#METHOD_UNLOCK)

However, most web applications only need to respond to GET and POST requests, providing user data in the URL query string or appended to the request respectively. The standard `<a href=""></a>` style links trigger a GET request; form data submitted via
`<form method='POST'></form>`trigger POST requests. Forms defined without a method also send data via GET by default.

Oddly, the other valid HTTP methods (mentioned earlier) are not supported by the [HTML standard](https://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13.1). Any HTTP method other than GET or POST needs to be called outside the HTML document. However, JavaScript and AJAX calls may send methods other than GET and POST. For this reason, most web applications should not need to accept other HTTP methods.

If an application has to accept other methods, e.g. when implementing a RESTful Web Service, test it thoroughly to make sure that all endpoints only accept the methods that they require, and that all requests regardless of method are properly authenticated and authorized.

### Arbitrary HTTP Methods

Arshan Dabirsiaghi (see links) discovered that many web application frameworks allowed well chosen or arbitrary HTTP methods to bypass an environment level access control check:

- Many frameworks and languages treat “HEAD” as a “GET” request, albeit one without any body in the response. If a security constraint was set on “GET” requests such that only “authenticatedUsers” could access GET requests for a particular servlet or resource, it would be bypassed for the “HEAD” version. This allowed unauthorized blind submission of any privileged GET request.

- Some frameworks allowed arbitrary HTTP methods such as “JEFF” or “CATS” to be used without limitation. These were treated as if a “GET” method was issued, and were found not to be subject to method role based access control checks on a number of languages and frameworks, again allowing unauthorized blind submission of privileged GET requests.

In many cases, code which explicitly checked for a “GET” or “POST” method would be safe.

## How to Test

### Discover the Supported Methods

To perform this test, the tester needs some way to figure out which HTTP methods are supported by the web server that is being examined. The OPTIONS HTTP method provides the tester with the most direct and effective way to do that. RFC 2616 states that, “The OPTIONS method represents a request for information about the communication options available on the request/response chain identified by the Request-URI”.

The testing method is extremely straightforward and we only need to fire up netcat (or telnet):

```bash
$ nc www.victim.com 80
OPTIONS / HTTP/1.1
Host: www.victim.com

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Date: Tue, 31 Oct 2006 08:00:29 GMT
Connection: close
Allow: GET, HEAD, POST, TRACE, OPTIONS
Content-Length: 0
```

As we can see in the example, OPTIONS provides a list of the methods that are supported by the web server, and in this case we can see that TRACE method is enabled. The danger that is posed by this method is illustrated in the following section

The same test can also be executed using nmap and the http-methods NSE script:

```console
C:\Tools\nmap-6.40>nmap -p 443 --script http-methods localhost

Starting Nmap 6.40 ( http://nmap.org ) at 2015-11-04 11:52 Romance Standard Time

Nmap scan report for localhost (127.0.0.1)
Host is up (0.0094s latency).
PORT    STATE SERVICE
443/tcp open  https
| http-methods: OPTIONS TRACE GET HEAD POST
| Potentially risky methods: TRACE
|_See http://nmap.org/nsedoc/scripts/http-methods.html

Nmap done: 1 IP address (1 host up) scanned in 20.48 seconds
```

### Test XST Potential

Note: in order to understand the logic and the goals of this attack one must be familiar with [Cross Site Scripting attacks](https://owasp.org/www-community/attacks/xss/).

The TRACE method, while apparently harmless, can be successfully leveraged in some scenarios to steal legitimate users' credentials. This attack technique was discovered by Jeremiah Grossman in 2003, in an attempt to bypass the [HTTPOnly](https://owasp.org/www-community/HttpOnly) tag that Microsoft introduced in Internet Explorer 6 SP1 to protect cookies from being accessed by JavaScript. As a matter of fact, one of the most recurring attack patterns in Cross Site Scripting is to access the document.cookie object and send it to a web server controlled by the attacker so that he or she can hijack the victim's session. Tagging a cookie as httpOnly forbids JavaScript from accessing it, protecting it from being sent to a third party. However, the TRACE method can be used to bypass this protection and access the cookie even in this scenario.

As mentioned before, TRACE simply returns any string that is sent to the web server. In order to verify its presence (or to double-check the results of the OPTIONS request shown above), the tester can proceed as shown in the following example:

```bash
$ nc www.victim.com 80
TRACE / HTTP/1.1
Host: www.victim.com

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Date: Tue, 31 Oct 2006 08:01:48 GMT
Connection: close
Content-Type: message/http
Content-Length: 39

TRACE / HTTP/1.1
Host: www.victim.com
```

The response body is exactly a copy of our original request, meaning that the target allows this method. Now, where is the danger lurking? If the tester instructs a browser to issue a TRACE request to the web server, and this browser has a cookie for that domain, the cookie will be automatically included in the request headers, and will therefore be echoed back in the resulting response. At that point, the cookie string will be accessible by JavaScript and it will be finally possible to send it to a third party even when the cookie is tagged as httpOnly.

There are multiple ways to make a browser issue a TRACE request, such as the XMLHTTP ActiveX control in Internet Explorer and XMLDOM in Mozilla and Netscape. However, for security reasons the browser is allowed to start a connection only to the domain where the hostile script resides. This is a mitigating factor, as the attacker needs to combine the TRACE method with another vulnerability in order to mount the attack.

An attacker has two ways to successfully launch a Cross Site Tracing attack:

- Leveraging another server-side vulnerability: the attacker injects the hostile JavaScript snippet that contains the TRACE request in the vulnerable application, as in a normal Cross Site Scripting attack
- Leveraging a client-side vulnerability: the attacker creates a malicious website that contains the hostile JavaScript snippet and exploits some cross-domain vulnerability of the browser of the victim, in order to make the JavaScript code successfully perform a connection to the site that supports the TRACE method and that originated the cookie that the attacker is trying to steal.

More detailed information, together with code samples, can be found in the original whitepaper written by Jeremiah Grossman.

### Testing for Arbitrary HTTP Methods

Find a page to visit that has a security constraint such that it would normally force a 302 redirect to a log in page or forces a log in directly. The test URL in this example works like this, as do many web applications. However, if a tester obtains a “200” response that is not a log in page, it is possible to bypass authentication and thus authorization.

```bash
$ nc www.example.com 80
JEFF / HTTP/1.1
Host: www.example.com

HTTP/1.1 200 OK
Date: Mon, 18 Aug 2008 22:38:40 GMT
Server: Apache
Set-Cookie: PHPSESSID=K53QW...
```

If the framework or firewall or application does not support the “JEFF” method, it should issue an error page (or preferably a 405 Not Allowed or 501 Not implemented error page). If it services the request, it is vulnerable to this issue.

If the tester feels that the system is vulnerable to this issue, they should issue CSRF-like attacks to exploit the issue more fully:

- FOOBAR /admin/createUser.php?member=myAdmin
- JEFF /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
- CATS /admin/groupEdit.php?group=Admins&member=myAdmin&action=add

With some luck, using the above three commands - modified to suit the application under test and testing requirements - a new user would be created, a password assigned, and made an administrator.

### Testing for HEAD Access Control Bypass

Find a page to visit that has a security constraint such that it would normally force a 302 redirect to a log in page or forces a log in directly. The test URL in this example works like this, as do many web applications. However, if the tester obtains a “200” response that is not a login page, it is possible to bypass authentication and thus authorization.

```bash
$ nc www.example.com 80
HEAD /admin HTTP/1.1
Host: www.example.com

HTTP/1.1 200 OK
Date: Mon, 18 Aug 2008 22:44:11 GMT
Server: Apache
Set-Cookie: PHPSESSID=pKi...; path=/; HttpOnly
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Set-Cookie: adminOnlyCookie1=...; expires=Tue, 18-Aug-2009 22:44:31 GMT; domain=www.example.com
Set-Cookie: adminOnlyCookie2=...; expires=Mon, 18-Aug-2008 22:54:31 GMT; domain=www.example.com
Set-Cookie: adminOnlyCookie3=...; expires=Sun, 19-Aug-2007 22:44:30 GMT; domain=www.example.com
Content-Language: EN
Connection: close
Content-Type: text/html; charset=ISO-8859-1
```

If the tester gets a “405 Method not allowed” or “501 Method Unimplemented”, the target (application/framework/language/system/firewall) is working correctly. If a “200” response code comes back, and the response contains no body, it's likely that the application has processed the request without authentication or authorization and further testing is warranted.

If the tester thinks that the system is vulnerable to this issue, they should issue CSRF-like attacks to exploit the issue more fully:

- HEAD /admin/createUser.php?member=myAdmin
- HEAD /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
- HEAD /admin/groupEdit.php?group=Admins&member=myAdmin&action=add

With some luck, using the above three commands - modified to suit the application under test and testing requirements - a new user would be created, a password assigned, and made an administrator, all using blind request submission.

### Testing for HTTP Method Overriding

Some web frameworks provide a way to override the actual HTTP method in the request by emulating the missing HTTP verbs passing some custom header in the requests. The main purpose of this is to circumvent some middleware (e.g. proxy, firewall) limitation where methods allowed usually do not encompass verbs such as `PUT` or `DELETE`. The following alternative headers could be used to do such verb tunneling:

- `X-HTTP-Method`
- `X-HTTP-Method-Override`
- `X-Method-Override`

In order to test this, in the scenarios where restrictive verbs such as PUT or DELETE return a “405 Method not allowed”, replay the same request with the addition of the alternative headers for HTTP method overriding, and observe how the system will respond. The application should respond with a different status code (e.g. 200) in cases where method overriding is supported:

```bash
$ nc www.example.com 80
DELETE /resource.html HTTP/1.1
Host: www.example.com

HTTP/1.1 405 Method Not Allowed
Date: Sat, 04 Apr 2020 18:26:53 GMT
Server: Apache
Allow: GET,HEAD,POST,OPTIONS
Content-Length: 320
Content-Type: text/html; charset=iso-8859-1
Vary: Accept-Encoding

$ nc www.example.com 80
DELETE /resource.html HTTP/1.1
Host: www.example.com
X-HTTP-Method: DELETE

HTTP/1.1 200 OK
Date: Sat, 04 Apr 2020 19:26:01 GMT
Server: Apache
```

## Tools

- [NetCat](http://nc110.sourceforge.net)
- [cURL](https://curl.haxx.se/)
- [nmap http-methods NSE script](https://nmap.org/nsedoc/scripts/http-methods.html)

## References

### Whitepapers

- [RFC 2616: “Hypertext Transfer Protocol -- HTTP/1.1”](https://tools.ietf.org/html/rfc2616)
- [RFC 2109](https://tools.ietf.org/html/rfc2109) and [RFC 2965](https://tools.ietf.org/html/rfc2965): “HTTP State Management Mechanism”
- [Arshan Dabirsiaghi: “Bypassing URL Authentication and Authorization with HTTP Verb Tampering”](https://web.archive.org/web/20081116154150/http://www.aspectsecurity.com/documents/Bypassing_VBAAC_with_HTTP_Verb_Tampering.pdf)
- [Jeremiah Grossman: “Cross Site Tracing (XST)](https://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf)
- [Amit Klein: “XS(T) attack variants which can, in some cases, eliminate the need for TRACE”](https://www.securityfocus.com/archive/107/308433)
- [Fortify - Misused HTTP Method Override](https://vulncat.fortify.com/en/detail?id=desc.dynamic.xtended_preview.often_misused_http_method_override)
