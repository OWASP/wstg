# Testing for SSI Injection

|ID          |
|------------|
|WSTG-INPV-08|

## Summary

Web servers usually give developers the ability to add small pieces of dynamic code inside static HTML pages, without having to deal with full-fledged server-side or client-side languages. This feature is provided by [Server-Side Includes](https://owasp.org/www-community/attacks/Server-Side_Includes_(SSI)_Injection)(SSI).

Server-Side Includes are directives that the web server parses before serving the page to the user. They represent an alternative to writing CGI programs or embedding code using server-side scripting languages, when there's only need to perform very simple tasks. Common SSI implementations provide directives(commands) to include external files, to set and print web server CGI environment variables, and to execute external CGI scripts or system commands.

SSI can lead to a Remote Command Execution (RCE), however most webservers have the `exec` directive disabled by default.

This is a vulnerability very similar to a classical scripting language injection vulnerability. One mitigation is that the web server needs to be configured to allow SSI. On the other hand, SSI injection vulnerabilities are often simpler to exploit, since SSI directives are easy to understand and, at the same time, quite powerful, e.g., they can output the content of files and execute system commands.

## Test Objectives

- Identify SSI injection points.
- Assess the severity of the injection.

## How to Test

When testing for SSI we are injecting SSI directives as user input and if SSI are enabled and there is no user input validation the server will execute the directive. This is very similar to a classical scripting language injection vulnerability, it occurs when user input is not properly validated and sanitized.

The first thing to do when testing is finding if the web server actually supports SSI directives. Often, the answer is yes, as SSI support is quite common. To find out we just need to discover which kind of web server is running on our target, using classic information gathering techniques. If we have access to the code we can check if SSI directives are used in it or grep trough the webserver configuration files for specific keywords.

Another way of verifying that SSI are enabled, is checking for pages with the `.shtml` extension, since it is associated with SSI directives. Unfortunately, the use of the `.shtml` extension is not mandatory, so not having found any `.shtml` files doesn't necessarily mean that the target is not prone to SSI injection attacks.

The next step is determining all the possible user input vectors and testing if the SSI Injection is exploitable.

To test this we have to find all the pages where user input is allowed. Possible input vectors may also include Headers and Cookies. Determine how the input is stored and used, i.e if the input is returned as an error message or page element and if it was modified in some way. If we have access to the source code we can easily determine where the input vectors are and how input is handled.

Once we have a list of potential injection points, we can check if the input is correctly validated. We need to make sure that we can inject characters used in SSI directives:

`< ! # = / . " - > and [a-zA-Z0-9]`

Testing if the SSI Injection is exploitable is very simillar to testing for XSS using

`<script>alert("XSS")</script>`

For SSI Injection we can use the directives listed below.

`<!--#echo var="VAR" -->`

Returns the value of the variable. [List of SSI include variables](https://httpd.apache.org/docs/current/howto/ssi.html)

`<!--#include virtual="FILENAME" -->`

If the supplied file is a CGI script the directive will include the output of the CGI script. But the directive may also be used to include the content of a file or list files in a directory.

`<!--#exec cmd="OS_COMMAND" -->`

Returns the output of the supplied command.

There are more directives and variables which you can find [here](https://httpd.apache.org/docs/current/howto/ssi.html)

If the application is vulnerable, the directive is injected and it would be interpreted by the server the next time the page is served, thus including the content of the Unix standard password file.

The malicious data can also be injected in the HTTP headers, if the web application is using that data to build a dynamically generated page:

```txt
GET / HTTP/1.0
Referer: <!--#exec cmd="/bin/ps ax"-->
User-Agent: <!--#include virtual="/proc/version"-->
```

## Tools

- [Web Proxy Burp Suite](https://portswigger.net)
- [OWASP ZAP](https://www.zaproxy.org/)
- [String searcher: grep](https://www.gnu.org/software/grep)

## References

- [Nginx SSI module](http://nginx.org/en/docs/http/ngx_http_ssi_module.html)
- [Apache: “Module mod_include”](https://httpd.apache.org/docs/1.3/mod/mod_include.html)
- [SSI Include Variables Cheatsheet](http://www.cheat-sheets.org/sites/ssi.su/#includeVariables)

### Whitepapers

- [Apache Tutorial: “Introduction to Server Side Includes”](https://httpd.apache.org/docs/1.3/howto/ssi.html)
- [Apache: “Security Tips for Server Configuration”](https://httpd.apache.org/docs/1.3/misc/security_tips.html#ssi)
- [Header Based Exploitation](https://www.cgisecurity.com/papers/header-based-exploitation.txt)
- [SSI Injection instead of JavaScript Malware](https://jeremiahgrossman.blogspot.com/2006/08/ssi-injection-instead-of-javascript.html)
- [IIS: “Notes on Server-Side Includes (SSI) syntax”](https://blogs.iis.net/robert_mcmurray/archive/2010/12/28/iis-notes-on-server-side-includes-ssi-syntax-kb-203064-revisited.aspx)
