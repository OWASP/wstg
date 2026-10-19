# Testing API Rate Limiting and Resource Consumption

|ID          |
|------------|
|WSTG-APIT-06|

## Summary

APIs that do not enforce rate limiting, request size constraints, or
query complexity controls expose the application to denial of service,
financial abuse, and brute-force attacks. Unlike browser-based
applications, APIs are designed for automated consumption, which makes
them especially susceptible to high-volume and high-cost requests.

Resource consumption vulnerabilities arise when an API allows a caller
to request more data, open more connections, or trigger more expensive
operations than the infrastructure can sustain. The absence of
per-client, per-endpoint, or per-operation limits lets an attacker
exhaust compute, memory, bandwidth, or downstream service budgets.

Common manifestations include missing rate limits on authentication
endpoints, unbounded pagination, unchecked batch or bulk operations,
unrestricted file upload sizes, and GraphQL queries with excessive
depth, breadth, or alias counts.

## Test Objectives

- Determine whether the API enforces per-client and per-endpoint rate
  limits.
- Identify bypass techniques that circumvent existing rate limit
  controls.
- Verify that pagination, batch operations, and query complexity are
  bounded.
- Confirm that file upload, response size, and timeout controls are in
  place.

## How to Test

### Detect Rate Limit Headers and Behavior

Send a series of identical requests to an authenticated endpoint and
observe the response headers and status codes.

```bash
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code} " \
    -H "Authorization: Bearer <TOKEN>" \
    https://api.example.com/v1/users/me
done
```

Look for rate limit headers in an individual response:

```bash
curl -si -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me | grep -i "rate\|limit\|retry\|x-ratelimit"
```

Common response headers to record:

- `X-RateLimit-Limit`: the maximum number of requests allowed in a
  window.
- `X-RateLimit-Remaining`: the number of requests remaining.
- `X-RateLimit-Reset`: the time at which the limit resets.
- `Retry-After`: how long to wait before retrying.

If no rate limit headers appear and no `429 Too Many Requests` status
is returned after a high request volume, the endpoint may lack rate
limiting entirely.

### Bypass Rate Limits with Header Rotation

When rate limits are enforced per source IP using a reverse proxy or
load balancer, test whether the following headers override the
detected client address:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-Forwarded-For: 10.0.0.1" \
  https://api.example.com/v1/users/me
```

Rotate through spoofed addresses to determine whether the limit
resets:

```bash
for i in $(seq 1 20); do
  curl -s -o /dev/null -w "%{http_code} " \
    -H "Authorization: Bearer <TOKEN>" \
    -H "X-Forwarded-For: 192.168.1.$i" \
    https://api.example.com/v1/users/me
done
```

Headers to try:

- `X-Forwarded-For`
- `X-Real-IP`
- `X-Originating-IP`
- `X-Client-IP`
- `True-Client-IP`
- `CF-Connecting-IP`
- `X-Forwarded-Host`

### Bypass Rate Limits with Path and Method Variation

Some rate limit implementations key on the exact URL path or HTTP
method. Test variations that reach the same endpoint but use a
different key.

Path normalization bypass:

```bash
# Original path
curl -s https://api.example.com/v1/users

# Trailing slash
curl -s https://api.example.com/v1/users/

# Case variation
curl -s https://api.example.com/V1/Users

# Path parameter injection
curl -s https://api.example.com/v1/users?_=1234

# Double slash
curl -s https://api.example.com//v1//users

# URL-encoded slash
curl -s https://api.example.com/v1%2fusers

# Dot segment
curl -s https://api.example.com/v1/./users
```

HTTP method switching:

```bash
# If GET is rate-limited, try HEAD
curl -s -I https://api.example.com/v1/users

# Try POST with the same query as a body
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"same-as-get-param"}' \
  https://api.example.com/v1/users/search
```

### Bypass Rate Limits with Parameter Pollution

Add an extra parameter or duplicate the existing one to change the
request signature without changing its semantic effect:

```bash
# Original
curl -s "https://api.example.com/v1/login" \
  -d '{"email":"user@example.com","password":"test"}'

# Add a no-op parameter
curl -s "https://api.example.com/v1/login" \
  -d '{"email":"user@example.com","password":"test","_nonce":"abc"}'

# Duplicate the email parameter (JSON last-key-wins)
curl -s "https://api.example.com/v1/login" \
  -d '{"email":"decoy","email":"user@example.com","password":"test"}'
```

### Test Pagination Abuse

Request a page size larger than the application intends:

```bash
# Normal pagination
curl -s "https://api.example.com/v1/users?page=1&per_page=25"

# Excessive page size
curl -s "https://api.example.com/v1/users?page=1&per_page=100000"

# Negative offset
curl -s "https://api.example.com/v1/users?offset=-1&limit=100"

# Zero page size (may return all records or error)
curl -s "https://api.example.com/v1/users?page=1&per_page=0"

# Very large page number
curl -s "https://api.example.com/v1/users?page=999999&per_page=25"
```

Record the response size and server response time. A response that
returns significantly more data than the default page size or that
takes much longer indicates missing pagination controls.

For cursor-based pagination, test with a manipulated cursor value:

```bash
curl -s "https://api.example.com/v1/users?cursor=AAAA&limit=100000"
```

### Test Batch and Bulk Operation Abuse

If the API accepts array parameters, inflate the array to test
boundaries:

```bash
# Normal bulk operation
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"ids":["1","2","3"]}' \
  https://api.example.com/v1/users/lookup

# Inflated array
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"ids":['$(seq -s, 1 10000)']}' \
  https://api.example.com/v1/users/lookup
```

For GraphQL, test query batching:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '[
    {"query":"{ user(id:1) { name } }"},
    {"query":"{ user(id:2) { name } }"},
    {"query":"{ user(id:3) { name } }"}
  ]' \
  https://api.example.com/graphql
```

Send increasingly large batches (10, 100, 1000 queries) and observe
whether the server imposes a batch size limit or responds with an
error.

### Test GraphQL Query Complexity

#### Depth Attack

Send a deeply nested query to test for maximum depth enforcement:

```graphql
query {
  user(id: 1) {
    friends {
      friends {
        friends {
          friends {
            friends {
              name
            }
          }
        }
      }
    }
  }
}
```

#### Alias Attack

Use aliases to repeat an expensive operation within a single query:

```graphql
query {
  a1: user(id: 1) { name email }
  a2: user(id: 2) { name email }
  a3: user(id: 3) { name email }
  # ... repeat to a100, a500, a1000
}
```

#### Breadth Attack

Request many fields on a single object to test breadth limits:

```graphql
query {
  users(first: 10000) {
    edges {
      node {
        id name email phone address role createdAt updatedAt
        orders { id total items { id name price } }
        payments { id amount method }
      }
    }
  }
}
```

If the server returns all results without error, query cost analysis
is absent.

### Test File Upload Size Limits

Upload a file that exceeds a reasonable size boundary:

```bash
# Generate a 500 MB test file
dd if=/dev/zero of=/tmp/large_file.bin bs=1M count=500

# Upload it
curl -s -X POST -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/tmp/large_file.bin" \
  https://api.example.com/v1/upload
```

If the upload succeeds or the server hangs for a long time before
rejecting the file, upload size limits may be missing.

Also test:

- Uploading many small files in rapid succession.
- Uploading a file with a manipulated `Content-Length` header.

### Test Response Size Limits

Request an endpoint with parameters that retrieve all records at once:

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/logs?from=2000-01-01&to=2099-12-31" \
  -o /dev/null -w "Size: %{size_download} Time: %{time_total}"
```

If the response is tens or hundreds of megabytes, the API lacks
response size controls.

### Test Timeout and Slow Request Behavior

Send a request with an intentionally slow body to test server-side
timeout enforcement:

```bash
# Slow POST: send one byte per second
(echo -n '{"data":"'; sleep 5; echo -n 'value'; sleep 5; echo '"}') | \
  curl -s -X POST -H "Content-Type: application/json" \
  -H "Transfer-Encoding: chunked" \
  --data-binary @- \
  https://api.example.com/v1/process
```

For SQL or search endpoints, send a query designed to be slow:

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/search?q=a&sort=random&include=all"
```

Measure whether the server terminates the request within a reasonable
timeout window.

### Test Concurrent Connection Limits

Open many parallel connections to a single endpoint:

```bash
# Using GNU parallel or xargs
seq 1 200 | xargs -P 200 -I{} curl -s -o /dev/null -w "%{http_code} " \
  -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me
```

Observe whether the server begins rejecting connections (with `503`
or `429`) or whether all connections are served.

## Remediation

- Implement per-client, per-endpoint rate limits and return standard
  rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`,
  `X-RateLimit-Reset`).
- Key rate limits on the authenticated user identity, not only the
  source IP address.
- Enforce a maximum page size at the server, ignoring client-supplied
  values above the cap.
- Limit the number of items accepted in array and bulk parameters.
- For GraphQL APIs, enforce query depth limits, cost analysis, and
  batch size caps.
- Set upload and response size limits at the web server and
  application level.
- Configure server-side request timeouts and connection limits.
- See the [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html).

## References

- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
- [CWE-799: Improper Control of Interaction Frequency](https://cwe.mitre.org/data/definitions/799.html)
- [CWE-835: Loop with Unreachable Exit Condition (Infinite Loop)](https://cwe.mitre.org/data/definitions/835.html)
- [OWASP API Security Top 10 — API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
