# Test Other HTTP Security Header Misconfigurations

| ID         |
|------------|
|WSTG-CONF-14|

## Summary

Security headers play a vital role in protecting web applications from a wide range of attacks, including Cross-Site Scripting (XSS), Clickjacking, and data injection attacks. These headers instruct the browser on how to handle security-related aspects of a website’s communication, reducing exposure to known attack vectors. However, misconfigurations can lead to vulnerabilities, weakening the intended security protections or rendering them ineffective. This section outlines common security header misconfigurations, their risks, and how to properly test for them.

## Test Objectives

- Identify improperly configured security headers.
- Assess the impact of misconfigured security headers.
- Validate the correct implementation of required security headers.

## Common Security Header Misconfigurations

- **Security Header with an Empty Value:** Headers that are present but lack a value may be ignored by browsers, making them ineffective.
- **Security Header with an Invalid Value or Name (Typos):** Incorrect header names or misspellings result in headers not being recognized or enforced.
- **Overpermissive Security Headers:** Headers configured too broadly (e.g., using wildcard characters `*` or overly permissive directives) can leak information or allow access to resources beyond the intended scope.
- **Duplicate Security Headers:** Multiple occurrences of the same header with conflicting values can lead to unpredictable browser behavior, potentially disabling the security measures entirely.
- **Legacy or Deprecated Headers:** Inclusion of obsolete headers (e.g., HPKP) or directives (e.g., `ALLOW-FROM` in X-Frame-Options) that are no longer supported by modern browsers may create unnecessary risks.
- **Invalid Placement of Security Headers:** Some headers are only effective under specific conditions. For example, headers like HSTS must be delivered over HTTPS; if sent over HTTP, they become ineffective.
- **META Tag Handling Mistakes:** In cases where security policies such as Content-Security-Policy (CSP) are enforced via both HTTP headers and META tags (using `http-equiv`), there is a risk that the META tag value might override or conflict with the secure logic defined in the HTTP header. This can lead to a scenario where an insecure policy inadvertently takes precedence, weakening the overall security posture.

## Risks of Misconfigured Security Headers

- **Reduced Effectiveness:** Misconfigured headers might not provide the intended protection, leaving the application vulnerable to attacks such as XSS, Clickjacking, or CORS-related exploits.
- **Breakage of Security Measures:** Duplicate headers or conflicting directives can result in browsers ignoring the HTTP security headers entirely, thereby disabling the intended protections.
- **Introduction of New Attack Vectors:** The use of legacy or deprecated headers may introduce risks rather than mitigate them if modern browsers no longer support the intended security measures.

## How to Test

### Fetch and Review HTTP Security Headers

To inspect the security headers used by an application, employ the following methods:

- **Intercepting Proxies:** Use tools such as **Burp Suite** to analyze server responses.
- **Command Line Tools:** Execute a curl command to retrieve HTTP response headers: `curl -I https://example.com`
    - Sometimes the web application will redirect to a new page, in order to follow redirect use the following command:`curl -L -I https://example.com`
    - Some Firewalls may block curl's default User-Agent and some TLS/SSL errors will also prevent it from returning the correct information, in thise case you could try to use the following command:
`curl -I -L -k --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36" https://example.com`
- **Browser Developer Tools:** Open developer tools (F12), navigate to the **Network** tab, select a request, and view the **Headers** section.

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

- **Cross-Reference Documentation:** Use resources such as the [Mozilla Developer Network: Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) to review secure and insecure directives.

### Check for Duplicate, Deprecated / Obsolete Headers

- **Duplicate Headers:** Ensure that the same header is not defined multiple times with conflicting values.
- **Obsolete Headers:** Identify and remove deprecated headers (e.g., HPKP) and outdated directives (e.g., `ALLOW-FROM` in X-Frame-Options). Refer to sources like [Mozilla Developer Network: X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options) for current standards.

### Confirm Proper Placement of Security Headers

- **Protocol-Specific Requirements:** Validate that headers intended for secure contexts (e.g., HSTS) are delivered only under appropriate conditions (i.e., over HTTPS).
- **Conditional Delivery:** Some headers may only be effective under specific circumstances. Verify that these conditions are met for the header to function as intended.

### Evaluate META Tag Handling

- **Dual Enforcement Checks:** When a security policy like CSP is applied through both an HTTP header and a META tag using `http-equiv`, confirm that the HTTP header (which is generally considered more authoritative) is not inadvertently overridden by the META tag.
- **Review Browser Behavior:** Test the application in various browsers to see if any differences occur due to the presence of conflicting directives. Where possible, avoid using dual definitions to prevent unintended security lapses.

## Remediation

- **Correct Header Configuration:** Ensure that headers are correctly implemented with proper values and no typos.
- **Enforce Strict Directives:** Configure headers with the most secure settings that still allow for required functionality. For example, avoid using `*` in CORS policies unless absolutely necessary.
- **Remove Deprecated Headers:** Replace legacy security headers with modern equivalents and remove any that are no longer supported.
- **Avoid Conflicting Definitions:** Prevent duplicate header definitions and ensure that META tags do not conflict with HTTP headers for security policies.

## Tools

- [Mozilla Observatory](https://observatory.mozilla.org/)
- [ZAP](https://www.zaproxy.org/)
- [Burp Suite](https://portswigger.net/burp)
- Browser Developer Tools (Chrome, Firefox, Edge)

## References

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla Developer Network: Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [RFC 6797 - HTTP Strict Transport Security (HSTS)](https://datatracker.ietf.org/doc/html/rfc6797)
- [Google Web Security Guidelines](https://web.dev/security-headers/)
- [HPKP is No More](https://scotthelme.co.uk/hpkp-is-no-more/)
