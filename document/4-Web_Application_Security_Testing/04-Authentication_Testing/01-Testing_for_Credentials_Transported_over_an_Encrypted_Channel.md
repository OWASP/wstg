# Testing for Credentials Transported over an Encrypted Channel

|ID          |
|------------|
|WSTG-ATHN-01|

## Summary

Testing for credentials transport means verifying that the user's authentication data is transferred via an encrypted channel to avoid being intercepted by malicious users. Web applications use [HTTPS](https://tools.ietf.org/html/rfc2818) to encrypt information in transit for both client to server and server to client communications. When a user or client interacts with a web site, there several ways credentials and other sensitive information can be in transit:

1. A client sends a credential to request login
2. An authenticated client sends a [session token](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#session-id-properties) to request sensitive information from the web site
3. The server sends a session token back to the client after a successful login
4. A client sends a token to the web site if they [forgot their password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

Failure to protect any of these credentials with encryption allows an attacker with network sniffing tools to steal the user's account. The attacker could sniff traffic directly using [https://www.wireshark.org](Wireshark) or similar tools, or they could set up a proxy to capture HTTP requests. Therefore any sensitive data should be encrypted in transit.

The fact that traffic is encrypted does not necessarily mean that it's completely safe. The security also depends on the encryption algorithm used and the robustness of the keys that the application is using. See [Testing for Weak SSL TLS Ciphers Insufficient Transport Layer Protection](../09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_SSL_TLS_Ciphers_Insufficient_Transport_Layer_Protection.md) to verify the encrption algorithm is sufficient.

## How to Test

To test for credential transport, testers must capture traffic going to and from the client connected to the web application while performing actions that require authentication. To set up to capture traffic, turn on the web browser's [developer tools](https://developer.mozilla.org/en-US/docs/Tools) or use a proxy including [OWASP ZAP](https://owasp.org/www-project-zap/). Verify the capture works properly, and then interact with the web application in areas that require accounts or other credentials. In addition, testers should disable any features that make the web browser favour HTTPS, since some tests require the user to use [forced browsing](https://owasp.org/www-community/attacks/Forced_browsing) to intentionally request HTTP versions of sensitive pages.

In all of the captures from interacting with the application, verify any session tokens, passphrases, password reset codes, or other sensitive data only go to or from the server through HTTPS. The following examples show what capture tools may show if a test passes or fails, where the test application is called `site-undert.test`.

### Account Creation

These are samples for account creation.

A passing test will show HTTPS for the HTTP POST to create an account.

```
TODO: Create account with credentials in HTTPS POST
```

Attempt to force browse to the HTTP version of the account creation and create an account, example: `TODO: example forced browse`.
If the client sends new account credentials over HTTP, it is a test failure:

```
TODO: Create account with credentials in HTTP POST
```

### Login

These are samples for logging in to a site.

In a passing test, the login request should be HTTPS.

```
TODO: HTTPS POST for login
```
If the server returns cookie information for a session token, the cookie should also include the [secure](https://owasp.org/www-community/controls/SecureFlag) attribute/flag to avoid the client exposing the cookie over unencrpted channels later.

```
TODO: HTTPS response with secure cookie
```

Attempt to force browse to the HTTP version of the login page. If the user is automatically redirected to the HTTPS version (of either the login page or even just the HTTPS version of the home page of the site), the test is a pass.

```
TODO: Redirect to HTTPS login or home page
```

If a test can submit login credentials over HTTP as shown below, the test is a fail:

```
TODO: Login submitted over HTTP
```

### Accessing Resources while Logged In

After logging in, access items on the site that only authenticated users should be able to see. Verify that all captures when using the web application while logged in only send the session token over HTTPS.

```
TODO: Token with HTTPS
```

The test fails if the browser submits a session token over HTTP in any part of the web site, even if forced browsing is required to trigger this case.

```
TODO: Token over HTTP
```

### Remediation

The best remediation would be to make the entire web site or web application use HTTPS, where the server can redirect requests for HTTP directly to the HTTPS version of the site. API endpoints should also be HTTPS only. Using HTTPS on the whole site prevents attackers from modifying interactions with the web server (including placing JavaScript for advertising or to sniff credentials). Newer software (with good reason) also has a warning or restriction for HTTP traffic. Browsers [mark HTTP based web sites as insecure](https://www.blog.google/products/chrome/milestone-chrome-security-marking-http-not-secure/) and Android applications [need overrides](https://developer.android.com/training/articles/security-config#CleartextTrafficPermitted) to connect to anything via HTTP. If the organization does not already buy certificates for HTTPS, look in to enabling support for [Let's Encrypt](https://letsencrypt.org) on the server.
