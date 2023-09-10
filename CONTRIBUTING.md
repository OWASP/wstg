# Contributing to the Testing Guide

Thank you for considering contributing to the Web Security Testing Guide (WSTG)!

Here are some ways you can make a helpful contribution. The [Open Source Guide for why and how to contribute](https://opensource.guide/how-to-contribute/) is also a good resource. You will need a [GitHub account](https://help.github.com/en/github/getting-started-with-github/signing-up-for-a-new-github-account) in order to help out.

- [Become an Author](#become-an-author)
- [Become a Reviewer or Editor](#become-a-reviewer-or-editor)
    - [Technical Review](#technical-review)
    - [Editorial Review](#editorial-review)
- [How to Open an Issue](#how-to-open-an-issue)
- [How to Submit a Pull Request](#how-to-submit-a-pull-request)
- [How to Set Up Your Contributor Environment](#how-to-set-up-your-contributor-environment)
- [Contributing with Codespaces](#contributing-with-codespaces)

## Become an Author

This project would not be possible without the contributions of writers in the security community! Our authors help to keep the WSTG relevant and useful for everyone.

Whether you are submitting a new section or adding information to an existing one, please follow the [template example](template/999-Foo_Testing/1-Testing_for_a_Cat_in_a_Box.md). The [template sections are explained here](template/999-Foo_Testing/2-Template_Explanation.md).

When submitting your [pull request](#how-to-submit-a-pull-request), authors should link contributions to an issue:

1. Open an [Add New Content issue](https://github.com/OWASP/wstg/issues/new?assignees=&labels=New&template=new-content.md&title=), or choose an [unassigned new content issue](https://github.com/OWASP/wstg/issues?q=is%3Aopen+is%3Aissue+label%3ANew+no%3Aassignee) and ask to be assigned to it.
2. Create and switch to a new local branch with the name `new-<issue number>`. For example, `git checkout -b new-164`.

## Become a Reviewer or Editor

Keeping the project up to date and looking spiffy is a group effort! The WSTG is a constantly updated document and benefits from your technical or editorial review.

When submitting your [pull request](#how-to-submit-a-pull-request), reviewers and editors should link contributions to an issue:

1. Choose an [open issue with the `help wanted` label](https://github.com/OWASP/wstg/labels/help%20wanted) to work on, or [open an issue](https://github.com/OWASP/wstg/issues/new/choose) yourself. Post a comment in the issue and request to be assigned to it.
2. Create and switch to a new local branch with the name `fix-<issue number>`. For example, `git checkout -b fix-88`.

### Technical Review

If you have expertise in any topic covered by the WSTG, your technical review is encouraged. Please ensure that articles:

- Follow the [article template materials](template)
- Follow the [style guide](style_guide.md)
- Accurately describe vulnerabilities and tests
- Have appropriate and up-to-date inline links to resources
- Provide complete and relevant information suitable for an audience with basic technical expertise

### Editorial Review

Grammarians assemble! The WSTG welcomes your improvements in the areas of grammar, formatting, word choice, and brevity. All changes should adhere to the [style guide](style_guide.md).

Please don't hesitate to make as many changes as you see fit, especially if you notice that existing content does not match the [article template materials](template).

### Translation

Due to challenges with syncing images and removed content, the WSTG is no longer tackling in-bound translation efforts directly.

At this time we suggest that you start another repository in which to tackle translations of a specific language. Once you've produced a PDF for a given version of the guide we'll be happy to attach it to the appropriate release. Simply [open an issue](https://github.com/OWASP/wstg/issues/new) here asking us to do so.

Also we're willing to list your translation repository, just [let us know](https://github.com/OWASP/wstg/issues/new) where it is.

## How to Open an Issue

[Create an issue](https://github.com/OWASP/wstg/issues/new/choose) using the appropriate template.

Choose a short, descriptive title. Briefly explain what you think needs changing. Among other things, your suggestions may include grammar or spelling errors, or address insufficient or outdated content.

## How to Submit a Pull Request

Here are the steps for creating and submitting a Pull Request (PR) that we can quickly review and merge.

1. [Set up your environment](#how-to-set-up-your-contributor-environment) to fork the project and install a Markdown linter.
2. Associate your contribution with an [issue](https://github.com/OWASP/wstg/issues). To change existing content, read [Become a Reviewer or Editor](#become-a-reviewer-or-editor). To make additions, read [Become an Author](#become-an-author).
3. Make your modifications. Be sure to follow our [style guide](style_guide.md).
4. When you're ready to submit your work, push your changes to your fork. Ensure that your fork is [synced with `master`](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).
5. You can submit a [draft PR](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests#draft-pull-requests) or a [regular PR](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork). If your work is not yet ready for review and merge, choose a draft PR. When your changes are ready to be reviewed, you can convert to a regular PR. See [how to change the stage of a PR](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/changing-the-stage-of-a-pull-request) for more.

You may want to [allow edits from maintainers](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so we can help with small changes like fixing typos.

Once you've submitted your ready-for-review PR, we'll review it. We may comment to ask for clarification or changes, so please check back in the next few days.

To increase the chances that your PR is merged, please make sure that:

1. You've followed the guidelines above for associating your work with an issue.
2. Your work is Markdown linted.
3. Your writing follows the [article template materials](template) and [style guide](style_guide.md).
4. Your code snippets are correct, well-tested, and commented where necessary for understanding.

Once the PR is complete, we'll merge it! At that point, you may like to add yourself to [the project's list of authors, reviewers, or editors](document/1-Frontispiece/README.md).

## How to Set Up Your Contributor Environment

1. [Create an account on GitHub](https://help.github.com/en/github/getting-started-with-github/signing-up-for-a-new-github-account).
2. Install [Visual Studio Code](https://code.visualstudio.com/) and this [Markdown linter plugin](https://github.com/DavidAnson/vscode-markdownlint#install). We use this linter to help keep the project content consistent and pretty.

    1. From the gear icon/menu select "Settings".
    2. Select the "Workspace" tab.
    3. Expand "Extensions", and find "markdownlint".
    4. Just below "Markdownlint: config" click the "Edit in settings.json" link.
    5. Add the following:

    ```json
    "markdownlint.config": {
      "extends": ".github/configs/.markdownlint.json"
    }
    ```

3. Fork and clone your own copy of the repository. Here are complete instructions for [forking and syncing with GitHub](https://help.github.com/en/github/getting-started-with-github/fork-a-repo).

## Contributing with Codespaces

We've included settings for GitHub Codespaces so you can use a cloud-hosted IDE to contribute to this repository! Our configuration includes Visual Studio Code extensions and `markdownlint` configuration settings that help to keep work consistent across all our amazing contributors.

Codespaces is currently in limited beta. To learn more, see [About Codespaces](https://docs.github.com/en/github/developing-online-with-codespaces/about-codespaces).

If you have access to the beta, get started by [creating a codespace](https://docs.github.com/en/github/developing-online-with-codespaces/creating-a-codespace) for this repository.
