## Unprotected-functionality

![2](https://user-images.githubusercontent.com/57036558/77707404-eda88300-6fbc-11ea-89b8-696ae6c6fcd5.png)

In this lab we need to delete the user `carlos`.

Vertical privilege escalation arises where an application does not enforce any protection over sensitive functionality. Administrative functions linked from an administrator's welcome page might not be linked from a user's welcome page, but a user might simply be able to access the administrative functions by browsing directly to the relevant admin URL. In some cases, the administrative URL might be discoles in other locations, such as the `robots.txt` file.

To solve this lab we just need to access the `robots.txt` file:

```
User-agent: *
Disallow: /administrator-panel
```

Then, we just need to browse the `/administrator-panel` subdirectory and use the administrator functionalities to delete the user `carlos`.


![3](https://user-images.githubusercontent.com/57036558/77707985-b0dd8b80-6fbe-11ea-8d21-04e184bb53a5.png)

In this lab we have to delete the user `carlos`, like the previous one.

In some cases, sensitive functionality is concealed by giving it a less predictable URL. This might not be directly guessable by an attacker, but the application might still leak the URL to users in JavaScript that constructs the user interface based on the user's role.

To solve the lab we just need to read the source code of the page and find the administrative function's directory:

```
var isAdmin = false;
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-8cbwxt');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
}
```

Then we just need to add `/admin-8cbwxt` to the URL and delete the user `carlos`.

## Parameter-based access control methods

![4](https://user-images.githubusercontent.com/57036558/77709449-f603bc80-6fc2-11ea-9fd6-230984df9b98.png)

Again to solve both labs we need to delete the user `carlos`.

In the first lab we just need to log in the application, then navigate to the `/admin` directory and intercept the request to change the value `admin=false` to `admin=true`.
In the second you, we login and then go to my account to change the user's email. In the response body we see the `roleid` parameter. All we have to do it add `"roleid":2` to the JSON in the request body and we have access to the admin functionality.
