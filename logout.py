#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from http.cookies import SimpleCookie

print('Content-Type: text/html')
print()

result = '<p>You are already logged out</p>'
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'cfgof_sid' in cookie:
            cfgof_sid = cookie['cfgof_sid'].value
            session_store = open('users/sess_' + cfgof_sid, writeback=True)
            session_store['authenticated'] = False
            session_store.close()
            result = """
                <p>You are now logged out. Thanks for coming to play
                Conor's Fun Games Of Fun Games... Of Fun... Yeah I think
                that's it. Please come back again soon or click below above to log back in!</p>
                """
except IOError:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Goodbye!</title>
            <link rel = "stylesheet" href = "styles/games.css" />
        </head>
        <body>
            <header class="header_with_nav">
                <h1>Conor's Fun Games Of Fun</h1>
            </header>
            <nav>
                <a href="login.py">Login Again</a>
            </nav>
            <main>
                <h1>Goodbye For Now!</h1>
            </main>
            %s
        </body>
    </html>"""  %(result)
    )
