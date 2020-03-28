# Table of Contents

## [Foreword by Eoin Keary](0-Foreword/README.md)

## [1. Frontispiece](1-Frontispiece/)

### [1.1 About the OWASP Testing Guide Project](1-Frontispiece/README.md)

## [2. Introduction](2-Introduction/)

### [2.1 The OWASP Testing Project](2-Introduction/README.md#The-OWASP-Testing-Project)

### [2.2 Principles of Testing](2-Introduction/README.md#Principles-of-Testing)

### [2.3 Testing Techniques Explained](2-Introduction/README.md#Testing-Techniques-Explained)

### [2.4 Manual Inspections & Reviews](2-Introduction/README.md#Manual-Inspections-and-Reviews)

### [2.5 Threat Modeling](2-Introduction/README.md#Threat-Modeling)

### [2.6 Source Code Review](2-Introduction/README.md#Source-Code-Review)

### [2.7 Penetration Testing](2-Introduction/README.md#Penetration-Testing)

### [2.8 The Need for a Balanced Approach](2-Introduction/README.md#The-Need-for-a-Balanced-Approach)

### [2.9 Deriving Security Test Requirements](2-Introduction/README.md#Deriving-Security-Test-Requirements)

### [2.10 Security Tests Integrated in Development and Testing Workflows](2-Introduction/README.md#Security-Tests-Integrated-in-Development-and-Testing-Workflows)

### [2.11 Security Test Data Analysis and Reporting](2-Introduction/README.md#Security-Test-Data-Analysis-and-Reporting)

## [3. The OWASP Testing Framework](3-The_OWASP_Testing_Framework/)

### [3.1 Overview](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#Overview)

### [3.2 Phase 1: Before Development Begins](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#Phase-1:-Before-Development-Begins)

### [3.3 Phase 2: During Definition and Design](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#Phase-2:-During-Definition-and-Design)

### [3.4 Phase 3: During Development](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#Phase-3:-During-Development)

### [3.5 Phase 4: During Deployment](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#Phase-4:-During-Deployment)

### [3.6 Phase 5: Maintenance and Operations](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#Phase-5:-During-Maintenance-and-Operations)

### [3.7 A Typical SDLC Testing Workflow](3-The_OWASP_Testing_Framework/0-The_OWASP_Testing_Framework.md#A-Typical-SDLC-Testing-Workflow)

### [3.8 Penetration Testing Methodologies](3-The_OWASP_Testing_Framework/1-Penetration_Testing_Methodologies.md)

## [4. Web Application Security Testing](4-Web_Application_Security_Testing/)

### [4.0 Introduction and Objectives](4-Web_Application_Security_Testing/0-Introduction_and_Objectives/README.md)

### [4.1 Information Gathering](4-Web_Application_Security_Testing/1-Information_Gathering/)

#### [4.1.1 Conduct Search Engine Discovery and Reconnaissance for Information Leakage](4-Web_Application_Security_Testing/1-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage.md)

#### [4.1.2 Fingerprint Web Server](4-Web_Application_Security_Testing/1-Information_Gathering/02-Fingerprint_Web_Server.md)

#### [4.1.3 Review Webserver Metafiles for Information Leakage](4-Web_Application_Security_Testing/1-Information_Gathering/03-Review_Webserver_Metafiles_for_Information_Leakage.md)

#### [4.1.4 Enumerate Applications on Webserver](4-Web_Application_Security_Testing/1-Information_Gathering/04-Enumerate_Applications_on_Webserver.md)

#### [4.1.5 Review Webpage Comments and Metadata for Information Leakage](4-Web_Application_Security_Testing/1-Information_Gathering/05-Review_Webpage_Comments_and_Metadata_for_Information_Leakage.md)

#### [4.1.6 Identify Application Entry Points](4-Web_Application_Security_Testing/1-Information_Gathering/06-Identify_Application_Entry_Points.md)

#### [4.1.7 Map Execution Paths Through Application](4-Web_Application_Security_Testing/1-Information_Gathering/07-Map_Execution_Paths_Through_Application.md)

#### [4.1.8 Fingerprint Web Application Framework](4-Web_Application_Security_Testing/1-Information_Gathering/08-Fingerprint_Web_Application_Framework.md)

#### [4.1.9 Fingerprint Web Application](4-Web_Application_Security_Testing/1-Information_Gathering/09-Fingerprint_Web_Application.md)

#### [4.1.10 Map Application Architecture](4-Web_Application_Security_Testing/1-Information_Gathering/10-Map_Application_Architecture.md)

### [4.3 Configuration and Deployment Management Testing](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/)

#### [4.3.1 Test Network/Infrastructure Configuration](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/01-Test_Network_Infrastructure_Configuration.md)

#### [4.3.2 Test Application Platform Configuration](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/02-Test_Application_Platform_Configuration.md)

#### [4.3.3 Test File Extensions Handling for Sensitive Information](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/03-Test_File_Extensions_Handling_for_Sensitive_Information.md)

#### [4.3.4 Review Old, Backup and Unreferenced Files for Sensitive Information](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/04-Review_Old_Backup_and_Unreferenced_Files_for_Sensitive_Information.md)

#### [4.3.5 Enumerate Infrastructure and Application Admin Interfaces](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/05-Enumerate_Infrastructure_and_Application_Admin_Interfaces.md)

#### [4.3.6 Test HTTP Methods](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/06-Test_HTTP_Methods.md)

#### [4.3.7 Test HTTP Strict Transport Security](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/07-Test_HTTP_Strict_Transport_Security.md)

#### [4.3.8 Test RIA Cross Domain Policy](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/08-Test_RIA_Cross_Domain_Policy.md)

#### [4.3.9 Test File Permission](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/09-Test_File_Permission.md)

#### [4.3.10 Test for Subdomain Takeover](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/10-Test_for_Subdomain_Takeover.md)

#### [4.3.11 Test Cloud Storage](4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/11-Test_Cloud_Storage.md)

### [4.4 Identity Management Testing](4-Web_Application_Security_Testing/03-Identity_Management_Testing/)

#### [4.4.1 Test Role Definitions](4-Web_Application_Security_Testing/03-Identity_Management_Testing/01-Test_Role_Definitions.md)

#### [4.4.2 Test User Registration Process](4-Web_Application_Security_Testing/03-Identity_Management_Testing/02-Test_User_Registration_Process.md)

#### [4.4.3 Test Account Provisioning Process](4-Web_Application_Security_Testing/03-Identity_Management_Testing/03-Test_Account_Provisioning_Process.md)

#### [4.4.4 Testing for Account Enumeration and Guessable User Account](4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md)

#### [4.4.5 Testing for Weak or Unenforced Username Policy](4-Web_Application_Security_Testing/03-Identity_Management_Testing/05-Testing_for_Weak_or_Unenforced_Username_Policy.md)

### [4.5 Authentication Testing](4-Web_Application_Security_Testing/04-Authentication_Testing/)

#### [4.5.1 Testing for Credentials Transported Over an Encrypted Channel](4-Web_Application_Security_Testing/04-Authentication_Testing/01-Testing_for_Credentials_Transported_over_an_Encrypted_Channel.md)

#### [4.5.2 Testing for Default Credentials](4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials.md)

#### [4.5.3 Testing for Weak Lock out Mechanism](4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism.md)

#### [4.5.4 Testing for Bypassing Authentication Schema](4-Web_Application_Security_Testing/04-Authentication_Testing/04-Testing_for_Bypassing_Authentication_Schema.md)

#### [4.5.5 Test Remember Password Functionality](4-Web_Application_Security_Testing/04-Authentication_Testing/05-Testing_for_Vulnerable_Remember_Password.md)

#### [4.5.6 Testing for Browser Cache Weakness](4-Web_Application_Security_Testing/04-Authentication_Testing/06-Testing_for_Browser_Cache_Weaknesses.md)

#### [4.5.7 Testing for Weak Password Policy](4-Web_Application_Security_Testing/04-Authentication_Testing/07-Testing_for_Weak_Password_Policy.md)

#### [4.5.8 Testing for Weak Security Question/Answer](4-Web_Application_Security_Testing/04-Authentication_Testing/08-Testing_for_Weak_Security_Question_Answer.md)

#### [4.5.9 Testing for Weak Password Change or Reset Functionalities](4-Web_Application_Security_Testing/04-Authentication_Testing/09-Testing_for_Weak_Password_Change_or_Reset_Functionalities.md)

#### [4.5.10 Testing for Weaker Authentication in Alternative Channel](4-Web_Application_Security_Testing/04-Authentication_Testing/10-Testing_for_Weaker_Authentication_in_Alternative_Channel.md)

### [4.6 Authorization Testing](4-Web_Application_Security_Testing/05-Authorization_Testing/)

#### [4.6.1 Testing Directory Traversal/File Include](4-Web_Application_Security_Testing/05-Authorization_Testing/01-Testing_Directory_Traversal_File_Include.md)

#### [4.6.2 Testing for Bypassing Authorization Schema)](4-Web_Application_Security_Testing/05-Authorization_Testing/02-Testing_for_Bypassing_Authorization_Schema.md)

#### [4.6.3 Testing for Privilege Escalation](4-Web_Application_Security_Testing/05-Authorization_Testing/03-Testing_for_Privilege_Escalation.md)

#### [4.6.4 Testing for Insecure Direct Object References](4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md)

### [4.7 Session Management Testing](4-Web_Application_Security_Testing/06-Session_Management_Testing/)

#### [4.7.1 Testing for Bypassing Session Management Schema](4-Web_Application_Security_Testing/06-Session_Management_Testing/01-Testing_for_Session_Management_Schema.md)

#### [4.7.2 Testing for Cookies Attributes](4-Web_Application_Security_Testing/06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md)

#### [4.7.3 Testing for Session Fixation](4-Web_Application_Security_Testing/06-Session_Management_Testing/03-Testing_for_Session_Fixation.md)

#### [4.7.4 Testing for Exposed Session Variables](4-Web_Application_Security_Testing/06-Session_Management_Testing/04-Testing_for_Exposed_Session_Variables.md)

#### [4.7.5 Testing for Cross Site Request Forgery (CSRF)](4-Web_Application_Security_Testing/06-Session_Management_Testing/05-Testing_for_CSRF.md)

#### [4.7.6 Testing for Logout Functionality](4-Web_Application_Security_Testing/06-Session_Management_Testing/06-Testing_for_Logout_Functionality.md)

#### [4.7.7 Test Session Timeout](4-Web_Application_Security_Testing/06-Session_Management_Testing/07-Testing_Session_Timeout.md)

#### [4.7.8 Testing for Session Puzzling](4-Web_Application_Security_Testing/06-Session_Management_Testing/08-Testing_for_Session_Puzzling.md)

### [4.8 Input Validation Testing](4-Web_Application_Security_Testing/07-Input_Validation_Testing/)

#### [4.8.1 Testing for Reflected Cross Site Scripting](4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting.md)

#### [4.8.2 Testing for Stored Cross Site Scripting](4-Web_Application_Security_Testing/07-Input_Validation_Testing/02-Testing_for_Stored_Cross_Site_Scripting.md)

#### [4.8.3 Testing for HTTP Verb Tampering](4-Web_Application_Security_Testing/07-Input_Validation_Testing/03-Testing_for_HTTP_Verb_Tampering.md)

#### [4.8.4 Testing for HTTP Parameter Pollution](4-Web_Application_Security_Testing/07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution.md)

#### [4.8.5 Testing for SQL Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.md)

##### [4.8.5.1 Oracle Testing](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.1-Testing_for_Oracle.md)

##### [4.8.5.2 MySQL Testing](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.2-Testing_for_MySQL.md)

##### [4.8.5.3 SQL Server Testing](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.3-Testing_for_SQL_Server.md)

##### [4.8.5.4 Testing PostgreSQL](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.4-Testing_PostgreSQL.md)

##### [4.8.5.5 MS Access Testing](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.5-Testing_for_MS_Access.md)

##### [4.8.5.6 Testing for NoSQL Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection.md)

#### [4.8.6 Testing for LDAP Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/06-Testing_for_LDAP_Injection.md)

#### [4.8.7 Testing for ORM Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/07-Testing_for_ORM_Injection.md)

#### [4.8.8 Testing for XML Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/08-Testing_for_XML_Injection.md)

#### [4.8.9 Testing for SSI Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_SSI_Injection.md)

#### [4.8.10 Testing for XPath Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/10-Testing_for_XPath_Injection.md)

#### [4.8.11 IMAP/SMTP Injection)](4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_IMAP_SMTP_Injection.md)

#### [4.8.12 Testing for Code Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Code_Injection.md)

##### [4.8.12.1 Testing for Local File Inclusion](4-Web_Application_Security_Testing/07-Input_Validation_Testing/12.1-Testing_for_Local_File_Inclusion.md)

##### [4.8.12.2 Testing for Remote File Inclusion](4-Web_Application_Security_Testing/07-Input_Validation_Testing/12.2-Testing_for_Remote_File_Inclusion.md)

#### [4.8.13 Testing for Command Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/13-Testing_for_Command_Injection.md)

#### [4.8.14 Testing for Buffer Overflow](4-Web_Application_Security_Testing/07-Input_Validation_Testing/14-Testing_for_Buffer_Overflow.md)

##### [4.8.14.1 Testing for Heap Overflow](4-Web_Application_Security_Testing/07-Input_Validation_Testing/14.1-Testing_for_Heap_Overflow.md)

##### [4.8.14.2 Testing for Stack Overflow](4-Web_Application_Security_Testing/07-Input_Validation_Testing/14.2-Testing_for_Stack_Overflow.md)

##### [4.8.14.3 Testing for Format String](4-Web_Application_Security_Testing/07-Input_Validation_Testing/14.3-Testing_for_Format_String.md)

#### [4.8.15 Testing for Incubated Vulnerabilities](4-Web_Application_Security_Testing/07-Input_Validation_Testing/15-Testing_for_Incubated_Vulnerability.md)

#### [4.8.16 Testing for HTTP Splitting/Smuggling](4-Web_Application_Security_Testing/07-Input_Validation_Testing/16-Testing_for_HTTP_Splitting_Smuggling.md)

#### [4.8.17 Testing for HTTP Incoming Requests](4-Web_Application_Security_Testing/07-Input_Validation_Testing/17-Testing_for_HTTP_Incoming_Requests.md)

#### [4.8.18 Testing for Host Header Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Host_Header_Injection.md)

#### [4.8.19 Testing for Server Side Template Injection](4-Web_Application_Security_Testing/07-Input_Validation_Testing/19-Testing_for_Server_Side_Template_Injection.md)

### [4.9 Testing for Error Handling](4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/)

#### [4.9.1 Analysis of Error Codes](4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/01-Testing_for_Error_Code.md)

#### [4.9.2 Analysis of Stack Traces](4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/02-Testing_for_Stack_Traces.md)

### [4.10 Testing for Weak Cryptography](4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/)

#### [4.10.1 Testing for Weak SSL/TLS Ciphers, Insufficient Transport Layer Protection](4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/01-Testing_for_Weak_SSL_TLS_Ciphers_Insufficient_Transport_Layer_Protection.md)

#### [4.10.2 Testing for Padding Oracle](4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/02-Testing_for_Padding_Oracle.md)

#### [4.10.3 Testing for Sensitive Information Sent via Unencrypted Channels](4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/03-Testing_for_Sensitive_Information_Sent_via_Unencrypted_Channels.md)

#### [4.10.4 Testing for Weak Encryption](4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/04-Testing_for_Weak_Encryption.md)

### [4.11 Business Logic Testing](4-Web_Application_Security_Testing/10-Business_Logic_Testing/)

#### [4.11.1 Test Business Logic Data Validation](4-Web_Application_Security_Testing/10-Business_Logic_Testing/01-Test_Business_Logic_Data_Validation.md)

#### [4.11.2 Test Ability to Forge Requests](4-Web_Application_Security_Testing/10-Business_Logic_Testing/02-Test_Ability_to_Forge_Requests.md)

#### [4.11.3 Test Integrity Checks](4-Web_Application_Security_Testing/10-Business_Logic_Testing/03-Test_Integrity_Checks.md)

#### [4.11.4 Test for Process Timing](4-Web_Application_Security_Testing/10-Business_Logic_Testing/04-Test_for_Process_Timing.md)

#### [4.11.5 Test Number of Times a Function Can Be Used Limits](4-Web_Application_Security_Testing/10-Business_Logic_Testing/05-Test_Number_of_Times_a_Function_Can_Be_Used_Limits.md)

#### [4.11.6 Testing for the Circumvention of Work Flows](4-Web_Application_Security_Testing/10-Business_Logic_Testing/06-Testing_for_the_Circumvention_of_Work_Flows.md)

#### [4.11.7 Test Defenses Against Application Misuse](4-Web_Application_Security_Testing/10-Business_Logic_Testing/07-Test_Defenses_Against_Application_Misuse.md)

#### [4.11.8 Test Upload of Unexpected File Types](4-Web_Application_Security_Testing/10-Business_Logic_Testing/08-Test_Upload_of_Unexpected_File_Types.md)

#### [4.11.9 Test Upload of Malicious Files](4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files.md)

### [4.12 Client Side Testing](4-Web_Application_Security_Testing/11-Client_Side_Testing/)

#### [4.12.1 Testing for DOM-Based Cross Site Scripting](4-Web_Application_Security_Testing/11-Client_Side_Testing/01-Testing_for_DOM-based_Cross_Site_Scripting.md)

#### [4.12.2 Testing for JavaScript Execution](4-Web_Application_Security_Testing/11-Client_Side_Testing/02-Testing_for_JavaScript_Execution.md)

#### [4.12.3 Testing for HTML Injection](4-Web_Application_Security_Testing/11-Client_Side_Testing/03-Testing_for_HTML_Injection.md)

#### [4.12.4 Testing for Client Side URL Redirect](4-Web_Application_Security_Testing/11-Client_Side_Testing/04-Testing_for_Client_Side_URL_Redirect.md)

#### [4.12.5 Testing for CSS Injection](4-Web_Application_Security_Testing/11-Client_Side_Testing/05-Testing_for_CSS_Injection.md)

#### [4.12.6 Testing for Client Side Resource Manipulation](4-Web_Application_Security_Testing/11-Client_Side_Testing/06-Testing_for_Client_Side_Resource_Manipulation.md)

#### [4.12.7 Testing Cross Origin Resource Sharing](4-Web_Application_Security_Testing/11-Client_Side_Testing/07-Testing_Cross_Origin_Resource_Sharing.md)

#### [4.12.8 Testing for Cross Site Flashing](4-Web_Application_Security_Testing/11-Client_Side_Testing/08-Testing_for_Cross_Site_Flashing.md)

#### [4.12.9 Testing for Clickjacking](4-Web_Application_Security_Testing/11-Client_Side_Testing/09-Testing_for_Clickjacking.md)

#### [4.12.10 Testing WebSockets](4-Web_Application_Security_Testing/11-Client_Side_Testing/10-Testing_WebSockets.md)

#### [4.12.11 Testing Web Messaging](4-Web_Application_Security_Testing/11-Client_Side_Testing/11-Testing_Web_Messaging.md)

#### [4.12.12 Testing Local Storage](4-Web_Application_Security_Testing/11-Client_Side_Testing/12-Testing_Web_Storage.md)

#### [4.12.13 Testing for Cross Site Script Inclusion](4-Web_Application_Security_Testing/11-Client_Side_Testing/13-Testing_for_Cross_Site_Script_Inclusion.md)

## [5. Reporting](5-Reporting/README.md)

## [Appendix A: Testing Tools Resource](Appx.A_Testing_Tools_Resource/README.md)

### Security Testing Tools

- [PTES_Technical_Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)
- [http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html](http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html)
- [https://sectools.org](https://sectools.org/)
- [https://www.kali.org](https://www.kali.org/)
- [https://www.blackarch.org/tools.html](https://www.blackarch.org/tools.html)

### Security Testing Tools in Virtual Image

- [https://tools.pentestbox.com/](https://tools.pentestbox.com/)
- [https://sourceforge.net/p/samurai/wiki/Home/](https://sourceforge.net/p/samurai/wiki/Home/)
- [https://sourceforge.net/projects/santoku/](https://sourceforge.net/projects/santoku/)
- [https://sourceforge.net/projects/parrotsecurity/?source=navbar](https://sourceforge.net/projects/parrotsecurity/?source=navbar)
- [https://sourceforge.net/projects/matriux/?source=navbar](https://sourceforge.net/projects/matriux/?source=navbar)
- [https://www.blackarch.org/downloads.html](https://www.blackarch.org/downloads.html)
- [https://www.kali.org/](https://www.kali.org/)
- [https://www.caine-live.net/index.html](https://www.caine-live.net/index.html)
- [https://www.pentoo.ch/download/](https://www.pentoo.ch/download/)

## [Appendix B: Suggested Reading](Appx.B_Suggested_Reading/README.md)

- Whitepapers
- Books
- Useful Websites

## [Appendix C: Fuzz Vectors](Appx.C_Fuzz_Vectors/README.md)

- Fuzz Categories

## [Appendix D: Encoded Injection](Appx.D_Encoded_Injection/README.md)

- Input Encoding
- Output Encoding

## [Appendix E: Misc](Appx.E_Misc/README.md)

- History
