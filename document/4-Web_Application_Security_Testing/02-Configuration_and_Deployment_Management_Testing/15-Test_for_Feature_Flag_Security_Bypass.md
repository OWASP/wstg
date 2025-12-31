# Testing for Feature Flag Security Bypass

|ID          |
|------------|
|WSTG-CONF-15|

## Summary

Feature flags (also known as feature toggles, feature switches, or feature gates) are a software development technique that allows teams to enable or disable functionality without deploying new code. While feature flags provide significant benefits for progressive delivery and A/B testing, they can introduce security vulnerabilities when improperly implemented.

Common security issues with feature flags include:

- **Client-side manipulation**: Flags evaluated in the browser can be modified by attackers to enable restricted features.
- **Authorization bypass**: Hidden UI elements may still have accessible back-end endpoints.
- **Information disclosure**: Flag configurations may leak unreleased features or internal logic.
- **Insecure defaults**: Fallback values when the flag service is unavailable may fail open.
- **Stale flag vulnerabilities**: Unused flags referencing deprecated code paths may contain unpatched vulnerabilities.

Modern applications increasingly rely on feature flag services (LaunchDarkly, Split, Flagsmith, ConfigCat) or custom implementations for controlled rollouts, making security testing of these mechanisms essential.

## Test Objectives

- Identify feature flags that gate security-relevant functionality.
- Assess whether feature flag states can be manipulated client-side.
- Verify that back-end authorization is independent of flag state.
- Determine if flag configurations expose sensitive information.
- Evaluate fail-safe behavior when the flag service is unavailable.

## How to Test

### Identify Feature Flags in the Application

Search for evidence of feature flag implementations:

1. **Inspect JavaScript bundles** for references to feature flag services or configuration objects:

```javascript
// Common patterns to search for:
featureFlags
featureToggles
flags.isEnabled
LaunchDarkly
splitio
flagsmith
```

2. **Monitor network traffic** for requests to feature flag endpoints:

```http
GET /api/features HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: application/json

{
  "features": {
    "new_checkout_flow": true,
    "admin_panel_v2": false,
    "beta_api": false
  }
}
```

3. **Examine local storage and cookies** for cached flag values.

### Test Client-Side Flag Manipulation

Attempt to modify flag values to enable restricted features:

1. **Intercept and modify responses**: Use a proxy tool to change flag values from `false` to `true` in API responses.

```http
# Original response
{"admin_mode": false}

# Modified response
{"admin_mode": true}
```

2. **Modify local storage**: If flags are cached client-side, change the values directly.

```javascript
// In browser console
localStorage.setItem('featureFlags', JSON.stringify({
  ...JSON.parse(localStorage.getItem('featureFlags')),
  restricted_feature: true
}));
```

3. **Observe application behavior**: Determine if the application grants access to functionality that should be restricted.

### Verify Backend Authorization Independence

Ensure back-end endpoints enforce authorization independently of flag state:

1. **Identify hidden endpoints**: Extract API endpoints from JavaScript bundles that are associated with disabled features.

```bash
# Search for API patterns in JS files
grep -oE '/api/v[0-9]+/[a-zA-Z_]+' bundle.js
```

2. **Send direct requests**: Attempt to access endpoints for disabled features.

```http
POST /api/admin/users/delete HTTP/1.1
Host: example.com
Authorization: Bearer <user_token>
Content-Type: application/json

{"user_id": "12345"}
```

3. **Expected result**: The server should return `403 Forbidden` if the feature is disabled, not just hide the UI.

### Test Fallback Behavior

Evaluate what happens when the feature flag service is unavailable:

1. **Block connectivity** to the flag provider using browser DevTools network blocking or hosts file modification.

```bash
# Add to /etc/hosts (testing only)
127.0.0.1 sdk.launchdarkly.com
127.0.0.1 app.split.io
```

2. **Observe fallback behavior**: Determine if the application fails open (enables features) or fails closed (disables features).

3. **Security-critical result**: Features gating security controls should default to disabled when the flag service is unreachable.

### Analyze Flag Configuration for Information Leakage

Examine flag payloads for sensitive information:

1. **Capture flag configuration responses** and look for:
   - Unreleased feature names revealing roadmap
   - Internal tool references
   - Targeting rules containing email domains or user identifiers
   - Environment-specific configurations

2. **Example of information leakage**:

```json
{
  "flags": {
    "internal_admin_tool_q1_2025": false,
    "bypass_rate_limit_for_enterprise": false,
    "show_feature_if_email_contains_@internal.company.com": true
  }
}
```

### Test for Stale Feature Flags

Identify and test unused flags that may expose deprecated functionality:

1. **Map all flags** and their creation dates if available.
2. **Force-enable old flags** and observe if deprecated code paths are accessible.
3. **Assess deprecated code** for known vulnerabilities or security weaknesses.

## Remediation

To prevent feature flag security bypass vulnerabilities:

- **Server-side evaluation**: Evaluate security-critical flags on the server, never trust client-provided values.
- **Authorization independence**: Backend authorization checks must not depend on flag state.
- **Fail-secure defaults**: Configure security-relevant flags to default to disabled if the flag service fails.
- **Minimal client exposure**: Only send flag evaluation results to clients, not targeting rules or full configurations.
- **Flag hygiene**: Implement policies to remove flags after their purpose is complete (typically 30-90 days post-launch).
- **Audit logging**: Log flag evaluations for security-critical features.

For more details, see:

- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Top Ten - A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

## Tools

- [Burp Suite](https://portswigger.net/burp) - Intercept and modify HTTP traffic
- [OWASP ZAP](https://www.zaproxy.org/) - Web application security testing
- Browser Developer Tools - Network inspection and local storage modification

## References

- [Feature Toggles (aka Feature Flags) - Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- [LaunchDarkly Security Best Practices](https://docs.launchdarkly.com/home/security)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

