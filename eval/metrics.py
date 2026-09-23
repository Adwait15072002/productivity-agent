import sqlite3
from pathlib import Path

DB_PATH = Path("data/mock.db")


def check_tool_call(messages, expected_tool) -> bool:
    called_tools = set()
    for m in messages:
        tool_calls = getattr(m, "tool_calls", None)
        if tool_calls:
            called_tools.update(c["name"] for c in tool_calls)

    if expected_tool is None:
        return len(called_tools) == 0
    return expected_tool in called_tools


def check_groundedness(final_answer: str, expected_titles: list[str]) -> dict:
    found = [title for title in expected_titles if title in final_answer]
    missing = [title for title in expected_titles if title not in final_answer]
    return {"passed": len(missing) == 0, "found": found, "missing": missing}


def get_pending_task_titles() -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    titles = [row[0] for row in conn.execute("SELECT title FROM tasks WHERE done = 0")]
    conn.close()
    return titles


def get_all_task_titles() -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    titles = [row[0] for row in conn.execute("SELECT title FROM tasks")]
    conn.close()
    return titles


GROUNDEDNESS_SOURCES = {
    "pending": get_pending_task_titles,
    "all": get_all_task_titles,
}