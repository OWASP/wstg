# Test File Extensions Handling for Sensitive Information

|ID          |
|------------|
|WSTG-CONF-03|

## Summary

File extensions are commonly used in web servers to easily determine which technologies, languages and plugins must be used to fulfill the web request. While this behavior is consistent with RFCs and Web Standards, using standard file extensions provides the penetration tester useful information about the underlying technologies used in a web appliance and greatly simplifies the task of determining the attack scenario to be used on particular technologies. In addition, mis-configuration of web servers could easily reveal confidential information about access credentials.

Extension checking is often used to validate files to be uploaded, which can lead to unexpected results because the content is not what is expected, or because of unexpected OS filename handling.

Determining how web servers handle requests corresponding to files having different extensions may help in understanding web server behavior depending on the kind of files that are accessed. For example, it can help to understand which file extensions are returned as text or plain versus those that cause server-side execution. The latter are indicative of technologies, languages or plugins that are used by web servers or application servers, and may provide additional insight on how the web application is engineered. For example, a ".pl" extension is usually associated with server-side Perl support. However, the file extension alone may be deceptive and not fully conclusive. For example, Perl server-side resources might be renamed to conceal the fact that they are indeed Perl related. See the next section on "web server components" for more on identifying server-side technologies and components.

## Test Objectives

- Dirbust sensitive file extensions, or extensions that might contain raw data (*e.g.* scripts, raw data, credentials, etc.).
- Validate that no system framework bypasses exist on the rules set.

## How to Test

### Forced Browsing

Submit requests with different file extensions and verify how they are handled. The verification should be on a per web directory basis. Verify directories that allow script execution. Web server directories can be identified by scanning tools which look for the presence of well-known directories. In addition, mirroring the web site structure allows the tester to reconstruct the tree of web directories served by the application.

If the web application architecture is load-balanced, it is important to assess all of the web servers. This may or may not be easy, depending on the configuration of the balancing infrastructure. In an infrastructure with redundant components there may be slight variations in the configuration of individual web or application servers. This may happen if the web architecture employs heterogeneous technologies (think of a set of IIS and Apache web servers in a load-balancing configuration, which may introduce slight asymmetric behavior between them, and possibly different vulnerabilities).

#### Example

The tester has identified the existence of a file named `connection.inc`. Trying to access it directly gives back its contents, which are:

```php
<?
    mysql_connect("127.0.0.1", "root", "password")
        or die("Could not connect");
?>
```

The tester determines the existence of a MySQL DBMS back end, and the (weak) credentials used by the web application to access it.

The following file extensions should never be returned by a web server, since they are related to files which may contain sensitive information or to files for which there is no reason to be served.

- `.asa`
- `.inc`
- `.config`

The following file extensions are related to files which, when accessed, are either displayed or downloaded by the browser. Therefore, files with these extensions must be checked to verify that they are indeed supposed to be served (and are not leftovers), and that they do not contain sensitive information.

- `.zip`, `.tar`, `.gz`, `.tgz`, `.rar`, etc.: (Compressed) archive files
- `.java`: No reason to provide access to Java source files
- `.txt`: Text files
- `.pdf`: PDF documents
- `.docx`, `.rtf`, `.xlsx`, `.pptx`, etc.: Office documents
- `.bak`, `.old` and other extensions indicative of backup files (for example: `~` for Emacs backup files)

The list given above details only a few examples, since file extensions are too many to be comprehensively treated here. Refer to [FILExt](https://filext.com/) for a more thorough database of extensions.

To identify files having a given extensions a mix of techniques can be employed. These techniques can include Vulnerability Scanners, spidering and mirroring tools, manually inspecting the application (this overcomes limitations in automatic spidering), querying search engines (see [Testing: Spidering and googling](../01-Information_Gathering/01-Conduct_Search_Engine_Discovery_Reconnaissance_for_Information_Leakage.md)). See also [Testing for Old, Backup and Unreferenced Files](04-Review_Old_Backup_and_Unreferenced_Files_for_Sensitive_Information.md) which deals with the security issues related to "forgotten" files.

### File Upload

Windows 8.3 legacy file handling can sometimes be used to defeat file upload filters.

Usage Examples:

1. `file.phtml` gets processed as PHP code.
2. `FILE~1.PHT` is served, but not processed by the PHP ISAPI handler.
3. `shell.phPWND` can be uploaded.
4. `SHELL~1.PHP` will be expanded and returned by the OS shell, then processed by the PHP ISAPI handler.

### Gray-Box Testing

Performing white-box testing against file extensions handling amounts to checking the configurations of web servers or application servers taking part in the web application architecture, and verifying how they are instructed to serve different file extensions.

If the web application relies on a load-balanced, heterogeneous infrastructure, determine whether this may introduce different behavior.

## Tools

Vulnerability scanners, such as Nessus and Nikto check for the existence of well-known web directories. They may allow the tester to download the web site structure, which is helpful when trying to determine the configuration of web directories and how individual file extensions are served. Other tools that can be used for this purpose include:

- [wget](https://www.gnu.org/software/wget)
- [curl](https://curl.haxx.se)
- google for "web mirroring tools".
