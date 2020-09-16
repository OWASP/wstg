# Testing GraphQL

|ID          |
|------------|
|WSTG-API-01|

## Summary

GraphQL has become very pouplar in modern APIs. It provides simplicty, and nested objects, which allows developers for faster development.  
Every techonolgy, while having advantages can also expose the application to new attack srufaces.
The purpose of this guide is to provide some common misconfigurations and attack vectors on applications which utilize GraphQL.  
Some vectors are unique to GraphQL (Introspection Query for example) and some are not (SQL Injection for example).

The guide will use a demo vulnerable application which uses GraphQL for the API access in order to demonstrate vulnerable a GraphQL node.

The guide will be based on a vulnerable GraphQL application [poc-graphql](https://github.com/righettod/poc-graphql), which is run in a docker container which maps localhost:8080/graphql as the vulnerable GraphQL node.

## Test Objectives

Assess GraphQL's security configuration, as well as other common vulnerabilities which might affect GraphQL deployments.

## How to Test

Testing GraphQL nodes is not very different than testing other API technologies. This Guide suggests following these steps:

### Introspection Queries

A little bit of background:  
Introspection queries are the way GraphQL lets you ask it what queries it supports. This is a good starting point on the information garthering phase.

There are a couple of ways to extract that and visualise the output:

#### Using Native GrapQL Introspection

The most straight-forward way is to send an HTTP request with the following payload :

`query IntrospectionQuery {       __schema {         queryType { name }         mutationType { name }         subscriptionType { name }         types {           ...FullType         }         directives {           name           description           locations           args {             ...InputValue           }         }       }     }      fragment FullType on __Type {       kind       name       description       fields(includeDeprecated: true) {         name         description         args {           ...InputValue         }         type {           ...TypeRef         }         isDeprecated         deprecationReason       }       inputFields {         ...InputValue       }       interfaces {         ...TypeRef       }       enumValues(includeDeprecated: true) {         name         description         isDeprecated         deprecationReason       }       possibleTypes {         ...TypeRef       }     }      fragment InputValue on __InputValue {       name       description       type { ...TypeRef }       defaultValue     }      fragment TypeRef on __Type {       kind       name       ofType {         kind         name         ofType {           kind           name           ofType {             kind             name             ofType {               kind               name               ofType {                 kind                 name                 ofType {                   kind                   name                   ofType {                     kind                     name                   }                 }               }             }           }         }       }     } `

The result will usually b

#### Using the GraphiQL documentation pane

#### Using GraphQL Playgrounds

## Remediation

Do not make a habit of putting cats in boxes. Keep boxes away from cats as much as possible.

## Tools

* [GraphQL Playground](https://github.com/prisma-labs/graphql-playground)

### Burp GraphQL Extensions

* [InQL](https://portswigger.net/bappstore/296e9a0730384be4b2fffef7b4e19b1f)
* [GraphQL Raider](https://portswigger.net/bappstore/4841f0d78a554ca381c65b26d48207e6)

### Zap Proxy Extensions

* [GraphQL addon for (OWASP) ZAP](https://www.zaproxy.org/blog/2020-08-28-introducing-the-graphql-add-on-for-zap/)

## References

* [poc-graphql](https://github.com/righettod/poc-graphql)
* [GraphQL Offical Site](https://graphql.org/learn/)
