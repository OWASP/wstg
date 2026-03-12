# Testing for Broken Function Level Authorization

|ID          |
|------------|
|WSTG-APIT-03|

## Summary

Broken Function Level Authorization (BFLA) occurs when an API fails to properly verify that the authenticated user has permission to perform a specific function or access a particular endpoint. Unlike Broken Object Level Authorization (BOLA), which focuses on access to individual data objects, BFLA is concerned with access to functionality—particularly administrative or privileged operations.

This vulnerability is prevalent in APIs because:

- APIs often expose more methods and endpoints than traditional web applications
- API architectures may have complex permission hierarchies that are inconsistently enforced
- Administrative functions may be "hidden" but not properly secured
- Legacy API endpoints may lack proper authorization checks

Exploiting BFLA can allow attackers to:

- Access administrative functions without proper privileges
- Perform unauthorized operations (create, modify, delete)
- Escalate privileges from regular user to administrator
- Access internal or debug functionality

## Test Objectives

- Identify endpoints that perform privileged or administrative functions
- Verify that proper function-level authorization is enforced for all endpoints
- Test for privilege escalation by accessing functions beyond assigned permissions

## How to Test

### Map Administrative and Privileged Endpoints

First, identify endpoints that perform sensitive or privileged functions:

1. **Review API documentation**: Look for endpoints in OpenAPI/Swagger specs marked as admin-only or requiring elevated permissions
2. **Analyze endpoint naming patterns**: Look for patterns like:
   - `/api/admin/*`
   - `/api/v1/management/*`
   - `/api/internal/*`
   - `/api/debug/*`
3. **Monitor privileged user traffic**: If you have access to an admin account, record all API calls and note admin-specific endpoints
4. **Check response headers**: Some APIs return permission information or available actions in headers

### Test Access to Administrative Functions

With a low-privileged or anonymous user, attempt to access administrative endpoints:

```http
# Example: Attempt to access user management as a regular user
GET /api/admin/users HTTP/1.1
Host: api.example.com
Authorization: Bearer regular_user_token
```

```http
# Example: Attempt to create a new admin account
POST /api/admin/users HTTP/1.1
Host: api.example.com
Authorization: Bearer regular_user_token
Content-Type: application/json

{
  "username": "newadmin",
  "role": "administrator",
  "email": "attacker@example.com"
}
```

### Test HTTP Method Variations

Some APIs may allow certain HTTP methods but not others:

```http
# DELETE might be blocked
DELETE /api/v1/products/123 HTTP/1.1
Authorization: Bearer user_token

# But PUT with destructive action might work
PUT /api/v1/products/123 HTTP/1.1
Authorization: Bearer user_token
Content-Type: application/json

{"status": "deleted", "active": false}
```

### Test Parameter-Based Function Selection

Some APIs use parameters to determine which function to execute:

```http
# Regular action (allowed)
POST /api/v1/orders HTTP/1.1
Content-Type: application/json

{"action": "create", "product_id": 123}

# Administrative action (should be blocked for regular users)
POST /api/v1/orders HTTP/1.1
Content-Type: application/json

{"action": "delete_all", "confirm": true}
```

### Test GraphQL Function-Level Authorization

In GraphQL APIs, test access to administrative mutations and queries:

```graphql
# Test access to admin mutations
mutation {
  deleteAllUsers(confirm: true) {
    success
    deletedCount
  }
}

# Test access to system configuration
query {
  systemConfig {
    databaseConnection
    apiKeys
    secretSettings
  }
}
```

### Test for Debug and Internal Endpoints

APIs may expose debug or internal endpoints that should not be accessible:

- `/api/debug/logs`
- `/api/internal/metrics`
- `/api/health/detailed`
- `/api/swagger` or `/api/docs` (if these should be restricted)

```http
GET /api/debug/environment HTTP/1.1
Host: api.example.com
Authorization: Bearer regular_user_token
```

### Test Role Manipulation

Attempt to modify user roles through API calls:

```http
# Attempt self-promotion to admin
PATCH /api/v1/users/me HTTP/1.1
Authorization: Bearer regular_user_token
Content-Type: application/json

{"role": "admin", "permissions": ["all"]}
```

## Indicators of BFLA

- **Successful access**: If a low-privileged user can access administrative endpoints, the API is vulnerable
- **Inconsistent responses**: Some admin functions work while others don't, indicating incomplete authorization
- **Error message disclosure**: Detailed error messages revealing internal function names or missing permissions
- **HTTP 200 instead of 403**: Successful responses where access should be denied

## Remediation

- **Implement consistent authorization checks**: Verify permissions for every function call, not just at the route level
- **Use role-based access control (RBAC)**: Define clear roles and enforce them consistently across all endpoints
- **Deny by default**: All endpoints should require explicit authorization; deny access unless explicitly granted
- **Centralize authorization logic**: Use a centralized authorization component to ensure consistent enforcement
- **Log and monitor**: Log all access attempts to sensitive functions for audit purposes

## Tools

- **ZAP**: Use the fuzzer to test access to administrative endpoints
- **Burp Suite**: Use Repeater to test authorization on different endpoints; Autorize extension for automated testing
- **Postman**: Create collections with different user tokens to test access
- **Custom scripts**: Automate testing of endpoint lists with different permission levels

## Related Test Cases

- [API Broken Object Level Authorization](02-API_Broken_Object_Level_Authorization.md)
- [Testing for Bypassing Authorization Schema](../05-Authorization_Testing/02-Testing_for_Bypassing_Authorization_Schema.md)
- [Testing for Privilege Escalation](../05-Authorization_Testing/03-Testing_for_Privilege_Escalation.md)

## References

- [OWASP API Security Top 10: Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [CWE-285: Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)
