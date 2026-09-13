import sqlite3
from pathlib import Path

DB_PATH = Path("data/mock.db")

def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.executemany(
        "INSERT INTO tasks (title, due_date, done) VALUES (?, ?, ?)",
        [
            ("Finish Q3 report", "2026-09-15", 0),
            ("Email Raj about the trial extension", "2026-09-14", 0),
            ("Renew domain registration", "2026-10-01", 0),
        ],
    )
    conn.executemany(
        "INSERT INTO events (title, start_time, end_time) VALUES (?, ?, ?)",
        [
            ("Design sync", "2026-09-18 15:00", "2026-09-18 15:30"),
            ("1:1 with manager", "2026-09-16 11:00", "2026-09-16 11:30"),
        ],
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
    print("Seeded mock.db.")