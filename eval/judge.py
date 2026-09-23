import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

JUDGE_MODEL = "openai/gpt-oss-120b"

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

JUDGE_PROMPT = """You are checking an AI assistant's response for fabricated information.

TOOL OUTPUT (the actual, ground-truth data the assistant had access to):
{tool_output}

ASSISTANT'S FINAL ANSWER:
{final_answer}

List any specific claims, details, or facts in the assistant's answer that are NOT supported by the tool output above. Ignore formatting, rephrasing, or reasonable summarization — only flag genuinely invented content (e.g., made-up reasons, dates, or details not present in the tool output).

Respond in this exact format:
FABRICATIONS: <comma-separated list, or "none">
"""

def check_fabrication(tool_output: str, final_answer: str) -> dict:
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            tool_output=tool_output, final_answer=final_answer)}],
    )
    content = response.choices[0].message.content
    line = next((l for l in content.splitlines() if l.startswith("FABRICATIONS:")), "FABRICATIONS: none")
    fabrications = line.split("FABRICATIONS:", 1)[1].strip()
    return {"passed": fabrications.lower() == "none", "raw": fabrications}