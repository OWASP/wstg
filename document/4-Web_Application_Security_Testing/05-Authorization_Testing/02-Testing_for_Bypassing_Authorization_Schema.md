# Testing for Bypassing Authorization Schema

|ID          |
|------------|
|WSTG-ATHZ-02|

## Summary

This kind of test focuses on verifying how the authorization schema has been implemented for each role or privilege to get access to reserved functions and resources.

For every specific role the tester holds during the assessment, for every function and request that the application executes during the post-authentication phase, it is necessary to verify:

- Is it possible to access that resource even if the user is not authenticated?
- Is it possible to access that resource after the log-out?
- Is it possible to access functions and resources that should be accessible to a user that holds a different role or privilege?

Try to access the application as an administrative user and track all the administrative functions.

- Is it possible to access administrative functions also if the tester is logged as a user with standard privileges?
- Is it possible to use these administrative functions as a user with a different role and for whom that action should be denied?

## How to Test

### Testing for Access to Administrative Functions

For example, suppose that the `AddUser.jsp` function is part of the administrative menu of the application, and it is possible to access it by requesting the following URL:

`https://www.example.com/admin/addUser.jsp`

Then, the following HTTP request is generated when calling the AddUser function:

```html
POST /admin/addUser.jsp HTTP/1.1
Host: www.example.com
[...]

userID=fakeuser&role=3&group=grp001
```

What happens if a non-administrative user tries to execute that request? Will the user be created? If so, can the new user use their privileges?

### Testing for Access to Resources Assigned to a Different Role

For example analyze an application that uses a shared directory to store temporary PDF files for different users. Suppose that `documentABC.pdf` should be accessible only by the user `test1` with `roleA`. Verify if user `test2` with `roleB` can access that resource.

### Testing for Special Request Header Handling

Some applications support non-standard headers such as `X-Original-URL` or `X-Rewrite-URL` in order to allow overriding the target URL in requests with the one specified in the header value.

This behavior can be leveraged in a situation in which the application is behind a component that applies access control restriction based on the request URL.

The kind of access control restriction based on the request URL can be, for example, blocking access from Internet to an administration console exposed on `/console` or `/admin`.

To detect the support for the header `X-Original-URL` or `X-Rewrite-URL`, the following steps can be applied.

#### 1. Send a Normal Request without Any X-Original-Url or X-Rewrite-Url Header

```html
GET / HTTP/1.1
Host: www.example.com
[...]
```

#### 2. Send a Request with an X-Original-Url Header Pointing to a Non-Existing Resource

```html
GET / HTTP/1.1
Host: www.example.com
X-Original-URL: /donotexist1
[...]
```

#### 3. Send a Request with an X-Rewrite-Url Header Pointing to a Non-Existing Resource

```html
GET / HTTP/1.1
Host: www.example.com
X-Rewrite-URL: /donotexist2
[...]
```

If the response for either request contains markers that the resource was not found, this indicates that the application supports the special request headers. These markers may include the HTTP response status code 404, or a "resource not found" message in the response body.

Once the support for the header `X-Original-URL` or `X-Rewrite-URL` was validated then the tentative of bypass against the access control restriction can be leveraged by sending the expected request to the application but specifying a URL "allowed" by the front-end component as the main request URL and specifying the real target URL in the `X-Original-URL` or `X-Rewrite-URL` header depending on the one supported. If both are supported then try one after the other to verify for which header the bypass is effective.

#### 4. Other Headers to Consider

Often admin panels or administrative related bits of functionality are only accessible to clients on local networks/connections, therefore if may be possible to abuse various proxy or forwarder related HTTP headers to gain access. Some headers and values to test with are:

- Headers:
  - `X-Forward-For`
  - `X-Remote-IP`
  - `X-Originating-IP`
  - `X-Remote-Addr`
  - `X-Client-IP`
- Values
  - `127.0.0.1` (or anything in the `127.0.0.0/8` or `::1/128` address spaces)
  - `localhost`
  - Any [RFC1918](https://tools.ietf.org/html/rfc1918) address:
    - `10.0.0.0/8`
    - `172.16.0.0/12`
    - `192.168.0.0/16`

## Tools

- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org/)
- [Port Swigger Burp Suite](https://portswigger.net/burp)
