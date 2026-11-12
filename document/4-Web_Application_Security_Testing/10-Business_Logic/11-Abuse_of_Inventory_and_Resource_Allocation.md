# Abuse of Inventory and Resource Allocation

|ID          |
|------------|
|WSTG-BUSL-11|

## Summary

Applications allocate limited business resources, including appointments, products, and rental equipment. Allocation abuse can make those resources unavailable to legitimate customers while the application continues to respond normally. A small number of requests may be sufficient to affect a scarce resource pool.

This test follows resources from allocation through release. It checks whether the application enforces eligibility and aggregate allocation rules, and whether rejected, canceled, or expired reservations return resources to availability. Assess the result against the business's intended allocation policy.

[OWASP Automated Threat (OAT)-021: Denial of Inventory](https://owasp.github.io/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-021_Denial_of_Inventory.html) describes depletion without completing a purchase or commitment. [API6:2023: Unrestricted Access to Sensitive Business Flows](https://api-security.owasp.org/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/) provides the broader business-flow context, including abusive bookings. Use those sources for threat definitions; this procedure focuses on demonstrating allocation failures and their effect on another customer.

## Test Objectives

- Identify which actions remove business resources from availability.
- Verify eligibility and aggregate allocation limits across reservation states and booking paths.
- Demonstrate the effect on another eligible customer and verify recovery.

## How to Test

### Establish the Allocation Rules and Baseline

Use an isolated test pool or designated test resources. Agree on the maximum allocation, test duration, stop conditions, and cleanup with the application owner. Use two independent test users, A and B, who can access the same pool.

Record:

- The pool and its capacity, scoped to the relevant item, service, location, and period.
- The action that removes a resource from availability and any required verification or commitment.
- The maximum quantity a customer can hold, which reservation states count, and whether the rule spans accounts or booking channels.
- The release conditions and expected processing delay, including any staff recovery procedure.

Resolve undocumented rules with the owner. As User-B, complete a normal allocation, then cancel it and confirm that the baseline capacity returns. Capture the allocation, status, and cancellation requests. Reset the pool between tests.

### Test Allocation Failures

The following examples use hypothetical policies and small test pools. Adapt their values and request fields to the application. Apply the impact and recovery checks below to each example.

#### Example 1: Appointments Allocated without Required Verification

A repair service has three test appointments. Its policy requires contact verification before a booking can remain confirmed. Unverified requests may hold a slot only for a defined confirmation window.

1. As User-A, follow the normal booking flow using a controlled, unverified contact. Do not complete verification.
2. Check the actual booking state and availability. If the application marks the booking confirmed, determine whether this state bypasses the release rule for unverified requests.
3. Repeat for the remaining test slots, within the agreed bounds. As User-B, attempt to book from the same pool.
4. After the confirmation window and processing delay, check whether the unverified bookings still occupy capacity. Use the supported recovery path to remove them, then retry as User-B.

Expected result: the application enforces the verification policy and releases unverified allocations as specified. Record whether falsely confirmed bookings require staff intervention. A free booking or the absence of contact verification is not a finding unless it violates the agreed policy or exposes a demonstrated abuse case.

#### Example 2: Separate Orders Exceed the Customer's Inventory Allowance

A rental service has six test projectors for one rental period. A customer may hold two projectors in total before checkout. The application validates each order separately but may fail to count the customer's existing holds.

1. As User-A, create a hold for two projectors using the normal request. Do not complete checkout.
2. Submit a second order for two projectors, using a new order identifier but the same customer and period. If supported, compare the regular and bulk booking paths.
3. Verify the total actually allocated to A. If the second order succeeds, repeat once to reach the six-projector test capacity, then attempt an allocation as User-B.
4. Cancel User-A's holds and repeat User-B's attempt.

Expected result: no booking path allows User-A's combined active holds to exceed two. Compare allocation quantities, not just request counts: one request may allocate several units. For general function-use limit tests, see [Number of Times a Function Can Be Used Limits](05-Number_of_Times_a_Function_Can_Be_Used_Limits.md).

#### Example 3: Canceled Reservations Leave Inventory Unavailable

A store reserves three test products during checkout. Canceling an unpaid order should release its units, but the cancellation path may update the order without releasing the inventory reservation.

1. As User-A, reserve one product, cancel the unpaid order, and confirm that its status becomes canceled.
2. After the documented processing delay, check whether the product returns to availability. As User-B, attempt to reserve it; do not rely only on the displayed stock count.
3. If the unit remains blocked, repeat with the remaining test units to determine whether stale reservations accumulate. Check User-B's access to the pool again.
4. Have the owner run the supported reconciliation or administrative release procedure. Verify that User-B can reserve the recovered products.

Expected result: canceled orders no longer consume inventory. If a supported flow includes payment failure, test that release path separately. This checks reservation consistency after a state change; use [Process Timing](04-Process_Timing.md) for transaction timeout and hold-extension testing.

### Verify Customer Impact and Recovery

For each case, collect the following observations using the same eligible User-B and resource pool:

| Stage | Allocation Evidence | Customer Access |
|-------|---------------------|-----------------|
| Baseline | Known available capacity | User-B can allocate; cancel to restore the pool. |
| After User-A's test | Quantity and state of User-A's allocations or stale reservations | User-B cannot allocate resources made unavailable by A. |
| After release or recovery | Capacity restored within the expected delay | User-B can allocate again. |

Record the relevant requests, responses, reservation identifiers, quantities, and timestamps. Note the number of requests, duration of the blockage, and any staff action needed. Keep an unrelated application function as a control to distinguish inventory unavailability from a general outage.

Confirm that User-B's failure results from User-A's allocations, not a customer restriction, stale display, or different booking period. A successful response alone does not prove allocation; inability to book one occupied slot does not prove exhaustion of the entire pool. Report only the demonstrated scope, and identify any unverified impact.

Remove all test allocations, including stale reservations, and verify both availability and customer quota counters. If cleanup fails, provide the owner with the affected identifiers for recovery.

## Related Test Cases

- [Process Timing](04-Process_Timing.md): transaction duration and unpaid seat holds.
- [Number of Times a Function Can Be Used Limits](05-Number_of_Times_a_Function_Can_Be_Used_Limits.md): limits on repeated function execution.
- [Circumvention of Work Flows](06-Circumvention_of_Work_Flows.md): bypassing required steps in a business process.

## Remediation

- Enforce eligibility before granting the allocation state that requires it.
- Apply aggregate resource limits across the relevant states and channels. Make quota checks and allocation updates atomic.
- Keep inventory and reservation state consistent after cancellation, expiration, and failed confirmation or payment.
- Provide reconciliation and targeted cancellation procedures that restore capacity without removing legitimate bookings.

Use the business-flow protection guidance in API6:2023 alongside these allocation controls.
