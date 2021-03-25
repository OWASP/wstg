# Testing for Weak Transport Layer Security

|ID          |
|------------|
|WSTG-CRYP-01|

## Summary

When information is sent between the client and the server, it must be encrypted and protected in order to prevent an attacker from being able to read or modify it. This is most commonly done using HTTPS, which uses the [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security) protocol, a replacement for the older Secure Socket Layer (SSL) protocol. TLS also provides a way for the server to demonstrate to the client that they have connected to the correct server, by presenting a trusted digital certificate.

Over the years there have been a large number of cryptographic weaknesses identified in the SSL and TLS protocols, as well as in the ciphers that they use. Additionally, many of the implementations of these protocols have also had serious vulnerabilities. As such, it is important to test that sites are not only implementing TLS, but that they are doing so in a secure manner.

## Test Objectives

- Validate the service configuration.
- Review the digital certificate's cryptographic strength and validity.
- Ensure that the TLS security is not bypassable and is properly implemented across the application.

## How to Test

Transport layer security related issues can be broadly split into the following areas:

### Server Configuration

There are a large number of protocol versions, ciphers, and extensions supported by TLS. Many of these are considered to be legacy, and have cryptographic weaknesses, such as those listed below. Note that new weaknesses are likely to be identified over time, so this list may be incomplete.

- [SSLv2 (DROWN)](https://drownattack.com/)
- [SSLv3 (POODLE)](https://en.wikipedia.org/wiki/POODLE)
- [TLSv1.0 (BEAST)](https://www.acunetix.com/blog/web-security-zone/what-is-beast-attack/)
- [TLSv1.1 (Deprecated by RFC 8996)](https://tools.ietf.org/html/rfc8996)
- [EXPORT ciphers suites (FREAK)](https://en.wikipedia.org/wiki/FREAK)
- [NULL ciphers](https://www.rapid7.com/db/vulnerabilities/ssl-null-ciphers) ([they only provide authentication](https://tools.ietf.org/html/rfc4785)).
- Anonymous ciphers (these may be supported on SMTP servers, as discussed in [RFC 7672](https://tools.ietf.org/html/rfc7672#section-8.2))
- [RC4 ciphers (NOMORE)](https://www.rc4nomore.com/)
- CBC mode ciphers (BEAST, [Lucky 13](https://en.wikipedia.org/wiki/Lucky_Thirteen_attack))
- [TLS compression (CRIME)](https://en.wikipedia.org/wiki/CRIME)
- [Weak DHE keys (LOGJAM)](https://weakdh.org/)

The [Mozilla Server Side TLS Guide](https://wiki.mozilla.org/Security/Server_Side_TLS) details the protocols and ciphers that are currently recommended.

#### Exploitability

It should be emphasised that while many of these attacks have been demonstrated in a lab environment, they are not generally considered practical to exploit in the real world, as they require a (usually active) MitM attack, and significant resources. As such, they are unlikely to be exploited by anyone other than nation states.

### Digital Certificates

#### Cryptographic Weaknesses

From a cryptographic perspective, there are two main areas that need to be reviewed on a digital certificate:

- The key strength should be *at least* 2048 bits.
- The signature algorithm should be *at least* SHA-256. Legacy algorithms such as MD5 and SHA-1 should not be used.

#### Validity

As well as being cryptographically secure, the certificate must also be considered valid (or trusted). This means that it must:

- Be within the defined validity period.
    - Any certificates issued after 1st September 2020 must not have a maximum lifespan of more than [398 days](https://blog.mozilla.org/security/2020/07/09/reducing-tls-certificate-lifespans-to-398-days/).
- Be signed by a trusted certificate authority (CA).
    - This should either be a trusted public CA for externally facing applications, or an internal CA for internal applications.
    - Don't flag internal applications as having untrusted certificates just because *your* system doesn't trust the CA.
- Have a Subject Alternate Name (SAN) that matches the hostname of the system.
    - The Common Name (CN) field is ignored by modern browsers, which only look at the SAN.
    - Make sure that you're accessing the system with the correct name (for example, if you access the host by IP then any certificate will be appear untrusted).

Some certificates may be issued for wildcard domains (such as `*.example.org`), meaning that they can be valid for multiple subdomains. Although convenient, there are a number of security concerns around this that should be considered. These are discussed in the [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html#carefully-consider-the-use-of-wildcard-certificates).

Certificates can also leak information about internal systems or domain names in the Issuer and SAN fields, which can be useful when trying to build up a picture of the internal network or conduct social engineering activities.

### Implementation Vulnerabilities

Over the years there have been vulnerabilities in the various TLS implementations. There are too many to list here, but some of the key examples are:

- [Debian OpenSSL Predictable Random Number Generator](https://www.debian.org/security/2008/dsa-1571) (CVE-2008-0166)
- [OpenSSL Insecure Renegotiation](https://www.openssl.org/news/secadv/20091111.txt) (CVE-2009-3555)
- [OpenSSL Heartbleed](https://heartbleed.com) (CVE-2014-0160)
- [F5 TLS POODLE](https://support.f5.com/csp/article/K15882) (CVE-2014-8730)
- [Microsoft Schannel Denial of Service](https://docs.microsoft.com/en-us/security-updates/securitybulletins/2014/ms14-066) (MS14-066 / CVE CVE-2014-6321)

### Application Vulnerabilities

As well as the underlying TLS configuration being securely configured, the application also needs to use it in a secure way. Some of these points are addressed elsewhere in this guide:

- [Not sending sensitive data over unencrypted channels (WSTG-CRYP-03)](03-Testing_for_Sensitive_Information_Sent_via_Unencrypted_Channels.md)
- [Setting the HTTP Strict-Transport-Security header (WSTG-CONF-07)](../02-Configuration_and_Deployment_Management_Testing/07-Test_HTTP_Strict_Transport_Security.md)
- [Setting the Secure flag on cookies (WSTG-SESS-02)](../06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md)

#### Mixed Active Content

Mixed active content is when active resources (such as scripts to CSS) are loaded over unencrypted HTTP and included into a secure (HTTPS) page. This is dangerous because it would allow an attacker to modify these files (as they are sent unencrypted), which could allow them to execute arbitrary code (JavaScript or CSS) in the page. Passive content (such as images) loaded over an insecure connection can also leak information or allow an attacker to deface the page, although it is less likely to lead to a full compromise.

> Note: modern browsers will block active content being loaded from insecure sources into secure pages.

#### Redirecting from HTTP to HTTPS

Many sites will accept connections over unencrypted HTTP, and then immediately redirect the user to the secure (HTTPS) version of the site with a `301 Moved Permanently` redirect. The HTTPS version of the site then sets the `Strict-Transport-Security` header to instruct the browser to always use HTTPS in future.

However, if an attacker is able to intercept this initial request, they could redirect the user to a malicious site, or use a tool such as [sslstrip](https://github.com/moxie0/sslstrip) to intercept subsequent requests.

In order to defend against this type of attack, the site must use be added to the [preload list](https://hstspreload.org).

## Automated Testing

There are a large number of scanning tools that can be used to identify weaknesses in the SSL/TLS configuration of a service, including both dedicated tools and general purpose vulnerability scanners. Some of the more popular ones are:

- [Nmap](https://nmap.org) (various scripts)
- [OWASP O-Saft](https://owasp.org/www-project-o-saft/)
- [sslscan](https://github.com/rbsec/sslscan)
- [sslyze](https://github.com/nabla-c0d3/sslyze)
- [SSL Labs](https://www.ssllabs.com/ssltest/)
- [testssl.sh](https://github.com/drwetter/testssl.sh)

### Manual Testing

It is also possible to carry out most checks manually, using command-line looks such as `openssl s_client` or `gnutls-cli` to connect with specific protocols, ciphers or options.

When testing like this, be aware that the version of OpenSSL or GnuTLS shipped with most modern systems may will not support some outdated and insecure protocols such as SSLv2 or EXPORT ciphers. Make sure that your version supports the outdated versions before using it for testing, or you'll end up with false negatives.

It can also be possible to performed limited testing using a web browser, as modern browsers will provide details of the protocols and ciphers that are being used in their developer tools. They also provide an easy way to test whether a certificate is considered trusted, by browsing to the service and seeing if you are presented with a certificate warning.

## References

- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [Mozilla Server Side TLS Guide](https://wiki.mozilla.org/Security/Server_Side_TLS)
