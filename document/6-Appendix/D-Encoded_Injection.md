# Encoded Injection

## Background

Character encoding is the process of mapping characters, numbers and other symbols to a standard format. Typically, this is done to create a message ready for transmission between sender and receiver. It is, in simple terms, the conversion of characters (belonging to different languages like English, Chinese, Greek or any other known language) into bytes. An example of a widely used character encoding scheme is the American Standard Code for Information Interchange (ASCII) that initially used 7-bit codes. More recent examples of encoding schemes would be the Unicode `UTF-8` and `UTF-16` computing industry standards.

In the space of application security and due to the plethora of encoding schemes available, character encoding has a popular misuse. It is being used for encoding malicious injection strings in a way that obfuscates them. This can lead to the bypass of input validation filters, or take advantage of particular ways in which browsers render encoded text.

## Input Encoding – Filter Evasion

Web applications usually employ different types of input filtering mechanisms to limit the input that can be submitted by the user. If these input filters are not implemented sufficiently well, it is possible to slip a character or two through these filters. For instance, a `/` can be represented as `2F` (hex) in ASCII, while the same character (`/`) is encoded as `C0` `AF` in Unicode (2 byte sequence). Therefore, it is important for the input filtering control to be aware of the encoding scheme used. If the filter is found to be detecting only `UTF-8` encoded injections, a different encoding scheme may be employed to bypass this filter.

## Output Encoding – Server & Browser Consensus

Web browsers need to be aware of the encoding scheme used to coherently display a web page. Ideally, this information should be provided to the browser in the HTTP header (`Content-Type`) field, as shown below:

```http
Content-Type: text/html; charset=UTF-8
```

or through HTML META tag (`META HTTP-EQUIV`), as shown below:

``` html
<META http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
```

It is through these character encoding declarations that the browser understands which set of characters to use when converting bytes to characters. Note that the content type mentioned in the HTTP header has precedence over the META tag declaration.

CERT describes it here as follows:

Many web pages leave the character encoding (`charset` parameter in HTTP) undefined. In earlier versions of HTML and HTTP, the character encoding was supposed to default to `ISO-8859-1` if it wasn't defined. In fact, many browsers had a different default, so it was not possible to rely on the default being `ISO-8859-1`. HTML version 4 legitimizes this - if the character encoding isn't specified, any character encoding can be used.

If the web server doesn't specify which character encoding is in use, it can't tell which characters are special. Web pages with unspecified character encoding work most of the time because most character sets assign the same characters to byte values below 128. But which of the values above 128 are special? Some 16-bit `character-encoding` schemes have additional multi-byte representations for special characters such as `<`. Some browsers recognize this alternative encoding and act on it. This is "correct" behavior, but it makes attacks using malicious scripts much harder to prevent. The server simply doesn't know which byte sequences represent the special characters.

Therefore in the event of not receiving the character encoding information from the server, the browser either attempts to guess the encoding scheme or reverts to a default scheme. In some cases, the user explicitly sets the default encoding in the browser to a different scheme. Any such mismatch in the encoding scheme used by the web page (server) and the browser may cause the browser to interpret the page in a manner that is unintended or unexpected.

### Encoded Injections

All the scenarios given below form only a subset of the various ways obfuscation can be achieved to bypass input filters. Also, the success of encoded injections depends on the browser in use. For example, `US-ASCII` encoded injections were previously successful only in IE browser but not in Firefox. Therefore, it may be noted that encoded injections, to a large extent, are browser dependent.

### Basic Encoding

Consider a basic input validation filter that protects against injection of single quote character. In this case the following injection would easily bypass this filter:

``` html
<script>alert(String.fromCharCode(88,83,83))</script>
```

`String.fromCharCode` JavaScript function takes the given Unicode values and returns the corresponding string. This is one of the most basic forms of encoded injections. Another vector that can be used to bypass this filter is:

``` html
<IMG src="" onerror=javascript:alert(&quot;XSS&quot;)>
```

Or by using the respective [HTML character codes](https://www.rapidtables.com/code/text/unicode-characters.html):

``` html
<IMG src="" onerror="javascript:alert(&#34;XSS&#34;)">
```

The above uses HTML Entities to construct the injection string. HTML Entities encoding is used to display characters that have a special meaning in HTML. For instance, `>` works as a closing bracket for a HTML tag. In order to actually display this character on the web page HTML character entities should be inserted in the page source. The injections mentioned above are one way of encoding. There are numerous other ways in which a string can be encoded (obfuscated) in order to bypass the above filter.

### Hex Encoding

Hex, short for Hexadecimal, is a base 16 numbering system i.e it has 16 different values from `0` to `9` and `A` to `F` to represent various characters. Hex encoding is another form of obfuscation that is sometimes used to bypass input validation filters. For instance, hex encoded version of the string `<IMG SRC=javascript:alert('XSS')>` is

``` html
<IMG SRC=%6A%61%76%61%73%63%72%69%70%74%3A%61%6C%65%72%74%28%27%58%53%53%27%29>
```

A variation of the above string is given below. Can be used in case ‘%’ is being filtered:

``` html
<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>
```

There are other encoding schemes, such as Base64 and Octal, that may be used for obfuscation. Although, every encoding scheme may not work every time, a bit of trial and error coupled with intelligent manipulations would definitely reveal the loophole in a weakly built input validation filter.

### UTF-7 Encoding

UTF-7 encoding of

``` html
<SCRIPT>
    alert(‘XSS’);
</SCRIPT>
```

is as below

`+ADw-SCRIPT+AD4-alert('XSS');+ADw-/SCRIPT+AD4-`

For the above script to work, the browser has to interpret the web page as encoded in `UTF-7`.

### Multi-byte Encoding

Variable-width encoding is another type of character encoding scheme that uses codes of varying lengths to encode characters. Multi-Byte Encoding is a type of variable-width encoding that uses varying number of bytes to represent a character. Multi-byte encoding is primarily used to encode characters that belong to a large character set e.g. Chinese, Japanese and Korean.

Multibyte encoding has been used in the past to bypass standard input validation functions and carry out cross site scripting and SQL injection attacks.

## References

- [Encoding (Semiotics)](https://en.wikipedia.org/wiki/Encoding_(semiotics))
- [HTML Entities](https://www.w3schools.com/HTML/html_entities.asp)
- [How to prevent input validation attacks](https://searchsecurity.techtarget.com/answer/How-to-prevent-input-validation-attacks)
- [Unicode and Character Sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)
