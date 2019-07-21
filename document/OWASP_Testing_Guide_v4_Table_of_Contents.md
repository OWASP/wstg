\_\_NOTOC\_\_

**This is the FINAL table of content of the New Testing Guide v4.**\
\
You can download the Guide [here](https://www.owasp.org/images/1/19/OTGv4.pdf)\
Back to the OWASP Testing Guide Project: <http://www.owasp.org/index.php/OWASP_Testing_Project>

**Testing Guide Wiki last Updated: April 2016**

[**Contributors List**](OWTGv4_Contributors_list "wikilink")

------------------------------------------------------------------------

Table of Contents
-----------------

[Foreword by Eoin Keary](Testing_Guide_Foreword "wikilink")
-----------------------------------------------------------

[1. Frontispiece](Testing_Guide_Frontispiece "wikilink")
--------------------------------------------------------

**[1.1 About the OWASP Testing Guide Project](Testing_Guide_Frontispiece "wikilink")**

**[1.2 About The Open Web Application Security Project](About_The_Open_Web_Application_Security_Project "wikilink")**

[2. Introduction](Testing_Guide_Introduction "wikilink")
--------------------------------------------------------

**[2.1 The OWASP Testing Project](Testing_Guide_Introduction#The_OWASP_Testing_Project "wikilink")**

**[2.2 Principles of Testing](Testing_Guide_Introduction#Principles_of_Testing "wikilink")**

**[2.3 Testing Techniques Explained](Testing_Guide_Introduction#Testing_Techniques_Explained "wikilink")**

**[2.4 Manual Inspections & Reviews](Testing_Guide_Introduction#Manual_Inspections_.26_Reviews "wikilink")**

**[2.5 Threat Modeling](Testing_Guide_Introduction#Threat_Modeling "wikilink")**

**[2.6 Source Code Review](Testing_Guide_Introduction#Source_Code_Review "wikilink")**

**[2.7 Penetration Testing](Testing_Guide_Introduction#Penetration_Testing "wikilink")**

**[2.8 The Need for a Balanced Approach](Testing_Guide_Introduction#The_Need_for_a_Balanced_Approach "wikilink")**

**[2.9 Deriving Security Test Requirements](Testing_Guide_Introduction#Deriving_Security_Test_Requirements "wikilink")**

**[2.10 Security Tests Integrated in Development and Testing Workflows](Testing_Guide_Introduction#Security_Tests_Integrated_in_Development_and_Testing_Workflows "wikilink")**

**[2.11 Security Test Data Analysis and Reporting](Testing_Guide_Introduction#Security_Test_Data_Analysis_and_Reporting "wikilink")**

[3. The OWASP Testing Framework](The_OWASP_Testing_Framework "wikilink")
------------------------------------------------------------------------

**[3.1 Overview](The_OWASP_Testing_Framework#Overview "wikilink")**

**[3.2 Phase 1: Before Development Begins](The_OWASP_Testing_Framework#Phase_1:_Before_Development_Begins "wikilink")**

**[3.3 Phase 2: During Definition and Design](The_OWASP_Testing_Framework#Phase_2:_During_Definition_and_Design "wikilink")**

**[3.4 Phase 3: During Development](The_OWASP_Testing_Framework#Phase_3:_During_Development "wikilink")**

**[3.5 Phase 4: During Deployment](The_OWASP_Testing_Framework#Phase_4:_During_Deployment "wikilink")**

**[3.6 Phase 5: Maintenance and Operations](The_OWASP_Testing_Framework#Phase_5:_Maintenance_and_Operations "wikilink")**

**[3.7 A Typical SDLC Testing Workflow](The_OWASP_Testing_Framework#A_Typical_SDLC_Testing_Workflow "wikilink")**

**[3.8 Penetration Testing Methodologies](Penetration_testing_methodologies "wikilink")**

[4. Web Application Security Testing](Web_Application_Penetration_Testing "wikilink")
-------------------------------------------------------------------------------------

[**4.1 Introduction and Objectives**](Testing:_Introduction_and_objectives "wikilink")

[ 4.1.1 Testing Checklist](Testing_Checklist "wikilink")

['''4.2 Information Gathering '''](Testing_Information_Gathering "wikilink")

[4.2.1 Conduct Search Engine Discovery and Reconnaissance for Information Leakage (OTG-INFO-001)](Conduct_search_engine_discovery/reconnaissance_for_information_leakage_(OTG-INFO-001) "wikilink")

[4.2.2 Fingerprint Web Server (OTG-INFO-002)](Fingerprint_Web_Server_(OTG-INFO-002) "wikilink")

[4.2.3 Review Webserver Metafiles for Information Leakage (OTG-INFO-003)](Review_Webserver_Metafiles_for_Information_Leakage_(OTG-INFO-003) "wikilink")

[4.2.4 Enumerate Applications on Webserver (OTG-INFO-004)](Enumerate_Applications_on_Webserver_(OTG-INFO-004) "wikilink")

[4.2.5 Review Webpage Comments and Metadata for Information Leakage (OTG-INFO-005)](Review_webpage_comments_and_metadata_for_information_leakage_(OTG-INFO-005) "wikilink")

[4.2.6 Identify application entry points (OTG-INFO-006)](Identify_application_entry_points_(OTG-INFO-006) "wikilink")

[4.2.7 Map execution paths through application (OTG-INFO-007)](Map_execution_paths_through_application_(OTG-INFO-007) "wikilink")

[4.2.8 Fingerprint Web Application Framework (OTG-INFO-008)](Fingerprint_Web_Application_Framework_(OTG-INFO-008) "wikilink")

[4.2.9 Fingerprint Web Application (OTG-INFO-009)](Fingerprint_Web_Application_(OTG-INFO-009) "wikilink")

[4.2.10 Map Application Architecture (OTG-INFO-010)](Map_Application_Architecture_(OTG-INFO-010) "wikilink")

['''4.3 Configuration and Deployment Management Testing '''](Testing_for_configuration_management "wikilink")

[4.3.1 Test Network/Infrastructure Configuration (OTG-CONFIG-001)](Test_Network/Infrastructure_Configuration_(OTG-CONFIG-001) "wikilink")

[4.3.2 Test Application Platform Configuration (OTG-CONFIG-002)](Test_Application_Platform_Configuration_(OTG-CONFIG-002) "wikilink")

[4.3.3 Test File Extensions Handling for Sensitive Information (OTG-CONFIG-003)](Test_File_Extensions_Handling_for_Sensitive_Information_(OTG-CONFIG-003) "wikilink")

[4.3.4 Review Old, Backup and Unreferenced Files for Sensitive Information (OTG-CONFIG-004)](Review_Old,_Backup_and_Unreferenced_Files_for_Sensitive_Information_(OTG-CONFIG-004) "wikilink")

[4.3.5 Enumerate Infrastructure and Application Admin Interfaces (OTG-CONFIG-005)](Enumerate_Infrastructure_and_Application_Admin_Interfaces_(OTG-CONFIG-005) "wikilink")

[4.3.6 Test HTTP Methods (OTG-CONFIG-006)](Test_HTTP_Methods_(OTG-CONFIG-006) "wikilink")

[4.3.7 Test HTTP Strict Transport Security (OTG-CONFIG-007)](Test_HTTP_Strict_Transport_Security_(OTG-CONFIG-007) "wikilink")

[4.3.8 Test RIA cross domain policy (OTG-CONFIG-008)](Test_RIA_cross_domain_policy_(OTG-CONFIG-008) "wikilink")

[4.3.9 Test File Permission (OTG-CONFIG-009)](Test_File_Permission_(OTG-CONFIG-009) "wikilink")

[**4.4 Identity Management Testing**](Testing_Identity_Management "wikilink")

[4.4.1 Test Role Definitions (OTG-IDENT-001)](Test_Role_Definitions_(OTG-IDENT-001) "wikilink")

[4.4.2 Test User Registration Process (OTG-IDENT-002)](Test_User_Registration_Process_(OTG-IDENT-002) "wikilink")

[4.4.3 Test Account Provisioning Process (OTG-IDENT-003)](Test_Account_Provisioning_Process_(OTG-IDENT-003) "wikilink")

[4.4.4 Testing for Account Enumeration and Guessable User Account (OTG-IDENT-004)](Testing_for_Account_Enumeration_and_Guessable_User_Account_(OTG-IDENT-004) "wikilink")

[ 4.4.5 Testing for Weak or unenforced username policy (OTG-IDENT-005)](Testing_for_Weak_or_unenforced_username_policy_(OTG-IDENT-005) "wikilink")

['''4.5 Authentication Testing '''](Testing_for_authentication "wikilink")

[4.5.1 Testing for Credentials Transported over an Encrypted Channel (OTG-AUTHN-001)](Testing_for_Credentials_Transported_over_an_Encrypted_Channel_(OTG-AUTHN-001) "wikilink")

[4.5.2 Testing for default credentials (OTG-AUTHN-002)](Testing_for_default_credentials_(OTG-AUTHN-002) "wikilink")

[4.5.3 Testing for Weak lock out mechanism (OTG-AUTHN-003)](Testing_for_Weak_lock_out_mechanism_(OTG-AUTHN-003) "wikilink")

[4.5.4 Testing for bypassing authentication schema (OTG-AUTHN-004)](Testing_for_Bypassing_Authentication_Schema_(OTG-AUTHN-004) "wikilink")

[4.5.5 Test remember password functionality (OTG-AUTHN-005)](Testing_for_Vulnerable_Remember_Password_(OTG-AUTHN-005) "wikilink")

[4.5.6 Testing for Browser cache weakness (OTG-AUTHN-006)](Testing_for_Browser_cache_weakness_(OTG-AUTHN-006) "wikilink")

[4.5.7 Testing for Weak password policy (OTG-AUTHN-007)](Testing_for_Weak_password_policy_(OTG-AUTHN-007) "wikilink")

[4.5.8 Testing for Weak security question/answer (OTG-AUTHN-008)](Testing_for_Weak_security_question/answer_(OTG-AUTHN-008) "wikilink")

[4.5.9 Testing for weak password change or reset functionalities (OTG-AUTHN-009)](Testing_for_weak_password_change_or_reset_functionalities_(OTG-AUTHN-009) "wikilink")

[4.5.10 Testing for Weaker authentication in alternative channel (OTG-AUTHN-010)](Testing_for_Weaker_authentication_in_alternative_channel_(OTG-AUTHN-010) "wikilink")

[**4.6 Authorization Testing**](Testing_for_Authorization "wikilink")

[4.6.1 Testing Directory traversal/file include (OTG-AUTHZ-001)](Testing_Directory_traversal/file_include_(OTG-AUTHZ-001) "wikilink")

[4.6.2 Testing for bypassing authorization schema (OTG-AUTHZ-002)](Testing_for_Bypassing_Authorization_Schema_(OTG-AUTHZ-002) "wikilink")

[4.6.3 Testing for Privilege Escalation (OTG-AUTHZ-003)](Testing_for_Privilege_escalation_(OTG-AUTHZ-003) "wikilink")

[4.6.4 Testing for Insecure Direct Object References (OTG-AUTHZ-004)](Testing_for_Insecure_Direct_Object_References_(OTG-AUTHZ-004) "wikilink")

[**4.7 Session Management Testing**](Testing_for_Session_Management "wikilink")

[4.7.1 Testing for Bypassing Session Management Schema (OTG-SESS-001)](Testing_for_Session_Management_Schema_(OTG-SESS-001) "wikilink")

[4.7.2 Testing for Cookies attributes (OTG-SESS-002)](Testing_for_cookies_attributes_(OTG-SESS-002) "wikilink")

[4.7.3 Testing for Session Fixation (OTG-SESS-003)](Testing_for_Session_Fixation_(OTG-SESS-003) "wikilink")

[4.7.4 Testing for Exposed Session Variables (OTG-SESS-004)](Testing_for_Exposed_Session_Variables_(OTG-SESS-004) "wikilink")

[4.7.5 Testing for Cross Site Request Forgery (CSRF) (OTG-SESS-005)](Testing_for_CSRF_(OTG-SESS-005) "wikilink")

[4.7.6 Testing for logout functionality (OTG-SESS-006)](Testing_for_logout_functionality_(OTG-SESS-006) "wikilink")

[4.7.7 Test Session Timeout (OTG-SESS-007)](Test_Session_Timeout_(OTG-SESS-007) "wikilink")

[4.7.8 Testing for Session puzzling (OTG-SESS-008)](Testing_for_Session_puzzling_(OTG-SESS-008) "wikilink")

[**4.8 Input Validation Testing**](Testing_for_Input_Validation "wikilink")

[4.8.1 Testing for Reflected Cross Site Scripting (OTG-INPVAL-001)](Testing_for_Reflected_Cross_site_scripting_(OTG-INPVAL-001) "wikilink")

[4.8.2 Testing for Stored Cross Site Scripting (OTG-INPVAL-002)](Testing_for_Stored_Cross_site_scripting_(OTG-INPVAL-002) "wikilink")

[4.8.3 Testing for HTTP Verb Tampering (OTG-INPVAL-003)](Testing_for_HTTP_Verb_Tampering_(OTG-INPVAL-003) "wikilink")

[4.8.4 Testing for HTTP Parameter pollution (OTG-INPVAL-004)](Testing_for_HTTP_Parameter_pollution_(OTG-INPVAL-004) "wikilink")

[ 4.8.5 Testing for SQL Injection (OTG-INPVAL-005)](Testing_for_SQL_Injection_(OTG-INPVAL-005) "wikilink")

[4.8.5.1 Oracle Testing](Testing_for_Oracle "wikilink")

[4.8.5.2 MySQL Testing](Testing_for_MySQL "wikilink")

[4.8.5.3 SQL Server Testing](Testing_for_SQL_Server "wikilink")

[4.8.5.4 Testing PostgreSQL (from OWASP BSP)](OWASP_Backend_Security_Project_Testing_PostgreSQL "wikilink")

[4.8.5.5 MS Access Testing](Testing_for_MS_Access "wikilink")

[4.8.5.6 Testing for NoSQL injection](Testing_for_NoSQL_injection "wikilink")

[4.8.6 Testing for LDAP Injection (OTG-INPVAL-006)](Testing_for_LDAP_Injection_(OTG-INPVAL-006) "wikilink")

[4.8.7 Testing for ORM Injection (OTG-INPVAL-007)](Testing_for_ORM_Injection_(OTG-INPVAL-007) "wikilink")

[4.8.8 Testing for XML Injection (OTG-INPVAL-008)](Testing_for_XML_Injection_(OTG-INPVAL-008) "wikilink")

[4.8.9 Testing for SSI Injection (OTG-INPVAL-009)](Testing_for_SSI_Injection_(OTG-INPVAL-009) "wikilink")

[4.8.10 Testing for XPath Injection (OTG-INPVAL-010)](Testing_for_XPath_Injection_(OTG-INPVAL-010) "wikilink")

[4.8.11 IMAP/SMTP Injection (OTG-INPVAL-011)](Testing_for_IMAP/SMTP_Injection_(OTG-INPVAL-011) "wikilink")

[4.8.12 Testing for Code Injection (OTG-INPVAL-012)](Testing_for_Code_Injection_(OTG-INPVAL-012) "wikilink")

[4.8.12.1 Testing for Local File Inclusion](Testing_for_Local_File_Inclusion "wikilink")

[4.8.12.2 Testing for Remote File Inclusion](Testing_for_Remote_File_Inclusion "wikilink")

[4.8.13 Testing for Command Injection (OTG-INPVAL-013)](Testing_for_Command_Injection_(OTG-INPVAL-013) "wikilink")

[4.8.14 Testing for Buffer overflow (OTG-INPVAL-014)](Testing_for_Buffer_Overflow_(OTG-INPVAL-014) "wikilink")

[4.8.14.1 Testing for Heap overflow](Testing_for_Heap_Overflow "wikilink")

[4.8.14.2 Testing for Stack overflow](Testing_for_Stack_Overflow "wikilink")

[4.8.14.3 Testing for Format string](Testing_for_Format_String "wikilink")

[4.8.15 Testing for incubated vulnerabilities (OTG-INPVAL-015)](Testing_for_Incubated_Vulnerability_(OTG-INPVAL-015) "wikilink")

[4.8.16 Testing for HTTP Splitting/Smuggling (OTG-INPVAL-016)](Testing_for_HTTP_Splitting/Smuggling_(OTG-INPVAL-016) "wikilink")

[4.8.17 Testing for HTTP Incoming Requests (OTG-INPVAL-017)](Testing_for_HTTP_Incoming_requests_(OTG-INPVAL-017) "wikilink")

[**4.9 Testing for Error Handling**](Testing_for_Error_Handling "wikilink")

[4.9.1 Analysis of Error Codes (OTG-ERR-001)](Testing_for_Error_Code_(OTG-ERR-001) "wikilink")

[4.9.2 Analysis of Stack Traces (OTG-ERR-002)](Testing_for_Stack_Traces_(OTG-ERR-002) "wikilink")

[**4.10 Testing for weak Cryptography**](Testing_for_weak_Cryptography "wikilink")

[ 4.10.1 Testing for Weak SSL/TLS Ciphers, Insufficient Transport Layer Protection (OTG-CRYPST-001)](Testing_for_Weak_SSL/TLS_Ciphers,_Insufficient_Transport_Layer_Protection_(OTG-CRYPST-001) "wikilink")

[ 4.10.2 Testing for Padding Oracle (OTG-CRYPST-002)](Testing_for_Padding_Oracle_(OTG-CRYPST-002) "wikilink")

[4.10.3 Testing for Sensitive information sent via unencrypted channels (OTG-CRYPST-003)](Testing_for_Sensitive_information_sent_via_unencrypted_channels_(OTG-CRYPST-003) "wikilink")

[4.10.4 Testing for Weak Encryption (OTG-CRYPST-004)](Testing_for_Weak_Encryption_(OTG-CRYPST-004) "wikilink")

[**4.11 Business Logic Testing**](Testing_for_business_logic "wikilink")

[4.11.1 Test Business Logic Data Validation (OTG-BUSLOGIC-001)](Test_business_logic_data_validation_(OTG-BUSLOGIC-001) "wikilink")

[4.11.2 Test Ability to Forge Requests (OTG-BUSLOGIC-002)](Test_Ability_to_forge_requests_(OTG-BUSLOGIC-002) "wikilink")

[4.11.3 Test Integrity Checks (OTG-BUSLOGIC-003)](Test_integrity_checks_(OTG-BUSLOGIC-003) "wikilink")

[4.11.4 Test for Process Timing (OTG-BUSLOGIC-004)](Test_for_Process_Timing_(OTG-BUSLOGIC-004) "wikilink")

[4.11.5 Test Number of Times a Function Can be Used Limits (OTG-BUSLOGIC-005)](Test_number_of_times_a_function_can_be_used_limits_(OTG-BUSLOGIC-005) "wikilink")

[4.11.6 Testing for the Circumvention of Work Flows (OTG-BUSLOGIC-006)](Testing_for_the_Circumvention_of_Work_Flows_(OTG-BUSLOGIC-006) "wikilink")

[4.11.7 Test Defenses Against Application Mis-use (OTG-BUSLOGIC-007)](Test_defenses_against_application_mis-use_(OTG-BUSLOGIC-007) "wikilink")

[4.11.8 Test Upload of Unexpected File Types (OTG-BUSLOGIC-008)](Test_Upload_of_Unexpected_File_Types_(OTG-BUSLOGIC-008) "wikilink")

[4.11.9 Test Upload of Malicious Files (OTG-BUSLOGIC-009)](Test_Upload_of_Malicious_Files_(OTG-BUSLOGIC-009) "wikilink")

[**4.12 Client Side Testing**](Client_Side_Testing "wikilink")\
[4.12.1 Testing for DOM based Cross Site Scripting (OTG-CLIENT-001)](Testing_for_DOM-based_Cross_site_scripting_(OTG-CLIENT-001) "wikilink")

[4.12.2 Testing for JavaScript Execution (OTG-CLIENT-002)](Testing_for_JavaScript_Execution_(OTG-CLIENT-002) "wikilink")

[4.12.3 Testing for HTML Injection (OTG-CLIENT-003)](Testing_for_HTML_Injection_(OTG-CLIENT-003) "wikilink")

[4.12.4 Testing for Client Side URL Redirect (OTG-CLIENT-004)](Testing_for_Client_Side_URL_Redirect_(OTG-CLIENT-004) "wikilink")

[4.12.5 Testing for CSS Injection (OTG-CLIENT-005)](Testing_for_CSS_Injection_(OTG-CLIENT-005) "wikilink")

[4.12.6 Testing for Client Side Resource Manipulation (OTG-CLIENT-006)](Testing_for_Client_Side_Resource_Manipulation_(OTG-CLIENT-006) "wikilink")

[4.12.7 Test Cross Origin Resource Sharing (OTG-CLIENT-007)](Test_Cross_Origin_Resource_Sharing_(OTG-CLIENT-007) "wikilink")

[4.12.8 Testing for Cross Site Flashing (OTG-CLIENT-008)](Testing_for_Cross_site_flashing_(OTG-CLIENT-008) "wikilink")

[4.12.9 Testing for Clickjacking (OTG-CLIENT-009)](Testing_for_Clickjacking_(OTG-CLIENT-009) "wikilink")

[4.12.10 Testing WebSockets (OTG-CLIENT-010)](Testing_WebSockets_(OTG-CLIENT-010) "wikilink")

[4.12.11 Test Web Messaging (OTG-CLIENT-011)](Test_Web_Messaging_(OTG-CLIENT-011) "wikilink")

[4.12.12 Test Local Storage (OTG-CLIENT-012)](Test_Local_Storage_(OTG-CLIENT-012) "wikilink")

[5. Reporting](Reporting "wikilink")
------------------------------------

[Appendix A: Testing Tools Resource](Appendix_A:_Testing_Tools "wikilink")
--------------------------------------------------------------------------

Security Testing Tools

-   <http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines>
-   <http://www.vulnerabilityassessment.co.uk/Penetration%20Test.html>
-   <http://sectools.org/>
-   <https://www.kali.org/>
-   <http://www.blackarch.org/tools.html>

Security Testing Tools in Virtual Image

-   <https://tools.pentestbox.com/>
-   <https://sourceforge.net/p/samurai/wiki/Home/>
-   <https://sourceforge.net/projects/santoku/>
-   <https://sourceforge.net/projects/parrotsecurity/?source=navbar>
-   <https://sourceforge.net/projects/matriux/?source=navbar>
-   <http://www.blackarch.org/downloads.html>
-   <https://www.kali.org/>
-   <http://cyborg.ztrela.com/tools/>
-   <http://www.caine-live.net/index.html>
-   <http://www.pentoo.ch/download/>
-   <http://bugtraq-team.com/>

[ Appendix B: Suggested Reading](OWASP_Testing_Guide_Appendix_B:_Suggested_Reading "wikilink")
----------------------------------------------------------------------------------------------

-   Whitepapers
-   Books
-   Useful Websites

[ Appendix C: Fuzz Vectors](OWASP_Testing_Guide_Appendix_C:_Fuzz_Vectors "wikilink")
------------------------------------------------------------------------------------

-   Fuzz Categories

[ Appendix D: Encoded Injection](OWASP_Testing_Guide_Appendix_D:_Encoded_Injection "wikilink")
----------------------------------------------------------------------------------------------

-   Input Encoding
-   Output Encoding

------------------------------------------------------------------------

[Category:OWASP Testing Project](Category:OWASP_Testing_Project "wikilink") <Category:Popular>
