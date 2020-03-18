
# Testing for Vertical Bypassing Authorization Schema (WSTG-AUTHZ-00X)

## Summary

It is common in modern enterprises to define system roles to manage users and authorization to system resources. The purpose of the system role is to distinguish between user levels and to bind the assigned privileges to each role. An Authorization bypass enables an attacker to gain access to resources that are usually protected from an application or user. A Vertical authorization bypass is specific to the case that an attacker obtains a role higher than his own. This kind of test focuses on verifying how the Vertical authorization schema has been implemented for each role in getting access rights to data and resources of other users with different roles or privileges. Vertical authorization bypass may occur when an attacker gets access to more resources or data than they usually are allowed. The application should prevent such elevation or changes. For every function, page, specific role, and request that the application executes during the post-authentication phase, it is necessary to verify:

- Is it possible to access resources that should be accessible only to higher role user?
- Is it possible to operate functions on resources that should be operative only by a user that holds a higher or specific role identity?

## How to Test

If you want to test manually, the process of testing for bypass authorization scheme could look like this, for each role:

1. For each role, register/generate a user.
2. Generate and keep the session tokens by authenticating the application (one session token for each user).
3. For every request, change the session token from the original token to another role session token and diagnose the responses for each token.
4. An application will be considered vulnerable if the responses are the same, contain same private data or indicate successful operation on other users resource or data.

Under the section tools there are mulitple addons for pentesting frameworks OWASP Zed Attack Proxy (ZAP) and Burp, which enable testing the authorization bypass automatically and on a larger scale. Though a review of the process that is used, is recommendable.

### Example 1

The following table illustrates the system role on banking site. Each role bind with specific permissions for the event menu functionality:

| ROLE | PERMISSION | ADDITIONAL PERMISSION |
|------|------------|-----------------------|
| Administrator | Full Control     | Delete |
| Manager       | Modify, Add, Read | Add    |
| Staff         | Read, Modify     | Modify |
| Customer      | Read Only        |        |

The application will be considered vulnerable if:

1. Customer could operate administrator, manager or staff functions;
2. Staff user could operate manager or administrator functions;
3. Manager could operate administrator functions.

Suppose that the `deleteEvent.jsp` function is part of the administrator account menu of the application, and it is possible to access it by requesting the following URL:

`https://www.example.com/account/deleteEvent.jsp`

Then, the following HTTP request is generated when calling the `deleteEvent` function:

```html
POST /account/deleteEvent.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]
Cookie: SessionID=xh6Tm2DfgRp01AZ03

EventID=1000001
```

Valid and legitimate response:

```html
HTTP1.1 200 OK
[other HTTP headers]

{“message”:”Event was deleted”}
The attacker may try and execute the same request:
POST /account/deleteEvent.jsp HTTP/1.1
Host: www.example.com
[other HTTP headers]
Cookie: SessionID=GbcvA1_CUSTOMER_ATTACKER_SESSION_6fhTscd

EventID=1000002
```

If the response of the attacker’s request contains the same data (`“message”:”Event was deleted”`) the application is vulnerable.

### Example 2

Suppose that the administrator menu is part of the administrator account. The application will be considered vulnerable if any other role rather than administrator could access the administrator menu. Sometimes, developer perform authorization validation at the GUI level only, and leave the functions without authorization validation, thus potentially resulting in a vulnerability.

## Tools

- [ZAP extension: Access Control Testing](https://www.zaproxy.org/docs/desktop/addons/access-control-testing/)
- [Burp extension: AuthMatrix](https://github.com/SecurityInnovation/AuthMatrix/)
- [Burp extension: Authorize](https://github.com/Quitten/Autorize)

### References

OWASP Application Security Verification Standard 3.0.1, V4.1, 4.4, 4.9, 4.16.
