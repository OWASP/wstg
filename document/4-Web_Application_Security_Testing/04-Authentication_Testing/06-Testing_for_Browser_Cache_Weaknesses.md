# Testing for Browser Cache Weaknesses

|ID          |
|------------|
|WSTG-ATHN-06|

## Summary

In this phase the tester checks that the application correctly instructs the browser to not retain sensitive data.

Browsers can store information for purposes of caching and history. Caching is used to improve performance, so that previously displayed information doesn't need to be downloaded again. History mechanisms are used for user convenience, so the user can see exactly what they saw at the time when the resource was retrieved. If sensitive information is displayed to the user (such as their address, credit card details, Social Security Number, or username), then this information could be stored for purposes of caching or history, and therefore retrievable through examining the browser's cache or by simply pressing the browser's **Back** button.

## Test Objectives

- Review if the application stores sensitive information on the client-side.
- Review if access can occur without authorization.

## How to Test

### Browser History

Technically, the **Back** button is a history and not a cache (see [Caching in HTTP: History Lists](https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13.13)). The cache and the history are two different entities. However, they share the same weakness of presenting previously displayed sensitive information.

The first and simplest test consists of entering sensitive information into the application and logging out. Then the tester clicks the **Back** button of the browser to check whether previously displayed sensitive information can be accessed whilst unauthenticated.

If by pressing the **Back** button the tester can access previous pages but not access new ones, then it is not an authentication issue, but a browser history issue. If these pages contain sensitive data, it means that the application did not forbid the browser from storing it.

Authentication does not necessarily need to be involved in the testing. For example, when a user enters their email address in order to sign up to a newsletter, this information could be retrievable if not properly handled.

The **Back** button can be stopped from showing sensitive data. This can be done by:

- Delivering the page over HTTPS.
- Setting `Cache-Control: must-revalidate`

### Browser Cache

Here testers check that the application does not leak any sensitive data into the browser cache. In order to do that, they can use a proxy (such as OWASP ZAP) and search through the server responses that belong to the session, checking that for every page that contains sensitive information the server instructed the browser not to cache any data. Such a directive can be issued in the HTTP response headers with the following directives:

- `Cache-Control: no-cache, no-store`
- `Expires: 0`
- `Pragma: no-cache`

These directives are generally robust, although additional flags may be necessary for the `Cache-Control` header in order to better prevent persistently linked files on the file system. These include:

- `Cache-Control: must-revalidate, max-age=0, s-maxage=0`

```http
HTTP/1.1:
Cache-Control: no-cache
```

```html
HTTP/1.0:
Pragma: no-cache
Expires: "past date or illegal value (e.g., 0)"
```

For instance, if testers are testing an e-commerce application, they should look for all pages that contain a credit card number or some other financial information, and check that all those pages enforce the `no-cache` directive. If they find pages that contain critical information but that fail to instruct the browser not to cache their content, they know that sensitive information will be stored on the disk, and they can double-check this simply by looking for the page in the browser cache.

The exact location where that information is stored depends on the client operating system and on the browser that has been used. Here are some examples:

- Mozilla Firefox:
    - Unix/Linux: `~/.cache/mozilla/firefox/`
    - Windows: `C:\Users\<user_name>\AppData\Local\Mozilla\Firefox\Profiles\<profile-id>\Cache2\`
- Internet Explorer:
    - `C:\Users\<user_name>\AppData\Local\Microsoft\Windows\INetCache\`
- Chrome:
    - Windows: `C:\Users\<user_name>\AppData\Local\Google\Chrome\User Data\Default\Cache`
    - Unix/Linux: `~/.cache/google-chrome`

#### Reviewing Cached Information

Firefox provides functionality for viewing cached information, which may be to your benefit as a tester. Of course the industry has also produced various extensions, and external apps which you may prefer or need for Chrome, Internet Explorer, or Edge.

Cache details are also available via developer tools in most modern browsers, such as [Firefox](https://developer.mozilla.org/en-US/docs/Tools/Storage_Inspector#Cache_Storage), [Chrome](https://developers.google.com/web/tools/chrome-devtools/storage/cache), and Edge. With Firefox it is also possible to use the URL `about:cache` to check cache details.

#### Check Handling for Mobile Browsers

Handling of cache directives may be completely different for mobile browsers. Therefore, testers should start a new browsing session with clean caches and take advantage of features like Chrome's [Device Mode](https://developers.google.com/web/tools/chrome-devtools/device-mode) or Firefox's [Responsive Design Mode](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_Mode) to re-test or separately test the concepts outlined above.

Additionally, personal proxies such as ZAP and Burp Suite allow the tester to specify which `User-Agent` should be sent by their spiders/crawlers. This could be set to match a mobile browser `User-Agent` string and used to see which caching directives are sent by the application being tested.

### Gray-Box Testing

The methodology for testing is equivalent to the black-box case, as in both scenarios testers have full access to the server response headers and to the HTML code. However, with gray-box testing, the tester may have access to account credentials that will allow them to test sensitive pages that are accessible only to authenticated users.

## Tools

- [OWASP Zed Attack Proxy](https://www.zaproxy.org)

## References

### Whitepapers

- [Caching in HTTP](https://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html)
