# Testing for Default Credentials

|ID          |
|------------|
|WSTG-ATHN-02|

## Summary

Many systems come installed with default credentials. System administrators may forgo changing those credentials. Not changing default credentials introduces security risks. 

## Test Objectives

- Determine if the application uses known default credentials. 
- Determine if new user accounts have been created with known default credentials.

## How to Test

### Attempt Authentication with Default Credentials

1. [Gather information](../01-Information_Gathering/README.md) on the application.
1. Research any public lists of default credentials for that application.
1. Try to authenticate to the application using any of those credentials. 


### Testing for Default Password of New Accounts

It can also occur that when a new account is created in an application the account is assigned a default password. This password could have some standard characteristics making it predictable. If the user does not change it on first usage (this often happens if the user is not forced to change it) or if the user has not yet logged on to the application, this can lead an attacker to gain unauthorized access to the application.

The advice given before about a possible lockout policy and verbose error messages are also applicable here when testing for default passwords.

The following steps can be applied to test for these types of default credentials:

- Looking at the User Registration page may help to determine the expected format and minimum or maximum length of the application usernames and passwords. If a user registration page does not exist, determine if the organization uses a standard naming convention for usernames such as their email address or the name before the `@` in the email.
- Try to extrapolate from the application how usernames are generated. For example, can a user choose their own username or does the system generate an account name for the user based on some personal information or by using a predictable sequence? If the application does generate the account names in a predictable sequence, such as `user7811`, try fuzzing all possible accounts recursively. If you can identify a different response from the application when using a valid username and a wrong password, then you can try a brute force attack on the valid username (or quickly try any of the identified common passwords above or in the reference section).
- Try to determine if the system generated password is predictable. To do this, create many new accounts quickly after one another so that you can compare and determine if the passwords are predictable. If predictable, try to correlate these with the usernames, or any enumerated accounts, and use them as a basis for a brute force attack.
- If you have identified the correct naming convention for the user name, try to "brute force" passwords with some common predictable sequence like for example dates of birth.
- Attempt using all the above usernames with blank passwords or using the username also as password value.

#### Gray-Box Testing

The following steps rely on an entirely gray-box approach. If only some of this information is available to you, refer to black-box testing to fill the gaps.

- Talk to the IT personnel to determine which passwords they use for administrative access and how administration of the application is undertaken.
- Ask IT personnel if default passwords are changed and if default user accounts are disabled.
- Examine the user database for default credentials as described in the black-box testing section. Also check for empty password fields.
- Examine the code for hard coded usernames and passwords.
- Check for configuration files that contain usernames and passwords.
- Examine the password policy and, if the application generates its own passwords for new users, check the policy in use for this procedure.

## Remediation

- Change any system default credentials.

## References

- [How to guess account credentials](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md)
- [How to determine a weak password policy](07-Testing_for_Weak_Password_Policy.md)
- [A sample list of default credentials from CIRT.net](https://cirt.net/passwords)
