# Passkeys and WebAuthn

|ID          |
|------------|
|WSTG-ATHN-13|

## Summary

[Web Authentication (WebAuthn)](https://www.w3.org/TR/webauthn-3/) is a browser standard that lets a website sign users in with public-key cryptography instead of, or in addition to, a password. A passkey is a WebAuthn credential that the user can use across devices, usually synced by the platform or kept on a security key.

During registration, the user's authenticator creates a key pair for the website and the website (the relying party, RP) stores the public key. During authentication, the RP sends a random challenge, the authenticator signs it, and the RP checks the signature. The private key never leaves the authenticator, and the credential is bound to the RP ID (normally the site's domain), so it cannot be used on a look-alike site.

These properties remove most password attacks. The weaknesses that remain are in how the RP implements the checks, and in the paths around passkeys, such as account recovery and fallback to weaker methods. An attacker who cannot defeat a passkey will use those paths instead.

This page covers what is specific to WebAuthn. For second-factor use of other methods, see [Multi-Factor Authentication](11-Multi-Factor_Authentication.md). For recovery flows, see [Weak Password Change or Reset Functionalities](09-Weak_Password_Change_or_Reset_Functionalities.md).

## Test Objectives

- Determine whether the RP verifies the challenge, origin and RP ID on registration and authentication.
- Assess whether recovery and fallback paths weaken the protection that passkeys provide.
- Determine whether adding, listing and removing credentials is protected.
- Assess how the RP handles user identification and the data it stores for credentials.

## How to Test

### Observe the Registration and Authentication Calls

Use the browser developer tools and an intercepting proxy to follow a registration and a login. The browser calls `navigator.credentials.create()` and `navigator.credentials.get()`; the application usually exchanges the options and results with its server as JSON or binary data. Chromium-based browsers have a WebAuthn panel in the developer tools that can create a virtual authenticator, which makes the flows repeatable without hardware.

Note the following in the options the server sends:

- `challenge`: a new random value on each ceremony.
- `rpId` (or `rp.id`): the RP ID, which should be the application's domain or a registrable suffix of it.
- `userVerification`: `required`, `preferred` or `discouraged`.
- `allowCredentials`: whether the server lists the credentials of the account being signed in.
- `user.id` (registration): an opaque, stable handle for the user.

### Test Challenge Handling

Send the login response again after the login has completed, or with a response from a previous ceremony. The server should reject each of the following:

- A response replayed after it has been used once.
- A response that signs a challenge issued earlier, or for a different session.
- A response with the `challenge` in `clientDataJSON` changed.

Check that the challenge is generated on the server, is unpredictable, is tied to the session or user that started the ceremony, and expires quickly.

### Test Origin and RP ID Validation

In the `clientDataJSON` of a response, change the `origin` or the `type` (for example `webauthn.create` instead of `webauthn.get`) and send it. Also change the RP ID hash at the start of `authenticatorData`. The server should reject each change. If any is accepted, the RP does not validate the data that binds a credential to its site.

What a rejected change shows depends on the ceremony:

- For registration with `attestation: "none"`, the usual setting for passkeys, the response is not signed at all, so editing these values tests the RP's own checks directly.
- For authentication, the signature covers these values, so a rejected edit only shows that the signature is verified, not that the `origin` is checked. To test the origin check on its own, create a validly signed response with a different origin, using a virtual authenticator or a test harness that holds the key.

Two more inputs affect which origins the RP accepts:

- **Cross-origin iframes:** a page on another origin can call WebAuthn from an iframe if it is allowed by the `publickey-credentials-get` permissions policy. The browser then sets `crossOrigin` to `true` in `clientDataJSON` and, in newer browsers, adds the `topOrigin`. Check whether the RP accepts such responses, and if it does, whether it is meant to be embedded by those origins.
- **Related origins:** an RP can let other origins use its RP ID by listing them in a JSON file at `https://<rp-id>/.well-known/webauthn`. If the file exists, check that every origin in it belongs to the organization, and that the server accepts only those origins in `clientDataJSON`.

### Test Assertion Checks

- **User presence and verification:** if the application requires user verification (PIN or biometric), check that a response with the user-verified flag not set is rejected.
- **Signature counter:** if the authenticator reports a counter, check how the server handles a counter that does not increase. Many authenticators, such as synced passkeys, always report zero, so the server should not reject those, but should log or act on a counter that goes backwards when it was previously non-zero.
- **Credential ID:** send a response for a credential that belongs to a different account and check that the server matches the credential to the account it is signing in.
- **Backup flags:** the `authenticatorData` flags include backup eligibility (BE) and backup state (BS), which show whether a passkey is synced. If the RP treats synced and device-bound passkeys differently, check that it reads these flags and that a credential cannot change from device-bound to synced without the RP noticing.
- **Authenticator type:** some RPs only allow certain authenticator models, which they identify by the AAGUID in the registration data. With `attestation: "none"` the AAGUID is not signed, so change it during registration and check whether the restriction can be bypassed. An RP that relies on the model must request attestation and verify it, for example against the FIDO Metadata Service.

### Test Fallback and Recovery Paths

A passkey protects an account only if the other ways in are as strong.

- Check whether the login page offers a password, SMS code, email link or security questions in addition to the passkey, and whether an attacker can choose the weaker method for an account that has a passkey.
- Check whether the recovery flow for a lost passkey asks for less proof than the passkey provides (for example an email link only). See [Weak Password Change or Reset Functionalities](09-Weak_Password_Change_or_Reset_Functionalities.md) and [Weak Security Question Answer](08-Weak_Security_Question_Answer.md).
- Check whether registering a passkey is possible during recovery, without the old credentials being cancelled, and whether the user is told.
- Check that the account lock-out and rate limits apply to the fallback methods. See [Weak Lock Out Mechanism](03-Weak_Lock_Out_Mechanism.md).

### Test Credential Management

- Registering a new passkey should require a recent authentication or another proof from the user, and the user should be notified.
- Listing and removing credentials should be limited to the account owner. Try identifiers belonging to another account.
- Removing the last passkey should not leave the account without a safe way in, and should not silently fall back to a weaker method.
- Check that the same credential ID cannot be registered against two accounts.

### Test User Identification

- Check that `user.id` is an opaque value that does not contain personal data such as an email address.
- Check that registering a credential cannot overwrite the `user.id` or credential of another user, for example by sending a modified `user` object in the registration request.
- Check whether the login with `allowCredentials` reveals which accounts exist or which have passkeys (user enumeration). See [Account Enumeration and Guessable User Account](../03-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account.md).

## Remediation

- Generate a new random challenge on the server for each ceremony, bind it to the session, and accept it once.
- Verify the origin, RP ID hash, ceremony type, signature and credential on every response, using a maintained WebAuthn library.
- Require user verification for sensitive actions, and decide explicitly how the signature counter is handled.
- Make recovery and fallback methods at least as strong as the passkey, or limit what an account recovered with a weaker method can do.
- Require recent authentication to add or remove credentials, and notify the user of changes.
- Use opaque, random user handles, and give the same response for accounts with and without passkeys.
- Reject cross-origin responses unless the RP is meant to be embedded, and list only origins the organization controls in `/.well-known/webauthn`.
- Only rely on the authenticator model when attestation is requested and verified.

## Tools

- Chromium DevTools WebAuthn panel (virtual authenticators)
- [Burp Suite](https://portswigger.net/burp)
- [ZAP](https://www.zaproxy.org/)
- [webauthn.io](https://webauthn.io/) (a demo RP for comparing behavior)

## References

- [W3C: Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/)
- [FIDO Alliance: Passkeys](https://fidoalliance.org/passkeys/)
- [MDN: Web Authentication API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API)
- [OWASP: Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [passkeys.dev: Related Origin Requests](https://passkeys.dev/docs/advanced/related-origins/)
