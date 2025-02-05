# Test Other HTTP Security Header Misconfigurations

|ID          |
|------------|
|WSTG-CONF-14|

## Summary

Security headers play a vital role in protecting web applications from a wide range of attacks, including Cross-Site Scripting (XSS), Clickjacking, and data injection attacks. These headers instruct the browser on how to handle security-related aspects of a website’s communication, reducing exposure to known attack vectors. However, misconfigurations can lead to vulnerabilities, weakening the intended security protections or rendering the existing security protections ineffective. This section outlines common security header misconfigurations, their risks, and how to properly test for them.

### Common Security Header Misconfigurations:
- **Security Header with an Empty Value**: Headers present but lacking a value may be ignored by browsers, making them ineffective.
- **Security Header with an Invalid Value or Name (Typos)**: Incorrect header names or misspellings result in headers not being recognized or enforced.
- **Overpermissive Security Headers**: Overpermissive headers can leak information or allow access to resources beyond the intended scope.
- **Duplicate Security Headers**: Conflicting definitions of the same header can lead to unpredictable browser behavior and potentially disable security measures.
- **Legacy Security Headers**: The inclusion of obsolete headers, can create unnecessary risks instead of improving security.
- **Invalid Placement of Security Headers**: Certain headers must be delivered over specific conditions or protocols; using these headers when the right conditions are not met renders them ineffective.

## Risks of Misconfigured Security Headers

- **Reduced Effectiveness**: If headers are misconfigured, they may not provide the intended protection, allowing exploits such as XSS, Clickjacking, or CORS-related attacks.
- **Breakage of Security Measures**: Duplicate headers may lead to unexpected behavior, with some browsers completley ignoring the HTTP security headers because of this.
- **Legacy and Deprecated Headers**: Using obsolete security headers can introduce new attack vectors instead of securing the application.

## Test Objectives

- Identify security headers that are improperly configured.
- Assess the impact of misconfigured security headers.
- Validate correct implementation of required security headers.

## How to Test

### Fetch and Review HTTP Security Headers

To inspect the security headers used by an application, different methods can be applied:

- Use an intercepting proxy such as **Burp Suite** or **ZAP** to analyze server responses.
- Run the following curl command to retrieve HTTP response headers:
  
```bash
curl -I https://example.com
```

- Utilize browser developer tools to check server responses:
  - Open developer tools (F12) → Navigate to the **Network** tab → Select a request → View the **Headers** section.

### Check for Overly Permissive Security Headers

To evaluate overly permissive security headers, consider the following methods, especially when wildcard characters (*) are used or when certain security headers are configured too broadly:

1. Identify the headers that could allow excessive access, such as:
  
```
Access-Control-Allow-Origin
Access-Control-Allow-Credentials
X-Permitted-Cross-Domain-Policies
Referrer-Policy
```

2. Verify if strict directives are enforced or not. Here is an example of overpermissive security headers.

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
X-Permitted-Cross-Domain-Policies: all
Referrer-Policy: unsafe-url
```

And here is an example of its strict directive (secure) equivalents:

```http
Access-Control-Allow-Origin: {theallowedoriginurl}
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: no-referrer
```

To verify the directives make sure you search the header name on the [Mozilla Developer Network: Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) website as this will give you a proper overview of secure and insecure directives for each header.

3. Finally, ensure that the strict directives are implemented but keep in mind that sometimes strict directives can break normal functionality so always check that it works with your application.

### Check for Duplicate, Deprecated / Obsolete Headers

To detect duplicate or deprecated headers, perform the following:

- Look for multiple occurrences of the same security header with conflicting values.
- Be aware of obsolete headers such as HPKP or header directives such as, ALLOW-FROM in X-Frame-Options, which is no longer supported by modern browsers. Again, you can verify the deprecation status of headers on Mozilla's website for example: [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options). 
- Ensure deprecated headers are removed or replaced with modern equivalents.

### Confirm Proper Placement of Security Headers 

Similar to the `Secure` flag in cookies, some HTTP security headers are only effective under specific conditions. For instance, certain headers must be delivered over HTTPS; sending them over HTTP renders them ineffective.

To ensure security headers are correctly positioned:

- Validate that the correct conditions required for the header to work are present. For example; for HSTS make sure TLS/SSL is present.

## Remediation

- **Ensure headers are correctly configured**: Avoid empty or invalid values, and double-check for typos.
- **Apply strict directives**: Configure headers to minimize security risks (e.g., avoid using * in CORS policies unless required).
- **Remove deprecated headers**: Remove headers like HPKP that are no longer supported.
- **Beware of conditional exclusive headers**: Ensure that security headers like HSTS are correctly applied only in HTTPS responses.

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
