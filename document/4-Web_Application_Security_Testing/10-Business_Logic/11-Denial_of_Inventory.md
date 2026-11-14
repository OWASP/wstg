# Denial of Inventory

|ID          |
|------------|
|WSTG-BUSL-11|

## Summary

Applications allocate limited business resources, including appointments, products, and rental equipment. Allocation abuse can make those resources unavailable to legitimate customers while the application continues to respond normally. A small number of requests may be sufficient to affect a scarce resource pool.

This test follows resources from allocation through release. It checks whether the application enforces eligibility and aggregate allocation rules, and whether rejected, canceled, or expired reservations return resources to availability. Assess the result against the business's intended allocation policy.

This test provides practical guidance for testing [OAT-021: Denial of Inventory](https://owasp.github.io/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-021_Denial_of_Inventory.html) within the sensitive business flows described by [API6:2023: Unrestricted Access to Sensitive Business Flows](https://api-security.owasp.org/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/).

## Test Objectives

- Identify which actions remove business resources from availability.
- Verify eligibility and aggregate allocation limits across reservation states and booking paths.
- Demonstrate the effect on another eligible customer and verify recovery.

## How to Test

Perform testing against designated test resources or within limits agreed with the application owner. Use a separate account or session to verify whether the test affects other users.

### Identify the Allocation Functions

Follow the normal booking or reservation flow and identify the functions that:

- Display available resources.
- Hold or reserve a resource.
- Confirm the allocation.
- Cancel or release it.

Determine at which point the resource becomes unavailable and whether this happens before verification, payment, or confirmation.

### Understand the Allocation Rules

Identify the expected limits and release conditions:

- How many resources may one customer hold?
- Which verification or commitment is required?
- How long should an incomplete reservation remain active?
- What should happen after cancellation, expiration, or failure?

Where cancellation is supported, create and cancel a normal reservation, then verify that the resource returns to availability.

### Test for Allocation Abuse

#### Incomplete Allocations

Start an allocation but do not complete verification, payment, or confirmation. Check from a separate session whether the resource becomes unavailable and whether it is released after the defined expiration period.

For example, unverified appointment requests may occupy all available time slots.

#### Allocation Limit Bypass

Reach the permitted allocation limit, then create another cart, order, or reservation for the same resource. Check whether the application counts all active allocations together.

For example, a rental service may limit each order to two items while allowing the same customer to create several separate orders.

This test focuses on the total inventory made unavailable. General function-use limits are covered by [Number of Times a Function Can Be Used Limits](05-Number_of_Times_a_Function_Can_Be_Used_Limits.md).

#### Resources Not Released

Cancel an allocation or allow it to expire, then check whether the resource becomes available again. Where applicable, repeat the test after failed verification or payment.

For example, an order may be marked as canceled while its products remain reserved.

Reservation timeout manipulation is covered by [Process Timing](04-Process_Timing.md). This test focuses on whether the resource is released after the allocation ends.

### Evaluate the Result

The application may be vulnerable if one or more of the following conditions apply:

- Resources can be held without the required commitment.
- Allocation limits can be bypassed.
- Canceled or expired reservations continue to consume inventory.
- Another eligible user is prevented from obtaining the resource.
- Limited effort can block a meaningful portion of the available inventory.

A temporary hold is not necessarily a vulnerability if it follows the intended policy, expires within a reasonable period, and does not allow disproportionate allocation.

Record the affected resources, duration, number of requests or allocations, and any manual recovery required. Remove all test allocations after testing.

## Related Test Cases

- [Process Timing](04-Process_Timing.md): transaction duration and unpaid seat holds.
- [Number of Times a Function Can Be Used Limits](05-Number_of_Times_a_Function_Can_Be_Used_Limits.md): limits on repeated function execution.
- [Circumvention of Work Flows](06-Circumvention_of_Work_Flows.md): bypassing required steps in a business process.

## Remediation

- Complete required eligibility checks before confirming an allocation, and limit the duration of temporary holds.
- Apply aggregate resource limits across the relevant states and channels. Make quota checks and allocation updates atomic.
- Keep inventory and reservation state consistent after cancellation, expiration, and failed confirmation or payment.
- Provide reconciliation and targeted cancellation procedures that restore capacity without removing legitimate bookings.

Use the business-flow protection guidance in API6:2023 alongside these allocation controls.
