# Testing for Weak Lock Out Mechanism

|ID          |
|------------|
|WSTG-ATHN-03|

## Summary

Account lockout mechanisms are used to mitigate brute force attacks. Some of the attacks that can be defeated by using lockout mechanism:

- Login password or username guessing attack.
- Code guessing on any 2FA functionality or Security Questions.

Account lockout mechanisms require a balance between protecting accounts from unauthorized access and protecting users from being denied authorized access. Accounts are typically locked after 3 to 5 unsuccessful attempts and can only be unlocked after a predetermined period of time, via a self-service unlock mechanism, or intervention by an administrator.

Despite it being easy to conduct brute force attacks, the result of a successful attack is dangerous as the attacker will have full access on the user account and with it all the functionality and services they have access to.

## Test Objectives

- Evaluate the account lockout mechanism's ability to mitigate brute force password guessing.
- Evaluate the unlock mechanism's resistance to unauthorized account unlocking.

## How to Test

### Lockout Mechanism

To test the strength of lockout mechanisms, you will need access to an account that you are willing or can afford to lock. If you have only one account with which you can log on to the web application, perform this test at the end of your test plan to avoid losing testing time by being locked out.

To evaluate the account lockout mechanism's ability to mitigate brute force password guessing, attempt an invalid log in by using the incorrect password a number of times, before using the correct password to verify that the account was locked out. An example test may be as follows:

1. Attempt to log in with an incorrect password 3 times.
2. Successfully log in with the correct password, thereby showing that the lockout mechanism doesn't trigger after 3 incorrect authentication attempts.
3. Attempt to log in with an incorrect password 4 times.
4. Successfully log in with the correct password, thereby showing that the lockout mechanism doesn't trigger after 4 incorrect authentication attempts.
5. Attempt to log in with an incorrect password 5 times.
6. Attempt to log in with the correct password. The application returns "Your account is locked out.", thereby confirming that the account is locked out after 5 incorrect authentication attempts.
7. Attempt to log in with the correct password 5 minutes later. The application returns "Your account is locked out.", thereby showing that the lockout mechanism does not automatically unlock after 5 minutes.
8. Attempt to log in with the correct password 10 minutes later. The application returns "Your account is locked out.", thereby showing that the lockout mechanism does not automatically unlock after 10 minutes.
9. Successfully log in with the correct password 15 minutes later, thereby showing that the lockout mechanism automatically unlocks after a 10 to 15 minute period.

A CAPTCHA may hinder brute force attacks, but they can come with their own set of weaknesses, and should not replace a lockout mechanism. A CAPTCHA mechanism may be bypassed if implemented incorrectly. CAPTCHA flaws include:

1. Easily defeated challenge, such as arithimetic or limited question set.
2. CAPTCHA checks for HTTP response code instead of response success.
3. CAPTCHA server-side logic defaults to a successful solve.
4. CAPTCHA challenge result is never validated server-side.
5. CAPTCHA input field or parameter is manually processed, and is improperly validated or escaped.

To evaluate CAPTCHA effectiveness:

1. Assess CAPTCHA challenges and attempt automating solutions depending on difficulty.
2. Attempt to submit request without solving CAPTCHA via the normal UI mechanism(s).
3. Attempt to submit request with intentional CAPTCHA challenge failure.
4. Attempt to submit request without solving CAPTCHA (assuming some default values may be passed by client-side code, etc) while using a testing proxy (request submitted directly server-side).
5. Attempt to fuzz CAPTCHA data entry points (if present) with common injection payloads or special characters sequences.
6. Check if the solution to the CAPTCHA might be the alt-text of the image(s), filename(s), or a value in an associated hidden field.
7. Attempt to re-submit previously identified known good responses.
8. Check if clearing cookies causes the CAPTCHA to be bypassed (for example if the CAPTCHA is only shown after a number of failures).
9. If the CAPTCHA is part of a multi-step process, attempt to simply access or complete a step beyond the CAPTCHA (for example if CAPTCHA is the first step in a login process, try simply submitting the second step [username and password]).
10. Check for alternative methods that might not have CAPTCHA enforced, such as an API endpoint meant to facilitate mobile app access.

Repeat this process to every possible functionality that could require a lockout mechanism.

### Unlock Mechanism

To evaluate the unlock mechanism's resistance to unauthorized account unlocking, initiate the unlock mechanism and look for weaknesses. Typical unlock mechanisms may involve secret questions or an emailed unlock link. The unlock link should be a unique one-time link, to stop an attacker from guessing or replaying the link and performing brute force attacks in batches.

Note that an unlock mechanism should only be used for unlocking accounts. It is not the same as a password recovery mechanism, yet could follow the same security practices.

## Remediation

Apply account unlock mechanisms depending on the risk level. In order from lowest to highest assurance:

1. Time-based lockout and unlock.
2. Self-service unlock (sends unlock email to registered email address).
3. Manual administrator unlock.
4. Manual administrator unlock with positive user identification.

Factors to consider when implementing an account lockout mechanism:

1. What is the risk of brute force password guessing against the application?
2. Is a CAPTCHA sufficient to mitigate this risk?
3. Is a client-side lockout mechanism being used (e.g., JavaScript)? (If so, disable the client-side code to test.)
4. Number of unsuccessful log in attempts before lockout. If the lockout threshold is to low then valid users may be locked out too often. If the lockout threshold is to high then the more attempts an attacker can make to brute force the account before it will be locked. Depending on the application's purpose, a range of 5 to 10 unsuccessful attempts is typical lockout threshold.
5. How will accounts be unlocked?
    1. Manually by an administrator: this is the most secure lockout method, but may cause inconvenience to users and take up the administrator's "valuable" time.
        1. Note that the administrator should also have a recovery method in case his account gets locked.
        2. This unlock mechanism may lead to a denial-of-service attack if an attacker's goal is to lock the accounts of all users of the web application.
    2. After a period of time: What is the lockout duration? Is this sufficient for the application being protected? E.g. a 5 to 30 minute lockout duration may be a good compromise between mitigating brute force attacks and inconveniencing valid users.
    3. Via a self-service mechanism: As stated before, this self-service mechanism must be secure enough to avoid that the attacker can unlock accounts himself.

## References

- See the OWASP article on [Brute Force](https://owasp.org/www-community/attacks/Brute_force_attack) Attacks.
- [Forgot Password CS](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).
