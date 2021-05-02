# Testing JSON Web Tokens

|ID          |
|------------|
|WSTG-SESS-010|

## Summary

JSON Web Tokens (JWTs) are cryptographically signed JSON tokens, intended to share claims between systems. They are are frequently used as authentication or session tokens, particularly on REST APIs.

JWTs are a common source of vulnerabilities, both in how they are in implemented in applications, and in the underlying libraries. As they are used for authentication, a vulnerability can easily result in a complete compromise of the application.

## Test Objectives

- Determine whether the JWTs expose sensitive information.
- Determine whether the JWTs can be tampered with or modified.

## How to Test

### Overview

JWTs are are made up of three components:

- The header
- The payload (or body)
- The signature

Each component is Base64 encoded, and they are separated by periods (`.`). Note that the Base64 encoding used in a JWT strips out the equals signs (`=`), so you may need to add these back in to decode the sections.

### Analyse the Contents

#### Header

The header of a defines the type of the token (typically `JWT`), and the algorithm used for the signature. A example decoded header is shown below:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

There are three main types of algorithms that are used to calculate the signatures:

| Algorithm | Description |
|--------------|----------------|
| HSxxx | HMAC using a secret key and SHA-xxx |
| RSxxx and PSxxx | Public key signature using RSA |
| ESxxx | Public key signature using ECDSA |

There are also a wide range of [other algorithms](https://www.iana.org/assignments/jose/jose.xhtml#web-signature-encryption-algorithms) which may be used for encrypted tokens (JWEs), although these are less common.s

#### Payload

The payload of the JWT contains the actual data. An example payload is shown below:

```json
{
  "username": "admininistrator",
  "is_admin": true,
  "iat": 1516239022,
  "exp": 1516242622
}
```

The payload is it not usually encrypted, so review it to determine whether there is any sensitive of potentially inappropriate data included within it.

This JWT includes the username and administrative status of the user, as well as two standard claims (`iat` and `exp`). These claims are defined in [RFC 5719](https://tools.ietf.org/html/rfc7519#section-4.1), a brief summary of them is given in the table below:

| Claim | Full Name | Description |
|---------|-------------|-------------|
| `iss` | Issuer | The identity of the party who issued the token. |
| `iat` | Issued At | The Unix timestamp of when the token was issued. |
| `nbf` | Not Before | The Unix timestamp of earliest date that the token can be used. |
| `exp` | Expires | The Unix timestamp of when the token expires. |

#### Signature

The signature is calculated using the algorithm defined in the JWT header, and then Base64 encoded and appened to the token. Modifying any part of the JWT should cause the signature to be invalid, and the token to be rejected by the server.

### Review Usage

As well as being cryptographically secure itself, the JWT also needs to be stored and sent in a secure manner. This should include checks that:

- It is always [sent over encrypted (HTTPS) connections](../09-Testing_for_Weak_Cryptography/03-Testing_for_Sensitive_Information_Sent_via_Unencrypted_Channels.md).
- If it is stored in a cookie, then it should be [marked with appropriate attributes](../06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md).
- If it is stored in the browser storage, it should [use the sessionStorage rather than localStorage](../11-Client-side_Testing/12-Testing_Browser_Storage.md).

The validity of the JWT should also be reviewed, based on the `iat`, `nbf` and `exp` claims, to determine that:

- The JWT has a reasonable lifespan for the application.
- Expired tokens are rejected by the application.

### Signature Verification

One of the most serious vulnerabilities encountered with JWTs is when the application fails to validate that the signature is correct. This usually occurs when a developer uses a function such as the NodeJS `jwt.deode()` function, which simply decodes the body of the JWT, rather than `jwt.verify()`, which verifies the signature before decoding the JWT.

This can be easily tested for by modifying the body of the JWT without changing anything in the header or signature, submitting it in a request to see if the application accepts it.

#### The None Algorithm

As well as the public key and HMAC-based algorithms, the JWT specification also defines a signature algorithm called `none`. As the name suggests, this means that there is no signature for the JWT, allowing it to be modified.

This can be tested by modifying the signature algorithm (`alg`) in the JWT header to `none`, and resubmitting the JWT.

Some implementation try and avoid this by explicitly blocking the use of the `none` algorithm. If this is done in a case-insensitive way, it may be possible to bypass by specifying an algorithm such as `NoNe`.

### Weak HMAC Keys

If the JWT is signed using a HMAC-based algorithm (such as HS256), the security of the signature is entirely reliant on the strength of the secret key used in the HMAC.

If the application is using off-the-shelf or open source software, the first step should be go investigate the code, and see whether there is default HMAC signing key that is used.

If there isn't a default, then it may be possible to crack guess or brute-force they key. The simplest way to do this is to use the [crackjwt.py](https://github.com/Sjord/jwtcrack) script, which simply requires the JWT and a dictionary file.

A more powerful option is to convert convert the JWT into a format that can be used by [John the Ripper](https://github.com/openwall/john) using the [jwt2john.py](https://github.com/Sjord/jwtcrack/blob/master/jwt2john.py) script. John can then be used to carry out much more advanced attacks against the key.

If the JWT is large, it may exceed the maximum size supported by John. This can be worked around by increasing the value of the `SALT_LIMBS` variable in `/src/hmacSHA256_fmt_plug.c` (or the equivalent file for other HMAC formats) and recompiling John.

If this key can be obtained, then it is possible to create and sign arbitrary JWTs, which usually results in a complete compromise of the application.

### HMAC vs Public Key Confusion

If the application uses JWTs with public key based signatures, but does not check that the algorithm is correct, this can potentially exploit this in a signature type confusion attack. In order for this to be successful, the following conditions need to be met:

- The application must use public key (i.e, `RSxxx` or `ESxxx`) to verify the JWT signature.
- The application must not check which algorithm is actually used.
- The public key used to verify the JWT must be available to the attacker.

The main way that an attacker would be able to obtain the public key is if the application re-uses the same key for both signing JWTs and as part of the TLS certificate. This key can be downloaded from the server using a command such as the following:

```sh
openssl s_client -connect example.org:443 | openssl x509 -pubkey -noout
```

Alternatively, the key may be available from a public file on the site at a common location such as `/.well-known/jwks.json`.

In order to test this, modify the contents of the JWT, and then use the previously obtained public key to sign the JWT using the `HS256` algorithm. This is often difficult to perform when testing without access to the source code or implementation deatils, because the format of the key must be identical to the one used by the server, so issues such as emptyspace or CRLF encoding may result in the keys not matching.

### Attacker Provided Public Key

The JSON Web Signature (JWS) standard allows the key used to sign the token to be embedded in the header. If the library used to validate the token supports this, and doesn't check the key against a list of approved keys, this allows an attacker to sign an JWT with an arbitrary key that they provide.

There are a variety of scripts that can be used to do this, such as [jwk-node-jose.py](https://github.com/zi0Black/POC-CVE-2018-0114) or [jwt_tool](https://github.com/ticarpi/jwt_tool).

## Related Test Cases

- [Testing for Sensitive Information Sent via Unencrypted Channels](../09-Testing_for_Weak_Cryptography/03-Testing_for_Sensitive_Information_Sent_via_Unencrypted_Channels.md).
- [Testing for Cookie Attributes](../06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md).
- [Testing Browser Storage](../11-Client-side_Testing/12-Testing_Browser_Storage.md).

## Remediation

- Use a secure and up to date library to handle JWTs.
- Use a strong HMAC key or a unique private key to sign them.
- Ensure that there is no sensitive information exposed in the payload.
- Ensure that JWTs are securely stored and transmitted.
- See the [OWASP JSON Web Tokens Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

## Tools

- [John the Ripper](https://github.com/openwall/john)
- [jwt2john](https://github.com/Sjord/jwtcrack)
- [jwt-cracker](https://github.com/brendan-rius/c-jwt-cracker)
- [JSON Web Tokens Burp Extension](https://portswigger.net/bappstore/f923cbf91698420890354c1d8958fee6)
- [ZAP JWT Add-on](https://github.com/SasanLabs/owasp-zap-jwt-addon)

## References

- [RFC 7519 JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
