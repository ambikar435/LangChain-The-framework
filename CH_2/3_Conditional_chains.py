#A conditional chain is when LangChain decides which chain to run based on the input.
# Instead of running everything, we route the request to the correct pipeline.

from dotenv import load_dotenv
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_core.runnables import RunnableLambda, RunnableBranch
from pydantic import BaseModel
from typing import Literal

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

# llm 

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))


#Schema 
class llm_schema(BaseModel):
    Movie_summary_flag : Literal["positive", "negative"]
    
#Chain 1 for conditional chain

# Prompt Template

Prompt_Templet = ChatPromptTemplate.from_messages([
    ("system", "you are Movie review evaluator"),
    ("human", "please catagorize the movie review as postive or negative : {input}")
])

llm_structured_output = llm_openai.with_structured_output(llm_schema)

def pydantic_json(input:llm_schema)->str:
    return input.model_dump()['Movie_summary_flag']

pydantic_json_runnable = RunnableLambda(pydantic_json)


# Linked-In Post

# Prompt
Linkedin_Prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a linkedin Post Generator"),
    ("human", 'Create a Post for the Following text for linkedin : {text}')
])

# str_parser

str_parser = StrOutputParser()

linkedin_chain = Linkedin_Prompt | llm_openai | str_parser


def insta_chain(text:dict)->dict:
    Instagram_Prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a Instagram Post Generator"),
    ("human", 'Create a Post for the Following text for Instagaram : {text}')
    ])
    
    text = text["text"]
    #llm

    #llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))

    # str_parser

    str_parser = StrOutputParser()
    
    insta_chain = Instagram_Prompt | llm_openai | str_parser
    
    result = insta_chain.invoke({"text":text})
    
    return result

insta_chain_runnable = RunnableLambda(insta_chain)

conditional_chain = RunnableBranch(
    (lambda x : "positive" in x, linkedin_chain), insta_chain_runnable
)

final_chain = Prompt_Templet | llm_structured_output | pydantic_json_runnable | conditional_chain

result = final_chain.invoke({"input": "I liked the KGF Movie"})

print(result)