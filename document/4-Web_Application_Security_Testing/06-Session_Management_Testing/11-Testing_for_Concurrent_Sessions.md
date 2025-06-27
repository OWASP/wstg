# Testing for Concurrent Sessions

|ID          |
|------------|
|WSTG-SESS-11|

## Summary

Concurrent sessions are a common aspect of web applications that enable multiple simultaneous user interactions. This test case aims to evaluate the application's ability to handle multiple active sessions for a single user. This functionality is essential for effectively managing concurrent user sessions, particularly in sensitive areas such as admin panels containing Personally Identifiable Information (PII), personal user accounts, or APIs reliant on third-party services to enrich user-provided data. The primary objective is to ensure that concurrent sessions align with the application's security requirements.

Understanding the security needs in an application is key to assessing whether enabling concurrent sessions corresponds with the intended features. Allowing concurrent sessions isn't inherently detrimental and is intentionally permitted in many applications. However, it is crucial to ensure that the application’s functionality is effectively aligned with its security measures concerning concurrent sessions. If concurrent sessions are intended, it is vital to ensure additional security controls, such as managing active sessions, terminating sessions, and potential new session notifications. Conversely, if concurrent sessions are not intended or planned within the application, it is crucial to validate existing checks for session management vulnerabilities.

To recognize that concurrent sessions are essential, you should consider the following factors:

- Understanding the application's nature, particularly situations where users might require simultaneous access from different locations or devices.
- Identifying critical operations, such as financial transactions that require secure access.
- Handling sensitive data like Personally Identifiable Information (PII), indicating the necessity for secure interactions.
- Distinguishing between a management panel and a standard user dashboard for normal user access.

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

   - Store the generated authentication cookie. In some cases, the generated authentication cookie is replaced by tokens such as JSON Web Tokens (JWT).

2. **Test for Generating Active Sessions:**
   - Attempt to create multiple authentication cookies by submitting login requests (e.g., one hundred times).

   Note: Utilizing private browsing mode or multi-account containers might be beneficial for conducting these tests, as they can provide separate environments for testing session management without interference from existing sessions or cookies stored in the browser.

3. **Test for Validating Active Sessions:**
   - Try accessing the application using the initial session token (e.g., `SESSIONID=0add0d8eyYq3HIUy09hhus`).
   - If successful authentication occurs with the first generated token, consider it a potential issue indicating inadequate session management.

Also, there are additional test cases that extend the scope of the testing methodology to include scenarios involving multiple sessions originating from various IPs and locations. These test cases aid in identifying potential vulnerabilities or irregularities in session handling related to geographical or network-based factors:

- Test Multiple sessions from the same IP.
- Test Multiple sessions from different IPs.
- Test Multiple sessions from locations that are unlikely or impossible to be visited by the same user in a short period of time (e.g., one session created in a specific country, followed by another session generated five minutes later from a different country).

## Remediation

The application should monitor and limit the number of active sessions per user account. If the maximum allowed sessions are surpassed, the system must invalidate previous sessions to maintain security. Implementing additional solutions can further mitigate this vulnerability:

   1. **User Notification:** Notify users after each successful login to raise awareness of active sessions.
   2. **Session Management Page:** Create a dedicated page to display and allow termination of active sessions for enhanced user control.
   3. **IP Address Tracking:** Track the IP addresses of users who log in to an account and flag any suspicious activity, such as multiple logins from different locations.
   4. **IP Address Restrictions:** Allow users to specify trusted IP addresses or ranges from which they can access their accounts, enhancing security by restricting sessions to known and approved locations.

## Recommended Tools

### Intercepting Proxy Tools

- [Zed Attack Proxy](https://www.zaproxy.org)
- [Burp Suite Web Proxy](https://portswigger.net)
