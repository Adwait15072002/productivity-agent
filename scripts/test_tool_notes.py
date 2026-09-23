from productivity_agent.harness.runner import run

result = run("What did Raj recommend?")
for m in result["messages"]:
    tool_calls = getattr(m, "tool_calls", None)
    print(type(m).__name__, "| tool_calls:", tool_calls, "| content:", m.content[:200])