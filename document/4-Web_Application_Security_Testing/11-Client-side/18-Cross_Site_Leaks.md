# Cross-Site Leaks

|ID          |
|------------|
|WSTG-CLNT-18|

## Summary

Cross-site leaks (XS-Leaks) are a class of client-side issues where a page on another site learns something about a user's state on the target application without being able to read the target's responses. The same-origin policy stops the attacker's page from reading a cross-origin response, but the browser still exposes side effects of loading it: whether a request succeeded or failed, how many frames the page contains, how long it took, whether it redirected, and so on.

When a response differs depending on the user's data, those side effects turn into a yes/no oracle. Typical examples:

- A search endpoint that returns results or an empty page, so an attacker can test whether the victim's mailbox contains a given word, one guess per request.
- A profile or resource URL that returns `200` for one user and `403` or `404` for another, revealing who the victim is or which groups they belong to.
- A page that embeds an extra frame, or redirects elsewhere, only when the user is logged in.

The victim only has to visit the attacker's page while logged in to the target. The browser sends the victim's cookies with the cross-site requests where cookie settings allow it, so the leak is about the victim's data, not the attacker's.

This page covers the leak techniques and the defenses to check. For reading cross-origin data directly, see [Cross Origin Resource Sharing](07-Cross_Origin_Resource_Sharing.md) and [Cross Site Script Inclusion](13-Cross_Site_Script_Inclusion.md). For framing, see [Clickjacking](09-Clickjacking.md).

## Test Objectives

- Identify responses that change with the authenticated user's state or data.
- Determine whether a cross-site page can observe those differences through browser side channels.
- Assess whether the application uses the browser defenses that stop cross-site requests or remove the side channels.

## How to Test

### Find State-Dependent Responses

Leaks need a response that differs between two states the attacker wants to tell apart. Good candidates are:

- search, filter and autocomplete endpoints that take the query in the URL;
- pages and API endpoints for a specific object, user, group or tenant;
- pages that only exist, or look different, for logged-in users or for users with a role;
- endpoints that redirect depending on the session, such as a login page that sends an authenticated user straight to a dashboard.

For each candidate, request it in both states, for example with a matching and a non-matching search term, and compare the status code, the `Content-Type`, the number of `<iframe>` elements, the redirects and the response size and time. Any difference is a possible oracle. A candidate only matters if the attacker can choose the URL, so focus on parameters in the path or the query string of a `GET` request.

### Check Whether Cookies Are Sent Cross-Site

Most leaks rely on the browser sending the victim's session cookie with the cross-site request. Check the `SameSite` attribute of the session cookies (see [Cookies Attributes](../06-Session_Management/02-Cookies_Attributes.md)):

- `SameSite=Strict`: the cookie is not sent on any cross-site request, which stops most of the techniques below.
- `SameSite=Lax`, or no attribute in browsers that default to `Lax`: the cookie is sent on top-level `GET` navigations, such as `window.open()` or a link, but not on cross-site subresource requests like `<script>` or `<img>`. Window-based techniques like frame counting still work.
- `SameSite=None`: the cookie is sent on cross-site subresource requests too, where the browser still allows third-party cookies.

Browsers that block or partition third-party cookies remove many subresource-based leaks, so test in more than one browser and note the browser and settings used.

### Test the Leak Techniques

Host a test page on a different site from the target, log in to the target in the same browser, and open the test page. Run each check with the state that should match and the one that should not, and see whether the results differ.

#### Load and Error Events

Elements like `<script>`, `<img>` and `<link>` fire `load` or `error` depending on the response, which often reveals the status code class:

```html
<script>
  const s = document.createElement('script');
  s.src = 'https://target.example/api/search?q=invoice';
  s.onload = () => console.log('load');
  s.onerror = () => console.log('error');
  document.head.appendChild(s);
</script>
```

The exact event also depends on the `Content-Type`, `X-Content-Type-Options: nosniff` and the browser's cross-origin read blocking, so compare the two states instead of assuming which event means what. This technique needs the session cookie to be sent on subresource requests.

#### Frame Counting

A cross-origin window exposes the number of frames it contains through `window.length`. A page that renders an extra `<iframe>` for one state leaks that state to the page that opened it:

```javascript
const w = window.open('https://target.example/search?q=invoice');
setTimeout(() => {
  console.log(w.length);
  w.close();
}, 3000);
```

Because this is a top-level navigation, `SameSite=Lax` cookies are sent. The same check works on an `<iframe>` with `frames[0].length` when the target can be framed and its session cookie is `SameSite=None`, since a cross-site frame isn't a top-level navigation.

#### Redirects

If the target redirects to another origin in one state only, a test page can detect it with its own Content Security Policy. Serve the test page with a policy that only allows images from the target origin, such as `Content-Security-Policy: img-src https://target.example`, and load the URL as an image:

```html
<script>
  document.addEventListener('securitypolicyviolation', () => console.log('redirected off-origin'));
</script>
<img src="https://target.example/account">
```

When the request is redirected to an origin the policy does not allow, the browser blocks it and fires a `securitypolicyviolation` event on the test page. Like the error events above, this needs the cookie on subresource requests. The [XS-Leaks wiki](https://xsleaks.dev/) describes more navigation-based variants. Many of them depend on the browser, so treat a negative result as inconclusive rather than as proof of safety.

#### Timing

Where nothing else differs, the response time may. Measure a credentialed request from the test page several times in each state:

```javascript
async function time(url) {
  const start = performance.now();
  await fetch(url, { mode: 'no-cors', credentials: 'include' });
  return performance.now() - start;
}
```

A consistent difference, such as a search that does more work when it finds results, can be enough. Timing leaks are noisy, so repeat the measurement many times before reporting one.

### Check the Defenses

Look at the response headers of the state-dependent endpoints found above.

- **Fetch Metadata**: browsers send `Sec-Fetch-Site`, `Sec-Fetch-Mode` and `Sec-Fetch-Dest` with each request. A resource isolation policy rejects cross-site requests that are not top-level navigations. Replay a request with the headers a cross-site `<script>` would send and see whether the server still answers normally:

  ```bash
  curl -i 'https://target.example/api/search?q=invoice' \
    -H 'Cookie: session=<session cookie>' \
    -H 'Sec-Fetch-Site: cross-site' \
    -H 'Sec-Fetch-Mode: no-cors' \
    -H 'Sec-Fetch-Dest: script'
  ```

- **Cross-Origin-Opener-Policy**: with `Cross-Origin-Opener-Policy: same-origin`, a page opened from another site gets its own browsing context group, so the opener loses access to it and frame counting through `window.open()` stops working.
- **Cross-Origin-Resource-Policy**: `Cross-Origin-Resource-Policy: same-origin` or `same-site` stops other sites from loading the response as a subresource.
- **Framing controls**: `Content-Security-Policy: frame-ancestors` or `X-Frame-Options` stop the page from being framed, which removes the frame-based variants.
- **Cache**: modern browsers partition the HTTP cache by the top-level site, which stops most cache-probing leaks. Responses with sensitive, user-specific content should still use `Cache-Control: no-store`.

## Remediation

- Set session cookies with `SameSite=Lax` at least, or `Strict` where the application does not need cross-site navigations to stay logged in.
- Deploy a Fetch Metadata resource isolation policy that rejects cross-site requests other than top-level navigations, for endpoints that return user-specific data.
- Send `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Resource-Policy: same-origin` on pages and resources that depend on the user's state.
- Prevent framing with `frame-ancestors` where framing is not needed.
- Where possible, avoid observable differences: return the same status code and page structure whether or not a search matches, and require a `POST` or a user-specific token for sensitive queries.

## Tools

- [XSinator](https://xsinator.com/), a browser test suite that shows which XS-Leak techniques a browser is vulnerable to
- Browser developer tools, to inspect cookies, frames and response headers

## References

- [XS-Leaks Wiki](https://xsleaks.dev/)
- [OWASP XS Leaks Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XS_Leaks_Cheat_Sheet.html)
- [Protect your resources from web attacks with Fetch Metadata](https://web.dev/articles/fetch-metadata)
- [MDN: Cross-Origin-Opener-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy)
- [MDN: Cross-Origin-Resource-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy)
- [XSinator.com: From a Formal Model to the Automatic Evaluation of Cross-Site Leaks in Web Browsers](https://xsinator.com/paper.pdf)
