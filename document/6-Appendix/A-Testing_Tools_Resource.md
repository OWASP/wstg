# Testing Tools Resource

## Introduction

This appendix is intended to provide a list of common tools that are used for web application testing. It does not aim to be a complete tool reference, and the inclusion of a tool here should not be seen as a specific endorsement of that tool by OWASP.

The list contains only tools that are freely available to download and use (although they may have licenses restricting their use for commercial activity).

## General Web Testing

### Web Proxies

- [ZAP](https://www.zaproxy.org)
    - The Zed Attack Proxy (ZAP) is an easy to use integrated penetration testing tool for finding vulnerabilities in web applications. It is designed to be used by people with a wide range of security experience and as such is ideal for developers and functional testers who are new to penetration testing.
    - ZAP provides automated scanners as well as a set of tools that allow you to find security vulnerabilities manually.
- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
    - Burp Suite is an intercepting proxy for security testing. It allows intercepting and modifying all HTTP(S) traffic passing in both directions, it can work with custom TLS certificates and non-proxy-aware clients.
- [Telerik Fiddler](https://www.telerik.com/fiddler)
    - Fiddler an intercepting web proxy that is primarily aimed at developers rather than penetration testers, but still provides useful functionality. It also hooks directly into the Windows HTTP APIs, allowing it to intercept traffic from some software that doesn't allow custom proxies to be set.

### Firefox Extensions

- [Firefox HTTP Header Live](https://addons.mozilla.org/en-US/firefox/addon/http-header-live)
    - View HTTP headers of a page and while browsing.
- [Firefox Multi-Account Containers](https://addons.mozilla.org/en-GB/firefox/addon/multi-account-containers/)
    - Create multiple containers, each of which have their own isolated cookies and sessions. Useful for testing access control between different users.
- [Firefox Tamper Data](https://addons.mozilla.org/en-US/firefox/addon/tamper-data-for-ff-quantum/)
    - Use Tamper Data to view and modify HTTP/HTTPS headers and post parameters
- [Firefox Web Developer](https://addons.mozilla.org/en-US/firefox/addon/web-developer/)
    - The Web Developer extension adds various web developer tools to the browser.

### Chrome Extensions

- [Chrome Web Developer](https://chrome.google.com/webstore/detail/bfbameneiokkgbdmiekhjnmfkcnldhhm)
    - The Web Developer extension adds a toolbar button to the browser with various web developer tools. This is the official port of the Web Developer extension for Chrome.
- [HTTP Request Maker](https://chrome.google.com/webstore/detail/kajfghlhfkcocafkcjlajldicbikpgnp?hl=en-US)
    - Request Maker is a tool for penetration testing. With it you can easily capture requests made by web pages, tamper with the URL, headers and POST data and, of course, make new requests
- [Cookie Editor](https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg?hl=en-US)
    - Edit This Cookie is a cookie manager. You can add, delete, edit, search, protect and block cookies

### Testing for Specific Vulnerabilities

#### Testing for SQL Injection

- [sqlmap](http://sqlmap.org)

#### Testing TLS

- [OWASP O-Saft](https://owasp.org/www-project-o-saft/)
- [sslyze](https://github.com/nabla-c0d3/sslyze)
- [testssl.sh](https://github.com/drwetter/testssl.sh)
- [SSLScan](https://github.com/rbsec/sslscan)
- [SSLLabs](https://www.ssllabs.com/ssltest/)

#### Testing for Brute Force Attacks

##### Hash Crackers

- [John the Ripper](https://github.com/openwall/john)
- [hashcat](https://hashcat.net/hashcat/)

##### Remote Brute Force

- [ZAP](https://www.zaproxy.org)
- [Patator](https://github.com/lanjelot/patator)
- [THC Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [Burp Suite Community Edition (Intruder)](https://portswigger.net/burp/communitydownload)

#### Fuzzers

- [Ffuf](https://github.com/ffuf/ffuf)
- [Wfuzz](https://github.com/xmendez/wfuzz)
- [Jdam](https://gitlab.com/michenriksen/jdam)

#### Google Hacking

- [Google Hacking database](https://www.exploit-db.com/google-hacking-database/)

#### Slow HTTP

- [Slowloris](https://github.com/gkbrk/slowloris)
- [slowhttptest](https://github.com/shekyan/slowhttptest)

### Site Mirroring

- [wget](https://www.gnu.org/software/wget/)
- [wget for windows](http://gnuwin32.sourceforge.net/packages/wget.htm)
- [curl](https://curl.haxx.se)

### Content Discovery

- [Gobuster](https://github.com/OJ/gobuster)

### Port and Service Discovery

- [Nmap](https://nmap.org/)

## Vulnerability Scanners

- [ZAP](https://www.zaproxy.org)
- [Nikto](https://cirt.net/Nikto2)
- [Nuclei](https://nuclei.projectdiscovery.io/)
- [SecOps Solution](https://secopsolution.com)

## Exploitation Frameworks

- [Metasploit](https://github.com/rapid7/metasploit-framework)
- [BeEF](https://github.com/beefproject/beef/)

## Linux Distributions

- [Kali](https://www.kali.org)
- [Parrot](https://www.parrotsec.org)
- [Samurai](https://github.com/SamuraiWTF/samuraiwtf)
- [Santoku](https://sourceforge.net/projects/santoku/)
- [BlackArch](https://blackarch.org/downloads.html)

## Source Code Analyzers

- [Spotbugs](https://spotbugs.github.io)
- [Find Security Bugs](https://find-sec-bugs.github.io)
- [phpcs-security-audit](https://github.com/squizlabs/PHP_CodeSniffer)
- [PMD](https://pmd.github.io)
- [Microsoft's .NET Analyzers](https://docs.microsoft.com/en-us/visualstudio/code-quality/install-net-analyzers)
- [SonarQube Community Edition](https://www.sonarqube.org)

## Browser Automation Tools

Browser Automation tools are used to validate the functionality of web applications. Some follow a scripted approach and typically make use of a Unit Testing framework to construct test suites and test cases. Most, if not all, can be adapted to perform security specific tests in addition to functional tests.

### Open Source Tools

- [HtmlUnit](http://htmlunit.sourceforge.net)
    - A Java and JUnit based framework that uses the Apache HttpClient as the transport.
    - Very robust and configurable and is used as the engine for a number of other testing tools.
- [Selenium](https://www.selenium.dev)
    - JavaScript based testing framework, cross-platform and provides a GUI for creating tests.
