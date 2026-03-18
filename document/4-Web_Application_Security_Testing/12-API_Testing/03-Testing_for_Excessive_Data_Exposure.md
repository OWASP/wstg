# Testing for Excessive Data Exposure

|ID          |
|------------|
|WSTG-APIT-03|

## Summary

Excessive data exposure occurs when an API returns more information in its responses than the client needs to display or function. This commonly happens when developers implement API endpoints by serializing entire backend objects (such as database models or internal data structures) directly into API responses, relying on the client-side code to filter out sensitive fields before presenting them to the user.

The problem is that API responses are directly accessible to anyone who can make requests, regardless of what the user interface chooses to display. An attacker inspecting raw API traffic can observe all returned fields, including those the UI intentionally hides. This can expose passwords, authentication tokens, internal identifiers, personally identifiable information (PII), financial data, infrastructure details, or internal business logic.

This vulnerability maps to [OWASP API Security Top 10 API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/).

## Test Objectives

- Identify API responses that contain more data than what the client application displays or requires.
- Detect sensitive fields returned in API responses such as password hashes, authentication tokens, internal object IDs, PII, or infrastructure details.
- Determine whether the API relies on client-side filtering rather than server-side field selection to control data exposure.

## How to Test

### Compare API Responses Against Displayed Data

The most direct test is to compare what the user interface shows with what the API actually returns.

1. Open the application in a browser and navigate to a page that displays user or object data (e.g., a profile page, an order summary, or a dashboard).
2. Open the browser's developer tools (Network tab) or configure an intercepting proxy such as Burp Suite or ZAP.
3. Identify the API requests that populate the page content.
4. Compare the fields displayed in the UI against the full set of fields in the API response.

For example, a user profile page might display only a name and email, but the underlying API response might return:

```json
{
  "id": 12045,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "password_hash": "$2b$12$LJ3m4ys5qGn...",
  "role": "admin",
  "internal_account_id": "ACC-2024-88421",
  "ssn": "123-45-6789",
  "api_key": "REDACTED_EXAMPLE_KEY_12345",
  "created_by": "system_migration_v2",
  "last_login_ip": "10.0.3.47"
}
```

In this case, the API returns password hashes, social security numbers, API keys, internal identifiers, and internal IP addresses that the UI never displays.

### Inspect Responses Across Different API Endpoints

Do not limit testing to a single endpoint. Check responses from multiple endpoint types:

- **User and account endpoints:** `GET /api/users/{id}`, `GET /api/me`, `GET /api/account`
- **List and search endpoints:** `GET /api/users`, `GET /api/orders?status=completed` (list endpoints frequently return the same full object for every item in the list, amplifying the exposure)
- **Related object endpoints:** `GET /api/orders/{id}` may embed full user objects, payment details, or shipping addresses within the order response
- **Error responses:** Failed requests may return verbose error messages containing stack traces, internal file paths, database query details, or configuration values
- **Administrative or internal endpoints:** Check if endpoints intended for internal use are accessible externally and return elevated data

### Test with Different User Privilege Levels

The same endpoint may return different amounts of data depending on the requesting user's role. Test whether:

- A low-privilege user receives the same fields as an administrator when requesting the same resource.
- An unauthenticated request returns data that should require authentication.
- Requesting another user's data (IDOR) returns the same rich object as requesting your own.

For example, `GET /api/users/124` might return the full object including sensitive fields regardless of whether the requester is user 124, another user, or unauthenticated.

### Analyze Nested and Embedded Objects

Modern APIs frequently embed related objects within responses. A single API call may return deeply nested structures that expose data from multiple backend systems.

Example: An order endpoint returning an embedded customer object, a payment object, and a shipping object:

```json
{
  "order_id": "ORD-9923",
  "items": [...],
  "customer": {
    "id": 5001,
    "name": "Bob Smith",
    "email": "bob@example.com",
    "phone": "+1-555-0199",
    "date_of_birth": "1985-03-14",
    "loyalty_tier": "gold"
  },
  "payment": {
    "method": "card",
    "card_last_four": "4242",
    "card_brand": "Visa",
    "card_fingerprint": "fp_abc123xyz",
    "billing_address": {...}
  },
  "internal_notes": "Customer flagged for manual review - suspected fraud"
}
```

Each nested object should be reviewed for fields that exceed what the consuming client needs.

### Check for Sensitive Data in GraphQL Responses

GraphQL APIs present a specific form of this issue. While GraphQL allows clients to select which fields they want, the schema may expose sensitive fields that the default UI queries do not request but that an attacker can add to a custom query.

1. If introspection is enabled, retrieve the schema and review available fields on each type (see [Testing GraphQL](99-Testing_GraphQL.md)):

    ```graphql
    {
      __type(name: "User") {
        fields {
          name
          type { name }
        }
      }
    }
    ```

2. Look for fields such as `passwordHash`, `apiKey`, `ssn`, `internalId`, `role`, or `isAdmin` that are queryable but not used by the frontend.
3. Attempt to query these fields directly:

    ```graphql
    {
      user(id: "123") {
        name
        email
        passwordHash
        apiKey
        role
      }
    }
    ```

### Examine JavaScript Source Maps and Client-Side Bundles

Frontend JavaScript bundles and source maps can inadvertently reveal the expected API response structure, including fields the UI intentionally hides. If source maps are publicly accessible (e.g., at `main.js.map`), they can expose:

- The full list of fields the frontend expects from API responses
- Internal API endpoint paths
- Authentication and authorization flow logic
- Hardcoded API keys, tokens, or configuration values

Test for source map availability:

```http
GET /static/js/main.js.map
GET /assets/app.js.map
```

If the source map is accessible and contains `sourcesContent`, the original source code can be reconstructed and analyzed for expected API response structures and hidden fields.

### Check Error Responses and Debug Output

APIs may leak sensitive information through error responses, particularly when running in development or debug mode:

- **Stack traces** revealing internal file paths, framework versions, and code structure
- **Database error messages** exposing table names, column names, or query syntax
- **Verbose validation errors** listing all expected fields, including those not documented in the public API
- **Debug headers** such as `X-Debug-Token`, `X-Powered-By`, or custom headers containing internal information

Trigger error responses by sending malformed input, invalid authentication, or requests for non-existent resources, and inspect the full response including headers.

## Remediation

- **Implement server-side response filtering.** Never return raw database objects or full model serializations in API responses. Explicitly define response schemas that include only the fields the client needs for each endpoint and context.
- **Use Data Transfer Objects (DTOs) or serialization allowlists.** Map internal objects to purpose-specific response objects that contain only permitted fields. Most web frameworks provide mechanisms for this (e.g., serializers in Django REST Framework, JsonView in Spring, or ActiveModel::Serializers in Rails).
- **Apply field-level access control.** Some fields (such as email addresses or phone numbers) may be appropriate for one consumer but not another. Implement logic to include or exclude fields based on the requesting user's role and their relationship to the requested resource.
- **Avoid exposing internal identifiers.** Use external-facing identifiers (such as UUIDs or opaque tokens) rather than sequential internal database IDs, which reveal record counts and enable enumeration.
- **Restrict GraphQL schemas.** Remove sensitive fields from the GraphQL schema entirely rather than relying on resolver-level checks. If a field must exist in the schema for internal use, apply authorization directives to prevent unauthorized access.
- **Disable source maps in production.** Do not deploy JavaScript source maps to production environments. Configure the build pipeline to exclude `.map` files from production artifacts.
- **Sanitize error responses.** Return generic error messages in production. Log detailed error information server-side but do not include stack traces, internal paths, or query details in client-facing responses.

## Tools

- **Burp Suite:** Use the Comparer tool to diff displayed UI content against raw API responses. The Repeater and Intruder tools can be used to systematically test endpoints with different parameters and authentication contexts.
- **ZAP (Zed Attack Proxy):** Intercept and inspect API responses, use active scan rules to identify information disclosure, and fuzzing capabilities to trigger verbose error responses.
- **Postman:** Send API requests with different authentication tokens and compare response bodies to identify role-dependent data exposure differences.
- **Browser Developer Tools:** The Network tab provides immediate visibility into API responses without requiring a proxy setup. Useful for quick comparison of UI-rendered data vs raw response content.
- **jq:** Command-line JSON processor for extracting and comparing fields across API responses: `curl -s https://api.example.com/users/me | jq 'keys'` lists all returned fields.

## References

- [OWASP API Security Top 10: API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [OWASP ASVS V5: API and Web Service](https://github.com/OWASP/ASVS/blob/v5.0.0/5.0/en/0x13-V4-API-and-Web-Service.md)
- [Testing for Insecure Direct Object References (IDOR)](../05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md)
