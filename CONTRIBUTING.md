# Contributing to the Testing Guide

The team thanks you for considering contributing to the project!

The guidelines mentioned below will help you to contribute in a manner to conform to the project's rules, which makes all contributions uniform, and allows the reviewing team to review in a faster manner. If you feel like what you are working on breaks a rule, and that rule needs to be broken as a necessity for that contribution, kindly use your best judgement. If you feel like this document can be improved in any manner, send us a pull request and it will be taken into consideration.

## How to Contribute

Other than what is discussed in the below sections, you can check out the Open Source Guide for [why and how to contribute](https://opensource.guide/how-to-contribute/).

### Issues in the Testing Guide

This section guides you through reporting issues in the existing project content. These issues can range from, and are not restricted to the below list:

- Grammar mistakes.
- Lacking enough details to achieve a full attack.
- Deprecated attack implementation that no longer works.

In order to report an issue:

Create an [issue](https://github.com/OWASP/OWASP-Testing-Guide-v5/issues) using the [fix request template](https://github.com/OWASP/OWASP-Testing-Guide-v5/issues/new?assignees=&labels=QA%2FEdit&template=fix-request.md&title=)

In order to fix an [issue](https://github.com/OWASP/OWASP-Testing-Guide-v5/issues), follow the guidance of [how to send a PR](#how-to-send-a-PR).

### Creating New Testing Scenarios

This section guides you through providing new content to the testing guide. New content can be:

- New methods to test against a certain weakness.
- New techniques or details to test against a newly discovered weakness.

In order to suggest a new scenario, follow the guidance of [how to send a PR](#how-to-send-a-PR).

### How to Send a PR

- Make sure that you have properly [setup your environment](#how-to-set-up-my-contributor-environment).
- Fork the repository by using the Fork button in our [repository](https://github.com/OWASP/OWASP-Testing-Guide-v5).
  - If you have a fork that is behind from master, make sure that you [sync your fork](https://help.github.com/en/articles/syncing-a-fork) first.

#### Create a New Branch

```bash
# Checkout the master branch to be sure that your new branch is coming from master
git checkout master

# Create a new branch such as OTG-96
git branch OTG-[issue number]

# Switch to your new branch
git checkout OTG-[issue number]
```

Now, you can go high and low with your commits and contributions.

#### Submit the New Branch

Once done, you should submit your work to the main repository.

```bash
# Push all your changes to your repository
git push origin
```

Now you can safely go and create a new pull request from your repository.

At the PR submission, take into account reviewer's comments.

To update your work based on the reviews, simply create new commits on the branch you created and push them to your repository.

Once accepted, your name will be added to the project authors.

### How to Set Up My Contributor Environment

1. [Join GitHub](https://github.com/join).
2. Install [Visual Studio Code](https://code.visualstudio.com/).
3. Install the following [markdown linter plugin](https://github.com/DavidAnson/vscode-markdownlint#install).
4. You can safely follow now [how to send a PR](#how-to-send-a-pr).

#### How to Run Local CI Tests

1. Go to the project folder in your terminal
2. Make sure you have installed [node](https://nodejs.org)
3. Install node modules
    `npm install`
4. Run test
    `npm test`
