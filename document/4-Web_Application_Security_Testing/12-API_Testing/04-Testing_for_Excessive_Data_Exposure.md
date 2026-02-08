# Testing for Excessive Data Exposure

|ID          |
|------------|
|WSTG-APIT-04|

## Summary

Excessive Data Exposure occurs when an API returns more data than necessary to the client, relying on the client-side to filter and display only what the user should see. This is a common vulnerability in APIs because:

- Developers design generic API endpoints that return all object properties
- Client applications (web, mobile) are expected to filter displayed data
- Backend developers don't know which data the frontend actually needs
- APIs are designed for reusability across multiple clients with different needs

This vulnerability can expose:

- Sensitive personal information (PII)
- Internal system data
- Business-critical information
- Security-related fields (hashed passwords, internal IDs, etc.)

## Test Objectives

- Identify API responses that contain more data than necessary
- Detect exposure of sensitive data that should not be sent to clients
- Verify that server-side filtering is applied rather than client-side filtering

## How to Test

### Analyze API Responses for Excessive Data

Capture and analyze API responses to identify fields that contain more information than displayed in the user interface:

```http
GET /api/v1/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer user_token
```

Response (problematic - excessive data):

```json
{
  "id": 123,
  "username": "john_doe",
  "email": "john@example.com",
  "display_name": "John Doe",
  "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.Ake1M1UDaW1pXO",
  "internal_user_id": "usr_internal_00123",
  "role": "user",
  "role_id": 2,
  "created_at": "2023-01-15T10:30:00Z",
  "last_login": "2024-01-20T14:22:00Z",
  "failed_login_attempts": 3,
  "account_locked": false,
  "ssn": "123-45-6789",
  "credit_card": {
    "last_four": "4242",
    "full_number": "4242424242424242",
    "expiry": "12/25",
    "cvv": "123"
  },
  "internal_notes": "VIP customer - handle with care",
  "debug_info": {
    "server": "api-server-02",
    "region": "us-east-1"
  }
}
```

### Compare API Response to UI Display

1. Observe what data is actually displayed in the user interface
2. Capture the API response that populates that view
3. Identify fields in the response that are not displayed to users
4. Evaluate the sensitivity of unexposed fields

### Test Collection Endpoints

List endpoints often expose more data than individual record endpoints:

```http
GET /api/v1/users HTTP/1.1
Host: api.example.com
Authorization: Bearer admin_token
```

Check if each user object in the array contains sensitive fields that should not be returned in bulk listings.

### Test GraphQL for Over-fetching

GraphQL is particularly susceptible because clients can request any available field:

```graphql
# Attempt to request all possible fields
query {
  user(id: "123") {
    id
    username
    email
    password
    passwordHash
    ssn
    creditCard
    internalId
    apiKey
    secretToken
    __typename
  }
}

# Use introspection to discover all available fields
query {
  __type(name: "User") {
    fields {
      name
      type {
        name
      }
    }
  }
}
```

### Test Different Content Types

APIs may return different amounts of data based on content type negotiation:

```http
# Standard JSON response
GET /api/v1/users/123 HTTP/1.1
Accept: application/json

# Try verbose formats
GET /api/v1/users/123 HTTP/1.1
Accept: application/xml

# Try debug or internal formats
GET /api/v1/users/123 HTTP/1.1
Accept: application/json; verbose=true
X-Debug: true
```

### Test Nested Object Exposure

APIs returning nested objects may expose sensitive data in child objects:

```http
GET /api/v1/orders/456 HTTP/1.1
Authorization: Bearer user_token
```

```json
{
  "order_id": 456,
  "items": [...],
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "credit_score": 750,
    "internal_customer_segment": "high-value",
    "fraud_risk_score": 0.02
  },
  "payment": {
    "method": "card",
    "card_number": "4242424242424242",
    "authorization_code": "AUTH123456"
  }
}
```

### Test Error Responses for Data Exposure

Error responses may inadvertently expose sensitive information:

```http
POST /api/v1/users HTTP/1.1
Content-Type: application/json

{"email": "existing@example.com"}
```

Problematic response:

```json
{
  "error": "User already exists",
  "existing_user": {
    "id": 789,
    "email": "existing@example.com",
    "phone": "+1-555-123-4567",
    "created_at": "2022-05-10T08:00:00Z"
  }
}
```

## Indicators of Excessive Data Exposure

- API responses contain fields not displayed in the UI
- Responses include internal identifiers, debugging information, or metadata
- Sensitive PII (SSN, full credit card numbers) appears in responses
- Password hashes or security tokens are returned
- Internal system information (server names, database IDs) is exposed
- Nested objects contain data unrelated to the request context

## Remediation

- **Implement field-level filtering on the server**: Only return fields that the client genuinely needs
- **Use Data Transfer Objects (DTOs)**: Create specific response objects for each endpoint instead of returning complete database models
- **Apply role-based field filtering**: Different users should receive different fields based on their permissions
- **Review and classify data**: Identify and classify sensitive data; create policies for when each field can be returned
- **Use GraphQL field-level authorization**: For GraphQL APIs, implement resolvers that check permissions before returning sensitive fields
- **Avoid generic endpoints**: Create purpose-specific endpoints that return exactly what's needed

## Tools

- **Burp Suite**: Compare responses to identify excessive data
- **Postman**: Create tests to validate response structure
- **GraphQL Voyager**: Visualize GraphQL schema to identify excessive field exposure
- **Custom scripts**: Parse and analyze API responses for sensitive field patterns

## Related Test Cases

- [Testing for Sensitive Information in HTTP Responses](../01-Information_Gathering/05-Review_Web_Page_Content_for_Information_Leakage.md)
- [Testing for Error Handling](../08-Testing_for_Error_Handling/01-Testing_For_Improper_Error_Handling.md)

## References

- [OWASP API Security Top 10: Excessive Data Exposure](https://owasp.org/API-Security/editions/2019/en/0xa3-excessive-data-exposure/)
- [OWASP API Security Top 10 2023: Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [CWE-213: Exposure of Sensitive Information Due to Incompatible Policies](https://cwe.mitre.org/data/definitions/213.html)
