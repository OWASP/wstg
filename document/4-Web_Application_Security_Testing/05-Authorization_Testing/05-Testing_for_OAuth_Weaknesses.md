# Testing OAuth Weaknesses

|ID          |
|------------|
|WSTG-ATHZ-05|

## Summary

[OAuth2.0](https://oauth.net/2/) is an authorization framework used in web-enabled applications and APIs it will be referred to as just OAuth.
It enables a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner by orchestrating an approval interaction
between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf.

Authorization information is typically being proofed using a bearer token that if presented to a service should tell the service which access rights may be assigned to the request. Therefore the JWT checks in WSTG-SESS-10 also apply to the Testing for OAuth weaknesses chapter. The usage of Bearer Token with OAuth is described in rfc6750.

OAuth itself can be used for authentication but it is generally not recommended to implement your own way of doing so. Instead authentication should be implemented with the OpenID Connect standard.

Since OAuth's responsebillity is it to delegate access rights across several services, successfull atacks may lead to account takeover, unauthorized ressource access and the elevation of privileges.

## Test Objectives

- Are the clients confidential or public
- Determine which OAuth flow is used
- Retrieve credentials used for authorization
- Grant yourself access to arbitrary ressources trough forcefull browsing
- Bypass the authorization

## How to Test

### Overview

OAuth has five different entities that are part of an OAuth exchange.

- Ressource Owner (user)
- User Agent (browser, native app)
- Client (the application which requests access to a Ressource on behalf of the Ressource Owner)
- Authorization Server (a server which holds authorization information and grants the access)
- Ressource Server (an application that serves content accessed by the client)

Based on the applications abillity to keep a secret in secret it seperates clients into two distinct types:

- Confidential
- Public

Confidential Clients are typically applications with server side code that are able to prevent anyone from acessing the secret.
Public Clients in contrast are unable to keep the secret secret, an example for a Public Client would be a SPA which has all the code present on the User Agent

In order to understand the attack surface it is crucial to determine which OAuth Grant Type is used for the application you are testing against.

These are the most common OAuth Grant Types:

- Authorization Code
- Consent
- Proof Key for Code Exchange (PKCE)
- Client Credentials
- Device Code
- Refresh Token

Authorization Code Grant is commonly used in conjuction with the PKCE Grant. It is the recommended Grant Type in most situations.

### Testing for improper Grant Type

Depending on the architecture of the web app that is tested, different grant types should be used.

#### How to test

The grant type is part of the authorization request URL. It is present in the `response_type` query parameter

```http
GET /auth/realms/example/protocol/openid-connect/auth?client_id=app-angular2&redirect_uri=http%3A%2F%client.example.com%2Fapp-angular2%2F&state=19abbae7-79cb-4e82-8ea1-897d98251f4e&response_mode=fragment&response_type=code&scope=openid&nonce=636db683-18ba-4c92-a56f-a7f7ccd772ce HTTP/1.1
Host: idp.exemple.com
[...]
```

#### Public Clients

The proper grant for public clients is the code-grant with the PKCE extension.
The authorization request for Code Flow + PKCE should contain `response_type=code` and `code_challenge=sha256(xyz)`.

Improper grant types for public client:

- Code Grant without the PKCE extension
- Direct Access Grant
- Refresh Token (if the user agent can securly store the token) see. %%TODO Insert ref. to Session Storage%%

#### Confidential Clients

Most of the time the code-grant with the PKCE extension can also be used for confidential clients.

- Direct Access Grant

#### Restricted User Agent

Some clients have a user agent with limited capabilities. Those include Smart TVs and other devices with similar restricted input capabilities.
For such devices the `Device Grant` flow is appropiate.

#### Machine to Machine

Such clients may make use of the bearer only grant type. Since machine to nachine communication is per-definition invisible to a user-agent
it is generally not possible to test without a Machine in the middle setup.
%%TODO%%

### Cross Site Request Forgery

CSRF attacks are described in [CSRF](xxx.md) there are few targets in OAuth that can be attacked with CSRF.

Targets:

- Consent Page
- Code Flow

#### Consent Page

The consent page is displayed to a user to verify that this user consensts in the client accessing the ressource on the users behalf. Attacking the consent page with a CSRF migth grant an aritrary client access to a ressource on behalf of the user.

### Clickjacking

When the consent page is prone to clickjacking and the attacker is in posession of the clientId (for public clients) and additionally the client secret for confidential client, the attacker can forge the users consent and gain access to the users account information throug a rogue client.

### Mix-Up Attacks

TODO

### Access Token Injection

TODO

### Refresh Token Protection

- Use only once

### Client Impersonating Resource Owner

- public clients (csrf)

### Credential Leakage via Referer Header

TODO

### Credential Leakage via Browser History

TODO

## Related Test Cases

- [CORS](xxx.md)
- [CSRF](xxx.md)
- [Open Redirect](xxx.md)
- [JWT](xxx.md)
- [Clickjacking](xxx.md)

## Remediation

Do not make a habit of putting cats in boxes. Keep boxes away from cats as much as possible.

## Tools

- BurpSuite
- OWASP ZAP

## References

- [User Authentication with OAuth 2.0](https://oauth.net/articles/authentication/)
- [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
- [OAuth 2.0 Threat Model and Security Considerations](https://datatracker.ietf.org/doc/html/rfc6819)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-16)
- [Authorization Code Flow with Proof Key for Code Exchange](https://auth0.com/docs/authorization/flows/authorization-code-flow-with-proof-key-for-code-exchange-pkce)
