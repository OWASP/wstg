# Testing for MS Access

## Summary

As explained in the generic [SQL injection](https://owasp.org/www-community/attacks/SQL_Injection) section, SQL injection vulnerabilities occur whenever user-supplied input is used during the construction of a SQL query without being adequately constrained or sanitized. This class of vulnerabilities allows an attacker to execute SQL code under the privileges of the user that is used to connect to the database. In this section, relevant SQL injection techniques that utilize specific features of [Microsoft Access](https://en.wikipedia.org/wiki/Microsoft_Access) will be discussed.

## How to Test

### Fingerprinting

Fingerprinting the specific database technology while testing SQL-powered application is the first step to properly asses potential vulnerabilities. A common approach involves injecting standard SQL injection attack patterns (e.g. single quote, double quote, ...) in order to trigger database exceptions. Assuming that the application does not handle exceptions with custom pages, it is possible to fingerprint the underline DBMS by observing error messages.

Depending on the specific web technology used, MS Access driven applications will respond with one of the following errors:

`Fatal error: Uncaught exception 'com_exception' with message Source: Microsoft JET Database Engine`

or

`Microsoft JET Database Engine error '80040e14'`

or

`Microsoft Office Access Database Engine`

In all cases, we have a confirmation that we're testing an application using MS Access database.

### Basic Testing

Unfortunately, MS Access doesn't support typical operators that are traditionally used during SQL injection testing, including:

- No comments characters
- No stacked queries
- No LIMIT operator
- No SLEEP or BENCHMARK alike operators
- and many others

Nevertheless, it is possible to emulate those functions by combining multiple operators or by using alternative techniques. As mentioned, it is not possible to use the trick of inserting the characters `/*`, `--` or `#` in order to truncate the query. However, we can fortunately bypass this limitation by injecting a 'null' character. Using a null byte `%00` within a SQL query results in MS Access ignoring all remaining characters. This can be explained by considering that all strings are NULL terminated in the internal representation used by the database. It is worth mentioning that the `null` character can sometimes cause troubles too as it may truncate strings at the web server level. In those situations, we can however employ another character: `0x16` (`%16` in URL encoded format).

Considering the following query:

`SELECT [username],[password] FROM users WHERE [username]='$myUsername' AND [password]='$myPassword'`

We can truncate the query with the following two URLs:

- `http://www.example.com/page.asp?user=admin'%00&pass=foo`
- `http://www.example.com/page.app?user=admin'%16&pass=foo`

The `LIMIT` operator is not implemented in MS Access, however it is possible to limit the number of results by using the `TOP` or `LAST` operators instead.

`http://www.example.com/page.app?id=2'+UNION+SELECT+TOP+3+name+FROM+appsTable%00`

By combining both operators, it is possible to select specific results. String concatenation is possible by using `& (%26)` and `+ (%2b)` characters.

There are also many other functions that can be used while testing SQL injection, including but not limited to:

- ASC: Obtain the ASCII value of a character passed as input
- CHR: Obtain the character of the ASCII value passed as input
- LEN: Return the length of the string passed as parameter
- IIF: Is the IF construct, for example the following statement `IIF(1=1, 'a', 'b')` return `a`
- MID: This function allows you to extract substring, for example the following statement `mid('abc',1,1)` return `a`
- TOP: This function allows you to specify the maximum number of results that the query should return from the top. For example `TOP 1` will return only 1 row.
- LAST: This function is used to select only the last row of a set of rows. For example the following query `SELECT last(*)` FROM users will return only the last row of the result.

Some of these operators are essential to exploit blind SQL injections. For other advanced operators, please refer to the documents in the references.

#### Attributes Enumeration

In order to enumerate the column of a database table, it is possible to use a common error-based technique. In short, we can obtain the attributes name by analyzing error messages and repeating the query with different selectors. For example, assuming that we know the existence of a column, we can also obtain the name of the remaining attributes with the following query:

`' GROUP BY Id%00`

In the error message received, it is possible to observe the name of the next column. At this point, we can iterate the method until we obtain the name of all attributes. If we don't know the name of the first attribute, we can still insert a fictitious column name and obtain the name of the first attribute within the error message.

#### Obtaining Database Schema

Various system tables exist by default in MS Access that can be potentially used to obtain table names and columns. Unfortunately, in the default configuration of recent MS Access database releases, these tables are not accessible. Nevertheless, it is always worth trying:

- MSysObjects
- MSysACEs
- MSysAccessXML

For example, if a union SQL injection vulnerability exists, you can use the following query:

`' UNION SELECT Name FROM MSysObjects WHERE Type = 1%00`

Alternatively, it is always possible to bruteforce the database schema by using a standard wordlist (e.g. [FuzzDb](https://github.com/fuzzdb-project/fuzzdb)).

In some cases, developers or system administrators do not realize that including the actual `.mdb` file within the application webroot can allow to download the entire database. Database filenames can be inferred with the following query:

`http://www.example.com/page.app?id=1'+UNION+SELECT+1+FROM+name.table%00`

where `name` is the `.mdb` filename and `table` is a valid database table. In case of password protected databases, multiple software utilities can be used to crack the password. Please refer to the references.

### Blind SQL Injection Testing

[Blind SQL Injection](https://owasp.org/www-community/attacks/Blind_SQL_Injection) vulnerabilities are by no means the most easily exploitable SQL injections while testing real-life applications. In case of recent versions of MS Access, it is also not feasible to execute shell commands or read/write arbitrary files.

In case of blind SQL injections, the attacker can only infer the result of the query by evaluating time differences or application responses. It is supposed that the reader already knows the theory behind blind SQL injection attacks, as the remaining part of this section will focus on MS Access specific details.

The following example is used:

`http://www.example.com/index.php?myId=[sql]`

where the ID parameter is used within the following query:

`SELECT * FROM orders WHERE [id]=$myId`

Let's consider the `myId` parameter vulnerable to blind SQL injection. As an attacker, we want to extract the content of column `username` in the table `users`, assuming that we have already disclosed the database schema.

A typical query that can be used to infer the first character of the username of the 10th rows is:

`http://www.example.com/index.php?id=IIF((select%20MID(LAST(username),1,1)%20from%20(select%20TOP%2010%20username%20from%20users)='a',0,'no')`

If the first character is `a`, the query will return `0` or otherwise the string `no`.

By using a combination of the `IFF, MID, LAST` and `TOP` functions, it is possible to extract the first character of the username on a specifically selected row. As the inner query returns a set of records, and not just one, it is not possible to use it directly. Fortunately, we can combine multiple functions to extract a specific string.

Let's assume that we want to retrieve the username of the 10th row. First, we can use the TOP function to select the first ten rows using the following query:

`SELECT TOP 10 username FROM users`

Then, using this subset, we can extract the last row by using the LAST function. Once we have only one row and exactly the row containing our string, we can use the IFF, MID and LAST functions to infer the actual value of the username. In our example, we employ IFF to return a number or a string. Using this trick, we can distinguish whether we have a true response or not, by observing application error responses. As `id` is numeric, the comparison with a string results in a SQL error that can be potentially leaked by `500 Internal Server Error pages`. Otherwise, a standard `200 OK` page will be likely returned.

For example, we can have the following query:

`http://www.example.com/index.php?id='%20AND%201=0%20OR%20'a'=IIF((select%20MID(LAST(username),1,1)%20from%20(select%20TOP%2010%20username%20from%20users))='a','a','b')%00`

that is TRUE if the first character is 'a' or false otherwise.

As mentioned, this method allows to infer the value of arbitrary strings within the database:

1. By trying all printable values, until we find a match
2. By inferring the length of the string using the `LEN` function, or by simply stopping after we have found all characters

Time-based blind SQL injections are also possible by abusing [heavy queries](https://docs.microsoft.com/en-us/previous-versions/tn-archive/cc512676(v=technet.10)).

## References

- [MS Access SQL injection cheet sheet](http://nibblesec.org/files/MSAccessSQLi/MSAccessSQLi.html)
- [Access Through Access - Brett Moore](https://packetstormsecurity.com/files/65967/Access-Through-Access.pdf.html)
- [Access SQL Injection - Brett Moore](https://seclists.org/pen-test/2003/May/74)
- [MS Access: Functions](https://www.techonthenet.com/access/functions/index_alpha.php)
- [Microsoft Access - Wikipedia](https://en.wikipedia.org/wiki/Microsoft_Access)
