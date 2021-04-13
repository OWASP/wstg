# Testing for Weak Password Change or Reset Functionalities

|ID          |
|------------|
|WSTG-ATHN-09|

## Summary

TODO

## Test Objectives

- Determine whether the password change and reset functionality allows accounts to be compromised.

## How to Test

### Determine How Password Resets Are Performed

Key steps:

- Requests a password reset
- Prove identity
- Obtain or set new password

### General Concerns

- Is the password reset process weaker than the authentication process?
- Does password reset allow MFA bypass?
- Do the usual password complexity policy apply?
- Can the process be locked out?

### Requesting a Password Reset

- Does the reset process allow enumeration?
- Is there a CAPTCHA or other rate limiting?
- Are there multiple processes (webapp vs mobile)
- What information does the user provide (username, email address, etc)

### Email - New Password Sent

- Password emailed in cleartext (bad)
- DoS vector (locks out legitimate user)
- Is used forced to change password on initial login?
- Is password securely generated?
- Is existing password sent (implies encryption or plain text password)

### Email - Link Sent

- Can link be used multiple times?
- Does link expire?
- Is token long and random?
    - Not md5($email)
    - JWT - usual concerns
- Does link contain a user ID?
    - Can it be tampered?
- Can you inject a different host header?
- Is link revealed through referer/analytics scripts?
- When setting the password, can you specify the user ID?

### Security Questions

- See existing guidance

### SMS or Phone Call

- Is provided PIN/code long and random?
- Is SMS or a phone call considered sufficiently secure?
    - Number hijacking
    - May be accessible without a PIN, especially office phone

### Authenticated Password Changes

- Is the user required to re-authenticate?
    - If MFA is enabled, do they need to use that?
- Is the password change form vulnerable to CSRF?
    - Link to CSRF guidance
- Does the submission contain a user ID?
    - Can it be tampered?

## References

- [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
