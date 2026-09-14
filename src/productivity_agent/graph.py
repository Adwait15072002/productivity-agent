import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from pathlib import Path
from langchain_core.messages import SystemMessage

from productivity_agent.state import AgentState
from productivity_agent.tools.tasks import list_tasks

load_dotenv()

TOOLS = [list_tasks]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}
SYSTEM_PROMPT = Path("src/productivity_agent/prompts/system.md").read_text()


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
llm_with_tools = llm.bind_tools(TOOLS)


def planner(state: AgentState) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def executor(state: AgentState) -> dict:
    last_message = state["messages"][-1]
    results = []
    for call in last_message.tool_calls:
        tool = TOOLS_BY_NAME[call["name"]]
        try:
            output = tool.invoke(call["args"])
        except Exception as e:
            output = f"Tool error: {e}"   # proto-guardrail — real error handling comes in guardrails.py later
        results.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
    return {"messages": results}


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "executor"
    return END


graph = StateGraph(AgentState)
graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.set_entry_point("planner")
graph.add_conditional_edges("planner", should_continue, {"executor": "executor", END: END})
graph.add_edge("executor", "planner")

app = graph.compile()