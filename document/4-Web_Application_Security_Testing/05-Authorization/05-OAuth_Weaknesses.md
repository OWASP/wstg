# OAuth Weaknesses

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

- [Authorization Code](https://oauth.net/2/grant-types/authorization-code/): used by both confidential and public clients to exchange an authorization code for an access token. [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700#section-2.1.1) requires public clients to protect this grant with PKCE, and recommends PKCE for confidential clients as well
- [Proof Key for Code Exchange (PKCE)](https://oauth.net/2/pkce/): PKCE binds the authorization code to the client instance that started the flow. Public clients MUST use it. Confidential clients SHOULD use it, even when they also authenticate with a client secret
- [Client Credentials](https://oauth.net/2/grant-types/client-credentials/): used for machine to machine communication, where the "user" here is the machine requesting access to its own resources from the Resource Server
- [Device Code](https://oauth.net/2/grant-types/device-code/): used for devices with limited input capabilities.
- [Refresh Token](https://oauth.net/2/grant-types/refresh-token/): tokens provided by the authorization server to allow clients to refresh users' access tokens once they become invalid or expire. This grant type is used in conjunction with one other grant type.

Two flows will be deprecated in the release of [OAuth2.1](https://oauth.net/2.1/), and their usage is not recommended:

- [Implicit Flow*](https://oauth.net/2/grant-types/implicit/): PKCE's secure implementation renders this flow obsolete. Prior to PKCE, the implicit flow was used by client-side applications such as [single page applications](https://en.wikipedia.org/wiki/Single-page_application) since [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) relaxed the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy) for sites to inter-communicate. For more information on why the implicit grant is not recommended, review this [section](https://datatracker.ietf.org/doc/html/rfc9700#section-2.1.2).
- [Resource Owner Password Credentials](https://oauth.net/2/grant-types/password/):used to exchange users' credentials directly with the client, which then sends them to the authorization to exchange them for an access token. For information on why this flow is not recommended, review this [section](https://datatracker.ietf.org/doc/html/rfc9700#section-2.4).

*: The implicit flow in OAuth only is deprecated, yet is still a viable solution within Open ID Connect (OIDC) to retrieve `id_tokens`. Be careful to understand how the implicit flow is being used, which can be identified if only the `/authorization` endpoint is being used to gain an access token, without relying on `/token` endpoint in any way. An example on this can be found [here](https://auth0.com/docs/get-started/authentication-and-authorization-flow/implicit-flow-with-form-post).

*Please note that OAuth flows are a complex topic, and the above includes only a summary of the key areas. The inline references contain further information about the specific flows.*

## Test Objectives

- Determine if OAuth2 implementation is vulnerable or using a deprecated or custom implementation.

## How to Test

### Deprecated Grant Types

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
  "redirect_uri":"https://client.example.com"
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
- `code_challenge=<BASE64URL-SHA256 of the code_verifier>` with `code_challenge_method=S256`: Indicates the PKCE extension. Prefer `S256`. Do not put the `code_verifier` itself into the authorization request.

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
    &code_challenge=<BASE64URL-SHA256 of the code_verifier>
    &code_challenge_method=S256 HTTP/1.1
Host: as.example.com
[...]
```

#### Public Clients

Public clients MUST use the Authorization Code grant with PKCE. An authorization request should contain `response_type=code`, a per-transaction `code_challenge`, and `code_challenge_method=S256`.

The token exchange should contain the grant type `authorization_code` and the matching `code_verifier` in the token request body (or other non-URL transport), not in the browser-visible redirect URL.

Improper grant types for public clients are:

- Authorization Code grant without the PKCE extension
- Client Credentials
- Implicit Flow
- ROPC

#### Confidential Clients

Confidential clients SHOULD also use the Authorization Code grant with PKCE. Client authentication alone does not stop authorization code injection when an attacker can cause the legitimate confidential client to redeem a stolen code. See [RFC 9700 Section 2.1.1](https://datatracker.ietf.org/doc/html/rfc9700#section-2.1.1).

Improper grant types for confidential clients are:

- Authorization Code grant without PKCE when the deployment can support PKCE
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
  --data '{"client_id":"<some_client_id>","client_secret":"<some_client_secret>","grant_type":"client_credentials"}' --proxy https://localhost:8080/ -k
```

### Credential Leakage

Depending on the flow, OAuth transports several types of credentials in as URL parameters.

The following tokens can be considered to be leaked credentials:

- access token
- refresh token
- authorization code
- PKCE `code_challenge` (expected in the authorization request URL)
- PKCE `code_verifier` (must appear only in the token request, not in browser-visible URLs)

Due to how OAuth works, the authorization `code` and the PKCE `code_challenge` may appear in browser-visible URLs. The `code_verifier` belongs in the token request to the authorization server, typically as a POST body parameter, and MUST NOT be placed in the authorization redirect URL. The implicit flow transports the authorization token as part of the URL if the `response_mode` is not set to [`form_post`](https://openid.net/specs/oauth-v2-form-post-response-mode-1_0.html). This may lead to leakage of the requested token or code in the referrer header, in log files, and proxies due to these parameters being passed either in the query or the fragment.

The risk carried by the implicit flow leaking access tokens is far higher than leaking an authorization `code` or a `code_challenge`. A stolen code is still dangerous for public clients without PKCE, and for confidential clients if the attacker can force the legitimate client to redeem it.

In order to test this scenario, make use of an HTTP intercepting proxy such as ZAP and intercept the OAuth traffic.

- Step through the authorization process and identify any credentials present in the URL.
- Confirm the `code_verifier` is sent only on the token request and is absent from the authorization redirect.
- If any external resources are included in a page involved with the OAuth flow, analyze the request made to them. Credentials could be leaked in the referrer header.

After stepping through the OAuth flow and using the application, a few requests are captured in the request history of an HTTP intercepting proxy. Search for the HTTP referrer header (e.g. `Referer: https://idp.example.com/`) containing the authorization server and client URL in the request history.

Reviewing the HTML meta tags (although this tag is [not supported](https://caniuse.com/mdn-html_elements_meta_name_referrer) on all browsers), or the [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy) could help assess if any credential leakage is happening through the referrer header.

## Related Test Cases

- [JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md)

## Remediation

- When implementing OAuth, always consider the technology used and whether the application is a server-side application that can avoid revealing secrets, or a client-side application that cannot.
- Prefer the Authorization Code flow with PKCE for both public and confidential clients. One exception may be machine-to-machine Client Credentials flows.
- Send the `code_verifier` in the token request body or another non-URL channel. Keep `code_challenge_method=S256`.
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
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/rfc9700)
- [Proof Key for Code Exchange by OAuth Public Clients](https://datatracker.ietf.org/doc/html/rfc7636)
- [Authorization Code Flow with Proof Key for Code Exchange](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce)
