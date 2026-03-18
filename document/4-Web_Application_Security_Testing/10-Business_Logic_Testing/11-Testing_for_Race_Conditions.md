# Testing for Race Conditions

|ID          |
|------------|
|WSTG-BUSL-11|

## Summary

A race condition occurs when the behavior of an application depends on the timing or sequence of events that are not properly controlled. In web applications, this typically manifests when multiple concurrent requests interact with shared state (such as an account balance, an inventory count, or a one-time-use token) without adequate synchronization, allowing an attacker to exploit the time gap between a check and the subsequent action.

This class of vulnerability is commonly referred to as a Time-of-Check to Time-of-Use (TOCTOU) flaw. The application checks a condition (e.g., "does this user have sufficient balance?"), and then acts on it (e.g., "deduct the balance and complete the purchase"). If an attacker sends multiple requests simultaneously, each request may pass the check before any of them have completed the action, resulting in the condition being satisfied multiple times when it should only succeed once.

Race conditions are particularly impactful in functionality involving:

- Financial transactions (transfers, payments, withdrawals)
- One-time-use tokens or codes (coupons, gift cards, referral bonuses)
- Resource allocation with limited availability (inventory, seats, registrations)
- State transitions that should happen exactly once (account activation, approval workflows)

These vulnerabilities are difficult to detect with automated scanners because they require precise timing of concurrent requests and understanding of the application's business logic.

## Test Objectives

- Determine whether the application properly handles concurrent requests to state-changing operations.
- Identify functionality where the time gap between a check and the corresponding action can be exploited through parallel requests.

## How to Test

### Identify Candidate Functionality

Not all endpoints are susceptible to race conditions. Focus on functionality where:

- A value is checked and then modified (balance, inventory, quota)
- An action should only succeed once (redeeming a code, casting a vote, joining a group)
- A resource has limited availability (last item in stock, limited-time offer, registration cap)
- A status transition should be atomic (pending to approved, draft to published)

Common targets include:

- Money transfers and payment processing
- Coupon, gift card, or promotional code redemption
- Reward point or loyalty program transactions
- Voting or rating systems
- File operations (upload, rename, delete)
- Account creation or invitation acceptance
- Group or team membership joins with capacity limits

### Test with Concurrent Requests

The core testing technique is sending multiple identical requests simultaneously and observing whether the application processes more than one successfully when only one should succeed.

#### Using curl

Send parallel requests to a state-changing endpoint:

```bash
# Send 20 concurrent requests to redeem a single-use coupon
for i in $(seq 1 20); do
  curl -s -X POST https://example.com/api/redeem-coupon \
    -H "Cookie: session=USER_SESSION" \
    -H "Content-Type: application/json" \
    -d '{"code":"SINGLE-USE-CODE"}' &
done
wait
```

#### Using Burp Suite Turbo Intruder

Turbo Intruder enables precise concurrent request delivery:

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=20,
                           requestsPerConnection=1,
                           pipeline=False)
    for i in range(20):
        engine.queue(target.req, gate='race')
    engine.openGate('race')

def handleResponse(req, interesting):
    table.add(req)
```

The `gate` parameter ensures all 20 requests are held and released simultaneously, maximizing the chance of hitting the race window.

### Test Financial and Balance Operations

For applications that manage balances, credits, or quantities:

1. Note the current balance (e.g., account has 100 credits).
2. Identify the endpoint that deducts the balance (e.g., `POST /api/purchase`).
3. Send multiple concurrent requests that each spend the full balance.
4. Check whether the total debited exceeds the original balance.

If an account with 100 credits can make two simultaneous purchases of 100 credits each, resulting in a balance of -100 rather than being blocked on the second request, the application is vulnerable.

### Test One-Time-Use Tokens

For coupon codes, invitation links, password reset tokens, or any single-use value:

1. Obtain a valid single-use token.
2. Send multiple concurrent requests that each attempt to use the token.
3. Check how many requests succeed.

If more than one request successfully redeems the token, the application fails to atomically mark the token as used before processing the next request.

### Test Resource Limits

For functionality with capacity constraints (e.g., event registration with 1 spot remaining):

1. Identify the constrained resource and its current availability.
2. Send concurrent requests that each attempt to claim the resource.
3. Check whether more resources are allocated than should be available.

### Test State Transitions

For workflows where an object should transition through states exactly once (e.g., order pending to confirmed):

1. Place the object in its initial state.
2. Send concurrent requests that each attempt to trigger the transition.
3. Check whether the transition triggers duplicate side effects (e.g., multiple confirmation emails, double inventory deductions, repeated webhook notifications).

### Test with Minimal Time Differences

Some applications have race windows that are extremely narrow. To increase the chance of exploitation:

- Use HTTP/2 single-packet attacks where multiple requests are sent within a single TCP packet, ensuring they arrive at the server within microseconds of each other.
- Use Burp Suite Turbo Intruder's gate mechanism for synchronized request release.
- Test from a network location close to the target server to minimize latency variation.
- Increase the number of concurrent requests (20-50) to improve the probability of at least two requests hitting the race window.

## Indicators of Vulnerability

- Two or more concurrent requests to a single-use action both return success responses.
- Account balance goes negative after concurrent debit operations.
- A limited resource is allocated beyond its stated capacity.
- Duplicate side effects occur (multiple emails, double charges, repeated log entries) from what should be a single action.
- The application uses non-atomic read-then-write patterns on shared data (observable through timing differences or error messages under load).

## Remediation

- **Use database-level atomicity.** Wrap check-and-modify operations in database transactions with appropriate isolation levels. Use `SELECT ... FOR UPDATE` or equivalent row-level locking to prevent concurrent reads of the same row during a transaction.
- **Implement optimistic locking.** Add a version column to database records. Before updating, verify the version has not changed since the read. If it has, reject the operation and require the client to retry.
- **Use idempotency keys.** Require clients to supply a unique idempotency key with each state-changing request. The server stores the key and rejects duplicate requests with the same key, regardless of timing.
- **Apply distributed locks.** For state shared across multiple application instances or services, use distributed locking mechanisms (e.g., Redis-based locks, database advisory locks) to serialize access to critical sections.
- **Invalidate tokens atomically.** When consuming a single-use token, use an atomic database operation such as `DELETE FROM tokens WHERE token = ? RETURNING *` or the equivalent for your database. If the delete affects zero rows, another request already consumed the token.
- **Avoid client-side enforcement.** Never rely on disabling a button in the UI or checking a flag in client-side state to prevent double-submission. All enforcement must happen server-side.

## Tools

- [Burp Suite Turbo Intruder](https://portswigger.net/bappstore/9abfe09175524b47bb9345e82984155b): Extension for sending large numbers of precisely timed concurrent HTTP requests.
- [racepwn](https://github.com/racepwn/racepwn): Dedicated race condition testing tool.
- [race-the-web](https://github.com/TheHackerDev/race-the-web): Tool for testing race conditions in web applications by sending concurrent requests.

## References

- [OWASP Testing Guide: Test for Process Timing](04-Test_for_Process_Timing.md)
- [OWASP Testing Guide: Test Number of Times a Function Can Be Used Limits](05-Test_Number_of_Times_a_Function_Can_Be_Used_Limits.md)
- [OWASP Testing Guide: Testing for the Circumvention of Work Flows](06-Testing_for_the_Circumvention_of_Work_Flows.md)
- [PortSwigger Research: Smashing the State Machine](https://portswigger.net/research/smashing-the-state-machine)
- [HackerOne Report #1540969: Race Condition in Joining CTF Group](https://hackerone.com/reports/1540969)
