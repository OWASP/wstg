# Testing Tools Resource

## General Testing

- [OWASP ZAP](https://www.zaproxy.org)
  - The Zed Attack Proxy (ZAP) is an easy to use integrated penetration testing tool for finding vulnerabilities in web applications. It is designed to be used by people with a wide range of security experience and as such is ideal for developers and functional testers who are new to penetration testing.
  - ZAP provides automated scanners as well as a set of tools that allow you to find security vulnerabilities manually.
- [Burp Proxy](https://www.portswigger.net/Burp/)
  - Burp Proxy is an intercepting proxy server for security testing of web applications it allows Intercepting and modifying all HTTP(S) traffic passing in both directions, it can work with custom SSL certificates and non-proxy-aware clients.
- [Webstretch Proxy](https://sourceforge.net/projects/webstretch)
  - Webstretch Proxy enable users to view and alter all aspects of communications with a web site via a proxy. It can also be used for debugging during development.
- [Firefox HTTP Header Live](https://addons.mozilla.org/en-US/firefox/addon/http-header-live)
  - View HTTP headers of a page and while browsing.
- [Firefox Tamper Data](https://addons.mozilla.org/en-US/firefox/addon/tamper-data-for-ff-quantum/)
  - Use tamperdata to view and modify HTTP/HTTPS headers and post parameters
- [Firefox Web Developer Tools](https://addons.mozilla.org/en-US/firefox/addon/web-developer/)
  - The Web Developer extension adds various web developer tools to the browser.
- [DOM Inspector](https://developer.mozilla.org/en/docs/DOM_Inspector)
  - DOM Inspector is a developer tool used to inspect, browse, and edit the Document Object Model (DOM)
- [Grendel-Scan](https://sourceforge.net/projects/grendel/)
  - Grendel-Scan is an automated security scanning of web applications and also supports manual penetration testing.
  - SWFIntruder (pronounced Swiff Intruder) is the first tool specifically developed for analyzing and testing security of Flash applications at runtime.
- [w3af](https://w3af.org)
  - w3af is a Web Application Attack and Audit Framework. The project’s goal is finding and exploiting web application vulnerabilities.
- [skipfish](https://code.google.com/p/skipfish/)
  - Skipfish is an active web application security reconnaissance tool.
- [Web Developer toolbar](https://chrome.google.com/webstore/detail/bfbameneiokkgbdmiekhjnmfkcnldhhm)
  - The Web Developer extension adds a toolbar button to the browser with various web developer tools. This is the official port of the Web Developer extension for Firefox.
- [HTTP Request Maker](https://chrome.google.com/webstore/detail/kajfghlhfkcocafkcjlajldicbikpgnp?hl=en-US)
  - Request Maker is a tool for penetration testing. With it you can easily capture requests made by web pages, tamper with the URL, headers and POST data and, of course, make new requests
- [Cookie Editor](https://chrome.google.com/webstore/detail/fngmhnnpilhplaeedifhccceomclgfbg?hl=en-US)
  - Edit This Cookie is a cookie manager. You can add, delete, edit, search, protect and block cookies
- [Cookie swap](https://chrome.google.com/webstore/detail/dffhipnliikkblkhpjapbecpmoilcama?hl=en-US)
  - Swap My Cookies is a session manager, it manages cookies, letting you login on any website with several different accounts.
- [Session Manager](https://chrome.google.com/webstore/detail/session-manager/mghenlmbmjcpehccoangkdpagbcbkdpc)
  - With Session Manager you can quickly save your current browser state and reload it whenever necessary. You can manage multiple sessions, rename or remove them from the session library. Each session remembers the state of the browser at its creation time, i.e the opened tabs and windows.
- [Subgraph Vega](https://subgraph.com/vega/)
  - Vega is a free and open source scanner and testing platform to test the security of web applications. Vega can help you find and validate SQL Injection, Cross-Site Scripting (XSS), inadvertently disclosed sensitive information, and other vulnerabilities. It is written in Java, GUI based, and runs on Linux, OS X, and Windows.

### Testing for Specific Vulnerabilities

#### Testing for JavaScript Security, DOM XSS

- [BlueClosure BC Detect](https://www.blueclosure.com)

#### Testing for SQL Injection

- [Sqlninja: a SQL Server Injection & Takeover Tool](https://sourceforge.net/projects/sqlninja/)
- [Bernardo Damele A. G.: sqlmap, automatic SQL injection tool](http://sqlmap.org/)
- [Absinthe 1.1 (formerly SQLSqueal)](https://sourceforge.net/projects/absinthe/)
- [SQLInjector - Uses inference techniques to extract data and determine the backend database server](https://github.com/p4pentest/SQLInjector)
- [Bsqlbf-v2: A perl script allows extraction of data from Blind SQL Injections](https://code.google.com/p/bsqlbf-v2/)
- [Pangolin: An automatic SQL injection penetration testing tool](https://www.darknet.org.uk/2009/05/pangolin-automatic-sql-injection-tool/)
- [Multiple DBMS Sql Injection tool - SQL Power Injector](http://www.sqlpowerinjector.com/)

#### Testing Oracle

- [Toad for Oracle](https://www.quest.com/toad)

#### Testing SSL

- [O-Saft](https://github.com/OWASP/O-Saft)
- [sslyze](https://github.com/iSECPartners/sslyze)
- [TestSSLServer](https://www.bolet.org/TestSSLServer/)
- [SSLScan](https://sourceforge.net/projects/sslscan/)
- [SSLScan windows](https://github.com/rbsec/sslscan/releases)
- [SSLLabs](https://www.ssllabs.com/ssltest/)

#### Testing for Brute Force Password

- [THC Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [John the Ripper](https://www.openwall.com/john/)
- [Medusa](https://github.com/jmk-foofus/medusa)
- [Ncat](https://nmap.org/ncat/)
- [HashCat](https://hashcat.net/hashcat/#features-algos)
- [fgdump](http://foofus.net/goons/fizzgig/fgdump/)
- [Password Dictionary](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm)

#### Testing Buffer Overflow

- [OllyDbg](http://www.ollydbg.de)
  - “A windows based debugger used for analyzing buffer overflow vulnerabilities”
- [Spike](https://www.immunitysec.com/downloads/SPIKE2.9.tgz)
  - A fuzzer framework that can be used to explore vulnerabilities and perform length testing
- [Brute Force Binary Tester (BFB)](https://sourceforge.net/projects/bfbtester/)
  - A proactive binary checker
- [Metasploit](https://www.metasploit.com/)
  - A rapid exploit development and Testing frame work

#### Fuzzer

- [Wfuzz](http://www.darknet.org.uk/2007/07/wfuzz-a-tool-for-bruteforcingfuzzing-web-applications/)

#### Googling

- [Bishop Fox's Google Hacking Diggity Project](https://resources.bishopfox.com/resources/tools/google-hacking-diggity/)
- [Google Hacking database](https://www.exploit-db.com/google-hacking-database/)

#### Slow HTTP

- [Slowloris](https://github.com/gkbrk/slowloris)
- [slowhttptest](https://github.com/shekyan/slowhttptest)

## Commercial Black-Box Testing Tools

- [NGS Typhon](https://www.nccgroup.trust/uk/our-services/cyber-security/technology-solutions/)
- [IBM AppScan](https://www.ibm.com/hk-en/security/application-security/appscan)
- [Burp Intruder](https://portswigger.net/burp)
- [Acunetix Web Vulnerability Scanner](https://www.acunetix.com)
- [MaxPatrol Security Scanner](https://www.ptsecurity.com/ww-en/products/maxpatrol/)
- [Parasoft SOAtest (more QA-type tool)](https://www.parasoft.com/products/soatest)
- [N-Stalker Web Application Security Scanner](https://www.nstalker.com)
- [SoapUI (Web Service security testing)](https://www.soapui.org/security-testing/getting-started.html)
- [Netsparker](https://www.netsparker.com/web-vulnerability-scanner/)
- [SAINT](https://www.carson-saint.com/)
- [QualysGuard WAS](https://www.qualys.com/apps/web-app-scanning/)
- [IndusGuard Web](https://www.indusface.com/products/application-security/web-application-scanning/)

### Linux Distrubtion

- [PenTestBox](https://pentestbox.org/)
- [Samurai](https://sourceforge.net/p/samurai/wiki/Home/)
- [Santoku](https://sourceforge.net/projects/santoku/)
- [ParrotSecurity](https://www.parrotsec.org/)
- [Kali](https://www.kali.org/)
- [Matriux](https://sourceforge.net/projects/matriux/?source=navbar)
- [BlackArch](https://blackarch.org/downloads.html)
- [PenToo](https://www.pentoo.ch/download/)

## Source Code Analyzers

### Open Source / Freeware

- [Spotbugs](https://spotbugs.github.io/)
- [Find Security Bugs](https://find-sec-bugs.github.io/)
- [FlawFinder](https://dwheeler.com/flawfinder/)
- [phpcs-security-audit](https://github.com/squizlabs/PHP_CodeSniffer)
- [PMD](https://pmd.github.io/)
- [Microsoft’s FxCop](https://docs.microsoft.com/en-us/visualstudio/code-quality/install-fxcop-analyzers?view=vs-2019)
- [Oedipus](https://www.darknet.org.uk/2006/06/oedipus-open-source-web-application-security-analysis/)
- [Splint](https://splint.org/)
- [SonarQube](https://www.sonarqube.org/)
- [W3af](https://w3af.org/)

### Commercial

- [Checkmarx CxSuite](https://www.checkmarx.com/)
- [GrammaTech](https://www.grammatech.com/)
- [ITS4](https://testarmy.com/en/)
- [ParaSoft](https://www.parasoft.com/)
- [Virtual Forge CodeProfiler for ABAP](https://www.virtualforge.com/de/codeprofiler-for-abap)
- [Veracode](https://www.veracode.com/)
- [Peach Fuzzer](https://www.peach.tech/)
- [Burp Suite](https://portswigger.net/burp/)

## Acceptance Testing Tools

Acceptance testing tools are used to validate the functionality of web applications. Some follow a scripted approach and typically make use of a Unit Testing framework to construct test suites and test cases. Most, if not all, can be adapted to perform security specific tests in addition to functional tests.

- [BDD Security](https://github.com/continuumsecurity/bdd-security)

### Open Source Tools

- [HtmlUnit](http://htmlunit.sourceforge.net)
  - A Java and JUnit based framework that uses the Apache HttpClient as the transport.
  - Very robust and configurable and is used as the engine for a number of other testing tools.
- [jWebUnit](https://jwebunit.github.io/jwebunit/)
  - A Java based meta-framework that uses htmlunit or selenium as the testing engine.
- [HttpUnit](http://httpunit.sourceforge.net)
  - One of the first web testing frameworks, suffers from using the native JDK provided HTTP transport, which can be a bit limiting for security testing.
- [Solex](http://solex.sourceforge.net)
  - An Eclipse plugin that provides a graphical tool to record HTTP sessions and make assertions based on the results.
- [Selenium](https://www.seleniumhq.org/)
  - JavaScript based testing framework, cross-platform and provides a GUI for creating tests.
  - Mature and popular tool, but the use of JavaScript could hamper certain security tests.

## Other Tools

### Binary Analysis

- [BugScam IDC Package](https://sourceforge.net/projects/bugscam/)
- [Veracode](https://www.veracode.com)

### Site Mirroring

- [wget](https://www.gnu.org/software/wget/)
- [Wget for windows](http://gnuwin32.sourceforge.net/packages/wget.htm)
- [curl](https://curl.haxx.se/)
- [Xenu's Link Sleuth](http://home.snafu.de/tilman/xenulink.html)
