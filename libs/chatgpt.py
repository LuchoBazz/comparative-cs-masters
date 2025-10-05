from enum import Enum
import os
import time
import json

from openai import OpenAI
from dotenv import load_dotenv
import tiktoken

from utils import clean_content, parse_and_dump_json
from base_llm_model import BaseLLMModel
from providers import ChatGPTModels

load_dotenv()


class ChatGPT(BaseLLMModel):

    def __init__(self):
        self.model = None
        self.client = None
        self.system_message = None

    def initialize(self, model: str, system_content: str):
        self.model = model
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_message = {
            "role": "system",
            "content": system_content,
        }

    def run(self, prompt: str, default_value: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[self.system_message, {"role": "user", "content": prompt}],
                stream=False,
            )
            content = response.choices[0].message.content
            content = clean_content(content)
            return parse_and_dump_json(content)
        except Exception as e:
            print(e)
            print(f"[ERROR] UnknownException | {default_value}")
            return default_value
