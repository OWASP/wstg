# Open Source Black Box Testing Tools

## General Testing

- [OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)
  - The Zed Attack Proxy (ZAP) is an easy to use integrated penetration testing tool for finding vulnerabilities in web applications. It is designed to be used by people with a wide range of security experience and as such is ideal for developers and functional testers who are new to penetration testing.
  - ZAP provides automated scanners as well as a set of tools that allow you to find security vulnerabilities manually.
- [OWASP WebScarab](https://www.owasp.org/index.php/OWASP_WebScarab_Project)
  - WebScarab is a framework for analysing applications that communicate using the HTTP and HTTPS protocols. It is written in Java, and is portable to many platforms. WebScarab has several modes of operation that are implemented by a number of plugins.
- [OWASP CAL9000](https://www.owasp.org/index.php/OWASP_CAL9000_Project)
  - CAL9000 is a collection of browser-based tools that enable more effective and efficient manual testing efforts.
  - Includes an XSS Attack Library, Character Encoder/Decoder, HTTP Request Generator and Response Evaluator, Testing Checklist, Automated Attack Editor and much more.
- [OWASP Pantera Web Assessment Studio Project](https://www.owasp.org/index.php/Category:OWASP_Pantera_Web_Assessment_Studio_Project)
  - Pantera uses an improved version of SpikeProxy to provide a powerful web application analysis engine. The primary goal of Pantera is to combine automated capabilities with complete manual testing to get the best penetration testing results.
- [OWASP Mantra - Security Framework](https://www.owasp.org/index.php/:OWASP_Mantra_-_Security_Framework)
  - Mantra is a web application security testing framework built on top of a browser. It supports Windows, Linux(both 32 and 64 bit) and Macintosh. In addition, it can work with other software like ZAP using built in proxy management function which makes it much more convenient. Mantra is available in 9 languages: Arabic, Chinese - Simplified, Chinese - Traditional, English, French, Portuguese, Russian, Spanish and Turkish.
- [Burp Proxy](http://www.portswigger.net/Burp/)
  - Burp Proxy is an intercepting proxy server for security testing of web applications it allows Intercepting and modifying all HTTP(S) traffic passing in both directions, it can work with custom SSL certificates and non-proxy-aware clients.
- [Webstretch Proxy](http://sourceforge.net/projects/webstretch)
  - Webstretch Proxy enable users to view and alter all aspects of communications with a web site via a proxy. It can also be used for debugging during development.
- [WATOBO](http://sourceforge.net/apps/mediawiki/watobo/index.php?title=Main_Page)
  - WATOBO works like a local proxy, similar to Webscarab, ZAP or BurpSuite and it supports passive and active checks.
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
- [OWASP SWFIntruder](https://www.owasp.org/index.php/Category:SWFIntruder)
  - SWFIntruder (pronounced Swiff Intruder) is the first tool specifically developed for analyzing and testing security of Flash applications at runtime.
- [w3af](http://w3af.org)
  - w3af is a Web Application Attack and Audit Framework. The project’s goal is finding and exploiting web application vulnerabilities.
- [skipfish](http://code.google.com/p/skipfish/)
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
- [Subgraph Vega](http://www.subgraph.com/products.html)
  - Vega is a free and open source scanner and testing platform to test the security of web applications. Vega can help you find and validate SQL Injection, Cross-Site Scripting (XSS), inadvertently disclosed sensitive information, and other vulnerabilities. It is written in Java, GUI based, and runs on Linux, OS X, and Windows.

### Testing for Specific Vulnerabilities

#### Testing for JavaScript Security, DOM XSS

- [BlueClosure BC Detect](http://www.blueclosure.com)

#### Testing AJAX

- [OWASP Sprajax Project](https://www.owasp.org/index.php/Category:OWASP_Sprajax_Project)

#### Testing for SQL Injection

- [OWASP SQLiX](https://www.owasp.org/index.php/Category:OWASP_SQLiX_Project)
- [Sqlninja: a SQL Server Injection & Takeover Tool](http://sqlninja.sourceforge.net)
- [Bernardo Damele A. G.: sqlmap, automatic SQL injection tool](http://sqlmap.org/)
- [Absinthe 1.1 (formerly SQLSqueal)](http://sourceforge.net/projects/absinthe/)
- [SQLInjector - Uses inference techniques to extract data and determine the backend database server](https://github.com/p4pentest/SQLInjector)
- [Bsqlbf-v2: A perl script allows extraction of data from Blind SQL Injections](http://code.google.com/p/bsqlbf-v2/)
- [Pangolin: An automatic SQL injection penetration testing tool](http://www.darknet.org.uk/2009/05/pangolin-automatic-sql-injection-tool/)
- [Multiple DBMS Sql Injection tool - SQL Power Injector](http://www.sqlpowerinjector.com/)
- [MySql Blind Injection Bruteforcing, Reversing.org - sqlbftools](http://packetstormsecurity.org/files/43795/sqlbftools-1.2.tar.gz.html)

#### Testing Oracle

- [Toad for Oracle](http://www.quest.com/toad)

#### Testing SSL

- [O-Saft](https://www.owasp.org/index.php/O-Saft)
- [sslyze](https://github.com/iSECPartners/sslyze)
- [TestSSLServer](http://www.bolet.org/TestSSLServer/)
- [SSLScan](http://sourceforge.net/projects/sslscan/)
- [SSLScan windows](https://github.com/rbsec/sslscan/releases)
- [SSLLabs](https://www.ssllabs.com/ssltest/)

#### Testing for Brute Force Password

- [THC Hydra](https://github.com/vanhauser-thc/thc-hydra)
- [John the Ripper](http://www.openwall.com/john/)
- [Brutus](http://www.hoobie.net/brutus/)
- [Medusa](http://www.foofus.net/~jmk/medusa/medusa.html)
- [Ncat](http://nmap.org/ncat/)
- [HashCat](http://hashcat.net/hashcat/#features-algos)
- [fgdump](http://foofus.net/goons/fizzgig/fgdump/)
- [Password Dictionary](https://crackstation.net/buy-crackstation-wordlist-password-cracking-dictionary.htm)

#### Testing Buffer Overflow

- [OllyDbg](http://www.ollydbg.de)
  - “A windows based debugger used for analyzing buffer overflow vulnerabilities”
- [Spike](http://www.immunitysec.com/downloads/SPIKE2.9.tgz)
  - A fuzzer framework that can be used to explore vulnerabilities and perform length testing
- [Brute Force Binary Tester (BFB)](http://bfbtester.sourceforge.net)
  - A proactive binary checker
- [Metasploit](http://www.metasploit.com/)
  - A rapid exploit development and Testing frame work

#### Fuzzer

- [OWASP WSFuzzer](https://www.owasp.org/index.php/Category:OWASP_WSFuzzer_Project)
- [Wfuzz](http://www.darknet.org.uk/2007/07/wfuzz-a-tool-for-bruteforcingfuzzing-web-applications/)

#### Googling

- [Bishop Fox's Google Hacking Diggity Project](http://www.bishopfox.com/resources/tools/google-hacking-diggity/)
- [Google Hacking database](https://www.exploit-db.com/google-hacking-database/)

#### Slow HTTP

- [Slowloris](https://github.com/gkbrk/slowloris)
- [slowhttptest](https://github.com/shekyan/slowhttptest)

## Commercial Black Box Testing Tools

- [NGS Typhon](https://www.nccgroup.trust/uk/our-services/security-consulting/information-security-software/?utm_medium=rd0517)
- [IBM AppScan](https://www.ibm.com/hk-en/security/application-security/appscan)
- [Burp Intruder](http://www.portswigger.net/burp/intruder.html)
- [Acunetix Web Vulnerability Scanner](http://www.acunetix.com)
- [Sleuth](http://www.sandsprite.com/tools.php?id=-1)
- [MaxPatrol Security Scanner](https://www.ptsecurity.com/ww-en/products/maxpatrol/)
- [Parasoft SOAtest (more QA-type tool)](http://www.parasoft.com/jsp/products/soatest.jsp?itemId=101)
- [N-Stalker Web Application Security Scanner](http://www.nstalker.com)
- [SoapUI (Web Service security testing)](http://www.soapui.org/Security/getting-started.html)
- [Netsparker](http://www.mavitunasecurity.com/netsparker/)
- [SAINT](http://www.saintcorporation.com/)
- [QualysGuard WAS](http://www.qualys.com/enterprises/qualysguard/web-application-scanning/)
- [IndusGuard Web](https://www.indusface.com/index.php/products/indusguard-web)

### Linux Distrubtion

- [PenTestBox](https://tools.pentestbox.com/)
- [Samurai](https://sourceforge.net/p/samurai/wiki/Home/)
- [Santoku](https://sourceforge.net/projects/santoku/)
- [ParrotSecurity](https://www.parrotsec.org/)
- [Kali](https://www.kali.org/)
- [Matriux](https://sourceforge.net/projects/matriux/?source=navbar)
- [BlackArch](http://www.blackarch.org/downloads.html)
- [PenToo](http://www.pentoo.ch/download/)
- [bugtraq](http://bugtraq-team.com/)

## Source Code Analyzers

### Open Source / Freeware

- [Owasp Orizon](https://www.owasp.org/index.php/Category:OWASP_Orizon_Project)
- [OWASP LAPSE](https://www.owasp.org/index.php/Category:OWASP_LAPSE_Project)
- [OWASP O2 Platform](https://www.owasp.org/index.php/OWASP_O2_Platform)
- [OWASP WAP-Web Application Protection](https://www.owasp.org/index.php/OWASP_WAP-Web_Application_Protection)
- [FindBugs](http://findbugs.sourceforge.net)
- [Find Security Bugs](http://h3xstream.github.io/find-sec-bugs/)
- [FlawFinder](http://www.dwheeler.com/flawfinder)
- [phpcs-security-audit](https://github.com/squizlabs/PHP_CodeSniffer)
- [PMD](http://pmd.sourceforge.net/)
- [Microsoft’s FxCop](https://www.owasp.org/index.php/FxCop)
- [Oedipus](http://www.darknet.org.uk/2006/06/oedipus-open-source-web-application-security-analysis/)
- [Splint](http://splint.org)
- [SonarQube](http://sonarqube.org)
- [W3af](http://w3af.sourceforge.net/)

### Commercial

- [Checkmarx CxSuite](http://www.checkmarx.com)
- [GrammaTech](http://www.grammatech.com)
- [ITS4](http://seclab.cs.ucdavis.edu/projects/testing/tools/its4.html)
- [ParaSoft](http://www.parasoft.com)
- [Virtual Forge CodeProfiler for ABAP](https://www.virtualforge.com/de/codeprofiler-for-abap)
- [Veracode](http://www.veracode.com)
- [Peach Fuzzer](http://www.peachfuzzer.com/)
- [Burp Suite](https://portswigger.net/burp/)

## Acceptance Testing Tools

Acceptance testing tools are used to validate the functionality of web applications. Some follow a scripted approach and typically make use of a Unit Testing framework to construct test suites and test cases. Most, if not all, can be adapted to perform security specific tests in addition to functional tests.

- [BDD Security](https://github.com/continuumsecurity/bdd-security)

### Open Source Tools

- [HtmlUnit](http://htmlunit.sourceforge.net)
  - A Java and JUnit based framework that uses the Apache HttpClient as the transport.
  - Very robust and configurable and is used as the engine for a number of other testing tools.
- [jWebUnit](http://jwebunit.sourceforge.net)
  - A Java based meta-framework that uses htmlunit or selenium as the testing engine.
- [HttpUnit](http://httpunit.sourceforge.net)
  - One of the first web testing frameworks, suffers from using the native JDK provided HTTP transport, which can be a bit limiting for security testing.
- [Solex](http://solex.sourceforge.net)
  - An Eclipse plugin that provides a graphical tool to record HTTP sessions and make assertions based on the results.
- [Selenium](http://seleniumhq.org/)
  - JavaScript based testing framework, cross-platform and provides a GUI for creating tests.
  - Mature and popular tool, but the use of JavaScript could hamper certain security tests.

## Other Tools

### Binary Analysis

- [BugScam IDC Package](http://sourceforge.net/projects/bugscam)
- [Veracode](http://www.veracode.com)

### Site Mirroring

- [wget](http://www.gnu.org/software/wget)
- [Wget for windows](http://www.interlog.com/~tcharron/wgetwin.html)
- [curl](http://curl.haxx.se)
- [Xenu's Link Sleuth](http://home.snafu.de/tilman/xenulink.html)
