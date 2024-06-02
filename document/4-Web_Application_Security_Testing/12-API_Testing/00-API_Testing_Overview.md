# API Testing Overview

|ID          |
|------------|
|WSTG-APIT-00|

## Web API Introduction

A Web API (Application Programming Interface) facilitates communication and data exchange between different software systems over a network or the Internet. Web APIs enable different applications to interact with each other in a standardized and efficient manner, allowing them to leverage each other's functionalities and data. 

The adoption of different technologies such as cloud computing, microservice architectures, and single page applications have all contributed to the adoption of APIs as an architectural movement.

And as with every introduction of new concepts follows the flaws, vulnerabilities, and the need for testing. Otherwise, poorly secured APIs may provide an unrestricted direct path to sensitive data.

This chapter attempts to guide the security researcher in the concepts neccessary for testing. This section in particular investigates the different API technologies and their history as a backgrounder.

## Which API Technology?

Before we stampede to REST based Web APIs we need to be aware of the full scope of the problem space that the security researcher may encounter. These include:

1. REST (Representational State Transfer) APIs.
2. SOAP (Simple Object Access Protocol) APIs.
3. GraphQL APIs.
4. gRPC (gRPC Remote Procedure Calls).
5. WebSockets APIs.


## REST (Representational State Transfer) APIs.

### History

Due to their simplicity, scalability, and compatibility with the existing web infrastructure REST based APIs have become the most common API architecture on the Internet at the time of this writing. REST based APIs did not immediately manifest, but rather have a long path from research to adoption.

In 1994 Roy Fielding, one of the principal authors of the HTTP specification, began his work on REST as part of his doctoral dissertation at the University of California, Irvine. By 2000, he published his dissertation, [Architectural Styles and the Design of Network-based Software Architectures](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm), where he introduced and defined REST as an architectural style. REST was designed to take advantage of the existing features of HTTP, emphasizing scalability, stateless interactions, and a uniform interface.

In the 2010s REST became the de facto standard for web APIs due to its simplicity and compatibility with the web's underlying architecture. The widespread use of RESTful APIs was driven by the growth of mobile applications, cloud computing, and microservices architecture. The development of tools and frameworks like Swagger (now OpenAPI), RAML, and API Blueprint facilitated the design, documentation, and testing of REST APIs.

By the 2020s modern developments evolved REST with technologies such as GraphQL. In addition, the OpenAPI specification (OAS), which evolved from Swagger, became a widely adopted standard for describing REST APIs, enabling better integration and automation.

### What is REST?

REST is a set of rules and conventions for interacting with web resources. The key components of URI, HTTP Methods, Headers, and Status Codes support the principles of REST.

#### The URI

REST APIs use URIs (Uniform Resource Identifiers) to access resources and is therefore a crucial element of a REST Architecture.  A URI is a string of characters that uniquely identifies a particular resource. URIs are used extensively on the internet to locate and interact with resources, such as web pages, files, and services.

A URI consists of several components, each serving a specific purpose. The generic URI syntax as defined in [RFC3986](https://tools.ietf.org/html/rfc3986) as below:

> URI = scheme "://" authority "/" path [ "?" query ] [ "#" fragment ]

For REST the **scheme**, is typically `http` or `https` but generically indicates the protocol or method used to access the resource. Common schemes include http, https, ftp, mailto, file, etc.

The **authority** ispecifies the domain name or IP address of the server where the resource resides, and may include a port number. It may also include userinfo as a subcomponent.

The **path** specifies the specific location of the resource on the server. We are interested in the path of URI as the relationship between user and resources. For example, `https://api.test.xyz/admin/testing/report`, this shows report of testing, there is relationship between user admin and their reports.

The path of any URI will define REST API resource model, resources are separated by a forward slash and based on Top-Down design.
For example:

- `https://api.test.xyz/admin/testing/report`
- `https://api.test.xyz/admin/testing/`
- `https://api.test.xyz/admin/`

The **query** provides additional parameters for the resource. It starts with a `?` and consists of key-value pairs separated by `&`.

The **fragment** indicates a specific part of the resource, such as a section within a web page. It starts with a #.

#### The HTTP Methods

REST APIs use standard HTTP methods to perform operations on resources following the [HTTP Request Methods](https://tools.ietf.org/html/rfc7231#section-4) defined in [RFC7231](https://tools.ietf.org/html/rfc7231). These methods map to CRUD, the four basic functions of persistent storage in computer science. CRUD stands for Create, Read, Update, and Delete, which are the four operations that can be performed on data.  

| Methods | Description                                   |
|---------|-----------------------------------------------|
| GET     | Get the representation of resource’s state    |
| POST    | Create a new resource                         |
| PUT     | Update a resource                             |
| DELETE  | Remove a resource                             |
| HEAD    | Get metadata associated with resource’s state |
| OPTIONS | List available methods                        |

#### The Headers

REST relies on headers to support communication of additional information within the request or response.

* Content-Type: Indicates the media type of the resource (e.g., application/json).
* Authorization: Contains credentials for authentication (e.g., tokens).
* Accept: Specifies the media types that are acceptable for the response.

#### The Status Codes

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
| 500           | Internal Server Error | Server failed to process request due to an internal error        

