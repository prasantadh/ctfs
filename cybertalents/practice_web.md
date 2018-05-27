### Admin Has The Power

```html
Challenge: Administrators only has the power to see the flag , can you be one ?
```

1. Enter the website provided in the challenge and you'll be redirected to a login page.

2. View the page source of the webpage by right clicking and selecting 'View Page Source'.

3. You'll find a comment that includes support username and password. 

   _TODO: remove this line ,  for maintenance purpose use this(user:support password:x34245323)_

4. Trying to use these credentials would only redirect you to the support page with no flag.

5. Next you want to open up burp suite and intercept your requests.

6. Try logging back in again with the same credentials but this time with proxy intercept on.

7. You'll find that there is a role variable that is set to support, change that to admin and forward your request.

8. After forwarding your request you should see a new webpage that includes the flag (hiadminyouhavethepower).



### This Is Sparta

```html
Challenge: Morning has broken today they're fighting in the shade when arrows blocked the sun they fell tonight they dine in hell
```

1. Enter the website provided in the challenge and you'll be redirected to a login page
2. View the page source of the webpage by right clicking and selecting 'View Page Source'
3. In the source code you'll find a script that is encoded in ascii-hex
4. Decoded this using an online decoder such as [this one](http://ddecode.com/hexdecoder/)
5. After decoding it you would get a simplified code that includes an array with multiple variables followed by an if statement
6. Rearrange the decoded script so it's more readable 
7. After doing so, you'll be able to see that the if statement will redirect you to a page if both the first variable and second variable are equal to the 5th value in the array (Cyber-Talent)
8. Input that in both the username and password of the original webpage and you will be redirected to a page with the flag ({J4V4_Scr1Pt_1S_Aw3s0me})

### Share the Ideas

```html
Challenge: can you reveal the admin password ?
```

1. Enter the website provided in the challenge and you'll be redirected to a blogpost like webpage

2. Register a username and password

3. check if sql injection is possible by typing a ' or a - followed by something

4. You will get an error on the top left so we know that it is possible, but we have to find out what type of sql injection are we going to use

5. try finding the sql version used in the webpage by using 			

   ```
   sddffjk' || (select sqlite_version()));--
   ```

6. You'll find that its sqlite so we need to find the tables used so we type in this:

   ```
   sdfjsks' || (SELECT sql FROM sqlite_master));--
   ```

7. Now we know that there's a table called xde43_users which has a password field and a role field
   so we create a query that searches for all passwords with users that have the admin role		

   ```
   adjkasw' || (select password from xde43_users where role="admin"));--
   ```

8. After doing so, a new post will be seen with the flag included (flag245698)

### I Am Legend

```html
Challenge: If I am a legend, then why am I so lonely?
```

1. Enter the website provided in the challenge and you'll be redirected to a login page

2. View the page source of the webpage by right clicking and selecting 'View Page Source'

3. You'll find a script that is obfuscated in a weird format

4. doing some research, I found that it was obfuscated using an encoding called [jsfuck](http://www.jsfuck.com/#)

5. Going to the original decoder website and using their decoder did not work, as I only got "undefined"

6. I searched for different decoders online and found one called [poisonJS](http://ooze.ninja/javascript/poisonjs/) that de-obfuscates eval based jsfuck obfuscations

7. after using the decoder, we get multiple functions including the check function for the username and password

8. In the function, we see an if statement that includes the needed variables for the username and password 

   ```
   (user=="Cyber" && pass=="Talent")
   ```

9. Entering those credentials will redirect you to a page with the Flag: {J4V4_Scr1Pt_1S_S0_D4MN_FUN}




