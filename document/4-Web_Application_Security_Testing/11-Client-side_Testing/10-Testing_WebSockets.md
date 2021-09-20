# Testing WebSockets

|ID          |
|------------|
|WSTG-CLNT-10|

## Summary

Traditionally, the HTTP protocol only allows one request/response per TCP connection. Asynchronous JavaScript and XML (AJAX) allows clients to send and receive data asynchronously (in the background without a page refresh) to the server, however, AJAX requires the client to initiate the requests and wait for the server responses (half-duplex).

[WebSockets](https://html.spec.whatwg.org/multipage/web-sockets.html#network) allow the client or server to create a 'full-duplex' (two-way) communication channel, allowing the client and server to truly communicate asynchronously. WebSockets conduct their initial *upgrade* handshake over HTTP and from then on all communication is carried out over TCP channels by use of frames. For more, see the [WebSocket Protocol](https://tools.ietf.org/html/rfc6455).

### Origin

It is the server’s responsibility to verify the [`Origin` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin) in the initial HTTP WebSocket handshake. If the server does not validate the origin header in the initial WebSocket handshake, the WebSocket server may accept connections from any origin. This could allow attackers to communicate with the WebSocket server cross-domain allowing for CSRF-like issues. See also [Top 10-2017 A5-Broken Access Control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control).

### Confidentiality and Integrity

WebSockets can be used over unencrypted TCP or over encrypted TLS. To use unencrypted WebSockets the `ws://` URI scheme is used (default port 80), to use encrypted (TLS) WebSockets the `wss://` URI scheme is used (default port 443). See also [Top 10-2017 A3-Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure).

### Input Sanitization

As with any data originating from untrusted sources, the data should be properly sanitized and encoded. See also [Top 10-2017 A1-Injection](https://owasp.org/www-project-top-ten/2017/A1_2017-Injection) and [Top 10-2017 A7-Cross-Site Scripting (XSS)](https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_(XSS)).

## Test Objectives

- Identify the usage of WebSockets.
- Assess its implementation by using the same tests on normal HTTP channels.

## How to Test

### Black-Box Testing

1. Identify that the application is using WebSockets.
   - Inspect the client-side source code for the `ws://` or `wss://` URI scheme.
   - Use Google Chrome's Developer Tools to view the Network WebSocket communication.
   - Use [ZAP's](https://www.zaproxy.org) WebSocket tab.
2. Origin.
   - Using a WebSocket client (one can be found in the [Tools](#Tools) section below) attempt to connect to the remote WebSocket server. If a connection is established the server may not be checking the origin header of the WebSocket handshake.
3. Confidentiality and Integrity.
   - Check that the WebSocket connection is using SSL to transport sensitive information `wss://`.
   - Check the SSL Implementation for security issues (Valid Certificate, BEAST, CRIME, RC4, etc). Refer to the [Testing for Weak Transport Layer Security](../09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_Transport_Layer_Security.md) section of this guide.
4. Authentication.
   - WebSockets do not handle authentication, normal black-box authentication tests should be carried out. Refer to the [Authentication Testing](../04-Authentication_Testing/README.md) sections of this guide.
5. Authorization.
   - WebSockets do not handle authorization, normal black-box authorization tests should be carried out. Refer to the [Authorization Testing](../05-Authorization_Testing/README.md) sections of this guide.
6. Input Sanitization.
   - Use [ZAP's](https://www.zaproxy.org) WebSocket tab to replay and fuzz WebSocket request and responses. Refer to the [Testing for Data Validation](../07-Input_Validation_Testing/README.md) sections of this guide.

#### Example 1

Once we have identified that the application is using WebSockets (as described above) we can use the [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org) to intercept the WebSocket request and responses. ZAP can then be used to replay and fuzz the WebSocket request/responses.

![ZAP WebSockets](images/OWASP_ZAP_WebSockets.png)\
*Figure 4.11.10-1: ZAP WebSockets*

#### Example 2

Using a WebSocket client (one can be found in the [Tools](#Tools) section below) attempt to connect to the remote WebSocket server. If the connection is allowed the WebSocket server may not be checking the WebSocket handshake's origin header. Attempt to replay requests previously intercepted to verify that cross-domain WebSocket communication is possible.

![WebSocket Client](images/WebSocket_Client.png)\
*Figure 4.11.10-2: WebSocket Client*

### Gray-Box Testing

Gray-box testing is similar to black-box testing. In gray-box testing, the pen-tester has partial knowledge of the application. The only difference here is that you may have API documentation for the application being tested which includes the expected WebSocket request and responses.

## Tools

- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org)
- [WebSocket Client](https://github.com/ethicalhack3r/scripts/blob/master/WebSockets.html)
- [Google Chrome Simple WebSocket Client](https://chrome.google.com/webstore/detail/simple-websocket-client/pfdhoblngboilpfeibdedpjgfnlcodoo?hl=en)

## References

- [HTML5 Rocks - Introducing WebSockets: Bringing Sockets to the Web](https://www.html5rocks.com/en/tutorials/websockets/basics/)
- [W3C - The WebSocket API](https://html.spec.whatwg.org/multipage/web-sockets.html#network)
- [IETF - The WebSocket Protocol](https://tools.ietf.org/html/rfc6455)
- [Christian Schneider - Cross-Site WebSocket Hijacking (CSWSH)](http://www.christian-schneider.net/CrossSiteWebSocketHijacking.html)
- [Robert Koch- On WebSockets in Penetration Testing](http://www.ub.tuwien.ac.at/dipl/2013/AC07815487.pdf)
- [DigiNinja - OWASP ZAP and Web Sockets](http://www.digininja.org/blog/zap_web_sockets.php)
