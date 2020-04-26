# Review Webpage Comments, Metadata and Javascript for Information Leakage

|ID           |
|-------------|
|WSTG-INFO-05|

## Summary

It is very common, and even recommended, for programmers to include detailed comments and metadata on their source code. However, comments and metadata included into the HTML code might reveal internal information that should not be available to potential attackers. Comments and metadata review should be done in order to determine if any information is being leaked.

For modern web models, the use of client-Side Javascript for front end is becoming more popular. The popular front end construction technologies use client-side Javascript like ReactJS, AngularJS, Vue.  Similar to the comments and metadata on the HTML code, many programmers also hardcode sensitive information in Javascript variables on the front end. Sensitive information can be referred to as Private API Key (for example: Google Map API Key but not retricted), internal IP addresses, sensitive routes (for example: route to hidden admin page), or even credentials. This sensitive information can be leaked from their front end. Javascript code review should be done in order to determine if any sensitive information leaked could be used by attackers to abuse.

For large web application, performance issues are big concern to programmers. So programmers have used many different methods to optimize front-end performance. These include Syntactically Awesome StyleSheets (SASS), Sassy CSS (SCSS), WebPack, etc. This is also good for security when front end codes will become more difficult to understand and difficult to debug. But also because of that programmers often deploy source map files for debugging purposes. A “source map” is a special file that connects a minified/uglified version of an asset (CSS or JavaScript) to the original authored version. Programmers are still arguing over whether or not to bring source map files to the product environment. However, it is undeniable that source map files or files for debugging if released to the product environment will make their source to be human-readable and clearly, It can make it easier for attackers to find vulnerabilities from your front end or collect sensitive information from it. So Javascript code review should be done in order to determine if any debug files are exposed from your front end. Depending on the context and sensitivity of the project, security expert will decide whether the file should exist in the product environment or not.

## Test Objectives

* Review webpage comments and metadata to better understand the application and to find any information leakage.

* Identifying and gathering JavaScript files, review Javascript code in an application to better understand the application and to find any information leakage.

* Identifying if source map file and/or other front-end debug files exist.

## How to Test

### Review webpage comments and metadata

HTML comments are often used by the developers to include debugging information about the application. Sometimes they forget about the comments and they leave them on in production. Testers should look for HTML comments which start with " ".

#### Black-Box Testing

Check HTML source code for comments containing sensitive information that can help the attacker gain more insight about the application. It might be SQL code, usernames and passwords, internal IP addresses, or debugging information.

```html
...

<div class="table2">
  <div class="col1">1</div><div class="col2">Mary</div>
  <div class="col1">2</div><div class="col2">Peter</div>
  <div class="col1">3</div><div class="col2">Joe</div>

<!-- Query: SELECT id, name FROM app.users WHERE active='1' -->

</div>
...
```

The tester may even find something like this:

```html
<!-- Use the DB administrator password for testing:  f@keP@a$$w0rD -->
```

Check HTML version information for valid version numbers and Data Type Definition (DTD) URLs

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
```

- `strict.dtd` -- default strict DTD
- `loose.dtd` -- loose DTD
- `frameset.dtd` -- DTD for frameset documents

Some Meta tags do not provide active attack vectors but instead allow an attacker to profile an application to

```html
<META name="Author" content="Andrew Muller">
```

A common (but not WCAG compliant) Meta tag is the refresh.

```html
<META http-equiv="Refresh" content="15;URL=https://www.owasp.org/index.html">
```

A common use for Meta tag is to specify keywords that a search engine may use to improve the quality of search results.

```html
<META name="keywords" lang="en-us" content="OWASP, security, sunshine, lollipops">
```

Although most web servers manage search engine indexing via the robots.txt file, it can also be managed by Meta tags. The tag below will advise robots to not index and not follow links on the HTML page containing the tag.

```html
<META name="robots" content="none">` `
```

The Platform for Internet Content Selection (PICS) and Protocol for Web Description Resources (POWDER) provide infrastructure for associating meta data with Internet content.

#### Gray-Box Testing

Not applicable.

### Identifying Javascript code and gathering JavaScript files

Programmers often hardcode sensitive information with Javascript variables on the front end. Testers should check HTML source code and look for Javascript code between \<script\> and \<\/script\> tags. Testers should also identify external Javascript files to review the code (JavaScript files have the file extension .js and name of the JavaScript file usually put in the src (source) attribute of a \<script\> tag).

#### Black-Box Testing

Check Javascript code for any sensitive information leaked could be used by attackers to abuse. It might be Private API Key, internal IP addresses, sensitive routes or credentials.

```javascript
const myS3Credentials = {
  accessKeyId: config('AWSS3AccessKeyID'),
  secretAcccessKey: config('AWSS3SecretAccessKey'),
};
```

The tester may even find something like this:

```javascript
var conString = "tcp://postgres:1234@localhost/postgres";
```

When found an API Key, testers can check if the API Key restrictions are set per service or by IP, HTTP referrer, application, SDK, etc.

For example, if testers found a Google Map API Key, testers can check if this API Key is restricted by IP or restricted only per the Google Map APIs. If the Google API Key is restricted only per the Google Map APIs, attackers can still use that API Key to query unrestricted Google Map APIs and the victim must to pay for that.

```html

<script type="application/json">
...

{"GOOGLE_MAP_API_KEY":"AIzaSyDUEBnKgwiqMNpDplT6ozE4Z0XxuAbqDi4", "RECAPTCHA_KEY":"6LcPscEUiAAAAHOwwM3fGvIx9rsPYUq62uRhGjJ0"}

...
</script>
```

In some cases, testers may found sensitive routes from Javascript code, such as links to internal/hidden admin pages.

```html

<script type="application/json">
...

"runtimeConfig":{"BASE_URL_VOUCHER_API":"https://staging-voucher.victim.net/api", "BASE_BACKOFFICE_API":"https://10.10.10.2/api", "ADMIN_PAGE":"/hidden_administrator"}

...
</script>
```

#### Gray-Box Testing

Not applicable.

### Identifying source map files

Source map files will usually be loaded when DevTools open. Testers can also find source map files by adding the ".map" extension after the extension of each external Javascript file. For example, if tester see /static/js/main.chunk.js file, tester may found its source map file by visiting /static/js/main.chunk.js.map.

#### Black-Box Testing

Check source map files for any sensitive information that can help the attacker gain more insight about the application.

```json
{
  version: 3,
  file: "static/js/main.chunk.js",
  - sources: [
    "/home/sysadmin/cashsystem/src/actions/index.js",
    "/home/sysadmin/cashsystem/src/actions/reportAction.js",
    "/home/sysadmin/cashsystem/src/actions/cashoutAction.js",
    "/home/sysadmin/cashsystem/src/actions/userAction.js",

    ...

  ],

  ...

}
```

When websites load source map files, The front-end source code will become readable and easily to debug.

#### Gray-Box Testing

Not applicable.

## Tools

- [Wget](https://www.gnu.org/software/wget/wget.html)
- Browser “view source” function
- Eyeballs
- [Curl](https://curl.haxx.se/)
- [Burp Suite](https://portswigger.net/burp)
- [Waybackurls](https://github.com/tomnomnom/waybackurls)
- [Google Maps API Scanner](https://github.com/ozguralp/gmapsapiscanner/)
- 

## References
- [KeyHacks](https://github.com/streaak/keyhacks) 

### Whitepapers

- [HTML version 4.01](https://www.w3.org/TR/1999/REC-html401-19991224)
- [XHTML](https://www.w3.org/TR/2010/REC-xhtml-basic-20101123/)
- [HTML version 5](https://www.w3.org/TR/html5/)
