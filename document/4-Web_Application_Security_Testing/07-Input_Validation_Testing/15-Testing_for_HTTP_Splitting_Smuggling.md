# Testing for HTTP Splitting Smuggling

|ID          |
|------------|
|WSTG-INPV-15|

## Summary

This section illustrates examples of attacks that leverage specific features of the HTTP protocol, either by exploiting weaknesses of the web application or peculiarities in the way different agents interpret HTTP messages.
This section will analyze two different attacks that target specific HTTP headers:

- HTTP splitting
- HTTP smuggling

The first attack exploits a lack of input sanitization which allows an intruder to insert CR and LF characters into the headers of the application response and to 'split' that answer into two different HTTP messages. The goal of the attack can vary from a cache poisoning to cross site scripting.

In the second attack, the attacker exploits the fact that some specially crafted HTTP messages can be parsed and interpreted in different ways depending on the agent that receives them. HTTP smuggling requires some level of knowledge about the different agents that are handling the HTTP messages (web server, proxy, firewall) and therefore will be included only in the gray-box testing section.

## Test Objectives

- Assess if the application is vulnerable to splitting, identifying what possible attacks are achievable.
- Assess if the chain of communication is vulnerable to smuggling, identifying what possible attacks are achievable.

## How to Test

### Black-Box Testing

#### HTTP Splitting

Some web applications use part of the user input to generate the values of some headers of their responses. The most straightforward example is provided by redirections in which the target URL depends on some user-submitted value. Let's say for instance that the user is asked to choose whether they prefer a standard or advanced web interface. The choice will be passed as a parameter that will be used in the response header to trigger the redirection to the corresponding page.

More specifically, if the parameter 'interface' has the value 'advanced', the application will answer with the following:

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 03 Dec 2005 16:22:19 GMT
Location: https://victim.com/main.jsp?interface=advanced
<snip>
```

When receiving this message, the browser will bring the user to the page indicated in the Location header. However, if the application does not filter the user input, it will be possible to insert in the 'interface' parameter the sequence %0d%0a, which represents the CRLF sequence that is used to separate different lines. At this point, testers will be able to trigger a response that will be interpreted as two different responses by anybody who happens to parse it, for instance a web cache sitting between us and the application. This can be leveraged by an attacker to poison this web cache so that it will provide false content in all subsequent requests.

Let's say that in the previous example the tester passes the following data as the interface parameter:

`advanced%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:%20text/html%0d%0aContent-Length:%2035%0d%0a%0d%0a<html>Sorry,%20System%20Down</html>`

The resulting answer from the vulnerable application will therefore be the following:

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 03 Dec 2005 16:22:19 GMT
Location: https://victim.com/main.jsp?interface=advanced
Content-Length: 0

HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 35

<html>Sorry,%20System%20Down</html>
<other data>
```

The web cache will see two different responses, so if the attacker sends, immediately after the first request, a second one asking for `/index.html`, the web cache will match this request with the second response and cache its content, so that all subsequent requests directed to `victim.com/index.html` passing through that web cache will receive the "system down" message. In this way, an attacker would be able to effectively deface the site for all users using that web cache (the whole internet, if the web cache is a reverse proxy for the web application).

Alternatively, the attacker could pass to those users a JavaScript snippet that mounts a cross site scripting attack, e.g., to steal the cookies. Note that while the vulnerability is in the application, the target here is its users. Therefore, in order to look for this vulnerability, the tester needs to identify all user controlled input that influences one or more headers in the response, and check whether they can successfully inject a CR+LF sequence in it.

The headers that are the most likely candidates for this attack are:

- `Location`
- `Set-Cookie`

It must be noted that a successful exploitation of this vulnerability in a real world scenario can be quite complex, as several factors must be taken into account:

1. The pen-tester must properly set the headers in the fake response for it to be successfully cached (e.g., a Last-Modified header with a date set in the future). They might also have to destroy previously cached versions of the target pagers, by issuing a preliminary request with `Pragma: no-cache` in the request headers
2. The application, while not filtering the CR+LF sequence, might filter other characters that are needed for a successful attack (e.g., `<` and `>`). In this case, the tester can try to use other encodings (e.g., UTF-7)
3. Some targets (e.g., ASP) will URL-encode the path part of the Location header (e.g., `www.victim.com/redirect.asp`), making a CRLF sequence useless. However, they fail to encode the query section (e.g., ?interface=advanced), meaning that a leading question mark is enough to bypass this filtering

For a more detailed discussion about this attack and other information about possible scenarios and applications, check the papers referenced at the bottom of this section.

### Gray-Box Testing

#### HTTP Splitting

A successful exploitation of HTTP Splitting is greatly helped by knowing some details of the web application and of the attack target. For instance, different targets can use different methods to decide when the first HTTP message ends and when the second starts. Some will use the message boundaries, as in the previous example. Other targets will assume that different messages will be carried by different packets. Others will allocate for each message a number of chunks of predetermined length: in this case, the second message will have to start exactly at the beginning of a chunk and this will require the tester to use padding between the two messages. This might cause some trouble when the vulnerable parameter is to be sent in the URL, as a very long URL is likely to be truncated or filtered. A gray-box scenario can help the attacker to find a workaround: several application servers, for instance, will allow the request to be sent using POST instead of GET.

#### HTTP Smuggling

As mentioned in the introduction, HTTP Smuggling leverages the different ways that a particularly crafted HTTP message can be parsed and interpreted by different agents (browsers, web caches, application firewalls). This relatively new kind of attack was first discovered by Chaim Linhart, Amit Klein, Ronen Heled and Steve Orrin in 2005. There are several possible applications and we will analyze one of the most spectacular: the bypass of an application firewall. Refer to the original whitepaper (linked at the bottom of this page) for more detailed information and other scenarios.

#### Modern HTTP Request Smuggling (HTTP Desync)

Modern HTTP Request Smuggling attacks often target the discrepancies in how frontend servers (load balancers, reverse proxies) and backend servers process the `Content-Length` (CL) and `Transfer-Encoding` (TE) headers. When these two servers disagree on where a request ends, an attacker can smuggle a malicious request that gets interpreted by the backend as the beginning of the next user's request.

According to RFC 7230, if both headers are present, the `Content-Length` header should be ignored. However, if one server fails to follow this rule or creates a desynchronization state, vulnerabilities arise.

There are three main types of desynchronization attacks:

1. **CL.TE**: The frontend uses `Content-Length`, and the backend uses `Transfer-Encoding`.
2. **TE.CL**: The frontend uses `Transfer-Encoding`, and the backend uses `Content-Length`.
3. **TE.TE (Obfuscation)**: Both servers support `Transfer-Encoding`, but one can be induced to ignore it by obfuscating the header, effectively downgrading the attack to CL.TE or TE.CL.

##### Testing for CL.TE Vulnerabilities

In a CL.TE scenario, the frontend processes the request based on `Content-Length` and forwards the entire body. The backend, using `Transfer-Encoding`, stops processing at the termination chunk (`0`). The remaining data acts as a prefix for the next request.

**Example Payload (Triggering a 404):**

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 35
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```

- **Effect:** The backend reads up to the `0`. The `GET /404...` is left in the buffer. When the next legitimate request arrives, it is appended to this prefix, causing the server to respond with a 404 Not Found (proving the interference).

##### Testing for TE.CL Vulnerabilities

In a TE.CL scenario, the frontend handles the chunked encoding correctly. However, the backend uses `Content-Length` and stops reading early. The remainder of the chunked body is treated as the start of the next request.

**Example Payload:**

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 4
Transfer-Encoding: chunked

5c
GET /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

- **Effect:** The backend reads only the first few bytes (defined by `Content-Length`). The rest of the chunked data (starting with `GET /404...`) remains in the buffer and poisons the next request.

##### Testing for TE.TE (Obfuscated TE)

If both servers support `Transfer-Encoding`, the attacker can send an obfuscated header to confuse one of the servers into ignoring it and falling back to `Content-Length`.

**Example Obfuscations:**

- `Transfer-Encoding: xchunked`
- `Transfer-Encoding : chunked`
- `Transfer-Encoding: chunked`
- `Transfer-Encoding:[tab]chunked`

If successful, this desynchronizes the servers, allowing for CL.TE or TE.CL attacks as described above.

##### Testing Tools

- **[Burp Suite (HTTP Request Smuggler)](https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646):** The industry standard for detection and exploitation (BApp Store extension).
- **[Smuggler (Python)](https://github.com/defparam/smuggler):** Command-line alternative for scanning.

##### Application Firewall Bypass

There are several products that enable a system administration to detect and block a hostile web request depending on some known malicious pattern that is embedded in the request. For example, consider the infamous, old [Unicode directory traversal attack against IIS server](https://www.securityfocus.com/bid/1806), in which an attacker could break out the www root by issuing a request like:

`https://target/scripts/..%c1%1c../winnt/system32/cmd.exe?/c+<command_to_execute>`

Of course, it is quite easy to spot and filter this attack by the presence of strings like ".." and "cmd.exe" in the URL. However, IIS 5.0 is quite picky about POST requests whose body is up to 48K bytes and truncates all content that is beyond this limit when the Content-Type header is different from application/x-www-form-urlencoded. The pen-tester can leverage this by creating a very large request, structured as follows:

```html
POST /target.asp HTTP/1.1        <-- Request #1
Host: target
Connection: Keep-Alive
Content-Length: 49225
<CRLF>
<49152 bytes of garbage>
```

```html
POST /target.asp HTTP/1.0        <-- Request #2
Connection: Keep-Alive
Content-Length: 33
<CRLF>
```

```html
POST /target.asp HTTP/1.0        <-- Request #3
xxxx: POST /scripts/..%c1%1c../winnt/system32/cmd.exe?/c+dir HTTP/1.0   <-- Request #4
Connection: Keep-Alive
<CRLF>
```

What happens here is that the `Request #1` is made of 49223 bytes, which includes also the lines of `Request #2`. Therefore, a firewall (or any other agent beside IIS 5.0) will see Request #1, will fail to see `Request #2` (its data will be just part of #1), will see `Request #3` and miss `Request #4` (because the POST will be just part of the fake header xxxx).

Now, what happens to IIS 5.0 ? It will stop parsing `Request #1` right after the 49152 bytes of garbage (as it will have reached the 48K=49152 bytes limit) and will therefore parse `Request #2` as a new, separate request. `Request #2` claims that its content is 33 bytes, which includes everything until "xxxx: ", making IIS miss `Request #3` (interpreted as part of `Request #2`) but spot `Request #4`, as its POST starts right after the 33rd byte or `Request #2`. It is a bit complicated, but the point is that the attack URL will not be detected by the firewall (it will be interpreted as the body of a previous request) but will be correctly parsed (and executed) by IIS.

While in the aforementioned case the technique exploits a bug of a web server, there are other scenarios in which we can leverage the different ways that different HTTP-enabled devices parse messages that are not 1005 RFC compliant. For instance, the HTTP protocol allows only one Content-Length header, but does not specify how to handle a message that has two instances of this header. Some implementations will use the first one while others will prefer the second, cleaning the way for HTTP Smuggling attacks. Another example is the use of the Content-Length header in a GET message.

Note that HTTP Smuggling does `*not*` exploit any vulnerability in the target web application. Therefore, it might be somewhat tricky, in a pen-test engagement, to convince the client that a countermeasure should be looked for anyway.

## References

### Whitepapers

- [Amit Klein, "Divide and Conquer: HTTP Response Splitting, Web Cache Poisoning Attacks, and Related Topics"](https://packetstormsecurity.com/files/32815/Divide-and-Conquer-HTTP-Response-Splitting-Whitepaper.html)
- [Amit Klein: "HTTP Message Splitting, Smuggling and Other Animals"](https://www.slideserve.com/alicia/http-message-splitting-smuggling-and-other-animals-powerpoint-ppt-presentation)
- [Amit Klein: "HTTP Request Smuggling - ERRATA (the IIS 48K buffer phenomenon)"](https://web.archive.org/web/20210614052317/https://www.securityfocus.com/archive/1/411418)
- [Amit Klein: "HTTP Response Smuggling"](https://web.archive.org/web/20210126213458/https://www.securityfocus.com/archive/1/425593)
- [Chaim Linhart, Amit Klein, Ronen Heled, Steve Orrin: "HTTP Request Smuggling"](https://packetstormsecurity.com/files/37651/HTTP-Request-Smuggling.pdf.html)
- [James Kettle: "HTTP Desync Attacks: Request Smuggling Reborn" (PortSwigger Research)](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)
- [RFC 7230, Section 3.3.3: Message Body Length](https://datatracker.ietf.org/doc/html/rfc7230#section-3.3.3)
