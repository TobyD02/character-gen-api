import os
import sqlite3


def init_db():
    db_path = os.getenv("SQLITE_PATH")
    if not db_path:
        db_path = "./db.sqlite3"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS powerscale (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tier REAL,
        label TEXT UNIQUE,
        name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS character_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page_id INTEGER UNIQUE,
        name TEXT UNIQUE,
        image TEXT,
        description TEXT,
        powerscale_id INTEGER,
        html_colour_hex TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS character_category (
        character_id INTEGER,
        category TEXT,
        PRIMARY KEY (character_id, category)
    )
    """)

    conn.commit()
    conn.close()