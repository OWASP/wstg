# Testing for JavaScript Execution

|ID          |
|------------|
|WSTG-CLNT-02|

## Summary

A JavaScript injection vulnerability is a subtype of cross site scripting (XSS) that involves the ability to inject arbitrary JavaScript code that is executed by the application inside the victim's browser. This vulnerability can have many consequences, like the disclosure of a user's session cookies that could be used to impersonate the victim, or, more generally, it can allow the attacker to modify the page content seen by the victims or the application's behavior.

JavaScript injection vulnerabilities can occur when the application lacks proper user-supplied input and output validation. As JavaScript is used to dynamically populate web pages, this injection occurs during this content processing phase and consequently affects the victim.

When testing for this vulnerability, consider that some characters are treated differently by different browsers. For reference, see [DOM-based XSS](https://owasp.org/www-community/attacks/DOM_Based_XSS).

Here is an example of a script that does not perform any validation of the variable `rr`. The variable contains user-supplied input via the query string, and additionally does not apply any form of encoding:

```js
var rr = location.search.substring(1);
if(rr) {
    window.location=decodeURIComponent(rr);
}
```

This implies that an attacker could inject JavaScript code simply by submitting the following query string: `www.victim.com/?javascript:alert(1)`.

## Test Objectives

- Identify sinks and possible JavaScript injection points.

## How to Test

Consider the following: [DOM XSS exercise](http://www.domxss.com/domxss/01_Basics/04_eval.html)

The page contains the following script:

```html
<script>
function loadObj(){
    var cc=eval('('+aMess+')');
    document.getElementById('mess').textContent=cc.message;
}

if(window.location.hash.indexOf('message')==-1) {
    var aMess='({"message":"Hello User!"})';
} else {
    var aMess=location.hash.substr(window.location.hash.indexOf('message=')+8)
}
</script>
```

The above code contains a source `location.hash` that is controlled by the attacker that can inject directly in the `message` value a JavaScript Code to take the control of the user browser.
