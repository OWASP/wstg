# Testing for Content Security Policy

|ID          |
|------------|
|WSTG-CONF-12|

## Summary

Content Security Policy (CSP) is a declarative allow-list policy enforced through `Content-Security-Policy` response header or equivalent `<meta>` element. It allows developers to restrict the sources from which resources such as JavaScript, CSS, images, files etc. are loaded. CSP is an effective defense in depth technique to mitigate the risk of vulnerabilities such as Cross Site Scripting (XSS) and Clickjacking.

Content Security Policy supports directives which allow granular control to the flow of policies. (See [References](#references) for further details.)

## Test Objectives

- Review the Content-Security-Policy header or meta element to identify misconfigurations.

## How to Test

Testing for Content Security Policy (CSP) weaknesses requires more than verifying the presence of the header. The tester should evaluate whether the policy meaningfully reduces the attack surface and is properly enforced.

### Identify and Confirm CSP Enforcement

- Inspect HTTP responses for the presence of the `Content-Security-Policy` header.
- Check for `Content-Security-Policy-Report-Only`. If only Report-Only is present, the policy is not enforced.
- Verify whether CSP is delivered via HTTP header or `<meta>` tag (HTTP headers are preferred).
- Note that CSP delivered via `<meta>` tags does not support certain directives such as `frame-ancestors`, `report-uri`, `report-to`, or `sandbox`.
- Confirm that the policy is consistently applied across sensitive endpoints.

### Review High-Risk Directives

Inspect the policy for insecure or overly permissive directives:

- `unsafe-inline` allows inline scripts or styles and significantly weakens XSS protections.
- `unsafe-eval` permits dynamic code evaluation (`eval()`), increasing bypass risk.
- `unsafe-hashes` may allow inline execution if hashes are predictable or improperly scoped.
- Wildcard (`*`) sources may allow loading resources from any origin.
    - Partial wildcards such as `https://*` or `*.cdn.com` should be carefully evaluated.
    - Determine whether allowlisted domains host JSONP endpoints or user-controlled content.
- Absence or misuse of `frame-ancestors` may expose the application to clickjacking.
- Missing `object-src`, `base-uri`, or restrictive `default-src` directives may weaken policy effectiveness.
- Review usage of `require-trusted-types-for` and `trusted-types`. In high-risk applications, absence of Trusted Types may leave DOM-based injection sinks exposed. If `trusted-types` policies are defined, ensure they are not overly permissive.
- Check for duplicate directives or conflicting policy definitions that may result in unintended enforcement behavior.

### Validate Nonce and strict-dynamic Usage

If the policy uses nonces:

- Confirm that nonces are cryptographically random.
- Verify that nonces are regenerated per response and not reused.
- Ensure that legacy inline script patterns are not inadvertently trusted.

If `strict-dynamic` is used:

- Understand that trust propagates from nonce- or hash-based scripts.
- Confirm that no unsafe trust chain allows attacker-controlled script loading.

### Evaluate CSP Reporting Mechanisms

If `report-uri` or `report-to` is configured:

- Verify that reporting endpoints are reachable and functional.
- Determine whether sensitive information is exposed in reports.
- Confirm that reporting does not create new injection or denial-of-service vectors.

### Attempt Controlled Bypass Techniques

Where appropriate and authorized, attempt to validate enforcement by testing controlled payloads:

- Inline script injection attempts.
- Data URL–based payloads.
- JSONP callback manipulation from allowlisted domains.
- DOM-based gadget chaining using trusted script sources.

Successful execution of injected JavaScript indicates CSP misconfiguration or ineffective enforcement.

### Assess Policy Strength

Business-critical applications should aim to implement a strict policy. A robust CSP typically:

- Avoids `unsafe-inline` and `unsafe-eval`.
- Uses nonce- or hash-based script controls.
- Restricts object embedding (`object-src 'none'`).
- Restricts base tag manipulation (`base-uri 'none'`).
- Restricts framing using `frame-ancestors`.

### Common CSP Bypass Patterns

Even when CSP is present, misconfigurations or design weaknesses may allow bypass. Testers should consider the following common patterns:

#### JSONP and Trusted Third-Party Endpoints

If a CSP allowlists third-party domains (e.g., CDNs), determine whether those domains expose JSONP endpoints or user-controlled content. Attackers may leverage callback injection to execute arbitrary JavaScript while still complying with the policy.

#### Wildcard and Broad Source Policies

Policies that rely on wildcards (`*`, `https://*`, `*.example.com`) significantly expand the trust boundary. Subdomain takeovers or compromised third-party services may enable bypass within the allowed scope.

#### Nonce Reuse or Predictable Nonces

If nonces are reused across requests or generated predictably, attackers may reuse or guess them to execute injected scripts. Each response should generate a fresh, cryptographically strong nonce.

#### Over-Reliance on strict-dynamic

While `strict-dynamic` improves nonce-based policies, trust propagates from trusted scripts. If a trusted script loads attacker-controlled resources, the protection may be weakened.

#### Missing Defense-in-Depth Directives

Absence of directives such as:

- `object-src 'none'`
- `base-uri 'none'`
- `frame-ancestors`

may leave the application exposed to object injection, base tag manipulation, or clickjacking, even if script execution is partially restricted.

#### CSP in Report-Only Mode

Applications sometimes deploy CSP in `Report-Only` mode indefinitely. In such cases, violations are logged but not blocked, providing no real protection.

## Remediation

Organizations should implement a strong, well-scoped Content Security Policy that meaningfully reduces the attack surface rather than simply satisfying compliance requirements.

### General Recommendations

- Avoid use of `unsafe-inline` and `unsafe-eval`.
- Prefer nonce- or hash-based script controls.
- Use a restrictive `default-src` directive.
- Explicitly define:
    - `object-src 'none'`
    - `base-uri 'none'`
    - `frame-ancestors`
- Minimize the number of allowlisted third-party domains.
- Regularly review CSP policies when introducing new frontend dependencies.

### Deployment Best Practices

- Deploy `Content-Security-Policy-Report-Only` temporarily for testing, then enforce `Content-Security-Policy` once validated.
- Monitor violation reports for legitimate breakage and potential attack attempts.
- Prefer `report-to` (CSP Level 3) while maintaining `report-uri` for backward compatibility where required.
- Ensure nonces are cryptographically random and regenerated per response.
- Review policies during major frontend refactoring or framework changes.

### Strict Policy Guidance

A strict policy provides protection against stored, reflected, and certain DOM-based XSS attacks and should be the goal for high-risk or business-critical applications.

Based on nonce-based approaches, example policies include:

Moderate Strict Policy:

```HTTP
script-src 'nonce-r4nd0m' 'strict-dynamic';
object-src 'none';
base-uri 'none';
```

Locked Down Strict Policy:

```HTTP
script-src 'nonce-r4nd0m';
object-src 'none';
base-uri 'none';
```

Note: `'nonce-r4nd0m'` is shown as an example placeholder. In practice, nonces must be cryptographically strong, base64-encoded values that are uniquely generated for every HTTP response.

Teams should adapt strict policies carefully, ensuring compatibility with application architecture while maintaining security objectives.

## Tools

- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)
- [CSP Auditor - Burp Suite Extension](https://portswigger.net/bappstore/35237408a06043e9945a11016fcbac18)
- [CSP Generator Chrome](https://chrome.google.com/webstore/detail/content-security-policy-c/ahlnecfloencbkpfnpljbojmjkfgnmdc) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/csp-generator/)
- [CSP Validator](https://cspvalidator.netlify.app/)
- [OWASP ZAP](https://www.zaproxy.org/) – Includes automated and passive analysis for CSP misconfigurations.
- [CSPBypass](https://cspbypass.com/) – Tool designed to help security testers analyze and attempt bypass techniques against restrictive CSP implementations.

## References

- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Mozilla Developer Network: Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [CSP Level 3 W3C](https://www.w3.org/TR/CSP3/)
- [CSP with Google](https://csp.withgoogle.com/docs/index.html)
- [Content-Security-Policy](https://content-security-policy.com/)
- [CSP A Successful Mess Between Hardening And Mitigation](https://speakerdeck.com/lweichselbaum/csp-a-successful-mess-between-hardening-and-mitigation)
- [The unsafe-hashes Source List Keyword](https://content-security-policy.com/unsafe-hashes/)
