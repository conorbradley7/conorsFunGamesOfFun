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
                        <h1>Space Invaders!</h1>
                        <h1>Instructions</h1>
                        <ul>
                            <li>Use the left and right arrow keys to move your space ship.</li>
                            <li>Use the space bar to fire your gun.</li>
                            <li>Destroy as many aliens as you can and don't let them reach your ship!</li>
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
    <html lang="en" id="space_invaders">
        <head>
            <meta charset="UTF-8">
            <title>Space Invaders</title>
            <link rel = "stylesheet" href = "../styles/games.css" />
            <script src = "space_invaders.js" type = "module"></script>
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
    </html>
""" %(result))
