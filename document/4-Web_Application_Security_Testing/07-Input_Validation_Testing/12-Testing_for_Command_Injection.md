# Testing for Command Injection

|ID          |
|------------|
|WSTG-INPV-12|

## Summary

This article describes how to test an application for OS command injection. The tester will try to inject an OS command through an HTTP request to the application.

OS command injection is a vulnerability that occurs when user input is directly passed to an operating system command without proper validation or sanitization. This allows the user to inject and execute arbitrary commands on the server which can lead to unauthorized data access, data corruption, and full server compromise. This vulnerability can be prevented by emphasizing security during the design and development of applications.

## Test Objectives

- Identify and assess command injection points.
- Bypass special characters and OS commands filter.

## How to Test

When viewing a file in a web application, the filename is often shown in the URL. Perl allows piping data from a process into an open statement. The user can simply append the Pipe symbol `|` onto the end of the filename.

Example URL before alteration:

`https://sensitive/cgi-bin/userData.pl?doc=user1.txt`

Example URL modified:

`https://sensitive/cgi-bin/userData.pl?doc=/bin/ls|`

This will execute the command `/bin/ls`.

Appending a semicolon to the end of a URL for a .PHP page followed by an operating system command, will execute the command. `%3B` is URL encoded and decodes to semicolon

Example:

`https://sensitive/something.php?dir=%3Bcat%20/etc/passwd`

### Example

Consider the case of an application that contains a set of documents that you can browse from the internet. If you fire up a personal proxy (such as ZAP or Burp Suite), you can obtain a POST HTTP like the following (`https://www.example.com/public/doc`):

```txt
POST /public/doc HTTP/1.1
Host: www.example.com
[...]
Referer: https://127.0.0.1/WebGoat/attack?Screen=20
Cookie: JSESSIONID=295500AD2AAEEBEDC9DB86E34F24A0A5
Authorization: Basic T2Vbc1Q9Z3V2Tc3e=
Content-Type: application/x-www-form-urlencoded
Content-length: 33

Doc=Doc1.pdf
```

In this post request, we notice how the application retrieves the public documentation. Now we can test if it is possible to add an operating system command to inject in the POST HTTP. Try the following (`https://www.example.com/public/doc`):

```txt
POST /public/doc HTTP/1.1
Host: www.example.com
[...]
Referer: https://127.0.0.1/WebGoat/attack?Screen=20
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

## Special Characters for Command Injection

Special characters are used to chain multiple commands together.
These characters will vary based on the operating system running on the web server.
For instance, the following types of command chaining can be used on both Windows and Unix-based systems :

- `cmd1|cmd2` : cmd2 will be executed whether cmd1 succeeds or not.
- `cmd1||cmd2` : cmd2 will only be executed if cmd1 fails.
- `cmd1&&cmd2` : cmd2 will only be executed if cmd1 succeeds.
- `cmd1&cmd2` : cmd2 will be executed whether cmd1 succeeds or not.  

Note that, `;` will work on Unix-based systems and PowerShell. However, it will not work on Windows Command Prompt (CMD).  
Furthermore, you can use Bash command substitution `$(cmd)` or &grave;`cmd`&grave; to execute commands on Unix-based systems.  
Additionally, Linux file descriptors such as `>(cmd)`, `<(cmd)` can also be used.

## Filter Evasion

To prevent OS command injection, web developers often use filters. However, these filters are sometimes not properly implemented which allows attackers to bypass them.
In this section, we will cover different techniques used to bypass those filters.

### Methodology

First of all, it is always good practice to have a basic understanding of how the filter works before trying to bypass it.
Here is a methodology we can use when we come across a filter:

- Is the filter client-side or server-side ?
- Is the filter applied on special characters, OS commands, or both ?
- Is the webapp using a allowlist or blocklist filter ?
- What OS is running on the web server? This allows us to have an idea of the commands and special characters we can use.

### Special Characters Filter Evasion

As previously mentionned, filters can either be applied on special characters, OS commands or both.
To bypass filters applied on special characters, we can use environment variables, Bash brace expansion or URL encoding.

#### URL Encoding

URL encoding special characters can allow us to bypass the filter if the web server only blocks the plaintext special characters.
Here are some special characters with their URL encoded format:

|Special Character|URL Encoding|
|-----------------|------------|
|;                | %3b        |
|space            | %20        |
|tab              | %09        |
|&                | %26        |
|New line         | %0a        |

For instance, instead of using `;whoami`, we could use `%3bwhoami`.

#### Environment Variables

Special characters like space, semi-colon, tab, or new line will generally be filtered by the web server especially if they are not useful for the specified input.  
To escape this restriction, we can use environment variables such as **IFS**, **PATH** or **LS_COLORS** on Linux, and **HOMEPATH** on Windows.  
For instance, on Linux, `/`, `;`, and `[space]` can be replaced respectively with `${PATH:0:1}`, `${LS_COLORS:10:1}`, and `${IFS}`.  
On Windows CMD, we can replace `\` with `%HOMEPATH:~6,1%`, or use `$env:HOMEPATH[0]` in PowerShell.

#### Bash Brace Expansion

Bash brace expansion is a Bash feature that allows you to execute commands by using curly braces.  
For example, `{ls,-la}` will execute `ls -la` command. This can be extremely useful if the web server is filtering space, new line, or tab characters.  
Let's assume that we want to display the content of '/etc/passwd' file. Thus, instead of using `;cat /etc/passwd`, we can use `;{cat,/etc/passwd}`.
That said, it's important to note that this technique will only work if the web server is using Bash and if characters like `}{/,;` are not filtered.

### Commands Filter Evasion

In this section, we are going to explore some techniques used to bypass filters applied on operating system commands.

#### Case Modification

Case modification is a technique that is used to bypass OS command filters. This will be helpful if the server-side filter is case sensitive.  
For instance, if we notice during our testing that the web server is blocking `;whoami`, we can try to use instead `;WhoAmi`, and see that the server-side filter is only blocking lowercase commands, we will be able to bypass it.  
Note that this technique will generally work on Windows systems.  
On Linux, we will use a technique called **character shifting**. For instance, the command below will translate each uppercase character to its corresponding lowercase character.  

```bash
;$(tr "[A-Z]" "[a-z]"<<<"WhoaMi")
```

#### Character Insertion

Characters like `\`; `$@`, `'` can be inserted into Linux OS commands without affecting the normal execution of the command.  
For example, `who\ami`, `w$@hoami` or `wh'o'ami` will all execute the `whoami` command  

Note that the number of single quotes `'` in the Linux command must be **even**, otherwise you will get an error. If you're using Windows CMD, make sure to use double quotes `"` instead.  
Furthermore, you can also use a caret `^` in CMD commands. For example, `whoa^mi` will execute the `whoami` command. This does not work in PowerShell.

#### Base64 Encoding

In certain scenarios, the web server may filter commands such as `whoami`, `id`, etc.  
Let's suppose that `whoami` is blocked by the web server. Therefore, we cannot use a payload like `;whoami`.  
To bypass this restriction, we will use the base64 encoded format of `whoami` by executing: `echo -n 'whoami' | base64`. This will return `d2hvYW1p`.
After that, we will send the following payload: `;bash<<<$(base64 -d<<< d2hvYW1p)` in the vulnerable parameter. This should then bypass the server-side filter and allow us to achieve remote command execution.

**Finally, note that you may need to combine different special characters and OS command filter evasion techniques to successfully bypass the filters put it place by the web server.**

## Blind Command Injection

Sometimes, we may not be able to see the output from our injected command in the web server's HTTP response. Thus, we will need to find a way to confirm whether or not our injection succeeded. To do that, we can use `HTTP`, `DNS`, or `SMTP` remote servers under our control.  
We can also use **time delay system commands** like `sleep` (Linux), `timeout` (Windows), or network utility like `ping`.  
For instance, we can execute `;sleep(5)` and if the web server waits 5 seconds before sending a response back to us, we can confirm that it is vulnerable to a blind command injection.  
Moreover, we can also **redirect the output of the injected command in the web server's web root**. `;whoami>/var/www/html/poc.txt;`  
After that, we can execute `curl http://website.com/poc.txt`. If we are able to retrieve the file, we can then confirm that the web server is vulnerable to a blind command injection.

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
- `passthru`

## Remediation

### Sanitization

The URL query parameters and form data need to be validated and sanitized to prevent the injection of malicious characters.  
A blocklist of characters is an option but it may be difficult to think of all of the characters to validate against. Also there may be some that were not discovered as of yet.  
A allowlist containing only authorized characters or commands should be created to validate the user input. Characters that were missed, as well as undiscovered threats, should be eliminated by this list.  

General deny list to be included for command injection can be `|` `;` `&` `$` `>` `<` `'` `\` `!` `>>` `#`  

Escape or filter special characters for windows, `(` `)` `<` `>` `&` `*` `‘` `|` `=` `?` `;` `[` `]` `^` `~` `!` `.` `"` `%` `@` `/` `\` `:` `+` `,`  ``` ` ```  

Escape or filter special characters for Linux, `{` `}` `(` `)` `>` `<` `&` `*` `‘` `|` `=` `?` `;` `[` `]` `$` `–` `#` `~` `!` `.` `"` `%`  `/` `\` `:` `+` `,` ``` ` ```  

Moreover, avoid using functions that execute operating system commands in your application unless absolutely necessary. For instance, instead of using `system("cp /path/to/file1.txt /path/to/file2.txt")` to copy a file, you can directly use the php built-in function `copy("cp /path/to/file1.txt, /path/to/file2.txt")` which does exactly the same thing. It's worth noting that other development languages/frameworks generally offer similar built-in functionality.

### Permissions

The web application and its components should be running under strict permissions that do not allow operating system command execution. Try to verify all this information to test from a gray-box testing point of view.

## Tools

- OWASP [WebGoat](https://owasp.org/www-project-webgoat/)
- [Commix](https://github.com/commixproject/commix)
- [Invoke-DOSfuscation](https://github.com/danielbohannon/Invoke-DOSfuscation)
- [Bashfuscator](https://github.com/Bashfuscator/Bashfuscator)

## References

- [CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')](https://cwe.mitre.org/data/definitions/78.html)
- [ENV33-C. Do not call system()](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152177)
