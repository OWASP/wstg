# Weak Cryptographic Primitives

|ID          |
|------------|
|WSTG-CRYP-04|

## Summary

Incorrect uses of encryption algorithms may result in sensitive data exposure, key leakage, broken authentication, insecure session, and spoofing attacks. There are some encryption or hash algorithms known to be weak and are not suggested for use such as MD5 and RC4.

In addition to the right choices of secure encryption or hash algorithms, the right uses of parameters also matter for the security level. For example, ECB (Electronic Code Book) mode generally should not be used.

## Test Objectives

- Provide a guideline for the identification weak encryption or hashing uses and implementations.
- Identify weak digital signature algorithms and missing or incorrect signature verification.

## How to Test

### Basic Security Checklist

Encryption, digital signatures and hashing solve different problems and use different algorithms, so check each use on its own. Encryption keeps data confidential, a signature proves who produced the data and that it wasn't changed, and a hash is a one-way fingerprint with no key.

#### Encryption

- When using AES128 or AES256, the IV (Initialization Vector) must be random and unpredictable. Refer to [FIPS 140-3, Security Requirements for Cryptographic Modules](https://csrc.nist.gov/pubs/fips/140-3/final), section random number generation tests. For example, in Java, `java.util.Random` is considered a weak random number generator. `java.security.SecureRandom` should be used instead of `java.util.Random`.
- When a symmetric encryption algorithm is used, ECB (Electronic Code Book) mode should not be used. Prefer an authenticated mode such as GCM.
- For SSH, CBC mode should not be used.
- Weak ciphers such as RC4, DES, Blowfish and two-key triple DES (2TDEA, 80-bit security) should not be used.
- Asymmetric encryption is normally done with a hybrid scheme: an elliptic curve key exchange such as X25519 (ECDH over `Curve25519`) or ECDH with P-256 agrees on a symmetric key, which then encrypts the data. Where RSA is used to encrypt directly, it needs OAEP padding and a key of at least 2048 bits. RSA with PKCS#1 v1.5 encryption padding is vulnerable to padding oracle attacks.

#### Digital Signatures

- Use RSA with PSS padding (RSASSA-PSS) and a key of at least 2048 bits, ECDSA with a curve of at least 256 bits such as P-256, or EdDSA (`Ed25519`). These are among the algorithms approved in [FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final), which no longer approves DSA for generating new signatures.
- Keys that are too short, such as 1024-bit RSA or DSA and 160-bit ECDSA curves, should not be used.
- Signatures must not use SHA-1 or MD5 as the hash. [NIST SP 800-131A](https://csrc.nist.gov/pubs/sp/800/131/a/r2/final) disallows SHA-1 for generating digital signatures.
- A signature only protects data if it is verified. Check that the application verifies signatures before trusting the data, with a key it trusts, and that it doesn't let the signed data choose the algorithm, such as `alg: none` in a JSON Web Token (see [JSON Web Tokens](../06-Session_Management/10-JSON_Web_Tokens.md)).

#### Hashing and Password Storage

- Weak hash algorithms such as MD5 and SHA-1 should not be used.
- Passwords should be stored with a password hashing function such as Argon2id, scrypt, bcrypt or PBKDF2, with the parameters from the [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), for example 600,000 iterations for PBKDF2-HMAC-SHA256. MD5 must not be used with PBKDF2, such as PBKDF2WithHmacMD5.

#### Minimum Key Lengths

```text
Key exchange: Diffie-Hellman key exchange with minimum 2048 bits
Message Integrity: HMAC-SHA2
Message Hash: SHA2 256 bits
Asymmetric encryption: RSA 2048 bits
Symmetric-key algorithm: AES 128 bits
Password Hashing: Argon2id, scrypt, bcrypt, PBKDF2
ECDH, ECDSA: 256 bits
Signatures: RSA-PSS 2048 bits, ECDSA P-256, Ed25519
```

### Source Code Review

- Search for the following keywords to identify use of weak algorithms: `MD4, MD5, RC4, RC2, DES, Blowfish, SHA-1, ECB`

- For Java implementations, the following API is related to encryption. Review the parameters of the encryption implementation. For example,

```java
SecretKeyFactory(SecretKeyFactorySpi keyFacSpi, Provider provider, String algorithm)
SecretKeySpec(byte[] key, int offset, int len, String algorithm)
Cipher c = Cipher.getInstance("DES/CBC/PKCS5Padding");
```

- For RSA encryption, the following padding modes are suggested.

```text
RSA/ECB/OAEPWithSHA-1AndMGF1Padding (2048)
RSA/ECB/OAEPWithSHA-256AndMGF1Padding (2048)
```

- Search for `ECB`, it's not allowed to be used in padding.
- Review if different IV (initial Vector) is used.

```java
// Use a different IV value for every encryption
byte[] newIv = ...;
s = new GCMParameterSpec(s.getTLen(), newIv);
cipher.init(..., s);
...
```

- Search for `IvParameterSpec`, check if the IV value is generated differently and randomly.

```java
 IvParameterSpec iv = new IvParameterSpec(randBytes);
 SecretKeySpec skey = new SecretKeySpec(key.getBytes(), "AES");
 Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
 cipher.init(Cipher.ENCRYPT_MODE, skey, iv);
```

- In Java, search for MessageDigest to check if weak hash algorithm (MD5 or CRC) is used. For example:

`MessageDigest md5 = MessageDigest.getInstance("MD5");`

- For signature, SHA1 and MD5 should not be used. For example:

`Signature sig = Signature.getInstance("SHA1withRSA");`

- Search for `Signature.getInstance` and check that received data is checked with `verify()`, not only signed with `sign()`, and that the result of `verify()` is acted on.

- Search for `PBKDF2`. To generate the hash value of password, `PBKDF2` is suggested to be used. Review the parameters to generate the `PBKDF2` has value.

The iterations should follow the [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) (600,000 for PBKDF2-HMAC-SHA256), and the **salt** value should be generated as **random value**.

```java
private static byte[] pbkdf2(char[] password, byte[] salt, int iterations, int bytes)
    throws NoSuchAlgorithmException, InvalidKeySpecException
  {
       PBEKeySpec spec = new PBEKeySpec(password, salt, iterations, bytes * 8);
       SecretKeyFactory skf = SecretKeyFactory.getInstance(PBKDF2_ALGORITHM);
       return skf.generateSecret(spec).getEncoded();
   }
```

- Hard-coded sensitive information:

```text
User related keywords: name, root, su, sudo, admin, superuser, login, username, uid
Key related keywords: public key, AK, SK, secret key, private key, passwd, password, pwd, share key, shared key, crypto, base64
Other common sensitive keywords: sysadmin, root, privilege, pass, key, code, master, admin, uname, session, token, Oauth, privatekey, shared secret
```

## Tools

- Vulnerability scanners such as Nessus, Nmap (scripts), or OpenVAS can scan for use or acceptance of weak encryption against protocol such as SNMP, TLS, SSH, SMTP, etc.
- Use static code analysis tool to do source code review such as klocwork, Fortify, Coverity, CheckMark for the following cases.

```text
CWE-261: Weak Cryptography for Passwords
CWE-323: Reusing a Nonce, Key Pair in Encryption
CWE-326: Inadequate Encryption Strength
CWE-327: Use of a Broken or Risky Cryptographic Algorithm
CWE-328: Reversible One-Way Hash
CWE-329: Not Using a Random IV with CBC Mode
CWE-330: Use of Insufficiently Random Values
CWE-347: Improper Verification of Cryptographic Signature
CWE-354: Improper Validation of Integrity Check Value
CWE-547: Use of Hard-coded, Security-relevant Constants
CWE-780: Use of RSA Algorithm without OAEP
```

## References

- [NIST FIPS Standards](https://csrc.nist.gov/publications/fips)
- [Wikipedia: Initialization Vector](https://en.wikipedia.org/wiki/Initialization_vector)
- [Secure Coding - Generating Strong Random Numbers](https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/rules/miscellaneous-msc/msc02-j)
- [Optimal Asymmetric Encryption Padding](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding)
- [Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Secure Coding - Do not use insecure or weak cryptographic algorithms](https://cmu-sei.github.io/secure-coding-standards/sei-cert-oracle-coding-standard-for-java/recommendations/miscellaneous-msc/msc61-j)
- [Insecure Randomness](https://owasp.org/www-community/vulnerabilities/Insecure_Randomness)
- [Insufficient Entropy](https://owasp.org/www-community/vulnerabilities/Insufficient_Entropy)
- [Insufficient Session-ID Length](https://owasp.org/www-community/vulnerabilities/Insufficient_Session-ID_Length)
- [Using a broken or risky cryptographic algorithm](https://owasp.org/www-community/vulnerabilities/Using_a_broken_or_risky_cryptographic_algorithm)
- [Javax.crypto.cipher API](https://docs.oracle.com/javase/8/docs/api/javax/crypto/Cipher.html)
- ISO 18033-1:2015 - Encryption Algorithms
- ISO 18033-2:2015 - Asymmetric Ciphers
- ISO 18033-3:2015 - Block Ciphers
