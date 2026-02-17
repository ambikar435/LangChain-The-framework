
# Structured output refers to the ability of a language model to generate output that adheres to a specific format 
# or structure, such as JSON, XML, or a custom data model. 

# This is particularly useful when you want to extract specific information from the model's response or 
# when you want to ensure that the output can be easily parsed and used in downstream applications. 

# In this code snippet, we will see how to use the with_structured_output method 
# from the ChatOpenAI class in the LangChain library to generate structured output based on a defined Pydantic model.    

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path    

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file
llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Define a Pydantic model to represent the structured output for weather data.

class Weather(BaseModel):
    country: str = Field(description="The Country Name")   
    temperature: float = Field(description="The Temperature in Celsius")
    condition: str = Field(description="The Weather Condition, e.g., Sunny, Rainy, etc.")
    
# Use the with_structured_output method to specify that we want the output to be structured according to the Weather model.
llm_structured_output = llm_openai.with_structured_output(Weather)

result = llm_structured_output.invoke(
    "Provide an example weather report for New York. "
    "If real-time weather is unavailable, give a reasonable estimate."
)
print(result)