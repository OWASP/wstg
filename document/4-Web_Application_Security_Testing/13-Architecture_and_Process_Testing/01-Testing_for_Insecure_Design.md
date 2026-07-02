# Testing for Insecure Design

|ID|
|---|
|WSTG-APT-01|

## Summary

Insecure Design describes risks originating from architectural or design flaws. Even if an application is technically implemented perfectly, a flawed design can lead to critical security vulnerabilities. This includes the absence of necessary security controls (such as rate limiting or strict segregation of duties) or faulty business logic that can be abused by attackers.

## Test Objectives

- Evaluate the application architecture and identify design flaws.
- Identify missing security controls in critical business processes.
- Test whether the application's business logic can be bypassed through unexpected usage.

## How to Test

Testing for insecure design requires a deep understanding of the business logic, as automated scanners typically cannot detect these types of flaws.

### Threat Modeling Analysis

Review the application's Threat Model (if available):

- Have potential threats to critical processes (e.g., password resets, checkout flows) been documented?
- Are sufficient security controls designed to mitigate these threats?

### Bypassing Business Logic

Look for ways to manipulate the intended workflow of the application.

- **Step Skipping:** If a process consists of multiple steps (e.g., E-commerce checkout: 1. Cart, 2. Shipping, 3. Payment, 4. Confirmation), try jumping directly from step 2 to step 4 without paying.
- **Rate Limiting:** Check if attackers can perform critical actions an unlimited number of times (e.g., mass-reserving concert tickets to mark them as sold out).

### Segregation of Duties

Review the role concept:

- Can a single user perform an action that should require multi-step approval (four-eyes principle)?
- Is it possible for administrators to approve their own actions without an audit trail tracking it?

## Remediation

- Conduct Threat Modeling during the software development planning phase.
- Implement "Secure by Design" principles and established design patterns.
- Validate not only data but also the state and flow of user sessions on the server side.
- Strictly segregate critical systems and networks into different zones (Segmentation).

## References

- OWASP Top 10:2021 - A04: Insecure Design
- OWASP Threat Modeling
- -- START OF FILE 02-Testing_for_Vulnerable_and_Outdated_Components.md ---