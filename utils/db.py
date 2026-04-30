import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # HABIT LOGS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        habit_name TEXT,
        completed INTEGER,
        points INTEGER,
        streak INTEGER
    )
    """)

    # MENTAL HEALTH
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mental_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        mood INTEGER,
        stress INTEGER,
        sleep INTEGER,
        energy INTEGER,
        appetite INTEGER,
        social INTEGER,
        journal TEXT,
        score INTEGER,
        level TEXT,
        ai_response TEXT
    )
    """)

    # DISEASE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        bmi REAL,
        exercise TEXT,
        sleep REAL,
        smoking TEXT,
        alcohol TEXT,
        sugar TEXT,
        family_history TEXT,
        bp TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        factors TEXT,
        advice TEXT
    )
    """)

    # MEDICINES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        medicine_name TEXT,
        dosage TEXT,
        morning INTEGER,
        afternoon INTEGER,
        night INTEGER,
        warning_text TEXT
    )
    """)

    # POINTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_points INTEGER
    )
    """)

    # CUSTOM HABITS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS custom_habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT
    )
    """)

    conn.commit()
    conn.close()