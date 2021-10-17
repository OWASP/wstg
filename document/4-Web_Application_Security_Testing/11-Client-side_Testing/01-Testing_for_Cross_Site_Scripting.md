# Testing for Cross Site Scripting

|ID          |
|------------|
|WSTG-CLNT-01|

## Summary

Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted websites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application uses input from a user within the output it generates without validating or encoding it.

An attacker can use XSS to send a malicious script to an unsuspecting user. The end user’s browser has no way to know that the script should not be trusted, and will execute the script. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with that site. These scripts can even rewrite the content of the HTML page.

## Test Objectives

- Identify XSS Injection Points
- Assess the severity of the injection and the level of access that can be achieved through it.

## How to Test

The [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) is a great resource on how to test for the various kinds of XSS vulnerabilities. For information on specicfic types of XSS, see the following pages for more details:

- [Testing for Reflected Cross Site Scripting](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/01.1-Testing_for_Reflected_Cross_Site_Scripting)
- [Testing for Stored Cross Site Scripting](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/01.2-Testing_for_Stored_Cross_Site_Scripting)
- [Testing for DOM-Based Cross Site Scripting](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/01.3-Testing_for_DOM-based_Cross_Site_Scripting)
- [Testing for Self DOM Based Cross-Site Scripting](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/01..4-Testing_for_Self_DOM_Based_Cross_Site_Scripting)

## Tools

- [PHP Charset Encoder(PCE)](https://cybersecurity.wtf/encoder/) helps you encode arbitrary texts to and from 65 kinds of character sets that you can use in your customized payloads.
- [Hackvertor](https://hackvertor.co.uk/public) is an online tool which allows many types of encoding and obfuscation of JavaScript (or any string input).
- [BeEF](https://www.beefproject.com) is the browser exploitation framework. A professional tool to demonstrate the real-time impact of browser vulnerabilities.
- [XSS-Proxy](http://xss-proxy.sourceforge.net/) is an advanced Cross-Site-Scripting (XSS) attack tool.
- [Burp Proxy](https://portswigger.net/burp/) is an interactive HTTP/S proxy server for attacking and testing web applications.
- [XSS Assistant](https://www.greasespot.net/) Greasemonkey script that allow users to easily test any web application for cross-site-scripting flaws.
- [OWASP Zed Attack Proxy (ZAP)](https://www.zaproxy.org) is an interactive HTTP/S proxy server for attacking and testing web applications with a built-in scanner.
- [XSS Hunter Portable](https://github.com/mandatoryprogrammer/xsshunter) XSS Hunter finds all kinds of cross-site scripting vulnerabilities, including the often-missed blind XSS.

## References

### OWASP Resources
* [Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
