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

## Test Objectives

- Enumerate supported HTTP methods.
- Test for access control bypass.
- Test HTTP method overriding techniques.

## How to Test

### Discover the Supported Methods

To perform this test, the tester needs some way to figure out which HTTP methods are supported by the web server that is being examined. While the `OPTIONS` HTTP method provides a direct way to do that, verify the server's response by issuing requests using different methods. This can be achieved by manual testing or something like the [`http-methods`](https://nmap.org/nsedoc/scripts/http-methods.html) Nmap script.

To use the `http-methods` Nmap script to test the endpoint `/index.php` on the server `localhost` using HTTPS, issue the command:

```bash
nmap -p 443 --script http-methods --script-args http-methods.url-path='/index.php' localhost
```

When testing an application that has to accept other methods, e.g. a RESTful Web Service, test it thoroughly to make sure that all endpoints accept only the methods that they require.

#### Testing the PUT Method

1. Capture the base request of the target with a web proxy.
2. Change the request method to `PUT` and add `test.html` file and send the request to the application server.

   ```html
   PUT /test.html HTTP/1.1
   Host: testing-website

   <html>
   HTTP PUT Method is Enabled
   </html>
   ```

3. If the server response with 2XX success codes or 3XX redirections and then confirm by `GET` request for `test.html` file. The application is vulnerable.

If the HTTP `PUT` method is not allowed on base URL or request, try other paths in the system.

> NOTE: If you are successful in uploading a web shell you should overwrite it or ensure that the security team of the target are aware and remove the component promptly after your proof-of-concept.

Leveraging the `PUT` method an attacker may be able to place arbitrary and potentially malicious content, into the system which may lead to remote code execution, defacing the site or denial of service.

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

Some web frameworks provide a way to override the actual HTTP method in the request by emulating the missing HTTP verbs passing some custom header in the requests. The main purpose of this is to circumvent some middleware (e.g. proxy, firewall) limitation where methods allowed usually do not encompass verbs such as `PUT` or `DELETE`. The following alternative headers could be used to do such verb tunneling:

- `X-HTTP-Method`
- `X-HTTP-Method-Override`
- `X-Method-Override`

In order to test this, in the scenarios where restricted verbs such as PUT or DELETE return a "405 Method not allowed", replay the same request with the addition of the alternative headers for HTTP method overriding, and observe how the system responds. The application should respond with a different status code (*e.g.* 200) in cases where method overriding is supported.

The web server in the following example does not allow the `DELETE` method and blocks it:

```bash
$ ncat www.example.com 80
DELETE /resource.html HTTP/1.1
Host: www.example.com

HTTP/1.1 405 Method Not Allowed
Date: Sat, 04 Apr 2020 18:26:53 GMT
Server: Apache
Allow: GET,HEAD,POST,OPTIONS
Content-Length: 320
Content-Type: text/html; charset=iso-8859-1
Vary: Accept-Encoding
```

After adding the `X-HTTP-Method` header, the server responds to the request with a 200:

```bash
$ ncat www.example.com 80
DELETE /resource.html HTTP/1.1
Host: www.example.com
X-HTTP-Method: DELETE

HTTP/1.1 200 OK
Date: Sat, 04 Apr 2020 19:26:01 GMT
Server: Apache
```

## Remediation

- Ensure that only the required methods are allowed, and that the allowed methods are properly configured.
- Ensure that no workarounds are implemented to bypass security measures implemented by user-agents, frameworks, or web servers.

## Tools

- [Ncat](https://nmap.org/ncat/)
- [cURL](https://curl.haxx.se/)
- [nmap http-methods NSE script](https://nmap.org/nsedoc/scripts/http-methods.html)

## References

- [RFC 2109](https://tools.ietf.org/html/rfc2109) and [RFC 2965](https://tools.ietf.org/html/rfc2965): "HTTP State Management Mechanism"
- [HTACCESS: BILBAO Method Exposed](https://web.archive.org/web/20160616172703/http://www.kernelpanik.org/docs/kernelpanik/bme.eng.pdf)
- [Fortify - Misused HTTP Method Override](https://vulncat.fortify.com/en/detail?id=desc.dynamic.xtended_preview.often_misused_http_method_override)
