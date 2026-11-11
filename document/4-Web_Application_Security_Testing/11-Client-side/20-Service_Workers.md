# Service Workers

|ID          |
|------------|
|WSTG-CLNT-20|

## Summary

A [service worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) is a script that the browser runs in the background, separate from any page. It sits between the application and the network: it can intercept every request made by the pages it controls, answer them from a cache, and receive push messages and background sync events while no tab is open.

Service workers only run in a secure context (HTTPS, or `localhost`), and a worker can only control pages at or below the path it was loaded from, unless the server widens this with a `Service-Worker-Allowed` header. They are registered with `navigator.serviceWorker.register()`, and they keep running between visits until they are updated or unregistered.

This lifetime and position make a service worker a high-value target:

- Script running in a worker sees every request made by the pages it controls, including requests to other paths and other origins, and can answer them with its own responses. This includes authenticated pages.
- A worker installed through a cross-site scripting (XSS) flaw can survive after the flaw is fixed, because the worker stays registered in the victim's browser.
- Cached responses can be served to the wrong user or after logout when the caching logic is careless.

This page covers what is specific to service workers. For general script injection, see [JavaScript Execution](02-JavaScript_Execution.md) and [DOM-Based Cross Site Scripting](01-DOM-based_Cross_Site_Scripting.md). For other client-side storage, see [Browser Storage](12-Browser_Storage.md).

## Test Objectives

- Identify the service workers an application registers and the scope each one controls.
- Determine whether an attacker can influence which script is registered, its scope, or the scripts it loads.
- Assess whether the worker's cache and fetch handling can expose or substitute sensitive responses.
- Determine whether a worker keeps running after logout or after a vulnerability is fixed.

## How to Test

### Identify Registered Service Workers

In the browser developer tools, open the **Application** tab (Chrome, Edge and Firefox) and look at **Service Workers**. Note for each worker the script URL, the scope, and its status.

The same information is available from a page's console:

```javascript
navigator.serviceWorker.getRegistrations().then(regs =>
  regs.forEach(r => console.log(r.scope, r.active && r.active.scriptURL))
);
```

Chromium-based browsers also list all registrations, for all sites, at `chrome://serviceworker-internals`, and Firefox at `about:debugging#/runtime/this-firefox`.

Search the application source for calls to `serviceWorker.register(` and note whether the script URL or the `scope` option is built from user-controlled data such as query parameters, the URL fragment, or stored values.

### Review the Script URL and Scope

Check the following:

- The worker script is served from the application's own origin, with a JavaScript MIME type, from a path an attacker cannot write to. A worker script served from a path where users can upload or host files can be replaced by an attacker's script.
- The registration scope is no wider than necessary. A worker registered at `/` controls every page of the site.
- The `Service-Worker-Allowed` response header, if present, does not give a worker at a user-writable path control of the whole origin.
- Registration cannot be triggered with attacker-chosen parameters, for example a script URL that is read from the query string.
- No same-origin URL returns attacker-controlled content with a JavaScript MIME type, such as an uploaded file, a JSONP endpoint or a reflected response. `register()` only accepts a same-origin script served as JavaScript, so such a URL is what lets an attacker register their own worker.

### Review Imported Scripts

Open the worker script and look for [`importScripts()`](https://developer.mozilla.org/en-US/docs/Web/API/WorkerGlobalScope/importScripts) calls and ES module imports. Any script the worker loads from another origin runs with the worker's full control over the application's requests and responses. Note third-party libraries, tag managers and CDNs, and whether the loaded files use fixed, versioned URLs. See also [Cross Site Script Inclusion](13-Cross_Site_Script_Inclusion.md) and [Content Security Policy](../02-Configuration_and_Deployment_Management/12-Content_Security_Policy.md).

### Review Cache and Fetch Handling

Read the worker's `fetch` event handler and the caching it performs. In the developer tools, open **Cache Storage** to see what is stored. Look for:

- Authenticated or user-specific responses (API responses, account pages, tokens in response bodies) being stored in the cache and then returned to a later visitor of the same browser, including after logout.
- Responses cached regardless of status code or of the `Cache-Control: no-store` and `Vary` headers.
- Redirect and error responses being cached and replayed.
- Requests to other origins being answered from the cache or forwarded without checks.
- Cache keys made from user-controlled parts of the URL, which allow one URL to poison the entry for another.

### Test Persistence

Service workers outlive the page that registered them. Check:

- Whether logging out unregisters the worker (`registration.unregister()`) and deletes its caches (`caches.delete()`).
- How the worker is updated. By default the browser bypasses the HTTP cache when it checks the worker script for changes, but not for scripts loaded with `importScripts()`. With `updateViaCache: 'all'` the cached script is used, for at most 24 hours. Note any `updateViaCache` setting and the `Cache-Control` headers on the worker script and its imports.
- If an XSS flaw exists, whether it can be used to register a worker, and whether a malicious worker would remain after the flaw is fixed. Registering a worker also needs a same-origin URL that returns the attacker's script as JavaScript.
- What happens when the worker script is removed. If the script URL starts returning an error, the update fails and the existing worker stays registered and keeps intercepting requests.

Do not leave a test worker registered in a production environment.

### Review Message and Push Handling

If the application uses `postMessage` between pages and the worker, or the Push API, review the `message`, `push` and `notificationclick` handlers:

- The `message` handler should check the sender, in the same way as [Web Messaging](11-Web_Messaging.md) describes for pages.
- Data from a push payload should not be inserted into pages as HTML. Notifications show plain text, but the pages that receive the push data may not.
- A `notificationclick` handler that opens a URL taken from the payload should only open URLs on expected origins.

## Remediation

- Serve the worker script from a fixed, version-controlled path that is not writable by users, and register it with the narrowest scope that works.
- Do not build the script URL or the scope from user input.
- Avoid `importScripts()` from third-party origins, or pin the resources to fixed, trusted versions.
- Never cache authenticated or user-specific responses in a shared cache, and respect `Cache-Control: no-store`.
- Unregister the worker and clear its caches when the user logs out, for example by sending a `Clear-Site-Data: "storage"` response header, which removes both the registration and the caches.
- To remove a worker, replace its script with one that unregisters itself, or send `Clear-Site-Data: "storage"`. Deleting the script file does not remove workers that are already registered.
- Validate the origin and shape of every `message` and `push` event.
- Use a Content Security Policy that restricts `worker-src` and `script-src`.

## Tools

- Browser developer tools (Application panel)
- `chrome://serviceworker-internals` and Firefox's `about:debugging#/runtime/this-firefox`
- [Burp Suite](https://portswigger.net/burp)
- [Zed Attack Proxy (ZAP)](https://www.zaproxy.org/)

## References

- [W3C: Service Workers](https://www.w3.org/TR/service-workers/)
- [MDN: Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [MDN: Using Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers)
- [MDN: Clear-Site-Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data)
- [MDN: Content-Security-Policy worker-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/worker-src)
