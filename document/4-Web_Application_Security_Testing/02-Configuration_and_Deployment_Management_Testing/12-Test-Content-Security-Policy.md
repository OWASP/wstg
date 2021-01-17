# Test Content Security Policy

|ID          |
|------------|
|WSTG-CONF-12|

## Summary

A Content Security Policy (CSP) is a mechanism that instructs the browser to
disable some potentially dangerous actions. It is used, for example, to reduce the
risk of cross-site scripting attacks. 

CSP is usually specified in an HTTP header named `Content-Security-Policy`. As
with other headers, it can also be specified in a `<meta>` tag with the attribute
`http-equiv=Content-Security-Policy` attribute of an HTML document.

A header named `Content-Security-Policy-Report-Only` can be used to instruct the
browser to no apply the restrictions but only report if they would have been
violated. 

### CSP directives

CSP directives are listed in the CSP header, delimited by semicolons. 

The various `-src` directives describe which sources are safe for loading
scripts or other elements of a page. `default-src 'self'` means than any
element, like scripts, images of fonts, can only be loaded from the same web
site. `script-src 'self' js.library.com` would allow loading scripts from the
same web server or from the designated site `js.library.com`.

The `script unsafe-eval` directive allows the usage of the eval function in JavaScript,
which is potentially dangerous and disallowed by default if a CSP header is
present. Similarly, `script unsafe-inline` allows the usage of JavaScript inside
an HTML document (e.g. in `<script>` tags or in attributes like `onclick`). 

Hashes and nonces can be used to allow only specific scripts or resources to be
loaded. Other directives control miscallaneous mechanisms like framing,
upgrading HTTP and HTTPS and more. 

## Test Objectives

Confirm that a CSP has been defined. Verify that it is not overly permissive. 


## How to Test

The presence of the CSP header can be confirmed by examining the server's
response through an intercepting proxy or by using curl as follows:

```bash
$ curl -s -D- https://www.w3.org | grep -i content-security-policy
content-security-policy: upgrade-insecure-requests
```

If the header is present, verify that it does not contain overly permissive
directives like `script-src *`, `script-src unsafe-eval` or `script-src
unsafe-inline`.

## Remediation

Create a content security policy that matches precisely the actions that need to
be allowed. Using the `report-only` option for a while can help finding out
which actions need to be allowed. 

## Related to

The correct usage of a CSP can prevent mots injection attacks that are listed in
[Chapter 4.11 Client-side Testing](../4-Web_Application_Security_Testing/11-Client-side_Testing/README.md)

## References

- [OWASP Content Security Policy Cheat
  Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [W3C Content Security Policy Level 3, Working
  Draft](https://www.w3.org/TR/CSP3/)
