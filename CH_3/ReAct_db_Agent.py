# SQL Database Agent using ReAct framework
from langchain_openai import ChatOpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

Path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(Path)

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))

#### Tools for ReAct Agent
# Tool 1 for React - [SQL DATABASE TOOL]

from langchain_community.utilities.sql_database import SQLDatabase

sql_db = SQLDatabase.from_uri("sqlite:///SalesDB/salesdb.db")

from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm_openai)

toolkit = sql_toolkit.get_tools()
#print(toolkit)

from langchain.agents import create_agent

model = ChatOpenAI(model="gpt-5-mini",
                   temperature=0.1,
                   max_tokens = 1000,
                   timeout=30)  

agent = create_agent(model=model, tools=toolkit)


query = "What are the total sales for the product Laptop?"

events = agent.stream({"messages": [("human", query)]}, stream_mode="values", )
for event in events:
    event["messages"][-1].pretty_print()