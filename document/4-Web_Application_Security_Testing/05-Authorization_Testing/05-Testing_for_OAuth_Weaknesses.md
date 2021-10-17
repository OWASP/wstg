# Testing OAuth Weaknesses

|ID          |
|------------|
|WSTG-ATHZ-05|

## Summary

[OAuth2.0](https://oauth.net/2/) is an authorization framework used in web-enabled applications and APIs it will be referred to as OAuth.
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

- Ressource Owner, the entity who grants access to a ressource
- User Agent, browser, native app
- Client, the application which requests access to a ressource on behalf of the Ressource Owner
- Authorization Server, a server which holds authorization information and grants the access
- Ressource Server, an application that serves content accessed by the client

Based on the applications abillity to keep a secret in secret it seperates clients into two distinct types:

- Confidential
- Public

Confidential Clients are typically applications with server side code that are able to prevent anyone from acessing the secret.
Public Clients in contrast are unable to keep the secret secret, an example for a Public Client would be a SPA which has all the code present on the User Agent

In order to understand the attack surface it is crucial to determine which OAuth Grant Type is used for the application you are testing against.

These are the most common OAuth Grant Types:

- Authorization Code, commonly used with confidential client
- Proof Key for Code Exchange (PKCE), commonly used with public clients in conjunction with Authorization Code
- Consent, Requiered for the approval of third party clients
- Client Credentials, used for machine to machine communication
- Device Code, used for devices with limited input capabilitied

### Testing for improper Grant Type

Depending on the architecture of the application, different grant types should be used. 

> **NOTE**:  
> The Ressource Owner Password Credential Grant (ROPCG) is deprecated and poses a security risk.  

#### How to test

It is generally possible to identify the grant type as it is part of the token exchange in the parameter `grant_type`. Following example shows the Authorization Code Grant + PKCE. PKCE can be identified by the `code_verifier` parameter.

```http
POST /oauth/token HTTP/2
Host: idp.exemple.com
[...]

{
    "client_id":"ZXhhbXBsZQ",
    "code_verifier":"fuV-R1Yyxs-1rSk7XInhp5NXGj0PJucD0q5J5VF_qWp",
    "grant_type":"authorization_code",
    "code":"ZqQcutj6aOe_TBfzOGJewgZsu99kgbrbW24zz-8QUpu86",
    "redirect_uri":"http://client.example.com
    }
```

#### Public Clients

Recommended for public client is the code-grant with the PKCE extension.
An authorization request for Code Flow + PKCE should contain `response_type=code` and `code_challenge=sha256(xyz)`.

```http
GET /authorize?redirect_uri=http%3A%2F%2Flocalhost%3A4200&client_id=ZXhhbXBsZQ&scope=openid%20profile%20email&response_type=code&response_mode=query&state=ZXhhbXBsZQ%3D%3D&nonce=ZXhhbXBsZQ%3D%3D&code_challenge=eNJJZHGTgeaB-RV61cQCesIdnCOQ_Pv5tENQ9xBnKh4&code_challenge_method=S256& HTTP/2
Host: idp.example.com
[...]
```

Improper grant types for public client:

- Code Grant without the PKCE extension
- Client Credentials
- Ressource Owner Password Credential Grant

#### Confidential Clients

The code-grant is recommended for confidential client and the PKCE extension may be used as well.

Improper grant types for confidential client:

- Ressource Owner Password Credential Grant

##### Machine to Machine

Machine to Machine clients generally should be able to keep a secret and therefore may be confidentials clients. No user interaction can happen and they may relie solely on the client secret with the Client Credentials grant.

If you already know the client secret it is possible to obtain a token.

```bash
λ curl --request POST \
  --url https://alcastronic.eu.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"ZXhhbXBsZQ","client_secret":"THE_CLIENT_SECRET","audience":"https://idp.example.com/","grant_type":"client_credentials"}' --proxy http://localhost:8080/ -k
```

#### Restricted User Agent

Some clients have a user agent with limited capabilities. Those include Smart TVs and other devices with similar restricted input capabilities.

For such devices the `Device Grant` flow is appropiate.

### Cross Site Request Forgery

CSRF attacks are described in [CSRF](xxx.md) there are few targets in OAuth that can be attacked with CSRF.

Targets:

- Consent Page
- Authorization Code Flow

#### Consent Page

The consent page is displayed to a user to verify that this user consensts in the client accessing the ressource on the users behalf. Attacking the consent page with a CSRF migth grant an arbitrary client access to a ressource on behalf of the user.

1. Client generates a state parameter and sends it with the consent request.
2. User Agent displays the consent page
3. Ressource Owner grant's access to the client
4. The consent is sent to the IdP together with the acknowledged scopes

To prevent CSRF attacks OAuth leaverages the `state` parameter as an anti CSRF token. Use a tool like OWASP ZAP to test if the state parameter is properly validated.

```http
POST /u/consent?state=Tampered_State HTTP/2
Host: idp.example.com
[...]

state=Tampered_State&audience=https%3A%2F%2Fidp.example.com%2Fuserinfo&scope%5B%5D=profile&scope%5B%5D=email&action=accept
```

#### Authorization Code Flow

CSRF with authorization code flow.

### Clickjacking

When the consent page is prone to clickjacking and the attacker is in posession of the clientId (for public clients) and additionally the client secret for confidential client, the attacker can forge the users consent and gain access to the users account information throug a rogue client.

### Mix-Up Attacks

TODO

### Access Token Injection

TODO

### Refresh Token Protection

- Use only once



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
