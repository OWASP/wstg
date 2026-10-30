# Session Timeout

|ID          |
|------------|
|WSTG-SESS-07|

## Summary

In this phase testers check that the application automatically logs out a user when that user has been idle for a certain amount of time, or when the session reaches its maximum lifetime, ensuring that it is not possible to "reuse" the same session and that no sensitive data remains stored in the browser cache.

All applications should implement an idle or inactivity timeout for sessions. This timeout defines the amount of time a session will remain active in case there is no activity by the user, closing and invalidating the session upon the defined idle period since the last HTTP request received by the web application for a given session ID. The most appropriate timeout should be a balance between security (shorter timeout) and usability (longer timeout) and heavily depends on the sensitivity level of the data handled by the application. For example, a 60 minute log out time for a public forum can be acceptable, but such a long time would be too much in a home banking application (where a maximum timeout of 15 minutes is recommended). In any case, any application that does not enforce a timeout-based log out should be considered not secure, unless such behavior is required by a specific functional requirement.

The idle timeout limits the chances that an attacker has to guess and use a valid session ID from another user, and under certain circumstances could protect public computers from session reuse. However, if the attacker is able to hijack a given session, the idle timeout does not limit the attacker’s actions, as he can generate activity on the session periodically to keep the session active for longer periods of time.

This is why applications should also enforce an absolute timeout, which limits the total lifetime of a session regardless of activity. Once it expires, the user has to authenticate again even if the session was never idle. Its value also depends on the sensitivity of the application, for example a few hours for a banking application or a working day for an internal business application.

Session timeout management and expiration must be enforced server-side. If some data under the control of the client is used to enforce the session timeout, for example using cookie values or other client parameters to track time references (e.g. number of minutes since log in time), an attacker could manipulate these to extend the session duration. So the application has to track the inactivity time and the session age server-side and, after a timeout is expired, automatically invalidate the current user's session and delete every data stored on the client.

When either timeout expires, the session must be terminated in the same way as on log out: all session tokens (e.g. cookies) must be destroyed or made unusable server-side, so that they cannot be replayed to "resurrect" the session of a legitimate user. See [Logout Functionality](06-Logout_Functionality.md) for details.

The most common scenario for this kind of attack is a public computer that is used to access some private information (e.g., web mail, online bank account). If the user moves away from the computer without explicitly logging out and the session timeout is not implemented on the application, then an attacker could access to the same account by simply pressing the "back" button of the browser.

## Test Objectives

- Validate that an idle timeout exists and is enforced server-side.
- Validate that an absolute timeout limits the total lifetime of a session.

## How to Test

### Black-Box Testing

#### Idle Timeout

Try to determine the idle timeout by sending requests to a page in the authenticated area of the application with increasing delays between them. When the application logs the user out, the last delay approximately matches the timeout value. After the timeout has passed, all session tokens should be destroyed or be unusable, as described in [Logout Functionality](06-Logout_Functionality.md).

Then, if the timeout is configured, testers need to understand whether the timeout is enforced by the client or by the server (or both). If the session cookie is non-persistent (or, more in general, the session cookie does not store any data about the time), testers can assume that the timeout is enforced by the server. If the session cookie contains some time related data (e.g., log in time, or last access time, or expiration date for a persistent cookie), then it's possible that the client is involved in the timeout enforcing. In this case, testers could try to modify the cookie (if it's not cryptographically protected) and see what happens to the session. For instance, testers can set the cookie expiration date far in the future and see whether the session can be prolonged.

As a general rule, everything should be checked server-side and it should not be possible, by re-setting the session cookies to previous values, to access the application again.

#### Absolute Timeout

1. Log in and note the time.
2. Keep the session active by sending a request to an authenticated page at intervals shorter than the idle timeout, for example with [Burp Repeater](https://portswigger.net/burp/documentation/desktop/tools/repeater) or a simple script.
3. Continue past a reasonable maximum lifetime for the application (see the Summary for typical values).
4. The application should eventually require the user to authenticate again, even though the session was never idle. If the session stays valid for as long as it keeps being used, no absolute timeout is enforced.

If the session lifetime appears to be tied to a value the client controls, such as the `Expires` or `Max-Age` attribute of a cookie or a timestamp inside a token (for example the `exp` claim of a [JSON Web Token](10-JSON_Web_Tokens.md)), check whether modifying it extends the session. As with the idle timeout, the limit must be enforced server-side.

### Gray-Box Testing

The tester needs to check that:

- An idle timeout is enforced by the server, based on the time since the last request in the session.
- An absolute timeout is enforced by the server, based on the time since the session was created, and is not reset by user activity.
- If the server uses an expiration time that is read from a token sent by the client (but this is not advisable), the token is cryptographically protected from tampering.

The most important thing is for the application to invalidate the session on the server-side when a timeout expires. Generally this means that the code must invoke the appropriate methods, e.g. `HttpSession.invalidate()` in Java and `Session.abandon()` in .NET. Clearing the cookies from the browser is advisable, but is not strictly necessary, since if the session is properly invalidated on the server, having the cookie in the browser will not help an attacker.

## References

### OWASP Resources

- [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
    - [Automatic Session Expiration](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#automatic-session-expiration)
