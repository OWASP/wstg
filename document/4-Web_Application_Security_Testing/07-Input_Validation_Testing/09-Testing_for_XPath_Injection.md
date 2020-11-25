# Testing for XPath Injection

|ID          |
|------------|
|WSTG-INPV-09|

## Summary

XPath is a language that has been designed and developed primarily to address parts of an XML document. In XPath injection testing, we test if it is possible to inject XPath syntax into a request interpreted by the application, allowing an attacker to execute user-controlled XPath queries. When successfully exploited, this vulnerability may allow an attacker to bypass authentication mechanisms or access information without proper authorization.

Web applications heavily use databases to store and access the data they need for their operations. Historically, relational databases have been by far the most common technology for data storage, but, in the last years, we are witnessing an increasing popularity for databases that organize data using the XML language. Just like relational databases are accessed via SQL language, XML databases use XPath as their standard query language.

Since, from a conceptual point of view, XPath is very similar to SQL in its purpose and applications, an interesting result is that XPath injection attacks follow the same logic as [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) attacks. In some aspects, XPath is even more powerful than standard SQL, as its whole power is already present in its specifications, whereas a large number of the techniques that can be used in a SQL Injection attack depend on the characteristics of the SQL dialect used by the target database. This means that XPath injection attacks can be much more adaptable and ubiquitous. Another advantage of an XPath injection attack is that, unlike SQL, no ACLs are enforced, as our query can access every part of the XML document.

## Test Objectives

- Identify XPATH injection points.

## How to Test

The [XPath attack pattern was first published by Amit Klein](http://dl.packetstormsecurity.net/papers/bypass/Blind_XPath_Injection_20040518.pdf) and is very similar to the usual SQL Injection. In order to get a first grasp of the problem, let's imagine a login page that manages the authentication to an application in which the user must enter their username and password. Let's assume that our database is represented by the following XML file:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<users>
    <user>
        <username>gandalf</username>
        <password>!c3</password>
        <account>admin</account>
    </user>
    <user>
        <username>Stefan0</username>
        <password>w1s3c</password>
        <account>guest</account>
    </user>
    <user>
        <username>tony</username>
        <password>Un6R34kb!e</password>
        <account>guest</account>
    </user>
</users>
```

An XPath query that returns the account whose username is `gandalf` and the password is `!c3` would be the following:

`string(//user[username/text()='gandalf' and password/text()='!c3']/account/text())`

If the application does not properly filter user input, the tester will be able to inject XPath code and interfere with the query result. For instance, the tester could input the following values:

```text
Username: ' or '1' = '1
Password: ' or '1' = '1
```

Looks quite familiar, doesn't it? Using these parameters, the query becomes:

`string(//user[username/text()='' or '1' = '1' and password/text()='' or '1' = '1']/account/text())`

As in a common SQL Injection attack, we have created a query that always evaluates to true, which means that the application will authenticate the user even if a username or a password have not been provided. And as in a common SQL Injection attack, with XPath injection, the first step is to insert a single quote (`'`) in the field to be tested, introducing a syntax error in the query, and to check whether the application returns an error message.

If there is no knowledge about the XML data internal details and if the application does not provide useful error messages that help us reconstruct its internal logic, it is possible to perform a [Blind XPath Injection](https://owasp.org/www-community/attacks/Blind_XPath_Injection) attack, whose goal is to reconstruct the whole data structure. The technique is similar to inference based SQL Injection, as the approach is to inject code that creates a query that returns one bit of information. [Blind XPath Injection](https://owasp.org/www-community/attacks/Blind_XPath_Injection) is explained in more detail by Amit Klein in the referenced paper.

## References

### Whitepapers

- [Amit Klein: "Blind XPath Injection"](http://dl.packetstormsecurity.net/papers/bypass/Blind_XPath_Injection_20040518.pdf)
- [XPath 1.0 specifications](https://www.w3.org/TR/1999/REC-xpath-19991116/)
