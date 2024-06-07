# API Reconnaissance

|ID          |
|------------|
|WSTG-APIT-01|

## Summary

Reconnaissance is an important step in any pentesting engagement. This includes API pentesting. Reconnaissance significantly enhances the effectiveness of the testing process by gathering information about the API and developing an understanding of the target. This phase not only increases the likelihood of discovering critical security issues but also ensures a comprehensive evaluation of the API’s security posture.

## API Types

APIs can be public or private.

### Public APIs

Public APIs typically have their details published in a Swagger/OpenAI document. Gaining access to this document is important to understand the attack surface. Equally important is finding older versions of this document that might show depricated but still functional code that may have security vulnerabilities.

Keep in mind that this document, however well intentioned, may not be accurate, and also may not dislose the complete API.

Public APIs may also be documented on shared libraries or directories of APIs.

### Private APIs

The visibility of private APIs depends on who the intended consumer is. An API can be private, but only accessible to subscribed clients (also known as `partners`) or only accessible to internal clients, such as other departments within the same company. Finding private APIs using reconnaissance techniques is also important. These APIs can be discovered using a number of techniques which we will discuss below.

## Find the Documentation

In both public and private cases, the API documentation will be useful based on its level of the quality and accurracy. Public API documentaton is typically shared with everyone whereas private API documentation is only shared with the intended client. However, in both cases finding documentation, accidentally leaked or otherwise will be helpfull in your investigation.

Regardless of the visibility of the API, searching for API documentation can find older, not-yet-published, or accidentally leaked API documentation. This documentation will be very helpfull in understanding the how the attack surface the API exposes.

If documentation is not readily apparent, then you can actively search the target for documentation based on a few obvious names or paths. These include:

- /api-docs
- /doc
- /swagger
- /swagger.json
- /openapi.json
- /.well-known/schema-discovery

If the application uses GitHub we can also search any of their repositories (also known as `GitDorking`), or the personal GitHub accounts of the target's employees.

Alternatives sources of API documentation can incluide API Directories:

- GitHub in general and
- [GitHub Public APIs Repository](https://github.com/public-apis/public-apis)
- [APIs.guru](apis.guru)
- [RapidAPI](https://rapidapi.com/)
- [PublicAPIs](https://publicapis.dev/) and [PublicAPIs](https://publicapis.io/)
- [Postman API Network](https://www.postman.com/explore)

## Browsing the Application

Even if you have the API documentation browsing the application is a good idea. Documentation can be outdated, inaccurate, or be incomplete.

Browsing the application with an intercepting proxy such as ZAP or Burp Suite records endpoints for later inspection. In addition, using their built-in spidering functionality can help generate a comprehensive list of endpoints. In the spidered urls look for links with obvious API URL naming schemes. These include:

- <https://example.com/api/v1> (or v2 etc)
- <https://example.com/graphql>

Or subdomains the the applications my consume:

- api.example.com/api/v1

It is important the the pentester attempts to exercise as much functionality in the application as possible. This is not only to have a comprehensive view of the endpoints but also to avoid issues with lazy loadingand code splitting.

Once completed, the endpoint information obtained from comprehensive browsing and spidering of the application can help the pentester compose API documentation of the target using other tools such as Postman.

## Dork the Google

Using passive reconnaissance techniques such as Google Dorking with parameters such as `site` and `inurl`allows us to tailor a search for common API keywords that the google indexer may have found.

For example:
> site:"mytargetsite.com" inurl:"/api"

Other keywords can include "v1", "api", "graphql".

We can extend the Google Dorking to include subdomains of the target.

Wordlists are helpfull here for a comprehensive list of common words used in APIs.

## Look Back, Way Back

Published and private APIs change over time. But deprecated or older version may still be operational either on purpose or by misconfiguration. These should also be tested as there is a good chance that they will contain vulnerabilities that newer versions have fixed. In addition, changes to APIs show newer features which may be lest robust and therefore a good candidate for testing.

To discover older version we can use the `Way back machine` to help find older endpoints. Tools like TomNomNom's [WayBackUrls](https://github.com/tomnomnom/waybackurls) that fetches all the URLs that the Wayback Machine knows about for a domain can be helpful.

## The Client Side Application

An excellent source of API and other information is the HTML and JavaScript that the server sends to the client. Sometimes, the client application leaks sensitive information including APIs and secrets.

There are a variety of tools that we can use to help us extract sensitive information from JavaScript transmitted to the browser. These tools typically are based on one of two approachs, Regex or AbstractSyntaxTrees (AST). And then there are generalized tools that help us organizer or manage JS files for investigation by AST and Regex tools.

Rexex is more straightforward by searching JS or HTML content for known patterns. However, this approach can miss content not explicitly identified in the regex. Given the structure of some JS this approach can miss a lot. ASTs on the other hand are tree-like structures that represent the syntax of source code. Each node in the tree corresponds to a part of the code. For JavaScript, an AST breaks the code into basic components, allowing tools and compilers to understand and modify the code easily.

### General Tools

1. [Uproot](https://github.com/0xDexter0us/uproot-JS). A BurpSuite plugin that saves any encountered JS files to disk. This helps extract the files for any analysis by command line tools.
2. [OpenAPI Support](https://www.zaproxy.org/docs/desktop/addons/openapi-support/). This ZAP add-on allows you to spider and import OpenAPI (Swagger) definitions, versions 1.2, 2.0, and 3.0.
3. [OpenAPI Parser](https://github.com/aress31/openapi-parser). A BurpSuite plugin that parses OpenAPI documents into Burp Suite for automating OpenAPI-based APIs security assessments.

### Regex Tools

1. [JSParser](https://github.com/nahamsec/JSParser). A python 2.7 script using Tornado and JSBeautifier to parse relative URLs from JavaScript files.
2. [JSMiner](https://github.com/PortSwigger/js-miner). A BurpSuite plugin tries to find interesting stuff inside static files; mainly JavaScript and JSON files. This tool scans "passively" while crawling the application.
3. [JSpector](https://github.com/hisxo/JSpector). A BurpSuite plugin that passively crawls JavaScript files and automatically creates issues with URLs, endpoints and dangerous methods found on the JS files.

### AST Tools

1. [JSLuice](https://github.com/BishopFox/jsluice).  A command line tool that extracts URLs, paths, secrets, and other interesting data from JavaScript source code.

### Other Recon Tools

1. [Attack Surface Detector](https://github.com/secdec/attack-surface-detector-burp). A BurpSuite plugin that uses static code analyses to identify web app endpoints by parsing routes and identifying parameters.
2. [Param Miner](https://github.com/portswigger/param-miner). A BurpSuite plug-in that identifies hidden, unlinked parameters.

## Active Fuzzing

Active Fuzzing involves using tools with wordlists and filtering requests results to bruteforce endpoint discovery.

### Kiterunner

### FFUF
