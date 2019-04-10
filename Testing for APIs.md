# Summary
Web APIs have gained a lot of popularity because they allow third-party programs to interact with website in a more efficient and easy way.
In this section, we will discuss with some basic concepts about API and the way to test security for APIs.
# Background Concepts
REST (Reperesentational Sate Tranfer) is an architechture that is implemented while developer design APIs.
Web application APIs following the REST style that called REST API.
REST APIs using URIs (Uniform Resource Identifires) to access resources. The generic URI sysntax as defined in RFC 3986 as below:
```
URI = scheme "://" authority "/" path [ "?" query ] [ "#" fragment ]
```
We are interseted in the path of URI as the relationship between user and resources. 
For example, https://api.test.xyz/admin/testing/report, this shows report of testing, there is relationship between user admin and their reports.

The path of any URI will definre REST API resource model, resources are seperated by a forward slash and based on Top-Down design.
For example:
* https://api.test.xyz/admin/testing/report
* https://api.test.xyz/admin/testing/
* https://api.test.xyz/admin/ 

Request moethods are HTTP methods like GET,POST,… But at REST API’s model, these methods have fixed meaning.

| Methods        | Description    |
| ------------- |-------------|
| GET      | Get the representation of resource’s state |
| POST     | Create a new resource      | 
| PUT      | Update a resource     |
| DELETE   | Remove a resource     | 
| HEAD     | Get metadata associated with resource’s state    |
| OPTIONS  | List avaiable methods    | 

REST APIs use the response status code of HTTP response message to notify the client about their request’s result.

|Response Code |	Response Message |	Description |
| ------------ | ---------------| -------------------|
|200|	OK	|Success while processing client's request
|201|	Created|	New resource created
|301|	Moved Permanently|	Permanent redirection
|304|	Not Modified|	Caching related response that returned when the client has the same copy of the resource as the server
|307|	Temporary Redirect|	Temporary redirection of resource
|400|	Bad Request|	Malformed request by the client
|401|	Unauthorized|	Client is not allowed to make requests or access a particular resource
|402|	Forbidden|	Client is forbidden to access the resource
|404|	Not Found|	Resource doesn't exist or incorrect based on the request
|405|	Method Not Allowed|	Invalid method or unknown method used
|500|	Internal Server Error|	Server failed to process request due to an internal error

HTTP headers are used in request and reponses. 
While making API request, Content-Type header is used and is set to application/JSON, because message body contains JSON data format.

JSON authentication types are based on:
* Basic HTTP authentication: While making API requests, a new header, called the “Authorization” header  which contains authenticated information of a user in Base64 format.
* Access token: In APIs, an access token is sent with the request which is verified by the API server, and thus, depending on its authenticity, the request is accepted or rejected.
* Cookies: A session cookie is used to authenticate the user. A session cookie is cookie which is used to verify the user and is created when a successful login is registered. 
This cookie should be replayed with every API request and based on this a cookie request is accepted or rejected by the server.

# How to test
## Generic Testing Method
### Testing steps:
Step 1: Listing endpoint and make different request method: Login with user and then using Spider tool to list the endpoints of this role.
To examine the endpoints, need to make different request methods and then observe how the API behaves.

Step 2: Exploit bugs- as know how to list endpoints and examine endpoints with HTTP methods at step 1, 
we will find some way to exploit bugs as some testing strategies below:
* IDOR testing
* Privilege escalation

## Specific Testing – Testing (Token-Based) Authentication
Token-based authentication is implemented by sending a signed token (verified by the server) with each HTTP request. 
The most commonly used token format is the JSON Web Token, defined at [RFC7519](https://tools.ietf.org/html/rfc7519). 
A JWT may encode the complete session state as a JSON object.
Therefore, the server doesn't have to store any session data or authentication information.

Example 1:

JWT tokens consist of three Base64-encoded parts separated by dots. The following example shows a Base64-encoded JSON Web Token:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMzQ1Njc4OTAiLCJuYW1lIjoiQWxpY2UiLCJpc0FkbWluIjoiRmFsc2UifQ.DERSXICJKao4Q4Cbao3FuPJWQy8CVAcwc84rLEeeQeQ
```
The header typically consists of two parts: the token type, which is JWT, and the hashing algorithm being used to compute the signature. In the example above, the header decodes as follows:
```
{ "alg": "HS256", "typ": "JWT"}
```
The second part of the token is the payload, which contains so-called claims. Claims are statements about an entity (typically, the user) and additional metadata. 
For example:
```
{ "id": "1234567890", "name": "Alice", "isAdmin": "False"}
```
The signature is created by applying the algorithm specified in the JWT header to the encoded header, encoded payload, and a secret value. For example, when using the HMAC SHA256 algorithm the signature is created in the following way:
```
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
```
### Testing Steps:
Step 1: Login with valid credential. With ZAProxy or Burpsuite, we can retrieve JWT token.

Step 2: Access to https://jwt.io/#debugger and then Decode the Base64-encoded JWT and find out what kind of data it transmits and whether that data is encrypted. 
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

Step 8: Resend one of the operations from step 6 with an interception proxy (Burp Repeater, for example). . 
This will send to the server a request with the session ID or token that was invalidated in step 7.

## Specific Testing – Brute Forcing Weak Secrets Used for JWT
### Testing steps:
Step 1: Clone the repository https://github.com/brendan-rius/c-jwt-cracker

Step 2: Navigate to cloned repository and compile the source code using 'make'

Step 3: Run ./jwtcrack <JWT>
	
In case of weak secret value, this will bruteforce the secret.
  
# Related Test Cases
* [IDOR](https://github.com/OWASP/OWASP-Testing-Guide-v5/blob/master/document/4%20Web%20Application%20Security%20Testing/4.6%20Authorization%20Testing/4.6.4%20Testing%20for%20Insecure%20Direct%20Object%20References%20(OTG-AUTHZ-004).md)
* [Privilege escalation](https://github.com/OWASP/OWASP-Testing-Guide-v5/blob/master/document/4%20Web%20Application%20Security%20Testing/4.6%20Authorization%20Testing/4.6.3%20Testing%20for%20Privilege%20escalation%20(OTG-AUTHZ-003).md)
* All [Session Management](https://github.com/OWASP/OWASP-Testing-Guide-v5/tree/master/document/4%20Web%20Application%20Security%20Testing/4.7%20Session%20Management%20Testing) test cases

# Tools
* ZAProxy
* Burp suite

# References
* REST HTTP Methods - https://restfulapi.net/http-methods/
* RFC3886 URI - https://tools.ietf.org/html/rfc3986
* JWT - https://jwt.io/
* Cracking JWT - https://www.sjoerdlangkemper.nl/2016/09/28/attacking-jwt-authentication/
