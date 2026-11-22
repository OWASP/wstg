# Contents

## 0. [Foreword](00-Foreword/README.md)

## 1. [About](01-About/)

## 2. [Introduction](02-Introduction/)

### 2.1 [Purpose and Scope](02-Introduction/README.md#purpose-and-scope)

### 2.2 [Why Web Application Security Testing Matters](02-Introduction/README.md#why-web-application-security-testing-matters)

### 2.3 [Who Should Use This Guide](02-Introduction/README.md#who-should-use-this-guide)

### 2.4 [Core Principles of Effective Security Testing](02-Introduction/README.md#core-principles-of-effective-security-testing)

### 2.5 [How the Guide Is Organized](02-Introduction/README.md#how-the-guide-is-organized)

### 2.6 [How to Reference WSTG Scenarios](02-Introduction/README.md#how-to-reference-wstg-scenarios)

### 2.7 [Feedback and Comments](02-Introduction/README.md#feedback-and-comments)

### 2.8 [Related OWASP Projects](02-Introduction/README.md#related-owasp-projects)

## 3. [The OWASP Testing Framework](03-The_OWASP_Testing_Framework/)

### 3.1 [The Web Security Testing Framework](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md)

### 3.2 [Testing Activities](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#testing-activities)

### 3.3 [Requirements and Policy Review](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#requirements-and-policy-review)

### 3.4 [Design, Architecture, and Threat Modeling](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#design-architecture-and-threat-modeling)

### 3.5 [Code-Level Review and Analysis](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#code-level-review-and-analysis)

### 3.6 [Dynamic and Penetration Testing](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#dynamic-and-penetration-testing)

### 3.7 [Continuous Integration Pipeline Testing](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#continuous-integration-pipeline-testing)

### 3.8 [Continuous and Crowd-Sourced Testing](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#continuous-and-crowd-sourced-testing)

### 3.9 [Matching Activity to Cadence](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#matching-activity-to-cadence)

### 3.10 [Where to Start](03-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework.md#where-to-start)

### 3.11 [Bug Bounty Programs as a Testing Technique](03-The_OWASP_Testing_Framework/1-Bug_Bounty_Programs.md)

### 3.12 [Human-AI Collaborative Testing](03-The_OWASP_Testing_Framework/2-Human-AI_Collaborative_Testing.md)

## 4. [Introduction and Objectives](04-Introduction_and_Objectives/README.md)

## 5. [Information Gathering](05-Information_Gathering/README.md)

### 5.1 [Conduct Search Engine Reconnaissance for Information Leakage](05-Information_Gathering/01-Conduct_Search_Engine_Reconnaissance_for_Information_Leakage.md)

### 5.2 [Fingerprint Web Server](05-Information_Gathering/02-Fingerprint_Web_Server.md)

### 5.3 [Review Webserver Metafiles for Information Leakage](05-Information_Gathering/03-Review_Webserver_Metafiles_for_Information_Leakage.md)

### 5.4 [Attack Surface Identification](05-Information_Gathering/04-Attack_Surface_Identification.md)

### 5.5 [Review Web Page Content for Information Leakage](05-Information_Gathering/05-Review_Web_Page_Content_for_Information_Leakage.md)

### 5.6 [Identify Application Entry Points](05-Information_Gathering/06-Identify_Application_Entry_Points.md)

### 5.7 [Map Execution Paths Through Application](05-Information_Gathering/07-Map_Execution_Paths_Through_Application.md)

### 5.8 [Fingerprint Web Application Framework](05-Information_Gathering/08-Fingerprint_Web_Application_Framework.md)

### 5.9 [Map Application Architecture](05-Information_Gathering/09-Map_Application_Architecture.md)

## 6. [Configuration and Deployment Management](06-Configuration_and_Deployment_Management/README.md)

### 6.1 [Network Infrastructure Configuration](06-Configuration_and_Deployment_Management/01-Network_Infrastructure_Configuration.md)

### 6.2 [Application Platform Configuration](06-Configuration_and_Deployment_Management/02-Application_Platform_Configuration.md)

### 6.3 [Review Old Backup and Unreferenced Files for Sensitive Information](06-Configuration_and_Deployment_Management/03-Review_Old_Backup_and_Unreferenced_Files_for_Sensitive_Information.md)

### 6.4 [Enumerate Infrastructure and Application Admin Interfaces](06-Configuration_and_Deployment_Management/04-Enumerate_Infrastructure_and_Application_Admin_Interfaces.md)

### 6.5 [HTTP Methods](06-Configuration_and_Deployment_Management/05-HTTP_Methods.md)

### 6.6 [HTTP Strict Transport Security](06-Configuration_and_Deployment_Management/06-HTTP_Strict_Transport_Security.md)

### 6.7 [File Permissions](06-Configuration_and_Deployment_Management/07-File_Permissions.md)

### 6.8 [Subdomain Takeover](06-Configuration_and_Deployment_Management/08-Subdomain_Takeover.md)

### 6.9 [Cloud Storage](06-Configuration_and_Deployment_Management/09-Cloud_Storage.md)

### 6.10 [Content Security Policy](06-Configuration_and_Deployment_Management/10-Content_Security_Policy.md)

### 6.11 [Path Confusion](06-Configuration_and_Deployment_Management/11-Path_Confusion.md)

### 6.12 [Additional Browser Security Controls](06-Configuration_and_Deployment_Management/12-Additional_Browser_Security_Controls.md)

### 6.13 [Feature Flag Security Bypass](06-Configuration_and_Deployment_Management/13-Feature_Flag_Security_Bypass.md)

### 6.14 [Web Cache Poisoning](06-Configuration_and_Deployment_Management/14-Web_Cache_Poisoning.md)

## 7. [Identity Management](07-Identity_Management/README.md)

### 7.1 [Role Definitions](07-Identity_Management/01-Role_Definitions.md)

### 7.2 [User Registration Process](07-Identity_Management/02-User_Registration_Process.md)

### 7.3 [Account Provisioning Process](07-Identity_Management/03-Account_Provisioning_Process.md)

### 7.4 [Account Enumeration and Guessable User Account](07-Identity_Management/04-Account_Enumeration_and_Guessable_User_Account.md)

### 7.5 [Email Address Verification](07-Identity_Management/05-Email_Address_Verification.md)

## 8. [Authentication](08-Authentication/README.md)

### 8.1 [Default Credentials](08-Authentication/01-Default_Credentials.md)

### 8.2 [Weak Lock Out Mechanism](08-Authentication/02-Weak_Lock_Out_Mechanism.md)

### 8.3 [Bypassing Authentication Schema](08-Authentication/03-Bypassing_Authentication_Schema.md)

### 8.4 [Vulnerable Remember Password](08-Authentication/04-Vulnerable_Remember_Password.md)

### 8.5 [Browser Cache Weaknesses](08-Authentication/05-Browser_Cache_Weaknesses.md)

### 8.6 [Weak Authentication Methods](08-Authentication/06-Weak_Authentication_Methods.md)

### 8.7 [Weak Security Question Answer](08-Authentication/07-Weak_Security_Question_Answer.md)

### 8.8 [Weak Password Change or Reset Functionalities](08-Authentication/08-Weak_Password_Change_or_Reset_Functionalities.md)

### 8.9 [Weaker Authentication in Alternative Channel](08-Authentication/09-Weaker_Authentication_in_Alternative_Channel.md)

### 8.10 [Multi-Factor Authentication (MFA)](08-Authentication/10-Multi-Factor_Authentication.md)

### 8.11 [SAML Authentication](08-Authentication/11-SAML_Authentication.md)

### 8.12 [Passkeys and WebAuthn](08-Authentication/12-Passkeys_and_WebAuthn.md)

### 8.13 [OpenID Connect Relying Party](08-Authentication/13-OpenID_Connect_Relying_Party.md)

## 9. [Authorization](09-Authorization/README.md)

### 9.1 [Directory Traversal and File Include](09-Authorization/01-Directory_Traversal_File_Include.md)

### 9.2 [Bypassing Authorization Schema](09-Authorization/02-Bypassing_Authorization_Schema.md)

### 9.3 [Privilege Escalation](09-Authorization/03-Privilege_Escalation.md)

### 9.4 [Insecure Direct Object References](09-Authorization/04-Insecure_Direct_Object_References.md)

### 9.5 [OAuth Weaknesses](09-Authorization/05-OAuth_Weaknesses.md)

#### 9.5.1 [OAuth Authorization Server Weaknesses](09-Authorization/05.1-OAuth_Authorization_Server_Weaknesses.md)

#### 9.5.2 [OAuth Client Weaknesses](09-Authorization/05.2-OAuth_Client_Weaknesses.md)

## 10. [Session Management](10-Session_Management/README.md)

### 10.1 [Session Management Schema](10-Session_Management/01-Session_Management_Schema.md)

### 10.2 [Cookies Attributes](10-Session_Management/02-Cookies_Attributes.md)

### 10.3 [Session Fixation](10-Session_Management/03-Session_Fixation.md)

### 10.4 [Exposed Session Variables](10-Session_Management/04-Exposed_Session_Variables.md)

### 10.5 [Cross Site Request Forgery](10-Session_Management/05-Cross_Site_Request_Forgery.md)

### 10.6 [Logout Functionality](10-Session_Management/06-Logout_Functionality.md)

### 10.7 [Session Timeout](10-Session_Management/07-Session_Timeout.md)

### 10.8 [Session Puzzling](10-Session_Management/08-Session_Puzzling.md)

### 10.9 [Session Hijacking](10-Session_Management/09-Session_Hijacking.md)

### 10.10 [JSON Web Tokens](10-Session_Management/10-JSON_Web_Tokens.md)

### 10.11 [Concurrent Sessions](10-Session_Management/11-Concurrent_Sessions.md)

## 11. [Injection](11-Injection/README.md)

### 11.1 [Reflected Cross Site Scripting](11-Injection/01-Reflected_Cross_Site_Scripting.md)

### 11.2 [Stored Cross Site Scripting](11-Injection/02-Stored_Cross_Site_Scripting.md)

### 11.3 [HTTP Parameter Pollution](11-Injection/03-HTTP_Parameter_Pollution.md)

### 11.4 [SQL Injection](11-Injection/04-SQL_Injection.md)

#### 11.4.1 [Oracle](11-Injection/04.1-Oracle.md)

#### 11.4.2 [MySQL](11-Injection/04.2-MySQL.md)

#### 11.4.3 [SQL Server](11-Injection/04.3-SQL_Server.md)

#### 11.4.4 [PostgreSQL](11-Injection/04.4-PostgreSQL.md)

#### 11.4.5 [MS Access](11-Injection/04.5-MS_Access.md)

#### 11.4.6 [NoSQL Injection](11-Injection/04.6-NoSQL_Injection.md)

#### 11.4.7 [ORM Injection](11-Injection/04.7-ORM_Injection.md)

### 11.5 [LDAP Injection](11-Injection/05-LDAP_Injection.md)

### 11.6 [XML Injection](11-Injection/06-XML_Injection.md)

### 11.7 [SSI Injection](11-Injection/07-SSI_Injection.md)

### 11.8 [XPath Injection](11-Injection/08-XPath_Injection.md)

### 11.9 [IMAP SMTP Injection](11-Injection/09-IMAP_SMTP_Injection.md)

### 11.10 [Code Injection](11-Injection/10-Code_Injection.md)

#### 11.10.1 [File Inclusion](11-Injection/10.1-File_Inclusion.md)

### 11.11 [Command Injection](11-Injection/11-Command_Injection.md)

### 11.12 [Format String Injection](11-Injection/12-Format_String_Injection.md)

### 11.13 [Incubated Vulnerability](11-Injection/13-Incubated_Vulnerability.md)

### 11.14 [HTTP Response Splitting](11-Injection/14-HTTP_Response_Splitting.md)

### 11.15 [HTTP Request Smuggling](11-Injection/15-HTTP_Request_Smuggling.md)

### 11.16 [Host Header Injection](11-Injection/16-Host_Header_Injection.md)

### 11.17 [Server-side Template Injection](11-Injection/17-Server-side_Template_Injection.md)

### 11.18 [Server-Side Request Forgery](11-Injection/18-Server-Side_Request_Forgery.md)

### 11.19 [Mass Assignment](11-Injection/19-Mass_Assignment.md)

### 11.20 [CSV Injection](11-Injection/20-CSV_Injection.md)

### 11.21 [Prototype Pollution](11-Injection/21-Prototype_Pollution.md)

### 11.22 [Insecure Deserialization](11-Injection/22-Insecure_Deserialization.md)

### 11.23 [Server-side URL Redirect](11-Injection/23-Server-side_URL_Redirect.md)

### 11.24 [Unicode Normalization and Case Mapping](11-Injection/24-Unicode_Normalization_and_Case_Mapping.md)

### 11.25 [JSON Parser Differentials](11-Injection/25-JSON_Parser_Differentials.md)

### 11.26 [Server-side Document Rendering Injection](11-Injection/26-Server-side_Document_Rendering_Injection.md)

### 11.27 [Regular Expression Denial of Service](11-Injection/27-Regular_Expression_Denial_of_Service.md)

## 12. [Error Handling](12-Error_Handling/README.md)

### 12.1 [Improper Error Handling](12-Error_Handling/01-Improper_Error_Handling.md)

## 13. [Weak Cryptography](13-Weak_Cryptography/README.md)

### 13.1 [Weak Transport Layer Security](13-Weak_Cryptography/01-Weak_Transport_Layer_Security.md)

### 13.2 [Padding Oracle](13-Weak_Cryptography/02-Padding_Oracle.md)

### 13.3 [Sensitive Information Sent via Unencrypted Channels](13-Weak_Cryptography/03-Sensitive_Information_Sent_via_Unencrypted_Channels.md)

### 13.4 [Weak Cryptographic Primitives](13-Weak_Cryptography/04-Weak_Cryptographic_Primitives.md)

## 14. [Business Logic](14-Business_Logic/README.md)

### 14.0 [Introduction to Business Logic](14-Business_Logic/00-Introduction_to_Business_Logic.md)

### 14.1 [Business Logic Data Validation](14-Business_Logic/01-Business_Logic_Data_Validation.md)

### 14.2 [Ability to Forge Requests](14-Business_Logic/02-Ability_to_Forge_Requests.md)

### 14.3 [Integrity Checks](14-Business_Logic/03-Integrity_Checks.md)

### 14.4 [Process Timing](14-Business_Logic/04-Process_Timing.md)

### 14.5 [Number of Times a Function Can Be Used Limits](14-Business_Logic/05-Number_of_Times_a_Function_Can_Be_Used_Limits.md)

### 14.6 [Circumvention of Work Flows](14-Business_Logic/06-Circumvention_of_Work_Flows.md)

### 14.7 [Defenses Against Application Misuse](14-Business_Logic/07-Defenses_Against_Application_Misuse.md)

### 14.8 [Upload of Unexpected File Types](14-Business_Logic/08-Upload_of_Unexpected_File_Types.md)

### 14.9 [Upload of Malicious Files](14-Business_Logic/09-Upload_of_Malicious_Files.md)

### 14.10 [Payment Functionality](14-Business_Logic/10-Payment_Functionality.md)

### 14.11 [Denial of Inventory](14-Business_Logic/11-Denial_of_Inventory.md)

## 15. [Client-side](15-Client-side/README.md)

### 15.1 [DOM-Based Cross Site Scripting](15-Client-side/01-DOM-based_Cross_Site_Scripting.md)

#### 15.1.1 [Self DOM Based Cross Site Scripting](15-Client-side/01.1-Self_DOM_Based_Cross_Site_Scripting.md)

### 15.2 [JavaScript Execution](15-Client-side/02-JavaScript_Execution.md)

### 15.3 [HTML Injection](15-Client-side/03-HTML_Injection.md)

### 15.4 [Client-side URL Redirect](15-Client-side/04-Client-side_URL_Redirect.md)

### 15.5 [CSS Injection](15-Client-side/05-CSS_Injection.md)

### 15.6 [Client-side Resource Manipulation](15-Client-side/06-Client-side_Resource_Manipulation.md)

### 15.7 [Cross Origin Resource Sharing](15-Client-side/07-Cross_Origin_Resource_Sharing.md)

### 15.8 [Clickjacking](15-Client-side/08-Clickjacking.md)

### 15.9 [WebSockets](15-Client-side/09-WebSockets.md)

### 15.10 [Web Messaging](15-Client-side/10-Web_Messaging.md)

### 15.11 [Browser Storage](15-Client-side/11-Browser_Storage.md)

### 15.12 [Cross Site Script Inclusion](15-Client-side/12-Cross_Site_Script_Inclusion.md)

### 15.13 [Reverse Tabnabbing](15-Client-side/13-Reverse_Tabnabbing.md)

### 15.14 [Client-side Template Injection](15-Client-side/14-Client-Side_Template_Injection.md)

### 15.15 [DOM Clobbering](15-Client-side/15-DOM_Clobbering.md)

### 15.16 [Cross-Site Leaks](15-Client-side/16-Cross_Site_Leaks.md)

### 15.17 [Client-side Path Traversal](15-Client-side/17-Client-side_Path_Traversal.md)

### 15.18 [Service Workers](15-Client-side/18-Service_Workers.md)

### 15.19 [DNS Rebinding](15-Client-side/19-DNS_Rebinding.md)

### 15.20 [Server-Sent Events](15-Client-side/20-Server-Sent_Events.md)

## 16. [API Testing](16-API_Testing/README.md)

### 16.0 [API Testing Overview](16-API_Testing/00-API_Testing_Overview.md)

### 16.1 [API Reconnaissance](16-API_Testing/01-API_Reconnaissance.md)

### 16.2 [API Broken Object Level Authorization](16-API_Testing/02-API_Broken_Object_Level_Authorization.md)

### 16.3 [Excessive Data Exposure](16-API_Testing/03-Excessive_Data_Exposure.md)

### 16.4 [API Broken Function Level Authorization](16-API_Testing/04-API_Broken_Function_Level_Authorization.md)

### 16.5 [Testing API Authentication Mechanisms](16-API_Testing/05-Testing_API_Authentication_Mechanisms.md)

### 16.6 [API Rate Limiting and Resource Consumption](16-API_Testing/06-API_Rate_Limiting_and_Resource_Consumption.md)

### 16.7 [API Mass Assignment](16-API_Testing/07-API_Mass_Assignment.md)

### 16.9 [Inbound Webhooks](16-API_Testing/09-Inbound_Webhooks.md)

### 16.10 [gRPC](16-API_Testing/10-gRPC.md)

### 16.99 [GraphQL](16-API_Testing/99-GraphQL.md)

## 17. [WebAssembly Testing](17-WebAssembly_Testing/README.md)

### 17.0 [WebAssembly Testing Overview](17-WebAssembly_Testing/00-WebAssembly_Testing_Overview.md)

### 17.1 [WebAssembly Reconnaissance](17-WebAssembly_Testing/01-WebAssembly_Reconnaissance.md)

### 17.2 [WebAssembly Static Analysis](17-WebAssembly_Testing/02-WebAssembly_Static_Analysis.md)

### 17.3 [WebAssembly Dynamic Analysis](17-WebAssembly_Testing/03-WebAssembly_Dynamic_Analysis.md)

### 17.4 [WebAssembly Memory Corruption](17-WebAssembly_Testing/04-WebAssembly_Memory_Corruption.md)

## 18. [Reporting](18-Reporting/README.md)

### 18.1 [Reporting Structure](18-Reporting/01-Reporting_Structure.md)

### 18.2 [Vulnerability Naming Schemes](18-Reporting/02-Naming_Schemes.md)

## Appendix A. [History](19-Appendix/A-History.md)

## Appendix B. [Testing Tools Resource](19-Appendix/B-Testing_Tools_Resource.md)

## Appendix C. [Suggested Reading](19-Appendix/C-Suggested_Reading.md)

## Appendix D. [Fuzzing](19-Appendix/D-Fuzzing.md)

## Appendix E. [Encoded Injection](19-Appendix/E-Encoded_Injection.md)

## Appendix F. [Leveraging Dev Tools](19-Appendix/F-Leveraging_Dev_Tools.md)

## Appendix G. [Penetration Testing Methodologies](19-Appendix/G-Penetration_Testing_Methodologies.md)
