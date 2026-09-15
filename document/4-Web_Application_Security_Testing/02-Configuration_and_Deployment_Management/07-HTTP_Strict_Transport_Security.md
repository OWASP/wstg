# HTTP Strict Transport Security

|ID          |
|------------|
|WSTG-CONF-07|

## Summary

The HTTP Strict Transport Security (HSTS) feature enables a web server to inform the user's browser, via a special response header, that it should never establish an unencrypted HTTP connection to the specified domain servers. Instead, it should automatically establish all connection requests to access the site through HTTPS. This also prevents users from overriding certificate errors.

Its absence, or a weak configuration, can lead to security issues such as:

- Attackers intercepting and accessing information transferred over an unencrypted network channel.
- Attackers carrying out manipulator-in-the-middle (MITM) attacks by taking advantage of users who accept untrusted certificates, or by downgrading/stripping a redirect to HTTPS (SSL stripping).
- Users who mistakenly enter an address in the browser using HTTP instead of HTTPS, or users who click on a link in a web application that incorrectly uses the HTTP protocol.

## Test Objectives

- Review the HSTS header, its directives, and their values for consistency with current best practice.
- Confirm the site is protected against the first-request trust gap, either via preload or an otherwise hardened HTTP-to-HTTPS path.
- Confirm HSTS is applied consistently across the domain and relevant subdomains, and does not mask mixed-content issues.

## How to Test

- Confirm the presence of the HSTS header on the HTTPS response by examining the server's response through an intercepting proxy.
- Use curl as follows:

```bash
$ curl -s -D- https://owasp.org | grep -i strict-transport-security:
Strict-Transport-Security: max-age=31536000
```

- Evaluate the directive values, an example preload-eligible header being `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`:
    - `max-age` (seconds until the browser stops forcing HTTPS for this host) should be at least `31536000` (1 year), or `63072000` (2 years) if the domain is being submitted to, or already on, the HSTS preload list; flag anything materially shorter or `max-age=0` outside of an intentional HSTS-disable rollback.
    - Check whether `includeSubDomains` (extends the policy to all subdomains) is present and, if so, spot-check a sample of subdomains - including ones outside the immediate application (mail, internal tools, staging, etc.) - to confirm they all serve valid HTTPS. A subdomain that cannot serve HTTPS will become unreachable to browsers that have cached the policy.
    - Check whether `preload` is present, and if so, confirm the domain actually appears on the [Chromium HSTS preload list](https://hstspreload.org/) that Chrome, Firefox, Safari, and Edge all consume (the `preload` directive itself has no browser effect; only actual list membership matters):

```bash
$ curl -s "https://hstspreload.org/api/v2/status?domain=example.com"
```

  If `preload` is present but the domain is not yet listed (or was removed), confirm this is an in-progress submission rather than a stale/no-op directive.

- Check the first-request/redirect path: HSTS only protects requests made after the browser has already seen the header once for that host (Trust On First Use), so a user's very first visit - or any visit after the cached policy has expired - is still made over plain HTTP unless the host is preloaded, and that first request/redirect can be intercepted or stripped before the browser ever learns about HSTS. Test it directly:

```bash
$ curl -s -D- http://example.com | head -n 5
```

  Confirm this returns a redirect (`301`/`308`) to the HTTPS equivalent, and that the resulting HTTPS response carries the HSTS header (the header itself is ignored by browsers if sent over plain HTTP, per spec, so it must be re-asserted on the HTTPS side of the redirect). `preload` is the only mechanism that closes this gap entirely, since the policy is then shipped inside the browser rather than learned from a prior response.

- Check the interaction with mixed content: HSTS force-upgrades top-level navigation and same-host subresource requests to HTTPS, but does not rewrite explicit cross-origin `http://` references in markup. Inspect the page source/network tab for absolute `http://otherhost/...` references - these are still subject to ordinary browser mixed-content blocking independent of HSTS (see [Cross Origin Resource Sharing](../11-Client-side/07-Cross_Origin_Resource_Sharing.md)). Separately, confirm any same-host `http://` links in markup are HTTPS by design rather than only "working" because HSTS silently upgraded them - that upgrade can mask a link that should have been fixed.

- For applications behind a CDN/load balancer/reverse proxy, confirm the header is added at (or survives through to) the edge that terminates TLS for end users, not only at an internal origin.

### Preload List Submission

Submission to the HSTS preload list ([hstspreload.org](https://hstspreload.org/)) is a manual, out-of-band step, not something enabled by the header alone. Before recommending submission, confirm the prerequisites are actually met:

- Serve a valid HTTPS certificate on the base domain, and redirect any HTTP request on that domain to HTTPS.
- Serve HTTPS, with a valid certificate, on the `www` subdomain if a DNS record for it exists.
- Send the `Strict-Transport-Security` header on the base domain's HTTPS response with `max-age` of at least `31536000` (one year, though the site recommends `63072000`), and both `includeSubDomains` and `preload` present.
- Confirm every subdomain, including ones outside the immediate application (mail, internal tools, staging, etc.), can serve HTTPS, since `includeSubDomains` applies preload-forced HTTPS to all of them.

Because preload-list changes ship inside browser releases and are difficult/slow to reverse (removal can take months to propagate to users on older cached browser builds), submission should be treated as a one-way, organization-level decision - confirm this is authorized before submitting, and do not submit a target's domain during an assessment.

## Remediation

- Send `Strict-Transport-Security` on every HTTPS response, with `max-age` of at least one year.
- Redirect all HTTP traffic to HTTPS, and ensure the redirect target itself returns the HSTS header.
- Use `includeSubDomains` once all subdomains are confirmed to support HTTPS.
- Consider `preload` and submission to the HSTS preload list for domains that need protection from the very first connection, after confirming the prerequisites above and getting organizational sign-off given the difficulty of reversing it.
- Do not rely on mixed-content upgrading behavior in place of fixing hardcoded `http://` links in markup.

## Tools

- [hstspreload.org](https://hstspreload.org/) - preload list status lookup and submission
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/) - reports HSTS configuration alongside TLS configuration
- [ZAP](https://www.zaproxy.org/) - passive scan rule flags missing/weak HSTS

## References

- [OWASP HTTP Strict Transport Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)
- [OWASP Appsec Tutorial Series - Episode 4: Strict Transport Security](https://www.youtube.com/watch?v=zEV3HOuM_Vw)
- [RFC 6797 - HTTP Strict Transport Security (HSTS)](https://tools.ietf.org/html/rfc6797)
- [hstspreload.org - Preload List Submission Requirements](https://hstspreload.org/)
- [Chromium HSTS Preload List Source](https://chromium.googlesource.com/chromium/src/+/main/net/http/transport_security_state_static.json)
- [MDN: Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [Enable HTTP Strict Transport Security In Nginx](https://www.nginx.com/blog/http-strict-transport-security-hsts-and-nginx/)
