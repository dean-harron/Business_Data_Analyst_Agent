from langchain.agents import create_agent
from config import settings
from llm import get_chat_model
from agent.prompts import SYSTEM_PROMPT
from agent.tools import TOOLS


def build_agent():
    model = get_chat_model()
    return create_agent(model=model, tools=TOOLS, system_prompt=SYSTEM_PROMPT)


def run_agent(question: str, data_path: str):
    agent = build_agent()
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": f"Dataset path: {data_path}\nBusiness question: {question}"}
        ]
    })
    return result
