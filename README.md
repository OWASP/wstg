# OWASP WSTG Interactive Checklist App

🚀 **[Access the Live Checklist App Here!](https://laurinengelen.github.io/OWASP-WSTG-Checklisten-App/)**

Welcome to the **OWASP WSTG Interactive Checklist App**! This repository contains an offline-capable, interactive companion app for the OWASP Web Security Testing Guide (WSTG).

## About the Checklist App

The `wstg_checklist_app` folder contains a client-side web application that allows you to:
- Track your progress during a penetration test based on the WSTG modules.
- Read summaries, test objectives, methodologies, and tools directly within the app.
- Add custom finding titles and notes.
- Export and import your current testing state as a JSON file.
- Generate a SysReptor report/project from the selected SysReptor findings.

### How to Use

**Online Version:**
Simply visit the live hosted application at [https://laurinengelen.github.io/OWASP-WSTG-Checklisten-App/](https://laurinengelen.github.io/OWASP-WSTG-Checklisten-App/).

**Offline Version:**
Alternatively, you can open the `wstg_checklist_app/index.html` file in any modern web browser locally. It runs entirely client-side, meaning no data is sent to any servers, making it safe for confidential assessments.

**Local SysReptor Report Generation:**
The SysReptor report button requires the local JavaScript server so the API token remains outside the browser.

1. Create or edit `.env` in the repository root:

```env
SYSREPTOR_URL=https://sysreptor.example.com
SYSREPTOR_TOKEN=replace-with-api-token
SYSREPTOR_PROJECT_DESIGN=replace-with-project-design-id
```

2. Start the local server:

```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000), select SysReptor findings, then use **Generate SysReptor Report**.

Set `SYSREPTOR_PROJECT_ID` in `.env` to populate an existing report/project instead of creating a new one.
Selected checklist findings are matched against current SysReptor finding templates tagged `web` by template title. Keep the checklist finding title equal to the SysReptor template title for automatic template import.
If a selected finding has no matching template title, it is written to `sysreptor_missing_templates.md` and imported as a TODO fallback finding.
If SysReptor rejects a matched template ID, the server retries without a forced language and then creates a TODO fallback finding by default.

### How it Works
The checklist data is generated from the official OWASP WSTG markdown files. The python script `wstg_checklist_app/extract_wstg.py` parses the markdown documentation and compiles it into a static JavaScript file (`wstg_checklist_data.js`) used by the app.

---

# Original OWASP Web Security Testing Guide

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/OWASP/wstg/issues)
[![OWASP Flagship](https://img.shields.io/badge/owasp-flagship-brightgreen.svg)](https://owasp.org/projects/)
[![Twitter Follow](https://img.shields.io/twitter/follow/owasp_wstg?style=social)](https://x.com/owasp_wstg)

[![Creative Commons License](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-sa/4.0/ "CC BY-SA 4.0")

Welcome to the official repository for the Open Worldwide Application Security Project® (OWASP®) Web Security Testing Guide (WSTG). The WSTG is a comprehensive guide to testing the security of web applications and web services. Created by the collaborative efforts of security professionals and dedicated volunteers, the WSTG provides a framework of best practices used by penetration testers and organizations all over the world.

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

You can @ us on 𝕏 (Twitter) [@owasp_wstg](https://x.com/owasp_wstg).

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
- [Persian (Farsi)](https://github.com/whoismh11/owasp-wstg-fa)
- [Turkish](https://github.com/enoskom/Owasp-wstg)
- [Spanish](https://github.com/frangelbarrera/wstg)

---

Open Worldwide Application Security Project and OWASP are registered trademarks of the OWASP Foundation, Inc.
