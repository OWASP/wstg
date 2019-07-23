# Reporting

Performing the technical side of the assessment is only half of the overall assessment process. The final product is the production of a well written and informative report. A report should be easy to understand and should highlight all the risks found during the assessment phase. The report should appeal to both executive management and technical staff.

The report needs to have three major sections. It should be created in a manner that allows each separate section to be printed and given to the appropriate teams, such as the developers or system managers. The recommended sections are outlined below.

## 1. Executive Summary

The executive summary sums up the overall findings of the assessment and gives business managers and system owners a high level view of the vulnerabilities discovered. The language used should be more suited to people who are not technically aware and should include graphs or other charts which show the risk level. Keep in mind that executives will likely only have time to read this summary and will want two questions answered in plain language:

1. *What's wrong?*
2. *How do I fix it?* You have one page to answer these questions.

The executive summary should plainly state that the vulnerabilities and their severity is an **input** to their organizational risk management process, not an outcome or remediation. It is safest to explain that tester does not understand the threats faced by the organization or business consequences if the vulnerabilities are exploited. This is the job of the risk professional who calculates risk levels based on this and other information. Risk management will typically be part of the organization's IT Security Governance, Risk and Compliance (GRC) regime and this report will simply provide an input to that process.

## 2. Test Parameters

The Introduction should outline the parameters of the security testing, the findings and remediation. Some suggested section headings include:

**2.1 Project Objective:** This section outlines the project objectives and the expected outcome of the assessment.

**2.2 Project Scope:** This section outlines the agreed scope.

**2.3 Project Schedule:** This section outlines when the testing commenced and when it was completed.

**2.4 Targets:** This section lists the number of applications or targeted systems.

**2.5 Limitations:** This section outlines every limitation which was faced throughout the assessment. For example, limitations of project-focused tests, limitation in the security testing methods, performance or technical issues that the tester come across during the course of assessment, etc.

**2.6 Findings Summary:** This section outlines the vulnerabilities that were discovered during testing.

**2.7 Remediation Summary:** This section outlines the action plan for fixing the vulnerabilities that were discovered during testing.

## 3. Findings

The last section of the report includes detailed technical information about the vulnerabilities found and the actions needed to resolve them. This section is aimed at a technical level and should include all the necessary information for the technical teams to understand the issue and resolve it. Each finding should be clear and concise and give the reader of the report a full understanding of the issue at hand.

The findings section should include:

- Screenshots and command lines to indicate what tasks were undertaken during the execution of the test case
- The affected item
- A technical description of the issue and the affected function or object
- A section on resolving the issue
- The severity rating, with vector notation if using [CVSS (Industry standard vulnerability severity and risk rankings)](http://www.first.org/cvss)

The following is the list of controls that were tested during the assessment:

| Test ID  | Test Description | Findings | Severity | Recommendations |
| ---------| -----------------| -------- | -------- | --------------- |
| **OTG-INFO**     | **Information Gathering**  |
| OTG-INFO-001 | Conduct Search Engine Discovery and Reconnaissance for Information Leakage |
| OTG-INFO-002 | Fingerprint Web Server |
| OTG-INFO-003 | Review Webserver Metafiles for Information |
| OTG-INFO-004 | Enumerate Applications on Webserver |
| OTG-INFO-005 | Review Webpage Comments and Metadata for Information Leakage |
| OTG-INFO-006 | Identify application entry points |
| OTG-INFO-007 | Map execution paths through application |
| OTG-INFO-009 | Fingerprint Web Application Framework |
| OTG-INFO-009 | Fingerprint Web Application |
| OTG-INFO-010 | Map Application Architecture |
| **OTG-CONFIG** | **Configuration and Deploy Management Testing** |
| OTG-CONFIG-001 | Test Network/Infrastructure Configuration |
| OTG-CONFIG-002 | Test Application Platform Configuration |
| OTG-CONFIG-003 | Test File Extensions Handling for Sensitive Information |
| OTG-CONFIG-004 | Backup and Unreferenced Files for Sensitive Information |
| OTG-CONFIG-005 | Enumerate Infrastructure and Application Admin Interfaces |
| OTG-CONFIG-006 | Test HTTP Methods |
| OTG-CONFIG-007 | Test HTTP Strict Transport Security |
| OTG-CONFIG-008 | Test RIA cross domain policy |
| **OTG-IDENT** | **Identity Management Testing** |
| OTG-IDENT-001 | Test Role Definitions |
| OTG-IDENT-002 | Test User Registration Process |
| OTG-IDENT-003 | Test Account Provisioning Process |
| OTG-IDENT-004 | Testing for Account Enumeration and Guessable User Account |
| OTG-IDENT-005 | Testing for Weak or unenforced username policy |
| OTG-IDENT-006 | Test Permissions of Guest/Training Accounts |
| OTG-IDENT-007 | Test Account Suspension/Resumption Process |
| **OTG-AUTHN** | **Authentication Testing** |
| OTG-AUTHN-001 | Testing for Credentials Transported over an Encrypted Channel |
| OTG-AUTHN-002 | Testing for default credentials |
| OTG-AUTHN-003 | Testing for Weak lock out mechanism |
| OTG-AUTHN-004 | Testing for bypassing authentication schema |
| OTG-AUTHN-005 | Test remember password functionality |
| OTG-AUTHN-006 | Testing for Browser cache weakness |
| OTG-AUTHN-007 | Testing for Weak password policy |
| OTG-AUTHN-008 | Testing for Weak security question/answer |
| OTG-AUTHN-009 | Testing for weak password change or reset functionalities |
| OTG-AUTHN-010 | Testing for Weaker authentication in alternative channel |
| **OTG-AUTHZ** | **Authorization Testing** |
| OTG-AUTHZ-001 | Testing Directory traversal/file include |
| OTG-AUTHZ-002 | Testing for bypassing authorization schema |
| OTG-AUTHZ-003 | Testing for Privilege Escalation |
| OTG-AUTHZ-004 | Testing for Insecure Direct Object References |
| **OTG-SESS** | **Session Management Testing** |
| OTG-SESS-001 | Testing for Bypassing Session Management Schema |
| OTG-SESS-002 | Testing for Cookies attributes |
| OTG-SESS-003 | Testing for Session Fixation |
| OTG-SESS-004 | Testing for Exposed Session Variables |
| OTG-SESS-005 | Testing for Cross Site Request Forgery |
| OTG-SESS-006 | Testing for logout functionality |
| OTG-SESS-007 | Test Session Timeout |
| OTG-SESS-008 | Testing for Session puzzling |
| **OTG-INPVAL** |**Input Validation Testing** |
| OTG-INPVAL-001 | Testing for Reflected Cross Site Scripting |
| OTG-INPVAL-002 | Testing for Stored Cross Site Scripting |
| OTG-INPVAL-003 | Testing for HTTP Verb Tampering |
| OTG-INPVAL-004 | Testing for HTTP Parameter pollution |
| OTG-INPVAL-005 | Testing for SQL Injection |
| | Oracle Testing |
| | MySQL Testing   |
| | SQL Server Testing |
| | Testing PostgreSQL |
| | MS Access Testing |
| | Testing for NoSQL injection |
| OTG-INPVAL-006 | Testing for LDAP Injection |
| OTG-INPVAL-007 | Testing for ORM Injection |
| OTG-INPVAL-008 | Testing for XML Injection |
| OTG-INPVAL-008 | Testing for SSI Injection |
| OTG-INPVAL-010 | Testing for XPath Injection |
| OTG-INPVAL-011 | IMAP/SMTP Injection |
| OTG-INPVAL-012 |Testing for Code Injection |
| |Testing for Local File Inclusion |
| |Testing for Remote File Inclusion |
| OTG-INPVAL-013 | Testing for Command Injection |
| OTG-INPVAL-014 | Testing for Buffer overflow |
| | Testing for Heap overflow |
| | Testing for Stack overflow |
| | Testing for Format string |
| OTG-INPVAL-015  | Testing for incubated vulnerabilities |
| OTG-INPVAL-016  | Testing for HTTP Splitting/Smuggling |
| OTG-INPVAL-017  | Testing for HTTP Incoming requests |
| **OTG-ERR**  |**Error Handling** |
| OTG-ERR-001  | Analysis of Error Codes |
| OTG-ERR-002  | Analysis of Stack Traces |
| **OTG-CRYPST** | **Cryptography** |
| OTG-CRYPST-001 | Testing for Weak SSL/TSL Ciphers, Insufficient|
| **OTG-CRYPST** | **Transport Layer Protection** |
| OTG-CRYPST-002 | Testing for Padding Oracle |
| OTG-CRYPST-003 | Testing for Sensitive information sent via unencrypted  channels |
| **OTG-BUSLOGIC** | **Business Logic Testing** |
| OTG-BUSLOGIC-001 | Test Business Logic Data Validation |
| OTG-BUSLOGIC-002 | Test Ability to Forge Requests |
| OTG-BUSLOGIC-003 | Test Integrity Checks |
| OTG-BUSLOGIC-004 | Test for Process Timing |
| OTG-BUSLOGIC-005 | Test Number of Times a Function Can be Used Limits |
| OTG-BUSLOGIC-006 | Testing for the Circumvention of Work Flows |
| OTG-BUSLOGIC-007 | Test Defenses Against Application Mis-use |
| OTG-BUSLOGIC-008 | Test Upload of Unexpected File Types |
| OTG-BUSLOGIC-009 | Test Upload of Malicious Files |
| **OTG-CLIENT** | **Client Side Testing** |
| OTG-CLIENT-001 | Testing for DOM based Cross Site Scripting |
| OTG-CLIENT-002 | Testing for JavaScript Execution |
| OTG-CLIENT-003 | Testing for HTML Injection |
| OTG-CLIENT-004 | Testing for Client Side URL Redirect |
| OTG-CLIENT-005 | Testing for CSS Injection |
| OTG-CLIENT-006 | Testing for Client Side Resource Manipulation |
| OTG-CLIENT-007 | Test Cross Origin Resource Sharing |
| OTG-CLIENT-008 | Testing for Cross Site Flashing |
| OTG-CLIENT-009 | Testing for Clickjacking |
| OTG-CLIENT-010 | Testing WebSockets |
| OTG-CLIENT-011 | Test Web Messaging |
| OTG-CLIENT-012 | Test Local Storage |

## Appendix

This section is often used to describe the commercial and open-source tools that were used in conducting the assessment. When custom scripts or code are utilized during the assessment, it should be disclosed in this section or noted as attachment. Customers appreciate when the methodology used by the consultants is included. It gives them an idea of the thoroughness of the assessment and what areas were included.
