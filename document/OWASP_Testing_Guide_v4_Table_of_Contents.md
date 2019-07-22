# Table of Contents

## [Foreword by Eoin Keary](0_Foreword/0_Foreword.md)

## [1. Frontispiece](1_Frontispiece/)

**[1.1 About the OWASP Testing Guide Project](1_Frontispiece/1_Frontispiece.md)**

**[1.2 About The Open Web Application Security Project](1_Frontispiece/1.2_About_The_Open_Web_Application_Security_Project.md)**

## [2. Introduction](2_Introduction/)

**[2.1 The OWASP Testing Project](2_Introduction/2_Introduction.md#The-OWASP-Testing-Project)**

**[2.2 Principles of Testing](2_Introduction/2_Introduction.md#Principles-of-Testing)**

**[2.3 Testing Techniques Explained](2_Introduction/2_Introduction.md#Testing-Techniques-Explained)**

**[2.4 Manual Inspections & Reviews](2_Introduction/2_Introduction.md#Manual-Inspections-and-Reviews)**

**[2.5 Threat Modeling](2_Introduction/2_Introduction.md#Threat-Modeling)**

**[2.6 Source Code Review](2_Introduction/2_Introduction.md#Source-Code-Review)**

**[2.7 Penetration Testing](2_Introduction/2_Introduction.md#Penetration-Testing)**

**[2.8 The Need for a Balanced Approach](2_Introduction/2_Introduction.md#The-Need-for-a-Balanced-Approach)**

**[2.9 Deriving Security Test Requirements](2_Introduction/2_Introduction.md#Deriving-Security-Test-Requirements)**

**[2.10 Security Tests Integrated in Development and Testing Workflows](2_Introduction/2_Introduction.md#Security-Tests-Integrated-in-Development-and-Testing-Workflows)**

**[2.11 Security Test Data Analysis and Reporting](2_Introduction/2_Introduction.md#Security-Test-Data-Analysis-and-Reporting)**

## [3. The OWASP Testing Framework](3_The_OWASP_Testing_Framework/)

**[3.1 Overview](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#Overview)**

**[3.2 Phase 1: Before Development Begins](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#Phase-1:-Before-Development-Begins)**

**[3.3 Phase 2: During Definition and Design](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#Phase-2:-During-Definition-and-Design)**

**[3.4 Phase 3: During Development](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#Phase-3:-During-Development)**

**[3.5 Phase 4: During Deployment](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#Phase-4:-During-Deployment)**

**[3.6 Phase 5: Maintenance and Operations](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#Phase-5:-Maintenance-and-Operations)**

**[3.7 A Typical SDLC Testing Workflow](3_The_OWASP_Testing_Framework/3_The_OWASP_Testing_Framework.md#A-Typical-SDLC-Testing-Workflow)**

**[3.8 Penetration Testing Methodologies](3_The_OWASP_Testing_Framework/3.8_Penetration_Testing_Methodologies.md)**

## [4. Web Application Security Testing](4_Web_Application_Security_Testing/4_Web_Application_Penetration_Testing.md)

**[4.1 Introduction and Objectives](4_Web_Application_Security_Testing/4.1_Introduction_and_Objectives/4.1_Testing_Introduction_and_Objectives.md)**

[4.1.1 Testing Checklist](4_Web_Application_Security_Testing/4.1_Introduction_and_Objectives/4.1.1_Testing_Checklist.md)

**[4.2 Information Gathering](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2_Testing_Information_Gathering.md)**

[4.2.1 Conduct Search Engine Discovery and Reconnaissance for Information Leakage (OTG-INFO-001)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.1_Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage_OTG-INFO-001.md)

[4.2.2 Fingerprint Web Server (OTG-INFO-002)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.2_Fingerprint_Web_Server_OTG-INFO-002.md)

[4.2.3 Review Webserver Metafiles for Information Leakage (OTG-INFO-003)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.3_Review_Webserver_Metafiles_for_Information_Leakage_OTG-INFO-003.md)

[4.2.4 Enumerate Applications on Webserver (OTG-INFO-004)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.4_Enumerate_Applications_on_Webserver_OTG-INFO-004.md)

[4.2.5 Review Webpage Comments and Metadata for Information Leakage (OTG-INFO-005)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.5_Review_Webpage_Comments_and_Metadata_for_Information_Leakage_OTG-INFO-005.md)

[4.2.6 Identify application entry points (OTG-INFO-006)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.6_Identify_Application_Entry_Points_OTG-INFO-006.md)

[4.2.7 Map execution paths through application (OTG-INFO-007)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.7_Map_Execution_Paths_Through_Application_OTG-INFO-007.md)

[4.2.8 Fingerprint Web Application Framework (OTG-INFO-008)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.8_Fingerprint_Web_Application_Framework_OTG-INFO-008.md)

[4.2.9 Fingerprint Web Application (OTG-INFO-009)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.9_Fingerprint_Web_Application_OTG-INFO-009.md)

[4.2.10 Map Application Architecture (OTG-INFO-010)](4_Web_Application_Security_Testing/4.2_Information_Gathering/4.2.10_Map_Application_Architecture_OTG-INFO-010.md)

**[4.3 Configuration and Deployment Management Testing](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3_Testing_for_Configuration_Management.md)**

[4.3.1 Test Network/Infrastructure Configuration (OTG-CONFIG-001)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.1_Test_Network_Infrastructure_Configuration_OTG-CONFIG-001.md)

[4.3.2 Test Application Platform Configuration (OTG-CONFIG-002)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.2_Test_Application_Platform_Configuration_OTG-CONFIG-002.md)

[4.3.3 Test File Extensions Handling for Sensitive Information (OTG-CONFIG-003)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.3_Test_File_Extensions_Handling_for_Sensitive_Information_OTG-CONFIG-003.md)

[4.3.4 Review Old, Backup and Unreferenced Files for Sensitive Information (OTG-CONFIG-004)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.4_Review_Old_Backup_and_Unreferenced_Files_for_Sensitive_Information_OTG-CONFIG-004.md)

[4.3.5 Enumerate Infrastructure and Application Admin Interfaces (OTG-CONFIG-005)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.5_Enumerate_Infrastructure_and_Application_Admin_Interfaces_OTG-CONFIG-005.md)

[4.3.6 Test HTTP Methods (OTG-CONFIG-006)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.6_Test_HTTP_Methods_OTG-CONFIG-006.md)

[4.3.7 Test HTTP Strict Transport Security (OTG-CONFIG-007)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.7_Test_HTTP_Strict_Transport_Security_OTG-CONFIG-007.md)

[4.3.8 Test RIA cross domain policy (OTG-CONFIG-008)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.8_Test_RIA_Cross_Domain_Policy_OTG-CONFIG-008.md)

[4.3.9 Test File Permission (OTG-CONFIG-009)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.9_Test_File_Permission_OTG-CONFIG-009.md)

[4.3.10 Test for Subdomain Takeover (OTG-CONFIG-010)](4_Web_Application_Security_Testing/4.3_Configuration_and_Deployment_Management_Testing/4.3.10_Test_for_Subdomain_Takeover_OTG-CONFIG-010.md)

**[4.4 Identity Management Testing](4_Web_Application_Security_Testing/4.4_Identity_Management_Testing/4.4_Identity_Management_Testing.md)**

[4.4.1 Test Role Definitions (OTG-IDENT-001)](4_Web_Application_Security_Testing/4.4_Identity_Management_Testing/4.4.1_Test_Role_Definitions_OTG-IDENT-001.md)

[4.4.2 Test User Registration Process (OTG-IDENT-002)](4_Web_Application_Security_Testing/4.4_Identity_Management_Testing/4.4.2_Test_User_Registration_Process_OTG-IDENT-002.md)

[4.4.3 Test Account Provisioning Process (OTG-IDENT-003)](4_Web_Application_Security_Testing/4.4_Identity_Management_Testing/4.4.3_Test_Account_Provisioning_Process_OTG-IDENT-003.md)

[4.4.4 Testing for Account Enumeration and Guessable User Account (OTG-IDENT-004)](4_Web_Application_Security_Testing/4.4_Identity_Management_Testing/4.4.4_Testing_for_Account_Enumeration_and_Guessable_User_Account_OTG-IDENT-004.md)

[4.4.5 Testing for Weak or unenforced username policy (OTG-IDENT-005)](4_Web_Application_Security_Testing/4.4_Identity_Management_Testing/4.4.5_Testing_for_Weak_or_Unenforced_Username_Policy_OTG-IDENT-005.md)

**[4.5 Authentication Testing](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5_Testing_for_Authentication.md)**

[4.5.1 Testing for Credentials Transported over an Encrypted Channel (OTG-AUTHN-001)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.1_Testing_for_Credentials_Transported_over_an_Encrypted_Channel_OTG-AUTHN-001.md)

[4.5.2 Testing for default credentials (OTG-AUTHN-002)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.2_Testing_for_Default_Credentials_OTG-AUTHN-002.md)

[4.5.3 Testing for Weak lock out mechanism (OTG-AUTHN-003)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.3_Testing_for_Weak_Lock_Out_Mechanism_OTG-AUTHN-003.md)

[4.5.4 Testing for bypassing authentication schema (OTG-AUTHN-004)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.4_Testing_for_Bypassing_Authentication_Schema_OTG-AUTHN-004.md)

[4.5.5 Test remember password functionality (OTG-AUTHN-005)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.5_Testing_for_Vulnerable_Remember_Password_OTG-AUTHN-005.md)

[4.5.6 Testing for Browser cache weakness (OTG-AUTHN-006)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.6_Testing_for_Browser_Cache_Weaknesses_OTG-AUTHN-006.md)

[4.5.7 Testing for Weak password policy (OTG-AUTHN-007)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.7_Testing_for_Weak_Password_Policy_OTG-AUTHN-007.md)

[4.5.8 Testing for Weak security question/answer (OTG-AUTHN-008)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.8_Testing_for_Weak_Security_Question_Answer_OTG-AUTHN-008.md)

[4.5.9 Testing for weak password change or reset functionalities (OTG-AUTHN-009)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.9_Testing_for_Weak_Password_Change_or_Reset_Functionalities_OTG-AUTHN-009.md)

[4.5.10 Testing for Weaker authentication in alternative channel (OTG-AUTHN-010)](4_Web_Application_Security_Testing/4.5_Authentication_Testing/4.5.10_Testing_for_Weaker_Authentication_in_Alternative_Channel_OTG-AUTHN-010.md)

**[4.6 Authorization Testing](4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6_Testing_for_Authorization.md)**

[4.6.1 Testing Directory traversal/file include (OTG-AUTHZ-001)](4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6.1_Testing_Directory_Traversal_File_Include_OTG-AUTHZ-001.md)

[4.6.2 Testing for bypassing authorization schema (OTG-AUTHZ-002)](4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6.2_Testing_for_Bypassing_Authorization_Schema_OTG-AUTHZ-002.md)

[4.6.3 Testing for Privilege Escalation (OTG-AUTHZ-003)](4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6.3_Testing_for_Privilege_Escalation_OTG-AUTHZ-003.md)

[4.6.4 Testing for Insecure Direct Object References (OTG-AUTHZ-004)](4_Web_Application_Security_Testing/4.6_Authorization_Testing/4.6.4_Testing_for_Insecure_Direct_Object_References_OTG-AUTHZ-004.md)

**[4.7 Session Management Testing](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7_Testing_for_Session_Management.md)**

[4.7.1 Testing for Bypassing Session Management Schema (OTG-SESS-001)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.1_Testing_for_Session_Management_Schema_OTG-SESS-001.md)

[4.7.2 Testing for Cookies attributes (OTG-SESS-002)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.2_Testing_for_Cookies_Attributes_OTG-SESS-002.md)

[4.7.3 Testing for Session Fixation (OTG-SESS-003)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.3_Testing_for_Session_Fixation_OTG-SESS-003.md)

[4.7.4 Testing for Exposed Session Variables (OTG-SESS-004)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.4_Testing_for_Exposed_Session_Variables_OTG-SESS-004.md)

[4.7.5 Testing for Cross Site Request Forgery (CSRF) (OTG-SESS-005)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.5_Testing_for_CSRF_OTG-SESS-005.md)

[4.7.6 Testing for logout functionality (OTG-SESS-006)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.6_Testing_for_Logout_Functionality_OTG-SESS-006.md)

[4.7.7 Test Session Timeout (OTG-SESS-007)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.7_Test_Session_Timeout_OTG-SESS-007.md)

[4.7.8 Testing for Session puzzling (OTG-SESS-008)](4_Web_Application_Security_Testing/4.7_Session_Management_Testing/4.7.8_Testing_for_Session_Puzzling_OTG-SESS-008.md)

**[4.8 Input Validation Testing](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8_Testing_for_Input_Validation.md)**

[4.8.1 Testing for Reflected Cross Site Scripting (OTG-INPVAL-001)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.1_Testing_for_Reflected_Cross_Site_Scripting_OTG-INPVAL-001.md)

[4.8.2 Testing for Stored Cross Site Scripting (OTG-INPVAL-002)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.2_Testing_for_Stored_Cross_Site_Scripting_OTG-INPVAL-002.md)

[4.8.3 Testing for HTTP Verb Tampering (OTG-INPVAL-003)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.3_Testing_for_HTTP_Verb_Tampering_OTG-INPVAL-003.md)

[4.8.4 Testing for HTTP Parameter pollution (OTG-INPVAL-004)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.4_Testing_for_HTTP_Parameter_Pollution_OTG-INPVAL-004.md)

[4.8.5 Testing for SQL Injection (OTG-INPVAL-005)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5_Testing_for_SQL_Injection_OTG-INPVAL-005.md)

[4.8.5.1 Oracle Testing](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5.1_Testing_for_Oracle.md)

[4.8.5.2 MySQL Testing](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5.2_Testing_for_MySQL.md)

[4.8.5.3 SQL Server Testing](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5.3_Testing_for_SQL_Server.md)

[4.8.5.4 Testing PostgreSQL (from OWASP BSP)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5.4_OWASP_Backend_Security_Project_Testing_PostgreSQL.md)

[4.8.5.5 MS Access Testing](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5.5_Testing_for_MS_Access.md)

[4.8.5.6 Testing for NoSQL injection](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.5.6_Testing_for_NoSQL_Injection.md)

[4.8.6 Testing for LDAP Injection (OTG-INPVAL-006)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.6_Testing_for_LDAP_Injection_OTG-INPVAL-006.md)

[4.8.7 Testing for ORM Injection (OTG-INPVAL-007)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.7_Testing_for_ORM_Injection_OTG-INPVAL-007.md)

[4.8.8 Testing for XML Injection (OTG-INPVAL-008)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.8_Testing_for_XML_Injection_OTG-INPVAL-008.md)

[4.8.9 Testing for SSI Injection (OTG-INPVAL-009)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.9_Testing_for_SSI_Injection_OTG-INPVAL-009.md)

[4.8.10 Testing for XPath Injection (OTG-INPVAL-010)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.10_Testing_for_XPath_Injection_OTG-INPVAL-010.md)

[4.8.11 IMAP/SMTP Injection (OTG-INPVAL-011)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.11_Testing_for_IMAP_SMTP_Injection_OTG-INPVAL-011.md)

[4.8.12 Testing for Code Injection (OTG-INPVAL-012)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.12_Testing_for_Code_Injection_OTG-INPVAL-012.md)

[4.8.12.1 Testing for Local File Inclusion](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.12.1_Testing_for_Local_File_Inclusion.md)

[4.8.12.2 Testing for Remote File Inclusion](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.12.2_Testing_for_Remote_File_Inclusion.md)

[4.8.13 Testing for Command Injection (OTG-INPVAL-013)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.13_Testing_for_Command_Injection_OTG-INPVAL-013.md)

[4.8.14 Testing for Buffer overflow (OTG-INPVAL-014)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.14_Testing_for_Buffer_Overflow_OTG-INPVAL-014.md)

[4.8.14.1 Testing for Heap overflow](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.14.1_Testing_for_Heap_Overflow.md)

[4.8.14.2 Testing for Stack overflow](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.14.2_Testing_for_Stack_Overflow.md)

[4.8.14.3 Testing for Format string](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.14.3_Testing_for_Format_String.md)

[4.8.15 Testing for incubated vulnerabilities (OTG-INPVAL-015)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.15_Testing_for_Incubated_Vulnerability_OTG-INPVAL-015.md)

[4.8.16 Testing for HTTP Splitting/Smuggling (OTG-INPVAL-016)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.16_Testing_for_HTTP_Splitting_Smuggling_OTG-INPVAL-016.md)

[4.8.17 Testing for HTTP Incoming Requests (OTG-INPVAL-017)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.17_Testing_for_HTTP_Incoming_requests_OTG-INPVAL-017.md)

[4.8.18 Testing for Host Header Injection (OTG-INPVAL-018)](4_Web_Application_Security_Testing/4.8_Input_Validation_Testing/4.8.18_Testing_for_Host_Header_Injection_OTG-INPVAL-018.md)

**[4.9 Testing for Error Handling](4_Web_Application_Security_Testing/4.9_Testing_for_Error_Handling/4.9_Testing_for_Error_Handling.md)**

[4.9.1 Analysis of Error Codes (OTG-ERR-001)](4_Web_Application_Security_Testing/4.9_Testing_for_Error_Handling/4.9.1_Testing_for_Error_Code_OTG-ERR-001.md)

[4.9.2 Analysis of Stack Traces (OTG-ERR-002)](4_Web_Application_Security_Testing/4.9_Testing_for_Error_Handling/4.9.2_Testing_for_Stack_Traces_OTG-ERR-002.md)

**[4.10 Testing for weak Cryptography](4_Web_Application_Security_Testing/4.10_Testing_for_Weak_Cryptography/4.10_Testing_for_Weak_Cryptography.md)**

[4.10.1 Testing for Weak SSL/TLS Ciphers, Insufficient Transport Layer Protection (OTG-CRYPST-001)](4_Web_Application_Security_Testing/4.10_Testing_for_Weak_Cryptography/4.10.1_Testing_for_Weak_SSL_TLS_Ciphers_Insufficient_Transport_Layer_Protection_OTG-CRYPST-001.md)

[4.10.2 Testing for Padding Oracle (OTG-CRYPST-002)](4_Web_Application_Security_Testing/4.10_Testing_for_Weak_Cryptography/4.10.2_Testing_for_Padding_Oracle_OTG-CRYPST-002.md)

[4.10.3 Testing for Sensitive information sent via unencrypted channels (OTG-CRYPST-003)](4_Web_Application_Security_Testing/4.10_Testing_for_Weak_Cryptography/4.10.3_Testing_for_Sensitive_Information_Sent_via_Unencrypted_Channels_OTG-CRYPST-003.md)

[4.10.4 Testing for Weak Encryption (OTG-CRYPST-004)](4_Web_Application_Security_Testing/4.10_Testing_for_Weak_Cryptography/4.10.4_Testing_for_Weak_Encryption_OTG-CRYPST-004.md)

**[4.11 Business Logic Testing](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11_Testing_for_Business_Logic.md)**

[4.11.1 Test Business Logic Data Validation (OTG-BUSLOGIC-001)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.1_Test_Business_Logic_Data_Validation_OTG-BUSLOGIC-001.md)

[4.11.2 Test Ability to Forge Requests (OTG-BUSLOGIC-002)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.2_Test_Ability_to_Forge_Requests_OTG-BUSLOGIC-002.md)

[4.11.3 Test Integrity Checks (OTG-BUSLOGIC-003)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.3_Test_Integrity_Checks_OTG-BUSLOGIC-003.md)

[4.11.4 Test for Process Timing (OTG-BUSLOGIC-004)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.4_Test_for_Process_Timing_OTG-BUSLOGIC-004.md)

[4.11.5 Test Number of Times a Function Can be Used Limits (OTG-BUSLOGIC-005)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.5_Test_Number_of_Times_a_Function_Can_Be_Used_Limits_OTG-BUSLOGIC-005.md)

[4.11.6 Testing for the Circumvention of Work Flows (OTG-BUSLOGIC-006)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.6_Testing_for_the_Circumvention_of_Work_Flows_OTG-BUSLOGIC-006.md)

[4.11.7 Test Defenses Against Application Mis-use (OTG-BUSLOGIC-007)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.7_Test_Defenses_Against_Application_Mis-use_OTG-BUSLOGIC-007.md)

[4.11.8 Test Upload of Unexpected File Types (OTG-BUSLOGIC-008)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.8_Test_Upload_of_Unexpected_File_Types_OTG-BUSLOGIC-008.md)

[4.11.9 Test Upload of Malicious Files (OTG-BUSLOGIC-009)](4_Web_Application_Security_Testing/4.11_Business_Logic_Testing/4.11.9_Test_Upload_of_Malicious_Files_OTG-BUSLOGIC-009.md)

**[4.12 Client Side Testing](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12_Client_Side_Testing.md)**

[4.12.1 Testing for DOM based Cross Site Scripting (OTG-CLIENT-001)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.1_Testing_for_DOM-based_Cross_Site_Scripting_OTG-CLIENT-001.md)

[4.12.2 Testing for JavaScript Execution (OTG-CLIENT-002)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.2_Testing_for_JavaScript_Execution_OTG-CLIENT-002.md)

[4.12.3 Testing for HTML Injection (OTG-CLIENT-003)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.3_Testing_for_HTML_Injection_OTG-CLIENT-003.md)

[4.12.4 Testing for Client Side URL Redirect (OTG-CLIENT-004)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.4_Testing_for_Client_Side_URL_Redirect_OTG-CLIENT-004.md)

[4.12.5 Testing for CSS Injection (OTG-CLIENT-005)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.5_Testing_for_CSS_Injection_OTG-CLIENT-005.md)

[4.12.6 Testing for Client Side Resource Manipulation (OTG-CLIENT-006)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.6_Testing_for_Client_Side_Resource_Manipulation_OTG-CLIENT-006.md)

[4.12.7 Test Cross Origin Resource Sharing (OTG-CLIENT-007)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.7_Test_Cross_Origin_Resource_Sharing_OTG-CLIENT-007.md)

[4.12.8 Testing for Cross Site Flashing (OTG-CLIENT-008)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.8_Testing_for_Cross_Site_Flashing_OTG-CLIENT-008.md)

[4.12.9 Testing for Clickjacking (OTG-CLIENT-009)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.9_Testing_for_Clickjacking_OTG-CLIENT-009.md)

[4.12.10 Testing WebSockets (OTG-CLIENT-010)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.10_Testing_WebSockets_OTG-CLIENT-010.md)

[4.12.11 Test Web Messaging (OTG-CLIENT-011)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.11_Test_Web_Messaging_OTG-CLIENT-011.md)

[4.12.12 Test Local Storage (OTG-CLIENT-012)](4_Web_Application_Security_Testing/4.12_Client_Side_Testing/4.12.12_Test_Local_Storage_OTG-CLIENT-012.md)

## [5. Reporting](5_Reporting/Reporting.md)

## [Appendix A: Testing Tools Resource](Appx.A_Testing_Tools_Resource/Appx.A_Testing_Tools.md)

### Security Testing Tools

- [PTES_Technical_Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)
- [http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html](http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html)
- [http://sectools.org](http://sectools.org/)
- [https://www.kali.org](https://www.kali.org/)
- [http://www.blackarch.org/tools.html](http://www.blackarch.org/tools.html)

### Security Testing Tools in Virtual Image

- [https://tools.pentestbox.com/](https://tools.pentestbox.com/)
- [https://sourceforge.net/p/samurai/wiki/Home/](https://sourceforge.net/p/samurai/wiki/Home/)
- [https://sourceforge.net/projects/santoku/](https://sourceforge.net/projects/santoku/)
- [https://sourceforge.net/projects/parrotsecurity/?source=navbar](https://sourceforge.net/projects/parrotsecurity/?source=navbar)
- [https://sourceforge.net/projects/matriux/?source=navbar](https://sourceforge.net/projects/matriux/?source=navbar)
- [http://www.blackarch.org/downloads.html](http://www.blackarch.org/downloads.html)
- [https://www.kali.org/](https://www.kali.org/)
- [http://www.caine-live.net/index.html](http://www.caine-live.net/index.html)
- [http://www.pentoo.ch/download/](http://www.pentoo.ch/download/)
- [http://bugtraq-team.com/](http://bugtraq-team.com/)

## [Appendix B: Suggested Reading](Appx.B_Suggested_Reading/Appx.B_Suggested_Reading.md)

- Whitepapers
- Books
- Useful Websites

## [Appendix C: Fuzz Vectors](Appx.C_Fuzz_Vectors/Appx.C_Fuzz_Vectors.md)

- Fuzz Categories

## [Appendix D: Encoded Injection](Appx.D_Encoded_Injection/Appx.D_Encoded_Injection.md)

- Input Encoding
- Output Encoding

## [Appendix E: Misc](Appx.E_Misc/AppxE_History.md)

- History
