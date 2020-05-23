# Test HTTP Methods

|ID          |
|------------|
|WSTG-CONF-06|

## Summary

HTTP offers a number of methods that can be used to perform actions on the web server (the HTTP 1.1 standard refers to them as `methods` but they are also commonly described as `verbs`). While GET and POST are by far the most common methods that are used to access information provided by a web server, HTTP allows several other (and somewhat less known) methods. Some of these can be used for nefarious purposes if the web server is misconfigured.

[RFC 7231 –  Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content](https://tools.ietf.org/html/rfc7231) defines the following valid HTTP request methods, or verbs:

- [`GET`](https://tools.ietf.org/html/rfc7231#section-4.3.1)
- [`HEAD`](https://tools.ietf.org/html/rfc7231#section-4.3.2)
- [`POST`](https://tools.ietf.org/html/rfc7231#section-4.3.3)
- [`PUT`](https://tools.ietf.org/html/rfc7231#section-4.3.4)
- [`DELETE`](https://tools.ietf.org/html/rfc7231#section-4.3.5)
- [`CONNECT`](https://tools.ietf.org/html/rfc7231#section-4.3.6)
- [`OPTIONS`](https://tools.ietf.org/html/rfc7231#section-4.3.7)
- [`TRACE`](https://tools.ietf.org/html/rfc7231#section-4.3.8)

However, most web applications only need to respond to GET and POST requests, receiving user data in the URL query string or appended to the request respectively. The standard `<a href=""></a>` style links as well as forms defined wihtout a method trigger a GET request; form data submitted via `<form method='POST'></form>` trigger POST requests. JavaScript and AJAX calls may send methods other than GET and POST but should usally not need to do that. If an application has to accept other methods, e.g. when implementing a RESTful Web Service, test it thoroughly to make sure that all endpoints only accept the methods that they require and that attacks such as Cross-Site Tracing (XST) are not possible.

Also, verify that the web application authenticates and authorizes all requests regardless of request method, e.g. if a GET request for an endpoint requires authentication and authorization then a POST request to the same endpoint should typically also require authentication and authorization and so should typically a HEAD request as well.

## How to Test

### Discover the Supported Methods

To perform this test, the tester needs some way to figure out which HTTP methods are supported by the web server that is being examined. While the OPTIONS HTTP method provides a direct way to do that, use a tool such as the http-methods nmap script to verify the servers response to the OPTIONS request.

To use the http-methods nmap script to test the endpoint `/admin` on the server `localhost` using HTTPs, issue the command `nmap -p 443 --script http-methods --script-args http-methods.url-path='/index.php' localhost`

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

### Testing for Access Control Bypass

Find a page to visit that has a security constraint such that a GET request would normally force a 302 redirect to a log in page or force a log in directly. Issue requests using various methods such as HEAD, POST, PUT etc. as well as arbitrarily made up methods such as BILBAO, FOOBAR, CATS etc., if the web application responds with a `HTTP/1.1 200 OK` that is not a login page, it may be possible to bypass authentication and/or authorization. The following example uses netcat, to test web applications using HTTPs, substitute netcat for another tool such as NMAPs `ncat`.

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

If the system appears vulnerable, issue CSRF-like attacks such as the following to exploit the issue more fully:

- HEAD /admin/createUser.php?member=myAdmin
- PUT /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
- CATS /admin/groupEdit.php?group=Admins&member=myAdmin&action=add

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
- [w3af plugin htaccess_methods](http://w3af.org/plugins/audit/htaccess_methods)

## References

### Whitepapers

- [RFC 2109](https://tools.ietf.org/html/rfc2109) and [RFC 2965](https://tools.ietf.org/html/rfc2965): “HTTP State Management Mechanism”
- [HTACCESS: BILBAO Method Exposed](https://web.archive.org/web/20160616172703/http://www.kernelpanik.org/docs/kernelpanik/bme.eng.pdf)
- [Jeremiah Grossman: “Cross Site Tracing (XST)](https://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf)
- [Amit Klein: “XS(T) attack variants which can, in some cases, eliminate the need for TRACE”](https://www.securityfocus.com/archive/107/308433)
- [Fortify - Misused HTTP Method Override](https://vulncat.fortify.com/en/detail?id=desc.dynamic.xtended_preview.often_misused_http_method_override)
