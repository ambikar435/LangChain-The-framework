# This code demonstrates how to use the LangChain framework to create a prompt template and invoke a language model (LLM) 
# to generate a response based on user input. 
# It loads environment variables from a .env file, initializes the ChatOpenAI model, 
# and uses a PromptTemplate to format the user's input before sending it to the LLM for processing. 
# Finally, it prints the generated response.
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path    

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Example of using PromptTemplate
prompt_template = PromptTemplate.from_template("What is the Capital of {country}?")

user_prompt = input("Enter a country name: ")

ready_prompt = prompt_template.invoke({"country": user_prompt})
final_output = llm_openai.invoke(ready_prompt)
print(final_output.content)

# Example of using ChatPromptTemplate
# ChatPromptTemplate allows us to create more complex prompts with multiple message types (system, human, AI) and placeholders for dynamic content.
from langchain_core.prompts import ChatPromptTemplate
chat_prompt_templet = ChatPromptTemplate.from_messages([
    ("system", "You are a {Tone} assistant."),
    ("human", "What is the weather in {country}?")
])
user_prompt = input("Enter a country name: ")
user_tone = input("Enter the tone you want the response in: ")

ready_prompt = chat_prompt_templet.invoke({"country": user_prompt, "Tone": user_tone})
final_output = llm_openai.invoke(ready_prompt)
print(final_output.content)