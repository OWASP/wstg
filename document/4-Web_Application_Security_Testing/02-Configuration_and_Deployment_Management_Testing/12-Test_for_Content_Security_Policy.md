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

To test for misconfigurations in CSPs, look for insecure configurations by examining the `Content-Security-Policy` HTTP response header or CSP `meta` element in a proxy tool:

- `unsafe-inline` directive enables inline scripts or styles, making the applications susceptible to [XSS](../07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting.md) attacks.
- `unsafe-eval` directive allows `eval()` to be used in the application and is susceptible to common bypass techniques such as data URL injection.
- `unsafe-hashes` directive allows use of inline scripts/styles, assuming they match the specified hashes.
- Resources such as scripts can be allowed to be loaded from any origin by the use wildcard (`*`) source.
    - Also consider wildcards based on partial matches, such as: `https://*` or `*.cdn.com`.
    - Consider whether allow listed sources provide JSONP endpoints which might be used to bypass CSP or same-origin-policy.
- Framing can be enabled for all origins by the use of the wildcard (`*`) source for the `frame-ancestors` directive. If the `frame-ancestors` directive is not defined in the Content-Security-Policy header it may make applications vulnerable to [clickjacking](../11-Client-side_Testing/09-Testing_for_Clickjacking.md) attacks.
- Business critical applications should require to use a strict policy.

## Remediation

Configure a strong content security policy which reduces the attack surface of the application. Developers can verify the strength of content security policy using online tools such as [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/).

### Strict Policy

A strict policy is a policy which provides protection against classical stored, reflected, and some of the DOM XSS attacks and should be the optimal goal of any team trying to implement CSP.

Google went ahead and set up a guide to adopt a strict CSP based on nonces. Based on a presentation at [LocoMocoSec](https://speakerdeck.com/lweichselbaum/csp-a-successful-mess-between-hardening-and-mitigation?slide=55), the following two policies can be used to apply a strict policy:

Moderate Strict Policy:

```HTTP
script-src 'nonce-r4nd0m' 'strict-dynamic';
object-src 'none'; base-uri 'none';
```

Locked down Strict Policy:

```HTTP
script-src 'nonce-r4nd0m';
object-src 'none'; base-uri 'none';
```

- `script-src` directive is used to restrict the sources from which scripts can be loaded and executed.
- `object-src` directive is used to restrict the sources from which objects can be loaded and executed.
- `base-uri` directive specifies the base URL for resolving relative URLs in the page. Without this directive, the page becomes vulnerable to HTML base tag injection attacks.

## Tools

- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)
- [CSP Auditor - Burp Suite Extension](https://portswigger.net/bappstore/35237408a06043e9945a11016fcbac18)
- [CSP Generator Chrome](https://chrome.google.com/webstore/detail/content-security-policy-c/ahlnecfloencbkpfnpljbojmjkfgnmdc) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/csp-generator/)

## References

- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Mozilla Developer Network: Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [CSP Level 3 W3C](https://www.w3.org/TR/CSP3/)
- [CSP with Google](https://csp.withgoogle.com/docs/index.html)
- [Content-Security-Policy](https://content-security-policy.com/)
- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)
- [CSP A Successful Mess Between Hardening And Mitigation](https://speakerdeck.com/lweichselbaum/csp-a-successful-mess-between-hardening-and-mitigation)
- [The unsafe-hashes Source List Keyword](https://content-security-policy.com/unsafe-hashes/)
