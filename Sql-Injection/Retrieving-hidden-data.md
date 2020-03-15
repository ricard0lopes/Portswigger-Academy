
![1](https://user-images.githubusercontent.com/57036558/76711312-c1604d00-6706-11ea-930c-19f769f73079.png)


This lab asks us to perform an SQL injection attack that causes the application to display details of all products in any category, both released and unreleased.

When accessing the website's Food & Drink category we have the following url:

```
web-security-academy.net/filter?category=Food+%26+Drink
```

Which causes the application to make an SQL query to retrieve details of the relevant products from the database:

```
SELECT * FROM products WHERE category = 'Food & Drink' AND release = 1
```

Lets break the syntax:

`SELECT *` -> select all details

`FROM products` -> from the products table

`WHERE category = 'Food & Drink'` -> where the category is Food & Drink

`AND release = 1` -> and release is 1 (1 is being used to show only released products and we presume that 0 would be used to show the unreleased)

We can use the double-dash sequence `--`, interpreted as a comment, to remove the remainder of the query so it no longer includes the `AND released = 1` and displays the all products of the category. Tho, to cause the application to display all the products in any category, we need to return all items where either category is Food & Drink or all of the other categories. To do that we need to create a statement that will evaluate to `true` (1=1 == true) and add the double-dash after it to ignore the rest of the query. 

The modified query will look like this:

```
SELECT * FROM products WHERE category = 'Food & Drink' OR 1=1--' AND release = 1
```

There are two ways to make this attack.

1 - Modifying the URL in the browser:

```
web-security-academy.net/filter?category=Food+%26+Drink'+OR+1=1--'
```

2 - Using Burp Suite to intercept the request and modify the URL:

![2](https://user-images.githubusercontent.com/57036558/76711934-09ce3980-670c-11ea-8af3-1a8122c8a2aa.png)



