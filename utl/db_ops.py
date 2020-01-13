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
        "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (username, password, 0, 0, 0, 0, "", 0, 0)
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

def changepw(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("UPDATE accounts SET password = (?) WHERE username = (?)", (password, username,))

    db.commit()
    db.close()

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

    db.close()
    return cookies, total_cookies

def get_trial_data(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT trial_15_sec FROM accounts WHERE username = (?)", (username,))
    trial_15_sec = c.fetchall()[0][0]
    c.execute("SELECT trial_30_sec FROM accounts WHERE username = (?)", (username,))
    trial_30_sec = c.fetchall()[0][0]

    db.close()
    return trial_15_sec, trial_30_sec

# Will necessitate JS that prevents buying something you already have + don't have the cookies for
def buy_perk(username, id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (int(id) == 0):
        c.execute("UPDATE accounts SET perk_0_lvl = perk_0_lvl + 1 WHERE username = (?)", (username,))
    if (int(id) == 1):
        c.execute("UPDATE accounts SET perk_1_lvl = perk_1_lvl + 1 WHERE username = (?)", (username,))

    db.commit()
    db.close()

def record_trial(username, trial_type, clicks):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (trial_type == "trial_15_sec"):
        c.execute("SELECT trial_15_sec FROM accounts WHERE username = (?)", (username,))
        prev_record = c.fetchall()[0][0]
        if (int(clicks) > prev_record):
            c.execute("UPDATE accounts SET trial_15_sec = (?) WHERE username = (?)", (clicks, username))

    if (trial_type == "trial_30_sec"):
        c.execute("SELECT trial_30_sec FROM accounts WHERE username = (?)", (username,))
        prev_record = c.fetchall()[0][0]
        if (int(clicks) > prev_record):
            c.execute("UPDATE accounts SET trial_30_sec = (?) WHERE username = (?)", (clicks, username))

    db.commit()
    db.close()

def get_leaderboards():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    leaderboard_15_sec = []
    c.execute("SELECT username, trial_15_sec FROM accounts WHERE trial_15_sec > 0 ORDER BY trial_15_sec")
    for row in c:
        dict = {}
        dict['username'] = row[0]
        dict['seconds'] = row[1]
        leaderboard_15_sec.append(dict)

    leaderboard_30_sec = []
    c.execute("SELECT username, trial_30_sec FROM accounts WHERE trial_30_sec > 0 ORDER BY trial_30_sec")
    for row in c:
        dict = {}
        dict['username'] = row[0]
        dict['seconds'] = row[1]
        leaderboard_30_sec.append(dict)

    db.close()
    return leaderboard_15_sec, leaderboard_30_sec

def calc_persecond(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    persecond = 0
    c.execute("SELECT perk_0_lvl, perk_1_lvl FROM accounts WHERE username = (?)", (username,))

    for row in c:
        print(row)
        print(row[0])
        print(row[1])
        perk_0_lvl = row[0]
        perk_1_lvl = row[1]

    persecond += (perk_0_lvl * 0.1)
    persecond += (perk_1_lvl)
    persecond = int(persecond * 10) / 10 #truncate the imprecise floats

    db.close()
    return persecond
