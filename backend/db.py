import sqlite3
import os

DB_PATH = os.path.join("backend", "database", "users.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            total_time REAL,
            t1 REAL,
            t2 REAL,
            t3 REAL,
            explosiveness REAL,
            endurance REAL,
            strength REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_run_to_db(username, run_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO runs (username, total_time, t1, t2, t3, explosiveness, endurance, strength, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        run_data["total_time"],
        run_data["t1"],
        run_data["t2"],
        run_data["t3"],
        run_data["explosiveness"],
        run_data["endurance"],
        run_data["strength"],
        run_data["category"]
    ))
    conn.commit()
    conn.close()

def get_user_runs(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT total_time, t1, t2, t3, explosiveness, endurance, strength, category
        FROM runs WHERE username = ?
        ORDER BY id DESC
    """, (username,))
    rows = c.fetchall()
    conn.close()
    keys = ["total_time", "t1", "t2", "t3", "explosiveness", "endurance", "strength", "category"]
    return [dict(zip(keys, row)) for row in rows]
