# OpenID Connect Relying Party

|ID          |
|------------|
|WSTG-ATHN-14|

## Summary

[OpenID Connect (OIDC)](https://openid.net/specs/openid-connect-core-1_0.html) layers identity on top of OAuth 2.0. An OAuth client that accepts an ID Token, UserInfo claims, or a social-login assertion to create or recover a local session is an OpenID Connect relying party (RP), not only an OAuth client.

OAuth chapters in this guide cover delegated authorization: grant types, PKCE, redirect URIs, and token leakage. They do not provide a procedure for authenticating a user from an ID Token. Failures in relying-party validation lead to account takeover, account linking to the wrong local user, and login with unverified identity claims.

This test evaluates the RP. Treat the identity provider (OP) as a separate system unless the engagement also includes that OP. Cross-link [OAuth Weaknesses](../05-Authorization/05-OAuth_Weaknesses.md) for grant-type and PKCE issues, and [JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md) for generic JWT cryptography.

> Note: Open PRs may add SAML (`WSTG-ATHN-12`) and WebAuthn (`WSTG-ATHN-13`). This article uses `WSTG-ATHN-14` so those additions can land without a numbering collision. Maintainers may renumber after merge.

## Test Objectives

- Confirm the RP validates issuer discovery, ID Token signatures, and authentication claims before creating a session.
- Confirm account identity is bound to `(iss, sub)`, not to email alone.
- Confirm account-linking and recovery flows cannot attach an attacker-controlled identity to another user's account.
- Confirm mix-up defenses when the RP can use more than one OP.

## How to Test

Use only tester-owned accounts at both the RP and any lab identity provider. Do not target production users.

### 1. Map the OIDC Surface

1. Identify authorization requests that include `scope=openid` or that return an `id_token`.
2. Capture the discovery document when present (`/.well-known/openid-configuration`) and record `issuer`, `jwks_uri`, `authorization_endpoint`, and `token_endpoint`.
3. Distinguish:
   - Login with an external OP.
   - Linking an external identity to an already authenticated local account.
   - Account recovery that trusts an OP email claim.

### 2. Discovery and Issuer Binding

1. If the RP performs discovery from a client-supplied issuer or identifier, point discovery at a tester-controlled HTTPS metadata document only.
2. Confirm the RP pins the expected issuer and does not follow attacker-controlled `authorization_endpoint` or `token_endpoint` values from untrusted metadata.
3. When dynamic registration or multi-OP login is supported, start a login toward OP A and complete the callback as if it came from OP B. The RP must detect the mismatch. See [RFC 9207](https://datatracker.ietf.org/doc/html/rfc9207) and [RFC 9700 Section 4.4](https://datatracker.ietf.org/doc/html/rfc9700#section-4.4).

### 3. ID Token Validation Matrix

Obtain a legitimate ID Token for a tester account, then mutate one claim or condition at a time before the RP consumes it. Prefer a lab OP or a replay against a local RP build. Do not attempt to forge production OP signatures.

| Mutation | Expected secure result |
|----------|------------------------|
| Wrong `iss` | Reject |
| Wrong or missing `aud` / unexpected `azp` | Reject |
| Expired `exp` or future `nbf`/`iat` outside skew | Reject |
| Replayed `nonce` or missing `nonce` when the RP sent one | Reject |
| Algorithm `none` or an unexpected algorithm | Reject |
| Signature created with a different key | Reject |
| Token substituted from another tester account | Session for the substituted subject must not be created under the victim's local account |

Also send the access token to the UserInfo endpoint, then present UserInfo claims for subject B while the ID Token subject is A. The RP must correlate UserInfo `sub` with the authenticated ID Token `sub`.

### 4. Email and Account-Linking Lifecycle

OIDC email claims are not a stable account primary key.

1. **Unverified email:** With a lab OP that can omit or set `email_verified=false`, attempt login or linking. The RP must not create or merge an account solely from an unverified email.
2. **Pre-account collision:** Register a local account using tester B's email if the RP allows unverified registration. Before B verifies, attach tester A's OP identity to that account. After B verifies or recovers the account, A's OP login must not remain attached unless B explicitly re-links it.
3. **Session-bound linking:** While authenticated as local account A, start "connect external identity." Complete the OP consent in a browser that is authenticated to the RP as local account B. The callback must not attach B's OP identity to A. Bind the linking `state` (and PKCE/`nonce` when used) to the initiating local session and purpose.
4. **Identifier change:** Change the local account email from address X to Y, then attempt old email-verification, reset, or linking tokens minted for X. They must be invalid after the identity transition.
5. **Stable subject:** Prefer `(iss, sub)`. Two OPs asserting the same email must not merge accounts automatically.

### 5. Session Creation and Step-Up

1. Confirm the RP creates its own session after validating the ID Token, and that logout or password change invalidates that session.
2. If MFA is required for local password login, attempt OP login paths that skip MFA. See [Multi-Factor Authentication](11-Multi-Factor_Authentication.md).
3. Confirm logout at the RP does not leave a reusable RP-side artifact that silently re-creates a session from a still-valid OP cookie without revalidation when that behavior is not intended.

## Remediation

- Validate ID Tokens per [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html): `iss`, `aud`, `exp`, signature, algorithm allowlist, and `nonce` when used.
- Key local accounts on `(iss, sub)`. Treat email as a contact attribute that requires verification before linking or recovery.
- Bind account-linking transactions to the authenticated local session that started them.
- Invalidate outstanding verification, reset, and linking artifacts when the primary identifier changes.
- Implement mix-up defenses when more than one OP is supported.

## Related Test Cases

- [OAuth Weaknesses](../05-Authorization/05-OAuth_Weaknesses.md)
- [OAuth Authorization Server Weaknesses](../05-Authorization/05.1-OAuth_Authorization_Server_Weaknesses.md)
- [OAuth Client Weaknesses](../05-Authorization/05.2-OAuth_Client_Weaknesses.md)
- [JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md)
- [Weak Password Change or Reset Functionalities](09-Weak_Password_Change_or_Reset_Functionalities.md)
- [Multi-Factor Authentication](11-Multi-Factor_Authentication.md)

## Tools

- [Zed Attack Proxy](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)
- [jwt_tool](https://github.com/ticarpi/jwt_tool)

## References

- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html)
- [RFC 9207 - OAuth 2.0 Authorization Server Issuer Identification](https://datatracker.ietf.org/doc/html/rfc9207)
- [RFC 9700 - OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/rfc9700)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
