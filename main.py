import os
import time
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from google import genai

load_dotenv()
client = genai.Client()

with open("system_prompt.gh", mode='r') as f:
    system_prompt = f.read()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=1.0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


agent = create_agent(
    model="gemini-3.5-flash",
    tools=[],
    system_prompt="",
    name="recommendation_assistant"
)
