# Test for Feature Flag Security Bypass

| ID          |
|-------------|
|WSTG-CONF-15|

## Summary

Feature flags are commonly used to control application functionality and enable progressive delivery. They allow features to be enabled, disabled, or gradually rolled out without a full application deployment. Modern applications increasingly use feature flags and kill-switches to gate security-relevant functionality such as authentication, authorization, fraud detection, rate limiting, and risk controls.

When security controls depend on feature flags, inconsistent flag states can introduce vulnerabilities. A control may be enabled in one service while disabled in another, or a rollback may restore application code without restoring the corresponding security configuration. Client-side flags may also be manipulated to reveal functionality that should remain protected.

A common failure pattern occurs when a kill-switch disables enforcement logic but leaves a trusted assertion behind. For example, a fraud-prevention control may be disabled due to performance issues while a backend service continues trusting a `fraud_checked=true` parameter that is no longer being set by the (now-disabled) control. An attacker can replay a previously captured request containing that parameter and bypass the fraud check entirely.

This test evaluates whether security controls remain consistently enforced across all feature flag states, including enablement, disablement, rollback, partial rollout, canary deployment, and feature-flag-service failure.

## Test Objectives

- Identify feature flags and kill-switches that control security-relevant functionality.
- Determine whether feature flag states can be manipulated by an unauthorized client.
- Verify that backend security controls remain enforced independently of client-side flag state.
- Test security behavior when flags are toggled on and off.
- Test security behavior during flag transitions, rollbacks, and staged deployments.
- Verify that security controls remain consistent across services and application instances.
- Determine whether stale security assertions or session state can be reused after a flag transition.
- Evaluate fail-safe behavior when the feature flag service is unavailable.
- Identify sensitive information exposed through feature flag configurations.
- Identify stale feature flags that may expose deprecated or unpatched code paths.

## Common Security Issues

- **Client-side manipulation:** Flags evaluated in the browser can be modified by an attacker to enable restricted functionality.
- **Authorization bypass:** Hidden UI elements may still have accessible backend endpoints.
- **Security control state drift:** Different application components may use different flag states, so a control is enforced by one component but bypassed by another.
- **Kill-switch bypass:** Disabling a control may leave trusted parameters, tokens, or session claims behind that allow the disabled control to be bypassed.
- **Rollback vulnerabilities:** A rollback may restore application code without restoring the corresponding security configuration.
- **Partial rollout vulnerabilities:** Canary or staged deployments may expose different security behavior depending on which instance or service handles a request.
- **Insecure defaults:** Fallback values used when the feature flag service is unavailable may fail open.
- **Information disclosure:** Feature flag configurations may reveal unreleased features, internal services, security controls, or implementation details.
- **Stale flag vulnerabilities:** Unused flags may continue to reference deprecated code paths that contain unpatched vulnerabilities.

Modern applications increasingly rely on feature flag services (LaunchDarkly, Split, Flagsmith, ConfigCat) or custom implementations to manage rollouts, which makes security testing of these mechanisms essential.

## How to Test

Feature flag testing can be performed as **black-box testing**, inferring flag-gated behavior through response diffing across rollout stages, replaying captured requests, and timing analysis; or as **gray-box testing**, where the tester has visibility into the flag management system and can directly toggle states to assess enforcement consistency. Where possible, combine both approaches: black-box testing confirms what an external attacker can actually exploit, while gray-box testing confirms whether the backend enforces controls independently of the flag state itself.

### Identify Security-Relevant Feature Flags

Identify feature flags, kill-switches, and configuration values that control security-relevant behavior, including authentication, multi-factor authentication, authorization, fraud detection, rate limiting, risk-based authentication, account recovery, administrative functionality, and security monitoring.

#### Analyze Client-Side Resources

Inspect JavaScript bundles and other client-side resources for common feature flag patterns:

```text
featureFlags
isFeatureEnabled
featureEnabled
flags
killSwitch
securityFeature
```

Tools such as `source-map-explorer` or the webpack Bundle Analyzer can help locate flag-related code inside minified bundles.

#### Monitor Network Traffic

Use an intercepting proxy (Burp Suite, OWASP ZAP) to capture requests made to feature flag services or internal configuration endpoints (for example, calls to `app.launchdarkly.com`, `/api/config`, or `/api/flags`). Review the response payloads for flag names, default values, and targeting rules.

#### Review API Responses and Configuration Endpoints

Check whether any endpoint returns the full set of flags evaluated for a session, including flags unrelated to the current page. Overly broad flag payloads are a common source of information disclosure (see below).

### Test for Client-Side Flag Manipulation

Where flags are evaluated or cached client-side (for example, in a JavaScript object, cookie, or local storage value), use a proxy to modify the flag value and replay the request:

```http
PUT /api/user/settings HTTP/1.1
Host: example.com
Content-Type: application/json

{"flags": {"betaAdminPanel": true}}
```

- **Vulnerable:** The application exposes hidden functionality, or the modified flag value is trusted without a corresponding server-side check.
- **Secure:** The client-side value has no effect on what the server will authorize; the server re-evaluates the flag independently.

### Verify Backend Authorization Independence

For every security-relevant flag identified, confirm that hiding a feature in the UI is matched by an equivalent restriction on the backend endpoint that feature calls. Attempt to call the underlying endpoint directly while the flag is disabled for the current user:

```http
GET /api/admin/reports HTTP/1.1
Host: example.com
Authorization: Bearer {low-privilege-token}
```

**Expected result:** The server must enforce authorization independently of client-side flag state — an unauthorized user must receive a `401 Unauthorized` or `403 Forbidden` response for this endpoint even if the flag is manipulated client-side. If the feature is disabled globally by design, the endpoint should remain inaccessible to all users (for example, `403`/`404`), rather than the flag only hiding the UI element while the endpoint remains reachable.

### Test Behavior During Flag Transitions and Rollbacks

- **Kill-switch bypass:** Disable a security-relevant flag (fraud check, rate limit, step-up authentication) and replay a request captured *before* the flag was disabled, which contains a parameter, token, or session claim previously set by that control (e.g. `fraud_checked=true`). Confirm the backend does not still trust that stale assertion.
- **Rollback:** Simulate or observe an application rollback and confirm that any security configuration tied to the rolled-back version is also restored — not left in its prior (potentially disabled) state.
- **Partial rollout / canary:** Where multiple instances or services may be running different flag states simultaneously, send repeated requests and compare responses across instances to detect inconsistent enforcement.
- **Second scenario — MFA kill-switch:** Disable step-up/MFA verification for a subset of users via a kill-switch. Confirm that a downstream service does not continue trusting an existing session claim (e.g. `mfa_verified=true`) that was only valid because MFA was previously enforced. If the claim is trusted after the control is disabled, an attacker with a stale session can bypass step-up verification entirely.

### Evaluate Fail-Safe Behavior When the Flag Service Is Unavailable

Block or throttle access to the feature flag service (for example, via proxy rules or DNS blackholing in a test environment) and observe how the application behaves when it cannot retrieve flag state.

- **Vulnerable:** The application fails open, defaulting security-relevant flags to an enabled/permissive state.
- **Expected Result:** Security-relevant controls remain enforced or fall back to a documented secure configuration when the feature flag service is unavailable.

### Analyze Feature Flag Configurations for Information Disclosure

Review any flag configuration retrievable by the client (via API response, JS bundle, or exposed admin panel) for:

- Names of unreleased features or internal services.
- Targeting rules that reveal internal user segments, employee accounts, or test cohorts.
- Configuration values (URLs, feature descriptions) that expose implementation details.

### Identify Stale Feature Flags

Search the codebase (where accessible) or ask for a list of flags no longer actively toggled. Stale flags that gate now-unused code paths can still be reachable and may reference logic that has not received subsequent security patches. Confirm whether such paths are still reachable in the running application and, if so, whether they are still enforced correctly.

## Remediation

- Enforce all security-relevant authorization checks on the backend, independent of any client-supplied or client-visible flag state.
- Ensure kill-switches remove trust in any parameter, token, or session claim that was only valid because the associated control was active.
- Tie security configuration to the same deployment/version control as application code so rollbacks restore both together.
- Ensure feature flag services use a documented secure fallback for security-relevant flags when unavailable.
- Avoid exposing the full flag configuration to the client; return only the flags relevant to the current user and context.
- Periodically audit and remove stale flags, along with the code paths they gate, once a rollout is complete.
- Apply consistent flag evaluation across all services and instances handling a given request.

## Tools

- [Burp Suite](https://portswigger.net/burp)
- [ZAP](https://www.zaproxy.org/)
- Browser Developer Tools (Chrome, Firefox, Edge)
- [source-map-explorer](https://github.com/danvk/source-map-explorer) / webpack Bundle Analyzer (for locating flag logic in minified JS bundles)

## References

- [Feature Toggles (aka Feature Flags) - Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- [LaunchDarkly Account Security](https://launchdarkly.com/docs/home/account/secure)
- [OWASP ASVS - Configuration](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE-284: Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)
- [CWE-863: Incorrect Authorization](https://cwe.mitre.org/data/definitions/863.html)
