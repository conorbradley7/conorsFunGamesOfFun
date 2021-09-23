#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie


result = """
       <p>You do not have permission to access this page. Please Login or Register.</p>
       <ul>
           <li><a href="../register.py">Register</a></li>
           <li><a href="../login.py">Login</a></li>
       </ul>
   """

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'cfgof_sid' in cookie:
            cfgof_sid = cookie['cfgof_sid'].value
            session_store = open('../users/sess_' + cfgof_sid, writeback=False)
            if session_store.get('authenticated'):
                result = """
                        <h1>Chicken Run!</h1>
                        <h1>Instructions</h1>
                        <ul>
                          <li>Use the space bar to jump and dodge obstacles.</li>
                          <li>Your score increases the longer you surrvive.</li>
                        </ul>
                        <ul>
                          <li id="startBtn">START</li>
                        </ul>
                        <p id = "score">Score: 0</p>
                        <canvas width="750" height="750"></canvas>
                        """
            session_store.close()
            print(cookie)
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'


print('Content-Type: text/html')
print()

print("""
    <!DOCTYPE html>
    <html lang="en" id = "chicken_run">
      <head>
          <meta charset="UTF-8">
          <title>Chicken Run</title>
          <link rel = "stylesheet" href = "../styles/games.css" />
          <script src = "chicken_run.js" type = "module"></script>
      </head>
      <body>
          <header class="header_with_nav">
              <h1>Conor's Fun Games of Fun!</h1>
          </header>
          <nav>
              <a href="../home.py">Home</a>
              <a href="logout.py">Logout</a>
          </nav>
          <main>
            %s
          </main>
      </body>
    </html>""" %(result))
