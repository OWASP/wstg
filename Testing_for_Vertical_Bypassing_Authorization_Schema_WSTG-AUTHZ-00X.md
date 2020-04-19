# Testing for Vertical Bypassing Authorization Schema

|ID           |
|-------------|
|WSTG-ATHZ-00X|

## Summary

Modern enterprises commonly define roles to manage users and authorization for system resources. Roles distinguish between user permission levels, each having certain privileges. An authorization bypass enables an attacker to gain access to permissions and resources that are assigned to other roles.

A vertical authorization bypass is specific to the case that an attacker obtains a role higher than their own. Testing for this bypass focuses on verifying how the vertical authorization schema has been implemented for each role. Vertical authorization bypass may occur when an attacker gets access to more resources or data than intended. For every function, page, specific role, and request that the application executes during the post-authentication phase, it is necessary to verify if it is possible to:

- Access resources that should be accessible only to a higher role user.
- Operate functions on resources that should be operative only by a user that holds a higher or specific role identity.

## How to Test

The process of testing for bypass authorization scheme follows:

1. For each role, register a user.
2. Generate and keep the session tokens by authenticating to the application (one session token for each role).
3. For every request, change the session token from the original token to another role session token and diagnose the responses for each token.
4. An application will be considered vulnerable if the responses are the same, contain the same private data, or indicate successful operations on other user resources or data.

In the [Tools](#tools) section, there are multiple add-ons for proxies such as ZAP and Burp that enables them to automatically conduct vertical authorization bypasses on a larger scale, coupling them with manual configuration and report reviewing.

### Example 1

The following table illustrates the system role on banking site. Each role bind with specific permissions for the event menu functionality:

| ROLE | PERMISSION | ADDITIONAL PERMISSION |
|------|------------|-----------------------|
| Administrator | Full Control     | Delete |
| Manager       | Modify, Add, Read | Add    |
| Staff         | Read, Modify     | Modify |
| Customer      | Read Only        |        |

The application will be considered vulnerable if the:

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

The valid response:

```html
HTTP/1.1 200 OK
[other HTTP headers]

{“message”:”Event was deleted”}
```

The attacker may try and execute the same request:

```html
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
- [Burp extension: Autorize](https://github.com/Quitten/Autorize)

### References

[OWASP Application Security Verification Standard 3.0.1](https://github.com/OWASP/ASVS/tree/master/3.0.1), V4.1, 4.4, 4.9, 4.16.
