# Testing for Weak Authentication Methods

|ID          |
|------------|
|WSTG-ATHN-07|

## Summary

The most prevalent and most easily administered authentication mechanism is a static password. The password represents the keys to the kingdom, but is often subverted by users in the name of usability. In each of the recent high profile hacks that have revealed user credentials, it is lamented that most common passwords are still: `123456`, `password` and `qwerty`.

Additionally, applications may utilize alternative credentials that are treated the same as a password, but are considerably weaker, such as a birthdates, social security numbers, PINs, or security questions. In some scenarios, these more easily guessed credentials may act as the only user supplied value for authentication.

## Test Objectives

- Determine the resistance of the application against brute force password guessing using available password dictionaries by evaluating the length, complexity, reuse, and aging requirements of passwords.

## How to Test

1. What characters are permitted and forbidden for use within a password? Is the user required to use characters from different character sets such as lower and uppercase letters, digits and special symbols?
2. How often can a user change their password? How quickly can a user change their password after a previous change? Users may bypass password history requirements by changing their password 5 times in a row so that after the last password change they have configured their initial password again.
3. When must a user change their password?
    - Both [NIST](https://pages.nist.gov/800-63-3/sp800-63b.html#memsecretver) and [NCSC](https://www.ncsc.gov.uk/collection/passwords/updating-your-approach#PasswordGuidance:UpdatingYourApproach-Don'tenforceregularpasswordexpiry) recommend **against** forcing regular password expiry, although it may be required by standards such as PCI DSS.
4. How often can a user reuse a password? Does the application maintain a history of the user's previous used 8 passwords?
5. How different must the next password be from the last password?
6. Is the user prevented from using his username or other account information (such as first or last name) in the password?
7. What are the minimum and maximum password lengths that can be set, and are they appropriate for the sensitivity of the account and application?
8. Is it possible to set common passwords such as `Password1` or `123456`?
9. Is the credential chosen for the user by the application, such as a social security number or a birthdate? Is the credential that's utilized in lieu of a standard password easily obtainable, predictable, or susceptible to brute-force attacks?

### API Authentication Methods

APIs utilize various authentication methods beyond traditional passwords. Each has unique weaknesses to test:

#### API Keys

API keys are simple authentication tokens but have several weaknesses:

- **Insufficient entropy**: Keys that are too short or predictable
- **No rotation policy**: Long-lived keys that are never rotated
- **Transmitted insecurely**: Keys sent in URLs (logged in access logs, referrer headers)
- **Overprivileged**: Single key grants access to all API functionality
- **No scope limitation**: Keys cannot be restricted to specific endpoints or methods

Testing approach:
1. Analyze key format and attempt to predict patterns
2. Test if expired or revoked keys are properly rejected
3. Check if keys are exposed in client-side code or documentation
4. Verify keys are transmitted only in headers, not URLs

#### OAuth 2.0 and OpenID Connect

OAuth flows can have implementation weaknesses:

- **Insecure token storage**: Tokens stored in localStorage or cookies without proper security
- **Missing state parameter**: Allows CSRF attacks during OAuth flow
- **Open redirect on callback**: Redirect URI validation can be bypassed
- **Refresh token theft**: Long-lived refresh tokens without binding to client
- **Scope creep**: Tokens granted more scopes than requested

#### JWT (JSON Web Tokens)

JWT has well-known implementation pitfalls:

- **Algorithm confusion**: Accepting `none` algorithm or switching `RS256` to `HS256`
- **Weak signing keys**: Short or predictable secrets for HMAC signing
- **Missing expiration**: Tokens without `exp` claim or very long expiration
- **Missing audience validation**: Tokens accepted across different services
- **Sensitive data in payload**: PII or secrets in the unencrypted payload

See [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md) for detailed JWT testing.

#### Mutual TLS (mTLS)

For APIs using client certificate authentication:

- **Certificate validation bypass**: Server not properly validating client certs
- **Self-signed certificates accepted**: No CA chain validation
- **Revocation not checked**: CRLs or OCSP not verified

#### Basic and Digest Authentication

Legacy authentication methods over APIs:

- **Basic auth over HTTP**: Credentials transmitted in cleartext when TLS not enforced
- **Credential caching**: Browsers caching credentials leading to session confusion
- **No logout mechanism**: No way to invalidate credentials short of changing password

## Remediation

To mitigate the risk of easily guessed passwords facilitating unauthorized access there are two solutions: introduce additional authentication controls (i.e. two-factor authentication) or introduce a strong password policy. The simplest and cheapest of these is the introduction of a strong password policy that ensures password length, complexity, reuse and aging; although ideally both of them should be implemented.

## References

- [Brute Force Attacks](https://owasp.org/www-community/attacks/Brute_force_attack)
