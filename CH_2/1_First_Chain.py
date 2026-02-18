from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

file_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(file_path)

#Task 1 [Prompt]

Prompt_Tamplate = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an Helpfull Assistance"),
        ("human", "{input}")
    ]
)

#Task_2 [LLM]

llm_openai = ChatOpenAI(model="gpt-5-mini", temperature=0, openai_api_key = os.getenv("OPENAI_API_KEY"))

#Task 3 [output]

str_parser = StrOutputParser()

# Chain invocation

chain = Prompt_Tamplate | llm_openai | str_parser

result = chain.invoke({"input": "What is the Capital of INDIA?"})
print(result)

# WE can also invoke the Chain using RunnableSequence

from langchain_core.runnables import RunnableSequence

chain_1 = RunnableSequence(Prompt_Tamplate, llm_openai, str_parser)

result = chain_1.invoke("What is the Capital of India?")

print(result)


# Mannual Invocation
"""
tamplet = Prompt_Tamplate.invoke({"input": "What is the Capital of INDIA"})

res = llm_openai.invoke(tamplet)

result = res.content

print(result)
"""