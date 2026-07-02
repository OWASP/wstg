# Testing for Security Logging and Monitoring Failures

|ID|
|---|
|WSTG-APT-04|

## Summary

Insufficient logging and monitoring allow attackers to carry out their operations over extended periods unnoticed, infiltrate deeper systems, and destroy evidence. If an application fails to log critical security-relevant events (such as failed logins, access control failures, or server-side input errors), or if the monitoring system fails to generate timely alerts, defenders lack the visibility needed to respond to incidents quickly.

## Test Objectives

- Verify whether critical security events (like authentication and authorization failures) are logged.
- Test whether attackers can manipulate or obfuscate logs (Log Injection).
- (If architectural access is granted) Validate whether the monitoring system detects unusual activities and triggers alerts.

## How to Test

### Triggering Security Events

Since testers usually do not have direct access to backend logs, the application's behavior often must be evaluated indirectly (or in collaboration with the operations team).

1. Intentionally provoke security-relevant errors, for example:
    - Enter the wrong password multiple times during login.
    - Try to access administrator endpoints (`/admin`) as a standard user (expecting HTTP 401/403).
    - Manipulate parameters to provoke server errors (HTTP 500).
2. Observe if the application reacts (e.g., by locking the account after several failed attempts). The absence of such a reaction is often a strong indicator of lacking monitoring and insufficient protection against automated attacks.

### Log Injection Analysis

If user input is written to log files unfiltered, attackers can manipulate the logs.

1. Send crafted text containing control characters like newlines (`\n`, `\r`) through login forms or HTTP headers (e.g., `User-Agent: Attacker\n[CRITICAL] Admin access granted`).
2. If the application logs this input without sanitization, the attacker can forge log entries, deceive administrators, or disrupt SIEM systems.

### Log Exposure

Check if sensitive data is exposed in error messages or logs.

- Send intentionally malformed requests and inspect the server's error messages.
- If API keys, passwords, session IDs, or Personally Identifiable Information (PII) are transmitted in URL parameters, they will automatically be recorded in standard web server access logs.

## Remediation

- Log all authentication attempts, access control failures, and server-side exceptions with sufficient context (who, what, when).
- Ensure that log entries are formatted in a way that can be easily parsed by centralized log management solutions (SIEM).
- Filter and sanitize all user input before writing it to logs to prevent Log Injection.
- Protect logs from tampering by using cryptographic hashes or write-only storage.
- Automatically alert system administrators to suspicious activities (e.g., mass 404 or 500 errors originating from a single IP address).

## References

- OWASP Top 10:2021 - A09: Security Logging and Monitoring Failures
- OWASP Logging Cheat Sheet

---