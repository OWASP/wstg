# Testing for Weak Password Change or Reset Functionalities

|ID          |
|------------|
|WSTG-ATHN-09|

## Summary

For any application that requires the user to authenticate with a password, there must be a mechanism by which the user can regain access to their account if they forget their password. Although this can sometimes be a manual process that involves contacting the owner of the website or a support team, users are frequently allowed to carry out a self-service password reset, and to regain access to their account by providing some other evidence of their identity.

As this functionality provides a direct route to compromise the user's account, it is crucial that it is implemented securely.

## Test Objectives

- Determine whether the password change and reset functionality allows accounts to be compromised.

## How to Test

### Information Gathering

The first step is to gather information about what mechanisms are available to allow the user to reset their password on the application. If there are multiple interfaces on the same site (such as a web interface, mobile application, and API) then these should all be reviewed, in case they provide different functionality.

Once this has been established, determine what information is required in order for a user to initiate a password reset. This can be the username or email address (both of which may be obtained from public information), but it could also be an internally-generated user ID.

### General Concerns

Regardless of the specific methods used to reset passwords, there are a number of common areas that need to be considered:

- Is the password reset process weaker than the authentication process?

  The password reset process provides an alternative mechanism to access a user's account, and so should be at least as secure as the usual authentication process. However, it can provide an easier way to compromise the account, especially if it uses weaker authentication factors such as security questions.

  Additionally, the password reset process may bypass the requirement to use Multi-Factor Authentication (MFA), which can substantially reduce the security of the application.

- Is there rate limiting or other protection against automated attacks?

  As with any authentication mechanism, the password reset process should have protection against automated or brute-force attacks. There are a variety of different methods that can be used to achieve this, such as rate limiting or the use of CAPTCHA. These are particularly important on functionality that triggers external actions (such as sending an email or SMS), or when the user is entering a password reset token.

  It is also possible to protect against brute-force attacks by locking out the account from the password reset process after a certain number of consecutive attempts. This could also prevent a legitimate user from being able to reset their password and regain access to their account, however.

- Is it vulnerable to common attacks?

  As well as the specific areas discussed in this guide, it's also important to check for other common vulnerabilities such as SQL injection or cross-site scripting.

- Does the reset process allow user enumeration?

  See the [Testing for Account Enumeration](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md) guide for further information.

### Email - New Password Sent

In this model, the user is sent a new password via email once they have proved their identity. This is considered less secure for two main reasons:

- The password is sent to the user in an unencrypted form.
- The password for the account is changed when the request is made, effectively locking the user out of their account until they receive the email. By making repeated requests, it is possible to prevent a user from being able to access their account.

Where this approach is used, the following areas should be reviewed:

- Is the user forced to change the password on initial login?

  The new password is sent over unencrypted email, and may sit in the user's inbox indefinitely if they don't delete the email. As such, the user should be required to change the password as soon as they log in for the first time.

- Is the password securely generated?

  The password should be generated using a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG), and should be sufficiently long to prevent password guessing or brute-force attacks. For a secure user-friendly experience, it should be generated using a secure passphrase-style approach (i.e, combining multiple words), rather than a string of random characters.

- Is the user's existing password sent to them?

  Rather than generating a new password for the user, some applications will send the user their existing password. This is a very insecure approach, as it exposes their current password over unencrypted email. Additionally, if the site is able to recover the existing password, this implies that passwords are either stored using reversible encryption, or (more likely) in unencrypted plain text, both of which represent a serious security weakness.

- Are the emails sent from a domain with anti-spoofing protection?

  The domain should implement SPF, DKIM, and DMARC to prevent attackers from spoofing emails from it, which could be used as part of a social engineering attack.

- Is email considered sufficiently secure?

  Emails are typically sent unencrypted, and in many cases the user's email account will not be protected by MFA. It may also be shared between multiple individuals, particularly in a corporate environment.

  Consider whether email-based password reset functionality is appropriate, based on the context of the application that is being tested.

### Email - Link Sent

In this model, the user is emailed a link that contains a token. They can then click this link, and are prompted to enter a new password on the site. This is the most common approach used for password reset, but is more complex to implement than the previously discussed approach. The key areas to test are:

- Does the link use HTTPS?

  If the token is sent over unencrypted HTTP, it may be possible for an attacker to intercept it.

- Can the link be used multiple times?

  Links should expire after they are used, otherwise they provide a persistent backdoor for the account.

- Does the link expire if it remains unused?

  Links should be time limited. Exactly how long is appropriate will depend on the site, but it should rarely be more than an hour.

- Is the token sufficiently long and random?

  The security of the process is entirely reliant on an attacker not being able to guess or brute-force a token. The tokens should be generated with a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG), and should be sufficiently long that it is impractical for an attacker to guess or brute-force. At least 128 bits (or 32 hex characters) is a sufficient minimum to make such an online attack impractical.

  Tokens should never be generated based on known values, such as by taking the MD5 hash of the user's email with `md5($email)`, or using GUIDs which may use insecure PRNG functions, or may not even be random depending on the type.

  An alternative approach to random tokens is to use a cryptographically signed token such as a JWT. In this case, the usual JWT checks should be carried out (is the signature verified, can the "nONe" algorithm be used, can the HMAC key be brute-forced, etc). See the [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md) guide for further information.

- Does the link contain a user ID?

  Sometimes the password reset link may include a user ID as well as a token, such as `reset.php?userid=1&token=123456`. In this case, it may be possible to modify the `userid` parameter to reset other users' passwords.

- Can you inject a different host header?

  If the application trusts the value of the `Host` header and uses this to generate the password reset link, it may be possible to steal tokens by injecting a modified `Host` header into the request. See the [Testing for Host Header Injection](../07-Input_Validation_Testing/17-Testing_for_Host_Header_Injection.md) guide for further information.

- Is the link exposed to third parties?

  If the page that the user is taken to includes content from other parties (such as loading scripts from other domains), then the reset token in the URL may be exposed in the HTTP `Referer` header sent in these requests. The `Referrer-Policy` HTTP header can be used to protect against this, so check if one is defined for the page.

  Additionally, if the page includes any tracking, analytics or advertising scripts, the token will also be exposed to them.

- Are the emails sent from a domain with anti-spoofing protection?

  The domain should implement SPF, DKIM, and DMARC to prevent attackers from spoofing emails from it, which could be used as part of a social engineering attack.

- Is email considered sufficiently secure?

  Emails are typically sent unencrypted, and in many cases the user's email account will not be protected by MFA. It may also be shared between multiple individuals, particularly in a corporate environment.

  Consider whether email-based password reset functionality is appropriate, based on the context of the application that is being tested.

### Tokens Sent Over SMS or Phone Call

Rather than sending a token in an email, an alternative approach is to send it via SMS or an automated phone call, which the user will then enter on the application. The key areas to test are:

- Is the token sufficiently long and random?

  Tokens sent this way are typically shorter, as they are intended to be manually typed by the user, rather than being embedded in a link. It's fairly common for applications to use six numeric digits, which only provides ~20 bits of security (feasible for an online brute-force attack), rather than the typically longer email token.

  This makes it much more important that the password reset functionality is protected against brute-force attacks.

- Can the token be used multiple times?

  Tokens should be invalidated after they are used, otherwise they provide a persistent backdoor for the account.

- Does the token expire if it remains unused?

  As the shorter tokens are more susceptible to brute-force attacks, a shorter expiration time should be implemented to limit the window available for an attacker to carry out an attack.

- Are appropriate rate limiting and restrictions in place?

  Sending an SMS or triggering an automated phone call to a user is significantly more disruptive than sending an email, and could be used to harass a user, or even carry out a denial of service attack against their phone. The application should implement rate limiting to prevent this.

  Additionally, SMS messages and phone calls often incur financial costs for the sending party. If an attacker is able to cause a large number of messages to be sent, this could result in significant costs for the website operator. This is especially true if they are sent to international or premium rate numbers. However, allowing international numbers may be a requirement of the application.

- Is SMS or a phone call considered sufficiently secure?

  [A variety of attacks](https://www.ncsc.gov.uk/guidance/protecting-sms-messages-used-in-critical-business-processes#section_4) have been demonstrated that would allow an attacker to effectively hijack SMS messages, there are conflicting views about whether SMS is sufficiently secure to be used as an authentication factor.

  It is usually possible to answer an automated phone call with physical access to a device, without needing any kind of PIN or fingerprint to unlock the phone. In some circumstances (such as a shared office environment), this could allow an internal attacker to trivially reset another user's password by walking over to their desk when they are out of office.

  Consider whether SMS or automated phone calls are appropriate, based on the context of the application that is being tested.

### Security Questions

Rather than sending them a link or new password, security questions can be used as a mechanism to authenticate the user. This is considered to be a weak approach, and should not be used if better options are available.

See the [Testing for Weak Security Questions](08-Testing_for_Weak_Security_Question_Answer.md) guide for further information.

### Authenticated Password Changes

Once the user has proved their identity (either through a password reset link, a recovery code, or by logging in on the application) they should be able to change their password. The key area to test are:

- When setting the password, can you specify the user ID?

  If the user ID is included in the password reset request and is not validated, it may be possible to modify it and change other users' passwords.

- Is the user required to re-authenticate?

  If a logged-in user tries to change their password, they should be asked to re-authenticate with their current password in order to protect against an attacker gaining temporary access to an unattended session. If the user has MFA enabled, then they would typically re-authenticate with that, rather than their password.

- Is the password change form vulnerable to CSRF?

  If the user isn't required to re-authenticate, then it may be possible to carry out a CSRF attack against the password reset form, allowing their account to be compromised. See the [Testing for Cross-Site Request Forgery](../06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md) guide for further information.

- Is a strong and effective password policy applied?

  The password policy should be consistent across the registration, password change, and password reset functionality. See the [Testing for Weak Password Policy](07-Testing_for_Weak_Password_Policy.md) guide for further information.

## References

- [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
