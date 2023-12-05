# OWASP Web Security Testing Guide

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/OWASP/wstg/issues)
[![OWASP Flagship](https://img.shields.io/badge/owasp-flagship-brightgreen.svg)](https://owasp.org/projects/)
[![Twitter Follow](https://img.shields.io/twitter/follow/owasp_wstg?style=social)](https://twitter.com/owasp_wstg)

[![Creative Commons License](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-sa/4.0/ "CC BY-SA 4.0")

Welcome to the official repository for the Open Web Application Security Project® (OWASP®) Web Security Testing Guide (WSTG). The WSTG is a comprehensive guide to testing the security of web applications and web services. Created by the collaborative efforts of security professionals and dedicated volunteers, the WSTG provides a framework of best practices used by penetration testers and organizations all over the world.

We are currently working on release version 5.0. You can [read the current document here on GitHub](https://github.com/OWASP/wstg/tree/master/document).

For the last stable release, [check release 4.2](https://github.com/OWASP/wstg/releases/tag/v4.2). Also available [online](https://owasp.org/www-project-web-security-testing-guide/v42/).

- [How To Reference WSTG Scenarios](#how-to-reference-wstg-scenarios)
    - [Linking](#linking)
- [Contributions, Feature Requests, and Feedback](#contributions-feature-requests-and-feedback)
- [Chat With Us](#chat-with-us)
- [Project Leaders](#project-leaders)
- [Core Team](#core-team)
- [Translations](#translations)

## How To Reference WSTG Scenarios

Each scenario has an identifier in the format `WSTG-<category>-<number>`, where: 'category' is a 4 character upper case string that identifies the type of test or weakness, and 'number' is a zero-padded numeric value from 01 to 99. For example:`WSTG-INFO-02` is the second Information Gathering test.

The identifiers may change between versions. Therefore, it is preferable that other documents, reports, or tools use the format: `WSTG-<version>-<category>-<number>`, where: 'version' is the version tag with punctuation removed. For example: `WSTG-v42-INFO-02` would be understood to mean specifically the second Information Gathering test from version 4.2.

If identifiers are used without including the `<version>` element, they should be assumed to refer to the latest Web Security Testing Guide content. As the guide grows and changes this becomes problematic, which is why writers or developers should include the version element.

### Linking

Linking to Web Security Testing Guide scenarios should be done using versioned links not `stable` or `latest`, which will change with time. However, it is the project team's intention that versioned links do not change. For example: `https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server.html`. Note: the `v42` element refers to version 4.2.

## Contributions, Feature Requests, and Feedback

We are actively inviting new contributors! To start, read the [contribution guide](CONTRIBUTING.md).

First time here? Here are [GitHub's suggestions for first-time contributors](https://github.com/OWASP/wstg/contribute) to this repository.

This project is only possible thanks to the work of many dedicated volunteers. Everyone is encouraged to help in ways large and small. Here are a few ways you can help:

- Read the current content and help us fix any spelling mistakes or grammatical errors.
- Help with [translation](CONTRIBUTING.md#translation) efforts.
- Choose an existing issue and submit a pull request to fix it.
- Open a new issue to report an opportunity for improvement.

To learn how to contribute successfully, read the [contribution guide](CONTRIBUTING.md).

Successful contributors appear on [the project's list of authors, reviewers, or editors](document/1-Frontispiece/README.md).

## Chat With Us

We're easy to find on Slack:

1. Join the OWASP Group Slack with this [invitation link](https://owasp.org/slack/invite).
2. Join this project's [channel, #testing-guide](https://app.slack.com/client/T04T40NHX/CJ2QDHLRJ).

Feel free to ask questions, suggest ideas, or share your best recipes.

You can @ us on Twitter [@owasp_wstg](https://twitter.com/owasp_wstg).

You can also join our [Google Group](https://groups.google.com/a/owasp.org/forum/#!forum/testing-guide-project).

## Project Leaders

- [Rick Mitchell](https://github.com/kingthorin)
- [Elie Saad](https://github.com/ThunderSon)

## Core Team

- [Rejah Rehim](https://github.com/rejahrehim)
- [Victoria Drake](https://github.com/victoriadrake)

## Translations

- [Portuguese-BR](https://github.com/doverh/wstg-translations-pt)
- [Russian](https://github.com/andrettv/WSTG/tree/master/WSTG-ru)
- [French](https://github.com/clallier94/wstg-translation-fr)
- [Persian (Farsi)](https://github.com/whoismh11/owasp-wstg-fa)

---

Open Web Application Security Project and OWASP are registered trademarks of the OWASP Foundation, Inc.
