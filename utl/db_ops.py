import sqlite3
from datetime import datetime #for timestamp

DB_FILE = "database.db"

def accountExists(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM accounts WHERE username = (?)", (user,))
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
        db.close() #only one iteration should happen anyway
        rowCount += 1

    if (rowCount != 1):
        return False

    return password == row[1]
