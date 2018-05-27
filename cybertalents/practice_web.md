### Admin Has The Power

```html
Challenge: Administrators only has the power to see the flag , can you be one ?
```

Enter the website provided in the challenge and you'll be redirected to a login page
View the page source of the webpage by right clicking and selecting 'View Page Source'
You'll find a comment that includes support username and password 

 _TODO: remove this line ,  for maintenance purpose use this inf(user:support password:x34245323)_

Trying to use these credentials would only redirect you to the support page with no flag
Next you want to open up burp suite and intercept your requests
Try logging back in again with the same credentials but this time with proxy intercept on
You'll find that there is a role variable that is set to support, change that to admin and forward your request
After forwarding your request you should see a new webpage that includes the flag (hiadminyouhavethepower)

