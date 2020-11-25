# Testing for the Circumvention of Work Flows

|ID          |
|------------|
|WSTG-BUSL-06|

## Summary

Workflow vulnerabilities involve any type of vulnerability that allows the attacker to misuse an application/system in a way that will allow them to circumvent (not follow) the designed/intended workflow.

[Definition of a workflow on Wikipedia](https://en.wikipedia.org/wiki/Workflow):

> A workflow consists of a sequence of connected steps where each step follows without delay or gap and ends just before the subsequent step may begin. It is a depiction of a sequence of operations, declared as work of a person or group, an organization of staff, or one or more simple or complex mechanisms. Workflow may be seen as any abstraction of real work.

The application’s business logic must require that the user complete specific steps in the correct/specific order and if the workflow is terminated without correctly completing, all actions and spawned actions are "rolled back" or canceled. Vulnerabilities related to the circumvention of workflows or bypassing the correct business logic workflow are unique in that they are very application/system specific and careful manual misuse cases must be developed using requirements and use cases.

The applications business process must have checks to ensure that the user's transactions/actions are proceeding in the correct/acceptable order and if a transaction triggers some sort of action, that action will be "rolled back" and removed if the transaction is not successfully completed.

### Example 1

Many of us receive so type of "club/loyalty points" for purchases from grocery stores and gas stations. Suppose a user was able to start a transaction linked to their account and then after points have been added to their club/loyalty account cancel out of the transaction or remove items from their "basket" and tender. In this case the system either should not apply points/credits to the account until it is tendered or points/credits should be "rolled back" if the point/credit increment does not match the final tender. With this in mind, an attacker may start transactions and cancel them to build their point levels without actually buy anything.

### Example 2

An electronic bulletin board system may be designed to ensure that initial posts do not contain profanity based on a list that the post is compared against. If a word on a deny list is found in the user entered text the submission is not posted. But, once a submission is posted the submitter can access, edit, and change the submission contents to include words included on the profanity/deny list since on edit the posting is never compared again. Keeping this in mind, attackers may open an initial blank or minimal discussion then add in whatever they like as an update.

## Test Objectives

- Review the project documentation for methods to skip or go through steps in the application process in a different order from the intended business logic flow.
- Develop a misuse case and try to circumvent every logic flow identified.

## How to Test

### Testing Method 1

- Start a transaction going through the application past the points that triggers credits/points to the users account.
- Cancel out of the transaction or reduce the final tender so that the point values should be decreased and check the points/ credit system to ensure that the proper points/credits were recorded.

### Testing Method 2

- On a content management or bulletin board system enter and save valid initial text or values.
- Then try to append, edit and remove data that would leave the existing data in an invalid state or with invalid values to ensure that the user is not allowed to save the incorrect information. Some "invalid" data or information may be specific words (profanity) or specific topics (such as political issues).

## Related Test Cases

- [Testing Directory Traversal/File Include](../05-Authorization_Testing/01-Testing_Directory_Traversal_File_Include.md)
- [Testing for Bypassing Authorization Schema](../05-Authorization_Testing/02-Testing_for_Bypassing_Authorization_Schema.md)
- [Testing for Bypassing Session Management Schema](../06-Session_Management_Testing/01-Testing_for_Session_Management_Schema.md)
- [Test Business Logic Data Validation](01-Test_Business_Logic_Data_Validation.md)
- [Test Ability to Forge Requests](02-Test_Ability_to_Forge_Requests.md)
- [Test Integrity Checks](03-Test_Integrity_Checks.md)
- [Test for Process Timing](04-Test_for_Process_Timing.md)
- [Test Number of Times a Function Can be Used Limits](05-Test_Number_of_Times_a_Function_Can_Be_Used_Limits.md)
- [Test Defenses Against Application Mis-use](07-Test_Defenses_Against_Application_Misuse.md)
- [Test Upload of Unexpected File Types](08-Test_Upload_of_Unexpected_File_Types.md)
- [Test Upload of Malicious Files](09-Test_Upload_of_Malicious_Files.md)

## Remediation

The application must be self-aware and have checks in place ensuring that the users complete each step in the work flow process in the correct order and prevent attackers from circumventing/skipping/or repeating any steps/processes in the workflow. Test for workflow vulnerabilities involves developing business logic abuse/misuse cases with the goal of successfully completing the business process while not completing the correct steps in the correct order.

## References

- [OWASP Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html)
- [CWE-840: Business Logic Errors](https://cwe.mitre.org/data/definitions/840.html)
