#========= ONLY RUN THIS FILE IF YOU WANT TO CREATE AN EMPTY DATABASE. ========#

import sqlite3

DB_FILE = "../database.db"
def init_db():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    #Create accounts table (empty)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts(
            username TEXT,
            password TEXT,
            clicks INTEGER,
            total_clicks INTEGER,
            perk_earned_ids TEXT,
            achievements_earned_ids TEXT,
            trial_30_sec INTEGER,
            trial_1_min INTEGER
        )
        """
    )

    #Create perks table (empty)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS perks(
            id INTEGER,
            name TEXT,
            description TEXT,
            cost INTEGER
        )
        """
    )

    #Create achievements table (empty)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS achievements(
            id INTEGER,
            name TEXT,
            description TEXT
        )
        """
    )

    db.commit() #save changes
    db.close()


def add_perks():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    #In order: ID, name of perk, description of perk, cost of perk
    c.execute("INSERT INTO perks VALUES (?, ?, ?, ?)", (0, "Cursor", "Generates clicks while idle!", 20))
    c.execute("INSERT INTO perks VALUES (?, ?, ?, ?)", (1, "Cursor 2", "Generates clicks while idle!", 100))
    c.execute("INSERT INTO perks VALUES (?, ?, ?, ?)", (2, "Cursor 3", "Generates clicks while idle!", 250))
    c.execute("INSERT INTO perks VALUES (?, ?, ?, ?)", (3, "Cursor 4", "Generates clicks while idle!", 500))
    c.execute("INSERT INTO perks VALUES (?, ?, ?, ?)", (4, "Cursor 5", "Generates clicks while idle!", 1000))

    db.commit() #save changes
    db.close()

def add_achievements():
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    #In order: ID, name of achievement, description of achievement
    c.execute("INSERT INTO achievements VALUES (?, ?, ?)", (0, "Fast Fingers", "Click more than 60 times a minute."))
    c.execute("INSERT INTO achievements VALUES (?, ?, ?)", (1, "Speed Demon!", "Click more than 120 times a minute."))
    c.execute("INSERT INTO achievements VALUES (?, ?, ?)", (2, "Consumer", "Spend a total of 50 clicks at the shop."))
    c.execute("INSERT INTO achievements VALUES (?, ?, ?)", (3, "Capitalist", "Spend a total of 1000 clicks at the shop."))
    c.execute("INSERT INTO achievements VALUES (?, ?, ?)", (4, "Get perked up!", "Purchase at least 5 perks."))
    c.execute("INSERT INTO achievements VALUES (?, ?, ?)", (5, "Autoclicking Specialist", "Purchase all of the autoclickers at the shop."))

    db.commit() #save changes
    db.close()

#Run this file to generate an empty database file. Do not run this in any other case.init_db();
init_db();
add_perks();
add_achievements();
