# Penetration Testing Methodologies

## Summary

- [OWASP Testing Guides](#owasp-testing-guides)
    - Web Security Testing Guide (WSTG)
    - Mobile Security Testing Guide (MSTG)
    - Firmware Security Testing Methodology
- [Penetration Testing Execution Standard](#penetration-testing-execution-standard)
- [PCI Penetration Testing Guide](#pci-penetration-testing-guide)
    - [PCI DSS Penetration Testing Guidance](#pci-dss-penetration-testing-guidance)
    - [PCI DSS Penetration Testing Requirements](#pci-dss-penetration-testing-requirements)
- [Penetration Testing Framework](#penetration-testing-framework)
- [Technical Guide to Information Security Testing and Assessment](#technical-guide-to-information-security-testing-and-assessment)
- [Open Source Security Testing Methodology Manual](#open-source-security-testing-methodology-manual)
- [References](#references)

## OWASP Testing Guides

In terms of technical security testing execution, the OWASP testing guides are highly recommended. Depending on the types of the applications, the testing guides are listed below for the web/cloud services, Mobile app (Android/iOS), or IoT firmware respectively.

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [OWASP Firmware Security Testing Methodology](https://github.com/scriptingxss/owasp-fstm)

## Penetration Testing Execution Standard

Penetration Testing Execution Standard (PTES) defines penetration testing as 7 phases. Particularly, PTES Technical Guidelines give hands-on suggestions on testing procedures, and recommendation for security testing tools.

- Pre-engagement Interactions
- Intelligence Gathering
- Threat Modeling
- Vulnerability Analysis
- Exploitation
- Post Exploitation
- Reporting

[PTES Technical Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)

## PCI Penetration Testing Guide

Payment Card Industry Data Security Standard (PCI DSS) Requirement 11.3 defines the penetration testing. PCI also defines Penetration Testing Guidance.

### PCI DSS Penetration Testing Guidance

The PCI DSS Penetration testing guideline provides guidance on the following:

- Penetration Testing Components
- Qualifications of a Penetration Tester
- Penetration Testing Methodologies
- Penetration Testing Reporting Guidelines

### PCI DSS Penetration Testing Requirements

The PCI DSS requirement refer to Payment Card Industry Data Security Standard (PCI DSS) Requirement 11.3

- Based on industry-accepted approaches
- Coverage for CDE and critical systems
- Includes external and internal testing
- Test to validate scope reduction
- Application-layer testing
- Network-layer tests for network and OS

[PCI DSS Penetration Test Guidance](https://www.pcisecuritystandards.org/documents/Penetration-Testing-Guidance-v1_1.pdf)

## Penetration Testing Framework

The Penetration Testing Framework (PTF) provides comprehensive hands-on penetration testing guide. It also lists usages of the security testing tools in each testing category. The major area of penetration testing includes:

- Network Footprinting (Reconnaissance)
- Discovery & Probing
- Enumeration
- Password cracking
- Vulnerability Assessment
- AS/400 Auditing
- Bluetooth Specific Testing
- Cisco Specific Testing
- Citrix Specific Testing
- Network Backbone
- Server Specific Tests
- VoIP Security
- Wireless Penetration
- Physical Security
- Final Report - template

[Penetration Testing Framework](http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html)

## Technical Guide to Information Security Testing and Assessment

Technical Guide to Information Security Testing and Assessment (NIST 800-115) was published by NIST, it includes some assessment techniques listed below.

- Review Techniques
- Target Identification and Analysis Techniques
- Target Vulnerability Validation Techniques
- Security Assessment Planning
- Security Assessment Execution
- Post-Testing Activities

The NIST 800-115 can be accessed [here](https://csrc.nist.gov/publications/detail/sp/800-115/final)

## Open Source Security Testing Methodology Manual

The Open Source Security Testing Methodology Manual (OSSTMM) is a methodology to test the operational security of physical locations, workflow, human security testing, physical security testing, wireless security testing, telecommunication security testing, data networks security testing and compliance. OSSTMM can be supporting reference of ISO 27001 instead of a hands-on or technical application penetration testing guide.

OSSTMM includes the following key sections:

- Security Analysis
- Operational Security Metrics
- Trust Analysis
- Work Flow
- Human Security Testing
- Physical Security Testing
- Wireless Security Testing
- Telecommunications Security Testing
- Data Networks Security Testing
- Compliance Regulations
- Reporting with the STAR (Security Test Audit Report)

[Open Source Security Testing Methodology Manual](https://www.isecom.org/OSSTMM.3.pdf)

## References

- [PCI Data Security Standard - Penetration TestingGuidance](https://www.pcisecuritystandards.org/documents/Penetration-Testing-Guidance-v1_1.pdf)
- [PTES Standard](http://www.pentest-standard.org/index.php/Main_Page)
- [Open Source Security Testing Methodology Manual (OSSTMM)](http://www.isecom.org/research/osstmm.html)
- [Technical Guide to Information Security Testing and Assessment NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final)
- [HIPAA Security Testing Guidance](https://www.hhs.gov/hipaa/for-professionals/security/guidance/cybersecurity/index.html)
- [Penetration Testing Framework 0.59](http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html)
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Security Testing Guidelines for Mobile Apps](https://owasp.org/www-pdf-archive/Security_Testing_Guidelines_for_mobile_Apps_-_Florian_Stahl+Johannes_Stroeher.pdf)
- [Kali Linux](https://www.kali.org/)
- [Information Supplement: Requirement 11.3 Penetration Testing](https://www.pcisecuritystandards.org/pdfs/infosupp_11_3_penetration_testing.pdf)
