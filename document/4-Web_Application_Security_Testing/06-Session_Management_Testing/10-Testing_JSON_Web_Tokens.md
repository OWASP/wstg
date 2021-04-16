# Testing JSON Web Tokens (JWTs)

|ID          |
|------------|
|WSTG-SESS-010|

## Summary

- JSON Web Tokens (JWTs) are cryptographically signed JSON tokens
- Commonly used to authenticate on APIs
- Lots of bad implementations and opportunities for things to go wrong

## Test Objectives

- Determine whether the JWTs expose sensitive information.
- Determine whether the JWTs can be tampered with or modified.

## How to Test

### Overview

- What a JWT is
    - Three b64 encoded parters (header, body, signature)
- Common usage scenarios

### Analyse the Contents

- JWTs are not usually encrypted
- May expose sensitive information

### Review Usage

- How is JWT sent?
- How is JWT stored?
- Does JWT expire?
- Can JWT be invalidated?

### Signature Verification

- Signature may not be verified at all (`jwt.decode()` vs `jwt.verify()`)
- `none` or `NoNe` algorithms may be allowed

### Weak HMAC Keys

- HMAC uses a secret key
- Convert JWT into crackable format
- Try and crack key
    - jwt2john
    - May need custom compiled john for long JWT (`SALT_LIMBS`)
    - jwtcrack

### HMAC vs RSA Confusion

- Obtain public key
    - May be in `/.well-known/jwks.json`
    - Can be obtained from TLS cert (shouldn't be re-used, but may be)
- Use public key as a secret to calculate a HMAC

### Attacker Provided RSA Key

- JSON Web Signature (JWS) allows embedding of public key in the header
- Sign with our own private key and see if server trusts it

## Related Test Cases

TODO

## Remediation

TODO

## Tools

- [John the Ripper](https://github.com/openwall/john)
- [jwt2john](https://github.com/Sjord/jwtcrack)
- [jwt-cracker](https://github.com/brendan-rius/c-jwt-cracker)
- [JSON Web Tokens Burp Extension](https://portswigger.net/bappstore/f923cbf91698420890354c1d8958fee6)

## References

- [RFC 7519 JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
