from productivity_agent.harness.runner import run

result = run("What tasks do I have pending?")
print(result["output"])