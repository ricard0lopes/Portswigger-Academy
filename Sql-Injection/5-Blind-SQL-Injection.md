<h1>Blind SQL injection</h1>


![2](https://user-images.githubusercontent.com/57036558/77020713-92531100-697c-11ea-8517-757ac170ded8.png)


When the HTTP responses do not contain the results of the relevant SQL query or the detail of any database errors doesn't mean that there isn't an SQL injection Vulnerability. Blind SQL injection is the process of access unauthorized data using different techniques than the ones seen before (many techniques such as UNION attacks are not effective while performing blind SQL injection)

## Exploiting blind SQL injection by triggering conditional responses

To solve this lab we need to log in as administrator user. We are given the information that the database contains a table called `users`, with columns called `username` and `password`.

In blind SQL injection, we can trigger conditional responses by injecting cookies. This lab contains an application that uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie. Since its a blind SQL injection, the results of the SQL query are not returned, and no error messages displayed, but the application includes a "Welcome back" message in the page if the query returns any rows.

To solve this challenge we use Burp Suite.

The firs step is send the application's request to Burp Intruder and modify the `TrackingId` cookie in order to verify that the "Welcome back" message appears in the response. To do this we need to change the cookie to `TrackingId=x'+OR+1=1--`:

![1](https://user-images.githubusercontent.com/57036558/77020668-6f286180-697c-11ea-8231-fc0a0f058ca5.png)

Then, we change it to `TrackingId=x'+OR+1=2--` which will return as `false` and let us verify that the "Welcome back" message does not appear in the response, to demonstrate that we can test a single boolean condition and infer the result.

![3](https://user-images.githubusercontent.com/57036558/77020881-0db4c280-697d-11ea-88d6-cdcf3748f1a7.png)

Now, we need to confirm that there is a user called administrator. To do that we change the cookie to `TrackingId=x'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'--`:

![4](https://user-images.githubusercontent.com/57036558/77020997-6a17e200-697d-11ea-8def-bb716bd116a7.png)

Next we need to determine how many characters are in the password of the administrator user. To do this we change the cookie to `TrackingId=x'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+length(password)>1--` and send it to burp intruder. Burp intruder will cycle through each position and possible value, testing each one in turn. We clear the default positions and add `1` making it look like §1§. Next, on the payloads tab we select a "Simple list" and add the range 1-9 to the "Payload Options". To be able to tell when we reach the current value of the password lenght, we need to grep each response for the expression "Welcome back". To do that we go to the Options tab and add the value "Welcome back" to the "Grep - Match" section. We can now lauch the attack clicking on "Start attack":

![5](https://user-images.githubusercontent.com/57036558/77022212-e9f37b80-6980-11ea-96ac-b146f81713d2.png)

We can notice by the of the response that it changes once our payload injected the number 6, meaning that the lenght of the password is bigger than 5 but not bigger than 6, therefore it has 6 characters. So now we know the lenght of the password, we need to find the actual characters it contains. To do this we change the cookie to `TrackingId=x'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+substring(password,1,1)='a'--`, change the payload type to "Cluster bomb" and select the first "1" and "a" as the payload markers. Then for the first payload we add a range of 1-6 and for the second from a-z. The rest of the process is like the previous method. We hit "Start attack" and wait for a response to tell us the password characters:

```
password: tyhmpe
```

Now we just need to log in and solve the lab:

![6](https://user-images.githubusercontent.com/57036558/77024341-2e354a80-6986-11ea-8278-5dde548f6ce1.png)

Although Burp Suite is a great tool, the process of finding a password using it took a long time in my opinion. And since I am a lazy guy I decided to write a simple script to solve this lab and perhaps reuse it on later labs:

[Blind SQL injection with conditional responses Python](https://github.com/ricard0lopes/Portswigger-Academy/blob/master/Sql-Injection/tools/blind.py)

## Inducing conditional responses by triggering SQL errors

![7](https://user-images.githubusercontent.com/57036558/77114105-dd742f00-6a23-11ea-9b81-d531c8d31abb.png)

This lab uses again tracking cookies for analytics, and performs an SQL query containing the value of the submitted cookie. We are given the infromation that the database contains a different table called users, with columns called username and password, and that to solve the lab we need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

Supposing that the SQL query does not behave any differently depending on whether the query returns any data, the techniques used before will not work since injecting different Boolean conditions makes no difference to the application's response. In this situation, we need to try to return conditional responses by triggering SQL errors conditionally. By modifying a query to `true`, it will cause a database error, and by modifiying it to `false` will not return any result whatsoever. 

So, to solve this lab, we first need to verify if an error message is received using (`'` or `''` may trigger the error). Then, we need to find which type of database the application is using. To do that we can check the 
[SQL injection cheat sheet](https://github.com/ricard0lopes/Portswigger-Academy/blob/master/Sql-Injection/SQL-injection-cheat-sheet.md) and try the different methods for testing conditional erros or each database. We will know which database is being used when our `false` conditional injection doesn't throw any error and returns the website page. The next step is is to verify the conditonal error using the right database's query injection and to notice how it throws the error only if the condition is `true`.

Now it is time to find if there is a user called administrator. Since this lab is running Oracle as its database we can use the following query (but the process is pretty much the same for other databases, you just need to modify the conditional part of the query):

```
TrackingId='+UNION+SELECT+CASE+WHEN+(username='administrator')+THEN+to_char(1/0)+ELSE+NULL+END+FROM+users--
```

Since the conditional returns an error from the application, it means that there is a user called administrator.
Now the process is basically the same as the lab before: finding the length of administrator's password, then find the characters of the password one by one. 

To solve this lab I decided to create my own script using Burp Suite to debug my requests. You can check the script [Python automated lab](https://github.com/ricard0lopes/Portswigger-Academy/blob/master/Sql-Injection/tools/blind2.py) and use or change it as you wish. 
