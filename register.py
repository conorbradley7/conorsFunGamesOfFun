#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
from datetime import date
import pymysql as db

form_data = FieldStorage()
username = ''
result = ''
email = ''
today = date.today().strftime("%Y-%m-%d")
form = """
        <p>I'm glad you decided to join! Please choose a username and password.</p>
        <form action="register.py" method="post">
            <label for="username">Username</label>
            <br>
            <input type="text" name="username" id="username" value="%s" placeholder="Eg: sweet_feet"/>
            <br>
            <label for="email">Email Address</label>
            <br>
            <input type="text" name="email" id="email" value="%s" placeholder="Eg: sweetfeet42@aussiemail.com"/>
            <br>
            <label for="password1">Password</label>
            <br>
            <input type="password" name="password1" id="password1" />
            <br>
            <label for="password2">Confirm Password</label>
            <br>
            <input type="password" name="password2" id="password2" />
            <br>
            <input type="submit" value="Register" />
        </form>
        """ %(username, email)

if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    email = escape(form_data.getfirst('email', '').strip())
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 = escape(form_data.getfirst('password2', '').strip())
    if not username or not password1 or not password2:
        result = '<p>Username and password required.</p>'
    elif password1 != password2:
        result = '<p>Passwords do not match.</p>'
    else:
        try:
            connection = db.connect('cs1.ucc.ie', 'cjb4', 'ohchu', 'cs6503_cs1106_cjb4')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s""", (username))
            if cursor.rowcount > 0:
                result = '<p>Username already taken.</p>'
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, password, email, date_joined, space_invaders, chicken_run)
                                  VALUES (%s, %s, %s, DATE(%s), 0, 0)""", (username, sha256_password, email, today))
                connection.commit()
                cursor.close()
                connection.close()
                cookie = SimpleCookie()
                cfgof_sid = sha256(repr(time()).encode()).hexdigest()
                cookie['cfgof_sid'] = cfgof_sid
                session_store = open('users/sess_' + cfgof_sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                form = ""
                result = """
                   <p>Succesfully registered!</p>
                   <p>Thanks for joining CFGOF. You may now login and enjoy the games I have created!</p>
                   <a href="login.py">Login</a>
                   """
                print(cookie)
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Register For CFGOF </title>
            <link rel = "stylesheet" href = "styles/games.css" />
        </head>
        <body>
            <header>
                <h1>Conor's Fun Games of Fun!</h1>
            </header>
            <main id = "login_reg">
                <h1>Welcome!</h1>
                %s
                %s
                <img src="media/logo.png" />
                <p>Already Have an account? Login <a href='login.py'>Here</a></p>
            </main>
        </body>
    </html>""" % (form, result))
