# Testing Tools Resource

## General Web Testing

### Web Proxies

- [OWASP ZAP](https://www.zaproxy.org)
  - The Zed Attack Proxy (ZAP) is an easy to use integrated penetration testing tool for finding vulnerabilities in web applications. It is designed to be used by people with a wide range of security experience and as such is ideal for developers and functional testers who are new to penetration testing.
  - ZAP provides automated scanners as well as a set of tools that allow you to find security vulnerabilities manually.
- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
  - Burp Suite is an intercepting proxy for security testing. It allows intercepting and modifying all HTTP(S) traffic passing in both directions, it can work with custom SSL certificates and non-proxy-aware clients.

### Firefox Extensions

- [Firefox HTTP Header Live](https://addons.mozilla.org/en-US/firefox/addon/http-header-live)
  - View HTTP headers of a page and while browsing.
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

#### Testing for DOM-based XSS

- [BlueClosure BC Detect](https://www.blueclosure.com)

#### Testing for SQL Injection

- [sqlmap](http://sqlmap.org)

#### Testing SSL

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

- [Patator](https://github.com/lanjelot/patator)
- [THC Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [Burp Suite Professional (Intruder)](https://portswigger.net/burp/pro)

#### Fuzzers

- [Wfuzz](https://github.com/xmendez/wfuzz)

#### Google Hacking

- [Google Hacking Diggity Project](https://resources.bishopfox.com/resources/tools/google-hacking-diggity/)
- [Google Hacking database](https://www.exploit-db.com/google-hacking-database/)

#### Slow HTTP

- [Slowloris](https://github.com/gkbrk/slowloris)
- [slowhttptest](https://github.com/shekyan/slowhttptest)

### Site Mirroring

- [wget](https://www.gnu.org/software/wget/)
- [wget for windows](http://gnuwin32.sourceforge.net/packages/wget.htm)
- [curl](https://curl.haxx.se)

## Vulnerability Scanners

### Open Source

- [w3af](https://w3af.org)
- [OWASP ZAP](https://www.zaproxy.org)

### Commercial

- [HCL AppScan](https://www.hcltechsw.com/products/appscan)
- [Burpsuite Professional](https://portswigger.net/burp)
- [Acunetix Web Vulnerability Scanner](https://www.acunetix.com)
- [MaxPatrol Security Scanner](https://www.ptsecurity.com/ww-en/products/maxpatrol/)
- [Parasoft SOAtest (more QA-type tool)](https://www.parasoft.com/products/soatest)
- [N-Stalker Web Application Security Scanner](https://www.nstalker.com)
- [SoapUI (Web Service security testing)](https://www.soapui.org/security-testing/getting-started.html)
- [Netsparker](https://www.netsparker.com/web-vulnerability-scanner/)
- [SAINT](https://www.carson-saint.com)
- [QualysGuard WAS](https://www.qualys.com/apps/web-app-scanning/)
- [Fortify WebInspect](https://www.microfocus.com/en-us/solutions/application-security)

## Linux Distributions

- [Kali](https://www.kali.org)
- [Parrot](https://www.parrotsec.org)
- [Samurai](https://github.com/SamuraiWTF/samuraiwtf)
- [Santoku](https://sourceforge.net/projects/santoku/)
- [BlackArch](https://blackarch.org/downloads.html)
- [PenToo](https://www.pentoo.ch)

## Source Code Analyzers

### Open Source / Freeware

- [Spotbugs](https://spotbugs.github.io)
- [Find Security Bugs](https://find-sec-bugs.github.io)
- [phpcs-security-audit](https://github.com/squizlabs/PHP_CodeSniffer)
- [PMD](https://pmd.github.io)
- [Microsoft's .NET Analyzers](https://docs.microsoft.com/en-us/visualstudio/code-quality/install-net-analyzers)
- [SonarQube](https://www.sonarqube.org)

### Commercial

- [Checkmarx CxSuite](https://www.checkmarx.com)
- [GrammaTech](https://www.grammatech.com)
- [ITS4](https://testarmy.com/en)
- [ParaSoft](https://www.parasoft.com)
- [Virtual Forge CodeProfiler for ABAP](https://www.virtualforge.com/de/codeprofiler-for-abap)
- [Veracode](https://www.veracode.com)
- [Peach Fuzzer](https://www.peach.tech)
- [Fortify SCA](https://www.microfocus.com/en-us/solutions/application-security)

## Browser Automation Tools

Browser Audomation tools are used to validate the functionality of web applications. Some follow a scripted approach and typically make use of a Unit Testing framework to construct test suites and test cases. Most, if not all, can be adapted to perform security specific tests in addition to functional tests.

### Open Source Tools

- [HtmlUnit](http://htmlunit.sourceforge.net)
  - A Java and JUnit based framework that uses the Apache HttpClient as the transport.
  - Very robust and configurable and is used as the engine for a number of other testing tools.
- [Selenium](https://www.selenium.dev)
  - JavaScript based testing framework, cross-platform and provides a GUI for creating tests.
