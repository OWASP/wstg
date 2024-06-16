# API Testing Overview

## Web API Introduction

A Web Application Programming Interface (API) facilitates communication and data exchange between different software systems over a network or the internet. Web APIs enable different applications to interact with each other in a standardized and efficient manner, allowing them to leverage each other's functionalities and data.

The adoption of different technologies such as cloud computing, microservice architectures, and single page applications have all contributed to the adoption of APIs as an architectural movement.

As with the introduction of any new concepts, there can be flaws and vulnerabilities that necessitate testing. Otherwise, poorly secured APIs may provide an unrestricted direct path to sensitive data.

This chapter attempts to guide the security researcher in the concepts necessary for testing APIs. This section in particular investigates the different API technologies and their history.

## Which API Technology?

Before we make assumptions about the type of API we are testing, it can be helpful to be aware of the full scope of the problem space that the security researcher may encounter. These include:

1. Representational State Transfer (REST) APIs
2. Simple Object Access Protocol (SOAP) APIs
3. GraphQL APIs
4. gRPC Remote Procedure Calls (gRPC)
5. WebSockets APIs

## REST (Representational State Transfer) APIs

### What is REST?

REST is a set of rules and conventions for interacting with web resources. The key components of URI, HTTP Methods, Headers, and Status Codes support the principles of REST.

### History
  
Due to their simplicity, scalability, and compatibility with existing web infrastructure, REST based APIs have become the most common API architecture on the internet at the time of this writing. REST based APIs did not immediately manifest, but rather have a long path from research to adoption.

In 1994 Roy Fielding, one of the principal authors of the HTTP specification, began his work on REST as part of his doctoral dissertation at the University of California, Irvine. By 2000, he published his dissertation, [Architectural Styles and the Design of Network-based Software Architectures](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm), where he introduced and defined REST as an architectural style. REST was designed to take advantage of the existing features of HTTP, emphasizing scalability, stateless interactions, and a uniform interface.

In the 2010s REST became the de facto standard for web APIs due to its simplicity and compatibility with the web's underlying architecture. The widespread use of RESTful APIs was driven by the growth of mobile applications, cloud computing, and microservices architecture. The development of tools and frameworks like Swagger/OpenAPI, RAML, and API Blueprint facilitated the design, documentation, and testing of REST APIs.

By the 2020s modern developments evolved REST with technologies such as GraphQL. In addition, the OpenAPI/Swagger specification became a widely adopted standard for describing REST APIs, enabling better integration and automation.

### Uniform Resource Identifiers

REST APIs use Uniform Resource Identifiers (URIs) to access resources. URIs are a crucial element of a REST Architecture. A URI is a string of characters that uniquely identifies a particular resource. URIs are used extensively on the internet to locate and interact with resources, such as web pages, files, and services.

A URI consists of several components, each serving a specific purpose. The generic URI syntax as defined in [RFC3986](https://tools.ietf.org/html/rfc3986) is below:

> `URI = scheme "://" authority "/" path [ "?" query ] [ "#" fragment ]`

For REST, the **scheme** is typically `HTTP` or `HTTPS` but generically indicates the protocol or method used to access the resource. Other common schemes include `ftp`, `mailto`, and `file`.

The **authority** specifies the domain name or IP address of the server where the resource resides, and may include a port number. It may also include userinfo as a subcomponent.

The **path** specifies the specific location of the resource on the server. We are interested in the path of URI as the relationship between user and resources. For example, `https://api.example.com/admin/testing/report` may show a test report. There is relationship between the user admin and their reports.

The path of any URI will define a REST API resource model. Resources are separated by a forward slash and based on Top-Down design.

For example:

- `https://api.example.com/admin/testing/report`
- `https://api.example.com/admin/testing/`
- `https://api.example.com/admin/`

The **query** provides additional parameters for the resource. It starts with a `?` and consists of key-value pairs separated by `&`.

The **fragment** indicates a specific part of the resource, such as a section within a web page. It starts with a `#`. It's worth noting that fragment identifiers are only processed client-side and not sent to the server.

### HTTP Methods

REST APIs use standard HTTP methods to perform operations on resources following the [HTTP Request Methods](https://tools.ietf.org/html/rfc7231#section-4) defined in [RFC7231](https://tools.ietf.org/html/rfc7231). These methods map to CRUD, the four basic functions of persistent storage in computer science. CRUD stands for Create, Read, Update, and Delete, which are the four operations that can be performed on data.

HTTP Request Methods are:

| Methods | Description                                   |
|---------|-----------------------------------------------|
| GET     | Get the representation of resource’s state    |
| POST    | Create a new resource                         |
| PUT     | Update a resource                             |
| DELETE  | Remove a resource                             |
| HEAD    | Get metadata associated with resource’s state |
| OPTIONS | List available methods                        |

#### Headers

REST relies on headers to support communication of additional information within the request or response. These include:

- `Content-Type`: Indicates the media type of the resource (e.g. `application/json`).
- `Authorization`: Contains credentials for authentication (e.g. tokens).
- `Accept`: Specifies the media types that are acceptable for the response.

#### Status Codes

Application APIs that conform to REST principles use the response status code of an HTTP response message to notify the client about their request’s result.

| Response Code | Response Message      | Description   |
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

## References

1. [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
2. [OWASP REST Assessment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Assessment_Cheat_Sheet.html)
3. [OWASP API Security Project](https://owasp.org/www-project-api-security/)
4. [OWASP API Security Tools](https://owasp.org/www-community/api_security_tools)
