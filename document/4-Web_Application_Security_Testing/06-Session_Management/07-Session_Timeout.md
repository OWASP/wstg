# Session Timeout

|ID          |
|------------|
|WSTG-SESS-07|

## Summary

In this phase testers check that the application automatically logs out a user when that user has been idle for a certain amount of time, or when the session reaches its maximum lifetime, ensuring that it is not possible to "reuse" the same session and that no sensitive data remains stored in the browser cache.

All applications should implement an idle or inactivity timeout for sessions. This timeout defines the amount of time a session will remain active in case there is no activity by the user, closing and invalidating the session upon the defined idle period since the last HTTP request received by the web application for a given session ID. The most appropriate timeout should be a balance between security (shorter timeout) and usability (longer timeout) and heavily depends on the sensitivity level of the data handled by the application. For example, a 60 minute log out time for a public forum can be acceptable, but such a long time would be too much in a home banking application (where a maximum timeout of 15 minutes is recommended). In any case, any application that does not enforce a timeout-based log out should be considered not secure, unless such behavior is required by a specific functional requirement.

A common scenario where a missing idle timeout can be abused is a public computer that is used to access some private information (e.g., web mail, online bank account). If the user moves away from the computer, or just closes the browser or a tab, without explicitly logging out and the session timeout is not implemented on the application, then an attacker could access the same account by simply pressing the "back" button of the browser.

The idle timeout limits the chances that an attacker has to guess and use a valid session ID from another user, and under certain circumstances could protect public computers from session reuse. However, if the attacker is able to hijack a given session, the idle timeout does not limit the attacker’s actions, as the attacker can generate activity on the session periodically to keep the session active for longer periods of time.

This is why applications should also enforce an absolute timeout, which limits the total lifetime of a session regardless of activity. Once it expires, the user has to authenticate again even if the session was never idle. Its value depends on how long a user usually uses the application. For example, the [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#automatic-session-expiration) suggests 4 to 8 hours for an application that an office worker uses for a full day.

Session timeout management and expiration must be enforced server-side. If some data under the control of the client is used to enforce the session timeout, for example using cookie values or other client parameters to track time references (e.g. number of minutes since log in time), an attacker could manipulate these to extend the session duration. So the application has to track the inactivity time and the session age server-side and, after a timeout is expired, automatically invalidate the current user's session and delete every data stored on the client.

When either timeout expires, the session must be terminated in the same way as on log out: all session tokens (e.g. cookies) must be destroyed or made unusable server-side, so that they cannot be replayed to "resurrect" the session of a legitimate user. See [Logout Functionality](06-Logout_Functionality.md) for details.

## Test Objectives

- Validate that an idle timeout exists and is enforced server-side.
- Validate that an absolute timeout limits the total lifetime of a session.

## How to Test

### Black-Box Testing

#### Idle Timeout

Try to determine the idle timeout by sending requests to a page in the authenticated area of the application with increasing delays between them. When the application logs the user out, the last delay approximately matches the timeout value. After the timeout has passed, all session tokens should be destroyed or be unusable, as described in [Logout Functionality](06-Logout_Functionality.md).

#### Absolute Timeout

1. Log in and note the time.
2. Keep the session active by sending a request to an authenticated page at intervals shorter than the idle timeout, for example with Burp Repeater or a simple script.
3. Continue for an agreed test window, ideally longer than the maximum session lifetime defined in the application's requirements. If there is no such requirement, the values in the Session Management Cheat Sheet (for example 8 hours for a full-day application) can be used as a starting point.
4. The application should require the user to authenticate again before the end of the window, even though the session was never idle. Replay the old session ID afterwards to confirm that it was invalidated server-side.

A black-box test can only show that the session lifetime exceeds the test window. If the session is still valid at the end of it, report the observed lifetime (for example "session still valid after 8 hours of continuous use") rather than concluding that no absolute timeout exists, and confirm the configured value with a gray-box review where possible.

If the application uses single sign-on, an expired session may be renewed silently through the identity provider without asking the user for credentials. In that case, check that a new session ID is issued and the old one is rejected, and keep in mind that the identity provider session has its own lifetime.

#### Client-Side and Server-Side Enforcement

For both timeouts, testers need to understand whether the timeout is enforced by the server, by the client, or both.

The `Expires` and `Max-Age` attributes of a cookie only tell the browser when to delete it, and are never sent back to the server. A session that has disappeared from the browser can therefore still be valid on the server. To test this, capture the session cookie or token, wait until the timeout (or the cookie's expiration time) has passed, then replay the captured value with an intercepting proxy. The server must reject it. In the same way, it should not be possible to access the application again by re-setting the session cookies to previous values.

If the cookie or token value itself contains time related data (e.g., log in time, last access time, or an expiration date) and is not cryptographically protected, try modifying it and see whether the session can be prolonged. For a signed token such as a [JSON Web Token](10-JSON_Web_Tokens.md), modifying the `exp` claim only breaks the signature, so a rejected request shows that the signature is verified, not that the timeout is enforced. Instead, replay the token after its `exp` time has passed, and check that refresh tokens cannot be used to extend the session beyond the absolute timeout.

### Gray-Box Testing

The tester needs to check that:

- An idle timeout is enforced by the server, based on the time since the last request in the session.
- An absolute timeout is enforced by the server, based on the time since the session was created, and is not reset by user activity.
- The configured idle and absolute timeout values match the application's requirements, for example in the application server or framework configuration, or in the time-to-live (TTL) of the session store.
- The server rejects the session identifiers of expired sessions when they are replayed, rather than only marking the sessions as expired.
- If the server uses an expiration time that is read from a token sent by the client (but this is not advisable), the token is cryptographically protected from tampering.

The most important thing is for the application to invalidate the session on the server-side when a timeout expires. Generally this means that the code must invoke the appropriate methods, e.g. `HttpSession.invalidate()` in Java and `Session.abandon()` in .NET. Clearing the cookies from the browser is advisable, but is not strictly necessary, since if the session is properly invalidated on the server, having the cookie in the browser will not help an attacker.

## Tools

- [Burp Suite - Repeater](https://portswigger.net/burp/documentation/desktop/tools/repeater)

## References

### OWASP Resources

- [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
    - [Automatic Session Expiration](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#automatic-session-expiration)
