# Test for Subdomain Takeover

|ID          |
|------------|
|WSTG-CONF-10|

## Summary

A successful exploitation of this kind of vulnerability allows an adversary to claim and take control of the victim's subdomain. This attack relies on the following:

1. The victim's external DNS server subdomain record is configured to point to a non-existing or non-active resource/external service/endpoint. The proliferation of XaaS (Anything as a Service) products and public cloud services offer a lot of potential targets to consider.
2. The service provider hosting the resource/external service/endpoint does not handle subdomain ownership verification properly.

If the subdomain takeover is successful, a wide variety of attacks are possible (serving malicious content, phishing, stealing user session cookies, credentials, etc.). This vulnerability could be exploited for a wide variety of DNS resource records including: `A`, `CNAME`, `MX`, `NS`, `TXT` etc. In terms of the attack severity, an `NS` subdomain takeover (although less likely) has the highest impact, because a successful attack could result in full control over the whole DNS zone and the victim's domain.

### GitHub

1. The victim (victim.com) uses GitHub for development and configured a DNS record (`coderepo.victim.com`) to access it.
2. The victim decides to migrate their code repository from GitHub to a commercial platform and does not remove `coderepo.victim.com` from their DNS server.
3. An adversary discovers that `coderepo.victim.com` is hosted on GitHub and claims it using GitHub Pages and their own GitHub account.

### Expired Domain

1. The victim (victim.com) owns another domain (victimotherdomain.com) and uses a CNAME record (www) to reference the other domain (`www.victim.com` --> `victimotherdomain.com`)
2. At some point, victimotherdomain.com expires, becoming available for registration by anyone. Since the CNAME record is not deleted from the victim.com DNS zone, anyone who registers `victimotherdomain.com` has full control over `www.victim.com` until the DNS record is removed or updated.

## Test Objectives

- Enumerate all possible domains (previous and current).
- Identify any forgotten or misconfigured domains.

## How to Test

### Black-Box Testing

Testing for subdomain takeover follows three phases: subdomain enumeration, automated fingerprint-based detection, and manual validation.

A dangling DNS record occurs when a DNS entry points to an external resource that no longer exists or has been deprovisioned. For example, a CNAME record pointing to a GitHub Pages site that the owner deleted still resolves, but the underlying resource is unclaimed. An attacker can register that resource and take control of the subdomain.

#### Subdomain Enumeration

Use [subfinder](https://github.com/projectdiscovery/subfinder) to discover subdomains for the target domain: `subfinder -d victim.com -o subdomains.txt`

This produces a list of subdomains to use in the detection phase.

#### Fingerprint-Based Detection

Fingerprint-based detection works by comparing each subdomain's HTTP response against a database of known vulnerable service responses. The [can-i-take-over-xyz](https://github.com/EdOverflow/can-i-take-over-xyz) project maintains this database, cataloging the specific response strings returned by service providers such as GitHub Pages, AWS S3, Heroku, and Fastly when a resource is unclaimed.

Use [subzy](https://github.com/LukaSikic/subzy) for a quick initial scan: `subzy run --targets subdomains.txt`

Follow up with [nuclei](https://github.com/projectdiscovery/nuclei) using the dedicated takeover templates for a more accurate result: `nuclei -l subdomains.txt -t takeovers/`

A positive result from either tool indicates that a subdomain's response matched a known vulnerable fingerprint, suggesting a dangling DNS record pointing to an unclaimed resource on a third-party service.

For example, a subdomain pointing to an unclaimed GitHub Pages site returns the following response:

```http
HTTP/1.1 404 Not Found
...
<p>There isn't a GitHub Pages site here.</p>
```

This specific string is listed in can-i-take-over-xyz as the GitHub Pages fingerprint. When subzy or nuclei matches this response, it flags the subdomain as potentially vulnerable.

#### Manual Validation

Automated tools produce false positives. Validate each finding manually before reporting it.

1. Confirm the DNS record and where it points: `dig CNAME subdomain.victim.com`

1. Confirm the response matches the expected fingerprint for that service provider as listed in [can-i-take-over-xyz](https://github.com/EdOverflow/can-i-take-over-xyz): `curl -i http://subdomain.victim.com`

1. Confirm the resource is unclaimed on the service provider's platform. Do not claim it.

#### Cloud-Specific Takeovers

Major cloud providers have distinct takeover patterns worth specific attention:

- AWS S3: A CNAME pointing to an S3 bucket URL (for example, `bucket.s3.amazonaws.com`) where the bucket no longer exists returns a `NoSuchBucket` response. Anyone who creates a bucket with the same name in any AWS account can claim the subdomain.
- Azure: Dangling CNAMEs pointing to deprovisioned Azure resources such as App Services or Traffic Manager endpoints can be claimed by registering the same resource name in a different Azure subscription.
- GCP: Similar patterns exist for Cloud Storage buckets and Firebase Hosting endpoints.

### Gray-Box Testing

The tester has the DNS zone file available, which means DNS enumeration is not necessary. The testing methodology is the same.

## Remediation

To mitigate the risk of subdomain takeover, the vulnerable DNS resource record(s) should be removed from the DNS zone. Continuous monitoring and periodic checks are recommended as best practice.

## Tools

- [subfinder - Subdomain enumeration tool](https://github.com/projectdiscovery/subfinder)
- [subzy - Subdomain takeover detection tool](https://github.com/LukaSikic/subzy)
- [nuclei - Vulnerability scanner with takeover templates](https://github.com/projectdiscovery/nuclei)
- [nuclei-templates - Community takeover templates](https://github.com/projectdiscovery/nuclei-templates)
- [can-i-take-over-xyz - Vulnerable service fingerprint database](https://github.com/EdOverflow/can-i-take-over-xyz)
- [dig - DNS lookup utility](https://man.cx/dig)
- [OWASP Domain Protect](https://owasp.org/www-project-domain-protect)

## References

- [HackerOne - A Guide To Subdomain Takeovers](https://www.hackerone.com/blog/Guide-Subdomain-Takeovers)
- [Subdomain Takeover: Basics](https://0xpatrik.com/subdomain-takeover-basics/)
- [Subdomain Takeover: Going beyond CNAME](https://0xpatrik.com/subdomain-takeover-ns/)
- [can-i-take-over-xyz - A list of vulnerable services](https://github.com/EdOverflow/can-i-take-over-xyz/)
- [OWASP AppSec Europe 2017 - Frans Rosén: DNS hijacking using cloud providers – no verification needed](https://2017.appsec.eu/presos/Developer/DNS%20hijacking%20using%20cloud%20providers%20%E2%80%93%20no%20verification%20needed%20-%20Frans%20Rosen%20-%20OWASP_AppSec-Eu_2017.pdf)
