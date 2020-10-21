# Testing for Improper Error Handling

|ID          |
|------------|
|WSTG-ERRH-01|

## Summary

All types of applications (web apps, web servers, databases, etc.) will generate errors for various reasons. A lot of the times, developers ignore handling these errors, or push away the idea that a user will ever try to push an error out (*e.g.* sending a string where an integer is expected). When the developer only consider the happy path, they forget all other possible user-input the code can receive but can't handle.

Errors sometimes rise as:

- stack traces,
- network timeouts,
- input mismatch,
- and memory dumps.

Most applications present them with error codes (and these codes can be understood from documentation), and they are shown usually as exceptions.

## Test Objectives

- Identify existent error codes.
- Analyse the different codes returned.
