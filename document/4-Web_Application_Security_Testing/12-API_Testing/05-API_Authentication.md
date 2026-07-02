# Testing API Authentication

|ID          |
|------------|
|WSTG-APIT-05|

## Summary

APIs (Application Programming Interfaces) form the backbone of many modern web and mobile applications. Because APIs often provide direct access to sensitive data and core business logic, robust authentication is essential. Vulnerabilities in API authentication (such as insecure API keys, flawed JSON Web Token (JWT) implementations, or entirely unprotected endpoints) can allow attackers to take over accounts, steal data, or compromise the entire system.

## Test Objectives

- Identify all API endpoints and their respective authentication mechanisms.
- Test whether API endpoints can be accessed without valid authentication.
- Verify the integrity, confidentiality, and security of the tokens and API keys in use.

## How to Test

### Missing Authentication

Look for API endpoints that should normally require authentication but still return a successful response even without or with invalid credentials.

1. Intercept the API traffic (e.g., using Burp Suite or OWASP ZAP).
2. Remove authentication headers (like `Authorization`) or session cookies from the request.
3. Resend the request. Check if the API still executes the action (e.g., returns a `200 OK` status code) or leaks sensitive data.

### API Key Exposure and Predictability

API keys are often used to authenticate clients.

- **Hardcoding:** Check if API keys are hardcoded in the source code (e.g., in JavaScript files, mobile apps, or public GitHub repositories).
- **Structure:** Analyze the structure of the keys. Are they predictable, easily guessable, or generated sequentially?
- **Transmission:** Check if the API keys are passed as URL parameters (e.g., `GET /api/data?apikey=123`). This is insecure because URLs are logged in web server logs, proxies, and browser histories. Keys should always be transmitted via HTTP headers.

### JWT (JSON Web Token) Vulnerabilities

If the API uses JWTs, test for common implementation flaws:

- **"None" Algorithm:** Change the `alg` header in the JWT to `none`, completely remove the signature, and send the token to the API.
- **Weak Secret (Brute Force):** Attempt to crack the secret used to sign the token offline using brute-force tools.
- **Algorithm Confusion:** If the API expects asymmetric encryption (like `RS256`), change the algorithm to symmetric (`HS256`) and sign the token using the application's public key.

## Remediation

- Rely on established and standardized authentication protocols like OAuth 2.0 or OpenID Connect.
- Transmit API keys and tokens exclusively via HTTP headers (e.g., `Authorization: Bearer <token>`) and enforce TLS (HTTPS).
- Strictly validate tokens on the server side (verifying the signature, algorithm, expiration `exp`, and issuer `iss`).
- Implement rate-limiting and account lockout mechanisms for authentication endpoints to prevent brute-force attacks.

## Tools

- Burp Suite / OWASP ZAP
- Postman
- JWT_Tool / Hashcat

## References

- OWASP API Security Top 10 - API2: Broken Authentication
- OWASP JSON Web Token (JWT) Cheat Sheet
- -- START OF FILE 01-Testing_for_Insecure_Design.md ---