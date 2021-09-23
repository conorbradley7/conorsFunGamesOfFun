#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from os import environ
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()

result = """
       <p>You do not have permission to access this page. Please Login or Register.</p>
       <ul>
           <li><a href="register.py">Register</a></li>
           <li><a href="login.py">Login</a></li>
       </ul>
   """

form = """<form action="leaderboards.py" method="post">
            <label>Type Of Leaderboard</label>
            <select name="type">
                <option value="personal">Personal</option>
                <option value="global">Global</option>
            </select>
            <label>Game</label>
            <select name="game">
                <option value="cr">Chicken Run</option>
                <option value="si">Space Invaders</option>
            </select>
            <input type="submit" value="See Leaderboard">
            </form>"""


try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'cfgof_sid' in cookie:
            cfgof_sid = cookie['cfgof_sid'].value
            session_store = open('users/sess_' + cfgof_sid, writeback=False)
            username = session_store.get("username")
            if session_store.get('authenticated'):
                result = ""
                if len(form_data) != 0:
                    type = escape(form_data.getfirst('type', '').strip())
                    game = escape(form_data.getfirst('game', '').strip())
                    result = """
                                <table>
                                    <th scope="col">Username</th><th scope="col">Score</th><th scope="col">Date</th>
                            """
                    connection = db.connect('cs1.ucc.ie', 'cjb4', 'ohchu', 'cs6503_cs1106_cjb4')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    if type == "personal":
                        if game == "cr":
                            cursor.execute("""SELECT username, score, date_scored FROM scores
                                                WHERE username = username AND game = "chicken_run"
                                                ORDER BY score;
                                              """(username))
                            for row in cursor.fetchall():
                                result += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (row["username"],row['score'], row['date_scored'])
                        if game == "si":
                            cursor.execute("""SELECT username, score, date_scored FROM scores
                                                WHERE username = username AND game = "space_invaders"
                                                ORDER BY score;
                                              """(username))
                            for row in cursor.fetchall():
                                result += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (row["username"],row['score'], row['date_scored'])
                    elif type == "global":
                        if game == "cr":
                            cursor.execute("""SELECT username, score, date_scored FROM scores
                                                WHERE game = "chicken_run"
                                                ORDER BY score;
                                              """(username))
                            for row in cursor.fetchall():
                                result += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (row["username"],row['score'], row['date_scored'])
                        if game == "si":
                            cursor.execute("""SELECT username, score, date_scored FROM scores
                                                WHERE game = "space_invaders"
                                                ORDER BY score;
                                              """(username))
                            for row in cursor.fetchall():
                                result += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (row["username"],row['score'], row['date_scored'])
                    result += '</table>'
                    cursor.close()
                    connection.close()

            session_store.close()
            print(cookie)

except (IOError, db.Error):
    form = ""
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
                    <h1>Conor's Fun Games of Fun! Leaderboards</h1>
                </header>
                <nav>
                    <a href="home.py">Home</a>
                    <a href="logout.py">Logout</a>
                </nav>
                <main>
                    %s
                    %s
                </main>
            </body>
        </html>
"""% (form,result))
