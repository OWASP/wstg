# Testing for Padding Oracle

|ID          |
|------------|
|WSTG-CRYP-02|

## Summary

A padding oracle is a function of an application which decrypts encrypted data provided by the client, e.g. internal session state stored on the client, and leaks the state of the validity of the padding after decryption. The existence of a padding oracle allows an attacker to decrypt encrypted data and encrypt arbitrary data without knowledge of the key used for these cryptographic operations. This can lead to leakage of sensible data or to privilege escalation vulnerabilities, if integrity of the encrypted data is assumed by the application.

Block ciphers encrypt data only in blocks of certain sizes. Block sizes used by common ciphers are 8 and 16 bytes. Data where the size doesn't match a multiple of the block size of the used cipher has to be padded in a specific manner so the decryptor is able to strip the padding. A commonly used padding scheme is PKCS#7. It fills the remaining bytes with the value of the padding length.

### Example 1

If the padding has the length of 5 bytes, the byte value `0x05` is repeated five times after the plain text.

An error condition is present if the padding doesn't match the syntax of the used padding scheme. A padding oracle is present if an application leaks this specific padding error condition for encrypted data provided by the client. This can happen by exposing exceptions (e.g. `BadPaddingException` in Java) directly, by subtle differences in the responses sent to the client or by another side-channel like timing behavior.

Certain modes of operation of cryptography allow bit-flipping attacks, where flipping of a bit in the cipher text causes that the bit is also flipped in the plain text. Flipping a bit in the n-th block of CBC encrypted data causes that the same bit in the (n+1)-th block is flipped in the decrypted data. The n-th block of the decrypted cipher text is garbaged by this manipulation.

The padding oracle attack enables an attacker to decrypt encrypted data without knowledge of the encryption key and used cipher by sending skillful manipulated cipher texts to the padding oracle and observing of the results returned by it. This causes loss of confidentiality of the encrypted data. E.g. in the case of session data stored on the client-side the attacker can gain information about the internal state and structure of the application.

A padding oracle attack also enables an attacker to encrypt arbitrary plain texts without knowledge of the used key and cipher. If the application assumes that integrity and authenticity of the decrypted data is given, an attacker could be able to manipulate internal session state and possibly gain higher privileges.

## Test Objectives

- Identify encrypted messages that rely on padding.
- Attempt to break the padding of the encrypted messages and analyze the returned error messages for further analysis.

## How to Test

### Black-Box Testing

First the possible input points for padding oracles must be identified. Generally the following conditions must be met:

1. The data is encrypted. Good candidates are values which appear to be random.
2. A block cipher is used. The length of the decoded (Base64 is used often) cipher text is a multiple of common cipher block sizes like 8 or 16 bytes. Different cipher texts (e.g. gathered by different sessions or manipulation of session state) share a common divisor in the length.

#### Example 2

`Dg6W8OiWMIdVokIDH15T/A==` results after Base64 decoding in `0e 0e 96 f0 e8 96 30 87 55 a2 42 03 1f 5e 53 fc`. This seems to be random and 16 byte long.

If such an input value candidate is identified, the behavior of the application to bit-wise tampering of the encrypted value should be verified. Normally this Base64 encoded value will include the initialization vector (IV) prepended to the cipher text. Given a plaintext *`p`* and a cipher with a block size *`n`*, the number of blocks will be *`b = ceil( length(b) / n)`*. The length of the encrypted string will be *`y=(b+1)*n`* due to the initialization vector. To verify the presence of the oracle, decode the string, flip the last bit of the second-to-last block *`b-1`* (the least significant bit of the byte at *`y-n-1`*), re-encode and send. Next, decode the original string, flip the last bit of the block *`b-2`* (the least significant bit of the byte at *`y-2*n-1`*), re-encode and send.

If it is known that the encrypted string is a single block (the IV is stored on the server or the application is using a bad practice hardcoded IV), several bit flips must be performed in turn. An alternative approach could be to prepend a random block, and flip bits in order to make the last byte of the added block take all possible values (0 to 255).

The tests and the base value should at least cause three different states while and after decryption:

- Cipher text gets decrypted, resulting data is correct.
- Cipher text gets decrypted, resulting data is garbled and causes some exception or error handling in the application logic.
- Cipher text decryption fails due to padding errors.

Compare the responses carefully. Search especially for exceptions and messages which state that something is wrong with the padding. If such messages appear, the application contains a padding oracle. If the three different states described above are observable implicitly (different error messages, timing side-channels), there is a high probability that there is a padding oracle present at this point. Try to perform the padding oracle attack to ensure this.

##### Example 3

- ASP.NET throws `System.Security.Cryptography.CryptographicException: Padding is invalid and cannot be removed.` if padding of a decrypted cipher text is broken.
- In Java a `javax.crypto.BadPaddingException` is thrown in this case.
- Decryption errors or similar can be possible padding oracles.

> A secure implementation will check for integrity and cause only two responses: `ok` and `failed`. There are no side channels which can be used to determine internal error states.

### Gray-Box Testing

Verify that all places where encrypted data from the client, that should only be known by the server, is decrypted. The following conditions should be met by such code:

1. The integrity of the cipher text should be verified by a secure mechanism, like HMAC or authenticated cipher operation modes like GCM or CCM.
2. All error states while decryption and further processing are handled uniformly.

### Example 4

[Visualization of the decryption process](https://erlend.oftedal.no/blog/poet/)

## Tools

- [Bletchley](https://code.blindspotsecurity.com/trac/bletchley)
- [PadBuster](https://github.com/GDSSecurity/PadBuster)
- [Padding Oracle Exploitation Tool (POET)](http://netifera.com/research/)
- [Poracle](https://github.com/iagox86/Poracle)
- [python-paddingoracle](https://github.com/mwielgoszewski/python-paddingoracle)

## References

- [Wikepedia - Padding Oracle Attack](https://en.wikipedia.org/wiki/Padding_oracle_attack)
- [Juliano Rizzo, Thai Duong, "Practical Padding Oracle Attacks"](https://www.usenix.org/event/woot10/tech/full_papers/Rizzo.pdf)
