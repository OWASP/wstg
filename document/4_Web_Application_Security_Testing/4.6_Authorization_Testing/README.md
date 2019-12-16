# 4.6 Authorization Testing

Authorization is the concept of allowing access to resources only to those permitted to use them. Testing for Authorization means understanding how the authorization process works, and using that information to circumvent the authorization mechanism.

Authorization is a process that comes after a successful authentication, so the tester will verify this point after he holds valid credentials, associated with a well-defined set of roles and privileges. During this kind of assessment, it should be verified if it is possible to bypass the authorization schema, find a path traversal vulnerability, or find ways to escalate the privileges assigned to the tester.

[4.6.1 Testing Directory Traversal/File Include (OTG-AUTHZ-001)](4.6.1_Testing_Directory_Traversal_File_Include_OTG-AUTHZ-001.md)

[4.6.2 Testing for bypassing authorization schema (OTG-AUTHZ-002)](4.6.2_Testing_for_Bypassing_Authorization_Schema_OTG-AUTHZ-002.md)

[4.6.3 Testing for Privilege Escalation (OTG-AUTHZ-003)](4.6.3_Testing_for_Privilege_Escalation_OTG-AUTHZ-003.md)

[4.6.4 Testing for Insecure Direct Object References (OTG-AUTHZ-004)](4.6.4_Testing_for_Insecure_Direct_Object_References_OTG-AUTHZ-004.md)
