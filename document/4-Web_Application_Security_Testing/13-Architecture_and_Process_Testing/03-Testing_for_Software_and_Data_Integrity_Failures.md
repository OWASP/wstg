# Testing for Software and Data Integrity Failures

|ID|
|---|
|WSTG-APT-03|

## Summary

Software and data integrity failures occur when code or infrastructure is not protected against manipulation. This happens when an application loads plugins, libraries, or modules from untrusted sources, repositories, or Content Delivery Networks (CDNs) without validation. Insecure CI/CD pipelines and the deserialization of untrusted data (Insecure Deserialization) also fall into this category. Attackers can exploit these flaws to inject malicious code, manipulate updates, or completely take over the system.

## Test Objectives

- Identify features that load or process data without integrity checks.
- Test for insecure deserialization processes.
- Verify client-side scripts for missing Subresource Integrity (SRI) controls.

## How to Test

### Insecure Deserialization

Look for data that is serialized (e.g., as Java objects, PHP objects, XML, or YAML), sent to the server, and deserialized there.

- Check cookies, hidden form fields, or API parameters for typical signatures of serialized objects (e.g., `rO0AB` for Java Base64, `O:4:"User"` in PHP).
- Attempt to inject manipulated objects to trigger logic flaws or achieve Remote Code Execution (RCE) using tools like `ysoserial`.

### Subresource Integrity (SRI) Check

If the application includes JavaScript or CSS from third parties (CDNs), check if Subresource Integrity (SRI) is implemented.

- Analyze the `<script>` and `<link>` tags in the source code.
- A secure tag must include the `integrity` attribute: `<script src="<https://cdn.example.com/script.js>" integrity="sha384-..." crossorigin="anonymous"></script>`. Without this attribute, an attacker who compromises the CDN could maliciously modify the code unnoticed.

### Unsigned Firmware/Update Mechanisms

For IoT devices, desktop clients, or mobile apps:

- Examine the update mechanism. Are updates downloaded over unencrypted HTTP?
- Does the application require and verify a cryptographic signature of the update payload before installing it?

## Remediation

- Always verify the integrity of software and data using digital signatures.
- Use Subresource Integrity (SRI) when loading external resources via CDNs.
- Replace complex deserialization with simple data types (like JSON) that do not directly bind to objects/classes.
- Secure the CI/CD pipeline (implement strict access controls, use code signing).

## Tools

- ysoserial (for Java Deserialization)
- Burp Suite Plugins (e.g., Java Deserialization Scanner)

## References

- OWASP Top 10:2021 - A08: Software and Data Integrity Failures
- OWASP Deserialization Cheat Sheet
- -- START OF FILE 04-Testing_for_Security_Logging_and_Monitoring_Failures.md ---