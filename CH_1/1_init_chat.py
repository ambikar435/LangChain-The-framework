from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from pathlib import Path    

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)  # Load environment variables from .env file

chat = init_chat_model(model="gpt-5-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
response = chat.invoke("How are you doing today?")
print(response.content)