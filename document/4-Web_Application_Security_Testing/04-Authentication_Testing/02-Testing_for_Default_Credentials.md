# Testing for Default Credentials

|ID          |
|------------|
|WSTG-ATHN-02|

## Summary

Many web applications and hardware devices have default passwords for the built-in administrative account. Although in some cases these can be randomly generated, they are often static, meaning that they can be easily guessed or obtained by an attacker.

Additionally, when new users are created on the applications, these may have predefined passwords set. These could either be generated automatically by the application, or manually created by staff. In both cases, if they are not generated in a secure manner, the passwords may be possible for an attacker to guess.

## Test Objectives

- Determine whether the application has any user accounts with default passwords.
- Review whether new user accounts are created with weak or predictable passwords.

## How to Test

### Testing for Vendor Default Credentials

The first step to identifying default passwords is to identify the software that is in use. This is covered in detail in the [Information Gathering](../01-Information_Gathering/README.md) section of the guide.

Once the software has been identified, try to find whether it uses default passwords, and if so, what they are. This should include:

- Searching for "[SOFTWARE] default password".
- Reviewing the manual or vendor documentation.
- Checking common default password databases, such as [CIRT.net](https://cirt.net/passwords), [SecLists Default Passwords](https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials) or [DefaultCreds-cheat-sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet/blob/main/DefaultCreds-Cheat-Sheet.csv).
- Inspecting the application source code (if available).
- Installing the application on a virtual machine and inspecting it.
- Inspecting the physical hardware for stickers (often present on network devices).

If a default password can't be found, try common options such as:

- "admin", "password", "12345", or other [common default passwords](https://github.com/nixawk/fuzzdb/blob/master/bruteforce/passwds/default_devices_users%2Bpasswords.txt).
- An empty or blank password.
- The serial number or MAC address of the device.

If the username is unknown, there are various options for enumerating users, discussed in the [Testing for Account Enumeration](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md) guide. Alternatively, try common options such as "admin", "root", or "system".

### Testing for Organisation Default Passwords

When staff within an organisation manually create passwords for new accounts, they may do so in a predictable way. This can often be:

- A single common password such as "Password1".
- Organisation specific details, such as the organisation name or address.
- Passwords that follow a simple pattern, such as "Monday123" if account is created on a Monday.

These types of passwords are often difficult to identify from a black-box perspective, unless they can successfully be guessed or brute-forced. However, they are easy to identify when performing grey-box or white-box testing.

### Testing for Application Generated Default Passwords

If the application automatically generates passwords for new user accounts, these may also be predictable. In order to test these, create multiple accounts on the application with similar details at the same time, and compare the passwords that are given for them.

The passwords may be based on:

- A single static string shared between accounts.
- A hashed or obfuscated part of the account details, such as `md5($username)`.
- A time-based algorithm.
- A weak pseudo-random number generator (PRNG).

This type of issue of often difficult to identify from a black-box perspective.

## Tools

- [Burp Intruder](https://portswigger.net/burp/documentation/desktop/tools/intruder)
- [THC Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [Nikto 2](https://www.cirt.net/nikto2)

## References

- [CIRT](https://cirt.net/passwords)
- [SecLists Default Passwords](https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials)
- [DefaultCreds-cheat-sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet/blob/main/DefaultCreds-Cheat-Sheet.csv)
