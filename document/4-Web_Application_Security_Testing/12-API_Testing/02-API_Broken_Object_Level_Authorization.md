# API Broken Object Level Authorization

|ID          |
|------------|
|WSTG-APIT-02|

## Summary

Broken Object Level Authorization (BOLA) occurs when an API does not properly enforce authorization checks for each object accessed by the client. Attackers can manipulate object identifiers in API requests (such as IDs, GUIDs, or tokens) to access or modify resources they are not authorized to. This vulnerability is critical in APIs due to their direct access to underlying objects and the prevalence of APIs in modern applications.

Exploiting BOLA can lead to unauthorized access to sensitive data, user impersonation, horizontal privilege escalation (accessing other users' resources), and vertical privilege escalation (gaining unauthorized admin-level access).

## Test Objectives

- The objective of this test is to identify whether the API enforces proper **object-level authorization** checks, ensuring that users can only access and manipulate objects they are authorized to interact with.

## How to Test

### Understand API Endpoints and Object References

Review API documentation (e.g. OpenAPI specification), traffic, or use an interception proxy (e.g., **Burp Suite**, **ZAP**) to identify endpoints that accept object identifiers of interest. These could be in the form of **IDs**, **UUIDs**, or other references.

Examples:

- `GET /api/users/{user_id}`
- `GET /api/orders/{order_id}`
- `POST /graphql`\
        `query: {user(id: "123") }`

With the knowledge gained in the previous step, review and collect third-party object identifiers (e.g. user IDs, orders IDs etc) that can be used subsequently in the object identifiers manipulation.

Additionaly, generate a list of potential object identifiers for brute-force. For example, if an API is retrieving a purchase order from an authenticated user, generate various purchase order IDs for testing.

### Manipulate Object Identifiers in API Requests

With the goal to determine if users can access or modify objects they do not own by altering object identifiers in API request, change the object identifier (e.g., user ID, order ID) in the URL or request body.
  
Example: Modify a request like `GET /api/users/123/profile` (where 123 is the current user ID) to `GET /api/users/124/profile` (where 124 is another user's ID).

Depending on the application context, utilize two different accounts to perform the tests. With an account A, create resources that exclusively belongs to that account (e.g. purchase order) and with an account B, try to access the resource from account A (e.g. purchase order).

### Test Object-Level Access with Different HTTP Methods

Test various **HTTP methods** for BOLA vulnerabilities:

- **GET**: Try accessing unauthorized objects by manipulating the object ID in the request.
- **POST/PUT/PATCH**: Attempt to create or modify objects that belong to other users.
- **DELETE**: Try to delete an object owned by another user.

### Test BOLA in GraphQL APIs

For **GraphQL APIs**, send a query with a modified object ID in the query parameters (see [Testing GraphQL](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL)):

Example: `query { user(id: "124") { name, email } }`.

### Test for Bulk Object Access

Test if the API allows unauthorized **bulk access** to objects. This could happen in endpoints that return lists of objects.

Example: `GET /api/users` returns data for all users instead of only the authenticated user’s data.

## Indicators of BOLA

- **Successful exploitation**: If modifying an object ID in the request returns data or allows actions on objects that belong to other users, the API is vulnerable to BOLA.
- **Error responses**: Properly secured APIs in general would return `403 Forbidden` or `401 Unauthorized` for unauthorized object access. A `200 OK` response for another user's object indicates BOLA.
- **Inconsistent responses**: If some endpoints enforce authorization and others do not, it points to incomplete or inconsistent security controls.

## Remediation

- **Object Ownership Checks**: Ensure that object-level authorization checks are performed for every API request. Always verify that the user making the request is authorized to access the requested object.
- **Role-Based Access Control (RBAC)**: Implement RBAC policies that define which roles can access or modify specific objects.
- **Least Privilege Principle**: Apply the principle of least privilege to ensure that users can only access the minimum set of objects they need for their role.
- **Use UUIDs or Non-Sequential IDs**: Prefer non-predictable, non-sequential object identifiers (e.g., **UUIDs** instead of simple integers) to make enumeration and brute-force attacks harder.

## Tools

- **ZAP**: Automated scanners or manual proxy tools can help test object references in API requests.
- **Burp Suite**: Use the **Repeater** or **Intruder** tools to manipulate object IDs and send multiple requests to test access control.
- **Postman**: Send requests with altered object IDs and observe the responses.
- **Fuzzing Tools**: Use fuzzers to brute-force object IDs and check for unauthorized access.

## References

- [OWASP API Security Top 10: BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP Testing Guide: Testing for Insecure Direct Object References (IDOR)](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)
- [OWASP Testing Guide: Testing for GraphQL](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/12-API_Testing/01-Testing_GraphQL)  
