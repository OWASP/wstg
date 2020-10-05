# Testing Checklist

The following is the list of controls to test during the assessment:

| Ref. No. | Category     | Test Name                  |
|----------|--------------|----------------------------|
| **4.1** | **WSTG-INFO** | **Information Gathering** |
| 4.1.1 | WSTG-INFO-01 | Conduct Search Engine Discovery and Reconnaissance for Information Leakage |
| 4.1.2 | WSTG-INFO-02 | Fingerprint Web Server |
| 4.1.3 | WSTG-INFO-03 | Review Webserver Metafiles for Information Leakage |
| 4.1.4 | WSTG-INFO-04 | Enumerate Applications on Webserver |
| 4.1.5 | WSTG-INFO-05 | Review Webpage Comments and Metadata for Information Leakage |
| 4.1.6 | WSTG-INFO-06 | Identify Application Entry Points |
| 4.1.7 | WSTG-INFO-07 | Map Execution Paths Through Application |
| 4.1.8 | WSTG-INFO-09 | Fingerprint Web Application Framework |
| 4.1.9 | WSTG-INFO-09 | Fingerprint Web Application |
| 4.1.10 | WSTG-INFO-10 | Map Application Architecture |
| **4.2** | **WSTG-CONF** | **Configuration and Deploy Management Testing** |
| 4.2.1 | WSTG-CONF-01 | Test Network Infrastructure Configuration |
| 4.2.2 | WSTG-CONF-02 | Test Application Platform Configuration |
| 4.2.3 | WSTG-CONF-03 | Test File Extensions Handling for Sensitive Information |
| 4.2.4 | WSTG-CONF-04 | Backup and Unreferenced Files for Sensitive Information |
| 4.2.5 | WSTG-CONF-05 | Enumerate Infrastructure and Application Admin Interfaces |
| 4.2.6 | WSTG-CONF-06 | Test HTTP Methods |
| 4.2.7 | WSTG-CONF-07 | Test HTTP Strict Transport Security |
| 4.2.8 | WSTG-CONF-08 | Test RIA Cross Domain Policy |
| 4.2.9 | WSTG-CONF-09 | Test File Permission |
| 4.2.10 | WSTG-CONF-10 | Test for Subdomain Takeover |
| 4.2.11 | WSTG-CONF-11 | Test Cloud Storage |
| **4.3** | **WSTG-IDNT** | **Identity Management Testing** |
| 4.3.1 | WSTG-IDNT-01 | Test Role Definitions |
| 4.3.2 | WSTG-IDNT-02 | Test User Registration Process |
| 4.3.3 | WSTG-IDNT-03 | Test Account Provisioning Process |
| 4.3.4 | WSTG-IDNT-04 | Testing for Account Enumeration and Guessable User Account |
| 4.3.5 | WSTG-IDNT-05 | Testing for Weak or Unenforced Username Policy |
| **4.4** | **WSTG-ATHN** | **Authentication Testing** |
| 4.4.1 | WSTG-ATHN-01 | Testing for Credentials Transported over an Encrypted Channel |
| 4.4.2 | WSTG-ATHN-02 | Testing for Default Credentials |
| 4.4.3 | WSTG-ATHN-03 | Testing for Weak Lock Out Mechanism |
| 4.4.4 | WSTG-ATHN-04 | Testing for Bypassing Authentication Schema |
| 4.4.5 | WSTG-ATHN-05 | Testing for Vulnerable Remember Password |
| 4.4.6 | WSTG-ATHN-06 | Testing for Browser Cache Weakness |
| 4.4.7 | WSTG-ATHN-07 | Testing for Weak Password Policy |
| 4.4.8 | WSTG-ATHN-08 | Testing for Weak Security Question Answer |
| 4.4.9 | WSTG-ATHN-09 | Testing for Weak Password Change or Reset Functionalities |
| 4.4.10 | WSTG-ATHN-10 | Testing for Weaker Authentication in Alternative Channel |
| **4.5** | **WSTG-ATHZ** | **Authorization Testing** |
| 4.5.1 | WSTG-ATHZ-01 | Testing Directory Traversal - File Include |
| 4.5.2 | WSTG-ATHZ-02 | Testing for Bypassing Authorization Schema |
| 4.5.3 | WSTG-ATHZ-03 | Testing for Privilege Escalation |
| 4.5.4 | WSTG-ATHZ-04 | Testing for Insecure Direct Object References |
| **4.6** | **WSTG-SESS** | **Session Management Testing** |
| 4.6.1 | WSTG-SESS-01 | Testing for Bypassing Session Management Schema |
| 4.6.2 | WSTG-SESS-02 | Testing for Cookies Attributes |
| 4.6.3 | WSTG-SESS-03 | Testing for Session Fixation |
| 4.6.4 | WSTG-SESS-04 | Testing for Exposed Session Variables |
| 4.6.5 | WSTG-SESS-05 | Testing for Cross Site Request Forgery |
| 4.6.6 | WSTG-SESS-06 | Testing for Logout Functionality |
| 4.6.7 | WSTG-SESS-07 | Test Session Timeout |
| 4.6.8 | WSTG-SESS-08 | Testing for Session Puzzling |
| **4.7** | **WSTG-INPV** |**Input Validation Testing** |
| 4.7.1 | WSTG-INPV-01 | Testing for Reflected Cross Site Scripting |
| 4.7.2 | WSTG-INPV-02 | Testing for Stored Cross Site Scripting |
| 4.7.3 | WSTG-INPV-03 | Testing for HTTP Verb Tampering |
| 4.7.4 | WSTG-INPV-04 | Testing for HTTP Parameter pollution |
| 4.7.5 | WSTG-INPV-05 | Testing for SQL Injection |
| 4.7.5.1 | | Oracle |
| 4.7.5.2 | | MySQL |
| 4.7.5.3 | | SQL Server |
| 4.7.5.4 | | PostgreSQL |
| 4.7.5.5 | | MS Access |
| 4.7.5.6 | | NoSQL |
| 4.7.5.7 | | ORM |
| 4.7.5.8 | | Client Side |
| 4.7.6 | WSTG-INPV-06 | Testing for LDAP Injection |
| 4.7.7 | WSTG-INPV-07 | Testing for XML Injection |
| 4.7.8 | WSTG-INPV-08 | Testing for SSI Injection |
| 4.7.9 | WSTG-INPV-09 | Testing for XPath Injection |
| 4.7.10 | WSTG-INPV-10 | IMAP/SMTP Injection |
| 4.7.11 | WSTG-INPV-11 | Testing for Code Injection |
| 4.7.11.1 | |Testing for Local File Inclusion |
| 4.7.11.2 | |Testing for Remote File Inclusion |
| 4.7.12 | WSTG-INPV-12 | Testing for Command Injection |
| 4.7.13 | WSTG-INPV-13 | Testing for Buffer overflow |
| 4.7.13.1 | | Testing for Heap Overflow |
| 4.7.13.2 | | Testing for Stack Overflow |
| 4.7.13.3 | | Testing for Format String |
| 4.7.14 | WSTG-INPV-14 | Testing for Incubated Vulnerabilities |
| 4.7.15 | WSTG-INPV-15 | Testing for HTTP Splitting/Smuggling |
| 4.7.16 | WSTG-INPV-16 | Testing for HTTP Incoming Requests |
| 4.7.17 | WSTG-INPV-17 | Testing for Host Header Injection |
| 4.7.18 | WSTG-INPV-18 | Testing for Server Side Template Injection |
| **4.8** | **WSTG-ERRH** |**Error Handling** |
| 4.8.1 | WSTG-ERRH-01 | Analysis of Error Codes |
| 4.8.2 | WSTG-ERRH-02 | Analysis of Stack Traces |
| **4.9** | **WSTG-CRYP** | **Cryptography** |
| 4.9.1 | WSTG-CRYP-01 | Testing for Weak Transport Layer Security |
| 4.9.2 | WSTG-CRYP-02 | Testing for Padding Oracle |
| 4.9.3 | WSTG-CRYP-03 | Testing for Sensitive Information Sent Via Unencrypted Channels |
| 4.9.4 | WSTG-CRYP-04 | Testing for Weak Encryption |
| **4.10** | **WSTG-BUSLOGIC** | **Business Logic Testing** |
| 4.10.1 | WSTG-BUSL-01 | Test Business Logic Data Validation |
| 4.10.2 | WSTG-BUSL-02 | Test Ability to Forge Requests |
| 4.10.3 | WSTG-BUSL-03 | Test Integrity Checks |
| 4.10.4 | WSTG-BUSL-04 | Test for Process Timing |
| 4.10.5 | WSTG-BUSL-05 | Test Number of Times a Function Can be Used Limits |
| 4.10.6 | WSTG-BUSL-06 | Testing for the Circumvention of Work Flows |
| 4.10.7 | WSTG-BUSL-07 | Test Defenses Against Application Misuse |
| 4.10.8 | WSTG-BUSL-08 | Test Upload of Unexpected File Types |
| 4.10.9 | WSTG-BUSL-09 | Test Upload of Malicious Files |
| **4.11** | **WSTG-CLIENT** | **Client Side Testing** |
| 4.11.1 | WSTG-CLNT-01 | Testing for DOM based Cross Site Scripting |
| 4.11.2 | WSTG-CLNT-02 | Testing for JavaScript Execution |
| 4.11.3 | WSTG-CLNT-03 | Testing for HTML Injection |
| 4.11.4 | WSTG-CLNT-04 | Testing for Client Side URL Redirect |
| 4.11.5 | WSTG-CLNT-05 | Testing for CSS Injection |
| 4.11.6 | WSTG-CLNT-06 | Testing for Client Side Resource Manipulation |
| 4.11.7 | WSTG-CLNT-07 | Test Cross Origin Resource Sharing |
| 4.11.8 | WSTG-CLNT-08 | Testing for Cross Site Flashing |
| 4.11.9 | WSTG-CLNT-09 | Testing for Clickjacking |
| 4.11.10 | WSTG-CLNT-10 | Testing WebSockets |
| 4.11.11 | WSTG-CLNT-11 | Test Web Messaging |
| 4.11.12 | WSTG-CLNT-12 | Test Local Storage |
| 4.11.13 | WSTG-CLNT-13 | Testing for Cross Site Script Inclusion |
