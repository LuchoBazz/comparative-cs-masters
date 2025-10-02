from enum import Enum
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class DeepSeekModels(Enum):
    CHAT = "deepseek-chat"
    REASONER = "deepseek-reasoner"

client = OpenAI(
    api_key = os.environ.get("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com"
)

response = client.chat.completions.create(
    model=DeepSeekModels.CHAT.value,
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, ¿quién eres?"}
    ],
    stream=False
)

print(response.choices[0].message.content)