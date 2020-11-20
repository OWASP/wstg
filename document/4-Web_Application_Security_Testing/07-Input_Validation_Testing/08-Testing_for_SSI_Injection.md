# Testing for SSI Injection

|ID          |
|------------|
|WSTG-INPV-08|

## Summary

Web servers usually give developers the ability to add small pieces of dynamic code inside static HTML pages, without having to deal with full-fledged server-side or client-side languages. This feature is provided by [Server-Side Includes](https://owasp.org/www-community/attacks/Server-Side_Includes_%28SSI%29_Injection)(SSI).

Server-Side Includes are directives that the web server parses before serving the page to the user. They represent an alternative to writing CGI programs or embedding code using server-side scripting languages, when there's only need to perform very simple tasks. Common SSI implementations provide directives (commands) to include external files, to set and print web server CGI environment variables, or to execute external CGI scripts or system commands.

SSI can lead to a Remote Command Execution (RCE), however most webservers have the `exec` directive disabled by default.

This is a vulnerability very similar to a classical scripting language injection vulnerability. One mitigation is that the web server needs to be configured to allow SSI. On the other hand, SSI injection vulnerabilities are often simpler to exploit, since SSI directives are easy to understand and, at the same time, quite powerful, e.g., they can output the content of files and execute system commands.

## Test Objectives

- Identify SSI injection points.
- Assess the severity of the injection.

## How to Test

To test for exploitable SSI, inject SSI directives as user input. If SSI are enabled and user input validation has not been properly implemented, the server will execute the directive. This is very similar to a classical scripting language injection vulnerability in that it occurs when user input is not properly validated and sanitized.

First determine if the web server supports SSI directives. Often, the answer is yes, as SSI support is quite common. To determine if SSI directives are supported, discover the type of web server that the target is running using information gathering techniques (see [Fingerprint Web Server](../01-Information_Gathering/02-Fingerprint_Web_Server.md)). If you have access to the code, determine if SSI directives are used by searching through the webserver configuration files for specific keywords.

Another way of verifying that SSI directives are enabled is by checking for pages with the `.shtml` extension, which is associated with SSI directives. The use of the `.shtml` extension is not mandatory, so not having found any `.shtml` files doesn't necessarily mean that the target is not vulnerable to SSI injection attacks.

The next step is determining all the possible user input vectors and testing to see if the SSI injection is exploitable.

First find all the pages where user input is allowed. Possible input vectors may also include headers and cookies. Determine how the input is stored and used, i.e if the input is returned as an error message or page element and if it was modified in some way. Access to the source code can help you to more easily determine where the input vectors are and how input is handled.

Once you have a list of potential injection points, you may determine if the input is correctly validated. Ensure it is possible to inject characters used in SSI directives such as `<!#=/."->` and `[a-zA-Z0-9]`

The below example returns the value of the variable. The [references](#references) section has helpful links with server-specific documentation to help you better assess a particular system.

```html
<!--#echo var="VAR" -->
```

When using the `include` directive, if the supplied file is a CGI script, this directive will include the output of the CGI script. This directive may also be used to include the content of a file or list files in a directory:

```html
<!--#include virtual="FILENAME" -->
```

To return the output of a system command:

```html
<!--#exec cmd="OS_COMMAND" -->
```

If the application is vulnerable, the directive is injected and it would be interpreted by the server the next time the page is served.

The SSI directives can also be injected in the HTTP headers, if the web application is using that data to build a dynamically generated page:

```text
GET / HTTP/1.1
Host: www.example.com
Referer: <!--#exec cmd="/bin/ps ax"-->
User-Agent: <!--#include virtual="/proc/version"-->
```

## Tools

- [Web Proxy Burp Suite](https://portswigger.net/burp/communitydownload)
- [OWASP ZAP](https://www.zaproxy.org/)
- [String searcher: grep](https://www.gnu.org/software/grep)

## References

- [Nginx SSI module](http://nginx.org/en/docs/http/ngx_http_ssi_module.html)
- [Apache: Module mod_include](https://httpd.apache.org/docs/current/mod/mod_include.html)
- [IIS: Server Side Includes directives](https://docs.microsoft.com/en-us/previous-versions/iis/6.0-sdk/ms525185%28v=vs.90%29)
- [Apache Tutorial: Introduction to Server Side Includes](https://httpd.apache.org/docs/current/howto/ssi.html)
- [Apache: Security Tips for Server Configuration](https://httpd.apache.org/docs/current/misc/security_tips.html#ssi)
- [SSI Injection instead of JavaScript Malware](https://jeremiahgrossman.blogspot.com/2006/08/ssi-injection-instead-of-javascript.html)
- [IIS: Notes on Server-Side Includes (SSI) syntax](https://blogs.iis.net/robert_mcmurray/archive/2010/12/28/iis-notes-on-server-side-includes-ssi-syntax-kb-203064-revisited.aspx)
- [Header Based Exploitation](https://www.cgisecurity.com/papers/header-based-exploitation.txt)
