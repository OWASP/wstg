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

~~~~
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
~~~~

The result will usually be very long, and it will contain the entire scheme of the GraphQL deployment.  

Response:  
```
{css, echo=FALSE}
.scroll-100 {
  max-height: 100px;
  overflow-y: auto;
  background-color: inherit;
}
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
        },
        {
          "kind": "OBJECT",
          "name": "__Field",
          "description": null,
          "fields": [
            {
              "name": "name",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "description",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "args",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "LIST",
                  "name": null,
                  "ofType": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "OBJECT",
                      "name": "__InputValue",
                      "ofType": null
                    }
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "type",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "OBJECT",
                  "name": "__Type",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "isDeprecated",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Boolean",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "deprecationReason",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "Query",
          "description": "",
          "fields": [
            {
              "name": "auth",
              "description": "Only used to simulate a external authentication service and have a way here to obtain a token",
              "args": [
                {
                  "name": "veterinaryName",
                  "description": "",
                  "type": {
                    "kind": "SCALAR",
                    "name": "String",
                    "ofType": null
                  },
                  "defaultValue": null
                }
              ],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "allDogs",
              "description": "Return a null object if no dog has been found",
              "args": [
                {
                  "name": "limit",
                  "description": "",
                  "type": {
                    "kind": "SCALAR",
                    "name": "Int",
                    "ofType": null
                  },
                  "defaultValue": "500"
                },
                {
                  "name": "onlyFree",
                  "description": "",
                  "type": {
                    "kind": "SCALAR",
                    "name": "Boolean",
                    "ofType": null
                  },
                  "defaultValue": "false"
                }
              ],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "Dog",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "dogs",
              "description": "Return a null object if no dog has been found",
              "args": [
                {
                  "name": "namePrefix",
                  "description": "",
                  "type": {
                    "kind": "SCALAR",
                    "name": "String",
                    "ofType": null
                  },
                  "defaultValue": null
                },
                {
                  "name": "limit",
                  "description": "",
                  "type": {
                    "kind": "SCALAR",
                    "name": "Int",
                    "ofType": null
                  },
                  "defaultValue": "500"
                }
              ],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "Dog",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "myDogs",
              "description": "Return a null object if the veterinary do not have any dog associated to him or if access is denied",
              "args": [
                {
                  "name": "veterinaryId",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "Int",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                },
                {
                  "name": "accessToken",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "String",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                }
              ],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "Dog",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "myInfo",
              "description": "Return a null object if the veterinary has not been found or if access is denied",
              "args": [
                {
                  "name": "veterinaryId",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "Int",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                },
                {
                  "name": "accessToken",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "String",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                }
              ],
              "type": {
                "kind": "OBJECT",
                "name": "Veterinary",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "__Schema",
          "description": "A GraphQL Introspection defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, the entry points for query, mutation, and subscription operations.",
          "fields": [
            {
              "name": "types",
              "description": "A list of all types supported by this server.",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "LIST",
                  "name": null,
                  "ofType": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "OBJECT",
                      "name": "__Type",
                      "ofType": null
                    }
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "queryType",
              "description": "The type that query operations will be rooted at.",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "OBJECT",
                  "name": "__Type",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "mutationType",
              "description": "If this server supports mutation, the type that mutation operations will be rooted at.",
              "args": [],
              "type": {
                "kind": "OBJECT",
                "name": "__Type",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "directives",
              "description": "'A list of all directives supported by this server.",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "LIST",
                  "name": null,
                  "ofType": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "OBJECT",
                      "name": "__Directive",
                      "ofType": null
                    }
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "subscriptionType",
              "description": "'If this server support subscription, the type that subscription operations will be rooted at.",
              "args": [],
              "type": {
                "kind": "OBJECT",
                "name": "__Type",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "__Type",
          "description": null,
          "fields": [
            {
              "name": "kind",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "ENUM",
                  "name": "__TypeKind",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "name",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "description",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "fields",
              "description": null,
              "args": [
                {
                  "name": "includeDeprecated",
                  "description": null,
                  "type": {
                    "kind": "SCALAR",
                    "name": "Boolean",
                    "ofType": null
                  },
                  "defaultValue": "false"
                }
              ],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "__Field",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "interfaces",
              "description": null,
              "args": [],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "__Type",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "possibleTypes",
              "description": null,
              "args": [],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "__Type",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "enumValues",
              "description": null,
              "args": [
                {
                  "name": "includeDeprecated",
                  "description": null,
                  "type": {
                    "kind": "SCALAR",
                    "name": "Boolean",
                    "ofType": null
                  },
                  "defaultValue": "false"
                }
              ],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "__EnumValue",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "inputFields",
              "description": null,
              "args": [],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "__InputValue",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "ofType",
              "description": null,
              "args": [],
              "type": {
                "kind": "OBJECT",
                "name": "__Type",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "__EnumValue",
          "description": null,
          "fields": [
            {
              "name": "name",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "description",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "isDeprecated",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Boolean",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "deprecationReason",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "ENUM",
          "name": "__DirectiveLocation",
          "description": "An enum describing valid locations where a directive can be placed",
          "fields": null,
          "inputFields": null,
          "interfaces": null,
          "enumValues": [
            {
              "name": "QUERY",
              "description": "Indicates the directive is valid on queries.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "MUTATION",
              "description": "Indicates the directive is valid on mutations.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "FIELD",
              "description": "Indicates the directive is valid on fields.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "FRAGMENT_DEFINITION",
              "description": "Indicates the directive is valid on fragment definitions.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "FRAGMENT_SPREAD",
              "description": "Indicates the directive is valid on fragment spreads.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INLINE_FRAGMENT",
              "description": "Indicates the directive is valid on inline fragments.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "SCHEMA",
              "description": "Indicates the directive is valid on a schema SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "SCALAR",
              "description": "Indicates the directive is valid on a scalar SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "OBJECT",
              "description": "Indicates the directive is valid on an object SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "FIELD_DEFINITION",
              "description": "Indicates the directive is valid on a field SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "ARGUMENT_DEFINITION",
              "description": "Indicates the directive is valid on a field argument SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INTERFACE",
              "description": "Indicates the directive is valid on an interface SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "UNION",
              "description": "Indicates the directive is valid on an union SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "ENUM",
              "description": "Indicates the directive is valid on an enum SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "ENUM_VALUE",
              "description": "Indicates the directive is valid on an enum value SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INPUT_OBJECT",
              "description": "Indicates the directive is valid on an input object SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INPUT_FIELD_DEFINITION",
              "description": "Indicates the directive is valid on an input object field SDL definition.",
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "possibleTypes": null
        },
        {
          "kind": "SCALAR",
          "name": "String",
          "description": "Built-in String",
          "fields": null,
          "inputFields": null,
          "interfaces": null,
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "SCALAR",
          "name": "Int",
          "description": "Built-in Int",
          "fields": null,
          "inputFields": null,
          "interfaces": null,
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "Mutation",
          "description": "",
          "fields": [
            {
              "name": "associateDogToMe",
              "description": "Return a null object if the dog/veterinary has not been found or if the dog is already associated to a Veterinary or if access is denied",
              "args": [
                {
                  "name": "dogId",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "Int",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                },
                {
                  "name": "veterinaryId",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "Int",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                },
                {
                  "name": "accessToken",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "String",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                }
              ],
              "type": {
                "kind": "OBJECT",
                "name": "Dog",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "disassociateDogFromMe",
              "description": "Return a null object if the dog/veterinary has not been found or if the dog is already disassociated from a Veterinary or if access is denied",
              "args": [
                {
                  "name": "dogId",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "Int",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                },
                {
                  "name": "veterinaryId",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "Int",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                },
                {
                  "name": "accessToken",
                  "description": "",
                  "type": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "SCALAR",
                      "name": "String",
                      "ofType": null
                    }
                  },
                  "defaultValue": null
                }
              ],
              "type": {
                "kind": "OBJECT",
                "name": "Dog",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "__InputValue",
          "description": null,
          "fields": [
            {
              "name": "name",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "description",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "type",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "OBJECT",
                  "name": "__Type",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "defaultValue",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "SCALAR",
          "name": "Boolean",
          "description": "Built-in Boolean",
          "fields": null,
          "inputFields": null,
          "interfaces": null,
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "Subscription",
          "description": "",
          "fields": [
            {
              "name": "newAssociation",
              "description": "Return the info about the new association when a Dog is associated to a Veterinary",
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "Veterinary",
          "description": "Represent a Veterinary",
          "fields": [
            {
              "name": "id",
              "description": "Unique identifier",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Int",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "name",
              "description": "Name Dr.xxx",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "popularity",
              "description": "Popularity (from 1 to 5)",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Int",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "dogs",
              "description": "List of dogs associated to this veterinary",
              "args": [],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "OBJECT",
                    "name": "Dog",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "Dog",
          "description": "Represent a Dog",
          "fields": [
            {
              "name": "id",
              "description": "Unique identifier",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Int",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "name",
              "description": "Friendly name",
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "String",
                  "ofType": null
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "veterinary",
              "description": "Veterinary in charge of him",
              "args": [],
              "type": {
                "kind": "OBJECT",
                "name": "Veterinary",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        },
        {
          "kind": "OBJECT",
          "name": "__Directive",
          "description": null,
          "fields": [
            {
              "name": "name",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "description",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "String",
                "ofType": null
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "locations",
              "description": null,
              "args": [],
              "type": {
                "kind": "LIST",
                "name": null,
                "ofType": {
                  "kind": "NON_NULL",
                  "name": null,
                  "ofType": {
                    "kind": "ENUM",
                    "name": "__DirectiveLocation",
                    "ofType": null
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "args",
              "description": null,
              "args": [],
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "LIST",
                  "name": null,
                  "ofType": {
                    "kind": "NON_NULL",
                    "name": null,
                    "ofType": {
                      "kind": "OBJECT",
                      "name": "__InputValue",
                      "ofType": null
                    }
                  }
                }
              },
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "onOperation",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "Boolean",
                "ofType": null
              },
              "isDeprecated": true,
              "deprecationReason": "Use `locations`."
            },
            {
              "name": "onFragment",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "Boolean",
                "ofType": null
              },
              "isDeprecated": true,
              "deprecationReason": "Use `locations`."
            },
            {
              "name": "onField",
              "description": null,
              "args": [],
              "type": {
                "kind": "SCALAR",
                "name": "Boolean",
                "ofType": null
              },
              "isDeprecated": true,
              "deprecationReason": "Use `locations`."
            }
          ],
          "inputFields": null,
          "interfaces": [],
          "enumValues": null,
          "possibleTypes": null
        }
      ],
      "directives": [
        {
          "name": "include",
          "description": "Directs the executor to include this field or fragment only when the `if` argument is true",
          "locations": [
            "FIELD",
            "FRAGMENT_SPREAD",
            "INLINE_FRAGMENT"
          ],
          "args": [
            {
              "name": "if",
              "description": "Included when true.",
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Boolean",
                  "ofType": null
                }
              },
              "defaultValue": null
            }
          ]
        },
        {
          "name": "skip",
          "description": "Directs the executor to skip this field or fragment when the `if`'argument is true.",
          "locations": [
            "FIELD",
            "FRAGMENT_SPREAD",
            "INLINE_FRAGMENT"
          ],
          "args": [
            {
              "name": "if",
              "description": "Skipped when true.",
              "type": {
                "kind": "NON_NULL",
                "name": null,
                "ofType": {
                  "kind": "SCALAR",
                  "name": "Boolean",
                  "ofType": null
                }
              },
              "defaultValue": null
            }
          ]
        },
        {
          "name": "defer",
          "description": "This directive allows results to be deferred during execution",
          "locations": [
            "FIELD"
          ],
          "args": []
        }
      ]
    }
  }
}
```

#### Using the GraphiQL

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
