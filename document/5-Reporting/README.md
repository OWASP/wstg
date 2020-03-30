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
| **WSTG-INFO**     | **Information Gathering**  |
| WSTG-INFO-01 | Conduct Search Engine Discovery and Reconnaissance for Information Leakage |
| WSTG-INFO-02 | Fingerprint Web Server |
| WSTG-INFO-03 | Review Webserver Metafiles for Information |
| WSTG-INFO-04 | Enumerate Applications on Webserver |
| WSTG-INFO-05 | Review Webpage Comments and Metadata for Information Leakage |
| WSTG-INFO-06 | Identify application entry points |
| WSTG-INFO-07 | Map execution paths through application |
| WSTG-INFO-09 | Fingerprint Web Application Framework |
| WSTG-INFO-09 | Fingerprint Web Application |
| WSTG-INFO-10 | Map Application Architecture |
| **WSTG-CONFIG** | **Configuration and Deploy Management Testing** |
| WSTG-CONF-01 | Test Network/Infrastructure Configuration |
| WSTG-CONF-02 | Test Application Platform Configuration |
| WSTG-CONF-03 | Test File Extensions Handling for Sensitive Information |
| WSTG-CONF-04 | Backup and Unreferenced Files for Sensitive Information |
| WSTG-CONF-05 | Enumerate Infrastructure and Application Admin Interfaces |
| WSTG-CONF-06 | Test HTTP Methods |
| WSTG-CONF-07 | Test HTTP Strict Transport Security |
| WSTG-CONF-08 | Test RIA cross domain policy |
| **WSTG-IDENT** | **Identity Management Testing** |
| WSTG-IDENT-001 | Test Role Definitions |
| WSTG-IDENT-002 | Test User Registration Process |
| WSTG-IDENT-003 | Test Account Provisioning Process |
| WSTG-IDENT-004 | Testing for Account Enumeration and Guessable User Account |
| WSTG-IDENT-005 | Testing for Weak or unenforced username policy |
| WSTG-IDENT-006 | Test Permissions of Guest/Training Accounts |
| WSTG-IDENT-007 | Test Account Suspension/Resumption Process |
| **WSTG-AUTHN** | **Authentication Testing** |
| WSTG-AUTHN-001 | Testing for Credentials Transported over an Encrypted Channel |
| WSTG-AUTHN-002 | Testing for default credentials |
| WSTG-AUTHN-003 | Testing for Weak lock out mechanism |
| WSTG-AUTHN-004 | Testing for bypassing authentication schema |
| WSTG-AUTHN-005 | Test remember password functionality |
| WSTG-AUTHN-006 | Testing for Browser cache weakness |
| WSTG-AUTHN-007 | Testing for Weak password policy |
| WSTG-AUTHN-008 | Testing for Weak security question/answer |
| WSTG-AUTHN-009 | Testing for weak password change or reset functionalities |
| WSTG-AUTHN-010 | Testing for Weaker authentication in alternative channel |
| **WSTG-AUTHZ** | **Authorization Testing** |
| WSTG-AUTHZ-001 | Testing Directory traversal/file include |
| WSTG-AUTHZ-002 | Testing for bypassing authorization schema |
| WSTG-AUTHZ-003 | Testing for Privilege Escalation |
| WSTG-AUTHZ-004 | Testing for Insecure Direct Object References |
| **WSTG-SESS** | **Session Management Testing** |
| WSTG-SESS-001 | Testing for Bypassing Session Management Schema |
| WSTG-SESS-002 | Testing for Cookies attributes |
| WSTG-SESS-003 | Testing for Session Fixation |
| WSTG-SESS-004 | Testing for Exposed Session Variables |
| WSTG-SESS-005 | Testing for Cross Site Request Forgery |
| WSTG-SESS-006 | Testing for logout functionality |
| WSTG-SESS-007 | Test Session Timeout |
| WSTG-SESS-008 | Testing for Session puzzling |
| **WSTG-INPVAL** |**Input Validation Testing** |
| WSTG-INPVAL-001 | Testing for Reflected Cross Site Scripting |
| WSTG-INPVAL-002 | Testing for Stored Cross Site Scripting |
| WSTG-INPVAL-003 | Testing for HTTP Verb Tampering |
| WSTG-INPVAL-004 | Testing for HTTP Parameter pollution |
| WSTG-INPVAL-005 | Testing for SQL Injection |
| | Oracle Testing |
| | MySQL Testing   |
| | SQL Server Testing |
| | Testing PostgreSQL |
| | MS Access Testing |
| | Testing for NoSQL injection |
| WSTG-INPVAL-006 | Testing for LDAP Injection |
| WSTG-INPVAL-007 | Testing for ORM Injection |
| WSTG-INPVAL-008 | Testing for XML Injection |
| WSTG-INPVAL-008 | Testing for SSI Injection |
| WSTG-INPVAL-010 | Testing for XPath Injection |
| WSTG-INPVAL-011 | IMAP/SMTP Injection |
| WSTG-INPVAL-012 |Testing for Code Injection |
| |Testing for Local File Inclusion |
| |Testing for Remote File Inclusion |
| WSTG-INPVAL-013 | Testing for Command Injection |
| WSTG-INPVAL-014 | Testing for Buffer overflow |
| | Testing for Heap overflow |
| | Testing for Stack overflow |
| | Testing for Format string |
| WSTG-INPVAL-015  | Testing for incubated vulnerabilities |
| WSTG-INPVAL-016  | Testing for HTTP Splitting/Smuggling |
| WSTG-INPVAL-017  | Testing for HTTP Incoming requests |
| **WSTG-ERR**  |**Error Handling** |
| WSTG-ERR-001  | Analysis of Error Codes |
| WSTG-ERR-002  | Analysis of Stack Traces |
| **WSTG-CRYPST** | **Cryptography** |
| WSTG-CRYPST-001 | Testing for Weak SSL/TSL Ciphers, Insufficient|
| **WSTG-CRYPST** | **Transport Layer Protection** |
| WSTG-CRYPST-002 | Testing for Padding Oracle |
| WSTG-CRYPST-003 | Testing for Sensitive information sent via unencrypted  channels |
| **WSTG-BUSLOGIC** | **Business Logic Testing** |
| WSTG-BUSLOGIC-001 | Test Business Logic Data Validation |
| WSTG-BUSLOGIC-002 | Test Ability to Forge Requests |
| WSTG-BUSLOGIC-003 | Test Integrity Checks |
| WSTG-BUSLOGIC-004 | Test for Process Timing |
| WSTG-BUSLOGIC-005 | Test Number of Times a Function Can be Used Limits |
| WSTG-BUSLOGIC-006 | Testing for the Circumvention of Work Flows |
| WSTG-BUSLOGIC-007 | Test Defenses Against Application Mis-use |
| WSTG-BUSLOGIC-008 | Test Upload of Unexpected File Types |
| WSTG-BUSLOGIC-009 | Test Upload of Malicious Files |
| **WSTG-CLIENT** | **Client Side Testing** |
| WSTG-CLIENT-001 | Testing for DOM based Cross Site Scripting |
| WSTG-CLIENT-002 | Testing for JavaScript Execution |
| WSTG-CLIENT-003 | Testing for HTML Injection |
| WSTG-CLIENT-004 | Testing for Client Side URL Redirect |
| WSTG-CLIENT-005 | Testing for CSS Injection |
| WSTG-CLIENT-006 | Testing for Client Side Resource Manipulation |
| WSTG-CLIENT-007 | Test Cross Origin Resource Sharing |
| WSTG-CLIENT-008 | Testing for Cross Site Flashing |
| WSTG-CLIENT-009 | Testing for Clickjacking |
| WSTG-CLIENT-010 | Testing WebSockets |
| WSTG-CLIENT-011 | Test Web Messaging |
| WSTG-CLIENT-012 | Test Local Storage |

## Appendix

This section is often used to describe the commercial and open-source tools that were used in conducting the assessment. When custom scripts or code are utilized during the assessment, it should be disclosed in this section or noted as attachment. Customers appreciate when the methodology used by the consultants is included. It gives them an idea of the thoroughness of the assessment and what areas were included.
