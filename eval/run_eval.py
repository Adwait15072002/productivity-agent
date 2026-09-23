import json
from pathlib import Path
from productivity_agent.harness.runner import run
from metrics import check_tool_call, check_groundedness, GROUNDEDNESS_SOURCES

TASKS_PATH = Path(__file__).parent / "benchmark" / "tasks.jsonl"

def load_tasks():
    with TASKS_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]

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

        results.append({
            "id": task["id"],
            "query": task["query"],
            "tool_ok": tool_ok,
            "grounded_detail": grounded_detail,
            "passed": tool_ok and grounded_ok,
        })

    passed_count = sum(r["passed"] for r in results)
    print(f"\nEval results: {passed_count}/{len(results)} passed\n")
    for r in results:
        print(f"[{'PASS' if r['passed'] else 'FAIL'}] {r['id']}: {r['query']}")
        if not r["tool_ok"]:
            print("    tool-call check failed")
        if r["grounded_detail"] and r["grounded_detail"]["missing"]:
            print(f"    missing facts: {r['grounded_detail']['missing']}")

if __name__ == "__main__":
    main()