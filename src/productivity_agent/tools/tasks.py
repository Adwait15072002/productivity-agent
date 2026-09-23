import sqlite3
from pathlib import Path
from langchain_core.tools import tool

DB_PATH = Path("data/mock.db")

@tool
def list_tasks(only_pending: bool = True) -> str:
    """List tasks from the user's task list. Set only_pending=False to include completed tasks."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT id, title, due_date, done FROM tasks"
    if only_pending:
        query += " WHERE done = 0"
    rows = conn.execute(query).fetchall()
    conn.close()
    if not rows:
        return "No tasks found."
    return "\n".join(
        f"[{r[0]}] {r[1]} (due {r[2]}, {'done' if r[3] else 'pending'})"
        for r in rows
    )