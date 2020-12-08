# Test for Subdomain Takeover

|ID          |
|------------|
|WSTG-CONF-10|

## Summary

A successful exploitation of this kind of vulnerability allows an adversary to claim and take control of the victim's subdomain. This attack relies on the following:

1. The victim's external DNS server subdomain record is configured to point to a non-existing or non-active resource/external service/endpoint. The proliferation of XaaS (Anything as a Service) products and public cloud services offer a lot of potential targets to consider.
2. The service provider hosting the resource/external service/endpoint does not handle subdomain ownership verification properly.

If the subdomain takeover is successful a wide variety of attacks are possible (serving malicious content, phising, stealing user session cookies, credentials, etc.). This vulnerability could be exploited for a wide variety of DNS resource records including: `A`, `CNAME`, `MX`, `NS`, `TXT` etc. In terms of the attack severity an `NS` subdomain takeover (although less likely) has the highest impact because a successful attack could result in full control over the whole DNS zone and  the victim's domain.

### GitHub

1. The victim (victim.com) uses GitHub for development and configured a DNS record (`coderepo.victim.com`) to access it.
2. The victim decides to migrate their code repository from GitHub to a commercial platform and does not remove `coderepo.victim.com` from their DNS server.
3. An adversary finds out that `coderepo.victim.com` is hosted on GitHub and uses GitHub Pages to claim `coderepo.victim.com` using their GitHub account.

### Expired Domain

1. The victim (victim.com) owns another domain (victimotherdomain.com) and uses a CNAME record (www) to reference the other domain (`www.victim.com` --> `victimotherdomain.com`)
2. At some point, victimotherdomain.com expires and is available for registration by anyone. Since the CNAME record is not deleted from the victim.com DNS zone, anyone who registers `victimotherdomain.com` has full control over `www.victim.com` until the DNS record is present.

## Test Objectives

- Enumerate all possible domains (previous and current).
- Identify forgotten or misconfigured domains.

## How to Test

### Black-Box Testing

The first step is to enumerate the victim DNS servers and resource records. There are multiple ways to accomplish this task, for example DNS enumeration using a list of common subdomains dictionary, DNS brute force or using web search engines and other OSINT data sources.

Using the dig command the tester looks for the following DNS server response messages that warrant further investigation:

- `NXDOMAIN`
- `SERVFAIL`
- `REFUSED`
- `no servers could be reached.`

#### Testing DNS A, CNAME Record Subdomain Takeover

Perform a basic DNS enumeration on the victim's domain (`victim.com`) using `dnsrecon`:

```bash
$ ./dnsrecon.py -d victim.com
[*] Performing General Enumeration of Domain: victim.com
...
[-] DNSSEC is not configured for victim.com
[*]      A subdomain.victim.com 192.30.252.153
[*]      CNAME subdomain1.victim.com fictioussubdomain.victim.com
...
```

Identify which DNS resource records are dead and point to inactive/not-used services. Using the dig command for the `CNAME` record:

```bash
$ dig CNAME fictioussubdomain.victim.com
; <<>> DiG 9.10.3-P4-Ubuntu <<>> ns victim.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 42950
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1
```

The following DNS responses warrant further investigation: `NXDOMAIN`.

To test the `A` record the tester performs a whois database lookup and identifies GitHub as the service provider:

```bash
$ whois 192.30.252.153 | grep "OrgName"
OrgName: GitHub, Inc.
```

The tester visits `subdomain.victim.com` or issues a HTTP GET request which returns a "404 - File not found" response which is a clear indication of the vulnerability.

![GitHub 404 File Not Found response](images/subdomain_takeover_ex1.jpeg)\
*Figure 4.2.10-1: GitHub 404 File Not Found response*

The tester claims the domain using GitHub Pages:

![GitHub claim domain](images/subdomain_takeover_ex2.jpeg)\
*Figure 4.2.10-2: GitHub claim domain*

#### Testing NS Record Subdomain Takeover

Identify all nameservers for the domain in scope:

```bash
$ dig ns victim.com +short
ns1.victim.com
nameserver.expireddomain.com
```

In this fictious example the tester checks if the domain `expireddomain.com` is active with a domain registrar search. If the domain is available for purchase the subdomain is vulnerable.

The following DNS responses warrant further investigation: `SERVFAIL` or `REFUSED`.

### Gray-Box Testing

The tester has the DNS zone file available which means DNS enumeration is not necessary. The testing methodology is the same.

## Remediation

To mitigate the risk of subdomain takeover the vulnerable DNS resource record(s) should be removed from the DNS zone. Continous monitoring and periodic checks are recommended as best practice.

## Tools

- [dig - man page](https://linux.die.net/man/1/dig)
- [recon-ng - Web Reconnaissance framework](https://github.com/lanmaster53/recon-ng)
- [theHarvester - OSINT intelligence gathering tool](https://github.com/laramies/theHarvester)
- [Sublist3r - OSINT subdomain enumeration tool](https://github.com/aboul3la/Sublist3r)
- [dnsrecon - DNS Enumeration Script](https://github.com/darkoperator/dnsrecon)
- [OWASP Amass DNS enumeration](https://github.com/OWASP/Amass)

## References

- [HackerOne - A Guide To Subdomain Takeovers](https://www.hackerone.com/blog/Guide-Subdomain-Takeovers)
- [Subdomain Takeover: Basics](https://0xpatrik.com/subdomain-takeover-basics/)
- [Subdomain Takeover: Going beyond CNAME](https://0xpatrik.com/subdomain-takeover-ns/)
- [can-i-take-over-xyz - A list of vulnerable services](https://github.com/EdOverflow/can-i-take-over-xyz/)
- [OWASP AppSec Europe 2017 - Frans Rosén: DNS hijacking using cloud providers – no verification needed](https://2017.appsec.eu/presos/Developer/DNS%20hijacking%20using%20cloud%20providers%20%E2%80%93%20no%20verification%20needed%20-%20Frans%20Rosen%20-%20OWASP_AppSec-Eu_2017.pdf)
