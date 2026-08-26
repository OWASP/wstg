# Penetration Testing Methodologies

This appendix documents established penetration testing methodologies and frameworks. These standards provide detailed guidance on testing procedures, phases, and reporting. The [OWASP Testing Framework](../3-The_OWASP_Testing_Framework/README.md) (Section 3) describes *when* to test and what techniques to apply. This appendix catalogs the *how* - structured methodologies that practitioners can reference when conducting formal penetration testing engagements.

## Summary

- [OWASP Testing Guides](#owasp-testing-guides)
- [PCI Penetration Testing Guide](#pci-penetration-testing-guide)
- [Penetration Testing Framework](#penetration-testing-framework)
- [Technical Guide to Information Security Testing and Assessment](#technical-guide-to-information-security-testing-and-assessment)
- [Open Source Security Testing Methodology Manual](#open-source-security-testing-methodology-manual)
- [Adversary Emulation and MITRE ATT&CK](#adversary-emulation-and-mitre-attck)

## OWASP Testing Guides

The OWASP project maintains testing guides for different application types:

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) - web applications and web services
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/) - iOS and Android applications
- [OWASP Firmware Security Testing Methodology](https://github.com/scriptingxss/owasp-fstm) - embedded systems and firmware
- [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/) - AI and Large Language Model (LLM) applications

## PCI Penetration Testing Guide

[PCI DSS Requirement 11.3](https://www.pcisecuritystandards.org/documents/Penetration-Testing-Guidance-v1_1.pdf) mandates penetration testing for organizations handling payment card data. The PCI guidance covers:

- Penetration testing components and qualifications
- Industry-accepted testing methodologies
- Coverage for cardholder data environments (CDE) and critical systems
- External and internal testing requirements
- Application-layer and network-layer testing
- Scope validation and testing procedures

## Penetration Testing Framework

The Penetration Testing Framework (PTF) was a comprehensive resource for hands-on penetration testing, but the project is no longer actively maintained. For historical reference, it categorized penetration testing activities across network footprinting, discovery, enumeration, vulnerability assessment, and specialized testing areas (wireless, VoIP, physical security). Modern practitioners should refer to the active frameworks listed above (NIST 800-115, OSSTMM) and the OWASP Testing Guides for current guidance.

## Technical Guide to Information Security Testing and Assessment

[NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final) provides a technical reference for security testing and assessment, covering:

- Review Techniques (document review, code review, security testing)
- Target Identification and Analysis Techniques (active/passive reconnaissance)
- Target Vulnerability Validation Techniques (dynamic and static analysis)
- Security Assessment Planning and Execution
- Post-Testing Activities (analysis and reporting)

The related [NIST SP 800-218 (Secure Software Development Framework)](https://csrc.nist.gov/publications/detail/sp/800-218/final) provides broader guidance on secure development practices across the SDLC.

## Open Source Security Testing Methodology Manual

[OSSTMM](https://www.isecom.org/OSSTMM.3.pdf) is a comprehensive methodology for testing operational security across physical locations, workflows, and technical systems. It covers:

- Security Analysis and Risk Assessment
- Human Security Testing (social engineering, awareness)
- Physical Security Testing
- Wireless and Telecommunications Security Testing
- Data Networks Security Testing
- Compliance and Audit Procedures
- Reporting via the STAR (Security Test Audit Report) framework

OSSTMM is often used as a reference for compliance testing and operational risk assessment, complementing technical vulnerability testing.

## Adversary Emulation and MITRE ATT&CK

In addition to structured penetration testing methodologies, adversary-emulation exercises frame testing around real attack techniques and tactics. [MITRE ATT&CK](https://attack.mitre.org/) is a globally accessible knowledge base of adversary tactics and techniques derived from real-world observation. Security teams and red teams increasingly use ATT&CK to:

- Structure penetration testing engagements around realistic attack paths
- Prioritize threat modeling and defense investments
- Design detection engineering and threat hunting procedures

ATT&CK complements the traditional penetration testing methodologies listed above by providing a common taxonomy and an adversary-focused perspective rather than a phase-based or tool-focused one.

## References

- [MITRE ATT&CK](https://attack.mitre.org/)
- [HIPAA Security Testing Guidance](https://www.hhs.gov/hipaa/for-professionals/security/guidance/cybersecurity/index.html)
