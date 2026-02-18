"""
PROJECT: Movie → Social Media Post Generator

FLOW:
1. User provides movie name
2. LLM summarizes movie
3. Convert summary into dictionary
4. Run LinkedIn + Instagram generation in parallel
5. Return both posts as output

Concepts Used:
- ChatPromptTemplate
- ChatOpenAI
- StrOutputParser
- RunnableLambda
- RunnableParallel
- LCEL (LangChain Expression Language) with |
"""

from dotenv import load_dotenv
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_core.runnables import RunnableLambda, RunnableParallel

env_path = Path(__file__).resolve().parents[1] / ".env"

load_dotenv(env_path)


Prompt_Templet = ChatPromptTemplate.from_messages([
    ("system", "you are Movie Summarizer"),
    ("human", "please summerize the Movie {input} in brief")
])

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))

"""
StrOutputParser:
----------------
Extracts plain text from LLM response.
Without this, you'd get an AIMessage object.
"""

str_parser = StrOutputParser()

# Custom Function

"""
dictionary_maker:
-----------------
Purpose:
Convert string output into dictionary format.

Why?
RunnableParallel expects dictionary-style inputs
to distribute data to multiple branches.
"""

def dictionary_maker(text: str)-> dict:
    result = {"text":text}
    return result

"""
RunnableLambda:
---------------
Wraps a normal Python function
so it becomes a LangChain Runnable
and can be used inside LCEL pipelines.
"""

dictionary_maker_runnable = RunnableLambda(dictionary_maker)
# Parallel Chains 1

# Linked-In Post

# Prompt
Linkedin_Prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a linkedin Post Generator"),
    ("human", 'Create a Post for the Following text for linkedin : {text}')
])

#llm

#llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))

# str_parser

str_parser = StrOutputParser()

linkedin_chain = Linkedin_Prompt | llm_openai | str_parser

#linkedin_chain_runnable = RunnableLambda(linkedin_chain)

# Parallel Chains 2

# Instagram Post using functions

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


# Final Orchestration

final_chain = (
    Prompt_Templet |
    llm_openai | 
    str_parser |
    dictionary_maker_runnable |
    RunnableParallel(branches = {"linkedIn": linkedin_chain, "Instagram" : insta_chain_runnable})
)

result = final_chain.invoke("KGF")

print(result)