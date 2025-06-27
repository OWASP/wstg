# API Reconnaissance

|ID          |
|------------|
|WSTG-APIT-01|

## Summary

Reconnaissance is an important step in any pentesting engagement. This includes API pentesting. Reconnaissance significantly enhances the effectiveness of the testing process by gathering information about the API and developing an understanding of the target. This phase not only increases the likelihood of discovering critical security issues but also ensures a comprehensive evaluation of the APIs' security posture.

This guide has a section on [Information Gathering](../01-Information_Gathering/README.md) which can apply when auditing APIs. However, there are some differences. As security researchers, we often focus on specific areas and searching this guide for the sections that apply can be time consuming. To ensure the researcher has a single location to focus on APIs this section concentrates on those items that apply to APIs and provides references to supporting content elsewhere in the guide.

### API Types

APIs can be public or private.

#### Public APIs

Public APIs typically have their details published in a Swagger/OpenAPI document. Gaining access to this document is important to understand the attack surface. Equally important is finding older versions of this document that might show depricated but still functional code that may have security vulnerabilities.

Keep in mind that this document, however well intentioned, may not be accurate, and also may not dislose the complete API.

Public APIs may also be documented on shared libraries or directories of APIs.

#### Private APIs

The visibility of private APIs depends on who the intended consumer is. An API can be private, but only accessible to subscribed clients (also known as `partners`) or only accessible to internal clients, such as other departments within the same company. Finding private APIs using reconnaissance techniques is also important. These APIs can be discovered using a number of techniques which we will discuss below.

## Test Objectives

- Find all API endpoints supported by the backend server code, documented or undocumented.
- Find all parameters for each endpoint supported by the backend server, documented or undocumented.
- Discover interesting data related to APIs in HTML and JavaScript sent to clients.

## How to Test

### Find the Documentation

In both public and private cases, the API documentation will be useful based on its level of the quality and accurracy. Public API documentaton is typically shared with everyone whereas private API documentation is only shared with the intended client. However, in both cases finding documentation, accidentally leaked or otherwise will be helpfull in your investigation.

Regardless of the visibility of the API, searching for API documentation can find older, not-yet-published, or accidentally leaked API documentation. This documentation will be very helpfull in understanding what the attack surface the API exposes.

### API Directories

Alternatives sources of API documentation can incluide API Directories, such as:

- GitHub in general
- [GitHub Public APIs Repository](https://github.com/public-apis/public-apis)
- [APIs.guru](https://apis.guru)
- [RapidAPI](https://rapidapi.com/)
- [PublicAPIs](https://publicapis.dev/) and [PublicAPIs](https://publicapis.io/)
- [Postman API Network](https://www.postman.com/explore)

### Looking in Well Known Places

If documentation is not readily apparent, then you can actively search the target for documentation based on a few obvious names or paths. These include:

- /api-docs
- /doc
- /swagger
- /swagger.json
- /openapi.json
- /.well-known/schema-discovery

### Robots.txt

`robots.txt` is a text file that site owners create to instruct web crawlers (such as search engine bots) on how to crawl and index their site. It is part of the Robots Exclusion Protocol (REP), which regulates how bots interact with sites.

This file may provide additional clues to path structure or API endpoints.

The [Information Gathering](../01-Information_Gathering/README.md) section refers to robots.txt in several cases including WSTG-INFO-01, WSTG-INFO-03, WSTG-INFO-05, and WSTG-INFO-08.

### GitDorking

If the application uses GitHub, GitLab, or other public facing Git based repositories then we can also search for any clues or sensitive content (also known as `GitDorking`). This information can include passwords, API keys, configuration files, and other confidential data that developers may accidentally or inadvertently commit to their repositories. Organizations can accidentally share sensitive code, sample, or test code that may provide clues to implementation details. The personal GitHub accounts of the target's employees may also accidentally release information that can provide clues.

### Browsing and Spidering the Application

Even if you have the API documentation browsing the application is a good idea. Documentation can be outdated, inaccurate, or incomplete.

Browsing the application with an intercepting proxy such as ZAP or Burp Suite records endpoints for later inspection. In addition, using their built-in spidering functionality, intercepting proxies can help generate a comprehensive list of endpoints. From the spidered URLs look for links with obvious API URL naming schemes. These include:

- `https://example.com/api/v1` (or v2 etc)
- `https://example.com/graphql`

Or subdomains the the applications may consume or depend upon:

- `https://api.example.com/api/v1`

It is important that the pentester attempts to exercise as much functionality in the application as possible. This is not only to generate a comprehensive list of endpoints but also to avoid issues with lazy loading and code splitting. In addition, your pentest engagement should include sample accounts at different privilege levels so that your browser and spidering can access and expose endpoints for as much functionality as possible.

Once completed, the endpoint information obtained from browsing and spidering of the application can help the pentester compose API documentation of the target using other tools such as Postman.

### Google Dorking

Using passive reconnaissance techniques such as Google Dorking with directives such as `site` and `inurl` allows us to tailor a search for common API keywords that the Google indexer may have found. Review [Conduct Search Engine Discovery Reconnaissance for Information Leakage](../01-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage.md) for additional information.

Here are a few API specific examples:

`site:"mytargetsite.com" inurl:"/api"`

`inurl:apikey filetype:env`

Other keywords can include `"v1"`, `"api"`, `"graphql"`.

We can extend the Google Dorking to include subdomains of the target.

Wordlists are helpful here for a comprehensive list of common words used in APIs.

### Look Back, Way Back

In general APIs change over time. But deprecated or older version may still be operational either on purpose or by misconfiguration. These should also be tested as there is a good chance that they will contain vulnerabilities that newer versions have fixed. In addition, changes to APIs show newer features which may be less robust and therefore a good candidate for testing.

To discover older versions we can use the `Wayback machine` to help find older endpoints. A helpful tool know as TomNomNom's [WayBackUrls](https://github.com/tomnomnom/waybackurls) fetches all the URLs that the Wayback Machine knows about for a domain.

- [WayBackUrls](https://github.com/tomnomnom/waybackurls). Fetch all the URLs that the Wayback Machine knows about for a domain.
- [waymore](https://github.com/xnl-h4ck3r/waymore). Find way more from the Wayback Machine, Common Crawl, Alien Vault OTX, URLScan & VirusTotal.
- [gau](https://github.com/lc/gau). Fetch known URLs from AlienVault's Open Threat Exchange, the Wayback Machine, and Common Crawl.

### The Client-Side Application

An excellent source of API and other information is the HTML and JavaScript that the server sends to the client. Sometimes, the client application leaks sensitive information including APIs and secrets. The [Review Web Page Content for Information Leakage](../01-Information_Gathering/05-Review_Web_Page_Content_for_Information_Leakage.md) section has some general information for reviewing web content for leakage. Here we will expand to focus on reviewing the JavaScript content for API related secrets.

There are a variety of tools that we can use to help us extract sensitive information from JavaScript transmitted to the browser. These tools are typically based on one of two approaches: Regular Expressions or Abstract Syntax Trees (AST). Then there are generalized tools that help us organize or manage JS files for investigation by AST and Regular Expression tools.

Regex is more straightforward by searching JS or HTML content for known patterns. However, this approach can miss content not explicitly identified in the Regular Expression. Given the structure of some JS this approach can miss a lot. ASTs on the other hand are tree-like structures that represent the syntax of source code. Each node in the tree corresponds to a part of the code. For JavaScript, an AST breaks the code into basic components, allowing tools and compilers to understand and modify the code easily.

#### General Tools

1. [Uproot](https://github.com/0xDexter0us/uproot-JS). A BurpSuite plugin that saves any encountered JS files to disk. This helps extract the files for any analysis by command-line tools.
2. [OpenAPI Support](https://www.zaproxy.org/docs/desktop/addons/openapi-support/). This ZAP add-on allows you to spider and import OpenAPI (Swagger) definitions, versions 1.2, 2.0, and 3.0.
3. [OpenAPI Parser](https://github.com/aress31/openapi-parser). A BurpSuite plugin that parses OpenAPI documents into Burp Suite for automating OpenAPI-based APIs security assessments.

#### Regular Expression Tools

1. [JSParser](https://github.com/nahamsec/JSParser). A python 2.7 script using Tornado and JSBeautifier to parse relative URLs from JavaScript files.
2. [JSMiner](https://github.com/PortSwigger/js-miner). A BurpSuite plugin tries to find interesting stuff inside static files; mainly JavaScript and JSON files. This tool scans "passively" while crawling the application.
3. [JSpector](https://github.com/hisxo/JSpector). A BurpSuite plugin that passively crawls JavaScript files and automatically creates issues with URLs, endpoints and dangerous methods found on the JS files.
4. [Link Finder](https://github.com/GerbenJavado/LinkFinder). A python script that finds endpoints in JavaScript files.

#### AST Tools

1. [JSLuice](https://github.com/BishopFox/jsluice). A command-line tool that extracts URLs, paths, secrets, and other interesting data from JavaScript source code.

### Other Recon Tools

1. [Attack Surface Detector](https://github.com/secdec/attack-surface-detector-burp). A BurpSuite plugin that uses static code analyses to identify web app endpoints by parsing routes and identifying parameters.
2. [Param Miner](https://github.com/portswigger/param-miner). A BurpSuite plugin that identifies hidden, unlinked parameters.
3. [xnLinkFinder](https://github.com/xnl-h4ck3r/xnLinkFinder). A python tool used to discover endpoints, potential parameters, and a target specific wordlist for a given target.
4. [GAP](https://github.com/xnl-h4ck3r/GAP-Burp-Extension). Burp Extension to find potential endpoints, parameters, and generate a custom target wordlist.

### Active Fuzzing

Active Fuzzing involves using tools with wordlists and filtering requests results to bruteforce endpoint discovery.

#### Kiterunner

[KiteRunner](https://github.com/assetnote/kiterunner) is a tool that performs traditional content discovery and bruteforcing routes/endpoints in modern applications and APIs.

```console
kr [scan|brute] <input> [flags]
```

To scan a target for APIs using a wordlist we can:

```console
kr scan https://example.com/api -w /usr/share/wordlists/apis/routes-large.kite --fail-status-codes 404,403
```

#### FFUF/DirBuster/GoBuster

All three of FFUF, DirBuster, and GoBuster are designed to discover hidden paths and files on web servers through brute-forcing techniques. All three use customizable wordlists to generate requests to the target web server, attempting to identify valid directories and files. All three support multi-threaded or highly efficient processing to speed up the brute-forcing process.

Some common wordlist files for APIs include: [SecLists](https://github.com/danielmiessler/SecLists) in the Discovery/Web-Content/api section, [GraphQL Wordlist](https://github.com/Escape-Technologies/graphql-wordlist), and [Assetnote](https://wordlists.assetnote.io/).

GoBuster Example:

`gobuster dir -u <target url> -w <wordlist file>`

## References

### OWASP Resources

- [REST Assessment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Assessment_Cheat_Sheet.html)

### Books

- Corey J. Ball - "Hacking APIs : breaking web application programming interfaces", No Starch, 2022 - ISBN-13: 978-1-7185-0244-4
- Confidence Staveley - "API Security for White Hat Hackers, Packt, 2024 - ISBN 978-1-80056-080-2  
