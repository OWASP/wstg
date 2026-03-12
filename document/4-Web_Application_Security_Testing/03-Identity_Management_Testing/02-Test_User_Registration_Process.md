# Test User Registration Process

|ID          |
|------------|
|WSTG-IDNT-02|

## Summary

Some websites offer a user registration process that automates (or semi-automates) the provisioning of system access to users. The identity requirements for access vary from positive identification to none at all, depending on the security requirements of the system. Many public applications completely automate the registration and provisioning process because the size of the user base makes it impossible to manage manually. However, many corporate applications will provision users manually, so this test case may not apply.

## Test Objectives

- Verify that the identity requirements for user registration are aligned with business and security requirements.
- Validate the registration process.

## How to Test

Verify that the identity requirements for user registration are aligned with business and security requirements:

1. Can anyone register for access?
2. Are registrations vetted by a human prior to provisioning, or are they automatically granted if the criteria are met?
3. Can the same person or identity register multiple times?
4. Can users register for different roles or permissions?
5. What proof of identity is required for a registration to be successful?
6. Are registered identities verified?

Validate the registration process:

1. Can identity information be easily forged or faked?
2. Can the exchange of identity information be manipulated during registration?

### Example

In the WordPress example below, the only identification requirement is an email address that is accessible to the registrant.

![WordPress Registration Page](images/Wordpress_registration_page.jpg)\
*Figure 4.3.2-1: WordPress Registration Page*

In contrast, in the Google example below the identification requirements include name, date of birth, country, mobile phone number, email address and CAPTCHA response. While only two of these can be verified (email address and mobile number), the identification requirements are stricter than WordPress.

![Google Registration Page](images/Google_registration_page.jpg)\
*Figure 4.3.2-2: Google Registration Page*

### API Registration Testing

When testing API registration endpoints, additional considerations apply:

#### API Registration Endpoints

APIs typically expose registration via dedicated endpoints:

- `POST /api/register`
- `POST /api/v1/users`
- `POST /api/auth/signup`

Test these endpoints for:

1. Can registration requests be submitted without CAPTCHA or rate limiting?
2. Does the API accept additional fields beyond those documented (mass assignment)?
3. Can privileged role values be injected during registration (`"role": "admin"`)?
4. Does the response leak sensitive information about existing users?

#### Token Issuance During Registration

For APIs that issue tokens upon registration:

1. Is the token granted before email verification is complete?
2. Does the token have full access or limited scope for unverified accounts?
3. Are refresh tokens issued immediately, potentially allowing persistent access?
4. Can tokens be obtained by replaying registration requests?

#### API Key Provisioning

For APIs that issue API keys:

1. Are API keys generated with sufficient entropy?
2. Is there a limit on how many API keys a user can create?
3. Are API key permissions properly scoped based on registration type?
4. Can API keys be enumerated through timing attacks on the registration response?

## Remediation

Implement identification and verification requirements that correspond to the security requirements of the information the credentials protect.

## Tools

A HTTP proxy can be a useful tool to test this control.

## References

[User Registration Design](https://mashable.com/2011/06/09/user-registration-design/)
