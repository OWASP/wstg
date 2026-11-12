# Server-side Document Rendering Injection

|ID          |
|------------|
|WSTG-INJT-27|

## Summary

Many applications turn user-supplied content into documents on the server: invoices, tickets and reports as PDF, web pages as images, uploaded SVG files as thumbnails, office documents converted to PDF, or XML transformed with XSLT. To do this they pass the content to a rendering engine, such as a headless browser driven by Puppeteer or Playwright, an HTML to PDF library, an image conversion tool, an office suite running without a user interface, or an XSLT processor.

These engines are much more capable than the application usually needs. A headless browser runs JavaScript, follows links to files and internal addresses, and loads fonts, images and style sheets from anywhere. When user input reaches the content being rendered without being escaped, an attacker can use the engine to:

- Read local files or internal web pages, and see the result in the rendered document.
- Send requests to internal services and cloud metadata endpoints, as described in [Server-Side Request Forgery](19-Server-Side_Request_Forgery.md).
- Run JavaScript inside the renderer, which can read the content of other pages it loads.
- Exploit vulnerabilities in the engine itself, which are common in libraries that are no longer maintained or in tools that parse many formats.

Examples include the [dompdf font cache issue (CVE-2022-28368)](https://positive.security/blog/dompdf-rce), where an injected `@font-face` rule could make the library store a PHP file in its font cache, which can be run if that directory is reachable from the web, and [ImageTragick (CVE-2016-3714)](https://imagetragick.com/), where crafted images led to command execution in ImageMagick. wkhtmltopdf, which is still widely used, is built on QtWebKit, which Qt removed in 2016, and the project's repository has been archived. It only [blocks local file access by default since version 0.12.6](https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.6).

## Test Objectives

- Identify features that render user-controlled content into documents or images on the server.
- Identify the rendering engine and determine whether it processes HTML, CSS, JavaScript, external resources or style sheets supplied by the user.
- Assess whether the renderer can be used to read local files, reach internal services or run code.

## How to Test

### Find Rendering Features

Look for features that produce a document from data the user controls, even indirectly:

- Export or download as PDF, print views, and emailed reports or invoices.
- Screenshots, link previews and social media cards generated on the server.
- Profile pictures, attachments and uploads that are converted or resized, especially SVG and office documents.
- Fields that end up in a generated document, such as names, addresses, comments, item descriptions or report titles.
- Features that accept XML together with a style sheet, or a style sheet on its own.

### Identify the Engine

Download a generated document and read its metadata. In a PDF, the `Producer` and `Creator` fields often name the engine and its version. PDFs printed by headless Chrome, for example, report `Skia/PDF` as the producer, and wkhtmltopdf names itself in the creator field. Tools such as `exiftool` or `pdfinfo` show these fields. The fonts embedded in the document, the way pages break, and error messages for malformed input also point to the engine.

Knowing the engine tells you which features to expect and which known vulnerabilities to check.

### Check Whether Markup Is Rendered

Put simple markup in each field that appears in the document, such as `<b>bold</b>` or `<u>test</u>`, and check whether it is rendered or shown as text. If HTML is rendered, try the following, one at a time, and look at the result in the document:

- An image or style sheet from a server you control, for example `<img src="https://attacker.example/x.png">` or `<link rel="stylesheet" href="https://attacker.example/x.css">`. A request to that server confirms the renderer loads external resources and shows its IP address and `User-Agent`.
- JavaScript that changes the page, for example `<script>document.write(navigator.userAgent)</script>`. If the user agent appears in the document, scripts run, and the renderer's version is visible too.
- Local files, for example `<iframe src="file:///etc/passwd" width="800" height="600"></iframe>`, and on Windows `file:///c:/windows/win.ini`. Whether this works depends on the engine, its settings, and how the HTML is loaded into it.
- Internal addresses, such as `http://127.0.0.1/`, `http://localhost:8080/` and cloud metadata endpoints. See [Server-Side Request Forgery](19-Server-Side_Request_Forgery.md) for the addresses and bypasses to try.

When scripts run, check whether a script can read the content of a page it loads and write it into the document, for example by fetching an internal URL and inserting the response. This turns a blind request into a readable one. Also check whether the rendering is done with the user's session or with a service account, since internal pages may then show data the user should not see.

If the engine is a known library, test for its published issues. For dompdf, check whether remote resources are enabled and fonts can be loaded with `@font-face`. For older wkhtmltopdf versions, check local file access.

### Images, SVG and Office Documents

Converting files also uses a rendering engine:

- SVG files can reference other files and URLs, for example with `<image href="file:///etc/passwd"/>` or an `href` to an internal address, and can include XML entities. See [XML Injection](07-XML_Injection.md) for entity-based attacks.
- Image conversion tools that guess the format from the content may parse formats the application does not expect. Check the version of the tool against known vulnerabilities, such as ImageTragick for ImageMagick.
- Office documents converted on the server can contain links to external images, linked objects and fields that are fetched or evaluated during conversion.

Combine these checks with [Upload of Malicious Files](../10-Business_Logic/09-Upload_of_Malicious_Files.md) where the content is uploaded.

### XSLT

If the application accepts XML and applies an XSLT style sheet, check whether the style sheet itself, or part of it, can be supplied by the user. An attacker-controlled style sheet can read files with the `document()` function and, in some processors, call extension functions that run code. Send a style sheet that outputs `system-property('xsl:vendor')` to identify the processor, then test what its extension functions allow.

## Related Test Cases

- [Server-Side Request Forgery](19-Server-Side_Request_Forgery.md)
- [Server-side Template Injection](18-Server-side_Template_Injection.md)
- [XML Injection](07-XML_Injection.md)
- [Upload of Malicious Files](../10-Business_Logic/09-Upload_of_Malicious_Files.md)

## Remediation

- Escape user input for the format being rendered, the same way as for output to a browser, so it is treated as text rather than markup.
- Disable features the conversion does not need, such as JavaScript, remote resources, local file access and external entities.
- Run the renderer in a sandbox without access to local files, internal networks or cloud metadata endpoints, and with a time and memory limit.
- Do not render with the user's session or with credentials that can reach internal services.
- Keep the rendering engine up to date, and replace engines that are no longer maintained.
- Do not accept style sheets from users. Where XSLT is required, disable extension functions and external document access.

## Tools

- [ExifTool](https://exiftool.org/), to read document metadata
- A server under your control, or an out-of-band interaction service, to see requests made by the renderer

## References

- [Positive Security: dompdf RCE through font cache poisoning (CVE-2022-28368)](https://positive.security/blog/dompdf-rce)
- [ImageTragick (CVE-2016-3714)](https://imagetragick.com/)
- [wkhtmltopdf: Status](https://wkhtmltopdf.org/status.html)
- [wkhtmltopdf 0.12.6 release notes](https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.6)
- [W3C: XSL Transformations (XSLT) Version 3.0](https://www.w3.org/TR/xslt-30/)
