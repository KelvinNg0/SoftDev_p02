import sqlite3
from datetime import datetime #for timestamp

DB_FILE = "database.db"

def accountExists(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM accounts WHERE username = (?)", (username,))
    rowCount = 0
    for row in c:
        rowCount += 1

    db.close()

    if (rowCount == 1):
        return True

    return False

def addAccount(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(
        "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (username, password, 0, 0, "", "", 0, 0)
    )

    db.commit()
    db.close()

def authenticate(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM accounts WHERE username = (?)", (username,))
    rowCount = 0
    for row in c:
        rowCount += 1

    db.close()
    if (rowCount != 1):
        return False

    return password == row[1]

def reg_clicks(username, num_clicks):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("UPDATE accounts SET clicks = clicks + num_clicks")
    c.execute("UPDATE accounts SET total_clicks = total_clicks + num_clicks")

    db.commit()
    db.close()

def get_clicks(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT clicks FROM accounts WHERE username = (?)", (username,))
    cookies = c.fetchall()[0][0]
    c.execute("SELECT total_clicks FROM accounts WHERE username = (?)", (username,))
    total_cookies = c.fetchall()[0][0]

    return cookies, total_cookies
