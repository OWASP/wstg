# Testing for Weak Security Question Answer

|ID          |
|------------|
|WSTG-ATHN-08|

## Summary

Often called "secret" questions and answers, security questions and answers are often used to recover forgotten passwords (see [Testing for weak password change or reset functionalities](09-Testing_for_Weak_Password_Change_or_Reset_Functionalities.md), or as extra security on top of the password.

They are typically generated upon account creation and require the user to select from some pre-generated questions and supply an appropriate answer. They may allow the user to generate their own question and answer pairs. Both methods are prone to insecurities.Ideally, security questions should generate answers that are only known by the user, and not guessable or discoverable by anybody else. This is harder than it sounds.
Security questions and answers rely on the secrecy of the answer. Questions and answers should be chosen so that the answers are only known by the account holder. However, although a lot of answers may not be publicly known, most of the questions that websites implement promote answers that are pseudo-private.

### Pre-generated Questions

The majority of pre-generated questions are fairly simplistic in nature and can lead to insecure answers. For example:

- The answers may be known to family members or close friends of the user, e.g. "What is your mother's maiden name?", "What is your date of birth?"
- The answers may be easily guessable, e.g. "What is your favorite color?", "What is your favorite baseball team?"
- The answers may be brute forcible, e.g. "What is the first name of your favorite high school teacher?" - the answer is probably on some easily downloadable lists of popular first names, and therefore a simple brute force attack can be scripted.
- The answers may be publicly discoverable, e.g. "What is your favorite movie?" - the answer may easily be found on the user's social media profile page.

### Self-generated Questions

The problem with having users to generate their own questions is that it allows them to generate very insecure questions, or even bypass the whole point of having a security question in the first place. Here are some real world examples that illustrate this point:

- "What is 1+1?"
- "What is your username?"
- "My password is S3curIty!"

## Test Objectives

- Determine the complexity and how straight-forward the questions are.
- Assess possible user answers and brute force capabilities.

## How to Test

### Testing for Weak Pre-generated Questions

Try to obtain a list of security questions by creating a new account or by following the "I don’t remember my password"-process. Try to generate as many questions as possible to get a good idea of the type of security questions that are asked. If any of the security questions fall in the categories described above, they are vulnerable to being attacked (guessed, brute-forced, available on social media, etc.).

### Testing for Weak Self-Generated Questions

Try to create security questions by creating a new account or by configuring your existing account’s password recovery properties. If the system allows the user to generate their own security questions, it is vulnerable to having insecure questions created. If the system uses the self-generated security questions during the forgotten password functionality and if usernames can be enumerated (see [Testing for Account Enumeration and Guessable User Account](../03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account.md), then it should be easy for the tester to enumerate a number of self-generated questions. It should be expected to find several weak self-generated questions using this method.

### Testing for Brute-forcible Answers

Use the methods described in [Testing for Weak lock out mechanism](03-Testing_for_Weak_Lock_Out_Mechanism.md) to determine if a number of incorrectly supplied security answers trigger a lockout mechanism.

The first thing to take into consideration when trying to exploit security questions is the number of questions that need to be answered. The majority of applications only need the user to answer a single question, whereas some critical applications may require the user to answer two or even more questions.

The next step is to assess the strength of the security questions. Could the answers be obtained by a simple Google search or with social engineering attack? As a penetration tester, here is a step-by-step walkthrough of exploiting a security question scheme:

- Does the application allow the end user to choose the question that needs to be answered? If so, focus on questions which have:

    - A "public" answer; for example, something that could be find with a simple search-engine query.
    - A factual answer such as a "first school" or other facts which can be looked up.
    - Few possible answers, such as "what model was your first car". These questions would present the attacker with a short list of possible answers, and based on statistics the attacker could rank answers from most to least likely.

- Determine how many guesses you have if possible.
    - Does the password reset allow unlimited attempts?
    - Is there a lockout period after X incorrect answers? Keep in mind that a lockout system can be a security problem in itself, as it can be exploited by an attacker to launch a Denial of Service against legitimate users.
    - Pick the appropriate question based on analysis from the above points, and do research to determine the most likely answers.

The key to successfully exploiting and bypassing a weak security question scheme is to find a question or set of questions which give the possibility of easily finding the answers. Always look for questions which can give you the greatest statistical chance of guessing the correct answer, if you are completely unsure of any of the answers. In the end, a security question scheme is only as strong as the weakest question.

## References

- [The Curse of the Secret Question](https://www.schneier.com/essay-081.html)
- [The OWASP Security Questions Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Choosing_and_Using_Security_Questions_Cheat_Sheet.html)
