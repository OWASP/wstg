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
| **WSTG-INFO** | **Information Gathering** |
| WSTG-INFO-01 | Conduct Search Engine Discovery and Reconnaissance for Information Leakage |
| WSTG-INFO-02 | Fingerprint Web Server |
| WSTG-INFO-03 | Review Webserver Metafiles for Information |
| WSTG-INFO-04 | Enumerate Applications on Webserver |
| WSTG-INFO-05 | Review Webpage Comments and Metadata for Information Leakage |
| WSTG-INFO-06 | Identify Application Entry Points |
| WSTG-INFO-07 | Map Execution Paths Through Application |
| WSTG-INFO-09 | Fingerprint Web Application Framework |
| WSTG-INFO-09 | Fingerprint Web Application |
| WSTG-INFO-10 | Map Application Architecture |
| **WSTG-CONF** | **Configuration and Deploy Management Testing** |
| WSTG-CONF-01 | Test Network Infrastructure Configuration |
| WSTG-CONF-02 | Test Application Platform Configuration |
| WSTG-CONF-03 | Test File Extensions Handling for Sensitive Information |
| WSTG-CONF-04 | Backup and Unreferenced Files for Sensitive Information |
| WSTG-CONF-05 | Enumerate Infrastructure and Application Admin Interfaces |
| WSTG-CONF-06 | Test HTTP Methods |
| WSTG-CONF-07 | Test HTTP Strict Transport Security |
| WSTG-CONF-08 | Test RIA Cross Domain Policy |
| WSTG-CONF-09 | Test File Permission |
| WSTG-CONF-10 | Test for Subdomain Takeover |
| WSTG-CONF-11 | Test Cloud Storage |
| **WSTG-IDNT** | **Identity Management Testing** |
| WSTG-IDNT-01 | Test Role Definitions |
| WSTG-IDNT-02 | Test User Registration Process |
| WSTG-IDNT-03 | Test Account Provisioning Process |
| WSTG-IDNT-04 | Testing for Account Enumeration and Guessable User Account |
| WSTG-IDNT-05 | Testing for Weak or Unenforced Username Policy |
| **WSTG-ATHN** | **Authentication Testing** |
| WSTG-ATHN-01 | Testing for Credentials Transported over an Encrypted Channel |
| WSTG-ATHN-02 | Testing for Default Credentials |
| WSTG-ATHN-03 | Testing for Weak Lock Out Mechanism |
| WSTG-ATHN-04 | Testing for Bypassing Authentication Schema |
| WSTG-ATHN-05 | Testing for Vulnerable Remember Password |
| WSTG-ATHN-06 | Testing for Browser Cache Weakness |
| WSTG-ATHN-07 | Testing for Weak Password Policy |
| WSTG-ATHN-08 | Testing for Weak Security Question Answer |
| WSTG-ATHN-09 | Testing for Weak Password Change or Reset Functionalities |
| WSTG-ATHN-10 | Testing for Weaker Authentication in Alternative Channel |
| **WSTG-ATHZ** | **Authorization Testing** |
| WSTG-ATHZ-01 | Testing Directory Traversal - File Include |
| WSTG-ATHZ-02 | Testing for Bypassing Authorization Schema |
| WSTG-ATHZ-03 | Testing for Privilege Escalation |
| WSTG-ATHZ-04 | Testing for Insecure Direct Object References |
| **WSTG-SESS** | **Session Management Testing** |
| WSTG-SESS-01 | Testing for Bypassing Session Management Schema |
| WSTG-SESS-02 | Testing for Cookies Attributes |
| WSTG-SESS-03 | Testing for Session Fixation |
| WSTG-SESS-04 | Testing for Exposed Session Variables |
| WSTG-SESS-05 | Testing for Cross Site Request Forgery |
| WSTG-SESS-06 | Testing for Logout Functionality |
| WSTG-SESS-07 | Test Session Timeout |
| WSTG-SESS-08 | Testing for Session Puzzling |
| **WSTG-INPV** |**Input Validation Testing** |
| WSTG-INPV-01 | Testing for Reflected Cross Site Scripting |
| WSTG-INPV-02 | Testing for Stored Cross Site Scripting |
| WSTG-INPV-03 | Testing for HTTP Verb Tampering |
| WSTG-INPV-04 | Testing for HTTP Parameter pollution |
| WSTG-INPV-05 | Testing for SQL Injection |
| | Oracle |
| | MySQL |
| | SQL Server |
| | PostgreSQL |
| | MS Access |
| | NoSQL |
| | ORM |
| | Client-side |
| WSTG-INPV-06 | Testing for LDAP Injection |
| WSTG-INPV-07 | Testing for XML Injection |
| WSTG-INPV-08 | Testing for SSI Injection |
| WSTG-INPV-09 | Testing for XPath Injection |
| WSTG-INPV-10 | IMAP/SMTP Injection |
| WSTG-INPV-11 | Testing for Code Injection |
| |Testing for Local File Inclusion |
| |Testing for Remote File Inclusion |
| WSTG-INPV-12 | Testing for Command Injection |
| WSTG-INPV-13 | Testing for Buffer overflow |
| | Testing for Heap Overflow |
| | Testing for Stack Overflow |
| | Testing for Format String |
| WSTG-INPV-14 | Testing for Incubated Vulnerabilities |
| WSTG-INPV-15 | Testing for HTTP Splitting/Smuggling |
| WSTG-INPV-16 | Testing for HTTP Incoming Requests |
| WSTG-INPV-17 | Testing for Host Header Injection |
| WSTG-INPV-18 | Testing for Server-side Template Injection |
| **WSTG-ERRH**  |**Error Handling** |
| WSTG-ERRH-01  | Analysis of Error Codes |
| WSTG-ERRH-02  | Analysis of Stack Traces |
| **WSTG-CRYP** | **Cryptography** |
| WSTG-CRYP-01 | Testing for Weak Transport Layer Security |
| WSTG-CRYP-02 | Testing for Padding Oracle |
| WSTG-CRYP-03 | Testing for Sensitive Information Sent Via Unencrypted Channels |
| WSTG-CRYP-04 | Testing for Weak Encryption |
| **WSTG-BUSLOGIC** | **Business Logic Testing** |
| WSTG-BUSL-01 | Test Business Logic Data Validation |
| WSTG-BUSL-02 | Test Ability to Forge Requests |
| WSTG-BUSL-03 | Test Integrity Checks |
| WSTG-BUSL-04 | Test for Process Timing |
| WSTG-BUSL-05 | Test Number of Times a Function Can be Used Limits |
| WSTG-BUSL-06 | Testing for the Circumvention of Work Flows |
| WSTG-BUSL-07 | Test Defenses Against Application Misuse |
| WSTG-BUSL-08 | Test Upload of Unexpected File Types |
| WSTG-BUSL-09 | Test Upload of Malicious Files |
| **WSTG-CLIENT** | **Client-side Testing** |
| WSTG-CLNT-01 | Testing for DOM based Cross Site Scripting |
| WSTG-CLNT-02 | Testing for JavaScript Execution |
| WSTG-CLNT-03 | Testing for HTML Injection |
| WSTG-CLNT-04 | Testing for Client-side URL Redirect |
| WSTG-CLNT-05 | Testing for CSS Injection |
| WSTG-CLNT-06 | Testing for Client-side Resource Manipulation |
| WSTG-CLNT-07 | Test Cross Origin Resource Sharing |
| WSTG-CLNT-08 | Testing for Cross Site Flashing |
| WSTG-CLNT-09 | Testing for Clickjacking |
| WSTG-CLNT-10 | Testing WebSockets |
| WSTG-CLNT-11 | Test Web Messaging |
| WSTG-CLNT-12 | Test Local Storage |
| WSTG-CLNT-13 | Testing for Cross Site Script Inclusion |

## Appendix

This section is often used to describe the commercial and open-source tools that were used in conducting the assessment. When custom scripts or code are utilized during the assessment, it should be disclosed in this section or noted as attachment. Customers appreciate when the methodology used by the consultants is included. It gives them an idea of the thoroughness of the assessment and what areas were included.
