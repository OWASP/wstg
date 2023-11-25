| ID          |
|-------------|
| WSTG-SESS-11|

## Summary

Concurrent sessions are a common aspect of web applications that enable multiple simultaneous user interactions. This test case aims to verify the application’s ability to handle multiple active sessions for a single user, which is crucial to ensure effective management of concurrent user sessions, particularly within sensitive areas such as admin panels containing Personally Identifiable Information (PII) data, personal user accounts, or APIs reliant on third-party services to enrich user-provided data, and to align concurrent sessions with an application’s security needs.

It is important to understand the security requirements of concurrent sessions in an application to determine whether concurrent sessions are a desirable or intended feature. While allowing concurrent sessions is not inherently negative and is intentionally permitted in numerous applications, it is crucial to ensure that the application’s functionality is effectively aligned with its security measures concerning concurrent sessions. If concurrent sessions are intended, it is vital to ensure additional security controls, such as managing active sessions, terminating sessions, and potential new session notifications. Conversely, if concurrent sessions are not intended or planned within the application, it is crucial to validate existing checks for session management vulnerabilities.

## Test Objectives

- Evaluate the application's session management by assessing the handling of multiple active sessions for a single user account.

## How to Test

1. **Generate Valid Session:**
   - Submit valid credentials (username and password) to create a session.
   - Example HTTP Request:

     ```http
     POST /login HTTP/1.1
     Host: www.example.com
     Content-Length: 32

     username=admin&password=admin123
     ```

   - Example Response:

     ```http
     HTTP/1.1 200 OK
     Set-Cookie: SESSIONID=0add0d8eyYq3HIUy09hhus; Path=/; Secure
     ```

   - Store the generated authentication token or cookie.

2. **Test for Generating Active Sessions:**
   - Attempt to create multiple authentication cookies by submitting login requests (e.g., one hundred times).

3. **Test for Validating Active Sessions:**
   - Try accessing the application using the initial session token (e.g., `SESSIONID=0add0d8eyYq3HIUy09hhus`).
   - If successful authentication occurs with the first generated token, consider it a potential issue indicating inadequate session management.

Note: Utilizing private browsing mode or multi-account containers might be beneficial for conducting these tests, as they can provide separate environments for testing session management without interference from existing sessions or cookies stored in the browser.

## Remediation

The application should monitor and limit the number of active sessions per user account. If the maximum allowed sessions are surpassed, the system must invalidate previous sessions to maintain security. Implementing additional solutions can further mitigate this vulnerability:

   1. **User Notification:** Notify users after each successful login to raise awareness of active sessions.
   2. **Session Management Page:** Create a dedicated page to display and allow termination of active sessions for enhanced user control.

## Recommended Tools

### Intercepting Proxy Tools

- [OWASP Zed Attack Proxy Project](https://www.zaproxy.org)
- [Burp Suite Web Proxy](https://portswigger.net)
