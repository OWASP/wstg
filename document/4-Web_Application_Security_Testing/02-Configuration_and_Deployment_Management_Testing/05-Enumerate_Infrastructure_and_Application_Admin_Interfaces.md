# Enumerate Infrastructure and Application Admin Interfaces

|ID          |
|------------|
|WSTG-CONF-05|

## Summary

Administrator interfaces may be present in the application or on the application server to allow certain users to undertake privileged activities on the site. Tests should be undertaken to reveal if and how this privileged functionality can be accessed by an unauthorized or standard user.

An application may require an administrator interface to enable a privileged user to access functionality that may make changes to how the site functions. Such changes may include:

- user account provisioning
- site design and layout
- data manipulation
- configuration changes

In many instances, such interfaces do not have sufficient controls to protect them from unauthorized access. Testing is aimed at discovering these administrator interfaces and accessing functionality intended for the privileged users.

## Test Objectives

- Identify hidden administrator interfaces and functionality.

## How to Test

### Black-Box Testing

The following section describes vectors that may be used to test for the presence of administrative interfaces. These techniques may also be used to test for related issues including privilege escalation, and are described elsewhere in this guide(for example [Testing for bypassing authorization schema](../05-Authorization_Testing/02-Testing_for_Bypassing_Authorization_Schema.md) and [Testing for Insecure Direct Object References](../05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md) in greater detail.

- Directory and file enumeration. An administrative interface may be present but not visibly available to the tester. Attempting to guess the path of the administrative interface may be as simple as requesting: */admin or /administrator etc..* or in some scenarios can be revealed within seconds using [Google dorks](https://www.exploit-db.com/google-hacking-database).
- There are many tools available to perform brute forcing of server contents, see the tools section below for more information. A tester may have to also identify the filename of the administration page. Forcibly browsing to the identified page may provide access to the interface.
- Comments and links in source code. Many sites use common code that is loaded for all site users. By examining all source sent to the client, links to administrator functionality may be discovered and should be investigated.
- Reviewing server and application documentation. If the application server or application is deployed in its default configuration it may be possible to access the administration interface using information described in configuration or help documentation. Default password lists should be consulted if an administrative interface is found and credentials are required.
- Publicly available information. Many applications such as WordPress have default administrative interfaces .
- Alternative server port. Administration interfaces may be seen on a different port on the host than the main application. For example, Apache Tomcat's Administration interface can often be seen on port 8080.
- Parameter tampering. A GET or POST parameter or a cookie variable may be required to enable the administrator functionality. Clues to this include the presence of hidden fields such as:

```html
<input type="hidden" name="admin" value="no">
```

or in a cookie:

`Cookie: session_cookie; useradmin=0`

Once an administrative interface has been discovered, a combination of the above techniques may be used to attempt to bypass authentication. If this fails, the tester may wish to attempt a brute force attack. In such an instance the tester should be aware of the potential for administrative account lockout if such functionality is present.

### Gray-Box Testing

A more detailed examination of the server and application components should be undertaken to ensure hardening (i.e. administrator pages are not accessible to everyone through the use of IP filtering or other controls), and where applicable, verification that all components do not use default credentials or configurations.
Source code should be reviewed to ensure that the authorization and authentication model ensures clear separation of duties between normal users and site administrators. User interface functions shared between normal and administrator users should be reviewed to ensure clear separation between the drawing of such components and information leakage from such shared functionality.

Each web framework may have its own admin default pages or path. For example

WebSphere:

```html
/admin
/admin-authz.xml
/admin.conf
/admin.passwd
/admin/*
/admin/logon.jsp
/admin/secure/logon.jsp
```

PHP:

```html
/phpinfo
/phpmyadmin/
/phpMyAdmin/
/mysqladmin/
/MySQLadmin
/MySQLAdmin
/login.php
/logon.php
/xmlrpc.php
/dbadmin
```

FrontPage:

```html
/admin.dll
/admin.exe
/administrators.pwd
/author.dll
/author.exe
/author.log
/authors.pwd
/cgi-bin
```

WebLogic:

```html
/AdminCaptureRootCA
/AdminClients
/AdminConnections
/AdminEvents
/AdminJDBC
/AdminLicense
/AdminMain
/AdminProps
/AdminRealm
/AdminThreads
```

WordPress:

```html
wp-admin/
wp-admin/about.php
wp-admin/admin-ajax.php
wp-admin/admin-db.php
wp-admin/admin-footer.php
wp-admin/admin-functions.php
wp-admin/admin-header.php
```

## Tools

- [OWASP ZAP - Forced Browse](https://www.zaproxy.org/docs/desktop/addons/forced-browse/) is a currently maintained use of OWASP's previous DirBuster project.
- [THC-HYDRA](https://github.com/vanhauser-thc/thc-hydra) is a tool that allows brute-forcing of many interfaces, including form-based HTTP authentication.
- A brute forcer is much better when it uses a good dictionary, for example the [netsparker](https://www.netsparker.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/) dictionary.

## References

- [Cirt: Default Password list](https://cirt.net/passwords)
- [FuzzDB can be used to do brute force browsing admin login path](https://github.com/fuzzdb-project/fuzzdb/blob/master/discovery/predictable-filepaths/login-file-locations/Logins.txt)
- [Common admin or debugging parameters](https://github.com/fuzzdb-project/fuzzdb/blob/master/attack/business-logic/CommonDebugParamNames.txt)
