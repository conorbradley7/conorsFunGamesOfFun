#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

result = """
       <p>You do not have permission to access this page. Please Login or Register.</p>
       <ul>
           <li><a href="register.py">Register</a></li>
           <li><a href="login.py">Login</a></li>
       </ul>
   """

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'cfgof_sid' in cookie:
            cfgof_sid = cookie['cfgof_sid'].value
            session_store = open('users/sess_' + cfgof_sid, writeback=False)
            if session_store.get('authenticated'):
                result = """
                    <h1>Please Select A Game!</h1>
                    <section id = "game_gallery">
                        <video src="media/si_sample.mp4" poster="media/space_background.jpeg" loop id="space_invaders"></video>
                        <a href="space_invaders/space_invaders.py">Space Invaders</a>
                        <video src="media/cr_sample.mp4" poster="media/chicken_run_background.jpg" loop id="chicken_run"></video>
                        <a href="chicken_run/chicken_run.py">Chicken Run</a>
                    </section>
                """

            session_store.close()
            print(cookie)

except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later. %s</p>'
print('Content-Type: text/html')
print()
print("""
        <!DOCTYPE html>
        <html lang="en" id = "home">
            <head>
                <meta charset="UTF-8">
                <title>Conor's Fun Games of Fun</title>
                <link rel = "stylesheet" href = "styles/games.css" />
                <script src = "previews.js" type = "module"></script>
            </head>
            <body>
                <header class="header_with_nav">
                    <h1>Conor's Fun Games of Fun!</h1>
                </header>
                <nav>
                    <a href="logout.py">Logout</a>
                </nav>
                <main>
                    %s
                </main>
            </body>
        </html>
"""% (result))
