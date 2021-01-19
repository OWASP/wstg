# Testing for HTTP Parameter Pollution

|ID          |
|------------|
|WSTG-INPV-04|

## Summary

HTTP Parameter Pollution tests the applications response to receiving multiple HTTP parameters with the same name; for example, if the parameter `username` is included in the GET or POST parameters twice.

Supplying multiple HTTP parameters with the same name may cause an application to interpret values in unanticipated ways. By exploiting these effects, an attacker may be able to bypass input validation, trigger application errors or modify internal variables values. As HTTP Parameter Pollution (in short *HPP*) affects a building block of all web technologies, server and client-side attacks exist.

Current HTTP standards do not include guidance on how to interpret multiple input parameters with the same name. For instance, [RFC 3986](https://www.ietf.org/rfc/rfc3986.txt) simply defines the term *Query String* as a series of field-value pairs and [RFC 2396](https://www.ietf.org/rfc/rfc2396.txt) defines classes of reversed and unreserved query string characters. Without a standard in place, web application components handle this edge case in a variety of ways (see the table below for details).

By itself, this is not necessarily an indication of vulnerability. However, if the developer is not aware of the problem, the presence of duplicated parameters may produce an anomalous behavior in the application that can be potentially exploited by an attacker. As often in security, unexpected behaviors are a usual source of weaknesses that could lead to HTTP Parameter Pollution attacks in this case. To better introduce this class of vulnerabilities and the outcome of HPP attacks, it is interesting to analyze some real-life examples that have been discovered in the past.

### Input Validation and Filters Bypass

In 2009, immediately after the publication of the first research on HTTP Parameter Pollution, the technique received attention from the security community as a possible way to bypass web application firewalls.

One of these flaws, affecting *ModSecurity SQL Injection Core Rules*, represents a perfect example of the impedance mismatch between applications and filters. The ModSecurity filter would correctly apply a deny list for the following string: `select 1,2,3 from table`, thus blocking this example URL from being processed by the web server: `/index.aspx?page=select 1,2,3 from table`. However, by exploiting the concatenation of multiple HTTP parameters, an attacker could cause the application server to concatenate the string after the ModSecurity filter already accepted the input. As an example, the URL `/index.aspx?page=select 1&page=2,3` from table would not trigger the ModSecurity filter, yet the application layer would concatenate the input back into the full malicious string.

Another HPP vulnerability turned out to affect *Apple Cups*, the well-known printing system used by many UNIX systems. Exploiting HPP, an attacker could easily trigger a Cross-Site Scripting vulnerability using the following URL: `http://127.0.0.1:631/admin/?kerberos=onmouseover=alert(1)&kerberos`. The application validation checkpoint could be bypassed by adding an extra `kerberos` argument having a valid string (e.g. empty string). As the validation checkpoint would only consider the second occurrence, the first `kerberos` parameter was not properly sanitized before being used to generate dynamic HTML content. Successful exploitation would result in JavaScript code execution under the context of the hosting web site.

### Authentication Bypass

An even more critical HPP vulnerability was discovered in *Blogger*, the popular blogging platform. The bug allowed malicious users to take ownership of the victim’s blog by using the following HTTP request (`https://www.blogger.com/add-authors.do`):

```html
POST /add-authors.do HTTP/1.1
[...]

security_token=attackertoken&blogID=attackerblogidvalue&blogID=victimblogidvalue&authorsList=goldshlager19test%40gmail.com(attacker email)&ok=Invite
```

The flaw resided in the authentication mechanism used by the web application, as the security check was performed on the first `blogID` parameter, whereas the actual operation used the second occurrence.

### Expected Behavior by Application Server

The following table illustrates how different web technologies behave in presence of multiple occurrences of the same HTTP parameter.

Given the URL and querystring: `http://example.com/?color=red&color=blue`

  | Web Application Server Backend | Parsing Result | Example |
  |--------------------------------|----------------|--------|
  | ASP.NET / IIS | All occurrences concatenated with a comma |  color=red,blue |
  | ASP / IIS     | All occurrences concatenated with a comma | color=red,blue |
  | .NET Core 3.1 / Kestrel | All occurrences concatenated with a comma | color=red,blue |
  | .NET 5 / Kestrel | All occurrences concatenated with a comma | color=red,blue |
  | PHP / Apache  | Last occurrence only | color=blue |
  | PHP / Zeus | Last occurrence only | color=blue |
  | JSP, Servlet / Apache Tomcat | First occurrence only | color=red |
  | JSP, Servlet / Oracle Application Server 10g | First occurrence only | color=red |
  | JSP, Servlet / Jetty  | First occurrence only | color=red |
  | IBM Lotus Domino | Last occurrence only | color=blue |
  | IBM HTTP Server | First occurrence only | color=red |
  | node.js / express | First occurence only | color=red |
  | mod_perl, libapreq2 / Apache | First occurrence only | color=red |
  | Perl CGI / Apache | First occurrence only | color=red |
  | mod_wsgi (Python) / Apache | First occurrence only | color=red |
  | Python / Zope | All occurrences in List data type | color=['red','blue'] |

(source: [Appsec EU 2009 Carettoni & Paola](https://owasp.org/www-pdf-archive/AppsecEU09_CarettoniDiPaola_v0.8.pdf))

## Test Objectives

- Identify the backend and the parsing method used.
- Assess injection points and try bypassing input filters using HPP.

## How to Test

Luckily, because the assignment of HTTP parameters is typically handled via the web application server, and not the application code itself, testing the response to parameter pollution should be standard across all pages and actions. However, as in-depth business logic knowledge is necessary, testing HPP requires manual testing. Automatic tools can only partially assist auditors as they tend to generate too many false positives. In addition, HPP can manifest itself in client-side and server-side components.

### Server-Side HPP

To test for HPP vulnerabilities, identify any form or action that allows user-supplied input. Query string parameters in HTTP GET requests are easy to tweak in the navigation bar of the browser. If the form action submits data via POST, the tester will need to use an intercepting proxy to tamper with the POST data as it is sent to the server. Having identified a particular input parameter to test, one can edit the GET or POST data by intercepting the request, or change the query string after the response page loads. To test for HPP vulnerabilities simply append the same parameter to the GET or POST data but with a different value assigned.

For example: if testing the `search_string` parameter in the query string, the request URL would include that parameter name and value:

```text
http://example.com/?search_string=kittens
```

The particular parameter might be hidden among several other parameters, but the approach is the same; leave the other parameters in place and append the duplicate:

```text
http://example.com/?mode=guest&search_string=kittens&num_results=100
```

Append the same parameter with a different value:

```text
http://example.com/?mode=guest&search_string=kittens&num_results=100&search_string=puppies
```

and submit the new request.

Analyze the response page to determine which value(s) were parsed. In the above example, the search results may show `kittens`, `puppies`, some combination of both (`kittens,puppies` or `kittens~puppies` or `['kittens','puppies']`), may give an empty result, or error page.

This behavior, whether using the first, last, or combination of input parameters with the same name, is very likely to be consistent across the entire application. Whether or not this default behavior reveals a potential vulnerability depends on the specific input validation and filtering specific to a particular application. As a general rule: if existing input validation and other security mechanisms are sufficient on single inputs, and if the server assigns only the first or last polluted parameters, then parameter pollution does not reveal a vulnerability. If the duplicate parameters are concatenated, different web application components use different occurrences or testing generates an error, there is an increased likelihood of being able to use parameter pollution to trigger security vulnerabilities.

A more in-depth analysis would require three HTTP requests for each HTTP parameter:

1. Submit an HTTP request containing the standard parameter name and value, and record the HTTP response. E.g. `page?par1=val1`
2. Replace the parameter value with a tampered value, submit and record the HTTP response. E.g. `page?par1=HPP_TEST1`
3. Send a new request combining step (1) and (2). Again, save the HTTP response. E.g. `page?par1=val1&par1=HPP_TEST1`
4. Compare the responses obtained during all previous steps. If the response from (3) is different from (1) and the response from (3) is also different from (2), there is an impedance mismatch that may be eventually abused to trigger HPP vulnerabilities.

Crafting a full exploit from a parameter pollution weakness is beyond the scope of this text. See the references for examples and details.

### Client-Side HPP

Similarly to server-side HPP, manual testing is the only reliable technique to audit web applications in order to detect parameter pollution vulnerabilities affecting client-side components. While in the server-side variant the attacker leverages a vulnerable web application to access protected data or to perform actions that either not permitted or not supposed to be executed, client-side attacks aim at subverting client-side components and technologies.

To test for HPP client-side vulnerabilities, identify any form or action that allows user input and shows a result of that input back to the user. A search page is ideal, but a login box might not work (as it might not show an invalid username back to the user).

Similarly to server-side HPP, pollute each HTTP parameter with `%26HPP_TEST` and look for *url-decoded* occurrences of the user-supplied payload:

- `&HPP_TEST`
- `&amp;HPP_TEST`
- etc.

In particular, pay attention to responses having HPP vectors within `data`, `src`, `href` attributes or forms actions. Again, whether or not this default behavior reveals a potential vulnerability depends on the specific input validation, filtering and application business logic. In addition, it is important to notice that this vulnerability can also affect query string parameters used in XMLHttpRequest (XHR), runtime attribute creation and other plugin technologies (e.g. Adobe Flash’s flashvars variables).

## Tools

- [OWASP ZAP Passive/Active Scanners](https://www.zaproxy.org)

## References

### Whitepapers

- [HTTP Parameter Pollution - Luca Carettoni, Stefano di Paola](https://owasp.org/www-pdf-archive/AppsecEU09_CarettoniDiPaola_v0.8.pdf)
- [Client-side HTTP Parameter Pollution Example (Yahoo! Classic Mail flaw) - Stefano di Paola](https://blog.mindedsecurity.com/2009/05/client-side-http-parameter-pollution.html)
- [How to Detect HTTP Parameter Pollution Attacks - Chrysostomos Daniel](https://www.acunetix.com/blog/whitepaper-http-parameter-pollution/)
- [CAPEC-460: HTTP Parameter Pollution (HPP) - Evgeny Lebanidze](https://capec.mitre.org/data/definitions/460.html)
- [Automated Discovery of Parameter Pollution Vulnerabilities in Web Applications - Marco Balduzzi, Carmen Torrano Gimenez, Davide Balzarotti, Engin Kirda](http://s3.eurecom.fr/docs/ndss11_hpp.pdf)
