# Test File Permission

|ID          |
|------------|
|WSTG-CONF-09|

## Summary

When a resource is given a permissions setting that provides access to a wider range of actors than required, it could lead to the exposure of sensitive information, or the modification of that resource by unintended parties. This is especially dangerous when the resource is related to program configuration, execution, or sensitive user data.

A clear example would be an executable file that can be run by unauthorized users. For another example, consider account information or a token value used to access an API. These are increasingly seen in modern web services and microservices, and may be stored in a configuration file that has world-readable permissions by default upon installation. Such sensitive data could be exposed either by malicious internal actors within the host system or by remote attackers. The latter may have compromised the service through other vulnerabilities, while gaining only normal user privileges.

## Test Objectives

- Review and identify any rogue file permissions.

## How to Test

In Linux, use `ls` command to check the file permissions. Alternatively, `namei` can also be used to recursively list file permissions.

`$ namei -l /PathToCheck/`

The files and directories that require file permission testing can include, but are not limited to, the following:

- Web files/directory
- Configuration files/directory
- Sensitive files(encrypted data, password, key)/directory
- Log files(security logs, operation logs, admin logs)/directory
- Executables(scripts, EXE, JAR, class, PHP, ASP)/directory
- Database files/directory
- Temp files/directory
- Upload files/directory

## Remediation

Set the permissions of the files and directories properly so that unauthorized users cannot access critical resources.

## Tools

- [Windows AccessEnum](https://technet.microsoft.com/en-us/sysinternals/accessenum)
- [Windows AccessChk](https://technet.microsoft.com/en-us/sysinternals/accesschk)
- [Linux namei](https://linux.die.net/man/1/namei)

## References

- [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html)
