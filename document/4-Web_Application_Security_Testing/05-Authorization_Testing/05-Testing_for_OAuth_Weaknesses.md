# Testing for OAuth Weaknesses

|ID          |
|------------|
|WSTG-ATHZ-05|

## Summary

[OAuth2.0](https://oauth.net/2/) (hereinafter referred to as OAuth) is an authorization framework that allows a client to access resources on the behalf of its user.

In order to achieve this, OAuth heavily relies on tokens to communicate between the different entities, each entity having a different [role](https://datatracker.ietf.org/doc/html/rfc6749#section-1.1):

- **Resource Owner:** The entity who grants access to a resource, the owner, and in most cases is the user themselves
- **Client:** The application that is requesting access to a resource on behalf of the Resource Owner. These clients come in two [types](https://oauth.net/2/client-types/):
    - **Public:** clients that can't protect a secret (*e.g.* frontend focused applications, such as SPAs, mobile applications, etc.)
    - **Confidential:** clients that are able to securely authenticate with the authorization server by keeping their registered secrets safe (*e.g.* backend services)
- **Authorization Server:** The server that holds authorization information and grants the access
- **Resource Server:** The application that serves the content accessed by the client

Since OAuth's responsibility is to delegate access rights by the owner to the client, this is a very attractive target for attackers, and bad implementations lead to unauthorized access to the users' resources and information.

In order to provide access to a client application, OAuth relies on several [authorization grant types](https://oauth.net/2/grant-types/) to generate an access token:

- [Authorization Code](https://oauth.net/2/grant-types/authorization-code/): used by both confidential and public clients to exchange an authorization code for an access token, but recommended only for confidential clients
- [Proof Key for Code Exchange (PKCE)](https://oauth.net/2/pkce/): PKCE builds on top of the Authorization Code grant, providing stronger security for it to be used by public clients, and improving the posture of confidential ones
- [Client Credentials](https://oauth.net/2/grant-types/client-credentials/): used for machine to machine communication, where the "user" here is the machine requesting access to its own resources from the Resource Server
- [Device Code](https://oauth.net/2/grant-types/device-code/): used for devices with limited input capabilities.
- [Refresh Token](https://oauth.net/2/grant-types/refresh-token/): tokens provided by the authorization server to allow clients to refresh users' access tokens once they become invalid or expire. This grant type is used in conjunction with one other grant type.

Two flows will be deprecated in the release of [OAuth2.1](https://oauth.net/2.1/), and their usage is not recommended:

- [Implicit Flow*](https://oauth.net/2/grant-types/implicit/): PKCE's secure implementation renders this flow obsolete. Prior to PKCE, the implicit flow was used by client-side applications such as [single page applications](https://en.wikipedia.org/wiki/Single-page_application) since [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) relaxed the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) for sites to inter-communicate. For more information on why the implicit grant is not recommended, review this [section](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics#section-2.1.2).
- [Resource Owner Password Credentials](https://oauth.net/2/grant-types/password/):used to exchange users' credentials directly with the client, which then sends them to the authorization to exchange them for an access token. For information on why this flow is not recommended, review this [section](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics#section-2.4).

*: The implicit flow in OAuth only is deprecated, yet is still a viable solution within Open ID Connect (OIDC) to retrieve `id_tokens`. Be careful to understand how the implicit flow is being used, which can be identified if only the `/authorization` endpoint is being used to gain an access token, without relying on `/token` endpoint in any way. An example on this can be found [here](https://auth0.com/docs/get-started/authentication-and-authorization-flow/implicit-flow-with-form-post).

*Please note that OAuth flows are a complex topic, and the above includes only a summary of the key areas. The inline references contain further information about the specific flows.*

## Test Objectives

- Determine if OAuth2 implementation is vulnerable or using a deprecated or custom implementation.

## How to Test

### Testing for Deprecated Grant Types

Deprecated grant types were obsoleted for security and functionality reasons. Identifying if they're being used allows us to quickly review if they're susceptible to any of the threats pertaining to their usage. Some might be out of scope to the attacker, such as the way a client might be using the users' credentials. This should be documented and raised to the internal engineering teams.

For public clients, it is generally possible to identify the grant type in the request to the `/token` endpoint. It is indicated in the token exchange with the parameter `grant_type`.

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

The Implicit Flow type is not indicated by the `grant_type` parameter since the token is presented in the response to the `/authorization` endpoint request, and instead can be identified through the `response_type`. Below is an example.

```http
GET /authorize
  ?client_id=<some_client_id>
  &response_type=token 
  &redirect_uri=https%3A%2F%2Fclient.example.com%2F
  &scope=openid%20profile%20email
  &state=<random_state>
```

The following URL parameters indicate the OAuth flow being used:

- `response_type=token`: Indicates Implicit Flow, as the client is directly requesting from the authorization server to return a token.
- `response_type=code`: Indicates Authorization Code flow, as the client is requesting from the authorization server to return a code, that will be exchanged afterwards with a token.
- `code_challenge=sha256(xyz)`: Indicates the PKCE extension, as no other flow uses this parameter.

The following is an example authorization request for Authorization Code flow with PKCE:

```http
GET /authorize
    ?redirect_uri=https%3A%2F%2Fclient.example.com%2F
    &client_id=<some_client_id>
    &scope=openid%20profile%20email
    &response_type=code
    &response_mode=query
    &state=<random_state>
    &nonce=<random_nonce>
    &code_challenge=<random_code_challenge>
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

In situations where no user interaction occurs and the clients are only confidential clients, the Client Credentials grant may be used.

If you know the `client_id` and `client_secret`, it is possible to obtain a token by passing the `client_credentials` grant type.

```bash
$ curl --request POST \
  --url https://as.example.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"<some_client_id>","client_secret":"<some_client_secret>","grant_type":"client_credentials"}' --proxy http://localhost:8080/ -k
```

### Credential Leakage

Depending on the flow, OAuth transports several types of credentials in as URL parameters.

The following tokens can be considered to be leaked credentials:

- access token
- refresh token
- authorization code
- PKCE code challenge / code verifier

Due to how OAuth works, the authorization `code` as well as the `code_challenge`, and `code_verifier` may be part of the URL. The implicit flow transports the authorization token as part of the URL if the `response_mode` is not set to [`form_post`](https://openid.net/specs/oauth-v2-form-post-response-mode-1_0.html). This may lead to leakage of the requested token or code in the referrer header, in log files, and proxies due to these parameters being passed either in the query or the fragment.

The risk that's carried by the implicit flow leaking the tokens is far higher than leaking the `code` or any other `code_*` parameters, as they are bound to specific clients and are harder to abuse in case of leakage.

In order to test this scenario, make use of an HTTP intercepting proxy such as ZAP and intercept the OAuth traffic.

- Step through the authorization process and identify any credentials present in the URL.
- If any external resources are included in a page involved with the OAuth flow, analyze the request made to them. Credentials could be leaked in the referrer header.

After stepping through the OAuth flow and using the application, a few requests are captured in the request history of an HTTP intercepting proxy. Search for the HTTP referrer header (e.g. `Referer: https://idp.example.com/`) containing the authorization server and client URL in the request history.

Reviewing the HTML meta tags (although this tag is [not supported](https://caniuse.com/mdn-html_elements_meta_name_referrer) on all browsers), or the [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) could help assess if any credential leakage is happening through the referrer header.

## Related Test Cases

- [Testing JSON Web Tokens](../06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md)

## Remediation

- When implementing OAuth, always consider the technology used and whether the application is a server-side application that can avoid revealing secrets, or a client-side application that cannot.
- In almost any case, use the Authorization Code flow with PKCE. One exception may be machine-to-machine flows.
- Use POST parameters or header values to transport secrets.
- When no other possibilities exists (for example, in legacy applications that can not be migrated), implement additional security headers such as a `Referrer-Policy`.

## Tools

- [BurpSuite](https://portswigger.net/burp/releases)
- [EsPReSSO](https://github.com/portswigger/espresso)
- [ZAP](https://www.zaproxy.org/)

## References

- [User Authentication with OAuth 2.0](https://oauth.net/articles/authentication/)
- [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
- [OAuth 2.0 Threat Model and Security Considerations](https://datatracker.ietf.org/doc/html/rfc6819)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-16)
- [Authorization Code Flow with Proof Key for Code Exchange](https://auth0.com/docs/authorization/flows/authorization-code-flow-with-proof-key-for-code-exchange-pkce)
