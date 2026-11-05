# API Rate Limiting and Resource Consumption

|ID          |
|------------|
|WSTG-APIT-06|

## Summary

APIs without rate limits, request size limits, or query complexity controls are exposed to denial of service, financial abuse, and brute-force attacks. Unlike traditional web applications that serve rendered pages, APIs return structured data and accept programmatic access, making automated abuse straightforward.

Common weaknesses include:

- Missing or bypassable rate limits on authentication and data endpoints.
- Unbounded pagination that allows a single request to dump entire datasets.
- Unchecked batch and bulk operations that multiply resource consumption.
- Unrestricted file upload sizes or counts.
- GraphQL queries with excessive depth, breadth, or alias counts that exhaust server-side resources.

This article corresponds to OWASP API Security Top 10 [API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/).

## Test Objectives

- Verify that per-client and per-endpoint rate limits are enforced.
- Identify bypass techniques for existing rate limits.
- Confirm that pagination, batch operations, and query complexity are bounded.
- Verify that upload size, response size, and timeout controls exist.

## How to Test

Run resource-exhaustion tests (large uploads, inflated batches, high concurrency, broad date ranges) only in agreed test windows or staging environments. These tests can degrade production service for real users.

### Detect Rate Limit Headers and Behavior

Send a burst of requests and observe the response headers and status codes:

```bash
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -H "Authorization: Bearer <TOKEN>" \
    https://api.example.com/v1/users/me
done
```

Check for rate limit headers:

```bash
curl -si -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me | grep -i "rate\|limit\|retry\|ratelimit"
```

Record these common rate limit headers when present:

| Header | Purpose |
|--------|---------|
| `X-RateLimit-Limit` | Maximum requests per window (de facto convention) |
| `X-RateLimit-Remaining` | Requests left in current window (de facto convention) |
| `X-RateLimit-Reset` | Timestamp when the window resets (de facto convention) |
| `RateLimit-Limit` | Maximum requests per window (IETF draft) |
| `RateLimit-Policy` | Rate limit policy definition (IETF draft) |
| `Retry-After` | Seconds to wait before retrying (RFC 7231) |

Insecure behavior: no rate limit headers returned and no `429 Too Many Requests` after high volume.

### Bypass Rate Limits via Header Spoofing

First, establish a baseline by triggering the rate limit:

```bash
for i in $(seq 1 200); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer <TOKEN>" \
    https://api.example.com/v1/users/me)
  echo "Request $i: $STATUS"
  [ "$STATUS" = "429" ] && echo "Rate limit hit at request $i" && break
done
```

Once `429` is returned, test whether spoofing the client IP header resets the limit:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Forwarded-For: 203.0.113.1" \
  https://api.example.com/v1/users/me
```

Test each of these headers with a different documentation address (RFC 5737):

- `X-Forwarded-For`
- `X-Real-IP`
- `X-Originating-IP`
- `X-Client-IP`
- `True-Client-IP`
- `CF-Connecting-IP`
- `Forwarded: for=203.0.113.1` (RFC 7239)

Insecure behavior: a `200 OK` returns after spoofing the header, indicating the rate limit resets per header value.

### Bypass via Path and Method Variation

After triggering a rate limit (see [header spoofing](#bypass-rate-limits-via-header-spoofing)), test whether path variations reset the counter:

```bash
# Trailing slash
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/v1/users/

# Case change
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/V1/Users

# Query parameter injection
curl -s -o /dev/null -w "%{http_code}" "https://api.example.com/v1/users?_=1234"

# Double slash
curl -s -o /dev/null -w "%{http_code}" https://api.example.com//v1//users

# URL-encoded slash
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/v1%2fusers

# Dot segment
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/v1/./users
```

Test HTTP method switching:

```bash
# HEAD instead of GET
curl -s -o /dev/null -w "%{http_code}" -I \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users

# POST search instead of GET list
curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query":"*"}' \
  https://api.example.com/v1/users/search
```

Insecure behavior: a `200 OK` on a path variant after the rate limit was triggered, indicating each variant is counted as a separate endpoint.

### Bypass via Parameter Pollution

Test whether the rate limiter and the application parse request bodies differently. If the rate limiter keys on the first occurrence of a field but the application uses the last, an attacker can bypass per-account rate limits. For background on parser-differential attacks, see [HTTP Parameter Pollution](../07-Injection/04-HTTP_Parameter_Pollution.md).

After triggering the rate limit against one account, test:

```bash
# Add a no-op field to create a unique request signature
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test","_nonce":"abc"}' \
  https://api.example.com/v1/login

# Duplicate keys: limiter may key on first "email", app authenticates on last
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"decoy@example.com","password":"test","email":"real@example.com"}' \
  https://api.example.com/v1/login
```

Insecure behavior: the rate limiter counts the request against `decoy@example.com` while the application authenticates as `real@example.com`, allowing unlimited attempts against the real target.

### Test Pagination Abuse

Test whether the API enforces server-side maximum page sizes:

```bash
# Normal request
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/users?page=1&per_page=25"

# Excessive page size
curl -s -o /dev/null -w "Size: %{size_download} Time: %{time_total}\n" \
  -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/users?page=1&per_page=100000"

# Negative offset
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/users?offset=-1&limit=100"

# Zero page size (may return all records)
curl -s -o /dev/null -w "Size: %{size_download}\n" \
  -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/users?per_page=0"

# Very high page number (enumerate total count)
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/users?page=999999&per_page=25"

# Cursor-based pagination abuse
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/users?cursor=AAAA&limit=100000"
```

Compare response sizes and times against the default. Insecure behavior: the API returns the requested page size regardless of value, or returns all records when `per_page=0`.

### Test Batch and Bulk Operation Abuse

Test whether array and bulk parameters are bounded:

```bash
# Normal batch lookup
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"ids":["1","2","3"]}' \
  https://api.example.com/v1/users/lookup

# Inflated batch (string IDs matching baseline format)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d "{\"ids\":[$(seq -f '\"%.0f\"' -s, 1 10000)]}" \
  https://api.example.com/v1/users/lookup
```

Increase batch sizes (10, 100, 1000) and observe whether the server rejects oversized batches.

### Test GraphQL Query Complexity

For comprehensive GraphQL denial-of-service testing (query depth, batching attacks, and alias-based denylist bypass), see [GraphQL (WSTG-APIT-99)](99-GraphQL.md). When testing rate limits specifically, verify that:

- Query batching is capped (e.g., no more than a fixed number of queries per batch request).
- Alias count per query is limited to prevent multiplying field resolution cost.
- Query cost or complexity analysis rejects expensive queries before execution.

Test batch size limits:

```bash
# Batch of queries in a single HTTP request
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '[
    {"query":"{ user(id:1) { name } }"},
    {"query":"{ user(id:2) { name } }"},
    {"query":"{ user(id:3) { name } }"}
  ]' \
  https://api.example.com/graphql
```

Scale to 100, 500, 1000 batched queries and observe whether the server rejects oversized batches or returns errors.

### Test File Upload Size and Count Limits

```bash
# Generate a large file
dd if=/dev/zero of=/tmp/large_file.bin bs=1M count=500 2>/dev/null

# Upload
curl -s -o /dev/null -w "%{http_code} Size:%{size_upload} Time:%{time_total}\n" \
  -X POST -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/tmp/large_file.bin" \
  https://api.example.com/v1/upload
```

Also test:

- Rapid successive uploads of small files (100 requests in 10 seconds).
- Manipulated `Content-Length` header claiming a smaller size than the actual payload.

### Test Response Size Limits

Request a large date range or unfiltered dataset:

```bash
curl -s -o /dev/null -w "Size: %{size_download} Time: %{time_total}\n" \
  -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/logs?from=2000-01-01&to=2099-12-31"
```

Insecure behavior: tens or hundreds of MB returned, indicating no server-side response size control.

### Test Timeouts and Slow Requests

Send a slow request using chunked transfer encoding:

```bash
(echo -ne "POST /v1/process HTTP/1.1\r\nHost: api.example.com\r\nTransfer-Encoding: chunked\r\nContent-Type: application/json\r\n\r\n"; \
 echo -ne "5\r\n{\"a\":\r\n"; sleep 5; \
 echo -ne "4\r\n\"b\"}\r\n"; sleep 5; \
 echo -ne "0\r\n\r\n") | openssl s_client -quiet -connect api.example.com:443
```

Also test slow search queries:

```bash
curl -s -o /dev/null -w "Time: %{time_total}\n" \
  -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/search?q=a&sort=random&include=all"
```

### Test Concurrent Connection Limits

```bash
seq 1 200 | xargs -P 200 -I{} curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me
```

Compare response codes and response times against the API's documented capacity or a baseline measured at normal load. Insecure behavior: the API shows no connection throttling (no `429` or `503` responses) and response times remain stable at volumes far exceeding documented limits, indicating absent per-client connection caps.

## Related Test Cases

- [GraphQL (WSTG-APIT-99)](99-GraphQL.md)
- [HTTP Parameter Pollution](../07-Injection/04-HTTP_Parameter_Pollution.md)

## Remediation

- Implement per-client, per-endpoint rate limits. Return rate limit headers (the common `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` or the IETF draft `RateLimit-Limit`, `RateLimit-Policy`).
- Key rate limits on authenticated user identity, not only source IP. Ignore client-supplied IP headers for rate limiting decisions.
- Normalize request paths before rate limit evaluation (case, trailing slashes, encoding).
- Enforce a server-side maximum page size. Ignore client-requested values that exceed it.
- Cap the number of items in array and bulk request parameters.
- Implement GraphQL query depth limits, cost analysis, and batch size caps. See the [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html).
- Set upload and response size limits at both the web server and application layers.
- Configure server-side request timeouts and per-client connection limits.
- See the [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html).

## References

- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
- [CWE-799: Improper Control of Interaction Frequency](https://cwe.mitre.org/data/definitions/799.html)
- [OWASP API Security Top 10 - API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
