# Test HTTP Methods

|ID          |
|------------|
|WSTG-CONF-06|

## Summary

HTTP offers a number of methods (or verbs) that can be used to perform actions on the web server. While GET and POST are by far the most common methods that are used to access information provided by a web server, there are a variety of other methods that may also be supported, and can sometimes be exploited by attackers.

[RFC 7231](https://tools.ietf.org/html/rfc7231) defines the following valid HTTP request methods, or verbs. Several of these verbs have bee re-used for different purposes in [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) applications, listed in the table below.

| Method | Original Purpose | RESTful Purpose |
|--------|------------------|-----------------|
| [`GET`](https://tools.ietf.org/html/rfc7231#section-4.3.1) | Request a file. | Request an object.|
| [`HEAD`](https://tools.ietf.org/html/rfc7231#section-4.3.2) | Request a file, but only return the HTTP headers. | |
| [`POST`](https://tools.ietf.org/html/rfc7231#section-4.3.3) | Submit data. | |
| [`PUT`](https://tools.ietf.org/html/rfc7231#section-4.3.4) | Upload a file. | Create an object. 
| [`DELETE`](https://tools.ietf.org/html/rfc7231#section-4.3.5) | Delete a file | Delete an object. |
| [`CONNECT`](https://tools.ietf.org/html/rfc7231#section-4.3.6) | Establish a connection to another system. | |
| [`OPTIONS`](https://tools.ietf.org/html/rfc7231#section-4.3.7) | List supported HTTP methods. | Perform a [CORS Preflight](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request) request.
| [`TRACE`](https://tools.ietf.org/html/rfc7231#section-4.3.8) | Echo the HTTP request for debug purposes. | | 

## Test Objectives

- Enumerate supported HTTP methods.
- Test for access control bypass.
- Test HTTP method overriding techniques.

## How to Test

### Discover the Supported Methods

To perform this test, the tester needs some way to identify which HTTP methods are supported by the web server that is being examined. The simplest way to do this is to make an `OPTIONS` request to the server:

```http
OPTIONS / HTTP/1.1
Host: example.org
```
The server should then response with a list of supported methods:

```http
HTTP/1.1 200 OK
Allow: OPTIONS, GET, HEAD, POST
```

However, some servers may not respond to `OPTIONS` requests, or may return inaccurate information. Additionally, servers may support different methods for different paths - so just because a method is not supported for the root `/` directory, this doesn't necessarily mean that it won't be supported elsewhere.

An alternatively way to test for supported methods is to simply make a request with that method type, and examine the server response. If the method is not permitted, the server should return a `405 Method Not Allowed` status.

Note that some servers treat unknown methods as equivalent to `GET`, so they may response to arbitrary methods, such as the request shown below. This can occasionally be useful to evade a web application firewall, or any other filtering that blocks specific methods.

```http
FOO / HTTP/1.1
Host: example.org
```

Requests with arbitrary methods can also be made using cURL with the `-X` option:

```bash
curl -X FOO https://example.org
```

There are also a variety of automated tools that can attempt to determine supported methods, such as the [`http-methods`](https://nmap.org/nsedoc/scripts/http-methods.html) Nmap script. However, these tools may not test for dangerous methods (such as `PUT` or `DELETE`), or may unintentionally cause changes to the web server if this methods are supported. As such, they should be used with care.

### PUT and DELETE

The `PUT` and `DELETE` methods can have different effects, depending on whether they are being interpreted by the web server or by the application running on it.

#### Legacy Web Servers

Some legacy web servers allowed the use of the `PUT` method to create files on the server. For example, if the server is configured to allow this, the request below would create a file on the server called `test.html` with the contents `<script>alert(1)</script>`.

```http
PUT /test.html HTTP/1.1
Host: example.org
Content-Length: 25

<script>alert(1)</script>
```

Similar requests can also be made with cURL:

```bash
curl https://example.org --upload-file test.html
```

This allows an attacker to upload arbitrary files to the webserver, which could potential result in a full system compromise if they are allowed to upload executable code such as PHP files. However, this configuration is extremely rare, and is unlikely to be seen on any modern systems.

Similarly, the `DELETE` method can be used to delete files from the webserver. Note that this is a **destructive action**, so care should be taken when testing this method.

```http
DELETE /test.html HTTP/1.1
Host: example.org
```

Or with cURL

```bash
curl http://example.org/test.html -X DELETE
```

#### RESTful APIs

By contrast, the `PUT` and `DELETE` methods are commonly used by modern RESTful applications to create and delete objects. For example, the API request below could be use to create a widget called "mywidget" with a value of 10:

```http
PUT /api/widgets/mywidget HTTP/1.1
Host: example.org
Content-Length: 34

{"value":"10"}
```

A similar requests with the DELETE method could be used to delete an object.

```http
DELETE /api/widgets/mywidget HTTP/1.1
Host: example.org
```

Although it may be reported by automated scanning tools, the presence of these methods on a RESTful API **is not a security issue**. However, this functionality may have other vulnerabilities (such as weak access control), should be thoroughly tested.

### TRACE

The `TRACE` method causes the server to echo back the contents of the request. This lead to a vulnerability called Cross-Site Tracing (XST) being published in [2003](https://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf) (PDF), which could be used to access cookies that had the `HttpOnly` flag set. The `TRACE` method has been blocked in all browsers and plugins for many years, and as such this issue is no longer exploitable. However, it may still be flagged by automated scanning tools, and the `TRACE` method being enabled on a web server suggests that is has not been properly hardened.

### CONNECT

The `CONNECT` method causes the web server to open a TCP connection to another system, and then to pass traffic from the client through to that system. This could allow an attacker to proxy traffic through the server, in order to hide their source address, access internal systems or access services that are bound to localhost. An example of a CONNECT request is shown below:

```http
CONNECT 192.168.0.1:443 HTTP/1.1
Host: example.org
```

### Testing for Access Control Bypass

Find a page to visit that has a security constraint such that a GET request would normally force a 302 redirect to a log in page or force a log in directly. Issue requests using various methods such as HEAD, POST, PUT etc. as well as arbitrarily made up methods such as BILBAO, FOOBAR, CATS, etc. If the web application responds with a `HTTP/1.1 200 OK` that is not a log in page, it may be possible to bypass authentication or authorization. The following example uses [Nmap's `ncat`](https://nmap.org/ncat/).

```bash
$ ncat www.example.com 80
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

- `HEAD /admin/createUser.php?member=myAdmin`
- `PUT /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123`
- `CATS /admin/groupEdit.php?group=Admins&member=myAdmin&action=add`

Using the above three commands, modified to suit the application under test and testing requirements, a new user would be created, a password assigned, and the user made an administrator, all using blind request submission.

### Testing for HTTP Method Overriding

Some web frameworks provide a way to override the actual HTTP method in the request by emulating the missing HTTP verbs passing some custom header in the requests. The main purpose of this is to circumvent a middleware application (such as a proxy or web application firewall) which blocks specific methods. The following alternative HTTP headers could be used to do such verb tunneling:

- `X-HTTP-Method`
- `X-HTTP-Method-Override`
- `X-Method-Override`

In order to test this, in the scenarios where restricted verbs such as PUT or DELETE return a "405 Method not allowed", replay the same request with the addition of the alternative headers for HTTP method overriding, and observe how the system responds. The application should respond with a different status code (*e.g.* 200) in cases where method overriding is supported.

The web server in the following example does not allow the `DELETE` method and blocks it:

```http
DELETE /resource.html HTTP/1.1
Host: www.example.com

HTTP/1.1 405 Method Not Allowed
[...]
```

After adding the `X-HTTP-Method` header, the server responds to the request with a 200:

```http
GET /resource.html HTTP/1.1
Host: www.example.com
X-HTTP-Method: DELETE

HTTP/1.1 200 OK
[...]
```

## Remediation

- Ensure that only the required methods are allowed, and that the allowed methods are properly configured.
- Ensure that no workarounds are implemented to bypass security measures implemented by user-agents, frameworks, or web servers.

## Tools

- [Ncat](https://nmap.org/ncat/)
- [cURL](https://curl.haxx.se/)
- [Nmap http-methods NSE script](https://nmap.org/nsedoc/scripts/http-methods.html)

## References

- [RFC 7231 - Hypertext Transfer Protocol (HTTP/1.1)](https://tools.ietf.org/html/rfc7231)
- [HTACCESS: BILBAO Method Exposed](https://web.archive.org/web/20160616172703/http://www.kernelpanik.org/docs/kernelpanik/bme.eng.pdf)
- [Fortify - Misused HTTP Method Override](https://vulncat.fortify.com/en/detail?id=desc.dynamic.xtended_preview.often_misused_http_method_override)
