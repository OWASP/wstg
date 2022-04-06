# Style Guide

The Web Security Testing Guide (WSTG) is a well-known document trusted by security professionals and organizations all over the world. These guidelines help ensure it reflects well on its many contributors and the security community.

To maintain the quality of the WSTG, please follow these general rules.

1. Be factual, specific, and ensure paragraphs are focused on their heading.
2. Ensure information is creditable and up to date. Provide links and citations where appropriate.
3. Avoid duplicating content. To refer to existing content, link to it inline.

## Write for the Reader

Readers of the WSTG come from many different countries and have varying levels of technical expertise. Write for an international audience with a basic technical background. Use words that are likely understood by a non-native English speaker. Use short sentences that are easy to understand.

The web tool [Hemingway](https://hemingwayapp.com/) can help you write with clarity.

## Formatting

Use consistent formatting to help us review and publish content, and help readers to digest information. Write all content using [Markdown syntax](https://guides.github.com/features/mastering-markdown/#examples).

Please follow these further guidelines for formatting.

### Article Template

We use an article template to help ensure topics are complete and easy to understand. Please use the [template materials](template) to structure new content.

### Project Folder Structure

When adding articles and images, please place articles in the appropriate sub-section directory. Place images in an `images/` folder within the article directory. Here is an example of the project structure:

```sh
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

### Code Syntax Highlighting

Use code fences with syntax highlighting for snippets. For example:

```md
    ```javascript
    if (isAwesome){
        return true
    }
    ```
```

### Caption Images

Caption images and figures using title case. Use the section and sub-section numbers, followed by the figure position in the document. Use the format `Figure <section>.<sub-section>-<position>: Caption Title`.

For example, caption the first image shown in section 4.8, sub-section 19 as follows:

```md
![SSTI XVWA Example](images/SSTI_XVWA.jpeg)\
*Figure 4.7.19-1: SSTI XVWA Example*
```

### Inline Links

Add links inline. Use words in the sentence to describe them, or include their specific title. For example:

```md
This project provides a [style guide](style_guide.md). Some style choices are taken from the [Chicago Manual of Style](https://www.chicagomanualofstyle.org/).
```

### Inline References

For resources where a link is not available, such as a whitepaper or book, we prefer a conversational in-line reference rather than any academic-styled citation. Work the title of the resource as well as its author into your text. For example:

> There are three possible cases: only the whale exists, only the petunias exist, or both the whale and petunias exist simultaneously. These possibilities are referenced in a series of books entitled *The Hitchhiker's Guide to the Galaxy,* by Douglas Adams.

This format has the advantage of continuing the flow of the article and not inviting readers to jump from paragraph to paragraph, looking for an asterisk, or to another location to find a reference list. It's also easy to read and to maintain since it appears in just one place.

### Bold, Italic, and Underline

Do not use bold, italic, or underlined text for emphasis.

You may italicize a word when referring to the word itself, though the need for this in technical writing is rare. For examples, see the section [Use Correct Words](#use-correct-words). Use asterisks: `*italic*`.

## Language and Grammar

To make the WSTG consistent and pleasant to read, please check your spelling (we use American English) and use proper grammar.

The sections below describe specific style choices to follow.

### Title Case

Use title case for headings, following the [Chicago Manual of Style](https://www.chicagomanualofstyle.org/book/ed17/frontmatter/toc.html). The "Chicago" tab on the website [Capitalize My Title](https://capitalizemytitle.com/#Chicago) may help.

### Active Voice

Avoid using passive voice. For example:

> Bad: "Vulnerabilities are found by running tests."  
> Good: "Run tests to find vulnerabilities."  

### Second Person

Do not write in the first or third person, such as by using *I* or *he*. When giving technical instruction, address the reader in the second person. Use a [zero or implied subject](https://en.wikipedia.org/wiki/Subject_(grammar)#Forms_of_the_subject), or if you must, use *you*.

> Bad: "He/she/an IT monkey would run this code to test..."  
> Better: "By running this code, you can test..."  
> Best: "Run this code to test..."

### Numbering Conventions

For numbers from zero to ten, write the word. For numbers higher than ten, use integers. For example:

> One broken automated test finds 42 errors if you run it ten times.

Describe simple fractions in words. For example:

> Half of all software developers like petunias, and a third of them like whales.

When describing an approximate magnitude of monetary value, write the whole word and do not abbreviate. For example:

> Bad: "Security testing saves companies $18M in beer every year."  
> Good: "Security testing saves companies eighteen million dollars in beer every year."

For specific monetary value, use currency symbols and integers. For example:

> A beer costs $6.75 today, and $8.25 tomorrow.

### Abbreviations

Explain abbreviations the first time they appear in your document. Capitalize the appropriate words to indicate the abbreviated form. For example:

> This project contains the source code for the Web Security Testing Guide (WSTG). The WSTG is a nice and accurate book.

### Lists and Punctuation

Use bulleted lists when the order is unimportant. Use numbered lists for sequential steps. For each line, capitalize the first word. If the line is a sentence or completes a sentence, end with a period. For example:

> Testing this scenario will:
>
> - Make the application safer.
> - Improve overall security posture.
> - Keep customers happy.
>
> To test this scenario:
>
> 1. Copy the code.
> 2. Open a terminal.
> 3. Run the code as root.
>
> Here are some foods to snack on while testing.
>
> - Apples
> - Beef jerky
> - Chocolate

For lists in a sentence, use serial or [Oxford commas](https://www.grammarly.com/blog/what-is-the-oxford-comma-and-why-do-people-care-so-much-about-it/). For example:

> Test the application using automated tests, static code review, and penetration tests.

### Use Correct Words

The following section covers some frequently misused words and instructions on how to correctly use them.

#### *and/or*

While sometimes used in legal documents, *and/or* leads to ambiguity and confusion in technical writing. Instead, use *or*, which in the English language includes *and*. For example:

> Bad: "The code will output an error number and/or description."  
> Good: "The code will output an error number or description."

The latter sentence does not exclude the possibility of having both an error number and description.

If you need to specify all possible outcomes, use a list:

> "The code will output an error number, or a description, or both."

#### *frontend, backend*

While it's true that the English language evolves over time, these are not yet words.

When referring to nouns, use *front end* and *back end*. For example:

> Security is equally important on the front end as it is on the back end.

As a descriptive adverb, use the hyphenated *front-end* and *back-end*.

> Both front-end developers and back-end developers are responsible for application security.

#### *whitebox*, *blackbox*, *greybox*

These are not words.

As nouns, use *white box*, *black box*, and *grey box*. These nouns rarely appear in connection with cybersecurity.

> My cat enjoys jumping into that grey box.

As adverbs, use the hyphenated *white-box*, *black-box*, and *grey-box*. Do not use capitalization unless the words are in a title.

> While white-box testing involves knowledge of source code, black-box testing does not. A grey-box test is somewhere in-between.

#### *ie*, *eg*

These are letters.

The abbreviation *ie* refers to the Latin `id est`, which means "in other words." The abbreviation *eg* is for `exempli gratia`, translating to "for example." To use these in a sentence:

> Write using proper English, i.e. correct spelling and grammar. Use common words over uncommon ones, e.g. "learn" instead of "glean."

#### *etc*

These are also letters.

The Latin phrase *et cetera* translates to "and the rest." It is abbreviated and typically placed at the end of a list that seems redundant to complete:

> WSTG authors like rainbow colors, such as red, yellow, green, etc.

In technical writing, the use of *etc* is problematic. It assumes that the reader knows what you're talking about, and they may not. Violet is one of the colors of the rainbow, but the example above does not explicitly tell you if violet is a color that WSTG authors like.

It is better to be explicit and thorough than to make assumptions of the reader. Only use *etc* to avoid completing a list that was given in full earlier in the document.

#### *...* (ellipsis)

The ellipsis punctuation mark can indicate that words have been left out of a quote:

> Linus Torvalds once said, "Once you realize that documentation should be laughed at... THEN, and only then, have you reached the level where you can safely read it and try to use it to actually implement a driver. "

As long as the omission does not change the meaning of the quote, this is acceptable usage of ellipsis in the WSTG.

All other uses of ellipsis, such as to indicate an unfinished thought, are not.

#### *ex*

While this is a word, it is likely not the word you are looking for. The word *ex* has particular meaning in the fields of finance and commerce, and may refer to a person if you are discussing your past relationships. None of these topics should appear in the WSTG.

The abbreviation may be used to mean "example" by lazy writers. Please don't be lazy, and write *example* instead.
