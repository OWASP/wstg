# Test Role Definitions

|ID          |
|------------|
|WSTG-IDNT-01|

## Summary

Applications have several types of functionalities and services, and those require access permissions based on the needs of the user. That user could be:

- an administrator, where they manage the application functionalities.
- an auditor, where they review the application transactions and provide a detailed report.
- a support engineer, where they help customers debug and fix issues on their accounts.
- a customer, where they interact with the application and benefit from its services.

In order to handle these uses and any other use case for that application, role definitions are setup (more commonly known as [RBAC](https://en.wikipedia.org/wiki/Role-based_access_control)). Based on these roles, the user is capable of accomplishing the required task.

## Test Objectives

- Identify and document roles used by the application.
- Attempt to switch, change, or access another role.
- Review the granularity of the roles and the needs behind the permissions given.

## How to Test

### Roles Identification

The tester should start by identifying the application roles being tested through any of the following methods:

- Application documentation.
- Guidance by the developers or administrators of the application.
- Application comments.
- Fuzz possible roles:
    - cookie variable (*e.g.* `role=admin`, `isAdmin=True`)
    - account variable (*e.g.* `Role: manager`)
    - hidden directories or files (*e.g.* `/admin`, `/mod`, `/backups`)
    - switching to well known users (*e.g.* `admin`, `backups`, etc.)

### Switching to Available Roles

After identifying possible attack vectors, the tester needs to test and validate that they can access the available roles.

> Some applications define the roles of the user on creation, through rigorous checks and policies, or by ensuring that the user's role is properly protected through a signature created by the backend. Finding that roles exist doesn't mean that they're a vulnerability.

### Review Roles Permissions

After gaining access to the roles on the system, the tester must understand the permissions provided to each role.

A support engineer shouldn't be able to conduct administrative functionalities, manage the backups, or conduct any transactions in the place of a user.

An administrator shouldn't have full powers on the system. Sensitive admin functionality should leverage a maker-checker principle, or use MFA to ensure that the administrator is conducting the transaction. A clear example on this was the [Twitter incident in 2020](https://blog.twitter.com/en_us/topics/company/2020/an-update-on-our-security-incident.html).

## Tools

The above mentioned tests can be conducted without the use of any tool, except the one being used to access the system.

To make things easier and more documented, one can use:

- [Burp's Autorize extension](https://github.com/Quitten/Autorize)
- [ZAP's Access Control Testing add-on](https://www.zaproxy.org/docs/desktop/addons/access-control-testing/)

## References

- [Role Engineering for Enterprise Security Management, E Coyne & J Davis, 2007](https://www.bookdepository.co.uk/Role-Engineering-for-Enterprise-Security-Management-Edward-Coyne/9781596932180)
- [Role engineering and RBAC standards](https://csrc.nist.gov/projects/role-based-access-control#rbac-standard)
