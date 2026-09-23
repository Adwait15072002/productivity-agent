import json
from pathlib import Path
from langchain_core.messages import ToolMessage
from productivity_agent.harness.runner import run
from metrics import check_tool_call, check_groundedness, GROUNDEDNESS_SOURCES
from judge import check_fabrication

TASKS_PATH = Path(__file__).parent / "benchmark" / "tasks.jsonl"

def load_tasks():
    with TASKS_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]

def get_tool_output(messages) -> str:
    tool_messages = [m.content for m in messages if isinstance(m, ToolMessage)]
    return "\n".join(tool_messages)

def main():
    tasks = load_tasks()
    results = []
    for task in tasks:
        result = run(task["query"])
        tool_ok = check_tool_call(result["messages"], task["expected_tool"])

        grounded_ok = True
        grounded_detail = None
        source_key = task.get("groundedness_source")
        if source_key:
            expected_titles = GROUNDEDNESS_SOURCES[source_key]()
            grounded_detail = check_groundedness(result["output"], expected_titles)
            grounded_ok = grounded_detail["passed"]

        fabrication_ok = True
        fabrication_detail = None
        tool_output = get_tool_output(result["messages"])
        if tool_output:
            fabrication_detail = check_fabrication(tool_output, result["output"])
            fabrication_ok = fabrication_detail["passed"]

        results.append({
            "id": task["id"],
            "query": task["query"],
            "tool_ok": tool_ok,
            "grounded_detail": grounded_detail,
            "fabrication_detail": fabrication_detail,
            "known_limitation": task.get("known_limitation"),
            "passed": tool_ok and grounded_ok and fabrication_ok,
        })

    passed_count = sum(r["passed"] for r in results)
    print(f"\nEval results: {passed_count}/{len(results)} passed\n")
    for r in results:
        print(f"[{'PASS' if r['passed'] else 'FAIL'}] {r['id']}: {r['query']}")
        if not r["tool_ok"]:
            print("    tool-call check failed")
        if r["grounded_detail"] and r["grounded_detail"]["missing"]:
            print(f"    missing facts: {r['grounded_detail']['missing']}")
        if r["fabrication_detail"] and not r["fabrication_detail"]["passed"]:
            print(f"    fabrications: {r['fabrication_detail']['raw']}")
        if r.get("known_limitation") and not r["passed"]:
            print(f"    (documented known limitation: {r['known_limitation']})")

if __name__ == "__main__":
    main()