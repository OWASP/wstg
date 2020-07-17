# Testing for Session Hijacking

|ID          |
|------------|
|WSTG-SESS-09|

## Summary



## How to test

The intuition behind the testing strategy for session hijacking is to simulate a scenario where Mallory steals all Alice's cookies she might be exposed to. We assume that Mallory is a network attacker (i.e. an attacker who has access to the same network as the victim), so we could have a cookie leakage in case of either no [HSTS](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security) adoption and the Secure attribute is not set, or partial HSTS adoption, the Secure attribute is not set and the Domain attribute is set to a parent domain. Mallory may then use these cookies to access Alice's account: if they are enough to act on Alice's behalf, session hijacking is possible. Even when this is not possible, however, security might still be at risk, because it might be that not all the cookies were disclosed to Mallory and the attempted operation failed because just a subset of the expected cookies was sent to the website. To account for this case, we also perform a fresh login to the website as Mallory to get a full set of cookies and then restore the cookies stolen from Alice before reattempting the operation, so that all the website cookies (though mixed from two different accounts) are sent as part of a new operation attempt: if the operation succeeds in Alice's account, session hijacking is possible. Specically, the testing strategy proceeds as follows:
