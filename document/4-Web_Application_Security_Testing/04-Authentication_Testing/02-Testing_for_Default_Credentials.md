# Testing for Default Credentials

|ID          |
|------------|
|WSTG-ATHN-02|

## Summary

Many systems come installed with default credentials.
System administrators may forgo changing those credentials.
This reality creates security risks.

## Test Objectives

- Determine if the application uses known default credentials.

## How to Test

The below steps oversimply the testing landscape.
Real applications often defend against these intrusions.
So expect to adjust the approach to the given application.

1. [Gather information](../01-Information_Gathering/README.md) on the application.
1. Research any public lists of default credentials for that application.
1. Try to authenticate to the application using any of those credentials.

## Remediation

- Change any system default credentials.

## References

- [How to guess account credentials](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md)
- [How to determine a weak password policy](07-Testing_for_Weak_Password_Policy.md)
- [A sample list of default credentials from CIRT.net](https://cirt.net/passwords)
