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
    - Fiddler is an intercepting web proxy that is primarily aimed at developers rather than penetration testers, but still provides useful functionality. It also hooks directly into the Windows HTTP APIs, allowing it to intercept traffic from some software that doesn't allow custom proxies to be set.

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
- [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
    - A powerful and easy to use browser extension that allows you to quickly create, edit and delete cookies for the current tab. Useful for developing, testing, or manually managing cookies.

### Testing for Specific Vulnerabilities

#### Testing for SQL Injection

- [sqlmap](https://sqlmap.org)

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
- [wget for windows](https://gnuwin32.sourceforge.net/packages/wget.htm)
- [cURL](https://curl.haxx.se)

### Content Discovery

- [Gobuster](https://github.com/OJ/gobuster)
- [Waybackurls](https://github.com/tomnomnom/waybackurls)
    - Waybackurls fetches all URLs known to the Wayback Machine for a given domain, useful for reconnaissance.
    - **Usage:**

```bash
waybackurls example.com
```

- [GAU (Get All URLs)](https://github.com/lc/gau)
    - GAU collects URLs from multiple public archives, including the Wayback Machine and Common Crawl.
    - **Usage:**

```bash
gau example.com
```

- [Unfurl](https://github.com/tomnomnom/unfurl)
    - Unfurl extracts subdomains, paths, and parameters from URLs for deeper analysis.
    - **Usage:**

```bash
unfurl "https://example.com/page?query=123"
```

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

- [HtmlUnit](https://htmlunit.sourceforge.io) - HtmlUnit is a GUI-less browser for Java programs. It models HTML documents and provides an API to invoke pages, fill out forms, click links, and interact with JavaScript and complex AJAX libraries. It can simulate Chrome, Firefox, or Edge depending on configuration, and is typically used for automated testing or web scraping. HtmlUnit can also be used as a Selenium-compatible browser via the [htmlunit-driver](https://github.com/SeleniumHQ/htmlunit-driver). The latest stable release is 4.21.0 (`org.htmlunit:htmlunit:4.21.0`).
    - GitHub Repository: [HtmlUnit/htmlunit](https://github.com/HtmlUnit/htmlunit)
- [Selenium](https://www.selenium.dev)
    - JavaScript based testing framework, cross-platform and provides a GUI for creating tests.

## Online Resources for Security Testing Tool Comparison

In addition to individual tools listed in this appendix, practitioners often need resources that help compare and evaluate security testing tools across categories such as SAST, DAST, SCA, and API security.

The following freely available resources provide curated comparisons and evaluation guidance.

### AppSec Santa Tool Comparison

- [AppSec Santa](https://appsecsanta.com)
    - A curated comparison of more than 160 application security tools across categories such as SAST, DAST, SCA, API Security, container security, and more.

### Security Headers Analyzer

- [SecurityHeaders](https://securityheaders.com)
    - A free online tool that analyzes HTTP response headers and highlights missing or misconfigured security protections such as Content Security Policy, HSTS, and X-Frame-Options.

### ZAP (Zed Attack Proxy) Documentation

Official documentation and learning resources for the ZAP (Zed Attack Proxy) dynamic application security testing tool.

- [ZAP Documentation](https://www.zaproxy.org/docs/)

### Nuclei Templates Project

A large open-source repository of vulnerability detection templates used for automated security scanning.

- [Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates)
