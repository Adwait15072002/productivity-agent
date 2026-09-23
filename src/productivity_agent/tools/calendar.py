import sqlite3
from pathlib import Path
from langchain_core.tools import tool

DB_PATH = Path("data/mock.db")

@tool
def list_events() -> str:
    """List all events on the user's calendar, including their start and end times."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, title, start_time, end_time FROM events").fetchall()
    conn.close()
    if not rows:
        return "No events found."
    return "\n".join(f"[{r[0]}] {r[1]} ({r[2]} - {r[3]})" for r in rows)