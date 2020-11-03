# Testing for Session Hijacking

|ID          |
|------------|
|WSTG-SESS-09|

## Summary

An attacker who gets access to a honest user's session cookies can impersonate her by presenting such cookies: this attack is known as session hijacking. When considering network attackers, i.e., attackers who control the network used by the victim, session cookies can be unduly exposed to the attacker over HTTP. To prevent this, session cookies should be marked with the `Secure` attribute, so that they are only communicated over HTTPS.

Note that the `Secure` attribute should be used also when the web application is entirely deployed over HTTPS, otherwise the following cookie theft attack is possible. Assume that `example.com` is entirely deployed over HTTPS, but does not mark its session cookies as `Secure`:

1. The victim sends a request to `http://another-site.com`
2. The attacker corrupts the corresponding response so that it triggers a request to `http://example.com`
3. The browser now tries to access `http://example.com`
4. Though the request fails, the session cookies are leaked in clear over HTTP.

Alternatively, session hijacking can be prevented by banning HTTP communication using [HSTS](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security). Note that there is a subtlety here related to cookie scoping. In particular, full HSTS adoption* is required when session cookies are issued with the `Domain` attribute set. These cookies can be shared across sub-domains, hence HTTP communication with sub-domains should be banned as well to prevent their disclosure. To exemplify this security flaw, assume that `example.com` activates HSTS without the `includeSubDomains` option and issues session cookies with the `Domain` attribute set to `example.com`, then the following attack is possible:

1. The victim sends a request to `http://another-site.com`
2. The attacker corrupts the corresponding response so that it triggers a request to `http://fake.example.com`
3. The browser now tries to access `http://fake.example.com`, which is allowed by the HSTS configuration
4. Since the request is sent to a sub-domain of `example.com`, it includes the session cookies, which are leaked in clear over HTTP.

Note that full HSTS should be activated on the apex domain to prevent this attack.

> `*` We refer to full HSTS adoption when a host activates HSTS for itself and all its sub-domains, and to partial HSTS adoption when a host activates HSTS just for itself.
> Ref: Calzavara, S., Rabitti, A., Ragazzo, A., Bugliesi, M.: Testing for Integrity Flaws in Web Sessions.

## How to test

### Black-Box Testing

The testing strategy is targeted at network attackers, hence it only needs to be applied to sites without full HSTS adoption (sites with full HSTS adoption are trivially secure, since their cookies can never be communicated over HTTP). We assume to have two testing accounts on the website under test, one to act as the victim and one to act as the attacker. We simulate a scenario where the attacker steals all the cookies which are not protected against disclosure over HTTP, and presents them to the website to access the victim's account: if these cookies are enough to act on the victim's behalf, session hijacking is possible.

The proposed testing strategy proceeds as follows:

1. Login to the website as the victim and reach any page offering a security-sensitive functionality requiring authentication;
2. Delete from the cookie jar all the cookies which satisfy either of the following conditions:
    * in case there is no HSTS adoption: the `Secure` attribute is set;
    * in case there is partial HSTS adoption: the `Secure` attribute is set or the `Domain` attribute is not set;
3. Save a snapshot of the cookie jar;
4. Trigger the security-sensitive functionality identified at step 1;
5. Check: has the operation at step 4 been performed? If yes, halt and report as insecure;
6. Clear the cookie jar, login as the attacker and reach the page at step 1;
7. Write in the cookie jar, one by one, the cookies saved at step 3;
8. Trigger again the security-sensitive functionality identified at step 1;
9. Clear the cookie jar and login again as the victim;
10. Check: has the operation at step 8 been performed in the victim's account? If yes, halt and report as insecure; otherwise, report as secure.

We recommend using two different machines or browsers for the victim and the attacker. This allows one to decrease the number of false positives if the web application does fingerprinting to verify an access enabled from a given cookie. A less precise, yet easier, variant of the testing strategy only requires one testing account: it follows the same pattern, but it halts at step 5 (note that this makes step 3 useless).

## Tools

* [OWASP ZAP](https://www.zaproxy.org)
* [JHijack - a numeric session hijacking tool](https://sourceforge.net/projects/jhijack/)
