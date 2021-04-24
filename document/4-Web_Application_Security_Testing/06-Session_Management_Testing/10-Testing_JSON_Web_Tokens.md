# Testing JSON Web Tokens

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

#### Header

- Header includes the algorithm
    - Algorithms have type (RS/PS/HS/ES) and strength in bits
    - Table of common algorithms
    - Ideally should be `HSxxx` (for HMAC) or `ESxxx` for public key
    - RSA (`RSxxx` and `PSxxx`) is legacy, but still acceptable
    - [Other algorithms](https://www.iana.org/assignments/jose/jose.xhtml#web-signature-encryption-algorithms) may also be used, especially for encryption tokens

#### Body

- JWTs are not usually encrypted
- Some standard fields (table)
    - iss = Issuer
    - iat = Issued At
    - nbf = Not Before
    - exp = Expiration Time
- Can also include custom data
    - May expose sensitive information

### Review Usage

- How is JWT sent?
- How is JWT stored?
- Does JWT expire?
- Can JWT be invalidated?

### Signature Verification

One of the most serious vulnerabilities encountered with JWTs is when the application fails to validate that the signature is correct. This usually occurs when a developer uses a function such as the NodeJS `jwt.deode()` function, which simply decodes the body of the JWT, rather than `jwt.verify()`, which verifies the signature before decoding the JWT.

This can be easily tested for by modifying the body of the JWT without changing anything in the header or signature, submitting it in a request to see if the application accepts it.

#### The None Algorithm

As well as the public key and HMAC-based algorithms, the JWT specification also defines a signature algorithm called `none`. As the name suggests, this means that there is no signature for the JWT, allowing it to be modified.

This can be tested by modifying the signature algorithm (`alg`) in the JWT header to `none`, and resubmitting the JWT.

Some implementation try and avoid this by blacklisting the use of the `none` algorithm. If this is done in a case-insensitive way, it may be possible to bypass by specifying an algorithm such as `NoNe`.

### Weak HMAC Keys

If the JWT is signed using a HMAC-based algorithm (such as HS256), the security of the signature is entirely reliant on the strength of the secret key used in the HMAC.

If the application is using off-the-shelf or open source software, the first step should be go investigate the code, and see whether there is default HMAC signing key that is used.

If there isn't a default, then it may be possible to crack guess or brute-force they key. The simplest way to do this is to use the [crackjwt.py](https://github.com/Sjord/jwtcrack) script, which simply requires the JWT and a dictionary file.

A more powerful option is to convert convert the JWT into a format that can be used by [John the Ripper](https://github.com/openwall/john) using the [jwt2john.py](https://github.com/Sjord/jwtcrack/blob/master/jwt2john.py) script. John can then be used to carry out much more advanced attacks against the key.

If the JWT is large, it may exceed the maximum size supported by John. This can be worked around by increasing the value of the `SALT_LIMBS` variable in `/src/hmacSHA256_fmt_plug.c` (or the equivalent file for other HMAC formats) and recompiling John.

If this key can be obtained, then it is possible to create and sign arbitrary JWTs, which usually results in a complete compromise of the application.

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
- [ZAP JWT Add-on](https://github.com/SasanLabs/owasp-zap-jwt-addon)

## References

- [RFC 7519 JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
