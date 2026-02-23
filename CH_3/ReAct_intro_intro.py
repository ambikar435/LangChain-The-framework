from langchain_openai import ChatOpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

Path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(Path)

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))

#### Tools for ReAct Agent
# Tool 1 for React - [NEWS SUMMARIZER]

from langchain_community.tools import DuckDuckGoSearchResults

search_tool = DuckDuckGoSearchResults()

#result = search_tool.invoke("who is Julie Sweet?")

#print(result)

#TOOL 2 for React - [WIKI SUMMARY]

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(), description="Use this tool to get summary of any topic from wikipedia")

#result = wiki_tool.invoke("Capital of India?")
#print(result)

#TOOL 3 for React - [CUSTOM TOOL]

from langchain.tools import tool

@tool
def enterprise_tool(query:str)->str:
    """This is the tool to send Email to the employees of the company"""
    return f"Email sent to employees with query: {query}"

# Agent Creation and connecting with toolkit

tool_kit = [search_tool, wiki_tool, enterprise_tool]
print(tool_kit)

from langchain.agents import create_agent

model = ChatOpenAI(model="gpt-5-mini",
                   temperature=0.1,
                   max_tokens = 1000,
                   timeout=30)

agent = create_agent(model=model, tools=tool_kit)

print(agent)

example_query = "Who is the CEO of Accenture?"

events = agent.stream({"messages": [("human", example_query)]}, stream_mode="values", )
for event in events:
    print(event)
    print("\n")
    
#Manually binding the LLM with toolkit

llm_binded = llm_openai.bind_tools(tool_kit)
result = llm_binded.invoke("Who is the CEO of Accenture?")
print(result)