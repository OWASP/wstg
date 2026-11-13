# Additional Browser Security Controls

| ID         |
|------------|
|WSTG-CONF-14|

## Summary

Security headers play a vital role in protecting web applications from a wide range of attacks, including Cross-Site Scripting (XSS), Clickjacking, and data injection attacks. These headers instruct the browser on how to handle security-related aspects of a website’s communication, reducing exposure to known attack vectors. However, misconfigurations can lead to vulnerabilities, weakening the intended security protections or rendering them ineffective. This section outlines common security header misconfigurations, their risks, and how to properly test for them. It also covers Subresource Integrity (SRI), which protects the application from changes to scripts and style sheets loaded from third parties.

## Test Objectives

- Identify improperly configured security headers.
- Assess the impact of misconfigured security headers.
- Validate the correct implementation of required security headers.
- Identify third-party scripts and style sheets and determine whether they are pinned with Subresource Integrity.

## Headers Covered by This Section

Per the [OWASP Secure Headers Project](https://owasp.org/projects/secure-headers-project), this section covers the security headers not addressed elsewhere in this guide's other CONF tests:

- X-Frame-Options (and its successor, the `frame-ancestors` CSP directive): clickjacking protection.
- X-Content-Type-Options: prevents MIME-sniffing.
- Referrer-Policy: controls referrer leakage.
- Permissions-Policy: restricts browser feature/API access.
- Cross-Origin-Opener-Policy (COOP) and Cross-Origin-Embedder-Policy (COEP): process isolation, required for cross-origin isolation.
- Clear-Site-Data: clears browsing data (cache, cookies, storage) on logout/sensitive transitions.
- Integrity-Policy: requires integrity metadata for scripts and style sheets, see [Subresource Integrity and Third-Party Resources](#subresource-integrity-and-third-party-resources).

Deprecated, do not recommend: `X-XSS-Protection` is deprecated and disabled or removed in modern browsers; it can itself introduce XSS in older browsers. Use CSP instead. Similarly, `Public-Key-Pins` (HPKP) is deprecated; see the Legacy/Deprecated Headers bullet below.

## Common Security Header Misconfigurations

- **Security Header with an Empty Value:** Headers that are present but lack a value may be ignored by browsers, making them ineffective.
- **Security Header with an Invalid Value or Name (Typos):** Incorrect header names or misspellings result in headers not being recognized or enforced.
- **Overpermissive Security Headers:** Headers configured too broadly (e.g., using wildcard characters `*` or overly permissive directives) can leak information or allow access to resources beyond the intended scope.
- **Duplicate Security Headers:** Multiple occurrences of the same header with conflicting values can lead to unpredictable browser behavior, potentially disabling the security measures entirely.
- **Legacy or Deprecated Headers:** Inclusion of obsolete headers (e.g., HPKP, `X-XSS-Protection`) or directives (e.g., `ALLOW-FROM` in X-Frame-Options) that are no longer supported by modern browsers may create unnecessary risks.
- **Invalid Placement of Security Headers:** Some headers are only effective under specific conditions. For example, headers like HSTS must be delivered over HTTPS; if sent over HTTP, they become ineffective.
- **META Tag Handling Mistakes:** In cases where security policies such as Content-Security-Policy (CSP) are enforced via both HTTP headers and META tags (using `http-equiv`), there is a risk that the META tag value might override or conflict with the secure logic defined in the HTTP header. This can lead to a scenario where an insecure policy inadvertently takes precedence, weakening the overall security posture.
- **Hop-by-Hop Header Injection:** Occurs when intermediaries incorrectly process the `Connection` header, allowing attackers to list and "strip" sensitive internal security headers (like `X-Forwarded-For`) before the request reaches the backend.

## Risks of Misconfigured Security Headers

- **Reduced Effectiveness:** Misconfigured headers might not provide the intended protection, leaving the application vulnerable to attacks such as XSS, Clickjacking, or CORS-related exploits.
- **Breakage of Security Measures:** Duplicate headers or conflicting directives can result in browsers ignoring the HTTP security headers entirely, thereby disabling the intended protections.
- **Introduction of New Attack Vectors:** The use of legacy or deprecated headers may introduce risks rather than mitigate them if modern browsers no longer support the intended security measures.

## How to Test

### Fetch and Review HTTP Security Headers

To inspect the security headers used by an application, employ the following methods:

- **Intercepting Proxies:** Use tools such as **Burp Suite** to analyze server responses.
- **Command-line Tools:** Execute a curl command to retrieve HTTP response headers: `curl -I https://example.com`
    - Sometimes the web application will redirect to a new page, in order to follow redirect use the following command:`curl -L -I https://example.com`
    - Some Firewalls may block curl's default User-Agent and some TLS/SSL errors will also prevent it from returning the correct information, in this case you could try to use the following command:
    `curl -I -L -k --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36" https://example.com`
- **Browser Developer Tools:** Open developer tools (F12), navigate to the **Network** tab, select a request, and view the **Headers** section.

### Check Individual Headers Against Recommended Values

For each header, confirm it is present and its value matches current guidance (see [OWASP Secure Headers Project](https://owasp.org/projects/secure-headers-project) for the authoritative reference table):

```http
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Clear-Site-Data: "cache","cookies","storage"
```

- Flag `X-XSS-Protection` if present - it is deprecated; confirm CSP is used instead for XSS mitigation.
- Flag `X-Frame-Options: ALLOW-FROM ...` - unsupported by modern browsers; recommend the CSP `frame-ancestors` directive.
- Confirm `Clear-Site-Data` is only sent where appropriate (e.g., logout endpoints), since it is destructive to client-side state.

### Check for Overly Permissive Security Headers

- **Identify Risky Headers:** Look for headers that could allow excessive access, such as:
- **Evaluate Directives:** Verify whether strict directives are enforced. For example, an overpermissive setup might appear as:

    ```http
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    X-Permitted-Cross-Domain-Policies: all
    Referrer-Policy: unsafe-url
    ```

    A safe configuration would look like:

    ```http
    Access-Control-Allow-Origin: {theallowedoriginurl}
    X-Permitted-Cross-Domain-Policies: none
    Referrer-Policy: no-referrer
    ```

- **Cross-Reference Documentation:** Use resources such as the [Mozilla Developer Network: Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers) to review secure and insecure directives.

### Check for Duplicate, Deprecated / Obsolete Headers

- **Duplicate Headers:** Ensure that the same header is not defined multiple times with conflicting values.
- **Obsolete Headers:** Identify and remove deprecated headers (e.g., HPKP) and outdated directives (e.g., `ALLOW-FROM` in X-Frame-Options). Refer to sources like [Mozilla Developer Network: X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options) for current standards.

### Confirm Proper Placement of Security Headers

- **Protocol-Specific Requirements:** Validate that headers intended for secure contexts (e.g., HSTS) are delivered only under appropriate conditions (i.e., over HTTPS).
- **Conditional Delivery:** Some headers may only be effective under specific circumstances. Verify that these conditions are met for the header to function as intended.

### Evaluate META Tag Handling

- **Dual Enforcement Checks:** When a security policy like CSP is applied through both an HTTP header and a META tag using `http-equiv`, confirm that the HTTP header (which is generally considered more authoritative) is not inadvertently overridden by the META tag.
- **Review Browser Behavior:** Test the application in various browsers to see if any differences occur due to the presence of conflicting directives. Where possible, avoid using dual definitions to prevent unintended security lapses.

### Test for Header Stripping (Hop-by-Hop Injection)

Attackers can exploit this by listing sensitive security headers inside the `Connection` header. The proxy, following the standard, strips these headers before forwarding the request to the backend. This can lead to:

- Bypassing IP-based Access Control Lists (ACLs).
- Bypassing Identity/Authentication checks performed at the edge.
- Disabling security features enforced by intermediary headers.

#### Identification of Internal/Sensitive Headers (Reconnaissance)

To perform this test, you first need to identify which headers are used by the internal infrastructure. You can identify them by:

- **Triggering Error Pages:** Send malformed requests to trigger error pages (404, 500), which might leak internal headers in the response.
- **Reflection Endpoints:** Search for debugging or "Echo" pages (e.g., `/phpinfo`, `/debug`, `/env`) that display all headers received by the backend.
- **Header Guessing:** Common targets include `X-Forwarded-For`, `X-Real-IP`, `X-Forwarded-Proto`, and `X-Authenticated-User`.

#### Execution of the Injection

Attempt to "strip" a target header by adding it as a value to the `Connection` header.

##### Scenario A: Bypassing IP-based Restrictions

```http
GET /admin HTTP/1.1
Host: example.com
X-Forwarded-For: 203.0.113.10
Connection: close, X-Forwarded-For
```

##### Scenario B: Stripping Authentication Context

```http
GET /api/user/profile HTTP/1.1
Host: example.com
X-Authenticated-User: victim_user
Connection: close, X-Authenticated-User
```

#### Analyzing the Response

- **Vulnerable:** The application behavior changes (e.g., access is granted, or a reflected IP disappears).
- **Secure:** The application behavior remains unchanged, or the proxy returns a `400 Bad Request`.

### Subresource Integrity and Third-Party Resources

Most applications load some scripts and style sheets from servers they do not control, such as content delivery networks (CDNs), analytics providers and widget vendors. A script loaded this way runs with the full privileges of the page that includes it. If the third-party server is compromised, or the resource is replaced for any other reason, the attacker's code runs in the application's origin and can read the page, steal session data and act as the user.

[Subresource Integrity (SRI)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) lets a page declare the cryptographic hash of the file it expects. The browser fetches the file, compares its hash, and refuses to run or apply it if the hash does not match:

```html
<script src="https://cdn.example.com/lib/1.2.3/lib.min.js"
        integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
        crossorigin="anonymous"></script>
```

SRI is supported for `<script>` and `<link rel="stylesheet">` elements. It does not protect resources that are added by other means, such as scripts that are created at runtime and the content a tag manager injects. Payment pages have an added requirement: requirement 6.4.3 of PCI DSS v4.0 asks for an inventory of every script loaded on the payment page, a reason for each, and a way to assure its integrity. SRI is one way to meet the last part.

#### Identify Third-Party Resources

List every external script and style sheet the application uses.

- Review the page source and the rendered DOM for `<script src>` and `<link rel="stylesheet" href>` elements whose host differs from the application's own origin.
- In the browser developer tools, open the **Network** tab, filter by **JS** and **CSS**, and look at the **Domain** column. Do this on each distinct page type, including the login page and pages shown after authentication, because they often load different resources.
- Note scripts that load further scripts. Tag managers and widget loaders can bring in resources that are not visible in the page source.

The following snippet lists external scripts and style sheets that have no `integrity` attribute on the current page:

```javascript
document.querySelectorAll('script[src], link[rel="stylesheet"][href]').forEach(el => {
  const url = new URL(el.src || el.href, location.href);
  if (url.origin !== location.origin && !el.integrity) {
    console.log(el.tagName, url.href);
  }
});
```

#### Check Integrity Attributes

For each external resource that has an `integrity` attribute, check that:

- The hash algorithm is SHA-256, SHA-384 or SHA-512. Browsers ignore unsupported algorithms.
- The `crossorigin` attribute is set. For a cross-origin resource, the integrity check needs the server to answer with CORS headers, and the request must be made in CORS mode (`crossorigin="anonymous"` is usual).
- The hash matches the file. To compute it, download the file and run:

```bash
curl -s https://cdn.example.com/lib/1.2.3/lib.min.js | openssl dgst -sha384 -binary | openssl base64 -A
```

Compare the result, with the `sha384-` prefix, to the attribute value. A mismatch makes the browser block the resource, which shows as a console error such as `Failed to find a valid digest in the 'integrity' attribute`.

#### Check How the Resource Is Referenced

SRI works only when the file at the URL does not change. Look for references that can change:

- URLs without a version, or with floating versions such as `latest`, `@1` or `/v1/`. A pinned hash on such a URL breaks the page when the file changes, so sites often leave it out.
- Vendor-hosted scripts that are updated by the vendor without notice, such as analytics, chat and A/B-testing scripts. SRI cannot be used for these, so the application relies on trust in the vendor.
- Hosts that have expired, are no longer in use or have a dangling DNS record. See [Subdomain Takeover](10-Subdomain_Takeover.md).
- Hosts whose owner has changed. In 2024 the `polyfill.io` domain was sold and started serving malicious code to the sites that still loaded it. Since that service returned different code for each browser, the sites could not have pinned it with SRI.
- Resources loaded over plain HTTP.

#### Check Runtime-Loaded Resources

SRI attributes are not applied to resources that are added with script such as `document.createElement('script')`, unless the code sets the `integrity` property itself. Review the application's scripts and tag manager configuration for such resources, and note which pages load them and who can change the tag manager configuration.

JavaScript modules need separate attention. The `integrity` attribute of a `<script type="module">` element covers only that file, not the modules it loads with `import` or `import()`. Those can be pinned with the `integrity` field of an [import map](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type/importmap). Check whether third-party modules are imported, and whether the page's import map lists a hash for each of them.

#### Check for an Integrity Policy

The [`Integrity-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Integrity-Policy) response header makes the browser block scripts or style sheets that are loaded without integrity metadata, so a resource that someone forgets to pin fails instead of loading silently:

```http
Integrity-Policy: blocked-destinations=(script)
```

The `Integrity-Policy-Report-Only` header reports violations without blocking them. Check whether either header is sent, which destinations it covers, and whether reports are sent to an endpoint that someone reviews. The header is newer than SRI and not every browser supports it, so treat it as an extra layer.

#### Check the Interaction with CSP

A [Content Security Policy](12-Content_Security_Policy.md) can restrict the hosts scripts may come from, and can allow scripts by hash or nonce. Check whether the policy allows broad hosts (for example a whole CDN domain) that would let an attacker load a different file from the same host. SRI and CSP complement each other: CSP limits where code may come from, and SRI limits which file from that location is accepted. For attacks that read cross-origin data through script inclusion, see [Cross Site Script Inclusion](../11-Client-side/13-Cross_Site_Script_Inclusion.md).

## Remediation

- **Correct Header Configuration:** Ensure that headers are correctly implemented with proper values and no typos.
- **Enforce Strict Directives:** Configure headers with the most secure settings that still allow for required functionality. For example, avoid using `*` in CORS policies unless absolutely necessary.
- **Remove Deprecated Headers:** Replace legacy security headers with modern equivalents and remove any that are no longer supported.
- **Avoid Conflicting Definitions:** Prevent duplicate header definitions and ensure that META tags do not conflict with HTTP headers for security policies.
- **Restrict Connection Header:** Configure proxies to ignore client-supplied values in the `Connection` header that match sensitive internal headers.
- **Zero Trust:** Avoid relying solely on hop-by-hop headers for critical security decisions.
- **Pin Third-Party Resources:** Add `integrity` and `crossorigin` attributes to third-party scripts and style sheets that can be pinned, reference exact versions or host a copy on the application's own origin, and pin imported JavaScript modules with the `integrity` field of an import map.
- **Review Third-Party Scripts:** Remove resources that are no longer used, review each remaining third-party script and its vendor, and limit the scripts a tag manager can load and who can edit it.
- **Require Integrity Metadata:** Send an `Integrity-Policy` header, or start with `Integrity-Policy-Report-Only`, so that resources without integrity metadata are reported or blocked, and combine SRI with a restrictive Content Security Policy.

## Tools

- [Mozilla Observatory](https://developer.mozilla.org/en-US/observatory)
- [ZAP](https://www.zaproxy.org/)
- [Burp Suite](https://portswigger.net/burp)
- Browser Developer Tools (Chrome, Firefox, Edge)
- `openssl` and `curl`, to compute SRI hashes

## References

- [OWASP Secure Headers Project](https://owasp.org/projects/secure-headers-project)
- [Mozilla Developer Network: Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers)
- [RFC 6797 - HTTP Strict Transport Security (HSTS)](https://datatracker.ietf.org/doc/html/rfc6797)
- [Google Web Security Guidelines](https://web.dev/security-headers/)
- [HPKP is No More](https://scotthelme.co.uk/hpkp-is-no-more/)
- [RFC 9110 - HTTP Semantics: Connection Header](https://datatracker.ietf.org/doc/html/rfc9110#section-7.6.1)
- [Abusing HTTP Hop-by-Hop Request Headers](https://nathandavison.com/blog/abusing-http-hop-by-hop-request-headers)
- [W3C: Subresource Integrity](https://www.w3.org/TR/SRI/)
- [MDN: Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
- [MDN: Integrity-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Integrity-Policy)
- [MDN: Import maps](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type/importmap)
- [OWASP: Third Party JavaScript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)
- [Sansec: Polyfill supply chain attack hits 100K+ sites](https://sansec.io/research/polyfill-supply-chain-attack)
