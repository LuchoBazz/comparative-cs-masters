from enum import Enum
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ChatGPTModels(Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

response = client.chat.completions.create(
    model=ChatGPTModels.GPT_4O_MINI.value,
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, ¿quién eres?"}
    ],
    stream=False
)

print(response.choices[0].message.content)
