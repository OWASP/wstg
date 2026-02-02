# Testing for Client-side Template Injection

|ID          |
|------------|
|WSTG-CLNT-15|

## Summary

Client-Side Template Injection (CSTI), also known as DOM-based Template Injection, arises when applications using client-side frameworks (such as Angular, Vue.js, or Alpine.js) dynamically embed user input into the web page's DOM. If this input is embedded into a template expression or interpreted by the framework's template engine, an attacker can inject malicious directives.

Unlike [Server-Side Template Injection (SSTI)](../07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection.md), where the template is rendered on the server, CSTI occurs entirely within the user's browser. When the framework scans the DOM for dynamic content, it may execute the injected template expressions. This often leads to Cross-Site Scripting (XSS), but the method of injection and exploitation differs from standard XSS because the payload must follow the specific syntax of the template engine (e.g., `{{ 7*7 }}`).

This vulnerability is particularly common in Single Page Applications (SPAs) where developers might rely on client-side rendering without strict context separation.

## Test Objectives

- Identify the client-side framework and its version used by the application.
- Detect injection points where user input is reflected into the DOM and processed by the template engine.
- Assess if the injection allows for arbitrary JavaScript execution (XSS) via the template syntax.

## How to Test

### Black-Box Testing

#### Framework Identification

The first step is to identify if a client-side framework is in use. Testers should look for specific attributes in the HTML source code or specific HTTP response headers.

- **Angular:** Look for attributes like `ng-app`, `ng-model`, or `ng-bind`.
- **Vue.js:** Look for attributes starting with `v-`, such as `v-if`, `v-for`, or the presence of the Vue global object in the console.
- **Alpine.js:** Look for `x-data`, `x-html`.

#### Injection Detection

To detect CSTI, testers should inject characters that are syntactically significant to the template engine. The most common syntax for interpolation in many frameworks is double curly braces `{{ }}`.

A simple arithmetic operation is the standard probe. If the application evaluates the math, it is vulnerable.

**Generic Probe:**

{% raw %}
```txt
Inject the string: {{ 7*7 }}
```
{% endraw %}

- If the application renders `49`, CSTI is present.
- If the application renders `{{ 7*7 }}`, it is likely not vulnerable or strict contextual escaping is in place.

#### Angular

Angular acts on the DOM. If an attacker can inject a string containing Angular expressions into the DOM before Angular bootstraps or compiles it, the expression will be executed.

**Payloads for Detection:**

{% raw %}
- `{{ 7*7 }}`
- `{{ constructor.constructor('alert(1)')() }}`
{% endraw %}

In older versions of Angular (1.x), the template engine works in a sandbox. Exploitation requires breaking out of this sandbox. The complexity of the payload depends heavily on the specific version.

**Example Payload (Angular 1.5.x sandbox bypass):**

{% raw %}
```javascript
{{x={'y':''.constructor.prototype};x['y'].charAt=[].join;$eval('x=alert(1)');}}
```
{% endraw %}

#### Vue.js

Vue.js is also susceptible if developers use the `v-html` directive with user input or if they mount a Vue instance on a DOM element that already contains user-controlled HTML.

**Payloads for Detection:**

{% raw %}
- `{{ 7*7 }}`
{% endraw %}

**Example Payload (Vue.js 2.x):**

{% raw %}
```javascript
{{_v.constructor('alert(1)')()}}
```
{% endraw %}

#### Alpine.js

Alpine.js relies heavily on DOM attributes. If an attacker can control an attribute name or inject into a directive, they can execute code.

**Example Payload:**

```html
<div x-data="" x-html="'<img src=x onerror=alert(1)>'"></div>
```

### Gray-Box Testing

#### Code Review

In a gray-box scenario, testers verify how user input is handled in the frontend code. The key is to identify where "sinks" that interpret HTML or Template Syntax are used with "tainted" sources (user input).

**Angular Sinks:**
Search for usages of `$compile` or `ng-bind-html`.
If `ng-bind-html` is used, check if `$sce` (Strict Contextual Escaping) is properly configured or if `$sce.trustAsHtml()` is used on untrusted data.

```javascript
// Vulnerable example in Angular
$scope.htmlSnippet = $sce.trustAsHtml(userInput);
```

**Vue.js Sinks:**
Search for the `v-html` directive. Using `v-html` on user-provided content is a primary cause of CSTI/XSS in Vue.

```html
<div v-html="userProvidedComment"></div>
```

**React Sinks:**
While React is generally safer regarding template injection because it does not scan the DOM for templates (JSX is compiled), improper use of `dangerouslySetInnerHTML` allows for DOM-based XSS, which is the React equivalent of the risk profile discussed here.

```javascript
// Vulnerable example in React
<div dangerouslySetInnerHTML={{__html: userContent}} />
```

#### Configuration Review

Check specifically for Content Security Policy (CSP) headers. A strong CSP can mitigate the impact of CSTI by restricting where scripts can be loaded from or preventing the execution of inline scripts (including those generated by template engines).

Look for `unsafe-eval` in the CSP. Many template engines (especially older ones) require `unsafe-eval` to compile templates dynamically. If `unsafe-eval` is present, CSTI attacks are significantly easier to exploit.

## Remediation

- **Avoid Rendering User Input as HTML:** Whenever possible, use safe directives that treat input as text only.
    - Angular: Use `ng-bind` instead of `ng-bind-html`.
    - Vue: Use `v-text` or curly braces `{{ }}` (which auto-escape HTML) instead of `v-html`.
    - React: Avoid `dangerouslySetInnerHTML`.
- **Sanitization:** If HTML rendering is required, use a dedicated sanitization library (like DOMPurify) to strip dangerous tags and attributes before passing the data to the framework.
- **Content Security Policy (CSP):** Implement a strict CSP that disables `unsafe-eval` and restricts script sources.
- **Use Offline Compilation:** For frameworks like Vue or React, prefer using build steps (webpack, vite) that compile templates ahead of time rather than using the runtime compiler that parses DOM content.

### Tools

- [DOMPurify](https://github.com/cure53/DOMPurify): A DOM-only, super-fast, uber-tolerant XSS sanitizer for HTML, MathML, and SVG.

## References

### Whitepapers and Articles

- [PortSwigger: Client-Side Template Injection](https://portswigger.net/research/server-side-template-injection)
- [Gareth Heyes: Angular Sandbox Bypasses](https://portswigger.net/research/dom-based-angularjs-sandbox-escapes)
- [Vue.js Security Guide](https://vuejs.org/guide/best-practices/security.html)
- [Angular Security Guide](https://angular.io/guide/security)
