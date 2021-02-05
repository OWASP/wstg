# Testing for Content Security Policy

|ID          |
|------------|
|WSTG-CONF-12|

## Summary

Content Security Policy is a declarative allow-list policy enforced through `Content-Security-Policy` response header or equivalent `<meta>` element. It allows developers to restrict the sources from which resources such as JavaScript, CSS, images, files etc. are loaded. CSP is an effective defense in depth technique to mitigate the risk of vulnerabilities such as Cross Site Scripting (XSS) and Clickjacking.

Content Security Policy can be implemented through one of two methods:

- `Content-Security-Policy` response header: `Content-Security-Policy: <policy>`
- Meta element: `<meta http-equiv="Content-Security-Policy" content="policy">`

Content Security Policy supports directives which allow granular control to the flow of policies.

- **Fetch directives**: determine the allowed sources to trust and load resources from. For example; `img-src`, `script-src`, `object-src`, `style-src` can be used to restrict sources of images, scripts, plugins and style sheets respectively. If `default-src` is configured, directives which are not specified will fall back to default configuration.
- **Document directives**: identifies the properties of the document to which policies are applied. `base-uri`, `plugin-types` or `sandbox` are allowed directives.
- **Navigation directives**: determine the locations that document can navigate to. `navigate-to` directive restricts URLs which can be navigated from the application by any means. `form-action` and `frame-ancestors` can be used to restrict URLs to which form can be submitted and URLs that can embed requested resource.
- **Reporting directives**: specify the locations to which violations of prevented behavior are to be reported. `report-to` or `report-uri` can be used to configure reporting location.

Below are few examples of content security policy implementation.

1. Restrict scripts to be loaded from same origin and api.example.com, media to loaded from media.example.com and allow to include images from all origins.

   ```HTTP
   script-src 'self' api.example.com; media-src media.example.com; img-src *
   ```

2. Enforce TLS for loading all resources.

   ```HTTP
   Content-Security-Policy: default-src https://secure.example.com
   ```

3. Enable violation reporting to URL specified in `report-uri`.

   ```HTTP
   Content-Security-Policy: default-src 'self'; report-uri http://reportcollector.example.com/collector.cgi
   ```

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

## Test Objectives

Review the Content-Security-Policy header or meta element to identify misconfigurations.

## How to Test

To test for misconfigurations in content security policies look for below insecure configurations by examining `Content-Security-Policy` HTTP response header or CSP meta element in a proxy tool:

- `unsafe-inline` directive enables inline scripts making the applications susceptible to Cross Site Scripting attacks.
- `unsafe-eval` directive allows eval() to be used in the application.
- Resources such as scripts can be allowed to be loaded from any origin by the use wildcard (*) source.
- Framing can be enabled for all origins by the use of wildcard (*) source for `frame-ancestors` directive.
- Business critical applications require to use a CSP strict policy.

## Remediation

Configure a strong CSP policy which reduces the attack surface of the application. Developers can verify the strength of content security policy using online tools such as [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/).

## Tools

- [CSP Auditor - Burp Suite Extension](https://portswigger.net/bappstore/35237408a06043e9945a11016fcbac18)

## References

- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [CSP Level 3 W3C](https://www.w3.org/TR/CSP3/)
- [CSP with Google](https://csp.withgoogle.com/docs/index.html)
- [Content-Security-Policy](https://content-security-policy.com/)
- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)
- [CSP A Successful Mess Between Hardening And Mitigation](https://speakerdeck.com/lweichselbaum/csp-a-successful-mess-between-hardening-and-mitigation)
