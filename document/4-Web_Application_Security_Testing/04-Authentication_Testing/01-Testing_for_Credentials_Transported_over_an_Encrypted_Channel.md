# Testing for Credentials Transported over an Encrypted Channel

|ID          |
|------------|
|WSTG-ATHN-01|

## Summary

Testing for credentials transport means verifying that the user's authentication data is transferred via an encrypted channel to avoid being intercepted by malicious users. Web applications use [HTTPS](https://tools.ietf.org/html/rfc2818) to encrypt information in transit for both client to server and server to client communications. Interactions with a web application can transfer credentials in several ways, including the following:

1. A client sends a credential to request login
2. The server responds to a successful login with a session token
3. An authenticated client sends a [session token](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#session-id-properties) to request sensitive information from the web site
4. A client sends a token to the web site if they [forgot their password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

Failure to encrypt any of these credentials in transit allows attackers with network sniffing tools to steal the user's account. The attacker could sniff traffic directly using [https://www.wireshark.org](Wireshark) or similar tools, or they could set up a proxy to capture HTTP requests. Therefore any sensitive data should be encrypted in transit.

The fact that traffic is encrypted does not necessarily mean that it's completely safe. The security also depends on the encryption algorithm used and the robustness of the keys that the application is using. See [Testing for Weak SSL TLS Ciphers Insufficient Transport Layer Protection](../09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_SSL_TLS_Ciphers_Insufficient_Transport_Layer_Protection.md) to verify the encrption algorithm is sufficient.

## How to Test

To test for credential transport, capture traffic between a client and web application server that needs credentials. Check for credentials transferred during login and while using the application with a valid session. To set up to capture traffic, turn on the web browser's [developer tools](https://developer.mozilla.org/en-US/docs/Tools) or use a proxy including [OWASP ZAP](https://owasp.org/www-project-zap/). Disable any features or plugins that make the web browser favour HTTPS, since some tests require the user to use [forced browsing](https://owasp.org/www-community/attacks/Forced_browsing) to intentionally request HTTP versions of sensitive pages.

In the captured traffic, verify any session passphrases, tokens, password reset codes, or other sensitive data only go to or from the server through HTTPS. The following examples show captured data that indicate passed or failed tests, where the web application is on a server called `site-under.test`.

### Account Creation

To test for unencryped account creation, attempt to force browse to the HTTP version of the account creation and create an account, example:

```
http://site-under.test/securityRealm/createAccount
```

The test passes if even after the forced browsing, the client still sends the new account request through HTTPS:

```
TODO: Create account with credentials in HTTPS POST
```

The test fails if the client sends a new account request with unencryped HTTP:

```
Request URL:http://site-under.test/securityRealm/createAccount
Request method:POST
...
POST data:
username=user456
fullname=User 456
remember_me=on
password1=My-Protected-Password-808
password2=My-Protected-Password-808
Submit=Create account
Jenkins-Crumb=8c96276321420cdbe032c6de141ef556cab03d91b25ba60be8fd3d034549cdd3
```
*   This Jeknins user creation form exposed all the new user details (name, full name, and password) in POST data to the HTTP create account page

### Login

Similar to the account creation test, attempt to log in to a previously created account while forced browsing to the HTTP login page if allowed.

In a passing test, the login request should be HTTPS:

```
TODO: HTTPS POST for login
```

If the server returns cookie information for a session token, the cookie should also include the [secure](https://owasp.org/www-community/controls/SecureFlag) attribute/flag to avoid the client exposing the cookie over unencrpted channels later.

```
TODO: HTTPS response with secure cookie
```

If a test can submit login credentials over HTTP as shown below, the test is a fail:

```
Request URL: http://site-under.test/j_acegi_security_check
Request method: POST
...
POST data:

j_username=userabc
j_password=My-Protected-Password-452
from=/
Submit=Sign in
```
* Note the fetch URL is `http://` and it exposes the plaintext `j_username` and `j_password` through the post data

### Password Reset, Change Password or Other Account Manipulation

Similar to login and account creation, if the web application has features that allow a user to change an account or call a different service with credentials, verify all of those interactions are HTTPS. The interactions to test include the following:

* Forms that allow users to handle a forgotten password or other credential
* Forms that allow users to edit credentials
* Forms that require the user to authenticate with another provider (for example, payment processing)

### Accessing Resources while Logged In

After logging in, access all the features of the application, including public features that do not necessarily require a login to access. Forced browse to the HTTP version of the web site to see if the client leaks credentials.

The test passes if all interactions send the session token over HTTPS:

```
TODO: Token with HTTPS
```

The test fails if the browser submits a session token over HTTP in any part of the web site, even if forced browsing is required to trigger this case:

```
Request URL:http://site-under.test/
Request method:GET
...
Request headers:

GET / HTTP/1.1
Host: site-under.test
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: language=en; welcomebanner_status=dismiss; cookieconsent_status=dismiss; screenResolution=1920x1200; JSESSIONID.c1e7b45b=node01warjbpki6icgxkn0arjbivo84.node0
Upgrade-Insecure-Requests: 1
```
*   The get request exposed the session token `JSESSIONID` (from browser to server) in request URL `http://site-under.test/`

## Remediation

The best remediation would be to make the entire web site or web application use HTTPS, and redirect plaintext requests to HTTPS. Using HTTPS on the whole site prevents attackers from modifying interactions with the web server (including placing JavaScript malware). Newer software also has a warning or restriction for HTTP traffic. Browsers [mark HTTP based web sites as insecure](https://www.blog.google/products/chrome/milestone-chrome-security-marking-http-not-secure/) and Android applications [need overrides](https://developer.android.com/training/articles/security-config#CleartextTrafficPermitted) to connect to anything via HTTP. Prioritize HTTPS for sensitive operations first. For the medium term, plan to convert the whole application to HTTPS to avoid losing customers to compromise or the warnings of HTTP being insecure. If the organization does not already buy certificates for HTTPS, look in at least using [Let's Encrypt](https://letsencrypt.org) or other free certificate authorities on the server.
