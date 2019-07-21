# API Testing

Web APIs have gained a lot of popularity as they allow third-party programs to interact with websites in a more efficient and easy way. In this guide, we will discuss some basic concepts about APIs and the way to test security for APIs.

## Background Concepts

REST (Representational State Transfer) is an architecture that is implemented while developer design APIs.
Web application APIs following the REST style are called REST API.
REST APIs use URIs (Uniform Resource Identifiers) to access resources. The generic URI syntax as defined in [RFC3986](https://tools.ietf.org/html/rfc3986) as below:

> URI = scheme "://" authority "/" path [ "?" query ] [ "#" fragment ]

We are interested in the path of URI as the relationship between user and resources.
For example, `https://api.test.xyz/admin/testing/report`, this shows report of testing, there is relationship between user admin and their reports.

The path of any URI will define REST API resource model, resources are separated by a forward slash and based on Top-Down design.
For example:

- `https://api.test.xyz/admin/testing/report`
- `https://api.test.xyz/admin/testing/`
- `https://api.test.xyz/admin/`

REST API requests follow the [HTTP Request Methods](https://tools.ietf.org/html/rfc7231#section-4) defined in [RFC7231](https://tools.ietf.org/html/rfc7231)

| Methods | Description                                   |
|---------|-----------------------------------------------|
| GET     | Get the representation of resource’s state    |
| POST    | Create a new resource                         |
| PUT     | Update a resource                             |
| DELETE  | Remove a resource                             |
| HEAD    | Get metadata associated with resource’s state |
| OPTIONS | List available methods                        |

REST APIs use the response status code of HTTP response message to notify the client about their request’s result.

| Response Code | Response Message      | Description                                                                                            |
|---------------|-----------------------|--------------------------------------------------------------------------------------------------------|
| 200           | OK                    | Success while processing client's request                                                              |
| 201           | Created               | New resource created                                                                                   |
| 301           | Moved Permanently     | Permanent redirection                                                                                  |
| 304           | Not Modified          | Caching related response that returned when the client has the same copy of the resource as the server |
| 307           | Temporary Redirect    | Temporary redirection of resource                                                                      |
| 400           | Bad Request           | Malformed request by the client                                                                        |
| 401           | Unauthorized          | Client is not allowed to make requests or access a particular resource                                 |
| 402           | Forbidden             | Client is forbidden to access the resource                                                             |
| 404           | Not Found             | Resource doesn't exist or incorrect based on the request                                               |
| 405           | Method Not Allowed    | Invalid method or unknown method used                                                                  |
| 500           | Internal Server Error | Server failed to process request due to an internal error                                              |

HTTP headers are used in requests and responses.
While making API requests, Content-Type header is used and is set to `application/json` because the message body contains JSON data format.

Web authentication types are based on:

- Bearer Tokens: Identified by the `Authorization: Bearer <token>` header. Once a user logs in, they are provided with a bearer token that is sent on every request in order to authenticate and authorize the user to access OAuth 2.0 protected resources.
- HTTP Cookies: Identified by the `Cookie: <name>=<unique value>` header. On user login success, the server replies with a `Set-Cookie` header specifying its name and unique value. On every request, the browser automatically appends it to the requests going to that server, following [SOP](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy).
- Basic HTTP authentication: Identified by the `Authorization: Basic <base64 value>` header. Once a user is trying to login, the request is sent with the mentioned header containing the a base64 value, having its content as `username:password`. This is one of the weakest forms of authentication as it transmits the username and password on every request in an encoded manner, which can be easily retrieved.

## How to Test

### Generic Testing Method

Step 1: List endpoint and make different request method: Login with user and then using a spider tool to list the endpoints of this role.
To examine the endpoints, need to make different request methods and then observe how the API behaves.

Step 2: Exploit bugs- as know how to list endpoints and examine endpoints with HTTP methods at step 1, we will find some way to exploit bugs as some testing strategies below:

- IDOR testing
- Privilege escalation

### Specific Testing – (Token-Based) Authentication

Token-based authentication is implemented by sending a signed token (verified by the server) with each HTTP request.
The most commonly used token format is the JSON Web Token (JWT), defined in [RFC7519](https://tools.ietf.org/html/rfc7519).
A JWT may encode the complete session state as a JSON object.
Therefore, the server doesn't have to store any session data or authentication information.

Example 1:

JWT consist of three Base64-encoded parts separated by dots. The following example shows a Base64-encoded JSON Web Token:

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMzQ1Njc4OTAiLCJuYW1lIjoiQWxpY2UiLCJpc0FkbWluIjoiRmFsc2UifQ.DERSXICJKao4Q4Cbao3FuPJWQy8CVAcwc84rLEeeQeQ`

The header typically consists of two parts: the token type, which is JWT, and the hashing algorithm being used to compute the signature. In the example above, the header decodes as follows:

```json
{ "alg": "HS256", "typ": "JWT"}
```

The second part of the token is the payload, which contains so-called claims. Claims are statements about an entity (typically, the user) and additional metadata.
For example:

```json
{ "id": "1234567890", "name": "Alice", "isAdmin": "False"}
```

The signature is created by applying the algorithm specified in the JWT header to the encoded header, encoded payload, and a secret value. For example, when using the HMAC SHA256 algorithm the signature is created in the following way:

```c#
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
```

Step 1: Login with valid credentials. With ZAProxy or BurpSuite, we can retrieve JWT token.

Step 2: Access the [JWT Debugger](https://jwt.io/#debugger) and then Decode the Base64-encoded JWT and find out what kind of data it transmits and whether that data is encrypted.
Verify that no sensitive data, such as personal identifiable information, is embedded in the JWT.
If, for some reason, the architecture requires transmission of such information in the token, make sure that payload encryption is being applied.

Step 3: Cracking the signing key. Token signatures are created via a private key on the server.
After you obtain a JWT, choose a tool for brute forcing the secret key offline.

Step 4: Analyze the decoded value, try to tamper parameter like “id” or “isAdmin” in above example to another value that lead to Insecure Direct Object References Attack or Privilege escalation attack.

Step 5: Modify the alg attribute in the token header, then delete HS256 , set it to ‘none’ , and use an empty signature (e.g., signature = ""). Use this token and replay it in a request.
Some libraries treat tokens signed with the none algorithm as a valid token with a verified signature.
This allows attackers to create their own "signed" tokens.

Step 6: Perform a couple of operations that require authentication inside the application.

Step 7: Log out or change password of concurrent working user.

Step 8: Resend one of the operations from step 6 with an interception proxy (Burp Repeater, for example). This will send to the server a request with the session ID or token that was invalidated in step 7.

### Specific Testing – Brute Forcing Weak Secrets Used for JWT

Step 1: Clone the repository [JWT Cracker](https://github.com/brendan-rius/c-jwt-cracker)

Step 2: Navigate to cloned repository and compile the source code using 'make'

Step 3: Run `./jwtcrack <JWT>`

In case of weak secret value, this will bruteforce the secret.
  
## Related Test Cases

- [IDOR](https://github.com/OWASP/OWASP-Testing-Guide-v5/blob/master/document/4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6.4_Testing_for_Insecure_Direct_Object_References_OTG-AUTHZ-004.md)
- [Privilege escalation](https://github.com/OWASP/OWASP-Testing-Guide-v5/blob/master/document/4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6.3_Testing_for_Privilege_Escalation_OTG-AUTHZ-003.md)
- All [Session Management](https://github.com/OWASP/OWASP-Testing-Guide-v5/tree/master/document/4_Web_Application_Security_Testing/4.7_Session_Management_Testing) test cases

## Tools

- ZAProxy
- Burp suite

## References

- [REST HTTP Methods](https://restfulapi.net/http-methods/)
- [RFC3986 URI](https://tools.ietf.org/html/rfc3986)
- [JWT](https://jwt.io/)
- [Cracking JWT](https://www.sjoerdlangkemper.nl/2016/09/28/attacking-jwt-authentication/)
