# Testing for Default Credentials

|ID          |
|------------|
|WSTG-ATHN-02|

## Summary

Many web applications and hardware devices have default passwords for the built-in administrative account. Although in some cases these can be randomly generated, they are often static, meaning that they can be easily guessed or obtained by an attacker.

Additionally, when new users are created on the applications, these may have pre-defined passwords set. These could either be generated automatically by the application, or manually created by staff. In both cases, if they are not generated in a secure manner, the passwords may be possible for an attacker to guess.

## Test Objectives

- Determine whether the application has any user accounts with default passwords.
- Review whether new user accounts are created with weak or predictable passwords.

## How to Test

### Testing for Vendor Default Credentials

The first step to identifying default passwords is to identify the software that is in use. This is covered in detail in the [Information Gathering](../01-Information_Gathering/README.md) section of the guide.

Once the software has been identified, try to find whether it uses default passwords, and if so, what they are. This should include:

- Searching for "SOFTWARE default password".
- Reviewing the manual or vendor documentation.
- Checking common default password databases, such as [CIRT.net](https://cirt.net/passwords).
- Inspecting the application source code (if available).
- Installing the application of a virtual machine and inspecting it.
- Inspecting the physical hardware for stickers (often present on network devices).

If a default password can't be found, try common options such as:

- "admin", "password", "12345" or other [common default passwords](https://github.com/nixawk/fuzzdb/blob/master/bruteforce/passwds/default_devices_users%2Bpasswords.txt)
- An empty or blank password.
- The serial number of MAC address of the device.

If the username is unknown, there are various options for enumerating users, discussed in the [Testing for Account Enumeration](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md) guide. Alternatively, try common options such as "admin", "root" or "system".

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

## Tools

- [Burp Intruder](https://portswigger.net/burp)
- [THC Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [Nikto 2](https://www.cirt.net/nikto2)

## References

- [CIRT](https://cirt.net/passwords)
