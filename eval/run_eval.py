import json
from pathlib import Path
from productivity_agent.harness.runner import run
from metrics import check_tool_call

TASKS_PATH = Path(__file__).parent / "benchmark" / "tasks.jsonl"

def load_tasks():
    with TASKS_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]

def main():
    tasks = load_tasks()
    results = []
    for task in tasks:
        result = run(task["query"])
        passed = check_tool_call(result["messages"], task["expected_tool"])
        results.append({"id": task["id"], "query": task["query"], "passed": passed})

    passed_count = sum(r["passed"] for r in results)
    print(f"\nEval results: {passed_count}/{len(results)} passed\n")
    for r in results:
        print(f"[{'PASS' if r['passed'] else 'FAIL'}] {r['id']}: {r['query']}")

if __name__ == "__main__":
    main()