# Testing Multi-Factor Authentication (MFA)

|ID          |
|------------|
|WSTG-ATHN-11|

## Summary

Many applications implement Multi-Factor Authentication (MFA) as an additional layer of security to protect the login process. This is also known as two-factor authentication (2FA) or two-step verification (2SV) - although these are not strictly the same thing. MFA means asking the user to provide *at least* two different [authentication factors](#types-of-mfa) when logging in.

MFA adds additional complexity to both the authentication functionality, and also to other security-related areas (such as credential management and password recovery), meaning that it is critical for it to be implemented in a correct and robust manner.

## Test Objectives

- Identify the type of MFA used by the application.
- Determine whether the MFA implementation is robust and secure.
- Attempt to bypass the MFA.

## How to Test

### Types of MFA

MFA means that *at least* two of the following factors are required to authentication:

| Factor | Examples |
|--------|----------|
| Something You Know | Passwords, PINs and security questions. |
| Something You Have | Hardware or software tokens, certificates, email*, SMS, and phone calls. |
| Something You Are | Fingerprints, facial recognition, iris scans, handprint scans and behavioural factors. |
| Location | Source IP ranges, and geolocation. |

\* Email only really constitutes "something you have" if the email account itself is protected with MFA. As such, it should be considered weaker than other alternatives such as certificates or TOTP, and may not be accepted as MFA under some definitions.

Note that requiring multiple examples of a single factor (such as needing both a password and a PIN) **does not constitute MFA**, although it may provide some security benefits over a simple password, and may be considered two-step verification (2SV).

Due to the complexity of implementing biometrics in a browser-based environment, "Something You Are" is rarely used for web applications, although it is starting to be adopted using standards such as WebAuthn. The most common second factor is "Something You Have".

### Check for MFA Bypasses

The first step for testing MFA is to identify all of the authentication functionality in the application, which may include:

- The main login page.
- Security critical functionality (such as disabling MFA or changing a password).
- Federated login providers.
- API endpoints (from both the main web interface and mobile apps).
- Alternative (non-HTTP) protocols.
- Test or debug functionality.

All of the different login methods should be reviewed, to ensure that MFA is enforced consistently. If some methods do not require MFA, then these can provide a simple method to bypass them.

If the authentication is done in multiple steps then it may be possible to bypass it by completing the first step of the authentication process (entering the username and password), and then force-browsing to the application or making direct API requests without completing the second stage (entering the MFA code).

In some cases, there may also be intentional MFA bypasses implemented, such as not requiring MFA:

- From specific IP addresses (which may be spoofable using the `X-Forwarded-For` HTTP header).
- When a specific HTTP header is set (such as a non-standard header like `X-Debug`).
- For a specific hard-coded account (such as a "root" or "breakglass" account).

Where an application supports both local and federated logins, it may be possible to bypass the MFA if there is no strong separation between these two types of accounts. For example, if a user registers a local account and configures MFA for it, but does not have MFA configured on their account on the federated login provider, it may be possible for an attacker to re-register (or link) a federated account on the target application with the same email address by compromising the user's account on the federated login provider.

Finally, if the MFA is implemented on a different system to the main application (such as on a reverse proxy, in order to protect a legacy application that does not natively support MFA), then it may be possible to bypass it by connecting directly to the backend application server, as discussed in the guide on how to [map the application architecture](../01-Information_Gathering/10-Map_Application_Architecture.md#content-delivery-network-cdn).

### Check MFA Management

The functionality used to manage MFA from inside the user's account should be tested for vulnerabilities, including:

- Is the user required to re-authenticate to remove or change MFA settings?
- Is the MFA management functionality vulnerable to [cross-site request forgery](../06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md)?
- Can other users' MFA setting be modified through [IDOR vulnerabilities](../05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md)?

### Check MFA Recovery Options

Many applications will provide users with a way to regain access to their account if they are unable to authenticate with their second factor (for example if they have lost their phone). These mechanisms can often represent a significant weakness in the application, as they effectively allow the second authentication factor to be bypassed.

#### Recovery Codes

Some applications will provide the user with a list of recovery or backup codes when they enable MFA, which can be used to login. These should be checked to ensure:

- They are sufficiently long and complex to protect against brute-force attacks.
- They are securely generated.
- They can only be used once.
- Brute-force protection is in place (such as account lockout).
- The user is notified (via email, SMS, etc) when a code is used.

See the ["Backup Codes" section in the Forgotten Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html#backup-codes) for further details.

#### MFA Reset Process

If the application implements an MFA reset process, this should be tested in the same way that the [password reset process](09-Testing_for_Weak_Password_Change_or_Reset_Functionalities.md) is tested. It is important that this process is *at least* as strong as the MFA implementation for the application.

#### Alternative Authentication

Some applications will allow the user to prove their identity through other means, such as the use of [security questions](08-Testing_for_Weak_Security_Question_Answer.md). This usually represents a significant weakness, as security questions provide a far lower level of security than MFA.

### One-Time Passwords

The most common form of MFA is the one of One-Time Passwords (OTPs), which are typically six-digit numeric codes (although they can be longer or shorter). These can either be generated by both the server and the user (for example, with an authenticator app), or can be generated on the server and sent to the user. There are various ways that this OTP can be provided to the user, including:

| Type | Description |
|------|-------------|
| HMAC One-Time Password (HOPT) | Generates a code based on the HMAC of a secret and a shared counter. |
| Time-based One-Time Password (TOTP) | Generates a code based on HMAC of a secret and the current time. |
| Email | Sends a code via email. |
| SMS | Sends a code via SMS. |
| Phone | Sends a code via a voice call to a phone number. |

The OTP is typically entered after the user has provided their username and password. There are various checks that should be performed, including:

- Is the account locked out after multiple failed MFA attempts?
- Is the user's IP address blocked after multiple failed MFA attempts across different accounts?
- Are failed MFA attempts logged?
- Is the form vulnerable to injection attacks, including [SQL wildcard injection](../07-Input_Validation_Testing/05-Testing_for_SQL_Injection.md#sql-wildcard-injection)?

Depending on the type of OTPs used, there are also some other specific checks that should be performed:

- How are OTPs sent to user (email, SMS, phone, etc)
    - Is there rate limiting to prevent SMS/phone spam costing money?
- How strong are OTPs (length and keyspace)?
- How long are OTPs valid for?
- Are multiple OTPs valid at once?
- Can the OTPs be used more than once?
- Are the OTPs tied to the correct user account or is it possible to authenticate with them on other accounts?

#### HOTP and TOTP

HOTP and TOTP codes are both based on a secret that is shared between the server and the user. For TOTP codes, this is usually provided to the user in the form of a QR code that they scan with an authenticator app (although it can also be provided as a text secret for them to manually enter).

Where the secret is generated on the server, it should be checked to ensure that it is sufficiently long and complex ([RFC 4226](https://www.rfc-editor.org/rfc/rfc4226#section-4) recommends at least 160 bits), and that it is generated using a [secure random function](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#secure-random-number-generation).

Where the secret can be provided by the user, an appropriate minimum length should be enforced, and the input should be checked for the usual injection attacks.

TOTP codes are typically valid for 30 seconds, but some applications choose to accept multiple codes (such as the previous, current, and next codes) in order to deal with differences between the system time on the server and on the user's device. Some applications may allow multiple codes on either side of the current one, which may make it easier for an attacker to guess or brute-force the code. The table below shows the chance of successfully brute-forcing an OTP code based on an attacker being able to make 10 requests a second, for applications that accept either only the current code, or multiple codes (see [this article](https://www.codasecurity.co.uk/articles/mfa-testing#case-study---brute-forcing-totp) for the calculations behind the table).

| Valid Codes | Success rate after 1 hour | Success rate after 4 hours | Success rate after 12 hours | Success rate after 24 hours |
|-------------|---------------------------|----------------------------|-----------------------------|-----------------------------|
| 1 | 4%  | 13% | 35% | 58% |
| 3 | 10% | 35% | 72% | 92% |
| 5 | 16% | 51% | 88% | 99% |
| 7 | 22% | 63% | 95% | 99% |

#### Email, SMS, and Phone

Where codes are generated by the server and sent to the client, the following areas should be considered:

- Is the transport mechanism (email, SMS, or voice) secure enough for the application?
- Are the codes sufficiently long and complex?
- Are the codes generated using a [secure random function](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#secure-random-number-generation)?
- How long are the codes valid for?
- Are multiple codes valid at once, or does generating a new code invalidate the previous one?
    - Could this be used to block access to an account by repeatedly requesting codes?
- Is there sufficient rate-limiting to prevent an attacker requesting large numbers of codes?
    - Large numbers of emailed code may get the server blocked for sending spam.
    - Large numbers of SMS or voice calls may cost money, or be used to harass a user.

### Mobile Apps and Push Notifications

An alternative approach to OTP codes is to send a push notification to the user's mobile phone, which they can either approve or deny. This method is less common, as it requires the user to install an application-specific authenticator.

Properly evaluating the security of this requires the scope of testing to be expanded to cover both the mobile app, and any supporting APIs or services used by it; meaning that it would often be outside of the scope of a traditional web application test. However, there are a couple of simple checks that can be performed without testing the mobile app, including:

- Does the notification provide sufficient context (IP addresses, location, etc) for the user to make an informed decision about whether to approve or deny it?
- Is there any kind of challenge and response mechanism (such as providing a code on the website that the user needs to enter into the app - often called "number matching" or "number challenge")?
- Is there any rate limiting or mechanisms to prevent the user from being spammed with notifications in the hope that they will just blindly accept one?

### IP Address and Location Filtering

One of the factors that is sometimes used with MFA is location ("somewhere you are"), although whether this constitutes a proper authentication factor is debatable. In the context of a web application, this typically means restricting access to specific IP addresses, or not prompting the user for a second factor as long as they are connecting from a specific trusted IP address. A common scenario for this would be to authenticate users with just their password when connecting from the office IP ranges, but requiring an OTP code when they connect from elsewhere.

Depending on the implementation, it may be possible for a user to spoof a trusted IP address by setting the `X-Forwarded-For` header, which could allow them to bypass this check. Note that if the application does not correctly sanitize the contents of this header, it may also be possible to carry out attack such as SQL injection here. If the application supports IPv6, then this should also be checked to ensure that appropriate restrictions are applied to those connections.

Additionally, the trusted IP addresses should be reviewed to ensure that they do not present any weaknesses, such as if they include:

- IP addresses that could be accessible by untrusted users (such as the guest wireless networks in an office).
- Dynamically assigned IP address that could change.
- Public network ranges where an attacker could host their own system (such as Azure or AWS).

### Certificates and Smartcards

Transport Layer Security (TLS) is commonly used to encrypt traffic between the client and the server, and to provide a mechanism for the client to confirm the identity of the server (by comparing Common Name (CN) or Subject Alternative Name (SAN) on the certificate to the requested domain). However, it can also provide a mechanism for the server to confirm the identity of the client, known as client certificate authentication or mutual TLS (mTLS). A full discussion of client certificate authentication is outside of the scope of this guide, but the key principle is that the user presents a digital certificate (stored either on their machine or on a smartcard), which is validated by the server.

The first step when testing is to determine whether the target application restricts the Certificate Authorities (CAs) that are trusted to issue certificates. This information can be obtained using various tools, or by manually examining the TLS handshake. The simplest way is to use OpenSSL's `s_client`:

```bash
$ openssl s_client -connect example:443
[...]
Acceptable client certificate CA names
C = US, ST = Example, L = Example, O = Example Org, CN = Example Org Root Certificate Authority
Client Certificate Types: RSA sign, DSA sign, ECDSA sign
```

If there are no restrictions, then it may be possible to authenticate using a certificate from a different CA. If there are restrictions but they are badly implemented, it may be possible to create a local CA with the correct name ("Example Org Root Certificate Authority" in the example above), and to use this new CA to sign client certificates.

If a valid certificate can be obtained, then it should also be verified that the certificate can only be used for the user that it is issued for (i.e, that you can't use a certificate issued to Alice to authenticate on Bob's account). Additionally, certificates should be checked to ensure that they have neither expired nor been revoked.

## Related Test Cases

- [Testing for Weak Lock Out Mechanism](03-Testing_for_Weak_Lock_Out_Mechanism.md)
- [Testing for Weak Password Change or Reset Functionalities](09-Testing_for_Weak_Password_Change_or_Reset_Functionalities.md)

## Remediation

Ensure that:

- MFA is implemented for all relevant accounts and functionality on the applications.
- The support MFA methods are appropriate for the application.
- The mechanisms used to implement MFA are appropriately secured and protected against brute-force attacks.
- There is appropriate auditing and logging for all MFA-related activity.

See the [OWASP Multi-Factor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) for further recommendations.

## References

- [OWASP Multi-Factor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
