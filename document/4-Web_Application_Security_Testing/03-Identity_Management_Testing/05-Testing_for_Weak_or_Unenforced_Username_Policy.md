# Testing for Weak or Unenforced Username Policy

|ID          |
|------------|
|WSTG-IDNT-05|

## Summary

User account names are often highly structured (e.g. Joe Bloggs account name is jbloggs and Fred Nurks account name is fnurks) and valid account names can easily be guessed.

## Test Objectives

- Determine whether a consistent account name structure renders the application vulnerable to account enumeration.
- Determine whether the application's error messages permit account enumeration.

## How to Test

- Determine the structure of account names.
- Evaluate the application's response to valid and invalid account names.
- Use different responses to valid and invalid account names to enumerate valid account names.
- Use account name dictionaries to enumerate valid account names.

## Remediation

Ensure the application returns consistent generic error messages in response to invalid account name, password or other user credentials entered during the log in process.
