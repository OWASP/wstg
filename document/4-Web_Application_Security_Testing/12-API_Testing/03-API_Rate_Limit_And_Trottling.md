# API Rate Limiting and Throttling on Payment & AI APIs

## Objective

Ensure that APIs exposed for payment processing or AI inference enforce rate limiting to mitigate abuse, denial-of-service, or automated fraud.

## Test Steps

1. Identify critical API endpoints—e.g., `/api/pay`, `/api/charge`, `/api/model/infer`.
2. Select a load testing tool (e.g., JMeter, Locust, curl with loops, or an in-house script).
3. Simulate high-frequency requests exceeding normal usage thresholds.
4. Verify API responses:
   - HTTP `429 Too Many Requests`, or other appropriate error codes (e.g., `503` if configured).
   - Consistent response across various attack rates.
5. Ensure legitimate users under threshold still receive successful responses.
6. Check logs or monitoring systems for rate-limit triggers or alerts.
7. Test reset behavior — wait for the configured window (e.g., 1 minute), then resend requests to confirm limits have been lifted.
8. Confirm configurability — rate limit thresholds, window size, and behavior can be adjusted as needed.

## Expected Result

API enforces rate limiting effectively, ensuring the system remains operational and secure under excessive request loads, while providing resilience against abuse or transaction flood, especially vital in financial and AI-driven environments.

## Rationale

Without explicit rate limiting, APIs — particularly those handling financial or high-value AI inference calls — are vulnerable to automated abuse, resource exhaustion, or fraud attempts. This test helps safeguard system integrity and ensures adherence to best practices.

## Related Test Cases

- WSTG-BUSL-07: Defenses Against Application Misuse  
- WSTG-BUSL-05: Function Call Limits  

## References

- [OWASP API Security Top 10 – API4: Lack of Rate Limiting](https://owasp.org/www-project-api-security/)  
- OWASP SCWE-077 — Lack of Rate Limiting in Smart Contracts (relevant analogy)
