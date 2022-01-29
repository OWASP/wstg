# Testing for OAuth Weaknesses

|ID          |
|------------|
|WSTG-ATHZ-05|

## Summary

[OAuth2.0](https://oauth.net/2/) is an authorization delegation framework used in web-enabled applications and APIs. Throughout this document it will be referred to as OAuth.

OAuth enables a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner by orchestrating an approval interaction between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf.

Authorization information is typically proofed using an access token that, if presented to a service, should tell the service which access rights may be assigned to the request. Access tokens may be opaque tokens called bearer tokens, but very often they are JSON Web Tokens (JWT). The JWT checks in [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md) are also relevant to testing for OAuth weaknesses. The usage of bearer tokens with OAuth is described in [RFC6750](https://datatracker.ietf.org/doc/html/rfc6750).

OAuth itself can be used for authentication, but implementing your own authentication is generally unwise. Instead, authentication should be implemented with the OpenID Connect standard.

Since OAuth's responsibility is to delegate access rights across several services, successful attacks may lead to account takeover, unauthorized resource access, and the elevation of privileges in regards to those services.

There are five different roles that are part of an OAuth exchange. In no particular order:

1. Resource Owner: The entity who grants access to a resource.
2. User Agent: The browser or native app.
3. Client: The application that is requesting access to a resource on behalf of the Resource Owner.
4. Authorization Server: The server that holds authorization information and grants the access.
5. Resource Server: The application that serves the content accessed by the client.

Clients may be confidential or public.

Confidential clients are typically applications with server-side code that are able to prevent anyone from accessing the secret.

Public clients, in contrast, are unable to prevent access to the secret. An example of a public client would be a single-page application that has all the code present on the user agent.

## Test Objectives

- Determine if deprecated or vulnerable OAuth methods are in use.

## How to Test

To test OAuth, two things must first be accomplished:

- Assess whether the clients are confidential or public.
- Determine which OAuth flow is used.

### Overview

In order to better understand the attack surface, it is crucial to determine which OAuth grant type is used for the application you are testing. The grant type determines the method by which the the application receives an access token.

These are the most common OAuth grant types:

- Authorization Code: Commonly used with confidential clients.
- Proof Key for Code Exchange (PKCE): Commonly used with public clients in conjunction with Authorization Code.
- Consent, Required for the approval of third party clients.
- Client Credentials: Used for machine to machine communication.
- Device Code: Used for devices with limited input capabilities.

### Testing for Deprecated Grant Type

The following two [OAuth grant types](https://oauth.net/2/grant-types/) are still part of the OAuth 2.0 specification, but are kept only to allow migration to newer grant types.

They are deprecated in [OAuth 2.1](https://oauth.net/2.1/) for security reasons.

- [Resource Owner Password Credential (ROPC)](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.3) grant: A long-lived token method used between trusted resource owner and client, now deprecated. This should only be used for migration purposes.
- [Implicit Flow](https://oauth.net/2/grant-types/implicit/): Designed to work around the lack of cross-site request possibilities in browsers. This issue is now solved with Cross-Origin Resource Sharing (CORS).

For public clients, it is generally possible to identify the grant type in the request to the token endpoint. It is indicated in the token exchange with the parameter `grant_type`.

The following example shows the Authorization Code grant with PKCE.

```http
POST /oauth/token HTTP/1.1
Host: as.example.com
[...]

{
  "client_id":"example-client",
  "code_verifier":"example",
  "grant_type":"authorization_code",
  "code":"example",
  "redirect_uri":"http://client.example.com"
}
```

The values for the `grant_type` parameter and the grant type they indicate are:

- `password`: Indicates the ROPC grant.
- `client_credentials`: Indicates the Client Credential grant.
- `authorization_code`: Indicates the Authorization Code grant.

The Implicit Flow type is not indicated by the `grant_type` parameter since the token is presented in the response to the authorization request. Below is an example.

The following URL parameters indicate the OAuth flow being used:

- `response_type=token`: Indicates Implicit Flow.
- `response_type=code`: Indicates Authorization Code flow.
- `code_challenge=sha256(xyz)`: Indicates the PKCE extension.

The following is an example authorization request for Authorization Code flow with PKCE:

```http
GET /authorize
    ?redirect_uri=http%3A%2F%2Fclient.example.com%2F
    &client_id=example-client
    &scope=openid%20profile%20email
    &response_type=code
    &response_mode=query
    &state=example
    &nonce=example
    &code_challenge=example
    &code_challenge_method=S256 HTTP/1.1
Host: as.example.com
[...]
```

#### Public Clients

The Authorization Code grant with PKCE extension is recommended for public clients. An authorization request for Authorization Code flow with PKCE should contain `response_type=code` and `code_challenge=sha256(xyz)`.

The token exchange should contain the grant type `authorization_code` and a `code_verifier`.

Improper grant types for public clients are:

- Authorization Code grant without the PKCE extension
- Client Credentials
- Implicit Flow
- ROPC

#### Confidential Clients

The Authorization Code grant is recommended for confidential clients. The PKCE extension may be used as well.

Improper grant types for confidential clients are:

- Client Credentials (Except for machine-to-machine -- see below)
- Implicit Flow
- ROPC

##### Machine-to-Machine

In situations where no user interaction occurs and the clients are only confidential clients, the Client Credentials grant may be used ([RFC6749 4.4](https://datatracker.ietf.org/doc/html/rfc6749#section-4.4)).

If you know the `client_id` and `client_secret`, it is possible to obtain a token by passing the `client_credentials` grant type.

```bash
$ curl --request POST \
  --url https://as.example.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"example-client","client_secret":"THE_CLIENT_SECRET","audience":"https://as.example.com/","grant_type":"client_credentials"}' --proxy http://localhost:8080/ -k
```

### Credential Leakage via Referrer Header

Depending on the flow, OAuth transports several types of credentials in as URL parameters.

The following tokens can be considered to be leaked credentials:

- access token
- refresh token
- authorization code
- PKCE code challenge / code verifier

Due to how OAuth works, the authorization `code` as well as the `code_challenge`, and `code_verifier` may be part of the URL. Therefore, it is even more relevant to ensure those are not sent in the referrer header.

Implicit Flow transports the authorization token as part of the URL. This may lead to leakage of the authorization token in the referrer header and in other places such as log files and proxies.

#### How to Test

Make use of an HTTP intercepting proxy such as OWASP ZAP and intercept the OAuth traffic.

- Step through the authorization process and identify any credentials present in the URL.
- If any external resources are included in a page involved with the OAuth flow, analyze the request made to them. Credentials could be leaked in the referrer header.

After stepping through the OAuth flow and using the application, a few requests are captured in the request history of an HTTP intercepting proxy. Search for the HTTP referrer header (e.g. `Referer: https://idp.example.com/`) containing the authorization server and client URL in the request history.

## Related Test Cases

- [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md)

## Remediation

- When implementing OAuth, always consider the technology used and whether the application is a server-side application that can avoid revealing secrets, or a client side application that cannot.
- In almost any case, use the Authorization Code flow with PKCE. One exception may be machine-to-machine flows.
- Use POST parameters or header values to transport secrets.
- When no other possibilities exists (for example, in legacy applications that can not be migrated), implement additional security headers such as a `Referrer-Policy`.

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
