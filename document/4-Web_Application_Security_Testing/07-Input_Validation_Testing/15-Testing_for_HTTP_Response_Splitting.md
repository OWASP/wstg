# Testing for HTTP Response Splitting

|ID          |
|------------|
|WSTG-INPV-15|

## Summary

HTTP Response Splitting is a vulnerability that occurs when an application incorporates unsanitized user input into HTTP response headers, allowing an attacker to inject Carriage Return (CR) and Line Feed (LF) characters. As a result, a single HTTP response can be interpreted as multiple distinct responses by clients or intermediary systems.

Successful exploitation of HTTP Response Splitting can lead to various impacts, including web cache poisoning, cross-site scripting (XSS), content spoofing, session fixation, or other client-side attacks, depending on how the injected response is processed.

This section focuses exclusively on identifying and testing HTTP Response Splitting vulnerabilities at the application layer. HTTP Request Smuggling, which relies on parsing inconsistencies between multiple HTTP agents, is covered in a separate chapter.

## Test Objectives

- Identify user-controlled input that is reflected into HTTP response headers.
- Assess whether CR (`\r`) and LF (`\n`) characters can be injected into response headers.
- Determine the potential impact of successful HTTP Response Splitting attacks, such as cache poisoning or client-side exploitation.

## How to Test

### Black-Box Testing

Some web applications use user-supplied input to generate the values of certain HTTP response headers. A common example is redirection logic, where the destination URL is derived from a request parameter.

For instance, assume a user is asked to choose between a standard or advanced interface. The selected option is passed as a parameter and reflected in a redirection response header.

If the parameter `interface` has the value `advanced`, the application may respond with:

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 03 Dec 2005 16:22:19 GMT
Location: https://victim.com/main.jsp?interface=advanced
```

When the browser receives this response, it follows the URL specified in the `Location` header. However, if the application does not properly validate or sanitize user input, an attacker may inject the sequence `%0d%0a`, representing CRLF characters used to separate HTTP header lines.

By injecting CRLF sequences, a tester may cause the response to be interpreted as two separate HTTP responses by downstream clients or intermediary systems, such as web caches. This behavior can be exploited to poison caches or deliver malicious content to users.

For example, the tester supplies the following value for the `interface` parameter:

`advanced%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0aContent-Length:%2035%0d%0a%0d%0a<html>Sorry,%20System%20Down</html>`

The resulting response from the vulnerable application may be:

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 03 Dec 2005 16:22:19 GMT
Location: https://victim.com/main.jsp?interface=advanced
Content-Length: 0

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 35

<html>Sorry,%20System%20Down</html>
```

A web cache processing this response may interpret it as two distinct responses. If the attacker immediately issues a subsequent request for `/index.html`, the cache may associate that request with the second response and store it. As a result, all subsequent users accessing `victim.com/index.html` through that cache may receive the attacker-controlled content.

Alternatively, the attacker may inject a JavaScript payload to perform a cross-site scripting attack against users served by the poisoned cache. Although the vulnerability resides in the application, the primary targets are its users.

To identify this issue, testers should locate all user-controlled input that influences HTTP response headers and verify whether CRLF sequences can be injected.

The response headers most commonly associated with HTTP Response Splitting include:

- `Location`
- `Set-Cookie`

Successful exploitation in real-world scenarios may require careful consideration of additional factors:

- The tester may need to craft response headers suitable for caching (e.g., `Last-Modified` set to a future date) and potentially invalidate existing cache entries using headers such as `Pragma: no-cache`.
- Applications may filter CRLF characters but allow alternative encodings or character representations, which can sometimes be leveraged to bypass input validation.
- Some platforms URL-encode portions of response headers (such as the path in the `Location` header) while leaving the query string unencoded, allowing injection through specific components of the URL.

For a deeper discussion of this attack class and additional exploitation scenarios, refer to the whitepapers listed in the References section.

### Gray-Box Testing

In a gray-box testing scenario, knowledge of the application architecture and server behavior can significantly improve the reliability of HTTP Response Splitting exploitation.

Different servers, intermediaries, or clients may determine message boundaries using different techniques. Some rely strictly on HTTP header boundaries, while others may assume messages are separated by network packets or fixed-size buffers. In such cases, the injected response must begin at a precise offset, requiring the tester to use padding between messages.

This constraint may pose challenges when the vulnerable parameter is transmitted in a URL, as excessively long URLs may be truncated or rejected. With architectural insight, testers may identify alternative request methods (such as POST instead of GET) or injection points that allow greater control over payload length and positioning.

## Remediation

Ensure that user-supplied input is never placed into HTTP headers without strict validation and sanitization.

- **Input Validation:** Reject or strip input containing Carriage Return (`\r`, `%0d`) or Line Feed (`\n`, `%0a`) characters before it is used in HTTP headers.
- **URL Encoding:** If the input is part of a URL (e.g., in a `Location` header), ensure it is properly URL-encoded to prevent control characters from being interpreted as delimiters.
- **Use Secure Frameworks:** Utilize built-in framework functions for setting headers (e.g., `setHeader()`, `addHeader()`) rather than manually constructing raw HTTP response strings. Modern environments typically block header injection by default.

## Tools

- [ZAP](https://www.zaproxy.org/)
- [Burp Suite](https://portswigger.net/burp)
- [CRLFuzz](https://github.com/dwisiswant0/crlfuzz) - A tool designed specifically to scan for CRLF vulnerabilities.
- [Nuclei](https://github.com/projectdiscovery/nuclei) - Can be used with specific templates to detect CRLF injection patterns.

## References

- [Amit Klein, "Divide and Conquer: HTTP Response Splitting, Web Cache Poisoning Attacks, and Related Topics"](https://packetstormsecurity.com/files/32815/Divide-and-Conquer-HTTP-Response-Splitting-Whitepaper.html)
- [Amit Klein: "HTTP Message Splitting, Smuggling and Other Animals"](https://www.slideserve.com/alicia/http-message-splitting-smuggling-and-other-animals-powerpoint-ppt-presentation)
- [Amit Klein: "HTTP Request Smuggling - ERRATA (the IIS 48K buffer phenomenon)"](https://web.archive.org/web/20210614052317/https://www.securityfocus.com/archive/1/411418)
- [Amit Klein: "HTTP Response Smuggling"](https://web.archive.org/web/20210126213458/https://www.securityfocus.com/archive/1/425593)
- [Chaim Linhart, Amit Klein, Ronen Heled, Steve Orrin: "HTTP Request Smuggling"](https://web.archive.org/web/20210816212852/https://www.cgisecurity.com/lib/http-request-smuggling.pdf)
