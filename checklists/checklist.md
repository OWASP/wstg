# Testing Checklist

The following is the list of items to test during the assessment:

> Note: The `Status` column can be set for values similar to "Pass", "Fail", "N/A".

| Test ID           | Test Name                                                                  | Status | Notes |
|-------------------|----------------------------------------------------------------------------|--------|-------|
| **WSTG-INFO**     | **Information Gathering**                                                  |        |       |
| WSTG-INFO-01      | Conduct Search Engine Reconnaissance for Information Leakage               |        |       |
| WSTG-INFO-02      | Fingerprint Web Server                                                     |        |       |
| WSTG-INFO-03      | Review Webserver Metafiles for Information Leakage                         |        |       |
| WSTG-INFO-04      | Attack Surface Identification                                              |        |       |
| WSTG-INFO-05      | Review Web Page Content for Information Leakage                            |        |       |
| WSTG-INFO-06      | Identify Application Entry Points                                          |        |       |
| WSTG-INFO-07      | Map Execution Paths Through Application                                    |        |       |
| WSTG-INFO-08      | Fingerprint Web Application Framework                                      |        |       |
| WSTG-INFO-09      | Map Application Architecture                                               |        |       |
| **WSTG-CONF**     | **Configuration and Deployment Management**                                |        |       |
| WSTG-CONF-01      | Network Infrastructure Configuration                                       |        |       |
| WSTG-CONF-02      | Application Platform Configuration                                         |        |       |
| WSTG-CONF-03      | Review Old Backup and Unreferenced Files for Sensitive Information         |        |       |
| WSTG-CONF-04      | Enumerate Infrastructure and Application Admin Interfaces                  |        |       |
| WSTG-CONF-05      | HTTP Methods                                                               |        |       |
| WSTG-CONF-06      | HTTP Strict Transport Security                                             |        |       |
| WSTG-CONF-07      | File Permissions                                                           |        |       |
| WSTG-CONF-08      | Subdomain Takeover                                                         |        |       |
| WSTG-CONF-09      | Cloud Storage                                                              |        |       |
| WSTG-CONF-10      | Content Security Policy                                                    |        |       |
| WSTG-CONF-11      | Path Confusion                                                             |        |       |
| WSTG-CONF-12      | Additional Browser Security Controls                                       |        |       |
| WSTG-CONF-13      | Feature Flag Security Bypass                                               |        |       |
| WSTG-CONF-14      | Web Cache Poisoning                                                        |        |       |
| **WSTG-IDNT**     | **Identity Management**                                                    |        |       |
| WSTG-IDNT-01      | Role Definitions                                                           |        |       |
| WSTG-IDNT-02      | User Registration Process                                                  |        |       |
| WSTG-IDNT-03      | Account Provisioning Process                                               |        |       |
| WSTG-IDNT-04      | Account Enumeration and Guessable User Account                             |        |       |
| WSTG-IDNT-05      | Email Address Verification                                                 |        |       |
| **WSTG-ATHN**     | **Authentication**                                                         |        |       |
| WSTG-ATHN-01      | Default Credentials                                                        |        |       |
| WSTG-ATHN-02      | Weak Lock Out Mechanism                                                    |        |       |
| WSTG-ATHN-03      | Bypassing Authentication Schema                                            |        |       |
| WSTG-ATHN-04      | Vulnerable Remember Password                                               |        |       |
| WSTG-ATHN-05      | Browser Cache Weaknesses                                                   |        |       |
| WSTG-ATHN-06      | Weak Authentication Methods                                                |        |       |
| WSTG-ATHN-07      | Weak Security Question Answer                                              |        |       |
| WSTG-ATHN-08      | Weak Password Change or Reset Functionalities                              |        |       |
| WSTG-ATHN-09      | Weaker Authentication in Alternative Channel                               |        |       |
| WSTG-ATHN-10      | Multi-Factor Authentication (MFA)                                          |        |       |
| WSTG-ATHN-11      | SAML Authentication                                                        |        |       |
| WSTG-ATHN-12      | Passkeys and WebAuthn                                                      |        |       |
| WSTG-ATHN-13      | OpenID Connect Relying Party                                               |        |       |
| **WSTG-ATHZ**     | **Authorization**                                                          |        |       |
| WSTG-ATHZ-01      | Directory Traversal and File Include                                       |        |       |
| WSTG-ATHZ-02      | Bypassing Authorization Schema                                             |        |       |
| WSTG-ATHZ-03      | Privilege Escalation                                                       |        |       |
| WSTG-ATHZ-04      | Insecure Direct Object References                                          |        |       |
| WSTG-ATHZ-05      | OAuth Weaknesses                                                           |        |       |
| **WSTG-SESS**     | **Session Management**                                                     |        |       |
| WSTG-SESS-01      | Session Management Schema                                                  |        |       |
| WSTG-SESS-02      | Cookies Attributes                                                         |        |       |
| WSTG-SESS-03      | Session Fixation                                                           |        |       |
| WSTG-SESS-04      | Exposed Session Variables                                                  |        |       |
| WSTG-SESS-05      | Cross Site Request Forgery                                                 |        |       |
| WSTG-SESS-06      | Logout Functionality                                                       |        |       |
| WSTG-SESS-07      | Session Timeout                                                            |        |       |
| WSTG-SESS-08      | Session Puzzling                                                           |        |       |
| WSTG-SESS-09      | Session Hijacking                                                          |        |       |
| WSTG-SESS-10      | JSON Web Tokens                                                            |        |       |
| WSTG-SESS-11      | Concurrent Sessions                                                        |        |       |
| **WSTG-INJT**     | **Injection**                                                              |        |       |
| WSTG-INJT-01      | Reflected Cross Site Scripting                                             |        |       |
| WSTG-INJT-02      | Stored Cross Site Scripting                                                |        |       |
| WSTG-INJT-03      | HTTP Parameter Pollution                                                   |        |       |
| WSTG-INJT-04      | SQL Injection                                                              |        |       |
| WSTG-INJT-05      | LDAP Injection                                                             |        |       |
| WSTG-INJT-06      | XML Injection                                                              |        |       |
| WSTG-INJT-07      | SSI Injection                                                              |        |       |
| WSTG-INJT-08      | XPath Injection                                                            |        |       |
| WSTG-INJT-09      | IMAP SMTP Injection                                                        |        |       |
| WSTG-INJT-10      | Code Injection                                                             |        |       |
| WSTG-INJT-11      | Command Injection                                                          |        |       |
| WSTG-INJT-12      | Format String Injection                                                    |        |       |
| WSTG-INJT-13      | Incubated Vulnerability                                                    |        |       |
| WSTG-INJT-14      | HTTP Response Splitting                                                    |        |       |
| WSTG-INJT-15      | HTTP Request Smuggling                                                     |        |       |
| WSTG-INJT-16      | Host Header Injection                                                      |        |       |
| WSTG-INJT-17      | Server-side Template Injection                                             |        |       |
| WSTG-INJT-18      | Server-Side Request Forgery                                                |        |       |
| WSTG-INJT-19      | Mass Assignment                                                            |        |       |
| WSTG-INJT-20      | CSV Injection                                                              |        |       |
| WSTG-INJT-21      | Prototype Pollution                                                        |        |       |
| WSTG-INJT-22      | Insecure Deserialization                                                   |        |       |
| WSTG-INJT-23      | Server-side URL Redirect                                                   |        |       |
| WSTG-INJT-24      | Unicode Normalization and Case Mapping                                     |        |       |
| WSTG-INJT-25      | JSON Parser Differentials                                                  |        |       |
| WSTG-INJT-26      | Server-side Document Rendering Injection                                   |        |       |
| WSTG-INJT-27      | Regular Expression Denial of Service                                       |        |       |
| **WSTG-ERRH**     | **Error Handling**                                                         |        |       |
| WSTG-ERRH-01      | Improper Error Handling                                                    |        |       |
| **WSTG-CRYP**     | **Weak Cryptography**                                                      |        |       |
| WSTG-CRYP-01      | Weak Transport Layer Security                                              |        |       |
| WSTG-CRYP-02      | Padding Oracle                                                             |        |       |
| WSTG-CRYP-03      | Sensitive Information Sent via Unencrypted Channels                        |        |       |
| WSTG-CRYP-04      | Weak Cryptographic Primitives                                              |        |       |
| **WSTG-BUSL**     | **Business Logic**                                                         |        |       |
| WSTG-BUSL-01      | Business Logic Data Validation                                             |        |       |
| WSTG-BUSL-02      | Ability to Forge Requests                                                  |        |       |
| WSTG-BUSL-03      | Integrity Checks                                                           |        |       |
| WSTG-BUSL-04      | Process Timing                                                             |        |       |
| WSTG-BUSL-05      | Number of Times a Function Can Be Used Limits                              |        |       |
| WSTG-BUSL-06      | Circumvention of Work Flows                                                |        |       |
| WSTG-BUSL-07      | Defenses Against Application Misuse                                        |        |       |
| WSTG-BUSL-08      | Upload of Unexpected File Types                                            |        |       |
| WSTG-BUSL-09      | Upload of Malicious Files                                                  |        |       |
| WSTG-BUSL-10      | Payment Functionality                                                      |        |       |
| WSTG-BUSL-11      | Denial of Inventory                                                        |        |       |
| **WSTG-CLNT**     | **Client-side**                                                            |        |       |
| WSTG-CLNT-01      | DOM-Based Cross Site Scripting                                             |        |       |
| WSTG-CLNT-02      | JavaScript Execution                                                       |        |       |
| WSTG-CLNT-03      | HTML Injection                                                             |        |       |
| WSTG-CLNT-04      | Client-side URL Redirect                                                   |        |       |
| WSTG-CLNT-05      | CSS Injection                                                              |        |       |
| WSTG-CLNT-06      | Client-side Resource Manipulation                                          |        |       |
| WSTG-CLNT-07      | Cross Origin Resource Sharing                                              |        |       |
| WSTG-CLNT-08      | Clickjacking                                                               |        |       |
| WSTG-CLNT-09      | WebSockets                                                                 |        |       |
| WSTG-CLNT-10      | Web Messaging                                                              |        |       |
| WSTG-CLNT-11      | Browser Storage                                                            |        |       |
| WSTG-CLNT-12      | Cross Site Script Inclusion                                                |        |       |
| WSTG-CLNT-13      | Reverse Tabnabbing                                                         |        |       |
| WSTG-CLNT-14      | Client-side Template Injection                                             |        |       |
| WSTG-CLNT-15      | DOM Clobbering                                                             |        |       |
| WSTG-CLNT-16      | Cross-Site Leaks                                                           |        |       |
| WSTG-CLNT-17      | Client-side Path Traversal                                                 |        |       |
| WSTG-CLNT-18      | Service Workers                                                            |        |       |
| WSTG-CLNT-19      | DNS Rebinding                                                              |        |       |
| WSTG-CLNT-20      | Server-Sent Events                                                         |        |       |
| **WSTG-APIT**     | **API Testing**                                                            |        |       |
| WSTG-APIT-01      | API Reconnaissance                                                         |        |       |
| WSTG-APIT-02      | API Broken Object Level Authorization                                      |        |       |
| WSTG-APIT-03      | Excessive Data Exposure                                                    |        |       |
| WSTG-APIT-04      | API Broken Function Level Authorization                                    |        |       |
| WSTG-APIT-05      | Testing API Authentication Mechanisms                                      |        |       |
| WSTG-APIT-06      | API Rate Limiting and Resource Consumption                                 |        |       |
| WSTG-APIT-07      | API Mass Assignment                                                        |        |       |
| WSTG-APIT-09      | Inbound Webhooks                                                           |        |       |
| WSTG-APIT-10      | gRPC                                                                       |        |       |
| WSTG-APIT-99      | GraphQL                                                                    |        |       |
| **WSTG-WASM**     | **WebAssembly Testing**                                                    |        |       |
| WSTG-WASM-01      | WebAssembly Reconnaissance                                                 |        |       |
| WSTG-WASM-02      | WebAssembly Static Analysis                                                |        |       |
| WSTG-WASM-03      | WebAssembly Dynamic Analysis                                               |        |       |
| WSTG-WASM-04      | WebAssembly Memory Corruption                                              |        |       |
| WSTG-WASM-05      | WebAssembly Host Boundary and WASI Misconfigurations                       |        |       |
