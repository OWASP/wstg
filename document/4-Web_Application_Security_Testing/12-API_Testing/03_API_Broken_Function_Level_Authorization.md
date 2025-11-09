# API Broken Function Level Authorization

|ID          |
|------------|
|WSTG-APIT-03|

## Summary

Broken Function Level Authorization (BFLA) occurs when an API improperly enforces restrictions on users accessing certain functions or operations. This vulnerability allows attackers to invoke sensitive functions they are not authorized to execute, such as administrative functions or other high-privilege operations.

BFLA commonly arises when APIs expose multiple endpoints that serve different user roles (e.g., user vs. admin) but fail to restrict access to these functions based on the user's authorization level.

Exploiting BFLA can lead to serious consequences such as privilege escalation, unauthorized access to sensitive functions (e.g., administrative operations), or exposure of critical functionalities that should only be accessible to specific user roles.

## Test Objectives

- The goal of this test is to determine if the API enforces **role or privilege-based access control** to restrict users from accessing or executing functions they are not authorized to use. This ensures that function-level security boundaries are properly enforced.

## How to Test

### Identify Function-Level Endpoints

Review API documentation (e.g. OpenAPI specification), traffic, or use an interception proxy (e.g., **Burp Suite**, **ZAP**) to identify different function-level endpoints. These might include:
  
- **Administrative functions** (e.g., `/api/admin/deleteUser`, `/api/admin/getAllUsers`)

- **Role-based operations** (e.g., `/api/admin/promoteUser`, `/api/user/createOrder`)

- **Critical functions** for users (e.g., `/api/user/withdrawFunds`)

Focus on **functionality differences** between different user roles (e.g., regular user, admin, partner, guest) and endpoints that offer more sensitive capabilities.

### Manipulate Role-Based Access Controls

Try to access or perform sensitive operations exposed in API endpoints that should be restricted based on user roles.

Log in as a lower-privilege user (e.g., guest or regular user) and send requests to endpoints that perform sensitive actions reserved for higher-privilege roles (e.g., admin).

Example: as a **regular user**, send a request to the following administrative endpoint to delete a random user:

```http
POST /api/admin/deleteUser
Authorization: Bearer <regular_user_token>

{ "userId": "12345" }
```

### Test Function-Level Access with Different HTTP Methods

Test various **HTTP methods** for BFLA vulnerabilities:

- **GET**: Attempt to access information available only to high-privilege users (e.g., administrators).

Example: `GET /api/admin/getAllUsers`

- **POST/PUT/PATCH**: Attempt to modify or create sensitive resources (e.g., changing user roles, creating or deleting system-critical data).

Example: `POST /api/admin/promoteUser { "userId": "12345", "newRole": "admin" }`

- **DELETE**: Attempt to delete sensitive resources, such as removing user accounts or data.

Example: `DELETE /api/admin/deleteUser/12345`

### Test for BFLA in GraphQL APIs

In **GraphQL APIs**, test if a user can invoke functions restricted to higher-privilege roles by modifying GraphQL queries.

Example: `mutation { deleteUser(id: "12345") { success } }`.

## Indicators of BFLA

- **Successful exploitation**: If a lower-privilege user (e.g., regular user or guest) can execute high-privilege functions or perform actions reserved for other roles (e.g., admin).
- **Error responses**: Properly secured APIs in general would return `403 Forbidden` or `401 Unauthorized` when invoked restricted functions instead of a `200 OK` response.
- **Inconsistent enforcement**: Some endpoints enforce role-based restrictions while others do not, which indicates inconsistent security controls.

## Remediations

To prevent BFLA vulnerabilities, implement the following mitigations:

- **Enforce Role-Based Access Control (RBAC)**: Ensure that the API checks user roles and permissions at the **function level** before allowing access to certain operations. Only authorized roles should be allowed to invoke sensitive functions.
- **Least Privilege Principle**: Apply the principle of least privilege by ensuring that users can only access the minimum set of functions they need for their role.
- **Centralized Access Control Logic**: Use centralized access control logic to ensure consistency across all API endpoints. This avoids gaps where some functions may lack proper access checks.

## Tools

- **ZAP**: Use automated scanners and manual proxy tools to inspect API requests and responses for BFLA vulnerabilities.
- **Burp Suite**: Use **Repeater** or **Intruder** to send requests as lower-privilege users to test if function-level restrictions are enforced.
- **Postman**: Manually send API requests as different user roles and observe responses.
- **Fuzzing Tools**: Use fuzzers to test different function parameters and methods to identify potential authorization weaknesses.

## References

- [OWASP API Security Top 10: BFLA](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)
- [OWASP Testing Guide: Testing for Privilege Escalation](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/05-Authorization_Testing/03-Testing_for_Privilege_Escalation)
- [OWASP Testing Guide: Testing for GraphQL](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL)
