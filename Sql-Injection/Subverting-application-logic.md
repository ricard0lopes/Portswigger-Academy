
![1](https://user-images.githubusercontent.com/57036558/76717793-9a1c7680-672c-11ea-93ad-faf4bdadbfdf.png)

This lab asks us to exploit a SQL injection vulnerability in the login function. To solve it we need to perfrom an SQL injection attack that logs in to the application as the administrator user.

When entering the application we are given access to a login page that lets us login with a username and password. By submitting the username and password credentials the application performs a SQL query to check them:

```
SELECT * FROM users WHERE username = 'username' AND password = 'password'
```

For the query to be successful it has to return the details of a user.

Again, we can use the comment sequence `--` to remove the password check from the `WHERE` clause in the query, while submitting the username `administrator` and log in to the application as the administrator user.

This is what we trying to achieve:

```
SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
```

To perform this attack we use Burp Suite. By intercepting the request, we can see `username` and `password`with some random credentials as parameters used to login:

![2](https://user-images.githubusercontent.com/57036558/76718385-883bd300-672e-11ea-8bac-25c75c306767.png)

If this login went forward it would be rejected, since the credentials used wouldn't match the details of a user. To log in as the administrator, we just need to use the technique described above and change the username parameter to `administrator'--` and ignore that password check in the query:

![2-2](https://user-images.githubusercontent.com/57036558/76719115-b3bfbd00-6730-11ea-8b6d-7597a9060393.png)

Forwarding the edited request will log us as administrator:

![3](https://user-images.githubusercontent.com/57036558/76719165-d651d600-6730-11ea-87b0-57c66da2f52b.png)


