from langchain_core.messages import HumanMessage
from langfuse.langchain import CallbackHandler
from productivity_agent.graph import app

langfuse_handler = CallbackHandler()

def run(user_input: str) -> dict:
    result = app.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"callbacks": [langfuse_handler]},
    )
    final_message = result["messages"][-1]
    return {"output": final_message.content, "messages": result["messages"]}