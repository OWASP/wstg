# Testing for Session Puzzling

|ID          |
|------------|
|WSTG-SESS-08|

## Summary

Session Variable Overloading (also known as Session Puzzling) is an application level vulnerability which can enable an attacker to perform a variety of malicious actions, including but not limited to:

- Bypass efficient authentication enforcement mechanisms, and impersonate legitimate users.
- Elevate the privileges of a malicious user account, in an environment that would otherwise be considered foolproof.
- Skip over qualifying phases in multi-phase processes, even if the process includes all the commonly recommended code level restrictions.
- Manipulate server-side values in indirect methods that cannot be predicted or detected.
- Execute traditional attacks in locations that were previously unreachable, or even considered secure.

This vulnerability occurs when an application uses the same session variable for more than one purpose. An attacker can potentially access pages in an order unanticipated by the developers so that the session variable is set in one context and then used in another.

For example, an attacker could use session variable overloading to bypass authentication enforcement mechanisms of applications that enforce authentication by validating the existence of session variables that contain identity–related values, which are usually stored in the session after a successful authentication process. This means an attacker first accesses a location in the application that sets session context and then accesses privileged locations that examine this context.

For example - an authentication bypass attack vector could be executed by accessing a publicly accessible entry point (e.g. a password recovery page) that populates the session with an identical session variable, based on fixed values or on user originating input.

## Test Objectives

- Identify all session variables.
- Break the logical flow of session generation.

## How to Test

### Black-Box Testing

This vulnerability can be detected and exploited by enumerating all of the session variables used by the application and in which context they are valid. In particular this is possible by accessing a sequence of entry points and then examining exit points. In case of black-box testing this procedure is difficult and requires some luck since every different sequence could lead to a different result.

#### Examples

A very simple example could be the password reset functionality that, in the entry point, could request the user to provide some identifying information such as the username or the email address. This page might then populate the session with these identifying values, which are received directly from the client-side, or obtained from queries or calculations based on the received input. At this point there may be some pages in the application that show private data based on this session object. In this manner the attacker could bypass the authentication process.

### Gray-Box Testing

The most effective way to detect these vulnerabilities is via a source code review.

## Remediation

Session variables should only be used for a single consistent purpose.

## References

- [Session Puzzles](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/puzzlemall/Session%20Puzzles%20-%20Indirect%20Application%20Attack%20Vectors%20-%20May%202011%20-%20Whitepaper.pdf)
- [Session Puzzling and Session Race Conditions](http://sectooladdict.blogspot.com/2011/09/session-puzzling-and-session-race.html)
