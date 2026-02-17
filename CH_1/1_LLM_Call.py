from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path 

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file

llm = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
response = llm.invoke("What is the capital of France?")
print(response.content)

