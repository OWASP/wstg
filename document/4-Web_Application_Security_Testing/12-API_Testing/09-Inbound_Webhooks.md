# Inbound Webhooks

|ID          |
|------------|
|WSTG-APIT-09|

## Summary

Inbound webhooks are HTTP callbacks that an external system sends to the application when an event occurs: payment captured, incident opened, repository updated, identity provider event, and similar notifications. The application trusts those requests to create incidents, update orders, provision accounts, or unlock workflows.

Unlike ordinary API authentication, the caller is not an end user. The application must authenticate the *sender*, bind the event to the correct tenant, and make delivery idempotent. Missing those controls allows forged events, cross-tenant impact, and replay.

This test covers inbound authenticity, authorization, replay, and lifecycle. Outbound webhook URL handling and SSRF belong with Server-Side Request Forgery testing and must not be duplicated here.

> Note: Open API PRs may add authentication, rate limiting, mass assignment, and SSRF articles as `05` through `08`. This article uses `09` to reduce collisions. Maintainers may renumber after those merges.

## Test Objectives

- Determine whether inbound webhook endpoints authenticate the sender.
- Verify tenant, project, and object binding so a valid event for one customer cannot affect another.
- Verify replay and duplicate-delivery handling.
- Verify that revoked integrations stop accepting events and become unmanageable only by authorized principals.

## How to Test

Use only tester-owned integrations and synthetic events. Do not send forged events against another customer's tenant.

### 1. Inventory Webhook Receivers

1. Review integration settings, API docs, and reverse-proxy routes for paths such as `/webhooks/`, `/callbacks/`, `/hooks/`, or vendor-specific suffixes.
2. Capture a legitimate delivery to a tester-owned endpoint, including headers and raw body.
3. Record claimed authentication: shared secret, HMAC signature, mutual TLS, IP allowlist, or none.

### 2. Sender Authentication

1. Replay the captured body without signature headers.
2. Replay with an empty or attacker-chosen signature.
3. Modify one byte of the raw body while keeping the original signature.
4. If the scheme signs selected fields only, reorder JSON properties or add unused fields and check whether verification is over the exact raw bytes.
5. If timestamps are signed, replay an old event outside the accepted skew.

Secure behavior rejects unauthenticated, mistyped, and body-tampered deliveries. IP allowlists alone are weak; treat them as defense in depth, not as the only control.

### 3. Tenant and Object Binding

1. Capture a valid event for tester tenant A.
2. Replace non-secret identifiers such as service ID, site ID, shop ID, project GUID, or account slug with tester tenant B's corresponding identifier, keeping A's signature material when the signature does not cover those fields.
3. Send the modified event to the global or B-facing webhook URL.

Secure behavior accepts the event only for the tenant whose credential signed it. Identifiers that are visible in UIs or APIs must not be treated as capabilities.

### 4. Replay and Idempotency

1. Send the same valid event twice.
2. Send two events with the same event ID or delivery ID and different payloads.
3. Concurrently deliver the same event twice.

The application should acknowledge duplicates without applying the side effect twice. State-changing handlers need an idempotency key derived from the vendor event ID or a signed delivery ID.

### 5. Lifecycle and Management

1. Disable or uninstall the integration as an authorized user, then replay a previously valid event. It must fail.
2. Rotate the signing secret, then replay events signed with the old secret.
3. As a low-privilege user, attempt to list, edit, or delete another team's webhook configuration. Apply [Broken Object Level Authorization](02-API_Broken_Object_Level_Authorization.md) and [Broken Function Level Authorization](04-API_Broken_Function_Level_Authorization.md).
4. Confirm disabled hooks do not remain active while disappearing from the management UI.

## Remediation

- Authenticate every inbound webhook with a per-tenant secret, HMAC over the raw body and relevant headers, or mutual TLS.
- Include timestamp and delivery identity in the signed material; reject stale and duplicate deliveries.
- Derive tenant context from the verified credential, not from mutable body fields alone.
- Make handlers idempotent.
- On uninstall, secret rotation, or permission removal, immediately invalidate verification material and stop processing.

## Related Test Cases

- [API Broken Object Level Authorization](02-API_Broken_Object_Level_Authorization.md)
- [API Broken Function Level Authorization](04-API_Broken_Function_Level_Authorization.md)
- [Server-Side Request Forgery](../07-Injection/19-Server-Side_Request_Forgery.md)
- [Testing for Weak Transport Layer Security](../09-Weak_Cryptography/01-Weak_Transport_Layer_Security.md)

## Tools

- [Zed Attack Proxy](https://www.zaproxy.org)
- [Burp Suite](https://portswigger.net/burp)
- Vendor webhook CLI or signed-request test harness for the integration under test

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [RFC 9110 - HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110)
- Vendor documentation for the specific webhook signature scheme under test
