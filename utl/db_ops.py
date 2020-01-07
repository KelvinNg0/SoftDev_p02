import sqlite3
from datetime import datetime #for timestamps

DB_FILE = "database.db"

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
            trial_time_30_sec INTEGER,
            trial_time_1_min INTEGER
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
    add_perks()

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
    #In order: ID, name of perk, description of perk, cost of perk
    c.execute(
        """
        INSERT INTO perks VALUES (?, ?, ?, ?),
          (0,
          "Autoclicker 1",
          "Generates clicks while idle!",
          50
          )
        """
    )

init_db();
