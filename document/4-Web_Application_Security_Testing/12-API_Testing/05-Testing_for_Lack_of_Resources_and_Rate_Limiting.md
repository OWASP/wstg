# Testing for Lack of Resources and Rate Limiting

|ID          |
|------------|
|WSTG-APIT-05|

## Summary

Lack of resources and rate limiting vulnerabilities occur when an API does not properly restrict the number or size of requests that a client can make within a given time period. This can lead to:

- **Denial of Service (DoS)**: Overwhelming the API with requests
- **Resource exhaustion**: Consuming server CPU, memory, or database connections
- **Brute force attacks**: Attempting enumeration or credential stuffing
- **Financial impact**: Especially for APIs with usage-based pricing or that trigger expensive operations

APIs are particularly vulnerable because:

- They are designed for programmatic access, making automation easy
- They may lack traditional protections like CAPTCHAs
- Microservices architectures can have cascading resource consumption
- Rate limits may not be consistently applied across all endpoints

## Test Objectives

- Identify endpoints lacking rate limiting
- Assess the effectiveness of existing rate limiting mechanisms
- Evaluate resource consumption limits for API operations

## How to Test

### Test for Missing Rate Limits

Send a high volume of requests in a short time period to various endpoints:

```bash
# Using curl in a loop
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    "https://api.example.com/v1/users" \
    -H "Authorization: Bearer token"
done

# Using specialized tools
wrk -t4 -c100 -d30s https://api.example.com/v1/resource
```

If all requests succeed without being throttled, rate limiting may be absent.

### Check Rate Limit Headers

Many APIs communicate rate limiting via response headers:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
Retry-After: 60
```

Observe these headers during testing to understand the rate limiting policy.

### Test Rate Limit Bypass Techniques

#### IP-Based Bypass

If rate limiting is IP-based, test with multiple source IPs or header manipulation:

```http
GET /api/v1/sensitive-operation HTTP/1.1
X-Forwarded-For: 1.2.3.4
X-Real-IP: 5.6.7.8
X-Originating-IP: 9.10.11.12
```

#### User-Based vs Session-Based

Test if limits apply per-user or per-session:

```bash
# Create multiple sessions for the same user
# and test if limits are shared or separate
```

#### Endpoint-Specific Limits

Test if different endpoints have different limits:

```bash
# Login endpoint might have stricter limits
for i in {1..10}; do
  curl -X POST "https://api.example.com/v1/login" \
    -d '{"user":"test","pass":"test'$i'"}'
done

# But other endpoints might be unlimited
for i in {1..1000}; do
  curl "https://api.example.com/v1/public-data/$i"
done
```

### Test Resource Consumption Limits

#### Large Payload Attacks

Test maximum payload size handling:

```bash
# Generate a large JSON payload
python -c "print('{\"data\":\"' + 'A'*10000000 + '\"}')" > large.json
curl -X POST "https://api.example.com/v1/resource" \
  -H "Content-Type: application/json" \
  -d @large.json
```

#### Pagination Abuse

Test if pagination parameters are validated:

```http
# Request excessive page sizes
GET /api/v1/users?page=1&per_page=999999 HTTP/1.1

# Request very deep pagination
GET /api/v1/users?page=99999999&per_page=100 HTTP/1.1
```

#### GraphQL-Specific Resource Consumption

GraphQL APIs are particularly vulnerable to resource consumption attacks:

```graphql
# Deep nesting attack
query {
  user(id: "1") {
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

# Batch query attack
query {
  user1: user(id: "1") { name email }
  user2: user(id: "2") { name email }
  user3: user(id: "3") { name email }
  # ... repeat hundreds of times
  user1000: user(id: "1000") { name email }
}

# Alias-based multiplication
query {
  a1: expensiveOperation { result }
  a2: expensiveOperation { result }
  # ... repeat
  a100: expensiveOperation { result }
}
```

### Test Expensive Operations

Identify and test operations that consume significant resources:

- Complex search queries
- Report generation
- Data export functions
- File processing endpoints
- Batch operations

```http
# Complex search that may cause slow database queries
POST /api/v1/search HTTP/1.1
Content-Type: application/json

{
  "query": "A",
  "filters": [
    {"field": "any", "operator": "contains", "value": "e"},
    {"field": "any", "operator": "contains", "value": "a"},
    {"field": "any", "operator": "contains", "value": "i"}
  ],
  "include_archived": true,
  "full_text_search": true
}
```

### Test Authentication Endpoints

Authentication endpoints are critical targets for rate limiting:

```bash
# Password brute force attempt
for pass in $(cat wordlist.txt); do
  curl -X POST "https://api.example.com/v1/login" \
    -d "{\"user\":\"victim\",\"password\":\"$pass\"}"
done

# Account enumeration
for user in $(cat userlist.txt); do
  curl -X POST "https://api.example.com/v1/forgot-password" \
    -d "{\"email\":\"$user@example.com\"}"
done
```

## Indicators of Missing Rate Limiting

- All requests succeed regardless of frequency
- No rate limit headers in responses
- No HTTP 429 (Too Many Requests) responses
- Server becomes slow or unresponsive under load
- Successful brute force or enumeration attacks
- Large data exports or operations complete without limits

## Remediation

- **Implement rate limiting**: Apply limits based on client identity (API key, user, IP)
- **Use sliding window algorithms**: More effective than fixed window rate limiting
- **Set appropriate limits**: Balance between usability and protection
- **Apply different limits per endpoint**: Stricter limits for sensitive operations
- **Limit request sizes**: Enforce maximum payload sizes
- **Implement pagination limits**: Cap maximum page sizes and depths
- **For GraphQL**: Implement query cost analysis and depth limiting
- **Return informative headers**: Help legitimate clients respect limits
- **Consider API gateways**: Centralize rate limiting implementation

## Tools

- **wrk**: High-performance HTTP benchmarking tool
- **Apache Bench (ab)**: Simple load testing
- **Burp Suite Intruder**: Send repeated requests with variations
- **OWASP ZAP**: Fuzzing and repeated request capabilities
- **Custom scripts**: Tailored testing for specific rate limit bypass techniques

## Related Test Cases

- [Testing for DoS Vulnerabilities](../09-Testing_for_Weak_Cryptography/README.md)
- [Testing for Bypassing Authentication Schema](../04-Authentication_Testing/04-Testing_for_Bypassing_Authentication_Schema.md)
- [Testing GraphQL](05-Testing_GraphQL.md)

## References

- [OWASP API Security Top 10: Lack of Resources and Rate Limiting](https://owasp.org/API-Security/editions/2019/en/0xa4-lack-of-resources-and-rate-limiting/)
- [OWASP API Security Top 10 2023: Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html)
