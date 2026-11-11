# Server-side URL Redirect

|ID          |
|------------|
|WSTG-INJT-24|

## Summary

A server-side URL redirect, usually called an open redirect or an unvalidated redirect, happens when the server takes a destination from the request and sends the browser there without checking it properly. The typical case is a parameter such as `/login?next=/account` or `/out?url=https://partner.example` that ends up in the `Location` header of a `301`, `302`, `303`, `307` or `308` response. The same problem exists when the value is written into a `Refresh` header or an HTML `<meta http-equiv="refresh">` tag. Redirects done by JavaScript in the browser are covered in [Client-side URL Redirect](../11-Client-side/04-Client-side_URL_Redirect.md).

Open redirects are often reported as a phishing aid, since the link starts on the trusted domain. They matter more when they are chained with other features that trust the application's own domain:

- OAuth and OpenID Connect authorization servers that accept any `redirect_uri` on the client's domain, or a prefix of it. An open redirect on that domain lets an attacker send the authorization code or token to their own site. When the redirect target has no fragment, the browser keeps the fragment of the original URL, so tokens returned in the fragment are carried along too.
- SSRF filters that only allow URLs on the application's own domain, but follow redirects when they fetch the URL.
- Single sign-on flows that send the user back with a `RelayState`, `returnTo` or `service` parameter.
- Other allow lists, such as Content Security Policy sources or `postMessage` origin checks, that trust a domain which hosts an open redirect.

A related problem is an unvalidated forward. Some frameworks let the server pass a request on to another internal page or handler, for example with `RequestDispatcher.forward()` in Java, without a round trip to the browser. If the target of the forward comes from the request, an attacker may be able to reach internal pages that are normally protected by access control.

## Test Objectives

- Identify request parameters, path segments and headers that control a redirect or forward.
- Assess whether the validation of redirect targets can be bypassed to reach an external site.
- Assess whether a redirect can be used to run script, or chained with OAuth, SSO or SSRF.

## How to Test

### Find Redirect Inputs

Browse the application through an intercepting proxy and look for responses that redirect to a location taken from the request. Common places are:

- Login, logout, registration and session timeout pages, which often take a return address.
- Language, region or theme switchers that send the user back to the previous page.
- Outbound link trackers and "you are leaving this site" pages.
- OAuth, OpenID Connect and SAML endpoints.
- Payment and checkout flows that return from a provider.

Parameter names that often hold a redirect target include `next`, `url`, `target`, `dest`, `destination`, `redirect`, `redirect_url`, `redirect_uri`, `return`, `returnTo`, `return_url`, `continue`, `goto`, `callback`, `RelayState` and `service`. The target can also be part of the path, such as `/redirect/https://partner.example`, or come from a header, such as `Referer` on "go back" links. A redirect built from the `Host` header is covered in [Host Header Injection](17-Host_Header_Injection.md).

For each input, change the value to a harmless page on a domain under the tester's control and check the response, for example:

```bash
curl -s -o /dev/null -D - 'https://example.com/login?next=https://attacker.example/'
```

```http
HTTP/1.1 302 Found
Location: https://attacker.example/
```

Also check the response body for `<meta http-equiv="refresh">` tags, `Refresh` headers and links built from the same value.

### Bypass the Validation

Most applications check the target in some way. The check and the browser often parse the URL differently, so try values that a weak check accepts but that a browser treats as an external address. The examples use `good.example` as the allowed domain and `attacker.example` as the tester's domain:

- Scheme-relative URLs, which use the scheme of the current page: `//attacker.example/`
- Extra slashes and backslashes, which browsers treat as slashes in `http` and `https` URLs: `///attacker.example/`, `/\attacker.example/`, `\/attacker.example/`
- Credentials before the host: `https://good.example@attacker.example/`
- Allowed domain as a prefix, suffix or part of the path or query: `https://good.example.attacker.example/`, `https://attacker-good.example/`, `https://attacker.example/good.example`, `https://attacker.example/?good.example`
- Encoded characters, in case the value is decoded again after the check: `%2F%2Fattacker.example`, `%252F%252Fattacker.example`, `https:%2F%2Fattacker.example`
- Whitespace and control characters, which browsers strip from URLs: `%09//attacker.example`, `/%09/attacker.example`, leading spaces
- Alternative dots, which internationalized domain name handling converts to `.`: `attacker。example`

When the allowed list only contains the application's own domain, look for another redirect, or a page that can be made to redirect, on an allowed domain. A redirect chain through two trusted endpoints often gets past a check that each endpoint alone would pass.

Always confirm a bypass in a real browser, as the way a browser handles the `Location` value is what decides whether the redirect works.

### Script Execution

Browsers do not follow `javascript:` URLs in a `Location` header. When the value is placed in a meta refresh tag, a `Refresh` header, a link or a JavaScript `location` assignment, try `javascript:` and `data:` URLs, including variations such as `JaVaScRiPt:`, `java%09script:` and `%20javascript:`. A working payload makes the redirect a cross-site scripting issue; see [Reflected Cross Site Scripting](01-Reflected_Cross_Site_Scripting.md).

### Chains with Other Features

- If the application is an OAuth or OpenID Connect client, check whether the authorization server accepts a `redirect_uri` that differs from the registered one only in path or query. Combine it with an open redirect on the client's domain and check whether the authorization code or token reaches the tester's domain, in the query, the fragment or the `Referer` header. See [OAuth Authorization Server Weaknesses](../05-Authorization/05.1-OAuth_Authorization_Server_Weaknesses.md).
- If the application fetches URLs server-side and only allows its own domain, point it at an open redirect on that domain and check whether the fetch follows the redirect. See [Server-Side Request Forgery](19-Server-Side_Request_Forgery.md).
- Check SAML `RelayState` and similar SSO return parameters with the same techniques. See [SAML Authentication](../04-Authentication/12-SAML_Authentication.md).

### Unvalidated Forwards

Look for parameters that select a page or handler, such as `?page=`, `?view=` or `?action=`, where the response comes from the same request without a redirect. Change the value to the name or path of a page that should require higher privileges, such as an administration page, and check whether its content is returned. Compare with a direct request to the same page to see whether the forward skips the access check.

## Related Test Cases

- [Client-side URL Redirect](../11-Client-side/04-Client-side_URL_Redirect.md)
- [Host Header Injection](17-Host_Header_Injection.md)
- [Server-Side Request Forgery](19-Server-Side_Request_Forgery.md)
- [OAuth Weaknesses](../05-Authorization/05-OAuth_Weaknesses.md)
- [Bypassing Authorization Schema](../05-Authorization/02-Bypassing_Authorization_Schema.md)

## Remediation

- Avoid taking a full URL from the request. Use an identifier that maps to a list of destinations kept on the server, or only accept a path on the same site.
- When only local paths are allowed, check that the value starts with a single `/` that is not followed by another `/` or `\`, after decoding, and build the final URL on the server from the site's own origin.
- When external destinations are needed, parse the URL with a standard URL parser and compare the scheme and host exactly against an allow list, rather than using prefix, suffix or substring checks.
- Only allow `http` and `https` schemes.
- Consider an interstitial page that shows the destination and asks the user to confirm before leaving the site.
- For OAuth and OpenID Connect, register exact redirect URIs and compare them with exact string matching, as required by [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html).
- Check access control on the target of every forward, not only on the page that performs it.

More guidance is available in the [Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html).

## Tools

- [ZAP](https://www.zaproxy.org/), whose [External Redirect](https://www.zaproxy.org/docs/alerts/20019/) scan rule tests for open redirects
- [Open Redirect Payloads](https://github.com/cujanovic/Open-Redirect-Payloads), a list of bypass values for fuzzing

## References

- [OWASP Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
- [OWASP: Open Redirect](https://owasp.org/www-community/attacks/open_redirect)
- [CWE-601: URL Redirection to Untrusted Site ('Open Redirect')](https://cwe.mitre.org/data/definitions/601.html)
- [RFC 9700: Best Current Practice for OAuth 2.0 Security, Section 4.11 Open Redirection](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.11)
- [RFC 9110: HTTP Semantics, Section 10.2.2 Location](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.2)
- [WHATWG URL Standard](https://url.spec.whatwg.org/)
