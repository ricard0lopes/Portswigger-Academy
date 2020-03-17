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

Note: Although I'm showing how to solve all the labs using the browser, Burp Suite is a way faster solution, special using Burp Repeater. In this case, it would encode the `#` character automatically, and would have saved me time and frustration trying to understand why the attack wasn't working even after peaking the solutions.

## Listing the contents of the database

![3](https://user-images.githubusercontent.com/57036558/76906208-614edf80-689b-11ea-9703-770413bf96bf.png)


In this lab we are given the information that the application has a login function, and the database contains a table that holds usernames and passwords. To solve it, we need to determine the name of this table and the columns it cointains, then retrieve the contents of the table to obrain the username and password of all users. At the end, we need to login with the administrator credentials to complete the lab.

In most of databases we can use a set of views called information schema which provides information about the database.

We list the tables in the database using `information_schema.tables`, and after the output reveals the tables in it we can use `information_schema.columns` to list the columns in individual tables.

Imagining we have a website vulnerable to SQL injection, and we find out that the database has two columns with both of them displaying data, we can list the tables of the database with the following input:

```
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--
```

After the table names have been revealed on output, we will then list the columns of a specific table. In this example, lets suppose we find the table `users` in the output:

```
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users'-- 
```

Now lets solve the lab, this time with Burp Suite.

First of all we try to find the number of columns:

![4](https://user-images.githubusercontent.com/57036558/76906546-11244d00-689c-11ea-8d8d-5a302f8b2834.png)

Then, after finding out that the website has two columns, which ones display content:

![5](https://user-images.githubusercontent.com/57036558/76906659-5d6f8d00-689c-11ea-98dc-96f17c3ba149.png)

In this case, both of the columns display content. Next step is to list the tables:

![6](https://user-images.githubusercontent.com/57036558/76906784-9e67a180-689c-11ea-9bcc-2ef49c547cf3.png)

The output shows loads of contents, but `users_kodcyi` of them seems the right one to search for the administrator credentials. Now we need to display the columns of this specific table:

![7](https://user-images.githubusercontent.com/57036558/76906990-11711800-689d-11ea-8d83-a8bfbc4fb533.png)

The output shows us two columns named for username and password: `username_gpwxfn` and `password_pnivlv`. Now its time to get the administrator credentials:

![8](https://user-images.githubusercontent.com/57036558/76907400-08cd1180-689e-11ea-9e30-d43594959cc6.png)

Now we've got the administrator credentials:

![9](https://user-images.githubusercontent.com/57036558/76907471-331ecf00-689e-11ea-9d48-3d977d172012.png)

## Equivalent to information scheman on Oracle

![10](https://user-images.githubusercontent.com/57036558/76908410-7f6b0e80-68a0-11ea-9f61-3dd4520ef43a.png)

For this lab we have to do pretty much the same as the previous one, but on an Oracle database.

Instead of `information_schema.tables` and `information_schema.columns` oracle uses the querie `all_tables` to list all tables and `all_tab_columns` to list all columns. Also, as mentioned earlier, every SELECT statement on Oracle must specify a table to select from, and has a built-in table called DUAL.

First step is to list the number of columns in the database:

![11](https://user-images.githubusercontent.com/57036558/76908611-0ae49f80-68a1-11ea-9770-a1b63e92649b.png)

This database also has two columns, like the previous one, and both display content so I am going to skip the check for contet display and proceed to the next phase that is listing the tables:

![12](https://user-images.githubusercontent.com/57036558/76908779-729aea80-68a1-11ea-93f1-9863758da99e.png)

After the tables being listed we find the table `USERS_AMEKVV`. Now its time to find its columns:

![13](https://user-images.githubusercontent.com/57036558/76908912-c9082900-68a1-11ea-990a-aa2444e61638.png)

The table displayed two columns named `USERNAME_ZXLXHR` and `PASSWORD_BCUGZO`, now we can try to find the administrator credentials:

![14](https://user-images.githubusercontent.com/57036558/76909050-1be1e080-68a2-11ea-86ac-17e2e0c5c400.png)

Administrator credentials found:

![15](https://user-images.githubusercontent.com/57036558/76909144-577caa80-68a2-11ea-9982-b7d4e09674d0.png)

