# Testing for Credentials Transported over an Encrypted Channel

|ID          |
|------------|
|WSTG-ATHN-01|

## Summary

Testing for credentials transport verifies that web applications encrypt authentication data in transit. This encryption prevents attackers from taking over accounts by [sniffing network traffic](https://owasp.org/www-community/attacks/Man-in-the-middle_attack). Web applications use [HTTPS](https://tools.ietf.org/html/rfc2818) to encrypt information in transit for both client to server and server to client communications. A client can send or receive authentication data during the following interactions:

- A client sends a credential to request login
- The server responds to a successful login with a [session token](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#session-id-properties)
- An authenticated client sends a session token to request sensitive information from the web site
- A client sends a token to the web site if they [forgot their password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

Failure to encrypt any of these credentials in transit can allow attackers with network sniffing tools to view credentials and possibly use them to steal a user's account. The attacker could sniff traffic directly using [Wireshark](https://www.wireshark.org) or similar tools, or they could set up a proxy to capture HTTP requests. Sensitive data should be encrypted in transit to prevent this.

The fact that traffic is encrypted does not necessarily mean that it's completely safe. The security also depends on the encryption algorithm used and the robustness of the keys that the application is using. See [Testing for Weak Transport Layer Security](../09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_Transport_Layer_Security.md) to verify the encryption algorithm is sufficient.

## Test Objectives

- Assess whether any use case of the web site or application causes the server or the client to exchange credentials without encryption.

## How to Test

To test for credential transport, capture traffic between a client and web application server that needs credentials. Check for credentials transferred during login and while using the application with a valid session. To set up for the test:

1. Set up and start a tool to capture traffic, such as one of the following:
   - The web browser's [developer tools](https://developer.mozilla.org/en-US/docs/Tools)
   - A proxy including [OWASP ZAP](https://owasp.org/www-project-zap/)
2. Disable any features or plugins that make the web browser favour HTTPS. Some browsers or extensions, such as [HTTPS Everywhere](https://www.eff.org/https-everywhere), will combat [forced browsing](https://owasp.org/www-community/attacks/Forced_browsing) by redirecting HTTP requests to HTTPS.

In the captured traffic, look for sensitive data including the following:

- Passphrases or passwords, usually inside a [message body](https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html)
- Tokens, usually inside [cookies](https://tools.ietf.org/html/rfc6265#section-4.2)
- Account or password reset codes

For any message containing this sensitive data, verify the exchange occurred using HTTPS (and not HTTP). The following examples show captured data that indicate passed or failed tests, where the web application is on a server called `www.example.org`.

### Login

Find the address of the login page and attempt to switch the protocol to HTTP. For example, the URL for the forced browsing could look like the following: `http://www.example.org/login`.

If the login page is normally HTTPS, attempt to remove the "S" to see if the login page loads as HTTP.

Log in using a valid account while attempting to force the use of unencrypted HTTP. In a passing test, the login request should be HTTPS:

```http
Request URL: https://www.example.org/j_acegi_security_check
Request method: POST
...
Response headers:
HTTP/1.1 302 Found
Server: nginx/1.19.2
Date: Tue, 29 Sep 2020 00:59:04 GMT
Transfer-Encoding: chunked
Connection: keep-alive
X-Content-Type-Options: nosniff
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Set-Cookie: JSESSIONID.a7731d09=node01ai3by8hip0g71kh3ced41pmqf4.node0; Path=/; Secure; HttpOnly
ACEGI_SECURITY_HASHED_REMEMBER_ME_COOKIE=dXNlcmFiYzoxNjAyNTUwNzQ0NDU3OjFmNDlmYTZhOGI1YTZkYTYxNDIwYWVmNmM0OTI1OGFhODA3Y2ZmMjg4MDM3YjcwODdmN2I2NjMwOWIyMDU3NTc=; Path=/; Expires=Tue, 13-Oct-2020 00:59:04 GMT; Max-Age=1209600; Secure; HttpOnly
Location: https://www.example.org/
...
POST data:
j_username=userabc
j_password=My-Protected-Password-452
from=/
Submit=Sign in
```

- In the login, the credentials are encrypted due to the HTTPS request URL
- If the server returns cookie information for a session token, the cookie should also include the [`Secure` attribute](https://owasp.org/www-community/controls/SecureFlag) to avoid the client exposing the cookie over unencrypted channels later. Look for the `Secure` keyword in the response header.

The test fails if any login transfers a credential over HTTP, similar to the following:

```http
Request URL: http://www.example.org/j_acegi_security_check
Request method: POST
...
POST data:
j_username=userabc
j_password=My-Protected-Password-452
from=/
Submit=Sign in
```

In this failing test example:

- The fetch URL is `http://` and it exposes the plaintext `j_username` and `j_password` through the post data.
- In this case, since the test already shows POST data exposing all the credentials, there is no point checking response headers (which would also likely expose a session token or cookie).

### Account Creation

To test for unencrypted account creation, attempt to force browse to the HTTP version of the account creation and create an account, for example: `http://www.example.org/securityRealm/createAccount`

The test passes if even after the forced browsing, the client still sends the new account request through HTTPS:

```http
Request URL: https://www.example.org/securityRealm/createAccount
Request method: POST
...
Response headers:
HTTP/1.1 200 OK
Server: nginx/1.19.2
Date: Tue, 29 Sep 2020 01:11:50 GMT
Content-Type: text/html;charset=utf-8
Content-Length: 3139
Connection: keep-alive
X-Content-Type-Options: nosniff
Set-Cookie: JSESSIONID.a7731d09=node011yew1ltrsh1x1k3m6g6b44tip8.node0; Path=/; Secure; HttpOnly
Expires: 0
Cache-Control: no-cache,no-store,must-revalidate
X-Hudson-Theme: default
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
X-Hudson: 1.395
X-Jenkins: 2.257
X-Jenkins-Session: 4551da08
X-Hudson-CLI-Port: 50000
X-Jenkins-CLI-Port: 50000
X-Jenkins-CLI2-Port: 50000
X-Frame-Options: sameorigin
Content-Encoding: gzip
X-Instance-Identity: MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3344ru7RK0jgdpKs3cfrBy2tteYI1laGpbP4fr5zOx2b/1OEvbVioU5UbtfIUHruD9N7jBG+KG4pcWfUiXdLp2skrBYsXBfiwUDA8Wam3wSbJWTmPfSRiIu4dsfIedj0bYX5zJSa6QPLxYolaKtBP4vEnP6lBFqW2vMuzaN6QGReAxM4NKWTijFtpxjchyLQ2o+K5mSEJQIWDIqhv1sKxdM9zkb6pW/rI1deJJMSih66les5kXgbH2fnO7Fz6di88jT1tAHoaXWkPM9X0EbklkHPT9b7RVXziOURXVIPUTU5u+LYGkNavEb+bdPmsD94elD/cf5ZqdGNoOAE5AYS0QIDAQAB
...
POST data:
username=user456
fullname=User 456
password1=My-Protected-Password-808
password2=My-Protected-Password-808
Submit=Create account
Jenkins-Crumb=58e6f084fd29ea4fe570c31f1d89436a0578ef4d282c1bbe03ffac0e8ad8efd6
```

- Similar to a login, most web applications automatically give a session token on a successful account creation. If there is a `Set-Cookie:`, verify it has a `Secure;` attribute as well.

The test fails if the client sends a new account request with unencrypted HTTP:

```http
Request URL: http://www.example.org/securityRealm/createAccount
Request method: POST
...
POST data:
username=user456
fullname=User 456
password1=My-Protected-Password-808
password2=My-Protected-Password-808
Submit=Create account
Jenkins-Crumb=8c96276321420cdbe032c6de141ef556cab03d91b25ba60be8fd3d034549cdd3
```

- This Jenkins user creation form exposed all the new user details (name, full name, and password) in POST data to the HTTP create account page

### Password Reset, Change Password or Other Account Manipulation

Similar to login and account creation, if the web application has features that allow a user to change an account or call a different service with credentials, verify all of those interactions are HTTPS. The interactions to test include the following:

- Forms that allow users to handle a forgotten password or other credential
- Forms that allow users to edit credentials
- Forms that require the user to authenticate with another provider (for example, payment processing)

### Accessing Resources While Logged In

After logging in, access all the features of the application, including public features that do not necessarily require a login to access. Forced browse to the HTTP version of the web site to see if the client leaks credentials.

The test passes if all interactions send the session token over HTTPS similar to the following example:

```http
Request URL:http://www.example.org/
Request method:GET
...
Request headers:
GET / HTTP/1.1
Host: www.example.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
DNT: 1
Connection: keep-alive
Cookie: JSESSIONID.a7731d09=node01ai3by8hip0g71kh3ced41pmqf4.node0; ACEGI_SECURITY_HASHED_REMEMBER_ME_COOKIE=dXNlcmFiYzoxNjAyNTUwNzQ0NDU3OjFmNDlmYTZhOGI1YTZkYTYxNDIwYWVmNmM0OTI1OGFhODA3Y2ZmMjg4MDM3YjcwODdmN2I2NjMwOWIyMDU3NTc=; screenResolution=1920x1200
Upgrade-Insecure-Requests: 1
```

- The session token in the cookie is encrypted since the request URL is HTTPS

The test fails if the browser submits a session token over HTTP in any part of the web site, even if forced browsing is required to trigger this case:

```http
Request URL:http://www.example.org/
Request method:GET
...
Request headers:
GET / HTTP/1.1
Host: www.example.org
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: language=en; welcomebanner_status=dismiss; cookieconsent_status=dismiss; screenResolution=1920x1200; JSESSIONID.c1e7b45b=node01warjbpki6icgxkn0arjbivo84.node0
Upgrade-Insecure-Requests: 1
```

- The GET request exposed the session token `JSESSIONID` (from browser to server) in request URL `http://www.example.org/`

## Remediation

Use HTTPS for the whole web site. Implement [HSTS](https://tools.ietf.org/html/rfc6797) and redirect any HTTP to HTTPS. The site gains the following benefits from using HTTPS for all its features:

- It prevents attackers from modifying interactions with the web server (including placing JavaScript malware through a [compromised router](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/over-200-000-mikrotik-routers-compromised-in-cryptojacking-campaign)).
- It avoids losing customers to insecure site warnings. New browsers [mark HTTP based web sites as insecure](https://www.blog.google/products/chrome/milestone-chrome-security-marking-http-not-secure/).
- It makes writing certain applications easier. For example, Android APIs [need overrides](https://developer.android.com/training/articles/security-config#CleartextTrafficPermitted) to connect to anything via HTTP.

If it is cumbersome to switch to HTTPS, prioritize HTTPS for sensitive operations first. For the medium term, plan to convert the whole application to HTTPS to avoid losing customers to compromise or the warnings of HTTP being insecure. If the organization does not already buy certificates for HTTPS, look in to [Let's Encrypt](https://letsencrypt.org) or other free certificate authorities on the server.
