# Testing for Weak SSL TLS Ciphers Insufficient Transport Layer Protection

|ID          |
|------------|
|WSTG-CRYP-01|

## Summary

**TODO**

## Common Issues

Transport layer security related issues can be broadly split into the following areas:

### Server Configuration

There are a large number of protocol versions, ciphers and extensions supported by TLS. Many of these are considered to be legacy, and have cryptographic weaknesses, such as those listed below. Note that new weaknesses are likely to be identified over time, so this list may be incomplete.

* SSLv2 (DROWN)
* SSLv3 (POODLE)
* TLSv1.0 (BEAST)
* EXPORT ciphers
* NULL ciphers
* Anonymous ciphers (these may be supported on SMTP servers, as discussed in [RFC 7672](https://tools.ietf.org/html/rfc7672#section-8.2)
* RC4 ciphers (NOMORE)
* CBC mode ciphers (BEAST, Lucky 13)
* TLS compression (CRIME)
* Weak DHE keys (LOGJAM)

#### Exploitability

It should be emphasised that while many of these attacks have been demonstrated in a lab environment, they are not generally considered practical to exploit in the real world, as they require a (usually active) man-in-the-middle attack, and significant resources. As such, they are unlikely to be exploited by anyone other than nation states.

### Digital Certificates

#### Cryptographic Weaknesses

From a cryptographic perspective, there are two main areas that need to be reviewed on a digital certificate:

* The key strength should be *at least* 2048 bits.
* The signature algorithm should be *at least* SHA-256. Legacy algorithms such as MD5 and SHA-1 should not be used.

#### Validity

As well as being cryptographically secure, the certificate must also be considered valid (or trusted). This means that it must:

* Be within the defined validity period.
  * Any certificates issued after 1st September 2020 must not have a maximum lifespan of more than [398 days](https://blog.mozilla.org/security/2020/07/09/reducing-tls-certificate-lifespans-to-398-days/).
* Be signed by a trusted certificate authority (CA).
  * This should either be a trusted public CA for externally facing applications, or an internal CA for internal applications.
  * Don't flag internal applications as having untrusted certificates just because *your* system doesn't trust the CA.
* Have a Subject Alternate Name (SAN) that matches the hostname of the system.
  * The Common Name (CN) field is ignored by modern browsers, which only look at the SAN.
  * Make sure that you're accessing the system with the correct name (for example, if you access the host by IP then any certificate will be untrusted).

Some certificates may be issued for wildcard domains (such as `*.example.org`), meaning that they can be valid for multiple hostnames. Although convenient, there are a number of security concerns around this that should be considered. These are discussed in the [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html#carefully-consider-the-use-of-wildcard-certificates).

Certificates can also leak information about internal systems or domain names in the Issuer and SAN fields, which can be useful when trying to build up a picture of the internal network.

### Implementation Vulnerabilities

Over the years there have been vulnerabilities in the various TLS implementations. There are too many to list here, but some of the key ones are:

* [Debian OpenSSL Predictable Random Number Generator](https://www.debian.org/security/2008/dsa-1571) (CVE-2008-0166)
* [OpenSSL Insecure Renegotiation](https://www.openssl.org/news/secadv/20091111.txt) (CVE-2009-3555)
* [OpenSSL Heartbleed](https://heartbleed.com) (CVE-2014-0160)
* [F5 TLS POODLE](https://support.f5.com/csp/article/K15882) (CVE-2014-8730)
* [Microsoft Schannel Denial of Service](https://docs.microsoft.com/en-us/security-updates/securitybulletins/2014/ms14-066) (MS14-066 / CVE CVE-2014-6321)

### Client Certificates

* Certificates not tied to individual
* Certificates from a public CA
* Generating certs with matching Issuer and CN/SAN
* Header spoofing

### Application Vulnerabilities

* Sensitive traffic over HTTP (especially cookies)
* Redirecting from HTTP > HTTPS
* Mixed active content
* HSTS
* Secure flag on cookies

## How to Test

* Web browser
* OpenSSL
* Main scanning tools (Nessus, Nmap, SSL Labs, sslscan, sslyze, etc)
* STARTTLS

## References

* [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)

---

### Other Vulnerabilities

The presence of a new service, listening in a separate tcp port may introduce vulnerabilities such as infrastructure vulnerabilities if the [software is not up to date](../02-Configuration_and_Deployment_Management_Testing/01-Test_Network_Infrastructure_Configuration.md). Furthermore, for the correct protection of data during transmission the Session Cookie must use the [Secure flag](../06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md) and some directives should be sent to the browser to accept only secure traffic (e.g. [HSTS](../02-Configuration_and_Deployment_Management_Testing/07-Test_HTTP_Strict_Transport_Security.md), CSP).

Also there are some attacks that can be used to intercept traffic if the web server exposes the application on both [HTTP](../02-Configuration_and_Deployment_Management_Testing/07-Test_HTTP_Strict_Transport_Security.md) and [HTTPS](https://resources.enablesecurity.com/resources/Surf%20Jacking.pdf) or in case of mixed HTTP and HTTPS resources in the same page.

## How to Test

### Testing for Weak SSL/TLS Ciphers/Protocols/Keys Vulnerabilities

The large number of available cipher suites and quick progress in cryptanalysis makes testing an SSL server a non-trivial task.

At the time of writing these criteria are widely recognized as minimum checklist:

* Renegotiation must be properly configured (e.g. Insecure Renegotiation must be disabled, due to [MiTM attacks](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3555) and Client-initiated Renegotiation must be disabled, due to [Denial of Service vulnerability](https://community.qualys.com/blogs/securitylabs/2011/10/31/tls-renegotiation-and-denial-of-service-attacks)).
* [Keys must be generated with proper entropy](https://www.ssllabs.com/projects/rating-guide/index.html) (e.g, Weak Key Generated with Debian).

A more complete checklist includes:

* Secure Renegotiation should be enabled.
* Server should support [Forward Secrecy](https://community.qualys.com/blogs/securitylabs/2013/06/25/ssl-labs-deploying-forward-secrecy).

The following standards can be used as reference while assessing SSL servers:

* [PCI-DSS](https://www.pcisecuritystandards.org/security_standards/documents.php) requires compliant parties to use “strong cryptography” without precisely defining key lengths and algorithms. Common interpretation, partially based on previous versions of the standard, is that at least 128 bit key cipher, no export strength algorithms and no SSLv2 should be used.
* [Qualsys SSL Labs Server Rating Guide](https://www.ssllabs.com/projects/rating-guide/index.html), [Deployment best practice](https://www.ssllabs.com/projects/best-practices/index.html), and [SSL Threat Model](https://www.ssllabs.com/projects/ssl-threat-model/index.html) has been proposed to standardize SSL server assessment and configuration. But is less updated than the [SSL Server tool](https://www.ssllabs.com/ssltest/index.html).
* OWASP has a lot of resources about SSL/TLS Security:
  * [Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html).
  * [OWASP Top 10 2017 A3-Sensitive Data Exposure](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A3-Sensitive_Data_Exposure).
  * [OWASP ASVS * Verification V9](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x17-V9-Communications.md).
  * [OWASP Application Security FAQ * Cryptography/SSL](https://owasp.org/www-community/OWASP_Application_Security_FAQ#cryptographyssl).

Some tools and scanners both free (e.g. [SSLScan](https://sourceforge.net/projects/sslscan/)) and commercial (e.g. [Tenable Nessus](https://www.tenable.com/products/nessus)), can be used to assess SSL/TLS vulnerabilities. But due to evolution of these vulnerabilities a good way to test is to check them manually with [OpenSSL](https://www.openssl.org/) or use the tool’s output as an input for manual evaluation using the references.

Sometimes the SSL/TLS enabled service is not directly accessible and the tester can access it only via a HTTP proxy using [CONNECT method](https://tools.ietf.org/html/rfc2817). Most of the tools will try to connect to desired tcp port to start SSL/TLS handshake. This will not work since desired port is accessible only via HTTP proxy. The tester can easily circumvent this by using relaying software such as [socat](https://linux.die.net/man/1/socat).

### Testing for Other Vulnerabilities

As mentioned previously, there are other types of vulnerabilities that are not related with the SSL/TLS protocol used, the cipher suites or Certificates. Apart from other vulnerabilities discussed in other parts of this guide, a vulnerability exists when the server provides the website both with the HTTP and HTTPS protocols, and permits an attacker to force a victim into using a non-secure channel instead of a secure one.

#### Surf Jacking

The [Surf Jacking attack](https://resources.enablesecurity.com/resources/Surf%20Jacking.pdf) was first presented by Sandro Gauci and permits to an attacker to hijack an HTTP session even when the victim’s connection is encrypted using SSL or TLS.

The following is a scenario of how the attack can take place:

* Victim logs into the secure website at `https://somesecuresite/`.
* The secure site issues a session cookie as the client logs in.
* While logged in, the victim opens a new browser window and goes to `http://examplesite/`
* An attacker sitting on the same network is able to see the clear text traffic to `http://examplesite`.
* The attacker sends back a `301 Moved Permanently` in response to the clear text traffic to `http://examplesite`. The response contains the header `Location: http://somesecuresite/`, which makes it appear that examplesite is sending the web browser to somesecuresite. Notice that the URL scheme is HTTP not HTTPS.
* The victim's browser starts a new clear text connection to `http://somesecuresite/` and sends an HTTP request containing the cookie in the HTTP header in clear text
* The attacker sees this traffic and logs the cookie for later use.

To test if a website is vulnerable carry out the following tests:

1. Check if website supports both HTTP and HTTPS protocols
2. Check if cookies do not have the `Secure` flag

#### SSL Strip

Some applications supports both HTTP and HTTPS, either for usability or so users can type both addresses and get to the site. Often users go into an HTTPS website from link or a redirect. Typically personal banking sites have a similar configuration with an iframed log in or a form with action attribute over HTTPS but the page under HTTP.

An attacker in a privileged position * as described in [SSL strip](https://github.com/moxie0/sslstrip) * can intercept traffic when the user is in the HTTP site and manipulate it to get a Manipulator-In-The-Middle attack under HTTPS. An application is vulnerable if it supports both HTTP and HTTPS.

### Testing via HTTP Proxy

Inside corporate environments testers can see services that are not directly accessible and they can access them only via HTTP proxy using the [CONNECT method](https://tools.ietf.org/html/rfc2817). Most of the tools will not work in this scenario because they try to connect to the desired tcp port to start the SSL/TLS handshake. With the help of relaying software such as [socat](https://linux.die.net/man/1/socat) testers can enable those tools for use with services behind an HTTP proxy.

#### Example 1. Testing via HTTP Proxy

To connect to `destined.application.lan:443` via proxy `10.13.37.100:3128` run `socat` as follows:

`$ socat TCP-LISTEN:9999,reuseaddr,fork PROXY:10.13.37.100:destined.application.lan:443,proxyport=3128`

Then the tester can target all other tools to `localhost:9999`:

`$ openssl s_client -connect localhost:9999`

All connections to `localhost:9999` will be effectively relayed by socat via proxy to `destined.application.lan:443`.
