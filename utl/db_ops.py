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

    c.execute("UPDATE accounts SET clicks = clicks + (?) WHERE username = (?)", (num_clicks, username,))
    c.execute("UPDATE accounts SET total_clicks = total_clicks + (?) WHERE username = (?)", (num_clicks, username,))

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


# Will necessitate JS that prevents buying something you already have + don't have the cookies for
def buy_perk(username, id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT perk_earned_ids FROM accounts WHERE username = (?)", (username,))
    ids = c.fetchall()[0][0]
    ids += str(id) + ","
    #print("Perk IDs (updated): " + ids)
    c.execute("UPDATE accounts SET perk_earned_ids = (?) WHERE username = (?)", (ids, username,))

    db.commit()
    db.close()
