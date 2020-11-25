# Testing for Cookies Attributes

|ID          |
|------------|
|WSTG-SESS-02|

## Summary

Web Cookies (herein referred to as cookies) are often a key attack vector for malicious users (typically targeting other users) and the application should always take due diligence to protect cookies.

HTTP is a stateless protocol, meaning that it doesn't hold any reference to requests being sent by the same user. In order to fix this issue, sessions were created and appended to HTTP requests. Browsers, as discussed in [testing browser storage](../11-Client-side_Testing/12-Testing_Browser_Storage.md), contain a multitude of storage mechanisms. In that section of the guide, each is discussed thoroughly.

The most used session storage mechanism in browsers is cookie storage. Cookies can be set by the server, by including a [`Set-Cookie`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie) header in the HTTP response or via JavaScript. Cookies can be used for a multitude of reasons, such as:

- session management
- personalization
- tracking

In order to secure cookie data, the industry has developed means to help lock down these cookies and limit their attack surface. Over time cookies have become a preferred storage mechanism for web applications, as they allow great flexibility in use and protection.

The means to protect the cookies are:

- [Cookie Attributes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Creating_cookies)
- [Cookie Prefixes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Cookie_prefixes)

## Test Objectives

- Ensure that the proper security configuration is set for cookies.

## How to Test

Below, a description of every attribute and prefix will be discussed. The tester should validate that they are being used properly by the application. Cookies can be reviewed by using an [intercepting proxy](#intercepting-proxy), or by reviewing the browser's cookie jar.

### Cookie Attributes

#### Secure Attribute

The [`Secure`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#Secure) attribute tells the browser to only send the cookie if the request is being sent over a secure channel such as `HTTPS`. This will help protect the cookie from being passed in unencrypted requests. If the application can be accessed over both `HTTP` and `HTTPS`, an attacker could be able to redirect the user to send their cookie as part of non-protected requests.

#### HttpOnly Attribute

The [`HttpOnly`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#HttpOnly) attribute is used to help prevent attacks such as session leakage, since it does not allow the cookie to be accessed via a client-side script such as JavaScript.

> This doesn't limit the whole attack surface of XSS attacks, as an attacker could still send request in place of the user, but limits immensely the reach of XSS attack vectors.

#### Domain Attribute

The [`Domain`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Scope_of_cookies) attribute is used to compare the cookie's domain against the domain of the server for which the HTTP request is being made. If the domain matches or if it is a subdomain, then the [`path`](#path-attribute) attribute will be checked next.

Note that only hosts that belong to the specified domain can set a cookie for that domain. Additionally, the `domain` attribute cannot be a top level domain (such as `.gov` or `.com`) to prevent servers from setting arbitrary cookies for another domain (such as setting a cookie for `owasp.org`). If the domain attribute is not set, then the hostname of the server that generated the cookie is used as the default value of the `domain`.

For example, if a cookie is set by an application at `app.mydomain.com` with no domain attribute set, then the cookie would be resubmitted for all subsequent requests for `app.mydomain.com` and its subdomains (such as `hacker.app.mydomain.com`), but not to `otherapp.mydomain.com`. If a developer wanted to loosen this restriction, then he could set the `domain` attribute to `mydomain.com`. In this case the cookie would be sent to all requests for `app.mydomain.com` and `mydomain.com` subdomains, such as `hacker.app.mydomain.com`, and even `bank.mydomain.com`. If there was a vulnerable server on a subdomain (for example, `otherapp.mydomain.com`) and the `domain` attribute has been set too loosely (for example, `mydomain.com`), then the vulnerable server could be used to harvest cookies (such as session tokens) across the full scope of `mydomain.com`.

#### Path Attribute

The [`Path`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Scope_of_cookies) attribute plays a major role in setting the scope of the cookies in conjunction with the [`domain`](#domain-attribute). In addition to the domain, the URL path that the cookie is valid for can be specified. If the domain and path match, then the cookie will be sent in the request. Just as with the domain attribute, if the path attribute is set too loosely, then it could leave the application vulnerable to attacks by other applications on the same server. For example, if the path attribute was set to the web server root `/`, then the application cookies will be sent to every application within the same domain (if multiple application reside under the same server). A couple of examples for multiple applications under the same server:

- `path=/bank`
- `path=/private`
- `path=/docs`
- `path=/docs/admin`

#### Expires Attribute

The [`Expires`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Permanent_cookies) attribute is used to:

- set persistent cookies
- limit lifespan if a session lives for too long
- remove a cookie forcefully by setting it to a past date

Unlike [session cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Session_cookies), persistent cookies will be used by the browser until the cookie expires. Once the expiration date has exceeded the time set, the browser will delete the cookie.

#### SameSite Attribute

The [`SameSite`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#SameSite_cookies) attribute is used to assert that a cookie ought not to be sent along with cross-site requests. This feature allows the server to mitigate the risk of cross-orgin information leakage. In some cases, it is used too as a risk reduction (or defense in depth mechanism) strategy to prevent [cross-site request forgery](05-Testing_for_Cross_Site_Request_Forgery.md) attacks. This attribute can be configured in three different modes:

- `Strict`
- `Lax`
- `None`

##### Strict Value

The `Strict` value is the most restrictive usage of `SameSite`, allowing the browser to send the cookie only to first-party context without top-level navigation. In other words, the data associated with the cookie will only be sent on requests matching the current site shown on the browser URL bar. The cookie will not be sent on requests generated by third-party websites. This value is especially recommended for actions performed at the same domain. However, it can have some limitations with some session management systems negatively affecting the user navigation experience. Since the browser would not send the cookie on any requests generated from a third-party domain or email, the user would be required to sign in again even if they already have an authenticated session.

##### Lax Value

The `Lax` value is less restrictive than `Strict`. The cookie will be sent if the URL equals the cookie’s domain (first-party) even if the link is coming from a third-party domain. This value is considered by most browsers the default behavior since it provides a better user experience than the `Strict` value. It doesn't trigger for assets, such as images, where cookies might not be needed to access them.

##### None Value

The `None` value specifies that the browser will send the cookie on cross-site requests (the normal behavior before the implementation of `SamseSite`) only if the `Secure` attribute is also used, _e.g._ `SameSite=None; Secure`. It is a recommended value, instead of not specifying any `SameSite` value, as it forces the use of the [`secure` attribute](#secure-attribute).

### Cookie Prefixes

By design cookies do not have the capabilities to guarantee the integrity and confidentiality of the information stored in them. Those limitations make it impossible for a server to have confidence about how a given cookie's attributes were set at creation. In order to give the servers such features in a backwards-compatible way, the industry has introduced the concept of [`Cookie Name Prefixes`](https://tools.ietf.org/html/draft-ietf-httpbis-cookie-prefixes-00) to facilitate passing such details embedded as part of the cookie name.

#### Host Prefix

The [`__Host-`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Cookie_prefixes) prefix expects cookies to fulfill the following conditions:

  1. The cookie must be set with the [`Secure` attribute](#secure-attribute).
  2. The cookie must be set from a URI considered secure by the user agent.
  3. Sent only to the host who set the cookie and MUST NOT include any [`Domain` attribute](#domain-attribute).
  4. The cookie must be set with the [`Path`attribute](#path-attribute) with a value of `/` so it would be sent to every request to the host.

For this reason, the cookie `Set-Cookie: __Host-SID=12345; Secure; Path=/` would be accepted while any of the following ones would always be rejected:
`Set-Cookie: __Host-SID=12345`
`Set-Cookie: __Host-SID=12345; Secure`
`Set-Cookie: __Host-SID=12345; Domain=site.example`
`Set-Cookie: __Host-SID=12345; Domain=site.example; Path=/`
`Set-Cookie: __Host-SID=12345; Secure; Domain=site.example; Path=/`

#### Secure Prefix

The [`__Secure-`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Cookie_prefixes) prefix is less restrictive and can be introduced by adding the case-sensitive string `__Secure-` to the cookie name. Any cookie that matches the prefix `__Secure-` would be expected to fulfill the following conditions:

  1. The cookie must be set with the `Secure` attribute.
  2. The cookie must be set from a URI considered secure by the user agent.

### Strong Practices

Based on the application needs, and how the cookie should function, the attributes and prefixes must be applied. The more the cookie is locked down, the better.

Putting all this together, we can define the most secure cookie attribute configuration as: `Set-Cookie: __Host-SID=<session token>; path=/; Secure; HttpOnly; SameSite=Strict`.

## Tools

### Intercepting Proxy

- [OWASP Zed Attack Proxy Project](https://www.zaproxy.org)
- [Web Proxy Burp Suite](https://portswigger.net)

### Browser Plug-in

- [Tamper Data for FF Quantum](https://addons.mozilla.org/en-US/firefox/addon/tamper-data-for-ff-quantum/)
- ["FireSheep" for FireFox](https://github.com/codebutler/firesheep)
- ["EditThisCookie" for Chrome](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en)
- ["Cookiebro - Cookie Manager" for FireFox](https://addons.mozilla.org/en-US/firefox/addon/cookiebro/)

## References

- [RFC 2965 - HTTP State Management Mechanism](https://tools.ietf.org/html/rfc2965)
- [RFC 2616 – Hypertext Transfer Protocol – HTTP 1.1](https://tools.ietf.org/html/rfc2616)
- [Same-Site Cookies - draft-ietf-httpbis-cookie-same-site-00](https://tools.ietf.org/html/draft-ietf-httpbis-cookie-same-site-00)
- [The important "expires" attribute of Set-Cookie](https://seckb.yehg.net/2012/02/important-expires-attribute-of-set.html)
- [HttpOnly Session ID in URL and Page Body](https://seckb.yehg.net/2012/06/httponly-session-id-in-url-and-page.html)
