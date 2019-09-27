# OWASP Testing Guide Project

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/OWASP/OWASP-Testing-Guide-v5/issues)
[![OWASP Flagship](https://img.shields.io/badge/owasp-flagship-brightgreen.svg)](https://www.owasp.org/index.php/OWASP_Project_Inventory#tab=Flagship_Projects)

Welcome to the OWASP Testing Guide (OTG) project!

You can download the stable version v4 [here](http://www.owasp.org/index.php/OWASP_Testing_Project).

1. [OWASP Testing Guide Project](#owasp-testing-guide-project)
   1. [Contributions, Feature Requests, and Feedback](#contributions-feature-requests-and-feedback)
   2. [Style Guidelines](#style-guidelines)
   3. [Maintainers](#maintainers)
   4. [Special Thanks](#special-thanks)
   5. [Project Summit 2017 Outcomes](#project-summit-2017-outcomes)

## Contributions, Feature Requests, and Feedback

**Everyone can contribute!** By simply reading the document, which you certainly should do, grammar mistakes, new ideas, or paragraph restructuring thoughts will show themselves! Just try it out, you'll see. :smile:

Not to mention, you'll be on the authors, or reviewers and editors list.

Before you start contributing, please read our [**contribution guide**](CONTRIBUTING.md) which should help you get started and follow our best practices.

Whenever you identify a contribution possibility, open up an [issue](https://github.com/OWASP/OWASP-Testing-Guide-v5/issues) with it in order for us to keep track and assign project milestones.

For the ones that enjoy providing constructive feedback and feel like they can review other's contributions, head straight to our [Pull Requests](https://github.com/OWASP/OWASP-Testing-Guide-v5/pulls)!

Despite us being technical, we love having technical and casual chats with others. Join us by following the below steps:

- Join [OWASP Slack](https://join.slack.com/t/owasp/shared_invite/enQtNjExMTc3MTg0MzU4LWQ2Nzg3NGJiZGQ2MjRmNzkzN2Q4YzU1MWYyZTdjYjA2ZTA5M2RkNzE2ZjdkNzI5ZThhOWY5MjljYWZmYmY4ZjM).
- Join this project's [channel: #testing-guide](https://app.slack.com/client/T04T40NHX/CJ2QDHLRJ) (yes, you can join other channels, we won't stop you!).

Feel free to ask questions, bounce ideas off us, or just hang out and chat!

You can also open up a post on our [Google Group](https://groups.google.com/a/owasp.org/forum/#!forum/testing-guide-project)!

## Style Guidelines

- Please don't write in the first person (Ex: no "I" or "Me" statements).
- Please do use Title Caps for headings, using Title Capitalization as defined by the *Chicago Manual of Style*. For quick reference you can use this [online tool](https://capitalizemytitle.com/#Chicago) (make sure you select the "Chicago" tab).
- Please do use serial or [Oxford commas](https://www.grammarly.com/blog/what-is-the-oxford-comma-and-why-do-people-care-so-much-about-it/).
- Don't use `and/or`. Chances are you can simply write `or`. (Note: The OR allows for the same True result as an AND, while also allowing for other combinations producing True results.) Unless you actually mean something like "A and/exclusive or B" in which case read the sentence to yourself with those words and then figure out a different way to write it. :smile:
- Caption figures using title case, with the section and sub-section numbers, followed by the figure position in the document. Use the format *`Figure <section>.<sub-section>-<position>: Caption Title`*. For example, the first image shown in section 4.8, sub-section 19 would be added as follows:

    ```md
    ![SSTI XVWA Example](images/SSTI_XVWA.jpeg)\
    *Figure 4.8.19-1: SSTI XVWA Example*
    ```

## Project Folder Structure

When adding articles and images, please place articles in the appropriate sub-section directory, and place images in an `images/` folder within the article directory. Here is an example of the project structure:

```console
document/
 ├───0_Foreword/
 │   └───0_Foreword.md
 ├───1_Frontispiece/
 │   ├───images/
 │   │   └───example.jpg
 │   └───1_Frontispiece.md
 ├───2_Introduction/
 │   ├───images/
 │   │   └───example.jpg
 │   └───2_Introduction.md
 ├───3_The_OWASP_Testing_Framework/
 │   ├───images/
 │   │   └───example.jpg
 │   └───3_The_OWASP_Testing_Framework.md
 ├───4_Web_Application_Security_Testing/
 │   ├───4.1_Introduction_and_Objectives/
 │   │   └───4.1_Testing_Introduction_and_Objectives.md
 │   ├───4.2_Information_Gathering/
 │   │   ├───images/
 │   │   │   └───example.jpg
 │   │   ├───4.2_Testing_Information_Gathering.md
 │   │   └───4.2.1_Conduct_Search_Engine_Discovery.md

```

## Maintainers

- [Rick Mitchell](https://github.com/kingthorin)
- [Elie Saad](https://github.com/ThunderSon)

## Special Thanks

For the people that helped migrate this project from MediaWiki to GitHub's flavored Markdown, thank you!

- [Rejah Rehim](https://github.com/rejahrehim)

## Project Summit 2017 Outcomes

The outcomes can be found [here](OWASP_Summit_Outcomes.md)
