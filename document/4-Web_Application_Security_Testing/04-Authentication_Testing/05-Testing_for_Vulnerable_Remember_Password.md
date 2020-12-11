# Testing for Vulnerable Remember Password

|ID          |
|------------|
|WSTG-ATHN-05|

## Summary

Credentials are the most widely used authentication technology. Due to such a wide usage of username-password pairs, users are no longer able to properly handle their credentials across the multitude of used applications.

In order to assist users with their credentials, multiple technologies surfaced:

- Applications provide a *remember me* functionality that allows the user to stay authenticated for long periods of time, without asking the user again for their credentials.
- Password Managers - including browser password managers - that allow the user to store their credentials in a secure manner and later on inject them in user-forms without any user intervention.

## Test Objectives

- Validate that the generated session is managed securely and do not put the user's credentials in danger.

## How to Test

As these methods provide a better user experience and allow the user to forget all about their credentials, they increase the attack surface area. Some applications:

- Store the credentials in an encoded fashion in the browser's storage mechanisms, which can be verified by following the [web storage testing scenario](../11-Client-side_Testing/12-Testing_Browser_Storage.md) and going through the [session analysis](../06-Session_Management_Testing/01-Testing_for_Session_Management_Schema.md#session-analysis) scenarios. Credentials shouldn't be stored in any way in the client-side application, and should be substitued by tokens generated server-side.
- Automatically inject the user's credentials that can be abused by:
    - [ClickJacking](../11-Client-side_Testing/09-Testing_for_Clickjacking.md) attacks.
    - [CSRF](../06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md) attacks.
- Tokens should be analyzed in terms of token-lifetime, where some tokens never expire and put the users in danger if those tokens ever get stolen. Make sure to follow the [session timeout](../06-Session_Management_Testing/07-Testing_Session_Timeout.md) testing scenario.

## Remediation

- Follow [session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) good practices.
- Ensure that no credentials are stored in clear text or are easily retrievable in encoded or encrypted forms in browser storage mechanisms; they should be stored server-side and follow good [password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) practices.
