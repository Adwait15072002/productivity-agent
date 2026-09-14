import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from productivity_agent.tools.tasks import list_tasks

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

llm_with_tools = llm.bind_tools([list_tasks])
response = llm_with_tools.invoke("What tasks do I have pending?")
print(response.tool_calls)