# Review Old Backup and Unreferenced Files for Sensitive Information

|ID          |
|------------|
|WSTG-CONF-04|

## Summary

While most of the files within a web server are directly handled by the server itself, it isn't uncommon to find unreferenced or forgotten files that can be used to obtain important information about the infrastructure or the credentials.

Most common scenarios include the presence of renamed old versions of modified files, inclusion files that are loaded into the language of choice and can be downloaded as source, or even automatic or manual backups in form of compressed archives. Backup files can also be generated automatically by the underlying file system the application is hosted on, a feature usually referred to as "snapshots".

All these files may grant the tester access to inner workings, back doors, administrative interfaces, or even credentials to connect to the administrative interface or the database server.

An important source of vulnerability lies in files which have nothing to do with the application, but are created as a consequence of editing application files, or after creating on-the-fly backup copies, or by leaving in the web tree old files or unreferenced files.Performing in-place editing or other administrative actions on production web servers may inadvertently leave backup copies, either generated automatically by the editor while editing files, or by the administrator who is zipping a set of files to create a backup.

It is easy to forget such files and this may pose a serious security threat to the application. That happens because backup copies may be generated with file extensions differing from those of the original files. A `.tar`, `.zip` or `.gz` archive that we generate (and forget...) has obviously a different extension, and the same happens with automatic copies created by many editors (for example, emacs generates a backup copy named `file~` when editing `file`). Making a copy by hand may produce the same effect (think of copying `file` to `file.old`). The underlying file system the application is on could be making `snapshots` of your application at different points in time without your knowledge, which may also be accessible via the web, posing a similar but different `backup file` style threat to your application.

As a result, these activities generate files that are not needed by the application and may be handled differently than the original file by the web server. For example, if we make a copy of `login.asp` named `login.asp.old`, we are allowing users to download the source code of `login.asp`. This is because `login.asp.old` will be typically served as text or plain, rather than being executed because of its extension. In other words, accessing `login.asp` causes the execution of the server-side code of `login.asp`, while accessing `login.asp.old` causes the content of `login.asp.old` (which is, again, server-side code) to be plainly returned to the user and displayed in the browser. This may pose security risks, since sensitive information may be revealed.

Generally, exposing server-side code is a bad idea. Not only are you unnecessarily exposing business logic, but you may be unknowingly revealing application-related information which may help an attacker (path names, data structures, etc.). Not to mention the fact that there are too many scripts with embedded username and password in clear text (which is a careless and very dangerous practice).

Other causes of unreferenced files are due to design or configuration choices when they allow diverse kind of application-related files such as data files, configuration files, log files, to be stored in file system directories that can be accessed by the web server. These files have normally no reason to be in a file system space that could be accessed via web, since they should be accessed only at the application level, by the application itself (and not by the casual user browsing around).

### Threats

Old, backup and unreferenced files present various threats to the security of a web application:

- Unreferenced files may disclose sensitive information that can facilitate a focused attack against the application; for example include files containing database credentials, configuration files containing references to other hidden content, absolute file paths, etc.
- Unreferenced pages may contain powerful functionality that can be used to attack the application; for example an administration page that is not linked from published content but can be accessed by any user who knows where to find it.
- Old and backup files may contain vulnerabilities that have been fixed in more recent versions; for example `viewdoc.old.jsp` may contain a directory traversal vulnerability that has been fixed in `viewdoc.jsp` but can still be exploited by anyone who finds the old version.
- Backup files may disclose the source code for pages designed to execute on the server; for example requesting `viewdoc.bak` may return the source code for `viewdoc.jsp`, which can be reviewed for vulnerabilities that may be difficult to find by making blind requests to the executable page. While this threat obviously applies to scripted languages, such as Perl, PHP, ASP, shell scripts, JSP, etc., it is not limited to them, as shown in the example provided in the next bullet.
- Backup archives may contain copies of all files within (or even outside) the webroot. This allows an attacker to quickly enumerate the entire application, including unreferenced pages, source code, include files, etc. For example, if you forget a file named `myservlets.jar.old` file containing (a backup copy of) your servlet implementation classes, you are exposing a lot of sensitive information which is susceptible to decompilation and reverse engineering.
- In some cases copying or editing a file does not modify the file extension, but modifies the filename. This happens for example in Windows environments, where file copying operations generate filenames prefixed with "Copy of " or localized versions of this string. Since the file extension is left unchanged, this is not a case where an executable file is returned as plain text by the web server, and therefore not a case of source code disclosure. However, these files too are dangerous because there is a chance that they include obsolete and incorrect logic that, when invoked, could trigger application errors, which might yield valuable information to an attacker, if diagnostic message display is enabled.
- Log files may contain sensitive information about the activities of application users, for example sensitive data passed in URL parameters, session IDs, URLs visited (which may disclose additional unreferenced content), etc. Other log files (e.g. ftp logs) may contain sensitive information about the maintenance of the application by system administrators.
- File system snapshots may contain copies of the code that contain vulnerabilities that have been fixed in more recent versions. For example `/.snapshot/monthly.1/view.php` may contain a directory traversal vulnerability that has been fixed in `/view.php` but can still be exploited by anyone who finds the old version.

## Test Objectives

- Find and analyse unreferenced files that might contain sensitive information.

## How to Test

### Black-Box Testing

Testing for unreferenced files uses both automated and manual techniques, and typically involves a combination of the following:

#### Inference from the Naming Scheme Used for Published Content

Enumerate all of the application’s pages and functionality. This can be done manually using a browser, or using an application spidering tool. Most applications use a recognizable naming scheme, and organize resources into pages and directories using words that describe their function. From the naming scheme used for published content, it is often possible to infer the name and location of unreferenced pages. For example, if a page `viewuser.asp` is found, then look also for `edituser.asp`, `adduser.asp` and `deleteuser.asp`. If a directory `/app/user` is found, then look also for `/app/admin` and `/app/manager`.

#### Other Clues in Published Content

Many web applications leave clues in published content that can lead to the discovery of hidden pages and functionality. These clues often appear in the source code of HTML and JavaScript files. The source code for all published content should be manually reviewed to identify clues about other pages and functionality. For example:

Programmers' comments and commented-out sections of source code may refer to hidden content:

```html
<!-- <A HREF="uploadfile.jsp">Upload a document to the server</A> -->
<!-- Link removed while bugs in uploadfile.jsp are fixed          -->
```

JavaScript may contain page links that are only rendered within the user’s GUI under certain circumstances:

```javascript
var adminUser=false;
if (adminUser) menu.add (new menuItem ("Maintain users", "/admin/useradmin.jsp"));
```

HTML pages may contain FORMs that have been hidden by disabling the SUBMIT element:

```html
<form action="forgotPassword.jsp" method="post">
    <input type="hidden" name="userID" value="123">
    <!-- <input type="submit" value="Forgot Password"> -->
</form>
```

Another source of clues about unreferenced directories is the `/robots.txt` file used to provide instructions to web robots:

```html
User-agent: *
Disallow: /Admin
Disallow: /uploads
Disallow: /backup
Disallow: /~jbloggs
Disallow: /include
```

#### Blind Guessing

In its simplest form, this involves running a list of common filenames through a request engine in an attempt to guess files and directories that exist on the server. The following netcat wrapper script will read a wordlist from stdin and perform a basic guessing attack:

```bash
#!/bin/bash

server=example.org
port=80

while read url
do
echo -ne "$url\t"
echo -e "GET /$url HTTP/1.0\nHost: $server\n" | netcat $server $port | head -1
done | tee outputfile
```

Depending upon the server, GET may be replaced with HEAD for faster results. The output file specified can be grepped for "interesting" response codes. The response code 200 (OK) usually indicates that a valid resource has been found (provided the server does not deliver a custom "not found" page using the 200 code). But also look out for 301 (Moved), 302 (Found), 401 (Unauthorized), 403 (Forbidden) and 500 (Internal error), which may also indicate resources or directories that are worthy of further investigation.

The basic guessing attack should be run against the webroot, and also against all directories that have been identified through other enumeration techniques. More advanced/effective guessing attacks can be performed as follows:

- Identify the file extensions in use within known areas of the application (e.g. jsp, aspx, html), and use a basic wordlist appended with each of these extensions (or use a longer list of common extensions if resources permit).
- For each file identified through other enumeration techniques, create a custom wordlist derived from that filename. Get a list of common file extensions (including ~, bak, txt, src, dev, old, inc, orig, copy, tmp, swp, etc.) and use each extension before, after, and instead of, the extension of the actual filename.

Note: Windows file copying operations generate filenames prefixed with "Copy of " or localized versions of this string, hence they do not change file extensions. While "Copy of " files typically do not disclose source code when accessed, they might yield valuable information in case they cause errors when invoked.

#### Information Obtained Through Server Vulnerabilities and Misconfiguration

The most obvious way in which a misconfigured server may disclose unreferenced pages is through directory listing. Request all enumerated directories to identify any which provide a directory listing.

Numerous vulnerabilities have been found in individual web servers which allow an attacker to enumerate unreferenced content, for example:

- Apache ?M=D directory listing vulnerability.
- Various IIS script source disclosure vulnerabilities.
- IIS WebDAV directory listing vulnerabilities.

#### Use of Publicly Available Information

Pages and functionality in Internet-facing web applications that are not referenced from within the application itself may be referenced from other public domain sources. There are various sources of these references:

- Pages that used to be referenced may still appear in the archives of Internet search engines. For example, `1998results.asp` may no longer be linked from a company’s website, but may remain on the server and in search engine databases. This old script may contain vulnerabilities that could be used to compromise the entire site. The `site:` Google search operator may be used to run a query only against the domain of choice, such as in: `site:www.example.com`. Using search engines in this way has lead to a broad array of techniques which you may find useful and that are described in the `Google Hacking` section of this Guide. Check it to hone your testing skills via Google. Backup files are not likely to be referenced by any other files and therefore may have not been indexed by Google, but if they lie in browsable directories the search engine might know about them.
- In addition, Google and Yahoo keep cached versions of pages found by their robots. Even if `1998results.asp` has been removed from the target server, a version of its output may still be stored by these search engines. The cached version may contain references to, or clues about, additional hidden content that still remains on the server.
- Content that is not referenced from within a target application may be linked to by third-party websites. For example, an application which processes online payments on behalf of third-party traders may contain a variety of bespoke functionality which can (normally) only be found by following links within the web sites of its customers.

#### Filename Filter Bypass

Because deny list filters are based on regular expressions, one can sometimes take advantage of obscure OS filename expansion features in which work in ways the developer didn't expect. The tester can sometimes exploit differences in ways that filenames are parsed by the application, web server, and underlying OS and it's filename conventions.

Example: Windows 8.3 filename expansion `c:\\program files` becomes `C:\\PROGRA\~1`

- Remove incompatible characters
- Convert spaces to underscores
- Take the first six characters of the basename
- Add `~<digit>` which is used to distinguish files with names using the same six initial characters
- This convention changes after the first 3 cname ollisions
- Truncate  file extension to three characters
- Make all the characters uppercase

### Gray-Box Testing

Performing gray box testing against old and backup files requires examining the files contained in the directories belonging to the set of web directories served by the web server(s) of the web application infrastructure. Theoretically the examination should be performed by hand to be thorough. However, since in most cases copies of files or backup files tend to be created by using the same naming conventions, the search can be easily scripted. For example, editors leave behind backup copies by naming them with a recognizable extension or ending and humans tend to leave behind files with a `.old` or similar predictable extensions. A good strategy is that of periodically scheduling a background job checking for files with extensions likely to identify them as copy or backup files, and performing manual checks as well on a longer time basis.

## Remediation

To guarantee an effective protection strategy, testing should be compounded by a security policy which clearly forbids dangerous practices, such as:

- Editing files in-place on the web server or application server file systems. This is a particularly bad habit, since it is likely to generate backup or temporary files by the editors. It is amazing to see how often this is done, even in large organizations. If you absolutely need to edit files on a production system, do ensure that you don’t leave behind anything which is not explicitly intended, and consider that you are doing it at your own risk.
- Carefully check any other activity performed on file systems exposed by the web server, such as spot administration activities. For example, if you occasionally need to take a snapshot of a couple of directories (which you should not do on a production system), you may be tempted to zip them first. Be careful not to leave behind those archive files.
- Appropriate configuration management policies should help prevent obsolete and un-referenced files.
- Applications should be designed not to create (or rely on) files stored under the web directory trees served by the web server. Data files, log files, configuration files, etc. should be stored in directories not accessible by the web server, to counter the possibility of information disclosure (not to mention data modification if web directory permissions allow writing).
- File system snapshots should not be accessible via the web if the document root is on a file system using this technology. Configure your web server to deny access to such directories, for example under Apache a location directive such this should be used:

```xml
<Location ~ ".snapshot">
    Order deny,allow
    Deny from all
</Location>
```

## Tools

Vulnerability assessment tools tend to include checks to spot web directories having standard names (such as "admin", "test", "backup", etc.), and to report any web directory which allows indexing. If you can’t get any directory listing, you should try to check for likely backup extensions. Check for example

- [Nessus](https://www.tenable.com/products/nessus)
- [Nikto2](https://cirt.net/Nikto2)

Web spider tools

- [wget](https://www.gnu.org/software/wget/)
- [Wget for Windows](http://www.interlog.com/~tcharron/wgetwin.html)
- [Sam Spade](https://web.archive.org/web/20090926061558/http://preview.samspade.org/ssw/download.html)
- [Spike proxy includes a web site crawler function](https://www.spikeproxy.com/)
- [Xenu](http://home.snafu.de/tilman/xenulink.html)
- [curl](https://curl.haxx.se)

Some of them are also included in standard Linux distributions. Web development tools usually include facilities to identify broken links and unreferenced files.
