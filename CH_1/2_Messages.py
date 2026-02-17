# Messages in LangChain are a structured way to represent the conversation between the user and the AI. 
# They consist of different types of messages, such as SystemMessage, HumanMessage, and AIMessage, 
# which help to organize the flow of the conversation and provide context for the AI's responses. 
# In this code snippet, we will see how to use these message types with the ChatOpenAI model from LangChain.
from langchain_core.messages import ChatMessage, HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))


my_message = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
]
final_output = llm_openai.invoke(my_message)
print(final_output.content)