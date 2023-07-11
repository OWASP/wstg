# Test HTTP Strict Transport Security

|ID          |
|------------|
|WSTG-CONF-07|

## Summary

The HTTP Strict Transport Security (HSTS) feature enables a web server to inform the user's browser, via a special response header, that it should never establish an unencrypted HTTP connection to the specified domain servers. Instead, it should automatically establish all connection requests to access the site through HTTPS. This also prevents users from overriding certificate errors.

Considering the importance of this security measure, it is prudent to verify that the site is using this HTTP header in order to ensure that all the data travels encrypted between the web browser and the server.

The HTTP strict transport security header uses three specific directives:

- `max-age`: to indicate the number of seconds that the browser should automatically convert all HTTP requests to HTTPS.
- `includeSubDomains`: to indicate that all related sub-domains must use HTTPS.
- `preload` Unofficial: to indicate that the domain(s) are on the preload list(s) and that browsers should never connect without HTTPS.
    - While this is supported by all the major browsers, it is not an official part of the specification. (See [hstspreload.org](https://hstspreload.org/) for more information.)

Here's an example of the HSTS header implementation:

`Strict-Transport-Security: max-age=31536000; includeSubDomains`

The presence of this header must be checked, as its absence could lead to security issues such as:

- Attackers intercepting and accessing the information transferred over an unencrypted network channel.
- Attackers carrying out manipulator-in-the-middle (MITM) attacks by taking advantage of users who accept untrusted certificates.
- Users who mistakenly enter an address in the browser using HTTP instead of HTTPS, or users who click on a link in a web application that incorrectly uses the HTTP protocol.

## Test Objectives

- Review the HSTS header and its validity.

## How to Test

- Confirm the presence of the HSTS header by examining the server's response through an intercepting proxy.
- Use curl as follows:

```bash
$ curl -s -D- https://owasp.org | grep -i strict-transport-security:
Strict-Transport-Security: max-age=31536000
```

## References

- [OWASP HTTP Strict Transport Security](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)
- [OWASP Appsec Tutorial Series - Episode 4: Strict Transport Security](https://www.youtube.com/watch?v=zEV3HOuM_Vw)
- [HSTS Specification](https://tools.ietf.org/html/rfc6797)
- [Enable HTTP Strict Transport Security In Apache](https://https.cio.gov/hsts/)
- [Enable HTTP Strict Transport Security In Nginx](https://www.nginx.com/blog/http-strict-transport-security-hsts-and-nginx/)
