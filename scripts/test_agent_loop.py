from langchain_core.messages import HumanMessage
from productivity_agent.graph import app

result = app.invoke({"messages": [HumanMessage(content="What tasks do I have pending?")]})
for m in result["messages"]:
    print(type(m).__name__, ":", m.content)