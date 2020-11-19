# Testing for Session Hijacking

|ID          |
|------------|
|WSTG-SESS-09|

## Summary

An attacker who gets access to user session cookies can impersonate them by presenting such cookies. This attack is known as session hijacking. When considering network attackers, i.e., attackers who control the network used by the victim, session cookies can be unduly exposed to the attacker over HTTP. To prevent this, session cookies should be marked with the `Secure` attribute so that they are only communicated over HTTPS.

Note that the `Secure` attribute should also be used when the web application is entirely deployed over HTTPS, otherwise the following cookie theft attack is possible. Assume that `example.com` is entirely deployed over HTTPS, but does not mark its session cookies as `Secure`. The following attack steps are possible:

1. The victim sends a request to `http://another-site.com`.
2. The attacker corrupts the corresponding response so that it triggers a request to `http://example.com`.
3. The browser now tries to access `http://example.com`.
4. Though the request fails, the session cookies are leaked in the clear over HTTP.

Alternatively, session hijacking can be prevented by banning use of HTTP using [HSTS](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security). Note that there is a subtlety here related to cookie scoping. In particular, full HSTS adoption is required when session cookies are issued with the `Domain` attribute set.

Full HSTS adoption is described in a paper called *Testing for Integrity Flaws in Web Sessions* by Stefano Calzavara, Alvise Rabitti, Alessio Ragazzo, and Michele Bugliesi. Full HSTS adoption occurs when a host activates HSTS for itself and all its sub-domains. Partial HSTS adoption is when a host activates HSTS just for itself.

With the `Domain` attribute set, session cookies can be shared across sub-domains. Use of HTTP with sub-domains should be avoided to prevent the disclosure of unencrypted cookies sent over HTTP. To exemplify this security flaw, assume that the website `example.com` activates HSTS without the `includeSubDomains` option. The website issues session cookies with the `Domain` attribute set to `example.com`. The following attack is possible:

1. The victim sends a request to `http://another-site.com`.
2. The attacker corrupts the corresponding response so that it triggers a request to `http://fake.example.com`.
3. The browser now tries to access `http://fake.example.com`, which is permitted by the HSTS configuration.
4. Since the request is sent to a sub-domain of `example.com` with the `Domain` attribute set, it includes the session cookies, which are leaked in the clear over HTTP.

Full HSTS should be activated on the apex domain to prevent this attack.

## Test Objectives

- Identify vulnerable session cookies.
- Hijack vulnerable cookies and assess the risk level.

## How to Test

The testing strategy is targeted at network attackers, hence it only needs to be applied to sites without full HSTS adoption (sites with full HSTS adoption are secure, since their cookies are not communicated over HTTP). We assume to have two testing accounts on the website under test, one to act as the victim and one to act as the attacker. We simulate a scenario where the attacker steals all the cookies which are not protected against disclosure over HTTP, and presents them to the website to access the victim's account. If these cookies are enough to act on the victim's behalf, session hijacking is possible.

Here are the steps for executing this test:

1. Login to the website as the victim and reach any page offering a secure function requiring authentication.
2. Delete from the cookie jar all the cookies which satisfy any of the following conditions.
    - in case there is no HSTS adoption: the `Secure` attribute is set.
    - in case there is partial HSTS adoption: the `Secure` attribute is set or the `Domain` attribute is not set.
3. Save a snapshot of the cookie jar.
4. Trigger the secure function identified at step 1.
5. Observe whether the operation at step 4 has been performed successfully. If so, the attack was successful.
6. Clear the cookie jar, login as the attacker and reach the page at step 1.
7. Write in the cookie jar, one by one, the cookies saved at step 3.
8. Trigger again the secure function identified at step 1.
9. Clear the cookie jar and login again as the victim.
10. Observe whether the operation at step 8 has been performed successfully in the victim's account. If so, the attack was successful; otherwise, the site is secure against session hijacking.

We recommend using two different machines or browsers for the victim and the attacker. This allows you to decrease the number of false positives if the web application does fingerprinting to verify access enabled from a given cookie. A shorter but less precise variant of the testing strategy only requires one testing account. It follows the same pattern, but it halts at step 5 (note that this makes step 3 useless).

## Tools

- [OWASP ZAP](https://www.zaproxy.org)
- [JHijack - a numeric session hijacking tool](https://sourceforge.net/projects/jhijack/)
