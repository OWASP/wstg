# SAML Authentication

|ID          |
|------------|
|WSTG-ATHN-12|

## Summary

Security Assertion Markup Language (SAML) 2.0 is an XML-based standard for single sign-on (SSO). A user signs in at an identity provider (IdP), which sends a signed statement about the user, called an assertion, to the application, called the service provider (SP). The SP trusts the assertion and starts a session for the user.

Two flows are common:

- **SP-initiated:** the user visits the SP, which sends an authentication request (`AuthnRequest`) to the IdP and receives a `SAMLResponse` in return.
- **IdP-initiated:** the user starts at the IdP, which sends a `SAMLResponse` to the SP without a prior request.

In the usual HTTP POST binding, the browser carries the `SAMLResponse` to the SP's Assertion Consumer Service (ACS) endpoint as a base64-encoded form field. Because the browser (and so the user, or an attacker) handles the message, the SP must verify everything it relies on. The most common failures are in signature validation and in how the SP reads the XML after validating it.

This page covers what is specific to SAML. For XML parsing flaws such as XML external entities, see [XML Injection](../07-Injection/07-XML_Injection.md). For session handling after login, see [Session Management](../06-Session_Management/README.md).

## Test Objectives

- Identify the SAML flow in use and the endpoints involved.
- Determine whether the SP validates the signature, and that the signature covers the data the SP uses.
- Determine whether the SP enforces the conditions in the assertion (audience, validity period, recipient, and request binding).
- Assess whether assertions can be replayed or accepted from an untrusted source.

## How to Test

### Identify the SAML Flow

Use an intercepting proxy to follow a login. Look for:

- A redirect to the IdP carrying a `SAMLRequest` parameter (SP-initiated).
- A POST to an endpoint such as `/saml/acs`, `/saml2/consume` or `/Shibboleth.sso/SAML2/POST` containing `SAMLResponse` and sometimes `RelayState`.
- The SP and IdP metadata, often published at paths such as `/saml/metadata`, which list the entity IDs, endpoints and certificates.

Decode the `SAMLResponse` value: URL-decode and base64-decode it to get the XML. A `SAMLRequest` or a logout message sent with the HTTP Redirect binding is also deflate-compressed. Browser extensions such as SAML-tracer, and the SAML Raider extension for [Burp Suite](https://portswigger.net/burp), make the decoded message and its signatures easy to edit and resend.

In the XML, note the `Issuer`, the `Subject`/`NameID`, the `Conditions` (`NotBefore`, `NotOnOrAfter`, `AudienceRestriction`), the `SubjectConfirmationData` (`Recipient`, `InResponseTo`, `NotOnOrAfter`), the attributes, and which elements carry a `Signature`. The `Response` and the `Assertion` can each be signed separately.

### Test Signature Validation

Resend the login with a modified `SAMLResponse`, using an account you are allowed to test with. The SP should reject each of these:

- The `Signature` elements removed.
- The signed values changed (for example the `NameID` or an attribute) while the signature is left as it was.
- The message re-signed with a different key, such as a self-signed certificate. SAML Raider can clone a certificate for this.
- A signature that is valid, but that covers only the `Response` while the SP reads data from an unsigned `Assertion`, or the reverse.
- A plain `Assertion` in place of the `EncryptedAssertion`, if the SP is configured to receive encrypted assertions. Some SPs decrypt when they find an encrypted assertion but also accept an unencrypted one.
- A `Transform` in the signature that uses XSLT. Some XML signature libraries run the transforms before they check the signature, so an XSLT that makes a network request to a server you control shows that the SP processes it, even when the signature is later rejected.

If a modified response is accepted, the SP does not verify signatures, or does not verify them against the IdP's key.

### Test for XML Signature Wrapping

In a signature wrapping attack, the attacker keeps a validly signed element but moves it so the signature still verifies, and adds a second, unsigned element that the SP's business logic reads in place of the signed one.

- Copy the signed `Assertion` into another location in the document (for example inside an `Extensions` element or after the original assertion), and place a modified assertion where the SP would normally look.
- Check whether the SP reads the identity from the same element whose signature it verified.

Because a signature check passes, such a response is accepted by a vulnerable SP. This often depends on the XML library and how the SP selects elements (by position, or by `ID` reference), so try several placements.

A related flaw is a parser differential, where the SP uses one XML parser to verify the signature and another to read the assertion. Markup that the two parsers interpret differently, such as unusual namespace declarations, comments, entities or duplicate elements, can make the verifier and the reader see different documents. In 2025 this allowed an authentication bypass in the `ruby-saml` library. If the SP's technology is known, check whether its SAML library has had such issues and whether the version in use is patched.

### Test NameID and Attribute Handling

- **Comment injection:** some parsers return only the text node after a comment. A `NameID` of `user@example.com<!---->.attacker.com` may be validated as one value and processed as another. Test with the value of an account you control, and check which identity the SP creates.
- Check how the SP maps `NameID` or attributes to local accounts. If it matches by email address or username only, an attacker who controls an account at the IdP, or at an IdP the SP trusts, may be able to claim another user's identity.
- Check whether attributes that decide roles or groups are accepted from the assertion without limits.

### Test Assertion Conditions

Change or replay the assertion, using the cases the SP should reject:

- **Audience:** an assertion issued for a different SP (a different `Audience` value) is accepted.
- **Validity period:** an assertion used after `NotOnOrAfter`, or before `NotBefore`, is accepted. Allow for a small clock skew.
- **Recipient:** `SubjectConfirmationData` `Recipient` is not compared to the ACS URL.
- **Replay:** the same assertion (`ID`) is accepted more than once, including after logout.
- **InResponseTo:** in an SP-initiated flow, a response that does not answer a request this SP made is accepted.
- **Issuer:** a response from an issuer other than the configured IdP is accepted.

### Test IdP-Initiated and RelayState Handling

- If the SP accepts unsolicited responses (IdP-initiated SSO), note it. It is valid, but it removes the `InResponseTo` check and makes login cross-site request forgery easier. See [Cross Site Request Forgery](../06-Session_Management/05-Cross_Site_Request_Forgery.md).
- `RelayState` is often used to return the user to a page after login. Check for open redirects by changing it to an external URL. See [Client-side URL Redirect](../11-Client-side/04-Client-side_URL_Redirect.md).

### Test Logout

If single logout is implemented, check that logging out at the SP ends the SP session and that a `LogoutRequest` is signed and verified. Check that an old session cannot be used after logout.

## Remediation

- Validate the signature on every message and assertion the SP uses, against the IdP's configured certificate, and use only the data that the signature covers.
- Use a maintained SAML library, keep it updated, and configure it to reject unsigned assertions.
- Enforce `Audience`, `Recipient`, `Issuer`, `NotBefore` and `NotOnOrAfter`, and for SP-initiated flows check `InResponseTo`.
- Record assertion IDs until they expire and reject repeats.
- Disable DTDs and external entities in the XML parser.
- Read the assertion from the same parsed document that was used to verify the signature, and reject signatures that use XSLT transforms.
- Map users using a stable, unique identifier, and do not let external attributes grant privileges that the application should control.
- Allow only expected values for `RelayState`.

## Tools

- [SAML Raider](https://github.com/CompassSecurity/SAMLRaider) (Burp Suite extension)
- [Burp Suite](https://portswigger.net/burp)
- Browser extensions that decode SAML messages, such as SAML-tracer
- [ZAP](https://www.zaproxy.org/) with a SAML add-on

## References

- [OASIS: Security Assertion Markup Language (SAML) V2.0 Technical Overview](https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html)
- [OASIS: SAML 2.0 Core Specification](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf)
- [OWASP: SAML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html)
- [On Breaking SAML: Be Whoever You Want to Be (Somorovsky et al., USENIX Security 2012)](https://www.usenix.org/system/files/conference/usenixsecurity12/sec12-final91.pdf)
- [GitHub Security Lab: Sign in as anyone: Bypassing SAML SSO authentication with parser differentials](https://github.blog/security/sign-in-as-anyone-bypassing-saml-sso-authentication-with-parser-differentials/)
