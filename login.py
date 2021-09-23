#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
username = ''
result = ''
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        result = '<p>User name and password are required</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('cs1.ucc.ie', 'cjb4', 'ohchu', 'cs6503_cs1106_cjb4')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users
                              WHERE username = %s
                              AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                result = '<p>Incorrect user name or password</p>'
            else:
                cookie = SimpleCookie()
                cfgof_sid = sha256(repr(time()).encode()).hexdigest()
                cookie['cfgof_sid'] = cfgof_sid
                session_store = open('users/sess_' + cfgof_sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result = """
                   <script>
                     window.location.assign("home.py");
                   </script>
                  """
                print(cookie)
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type: text/html')
print()


print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>CFGOF Login</title>
            <link rel = "stylesheet" href = "styles/games.css" />
        </head>
        <body>
            <header>
                <h1>Conor's Fun Games of Fun!</h1>
            </header>
            <main id = "login_reg">
                <h1>Login</h1>
                <p>Please enter your username and password.</p>
                <form action="login.py" method="post">
                    <input type="text" name="username" id="username" value="%s" placeholder="Username" />
                    <br>
                    <input type="password" name="password" id="password" placeholder="Password"/>
                    <br>
                    <input type="submit" value="Login" />
                </form>
                %s
                <img src="media/logo.png" />
                <p>Don't Have an account? Register <a href='register.py'>Here</a></p>
            </main>
        </body>
    </html>""" % (username, result)
)
