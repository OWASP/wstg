# Identify Application Entry Points

|ID          |
|------------|
|WSTG-INFO-06|

## Summary

Enumerating the application and its attack surface is a key precursor before any thorough testing can be undertaken, as it allows the tester to identify likely areas of weakness. This section aims to help identify and map out areas within the application that should be investigated once enumeration and mapping have been completed.

## Test Objectives

- Identify possible entry and injection points through request and response analysis.

## How to Test

Before any testing begins, the tester should always get a good understanding of the application and how the user and browser communicates with it. As the tester walks through the application, they should pay attention to all HTTP requests as well as every parameter and form field that is passed to the application. They should pay special attention to when GET requests are used and when POST requests are used to pass parameters to the application. In addition, they also need to pay attention to when other methods for RESTful services are used.

Note that in order to see the parameters sent in the body of requests such as a POST request, the tester may want to use a tool such as an intercepting proxy (See [tools](#tools)). Within the POST request, the tester should also make special note of any hidden form fields that are being passed to the application, as these usually contain sensitive information, such as state information, quantity of items, the price of items, that the developer never intended for anyone to see or change.

In the author's experience, it has been very useful to use an intercepting proxy and a spreadsheet for this stage of testing. The proxy will keep track of every request and response between the tester and the application as they explore it. Additionally, at this point, testers usually trap every request and response so that they can see exactly every header, parameter, etc. that is being passed to the application and what is being returned. This can be quite tedious at times, especially on large interactive sites (think of a banking application). However, experience will show what to look for and this phase can be significantly reduced.

As the tester walks through the application, they should take note of any interesting parameters in the URL, custom headers, or body of the requests/responses, and save them in a spreadsheet. The spreadsheet should include the page requested (it might be good to also add the request number from the proxy, for future reference), the interesting parameters, the type of request (GET, POST, etc), if access is authenticated/unauthenticated, if TLS is used, if it's part of a multi-step process, if WebSockets are used, and any other relevant notes. Once they have every area of the application mapped out, then they can go through the application and test each of the areas that they have identified and make notes for what worked and what didn't work. The rest of this guide will identify how to test each of these areas of interest, but this section must be undertaken before any of the actual testing can commence.

Below are some points of interests for all requests and responses. Within the requests section, focus on the GET and POST methods, as these appear the majority of the requests. Note that other methods, such as PUT and DELETE, can be used. Often, these more rare requests, if allowed, can expose vulnerabilities. There is a special section in this guide dedicated for testing these HTTP methods.

### Requests

- Identify where GETs are used and where POSTs are used.
- Identify all parameters used in a POST request (these are in the body of the request).
- Within the POST request, pay special attention to any hidden parameters. When a POST is sent all the form fields (including hidden parameters) will be sent in the body of the HTTP message to the application. These typically aren't seen unless a proxy or view the HTML source code is used. In addition, the next page shown, its data, and the level of access can all be different depending on the value of the hidden parameter(s).
- Identify all parameters used in a GET request (i.e., URL), in particular the query string (usually after a ? mark).
- Identify all the parameters of the query string. These usually are in a pair format, such as `foo=bar`. Also note that many parameters can be in one query string such as separated by a `&`, `\~`, `:`, or any other special character or encoding.
- A special note when it comes to identifying multiple parameters in one string or within a POST request is that some or all of the parameters will be needed to execute the attacks. The tester needs to identify all of the parameters (even if encoded or encrypted) and identify which ones are processed by the application. Later sections of the guide will identify how to test these parameters. At this point, just make sure each one of them is identified.
- Also pay attention to any additional or custom type headers not typically seen (such as `debug: false`).

### Responses

- Identify where new cookies are set (`Set-Cookie` header), modified, or added to.
- Identify where there are any redirects (3xx HTTP status code), 400 status codes, in particular 403 Forbidden, and 500 internal server errors during normal responses (i.e., unmodified requests).
- Also note where any interesting headers are used. For example, `Server: BIG-IP` indicates that the site is load balanced. Thus, if a site is load balanced and one server is incorrectly configured, then the tester might have to make multiple requests to access the vulnerable server, depending on the type of load balancing used.

### OWASP Attack Surface Detector

The Attack Surface Detector (ASD) tool investigates the source code and uncovers the endpoints of a web application, the parameters these endpoints accept, and the data type of those parameters. This includes the unlinked endpoints a spider will not be able to find, or optional parameters totally unused in client-side code. It also has the capability to calculate the changes in attack surface between two versions of an application.

The Attack Surface Detector is available as a plugin to both ZAP and Burp Suite, and a command-line tool is also available. The command-line tool exports the attack surface as a JSON output, which can then be used by the ZAP and Burp Suite plugin. This is helpful for cases where the source code is not provided to the penetration tester directly. For example, the penetration tester can get the json output file from a customer who does not want to provide the source code itself.

#### How to Use

The CLI jar file is available for download from [https://github.com/secdec/attack-surface-detector-cli/releases](https://github.com/secdec/attack-surface-detector-cli/releases).

You can run the following command for ASD to identify endpoints from the source code of the target web application.

`java -jar attack-surface-detector-cli-1.3.5.jar <source-code-path> [flags]`

Here is an example of running the command against [OWASP RailsGoat](https://github.com/OWASP/railsgoat).

```text
$ java -jar attack-surface-detector-cli-1.3.5.jar railsgoat/
Beginning endpoint detection for '<...>/railsgoat' with 1 framework types
Using framework=RAILS
[0] GET: /login (0 variants): PARAMETERS={url=name=url, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/sessions_contro
ller.rb (lines '6'-'9')
[1] GET: /logout (0 variants): PARAMETERS={}; FILE=/app/controllers/sessions_controller.rb (lines '33'-'37')
[2] POST: /forgot_password (0 variants): PARAMETERS={email=name=email, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/
password_resets_controller.rb (lines '29'-'38')
[3] GET: /password_resets (0 variants): PARAMETERS={token=name=token, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/p
assword_resets_controller.rb (lines '19'-'27')
[4] POST: /password_resets (0 variants): PARAMETERS={password=name=password, paramType=QUERY_STRING, dataType=STRING, user=name=user, paramType=QUERY_STRING, dataType=STRING, confirm_password=name=confirm_password, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/password_resets_controller.rb (lines '5'-'17')
[5] GET: /sessions/new (0 variants): PARAMETERS={url=name=url, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/sessions_controller.rb (lines '6'-'9')
[6] POST: /sessions (0 variants): PARAMETERS={password=name=password, paramType=QUERY_STRING, dataType=STRING, user_id=name=user_id, paramType=SESSION, dataType=STRING, remember_me=name=remember_me, paramType=QUERY_STRING, dataType=STRING, url=name=url, paramType=QUERY_STRING, dataType=STRING, email=name=email, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/sessions_controller.rb (lines '11'-'31')
[7] DELETE: /sessions/{id} (0 variants): PARAMETERS={}; FILE=/app/controllers/sessions_controller.rb (lines '33'-'37')
[8] GET: /users (0 variants): PARAMETERS={}; FILE=/app/controllers/api/v1/users_controller.rb (lines '9'-'11')
[9] GET: /users/{id} (0 variants): PARAMETERS={}; FILE=/app/controllers/api/v1/users_controller.rb (lines '13'-'15')
... snipped ...
[38] GET: /api/v1/mobile/{id} (0 variants): PARAMETERS={id=name=id, paramType=QUERY_STRING, dataType=STRING, class=name=class, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/api/v1/mobile_controller.rb (lines '8'-'13')
[39] GET: / (0 variants): PARAMETERS={url=name=url, paramType=QUERY_STRING, dataType=STRING}; FILE=/app/controllers/sessions_controller.rb (lines '6'-'9')
Generated 40 distinct endpoints with 0 variants for a total of 40 endpoints
Successfully validated serialization for these endpoints
0 endpoints were missing code start line
0 endpoints were missing code end line
0 endpoints had the same code start and end line
Generated 36 distinct parameters
Generated 36 total parameters
- 36/36 have their data type
- 0/36 have a list of accepted values
- 36/36 have their parameter type
--- QUERY_STRING: 35
--- SESSION: 1
Finished endpoint detection for '<...>/railsgoat'
----------
-- DONE --
0 projects had duplicate endpoints
Generated 40 distinct endpoints
Generated 40 total endpoints
Generated 36 distinct parameters
Generated 36 total parameters
1/1 projects had endpoints generated
To enable logging include the -debug argument
```

You can also generate a JSON output file using the `-json` flag, which can be used by the plugin to both ZAP and Burp Suite. See the following links for more details.

- [Home of ASD Plugin for OWASP ZAP](https://github.com/secdec/attack-surface-detector-zap/wiki)
- [Home of ASD Plugin for PortSwigger Burp](https://github.com/secdec/attack-surface-detector-burp/wiki)

### Testing for Application Entry Points

The following are two examples on how to check for application entry points.

#### Example 1

This example shows a GET request that would purchase an item from an online shopping application.

```http
GET /shoppingApp/buyme.asp?CUSTOMERID=100&ITEM=z101a&PRICE=62.50&IP=x.x.x.x HTTP/1.1
Host: x.x.x.x
Cookie: SESSIONID=Z29vZCBqb2IgcGFkYXdhIG15IHVzZXJuYW1lIGlzIGZvbyBhbmQgcGFzc3dvcmQgaXMgYmFy
```

> All the parameters of the request such as CUSTOMERID, ITEM, PRICE, IP, and the Cookie, which could just be encoded parameters or parameters used for session state.

#### Example 2

This example shows a POST request that would log you into an application.

```http
POST /example/authenticate.asp?service=login HTTP/1.1
Host: x.x.x.x
Cookie: SESSIONID=dGhpcyBpcyBhIGJhZCBhcHAgdGhhdCBzZXRzIHByZWRpY3RhYmxlIGNvb2tpZXMgYW5kIG1pbmUgaXMgMTIzNA==;CustomCookie=00my00trusted00ip00is00x.x.x.x00

user=admin&pass=pass123&debug=true&fromtrustIP=true
```

It can be noted that the parameters are sent in several locations:

1. In the query string: `service`
2. In the Cookie header: `SESSIONID`, `CustomCookie`
3. In the request body: `user`, `pass`, `debug`, `fromtrustIP`

Having a variety of injection locations provide the attacker with chaining possibilities that could improve the chances of finding a bug in the handling code.

## Tools

- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org/)
- [Burp Suite](https://www.portswigger.net/burp/)
- [Fiddler](https://www.telerik.com/fiddler)

## References

- [RFC 2616 – Hypertext Transfer Protocol – HTTP 1.1](https://tools.ietf.org/html/rfc2616)
- [OWASP Attack Surface Detector](https://owasp.org/www-project-attack-surface-detector/)
