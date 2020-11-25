# Testing Web Messaging

|ID          |
|------------|
|WSTG-CLNT-11|

## Summary

Web Messaging (also known as [Cross Document Messaging](https://html.spec.whatwg.org/multipage/web-messaging.html#web-messaging)) allows applications running on different domains to communicate in a secure manner. Before the introduction of web messaging, the communication of different origins (between iframes, tabs and windows) was restricted by the same origin policy and enforced by the browser. Developers used multiple hacks in order to accomplish these tasks, and most of them were mainly insecure.

This restriction within the browser is in place to prevent a malicious website from reading confidential data from other iframes, tabs, etc; however, there are some legitimate cases where two trusted websites need to exchange data with each other. To meet this need, Cross Document Messaging was introduced in the [WHATWG HTML5](https://html.spec.whatwg.org/multipage/) draft specification and was implemented in all major browsers. It enables secure communications between multiple origins across iframes, tabs and windows.

The messaging API introduced the [`postMessage()` method](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage), with which plain-text messages can be sent cross-origin. It consists of two parameters: message, and domain.

There are some security concerns when using `*` as the domain that we discuss below. In order to receive messages, the receiving website needs to add a new event handler, which has the following attributes:

- Data, the content of the incoming message;
- Origin of the sender document; and
- Source, the source window.

Here is an example of the messaging API in use. To send a message:

```js
iframe1.contentWindow.postMessage("Hello world","http://www.example.com");
```

To receive a message:

```js
window.addEventListener("message", handler, true);
function handler(event) {
    if(event.origin === 'chat.example.com') {
        /* process message (event.data) */
    } else {
        /* ignore messages from untrusted domains */
    }
}
```

### Origin Security

The origin is made up of a scheme, host name, and port. It uniquely identifies the domain sending or receiving the message, and does not include the path or the fragment part of the URL. For instance, `https://example.com` will be considered different from `http://example.com` because the schema of the former is `https`, while the latter is `http`. This also applies to web servers running in the same domain but on different ports.

## Test Objectives

- Assess the security of the message's origin.
- Validate that it's using safe methods and validating its input.

## How to Test

### Examine Origin Security

Testers should check whether the application code is filtering and processing messages from trusted domains. Within the sending domain, also ensure that the receiving domain is explicitly stated, and that `*` is not used as the second argument of `postMessage()`. This practice could introduce security concerns and could lead to, in the case of a redirection or if the origin changes by other means, the website sending data to unknown hosts, and therefore, leaking confidential data to malicious servers.

If the website fails to add security controls to restrict the domains or origins that are allowed to send messages to a website, it is likely to introduce a security risk. Testers should examine the code for message event listeners and get the callback function from the `addEventListener` method for further analysis. Domains must always be verified prior to data manipulation.

### Examine Input Validation

Although the website is theoretically accepting messages from trusted domains only, data must still be treated as externally-sourced, untrusted data, and processed with the appropriate security controls. Testers should analyze the code and look for insecure methods, in particular where data is being evaluated via `eval()` or inserted into the DOM via the `innerHTML` property, which may create DOM-based XSS vulnerabilities.

### Static Code Analysis

JavaScript code should be analyzed to determine how web messaging is implemented. In particular, testers should be interested in how the website is restricting messages from untrusted domains, and how the data is handled even for trusted domains.

In this example, access is needed for every subdomain (www, chat, forums, ...) within the owasp.org domain. The code is trying to accept any domain with `.owasp.org`:

```js
window.addEventListener("message", callback, true);

function callback(e) {
    if(e.origin.indexOf(".owasp.org")!=-1) {
        /* process message (e.data) */
    }
}
```

The intention is to allow subdomains such as:

- `www.owasp.org`
- `chat.owasp.org`
- `forums.owasp.org`

Unfortunately, this introduces vulnerabilities. An attacker can easily bypass the filter since a domain such as `www.owasp.org.attacker.com` will match.

Here is an example of code that lacks an origin check. This is very insecure, as it will accept input from any domain:

```js
window.addEventListener("message", callback, true);

function callback(e) {
        /* process message (e.data) */
}
```

Here is an example with input validation vulnerabilities that may lead to XSS attack:

```js
window.addEventListener("message", callback, true);

function callback(e) {
        if(e.origin === "trusted.domain.com") {
            element.innerHTML= e.data;
        }
}
```

A more secure approach would be to use the property `innerText` instead of `innerHTML`.

For further OWASP resources regarding web messaging, see [OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
