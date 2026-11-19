# Web Cache Poisoning

|ID          |
|------------|
|WSTG-CONF-16|

## Summary

Web caches and CDNs store responses so later requests can be served without contacting the origin. A cache keys each stored response on a subset of the request: typically the method, scheme, host, path, and query string, sometimes selected headers, cookies, or further query parameters. Anything that changes the origin response but is absent from that key is an unkeyed input.

Web cache poisoning occurs when an attacker supplies an unkeyed input that makes the origin emit a malicious or incorrect response, and the cache stores that response under a key that ordinary users later request. Impacts include stored XSS, open redirects, denial of service through cached errors or empty bodies, and leakage of authenticated content into a shared cache.

This test is about discovering and validating the cache key. It is distinct from:

- [Path Confusion](13-Path_Confusion.md), which covers cache deception through path identity mismatches.
- [Host Header Injection](../07-Injection/17-Host_Header_Injection.md), which covers one common poisoning input.
- [HTTP Request Smuggling](../07-Injection/16-HTTP_Request_Smuggling.md), which can also poison caches through desynchronization.

## Test Objectives

- Identify which responses are cacheable and which request inputs form the cache key.
- Find unkeyed headers, cookies, query parameters, or method-override inputs that change the origin response.
- Confirm that a clean request without the unkeyed input receives the poisoned or incorrect cached response.
- Verify that authenticated or personalized responses are not stored under keys reachable by other users.

## How to Test

Perform these tests only against assets you own or have written authorization to test. Prefer dedicated staging or uniquely named disposable URLs. Never prime a shared production asset with a harmful payload.

### 1. Establish a Cache Oracle

1. Choose a target URL that returns a stable body and is likely static or semi-static.
2. Append a unique cache-buster query parameter that the application ignores, for example `?wstg_cb=<random>`.
3. Before trusting the buster, confirm it is part of the cache key: request the same path with two different buster values. Both should miss (or otherwise stay independent). If the second buster is a hit of the first, the CDN is dropping the query string from the key for that resource, and every later "isolated" probe can poison the real URL. Stop and use a different path or a keyed input instead.
4. Request the URL twice with the same buster. Compare:
   - Status and body.
   - `Age`, `X-Cache`, `CF-Cache-Status`, `X-Cache-Status`, `X-Drupal-Cache`, or equivalent.
   - `Cache-Control`, `Expires`, `Vary`, `ETag`, and `Last-Modified`.
5. A rising `Age`, a hit/miss transition, or an identical body served faster on the second request indicates a cache is participating.

### 2. Discover the Cache Key

Do not send a baseline request first under the same cache-buster. If the baseline is cached, an unkeyed mutation becomes a cache hit and never reaches the origin, which hides the vulnerability.

For each candidate input:

1. Choose a fresh cache-buster that has not been requested before and that you confirmed is keyed in Establish a Cache Oracle.
2. Send the mutated request first (cache miss) so it reaches the origin, changing only one candidate input.
3. Send a clean request with that same cache-buster and no mutation.
4. Fetch a baseline response with a separate cache-buster for comparison.

| Observation | Meaning |
|-------------|---------|
| Clean request returns the mutated response | The input is unkeyed. Cache poisoning is possible. |
| Clean request returns the baseline response | The input is keyed, or the mutated response was not stored. |
| Mutated request is never cached | The cache may exclude that header or status. Record it and continue. |

Candidate unkeyed inputs to try one at a time:

- Headers that applications often trust: `X-Forwarded-Host`, `X-Forwarded-Scheme`, `X-Forwarded-Proto`, `X-Original-URL`, `X-Rewrite-URL`, `X-Host`, `Forwarded`.
- Content negotiation and routing: `Accept`, `Accept-Language`, `Accept-Encoding`, `Accept-Version`, custom API version headers.
- Method overrides: `X-HTTP-Method-Override`, `X-HTTP-Method`, `X-Method-Override` on a GET that the origin treats as HEAD or another method.
- Cookies that change page content but may be absent from the cache key.
- Query parameters the cache may exclude from the key while the origin still reads them: marketing parameters such as `utm_source`, `utm_campaign`, `fbclid`, and parameter-cloaking forms that append or duplicate a keyed parameter after an excluded one.
- Oversized or duplicate header chains that the cache accepts but the origin rejects. That is [cache-poisoned denial of service (CPDoS)](https://cpdos.org/), not a harmless canary. Use only unique cache-busted URLs, increase size gradually, and stop at the agreed lab limit.

### 3. Validate With Harmless Canaries

Prefer canaries that prove impact without harming other users:

- Reflect a unique token into an HTML body, location header, or JSON field.
- Force a distinctive error page or empty body for a disposable URL.
- Cache a redirect to a tester-controlled HTTPS canary host.

After the poisoned response is stored, request the same URL and cache-buster without the unkeyed input. Capture both the priming and the clean hit as evidence.

### 4. Authenticated and Personalized Content

1. Authenticate as tester A and request a personalized page through the cache with a unique buster.
2. From an anonymous session or tester B, request the same URL and buster.
3. If B receives A's private content, record the disclosure. Compare the result with a cache-bypassed baseline and cache telemetry before assigning a cause.

#### Verify Tenant Isolation

Use an isolated test environment with two tenants, A and B, that have no access to each other's data. Give each tenant a distinct synthetic record. Use separate sessions with equivalent roles. Choose a protected, read-only view that both tenants use, such as the list of records for the current tenant.

1. Establish the expected response for each tenant through an approved cache bypass that keeps the same origin routing and authorization. Verify that each session sees its own record. If a baseline exposes the other tenant's record, investigate origin routing and authorization before evaluating the shared cache.
2. Start with a known empty cache state for the test resource. Request the view using the normal tenant context in A's session, then in B's session. Repeat in reverse order from a fresh cache state. Where the policy allows caching within each tenant, repeat the authorized reads to observe a hit for each tenant.
3. Compare the status and tenant-specific response content with each baseline. Use cache logs, traces, or a [`Cache-Status`](https://www.rfc-editor.org/rfc/rfc9211.html) field from the relevant cache to confirm how it handled each request. If multiple caches are present, identify which layer the evidence describes.

An unexpected record from another tenant is an isolation failure even if the responsible layer is still unknown. Treat matching responses as evidence for the tested configuration when you can confirm the intended hits or policy-driven bypass. If cache behavior is unobservable or expected hits are absent, record the cache result as inconclusive. A correct response on a miss alone does not verify isolation on cache hits.

Record the tested route and access policy, request order, cache state and observations, expected and observed records, and the result. Remove credentials and session identifiers from the evidence.

### 5. Normalization Differentials

Path Confusion already covers deception through alternate paths. For poisoning, compare whether the cache and origin normalize the same:

- Slash versus backslash.
- Encoded separators.
- Dot-segments that stay inside the resource.
- Duplicate slashes.

If one form returns an error that is stored under the canonical key, ordinary clients receive the error. Keep the target URL unique to the test.

## Remediation

- Include every input that changes the response in the cache key, or strip those inputs before the request reaches the origin.
- Emit correct `Vary` values for headers that affect the response.
- Do not cache authenticated or personalized responses in a shared cache unless the key includes the relevant credential and the response is explicitly intended to be shared.
- Prefer origin-controlled `Cache-Control` over extension-based CDN heuristics.
- Reject or normalize unexpected forwarding and method-override headers at a trusted edge.

## Tools

- [Zed Attack Proxy](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)
- [Param Miner](https://github.com/PortSwigger/param-miner)

## References

- [RFC 9111 - HTTP Caching](https://datatracker.ietf.org/doc/html/rfc9111)
- [RFC 9110 - HTTP Semantics (`Vary`)](https://datatracker.ietf.org/doc/html/rfc9110#section-12.5.5)
- [OWASP Web Cache Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Web_Cache_Security_Cheat_Sheet.html)
- [Practical Web Cache Poisoning](https://portswigger.net/research/practical-web-cache-poisoning)
- [Bypassing Web Cache Poisoning Countermeasures](https://portswigger.net/research/bypassing-web-cache-poisoning-countermeasures)
- [Path Confusion](13-Path_Confusion.md)
- [Host Header Injection](../07-Injection/17-Host_Header_Injection.md)
