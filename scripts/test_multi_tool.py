from productivity_agent.harness.runner import run

queries = [
    "What's on my calendar?",
    "What tasks do I have pending?",
    "What do I have going on — both tasks and calendar?",
]

for q in queries:
    print(f"\n=== {q} ===")
    result = run(q)
    print(result["output"])