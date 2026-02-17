import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": "Tell me about Honey Bee."}], model="gpt-5-mini")
print(chat_completion.choices[0].message.content)
