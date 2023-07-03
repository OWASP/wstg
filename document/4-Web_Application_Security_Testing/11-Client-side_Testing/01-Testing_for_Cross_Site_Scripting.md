# Testing for Cross Site Scripting

|ID          |
|------------|
|WSTG-CLNT-01|

## Summary

Cross-Site Scripting (XSS) testing checks if it is possible to inject malicious scripts into a web application, which are then executed by users' browsers. XSS vulnerabilities occur when user-supplied input is not properly validated or sanitized before being included in the application's output. Successful exploitation of an XSS vulnerability allows attackers to execute arbitrary JavaScript code within the context of a victim's browser, leading to various attacks such as session hijacking, defacement, or stealing sensitive information.

XSS attacks can be classified into the following three types:

Stored XSS: The malicious script is permanently stored on the target server and is served to users when they access a particular page or view specific content.

Reflected XSS: The malicious script is embedded in a URL and is reflected back to the user by the web application, typically as part of an error message or search result.

DOM-based XSS: The vulnerability arises from insecure handling of client-side JavaScript in the Document Object Model (DOM) of a web page. The malicious script is directly executed by the victim's browser.

An XSS attack occurs when an attacker can inject untrusted data into a web application, which is then included in a response that is sent to other users. This untrusted data can be included in various contexts within an HTML document, including:

HTML tags: If user-supplied input is inserted without proper encoding into HTML tags, it can lead to script execution. For example:

```js
<script>alert('XSS');</script>
```

HTML attributes: If user-supplied input is included in HTML attributes without proper encoding, it can be exploited to execute scripts. For example:

```js
<img src="x" onerror="alert('XSS')">
```

JavaScript code: If user-supplied input is directly inserted into JavaScript code without proper escaping or validation, it can lead to script execution. For example:

```js
var userInput = '<%= userInput %>';
```

URLs: If user-supplied input is included in URLs without proper encoding, it can result in script execution. For example:

```js
https://example.com/search?q=<script>alert('XSS');</script>
```

XSS vulnerabilities can have severe consequences, ranging from stealing sensitive user information to performing actions on behalf of the user, such as modifying account settings or making unauthorized transactions.

## Test Objectives

Identify input fields or parameters vulnerable to XSS attacks.
Assess the impact and severity of XSS vulnerabilities.
Validate the effectiveness of input validation and output encoding mechanisms in preventing XSS attacks.

## How to Test

### Detection Techniques

The first step in XSS testing is to identify all user-supplied input fields or parameters within the web application. This includes input fields in web forms, query string parameters in URLs, hidden form fields, cookies, headers, and any other input sources that are used to generate dynamic content.

Once the input fields or parameters are identified, the following techniques can be employed to detect XSS vulnerabilities:

HTML Injection: Inject HTML tags and check if they are rendered as part of the web page. For example:

```js
<script>alert('XSS');</script>
```

If the injected HTML tags are not properly sanitized, they will be interpreted and executed by the browser.

Attribute Injection: Inject special characters or event handlers into HTML attributes and check if they are executed. For example:

```js
"><img src=x onerror=alert('XSS')>
```

If the injected content is rendered without proper encoding, the browser will interpret it as part of the attribute value, leading to script execution.

JavaScript Injection: Inject JavaScript code into areas of the application where it is expected to be executed. This includes JavaScript code within `<script>` tags, inline event handlers, or within JavaScript variables. For example:

```js
');alert('XSS');//
````

If the injected JavaScript code is not properly escaped or validated, it will be executed by the browser.

URL Injection: Inject script payloads into URLs and check if they are executed. For example:

```js
https://example.com/search?q=<script>alert('XSS');</script>
```

If the injected script is not properly encoded, it will be interpreted as part of the URL and executed by the browser.

Context-Specific Injection: Test for XSS vulnerabilities in specific contexts such as input fields used in search functionality, comment sections, messaging systems, or any other areas where user-supplied input is displayed to other users.

During testing, it is important to observe the behavior of the application and analyze the responses received. Look for any unexpected execution of scripts or the presence of injected content within the rendered HTML source code. Additionally, monitor the network traffic to identify any requests or responses that contain suspicious or unexpected content.

It is recommended to test various browsers to ensure cross-browser compatibility of the identified XSS vulnerabilities.

## Remediation

To mitigate XSS vulnerabilities, the following best practices should be implemented:

Input Validation: Perform strict input validation on all user-supplied input. Accept only the expected characters and reject or sanitize any input that contains special characters or script-like content.

Output Encoding: Encode all user-supplied input that is rendered within HTML, JavaScript, or URL contexts. Use proper encoding mechanisms specific to the context, such as HTML entity encoding, JavaScript escaping, or URL encoding.

Content Security Policy (CSP): Implement a strong CSP to restrict the execution of scripts from external sources and enforce a allow list(s) of trusted sources for content.

HTTP Only Cookies: Set the "HttpOnly" flag for session cookies to prevent access from client-side scripts, reducing the risk of session theft via XSS.

X-XSS-Protection Header: Enable the X-XSS-Protection header with the "1; mode=block" directive to instruct browsers to block or sanitize detected XSS attacks.

Contextual Output Encoding: Apply output encoding based on the context in which the user-supplied input is rendered. Different encoding mechanisms may be required for HTML, JavaScript, or URL contexts.
