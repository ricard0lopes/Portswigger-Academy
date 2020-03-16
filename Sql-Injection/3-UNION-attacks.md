<h1>SQL injection UNION attacks</h1>

When we get the confirmation of a possible SQL injecion vulnerability by having the results of the query returned within the application's responses, we can use the `UNION` keyword to retrieve data from other tables within the database.

The UNION keyword lets us execute one or more addictional SELECT queries, appending the results to the original query:

```
SELECT a, b FROM table1 UNION SELECT c, d FROM table2
```

For the UNION query to work, the individual queries must return the same number of columns, and the data types in each columns must be compatible between the individual queries.

To carry out an SQL injection UNION attack, we need to figure out the number of columns returned from the original query, and which of these columns displays data.

## Determining the number of columns required in an SQL injection UNION attack


![1](https://user-images.githubusercontent.com/57036558/76720663-5b3eee80-6735-11ea-9a42-b6a581acfdb8.png)

In this lab we are asked to perform an SQL injection UNION attack that returns an additional row containing null values.

To determine how many columns are being returned from the original query we have two methods: `ORDER BY` and `UNION SELECT NULL--`.

The first method works by incrementing the specified column indext until an error occurs.

For example on the URL:

```
https://web-security-academy.net/filter?category=Corporate+gifts
```

We would do this by adding `' ORDER BY 1--` to the URL, and continue using the method incrementing each time the number of columns. This method is specified by the columns index, so we don't need to know the name of any columns for it to work, and when the specified column index exceeds the number of actual columns the database returns an error (may not even return an error, but we should notice some difference in the application's response when we exceed the database's number of columns index).

Since we are asked to execute an UNION attack containing null values, we will use the second method on this lab.

The second method involves submitting a series of `UNION SELECT` payloads specifying the number of columns with a `NULL` value. 

Example:

```
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
etc. 
```

When the number of nulls matches the number of columns, the database returns an additional row in the results set, containing null values in each column. Until there, the application will keep returning some kind of error message.

We can exploit this vulnerabilty in two ways:

1 - Changing the URL on the browser by adding the `NULL` value until we get the correct number of columns:

```
https://web-security-academy.net/filter?category=Corporate+gifts'+UNION+SELECT+NULL,NULL,NULL--
```

2 - Using Burp Suite by modifying the request with the same method above:

![2](https://user-images.githubusercontent.com/57036558/76721614-837c1c80-6738-11ea-90bf-599b3f01d0aa.png)

In the end we can see that the database has 3 columns, and we solve the lab.

## Finding columns with a useful data type in an SQL injection UNION attack

![3](https://user-images.githubusercontent.com/57036558/76775503-5746b700-679d-11ea-9fed-f8d1f0866e41.png)

In this lab, we are asked to retrieve data from other tables using a UNION attack to find a column containing the value `'FzOyty'`.

The SQL injection UNION attack allows us to retrieve the results from an injected query. To do that, after finding the number of columns in the database, we need to find one or more columns in the original query results whose data type is, or is compatible with, string data (the data we will want to retrieve will be, generally, in string form).

We can use the `UNION SELECT` payload to place a string value into each column in turn, for example, the query in this lab returns three columns, so we will submit:

```
' UNION SELECT 'FzOyty',NULL,NULL--
' UNION SELECT NULL,'FzOyty',NULL--
' UNION SELECT NULL,NULL,'FzOyty'--
```

If an error does not occur, then the column that contains the string value is suitable for retrieving string data. Otherwise, the injected query will cause a database error.

To solve this exercise we can either use Burp Suite to intercept and modify the request, or do it directly in the browser:

```
https://web-security-academy.net/filter?category=Gifts%27+UNION+SELECT+NULL,%27FzOyty%27,NULL--
```

Placing the string in the second column will not result in an error and will display the content on the webpage, this solving the lab.
