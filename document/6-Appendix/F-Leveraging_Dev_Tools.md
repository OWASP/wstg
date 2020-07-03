# Leveraging Dev Tools

This appendix outlines various details for use of in browser Developer Tool functionality to aid in security testing activities.

Obviously in browser functionality is not a substitute for: DAST (Dynamic Application Security Testing) tools, SAST (Static Application Security Testing) tools, or a tester's experience, however, it can be leveraged for some testing activities and report production related tasks.

## Accessing Dev Tools

Opening Dev Tools can be accomplished in a number of ways.

1. Via the keyboard shortcut `F12`.
2. Via the keyboard shortcut `ctrl` + `shift` + `i` on Windows.
3. Via the keyboard short cut `cmd` + `option` + `i` on Mac.
4. Via the web page right click context menu and then selecting `Inspect` in Google Chrome.
5. Via the web page right click context menu and then selecting `Inspect Element` in Mozilla Firefox.
6. Via the triple dot 'kabob' menu in Google Chrome then selecting `More Tools` and then `Developer Tools`.
7. Via the triple line 'hamburger' (or 'pancake') menu in Mozilla Firefox then selecting `Web Developer` and then `Toggle Tools`.
8. Via the gear icon settings menu in Edge/IE then selecting `Developer Tools`.

## Capabilities

| Functionality         | Firefox | Chrome | Edge/IE | Safari |
|-----------------------|:-------:|:------:|:-------:|:------:|
| User Agent Switching  | Y       | Y      | Y       | Y      |
| Edit/Resend Requests  | N       | Y      | N       | N      |
| Cookie Editing        | Y       | Y      | Y       | N      |
| Local Storage Editing | Y       | Y      | Y       | N      |
| Disable CSS           | Y       | Y      | Y       | Y      |
| Disable JavaScript    | Y       | Y      | N       | Y      |
| View HTTP Headers     | Y       | Y      | Y       | Y      |
| Screenshots           | Y       | Y      | Y       | N      |
| Offline Mode          | Y       | Y      | N       | N      |
| Encoding and Decoding | Y       | Y      | Y       | Y      |

## User Agent Switching

## Edit/Resend Requests

## Cookie Editing

## Local Storage Editing

## Disable CSS

## Disable JavaScript

## View HTTP Headers

## Screenshots

## Offline Mode

## Encoding and Decoding

## Credit

This appendix was suggested by [Abhi-M](https://github.com/Abhi-M) and was assembled based on details from: [Web App Security Testing with Browsers](https://getmantra.com/web-app-security-testing-with-browsers/)
