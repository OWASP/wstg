# Testing for Server-side Template Injection

|ID          |
|------------|
|WSTG-INPV-18|

## Summary

Web applications commonly use server-side templating technologies (Jinja2, Twig, FreeMaker, etc.) to generate dynamic HTML responses. Server-side Template Injection vulnerabilities (SSTI) occur when user input is embedded in a template in an unsafe manner and results in remote code execution on the server. Any features that support advanced user-supplied markup may be vulnerable to SSTI including wiki-pages, reviews, marketing applications, CMS systems etc. Some template engines employ various mechanisms (eg. sandbox, allow listing, etc.) to protect against SSTI.

### Example - Twig

The following example is an excerpt from the [Extreme Vulnerable Web Application](https://github.com/s4n7h0/xvwa) project.

```php
public function getFilter($name)
{
        [snip]
        foreach ($this->filterCallbacks as $callback) {
        if (false !== $filter = call_user_func($callback, $name)) {
            return $filter;
        }
    }
    return false;
}
```

In the getFilter function the `call_user_func($callback, $name)` is vulnerable to SSTI: the `name` parameter is fetched from the HTTP GET request and executed by the server:

![SSTI XVWA Example](images/SSTI_XVWA.jpeg)\
*Figure 4.7.18-1: SSTI XVWA Example*

### Example - Flask/Jinja2

The following example uses Flask and Jinja2 templating engine. The `page` function accepts a 'name' parameter from an HTTP GET request and renders an HTML response with the `name` variable content:

```python
@app.route("/page")
def page():
    name = request.values.get('name')
    output = Jinja2.from_string('Hello ' + name + '!').render()
    return output
```

This code snippet is vulnerable to XSS but it is also vulnerable to SSTI. Using the following as a payload in the `name` parameter:

```bash
$ curl -g 'http://www.target.com/page?name={{7*7}}'
Hello 49!
```

## Test Objectives

- Detect template injection vulnerability points.
- Identify the templating engine.
- Build the exploit.

## How to Test

SSTI vulnerabilities exist either in text or code context. In plaintext context users allowed to use freeform 'text' with direct HTML code. In code context the user input may also be placed within a template statement (eg. in a variable name)

### Identify Template Injection Vulnerability

The first step in testing SSTI in plaintext context is to construct common template expressions used by various template engines as payloads and monitor server responses to identify which template expression was executed by the server.

Common template expression examples:

```text
a{{bar}}b
a{{7*7}}
{var} ${var} {{var}} <%var%> [% var %]
```

In this step an extensive [template expression test strings/payloads list](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection) is recommended.

Testing for SSTI in code context is slightly different. First, the tester constructs the request that result either blank or error server responses. In the example below the HTTP GET parameter is inserted info the variable `personal_greeting` in a template statement:

```text
personal_greeting=username
Hello user01
```

Using the following payload - the server response is blank "Hello":

```text
personal_greeting=username<tag>
Hello
```

In the next step is to break out of the template statement and injecting HTML tag after it using the following payload

```text
personal_greeting=username}}<tag>
Hello user01 <tag>
```

### Identify the Templating Engine

Based on the information from the previous step now the tester has to identify which template engine is used by supplying various template expressions. Based on the server responses the tester deduces the template engine used. This manual approach is discussed in greater detail in [this](https://portswigger.net/blog/server-side-template-injection?#Identify) PortSwigger article. To automate the identification of the SSTI vulnerability and the templating engine various tools are available including [Tplmap](https://github.com/epinna/tplmap) or the [Backslash Powered Scanner Burp Suite extension](https://github.com/PortSwigger/backslash-powered-scanner).

### Build the RCE Exploit

The main goal in this step is to identify to gain further control on the server with an RCE exploit by studying the template documentation and research. Key areas of interest are:

- **For template authors** sections covering basic syntax.
- **Security considerations** sections.
- Lists of built-in methods, functions, filters, and variables.
- Lists of extensions/plugins.

The tester can also identify what other objects, methods and properties can be exposed by focusing on the `self` object. If the `self` object is not available and the documentation does not reveal the technical details, a brute force of the variable name is recommended. Once the object is identified the next step is to loop through the object to identify all the methods, properties and attributes that are accessible through the template engine. This could lead to other kinds of security findings  including privilege escalations, information disclosure about application passwords, API keys, configurations and environment variables, etc.

## Tools

- [Tplmap](https://github.com/epinna/tplmap)
- [Backslash Powered Scanner Burp Suite extension](https://github.com/PortSwigger/backslash-powered-scanner)
- [Template expression test strings/payloads list](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)

## References

- [James Kettle: Server-Side Template Injection:RCE for the modern webapp (whitepaper)](https://portswigger.net/kb/papers/serversidetemplateinjection.pdf)
- [Server-Side Template Injection](https://portswigger.net/blog/server-side-template-injection)
- [Exploring SSTI in Flask/Jinja2](https://www.lanmaster53.com/2016/03/exploring-ssti-flask-jinja2/)
- [Server Side Template Injection: from detection to Remote shell](https://www.okiok.com/server-side-template-injection-from-detection-to-remote-shell/)
- [Extreme Vulnerable Web Application](https://github.com/s4n7h0/xvwa)
- [Divine Selorm Tsa: Exploiting server side template injection with tplmap](https://owasp.org/www-pdf-archive/Owasp_SSTI_final.pdf)
- [Exploiting SSTI in Thymeleaf](https://www.acunetix.com/blog/web-security-zone/exploiting-ssti-in-thymeleaf/)
