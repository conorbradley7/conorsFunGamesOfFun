#!/usr/local/bin/python3

from cgitb import enable
enable()

from os import environ
from shelve import open
from datetime import date
from cgi import FieldStorage
from html import escape
import pymysql as db
from http.cookies import SimpleCookie

result_message = """
       <p>You do not have permission to access this page. Please Login or Register.</p>
       <ul>
           <li><a href="register.py">Register</a></li>
           <li><a href="login.py">Login</a></li>
       </ul>
   """
form_data = FieldStorage()
score = ''
game = ''
result_message = ""
heading = "GAME OVER"
replay_link = ""
today = date.today().strftime("%Y-%m-%d")
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'cfgof_sid' in cookie:
            cfgof_sid = cookie['cfgof_sid'].value
            session_store = open('users/sess_' + cfgof_sid, writeback=False)
            if session_store.get('authenticated'):
                if len(form_data) != 0:
                    username = session_store.get("username")
                    score  = escape(form_data.getfirst('score', '').strip())
                    game  = escape(form_data.getfirst('game', '').strip())
                    score = int(score)
                    replay_link = game+"/"+game+".py"
                    if game not in ["space_invaders","chicken_run"]:
                        result_message = """
                                        <p>Woah woah woah. Where do you think you're going?
                                        You've got to play one of my games first before you come here!</p>
                                        """
                    else:
                        connection = db.connect('cs1.ucc.ie', 'cjb4', 'ohchu', 'cs6503_cs1106_cjb4')
                        cursor = connection.cursor(db.cursors.DictCursor)
                        cursor.execute("""INSERT INTO scores(username,game,score,date_scored)
                                            VALUES(%s,%s,%s,DATE(%s));""", (username, game, score, today))
                        if game == "chicken_run":
                            cursor.execute("""SELECT chicken_run FROM users
                                            WHERE username = %s;""", (username))

                        elif game == "space_invaders":
                            cursor.execute("""SELECT space_invaders FROM users
                                            WHERE username = %s;""", (username))
                        high_score = int(cursor.fetchone()[game])
                        if score > high_score:
                            heading = "NEW HIGH SCORE!"
                            result_message = """<p>Woah! Congratulations you scored
                                            %i! That's a new high score! Nice
                                            Job.</p>""" %(score)
                            if game == "chicken_run":
                                cursor.execute("""UPDATE users
                                                Set chicken_run = %s
                                                WHERE username = %s""", (score,username))
                            if game == "space_invaders":
                                cursor.execute("""UPDATE users
                                                Set space_invaders = %s
                                                WHERE username = %s""", (score,username))

                        elif score == high_score:
                            result_message = """<p>Nice job! You matched your high score,
                                            %i! Gowan, play again and try beat it... Just
                                            one more point, you can do it!</p>""" %(score)

                        else:
                            result_message = """
                                                <p>Nice Job! You scored %i.
                                                Although not quite your high
                                                score... Why not play again and
                                                beat that score? (%i)</p>
                                             """ %(score, high_score)

                        connection.commit()
                        cursor.close()
                        connection.close()

                        session_store.close()
                        print(cookie)

except(IOError, db.Error, ValueError):
    result_message = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print("Content-Type: text/html")
print()
print(
    """
    <!DOCTYPE html>
    <html lang="en" id = "game_over">
      <head>
          <meta charset="UTF-8">
          <title>Game Over</title>
          <link rel = "stylesheet" href = "styles/games.css" />
      </head>
      <body>
        <header class="header_with_nav">
          <h1>%s</h1>
        </header class="header_with_nav">
        <nav>
            <a href="logout.py">Logout</a>
            <a href = "home.py">Home</a>
            <a href = "%s">Play Again!</a>
        </nav>
        <main>
            %s
        </main>
      </body>
    </html>

    """ %(heading,replay_link,result_message)
)
