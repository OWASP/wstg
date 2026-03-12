# Pull Request: Enhance WSTG with Comprehensive API Security Testing Guidance

## 📋 Summary

This pull request extends the Web Security Testing Guide (WSTG) to comprehensively cover API security testing. The changes integrate API-specific testing guidance throughout existing test cases while leveraging the existing API Testing section for dedicated API tests.

**Related Issue:** [Link to issue if exists, otherwise suggest creating one]

## 🎯 Motivation

Modern web applications increasingly rely on APIs (REST, GraphQL, SOAP, gRPC) for their functionality. While the WSTG has traditionally focused on browser-based web application testing, security professionals need guidance on testing APIs that:

- May not have a browser-based interface
- Use different authentication mechanisms (API keys, OAuth, JWT, mTLS)
- Have unique vulnerability patterns (BOLA, mass assignment, excessive data exposure)
- Require different testing approaches and tools

This update ensures the WSTG remains relevant for contemporary web security testing by addressing these gaps.

## 🔄 Changes Overview

### Files Modified: 26 | Files Added: 3

| Section | Files Modified | Description |
|---------|---------------|-------------|
| Information Gathering | 4 | API endpoint discovery, architecture mapping |
| Identity Management | 3 | API role testing, registration, enumeration |
| Authentication Testing | 4 | API auth methods, rate limiting, default credentials |
| Authorization Testing | 3 | BOLA/IDOR, privilege escalation, authorization bypass |
| Session Management | 3 | Token-based auth, API cookies, CSRF considerations |
| Input Validation | 5 | SQL/NoSQL injection, XML injection, command injection, SSRF |
| Client-side Testing | 3 | API applicability notes for browser-specific tests |
| API Testing | 4 | New comprehensive API-specific tests |

## 📝 Detailed Changes

### 1. Information Gathering Section

**01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage.md**
- Added: API Endpoint and Documentation Discovery
- Covers: Swagger/OpenAPI discovery, Postman collections, GraphQL endpoints, exposed API keys

**10-Map_Application_Architecture.md**
- Added: API Architecture Components
- Covers: API gateways, versioning strategies, service discovery, BFF patterns

### 2. Identity Management Section

**01-Test_Role_Definitions.md**
- Added: API-Specific Role Testing
- Covers: OAuth scopes, JWT claims validation, API key permission levels, GraphQL authorization

**02-Test_User_Registration_Process.md**
- Added: API Registration Testing
- Covers: Registration endpoints, token issuance, API key provisioning, mass assignment during registration

**04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md**
- Added: API-Specific Enumeration Techniques
- Covers: Response structure analysis, rate limiting differences, GraphQL enumeration, timing attacks

### 3. Authentication Testing Section

**02-Testing_for_Default_Credentials.md**
- Added: API Default Credentials
- Covers: API keys, service accounts, cloud provider defaults, GraphQL/gateway defaults

**03-Testing_for_Weak_Lock_Out_Mechanism.md**
- Added: API Rate Limiting and Throttling
- Covers: Rate limit testing, bypass techniques, per-endpoint limits

**07-Testing_for_Weak_Authentication_Methods.md**
- Added: API Authentication Methods
- Covers: API keys, OAuth 2.0/OIDC, JWT vulnerabilities, mTLS, Basic/Digest auth

### 4. Authorization Testing Section

**03-Testing_for_Privilege_Escalation.md**
- Added: API Privilege Escalation
- Covers: Token claim manipulation, OAuth scope escalation, GraphQL privilege issues

**04-Testing_for_Insecure_Direct_Object_References.md**
- Added: API-Specific IDOR Testing (BOLA)
- Covers: REST API IDOR patterns, GraphQL IDOR, nested object references

### 5. Session Management Section

**01-Testing_for_Session_Management_Schema.md**
- Added: API Session Management
- Covers: Token-based vs session-based authentication comparison, stateless auth testing

**02-Testing_for_Cookies_Attributes.md**
- Added: API Considerations
- Covers: When APIs use cookies, when they don't, alternative mechanisms

**05-Testing_for_Cross_Site_Request_Forgery.md**
- Added: API CSRF Considerations
- Covers: When APIs are vulnerable to CSRF, protection mechanisms for APIs

### 6. Input Validation Section

**05.6-Testing_for_NoSQL_Injection.md**
- Added: API-Specific NoSQL Injection Testing
- Covers: JSON body injection, operator-based attacks, GraphQL NoSQL injection

**07-Testing_for_XML_Injection.md**
- Added: API-Specific XML Injection Testing
- Covers: SOAP APIs, REST with XML, XML-RPC, XXE/SSRF via APIs

**12-Testing_for_Command_Injection.md**
- Added: API-Specific Command Injection
- Covers: JSON parameters, headers, webhooks, file processing, container/cloud context

### 7. Client-side Testing Section

**01-Testing_for_DOM-based_Cross_Site_Scripting.md**
- Added: API non-applicability note (browser-specific test)

**09-Testing_for_Clickjacking.md**
- Added: API non-applicability note (browser-specific test)

### 8. API Testing Section (New Tests)

**03-Testing_for_Broken_Function_Level_Authorization.md** (NEW)
- Comprehensive guide for testing function-level authorization in APIs

**04-Testing_for_Excessive_Data_Exposure.md** (NEW)
- Testing for APIs that expose more data than necessary

**05-Testing_for_Lack_of_Resources_and_Rate_Limiting.md** (NEW)
- Testing for resource consumption and rate limiting issues

## ✅ Checklist

- [x] All changes follow the [WSTG style guide](style_guide.md)
- [x] All changes follow the [article template](template)
- [x] Content uses American English spelling
- [x] Active voice used throughout
- [x] Second person perspective maintained
- [x] Code snippets are correct and well-commented
- [x] Inline links provided for relevant references
- [x] Content suitable for audience with basic technical background
- [x] No bold/italic/underline used for emphasis
- [x] Proper formatting for lists and headings

## 🔗 Cross-References Added

The changes include cross-references between:
- Traditional test cases and their API-specific sections
- The dedicated API Testing section (12-API_Testing)
- OWASP API Security Top 10 vulnerabilities

## 🧪 Testing

- [x] All modified files render correctly in Markdown
- [x] Internal links verified
- [x] Code examples tested for accuracy
- [x] No duplicate content introduced

## 📚 References

- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## 👥 Reviewers

Requesting review from maintainers with expertise in:
- API security testing
- REST/GraphQL/SOAP API vulnerabilities
- OAuth/JWT security
- WSTG content and structure

## 💬 Additional Notes

1. **Backward Compatibility**: These changes enhance existing content without removing or contradicting current guidance.

2. **Scope Considerations**: Rather than creating an entirely separate API testing guide, this approach integrates API testing into the existing WSTG structure, making it easier for testers to understand when and how API testing differs from traditional web testing.

3. **Future Work**: The following areas could benefit from additional API-specific content in future updates:
   - Mass Assignment testing expansion
   - API Security Misconfigurations
   - Server-Side Request Forgery in APIs
   - API-specific tool recommendations

---

Thank you for reviewing this contribution. I'm happy to address any feedback or make adjustments as needed.
