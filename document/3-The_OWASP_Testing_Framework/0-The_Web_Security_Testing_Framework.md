# The Web Security Testing Framework

## Overview

This framework is meant to be a flexible set of testing activities that organizations can adopt and adapt, without assuming a fixed sequence or gated workflow. Security testing has no single home - it happens in requirements discussions, in architecture reviews, in the IDE, in CI/CD pipelines, in staging and production environments, and via continuous scanning and external researchers, often simultaneously.

Unlike a prescriptive methodology, this framework recognizes that the cadence, sequencing, and ownership of testing vary by context. A startup may begin with lightweight threat modeling and code review. A regulated organization may prioritize threat modeling, design review, and CI/CD automation. A mature product team may operate all activities continuously. The goal is to help organizations choose and scale the right mix of activities for their threat model, development practices, and risk tolerance. For cost comparison and business context, see the [Introduction](../2-Introduction/README.md#why-web-application-security-testing-matters).

## Testing Activities

The following six categories cover the main testing activities that contribute to application security. Each typically recurs on a cadence (triggered by requirements changes, architecture decisions, every commit, on a release schedule, or continuously) rather than happening once in a fixed sequence. They can and should also feed back into each other.

### Requirements and Policy Review

Establish and document security policies, secure coding standards, and security requirements baseline. The [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) and [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) provide reference controls. When reviewing requirements, ensure clarity on the following areas:

- User management and identity federation
- Authentication and multi-factor authentication (MFA)
- Authorization and access control (RBAC / ABAC)
- Data confidentiality, integrity, and privacy (including personally identifiable information (PII) handling)
- Session management and token handling
- Transport security and cryptographic standards
- API contracts and third-party integrations
- Infrastructure as code (IaC), container images, and cloud configuration
- Supply chain and dependency risk
- Incident response and monitoring requirements
- Applicable compliance standards (PCI DSS, HIPAA, GDPR, SOC 2, ISO/IEC 27001, etc.)

Revisit this baseline whenever requirements, regulations, or business priorities change.

### Design, Architecture, and Threat Modeling

Review design and architecture documentation (specifications, models, infrastructure-as-code templates) to verify alignment with security requirements. Identify emerging design risks across these areas:

- Microservices and APIs: service boundaries, inter-service authentication, API gateways
- Cloud and containers: identity and access management (IAM) policies, network isolation, container provenance, secrets management
- Client-side architectures: single-page applications (SPA), state handling, cross-origin resource sharing (CORS) policy
- Third-party dependencies and managed services: trust boundaries, compliance responsibilities Undertake threat modeling to identify realistic attack scenarios and ensure each threat has been mitigated, accepted as residual risk, or transferred to a third party. Tools such as [OWASP Threat Dragon](https://owasp.org/www-project-threat-dragon/) and [Pythonic Threat Modeling](https://owasp.org/www-project-pytm/) can help structure this exercise. Repeat this activity whenever the application's architecture or threat model changes.

### Code-Level Review and Analysis

Manually review code for security defects, particularly in complex logic, cryptographic implementations, access control, and API code. Combine manual review with automated static analysis:

- **Static Application Security Testing (SAST)** tools scan source code for known vulnerability patterns.
- **Secret scanning** tools detect accidentally committed credentials before they reach version control.
- **Software Composition Analysis (SCA)** tools scan dependencies for known vulnerabilities.

Use tools such as SonarQube, Semgrep, TruffleHog, OWASP Dependency-Check, or Snyk, and establish policies for remediating vulnerable dependencies. These activities are ideally integrated into the development environment (IDE plugins, pre-commit hooks) and the build pipeline, running on every commit or pull request.

### Dynamic and Penetration Testing

Test the running application for vulnerabilities that static analysis or manual code review may have missed. This activity includes:

- Dynamic Application Security Testing (DAST) tools like ZAP or Burp Suite crawl and fuzz the application
- Manual penetration testing validates exploitability, tests integration points, and probes business logic
- Configuration review ensures no unnecessary services are enabled, default credentials are changed, security headers are present, and TLS/SSL versions and ciphers are appropriate These activities can target staging or production environments, run on-demand or on a scheduled cadence, and be conducted by an internal team, a third-party consultant, or via a [bug bounty program](1-Bug_Bounty_Programs.md). For methodologies and frameworks for penetration testing, see [Appendix G](../6-Appendix/G-Penetration_Testing_Methodologies.md).

### Continuous Integration Pipeline Testing

Integrate security testing into continuous integration (CI) and continuous delivery (CD) pipelines so security is not an afterthought. Define security checks by pipeline stage:

- At build time, run SAST, SCA, and secret scanning
- In staging, run DAST and IaC/container image scanning
- Before release, require security sign-off and define thresholds for blocking deployment This is the connective tissue that allows code review, automated scanning, and dynamic testing to run continuously without becoming a bottleneck. Consult [OWASP SAMM](https://owaspsamm.org/model/) and [NIST SSDF](https://csrc.nist.gov/publications/detail/sp/800-218/final) for guidance on scaling these practices.

### Continuous and Crowd-Sourced Testing

Operate security testing as an always-on activity beyond the development pipeline. This includes operational security monitoring and periodic reassessment (rerunning SAST/DAST/SCA tooling, manual penetration testing, or threat modeling reviews) to catch new vulnerabilities introduced by code changes, dependency updates, or infrastructure drift. It also includes [bug bounty programs](1-Bug_Bounty_Programs.md), which operate continuously and leverage external security researchers to identify novel attacks and edge cases that internal testing may miss. Like other testing activities, this is not a one-time event but a sustained, parallel practice.

## Matching Activity to Cadence

The table below shows how testing activities typically fit into an organization's workflow, without assuming a fixed sequence:

| Testing Activity | Typical Cadence | Typical Owner | Examples & References |
|---|---|---|---|
| Requirements & Policy Review | Triggered (new feature, regulatory change) | Product manager + security | OWASP ASVS, Cheat Sheet Series, compliance docs |
| Design, Architecture & Threat Modeling | Triggered (architecture change) | Architects + security | Threat Dragon, pytm, STRIDE, NIST risk assessment |
| Code Review, SAST, SCA, Secret Scanning | Continuous (every commit / PR) | Developers + automated tooling | SonarQube, Semgrep, TruffleHog, Dependency-Check, Snyk |
| DAST & Penetration Testing | Scheduled + triggered (release schedule, on-demand) | Internal security team or third party | ZAP, Burp Suite, manual testing |
| Bug Bounty Programs | Continuous, always-on | External researchers | HackerOne, Bugcrowd, or self-hosted |
| CI/CD Pipeline Security Gates | Continuous (every build / deployment) | Developers + automated tooling | Build logs, SAST/SCA tool integration |
| Operational Monitoring & Periodic Reassessment | Continuous (monitoring), scheduled (assessments) | Operations + security teams | SIEM/log analysis, scheduled re-scanning, pentests |

## Where to Start

If your organization is building a testing program from scratch, do not feel obligated to implement all activities at once or in a fixed order. Instead, start with the activity that offers the most immediate value given your risk profile and development practices:

- Teams with strong development velocity may start with code review and SAST integration into CI/CD, catching common bugs early.
- Teams building complex, interconnected systems may prioritize threat modeling and architecture review.
- Teams deploying to cloud or microservices infrastructure may focus on IaC scanning and cloud configuration review.
- Product teams with a published API may prioritize API testing and security-focused penetration testing.
- Organizations handling sensitive data may start with data classification, encryption standards, and compliance-driven requirements review.

As things mature, expand coverage to include the other activities, refining your focus based on what testing reveals. The framework is not a checklist to complete in order, but a reference for the range of activities that, over time, build a comprehensive testing program.
