# API Testing

Web APIs have gained a lot of popularity as they allow third-party programs to interact with sites in a more efficient and easy way. In this guide, we will discuss some basic concepts about APIs and the way to test security for APIs.

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

Step 1: List endpoint and make different request method: Login with user profile and use a spider tool to list the endpoints of this role.
To examine the endpoints, you will need to make different request methods and observe how the API behaves.

Step 2: Exploit bugs - As know how to list endpoints and examine endpoints with HTTP methods at step 1, we will find some way to exploit bug. Some testing strategies are below:

- IDOR testing
- Privilege escalation

### Specific Testing – (Token-Based) Authentication

Token-based authentication is implemented by sending a signed token (verified by the server) with each HTTP request.

The most commonly used token format is the JSON Web Token (JWT), defined in [RFC7519](https://tools.ietf.org/html/rfc7519). The [Testing JSON Web Tokens](/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md) guide contains further details on how to test JWTs.

## Related Test Cases

- [IDOR](https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md)
- [Privilege escalation](https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/05-Authorization_Testing/03-Testing_for_Privilege_Escalation.md)
- All [Session Management](https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing/06-Session_Management_Testing) test cases
- [Testing JSON Web Tokens](/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md)

## Tools

- ZAP
- Burp suite

## References

- [REST HTTP Methods](https://restfulapi.net/http-methods/)
- [RFC3986 URI](https://tools.ietf.org/html/rfc3986)
- [JWT](https://jwt.io/)
- [Cracking JWT](https://www.sjoerdlangkemper.nl/2016/09/28/attacking-jwt-authentication/)
