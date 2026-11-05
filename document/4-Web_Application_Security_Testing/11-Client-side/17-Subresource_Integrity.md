# Testing Subresource Integrity and Third-Party Resources

|ID          |
|------------|
|WSTG-CLNT-17|

## Summary

Most applications load some scripts and style sheets from servers they do not control, such as content delivery networks (CDNs), analytics providers and widget vendors. A script loaded this way runs with the full privileges of the page that includes it. If the third-party server is compromised, or the resource is replaced for any other reason, the attacker's code runs in the application's origin and can read the page, steal session data and act as the user.

[Subresource Integrity (SRI)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) lets a page declare the cryptographic hash of the file it expects. The browser fetches the file, compares its hash, and refuses to run or apply it if the hash does not match:

```html
<script src="https://cdn.example.com/lib/1.2.3/lib.min.js"
        integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
        crossorigin="anonymous"></script>
```

SRI is supported for `<script>` and `<link rel="stylesheet">` elements. It does not protect resources that are added by other means, such as scripts that are created at runtime and the content a tag manager injects.

This page covers how third-party resources are loaded and pinned. For the policy header that limits where resources may be loaded from, see [Testing for Content Security Policy](../02-Configuration_and_Deployment_Management/12-Content_Security_Policy.md). For attacks that read cross-origin data through script inclusion, see [Testing for Cross Site Script Inclusion](13-Cross_Site_Script_Inclusion.md).

## Test Objectives

- Identify the scripts and style sheets an application loads from origins it does not control.
- Determine whether those resources are pinned with SRI.
- Assess how a change to a third-party resource would affect the application.

## How to Test

### Identify Third-Party Resources

List every external script and style sheet the application uses.

- Review the page source and the rendered DOM for `<script src>` and `<link rel="stylesheet" href>` elements whose host differs from the application's own origin.
- In the browser developer tools, open the **Network** tab, filter by **JS** and **CSS**, and look at the **Domain** column. Do this on each distinct page type, including the login page and pages shown after authentication, because they often load different resources.
- Note scripts that load further scripts. Tag managers and widget loaders can bring in resources that are not visible in the page source.

The following snippet lists external scripts and style sheets that have no `integrity` attribute on the current page:

```javascript
document.querySelectorAll('script[src], link[rel="stylesheet"][href]').forEach(el => {
  const url = new URL(el.src || el.href, location.href);
  if (url.origin !== location.origin && !el.integrity) {
    console.log(el.tagName, url.href);
  }
});
```

### Check for Integrity Attributes

For each external resource that has an `integrity` attribute, check that:

- The hash algorithm is SHA-256, SHA-384 or SHA-512. Browsers ignore unsupported algorithms.
- The `crossorigin` attribute is set. For a cross-origin resource, the integrity check needs the server to answer with CORS headers, and the request must be made in CORS mode (`crossorigin="anonymous"` is usual).
- The hash matches the file. To compute it, download the file and run:

```bash
curl -s https://cdn.example.com/lib/1.2.3/lib.min.js | openssl dgst -sha384 -binary | openssl base64 -A
```

Compare the result, with the `sha384-` prefix, to the attribute value. A mismatch makes the browser block the resource, which shows as a console error such as `Failed to find a valid digest in the 'integrity' attribute`.

### Check How the Resource Is Referenced

SRI works only when the file at the URL does not change. Look for references that can change:

- URLs without a version, or with floating versions such as `latest`, `@1` or `/v1/`. A pinned hash on such a URL breaks the page when the file changes, so sites often leave it out.
- Vendor-hosted scripts that are updated by the vendor without notice, such as analytics, chat and A/B-testing scripts. SRI cannot be used for these, so the application relies on trust in the vendor.
- Hosts that have expired, are no longer in use or have a dangling DNS record. See [Testing for Subdomain Takeover](../02-Configuration_and_Deployment_Management/10-Subdomain_Takeover.md).
- Resources loaded over plain HTTP.

### Check Runtime-Loaded Resources

SRI attributes are not applied to resources that are added with script such as `document.createElement('script')`, unless the code sets the `integrity` property itself. Review the application's scripts and tag manager configuration for such resources, and note which pages load them and who can change the tag manager configuration.

### Check the Interaction with CSP

A Content Security Policy can restrict the hosts scripts may come from, and can allow scripts by hash or nonce. Check whether the policy allows broad hosts (for example a whole CDN domain) that would let an attacker load a different file from the same host. SRI and CSP complement each other: CSP limits where code may come from, and SRI limits which file from that location is accepted.

## Remediation

- Add `integrity` and `crossorigin` attributes to third-party scripts and style sheets that can be pinned.
- Reference exact versions of libraries, or host a copy of the library on the application's own origin.
- Remove resources that are no longer used, and review each remaining third-party script and its vendor.
- Limit the scripts a tag manager can load and restrict who can edit it.
- Combine SRI with a restrictive Content Security Policy.

## Tools

- Browser developer tools (Network and Console panels)
- `openssl` and `curl`
- [Burp Suite](https://portswigger.net/burp)
- [OWASP ZAP](https://www.zaproxy.org/)

## References

- [W3C: Subresource Integrity](https://www.w3.org/TR/SRI/)
- [MDN: Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
- [OWASP: Third Party JavaScript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)
