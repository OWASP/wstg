# Testing OAuth Weaknesses

|ID          |
|------------|
|WSTG-ATHZ-05|

## Summary

[OAuth2.0](https://oauth.net/2/) is an authorization delegation framework used in web-enabled applications and APIs it will be referred to as OAuth.
It enables a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner by orchestrating an approval interaction
between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf.

Authorization information is typically being proofed using a access token that if presented to a service should tell the service which access rights may be assigned to the request. Access token may be opaque tokens but very often they are JWTs,therefore the JWT checks in [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md) also apply to the Testing for OAuth weaknesses chapter. The usage of Bearer Token with OAuth is described in rfc6750.

OAuth itself can be used for authentication but it is generally not recommended to implement your own way of doing so. Instead authentication should be implemented with the OpenID Connect standard.

Since OAuth's responsibility is it to delegate access rights across several services, successful attacks may lead to account takeover, unauthorized resource access and the elevation of privileges.

## Test Objectives

- Are the clients confidential or public
- Determine which OAuth flow is used

## How to Test

### Overview

OAuth has five different roles that are part of an OAuth exchange.

- Resource Owner, the entity who grants access to a resource
- User Agent, browser, native app
- Client, the application which requests access to a resource on behalf of the Resource Owner
- Authorization Server, a server which holds authorization information and grants the access
- Resource Server, an application that serves content accessed by the client

Based on the applications ability to keep a secret in secret it separates clients into two distinct types:

- Confidential
- Public

Confidential Clients are typically applications with server side code that are able to prevent anyone from accessing the secret.
Public Clients in contrast are unable to keep the secret secret, an example for a Public Client would be a SPA which has all the code present on the User Agent

In order to understand the attack surface better it is crucial to determine which OAuth Grant Type is used for the application you are testing against.

These are the most common OAuth Grant Types:

- Authorization Code, commonly used with confidential client
- Proof Key for Code Exchange (PKCE), commonly used with public clients in conjunction with Authorization Code
- Consent, Required for the approval of third party clients
- Client Credentials, used for machine to machine communication
- Device Code, used for devices with limited input capabilities

### Testing for improper Grant Type

Depending on the architecture of the application, different grant types should be used.

Some OAuth Grant Types are still part of the OAuth RFC but are kept for legacy purposes only.

The Resource Owner Password Credentials Grant ([ROPC](https://www.youtube.com/watch?v=qMtYaDmhnHU)) is deprecated and should only be used for migration purposes.  

The [Implicit Flow](https://oauth.net/2/grant-types/implicit/) was implemented when browser features like CORS where not implemented already and exists to workaround the lack of cross site request possibilities. It is considered less secure then Authorization Code Flow and thus should not be used for new applications it is a legacy flow as well.

#### How to test

For public clients it is generally possible to identify the grant type as it is part of the token exchange in the parameter `grant_type`. Following example shows the Authorization Code Grant + PKCE. PKCE can be identified by the `code_verifier` parameter.

```http
POST /oauth/token HTTP/2
Host: idp.example.com
[...]

{
    "client_id":"ZXhhbXBsZQ",
    "code_verifier":"fuV-R1Yyxs-1rSk7XInhp5NXGj0PJucD0q5J5VF_qWp",
    "grant_type":"authorization_code",
    "code":"ZqQcutj6aOe_TBfzOGJewgZsu99kgbrbW24zz-8QUpu86",
    "redirect_uri":"http://client.example.com"
    }
```

If presented with a confidential client, the authorization request might give away some hints on the grant type that is being used. The following URL parameters indicate the used flow as well.

- `response_type=token` indicates implicit flow
- `response_type=code` indicates authorization code flow
- `code_challenge=sha256(xyz)` indicates the PKCE extension

Following is an example for Authorization Code Flow + PKCE

```http
GET /authorize?redirect_uri=http%3A%2F%2Flocalhost%3A4200&client_id=ZXhhbXBsZQ&scope=openid%20profile%20email&response_type=code&response_mode=query&state=ZXhhbXBsZQ%3D%3D&nonce=ZXhhbXBsZQ%3D%3D&code_challenge=eNJJZHGTgeaB-RV61cQCesIdnCOQ_Pv5tENQ9xBnKh4&code_challenge_method=S256& HTTP/2
Host: idp.example.com
[...]
```

#### Public Clients

Recommended for public client is the code-grant with the PKCE extension.
An authorization request for Authorization Code Flow + PKCE should contain `response_type=code` and `code_challenge=sha256(xyz)`.

Further the token exchange should contain the  grant type `authorization_code` and a `code_verifier`.

Improper grant types for public client:

- Code Grant without the PKCE extension
- Client Credentials
- Implicit flow
- Resource Owner Password Credential Grant

#### Confidential Clients

The code-grant is recommended for confidential client and the PKCE extension may be used as well.

Improper grant types for confidential client:

- Resource Owner Password Credential Grant
- Implicit flow
- Client Credentials (Except for Machine to Machine)

##### Machine to Machine

Machine to Machine clients generally should be able to keep a secret and therefore may be confidential clients. No user interaction can happen and they may rely solely on the client secret with the Client Credentials grant.

If you already know the client secret it is possible to obtain a token.

```bash
λ curl --request POST \
  --url https://idp.example.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"ZXhhbXBsZQ","client_secret":"THE_CLIENT_SECRET","audience":"https://idp.example.com/","grant_type":"client_credentials"}' --proxy http://localhost:8080/ -k
```

### Credential Leakage via Referrer Header

OAuth transports, dependant on the flow, several types of credentials in the URL.
The following tokens can be considered as credentials.

- authorization token
- refresh token
- authorization code
- PKCE code challenge / code verifier

Due to how OAuth works, the authorization `code` as well as the `code_challenge` and `code_verifier` may be part of the URL. 
Therefore it is even more relevant to ensure those are not sent in the referrer header.

The implicit grant transports the authorization token as part of the URL which may lead to leakage of the authorization token in the referrer and other places like log files and proxies.

#### How to test

Make use of a HTTP Interception proxy such as OWASP ZAP and intercept the OAuth traffic.

- Step through the authorization process and identify any credentials being present in the URL.
- If any external resources are included in a page involved with the OAuth flow analyse request made to them as
  credentials could be leaked in the referrer header.

## Related Test Cases

- [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md)

## Remediation

- When implementing OAuth always consider the used technology wether it is a server side application that can keep a secret or a client side application which can't.
- In almost any case use the Authorization Code Flow + PKCE. Exceptions of that are M2M flows.
- Use Post parameters or Header values to transport secrets.
- When no other possibility exists, legacy applications that can not be migrated for example, implement additional
  security headers like a `Referrer-Policy` policy.

## Tools

- [BurpSuite](https://portswigger.net/burp/releases)
  - [EsPReSSO](https://github.com/portswigger/espresso)
- [OWASP ZAP](https://www.zaproxy.org/)

## References

- [User Authentication with OAuth 2.0](https://oauth.net/articles/authentication/)
- [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
- [OAuth 2.0 Threat Model and Security Considerations](https://datatracker.ietf.org/doc/html/rfc6819)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-16)
- [Authorization Code Flow with Proof Key for Code Exchange](https://auth0.com/docs/authorization/flows/authorization-code-flow-with-proof-key-for-code-exchange-pkce)
