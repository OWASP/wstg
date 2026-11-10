# HTTP Request Smuggling

|ID          |
|------------|
|WSTG-INJT-16|

## Summary

HTTP Request Smuggling is a class of vulnerabilities caused by inconsistencies in how HTTP requests are parsed by frontend and backend components. When intermediaries such as reverse proxies, load balancers, or API gateways interpret request boundaries differently from backend servers, attackers may inject or "smuggle" hidden requests that are processed out of sequence.

Modern infrastructures significantly expand the attack surface by introducing HTTP/2, protocol downgrades (HTTP/2 → HTTP/1.1), and cleartext upgrades (H2C), where request normalization and translation logic frequently diverges from RFC expectations.

Request smuggling exploits arise when two or more HTTP parsers disagree on where a request begins or ends. Historically, this discrepancy was most commonly observed in conflicting interpretations of the `Content-Length` (CL) and `Transfer-Encoding` (TE) headers.

In modern architectures, additional desynchronization vectors emerge from:

- HTTP/2 to HTTP/1.1 translation layers
- Cleartext HTTP/2 (H2C) upgrade mechanisms
- Header normalization mismatches
- Reintroduced forbidden headers during protocol downgrade
- Connection reuse across protocol boundaries

These behaviors can lead to persistent desynchronization, cache poisoning, credential hijacking, and access control bypass.

## Test Objectives

- Identify request boundary inconsistencies between frontend and backend components
- Detect classic CL/TE desynchronization vulnerabilities
- Evaluate protocol translation logic (HTTP/2 → HTTP/1.1)
- Assess H2C upgrade handling and downgrade safety
- Identify endpoints that ignore the request body (CL.0) and whether a browser can be made to desynchronize its own connection
- Confirm backend request queue poisoning

## How to Test

### Black-Box Testing

#### CL.TE Desynchronization

In a CL.TE scenario, the frontend uses `Content-Length` to determine request size, while the backend honors `Transfer-Encoding`.

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 35
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```

Expected Result:

- Backend stops parsing at the `0` chunk
- Smuggled request remains buffered
- Subsequent legitimate requests are corrupted or return unexpected responses (e.g., 404)

#### TE.CL Desynchronization

In a TE.CL scenario, the frontend processes chunked encoding correctly, but the backend relies on `Content-Length`.

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 4
Transfer-Encoding: chunked

5c
GET /admin HTTP/1.1
Content-Length: 0

0
```

Expected Result:

- Backend stops early
- Remaining payload is interpreted as a new request
- Unauthorized endpoint access or request poisoning may occur

#### TE.TE (Obfuscated Transfer-Encoding)

If both servers support `Transfer-Encoding`, header obfuscation may cause one parser to ignore it.

Common techniques include:

- Whitespace manipulation
- Header duplication
- Non-standard separators

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 44
Transfer-Encoding:\tchunked
Transfer-Encoding: identity

0

GET /404 HTTP/1.1
Foo: bar
```

### Modern Attack Vectors

#### HTTP/2 to HTTP/1.1 Desynchronization

In many deployments, clients communicate with edge servers using HTTP/2, while backend services still operate over HTTP/1.1. During protocol translation, intermediaries must reconstruct HTTP/1.1 requests from HTTP/2 frames.

Common failure points include:

- Incorrect reconstruction of `Content-Length`
- Reintroduction of hop-by-hop headers
- Multiple logical requests collapsed into a single backend request

> Note: HTTP/2 downgrading is not inherently vulnerable by itself.  
> Exploitation becomes possible when protocol translation reconstructs an HTTP/1.1 request that violates backend parsing assumptions, leading to request boundary desynchronization.

Testing Approach:

- Send multiple HTTP/2 DATA frames with conflicting length semantics
- Observe backend behavior via timing discrepancies or response splitting
- Monitor for request queue poisoning

##### Example: HTTP/2 Downgrade Smuggling via Request Reconstruction

In this scenario, the client communicates with the frontend over HTTP/2, while the backend only supports HTTP/1.1. The intermediary reconstructs an HTTP/1.1 request from multiple HTTP/2 DATA frames.

**HTTP/2 (Conceptual Representation):**

- DATA frame 1:

```http
0\r\n\r\n
```

- DATA frame 2:

```http
GET /admin HTTP/1.1
Host: internal
```

**Reconstructed HTTP/1.1 Request (Backend View):**

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 0

GET /admin HTTP/1.1
Host: internal
```

If the frontend treats the request as complete while the backend continues parsing buffered data, the second request may be processed out of sequence, resulting in request smuggling.

> Implicit Downgrades:
> Even in the absence of an explicit `Upgrade: h2c` mechanism, many CDNs and reverse proxies silently downgrade HTTP/2 client connections to HTTP/1.1 when forwarding requests to backend services.  
> These implicit downgrades expand the smuggling attack surface, especially when combined with connection reuse and insufficient request normalization.

#### H2C Smuggling (Cleartext HTTP/2 Upgrade)

H2C allows upgrading an HTTP/1.1 connection to HTTP/2 using the `Upgrade: h2c` mechanism.  
Unlike protocol downgrades, H2C smuggling occurs during an in-place protocol transition, where frontend and backend components may temporarily disagree on the active parsing state of the same connection, potentially leaving residual bytes in the backend buffer.

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA

0

GET /admin HTTP/1.1
Host: internal
```

Risk Factors:

- Partial upgrade acceptance
- Backend continues parsing as HTTP/1.1
- Smuggled request processed post-upgrade

#### Request Queue Poisoning via Protocol Downgrade

Some proxies downgrade HTTP/2 requests to HTTP/1.1 but fail to fully sanitize:

- `Content-Length`
- Duplicated headers
- Invalid pseudo-header ordering

Attackers can exploit this to poison persistent backend connections, impacting multiple users.

#### CL.0 Desynchronization

Some backends ignore `Content-Length` on endpoints that don't expect a body, such as static files, redirects or health checks. They answer the request right away and treat its body as the start of the next request on the same connection, even when the frontend parsed the request correctly.

Send a request with a body to such an endpoint, followed by a normal request on the same connection. In Burp Suite Repeater, put both in a group and use "Send group in sequence (single connection)":

```http
POST /static/logo.png HTTP/1.1
Host: vulnerable-website.com
Content-Length: 30
Connection: keep-alive

GET /404 HTTP/1.1
X-Ignore: X
```

```http
GET / HTTP/1.1
Host: vulnerable-website.com
```

Expected Result:

- The second request gets the response for `GET /404` instead of the home page
- The behavior is specific to some endpoints, so try several: static files, redirects, server-level endpoints and error pages

#### Client-Side Desync

When the server that ignores the body is the one the browser talks to directly over HTTP/1.1, the victim's own browser can be made to send the desynchronizing request. A page on another site sends a cross-origin `POST` with the smuggled prefix as its body, then a second request that reuses the same connection:

```javascript
fetch('https://vulnerable-website.com/redirect-me', {
  method: 'POST',
  body: 'GET /404 HTTP/1.1\r\nX-Ignore: X',
  mode: 'cors',
  credentials: 'include',
}).catch(() => {
  fetch('https://vulnerable-website.com/', { mode: 'no-cors', credentials: 'include' });
});
```

Using `mode: 'cors'` against an endpoint that redirects makes the first fetch fail before the redirect is followed, so the browser keeps the connection and the second request is answered with the smuggled response.

To test:

1. Find an endpoint that ignores the body, as in the CL.0 test, on a host the browser reaches over HTTP/1.1 without a normalizing proxy in between.
2. Confirm the desync with two requests on a single connection in Burp Suite.
3. Reproduce it from a test page on another origin and check in the browser's developer tools whether the second request got the smuggled response.

If it works, the attacker controls a response in the victim's browser for the target origin, which can lead to stored XSS-like effects, cache poisoning in the browser, or capturing the victim's next request.

### Indicators of Vulnerability

- Inconsistent responses across identical requests
- Unexpected 404 or 400 responses
- Delayed or mismatched responses
- Cross-user response leakage

## Remediation

- Enforce strict RFC-compliant parsing
- Normalize request handling across all intermediaries
- Disable H2C where not required
- Avoid protocol downgrades on untrusted connections
- Terminate and revalidate backend connections upon parsing errors
- Make every endpoint either read or reject a request body it doesn't use, and close the connection when in doubt
- Use HTTP/2 end-to-end where possible, which removes most length ambiguity

## Tools

- [HTTP Request Smuggler (Burp Suite Extension)](https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646)
- [Smuggler (Python) by defparam](https://github.com/defparam/smuggler)
- [h2csmuggler by Bishop Fox](https://github.com/BishopFox/h2csmuggler)

## References

- [James Kettle, "HTTP Desync Attacks: Request Smuggling Reborn" (PortSwigger Research)](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)
- [James Kettle, "HTTP/2: The Sequel is Always Worse" (PortSwigger Research)](https://portswigger.net/research/http2)
- [James Kettle, "Browser-Powered Desync Attacks" (PortSwigger Research)](https://portswigger.net/research/browser-powered-desync-attacks)
- [Jake Miller, "h2c Smuggling: Request Smuggling Via HTTP/2 Cleartext" (Bishop Fox)](https://bishopfox.com/blog/h2c-smuggling-request)
- [Amit Klein, Chaim Linhart, Ronen Heled, Steve Orrin: "HTTP Request Smuggling" (2005)](https://web.archive.org/web/20210816212852/https://www.cgisecurity.com/lib/http-request-smuggling.pdf)
- [RFC 9112, Section 6.3: Message Body Length](https://datatracker.ietf.org/doc/html/rfc9112#section-6.3)
- [RFC 9113: HTTP/2](https://datatracker.ietf.org/doc/html/rfc9113)
