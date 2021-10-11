# Testing for Weak Password Policy

|ID          |
|------------|
|WSTG-ATHN-07|

## Summary

The most prevalent and most easily administered authentication mechanism is a static password. The password represents the keys to the kingdom, but is often subverted by users in the name of usability. In each of the recent high profile hacks that have revealed user credentials, it is lamented that most common passwords are still: `123456`, `password` and `qwerty`.

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

## Remediation

To mitigate the risk of easily guessed passwords facilitating unauthorized access there are two solutions: introduce additional authentication controls (i.e. two-factor authentication) or introduce a strong password policy. The simplest and cheapest of these is the introduction of a strong password policy that ensures password length, complexity, reuse and aging; although ideally both of them should be implemented.

## References

- [Brute Force Attacks](https://owasp.org/www-community/attacks/Brute_force_attack)
