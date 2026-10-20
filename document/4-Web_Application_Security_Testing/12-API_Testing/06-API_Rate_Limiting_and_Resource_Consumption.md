# Testing API Rate Limiting and Resource Consumption

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
  https://api.example.com/v1/users/me | grep -i "rate\|limit\|retry\|x-ratelimit"
```

Record these standard headers when present:

| Header | Purpose |
|--------|---------|
| `X-RateLimit-Limit` | Maximum requests per window |
| `X-RateLimit-Remaining` | Requests left in current window |
| `X-RateLimit-Reset` | Timestamp when the window resets |
| `Retry-After` | Seconds to wait before retrying |

Insecure behavior: no rate limit headers returned and no `429 Too Many Requests` after high volume.

### Bypass Rate Limits via Header Spoofing

When rate limits are keyed on source IP behind a reverse proxy or load balancer, spoofing the client IP header bypasses the limit:

```bash
for i in $(seq 1 20); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -H "Authorization: Bearer <TOKEN>" \
    -H "X-Forwarded-For: 192.168.1.$i" \
    https://api.example.com/v1/users/me
done
```

Test these headers:

- `X-Forwarded-For`
- `X-Real-IP`
- `X-Originating-IP`
- `X-Client-IP`
- `True-Client-IP`
- `CF-Connecting-IP`
- `X-Forwarded-Host`

Insecure behavior: rate limit resets when a different IP header value is sent.

### Bypass via Path and Method Variation

Test whether the rate limiter normalizes request paths:

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

Insecure behavior: each path variant is counted as a separate endpoint, multiplying the effective rate limit.

### Bypass via Parameter Pollution

Test whether the rate limiter uses request body content as part of the key:

```bash
# Add a no-op field to create a unique request
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test","_nonce":"abc"}' \
  https://api.example.com/v1/login

# Duplicate keys (JSON last-key-wins behavior)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"decoy@example.com","password":"test","email":"real@example.com"}' \
  https://api.example.com/v1/login
```

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

# Inflated batch
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d "{\"ids\":[$(seq -s, 1 10000)]}" \
  https://api.example.com/v1/users/lookup
```

Test GraphQL query batching:

```bash
# Batch of queries
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '[
    {"query":"{ user(id:1) { name } }"},
    {"query":"{ user(id:2) { name } }"},
    {"query":"{ user(id:3) { name } }"}
  ]' \
  https://api.example.com/graphql
```

Increase batch sizes (10, 100, 1000) and observe whether the server rejects oversized batches.

### Test GraphQL Query Complexity

#### 1. Query Depth

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"query":"{ user(id:1) { friends { friends { friends { friends { friends { name } } } } } } }"}' \
  https://api.example.com/graphql
```

#### 2. Query Aliases

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"query":"{ a1:user(id:1){name} a2:user(id:2){name} a3:user(id:3){name} a4:user(id:4){name} a5:user(id:5){name} }"}' \
  https://api.example.com/graphql
```

Scale to 100, 500, 1000 aliases and observe response times and errors.

#### 3. Query Breadth

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"query":"{ users(first:10000) { id name email role orders { id total items { id name price } } payments { id amount date } } }"}' \
  https://api.example.com/graphql
```

Insecure behavior: all queries return full results with no complexity errors, indicating absent query cost analysis.

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
 echo -ne "5\r\n\"b\"}\r\n"; sleep 5; \
 echo -ne "0\r\n\r\n") | nc api.example.com 443
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

Insecure behavior: all 200 concurrent requests succeed with no `429` or `503` responses.

## Remediation

- Implement per-client, per-endpoint rate limits. Return standard rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`).
- Key rate limits on authenticated user identity, not only source IP. Ignore client-supplied IP headers for rate limiting decisions.
- Normalize request paths before rate limit evaluation (case, trailing slashes, encoding).
- Enforce a server-side maximum page size. Ignore client-requested values that exceed it.
- Cap the number of items in array and bulk request parameters.
- Implement GraphQL query depth limits, cost analysis, and batch size caps.
- Set upload and response size limits at both the web server and application layers.
- Configure server-side request timeouts and per-client connection limits.
- See the [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) and the [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html).

## References

- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
- [CWE-799: Improper Control of Interaction Frequency](https://cwe.mitre.org/data/definitions/799.html)
- [CWE-835: Loop with Unreachable Exit Condition (Infinite Loop)](https://cwe.mitre.org/data/definitions/835.html)
- [OWASP API Security Top 10 — API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
