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
            response = self.client.responses.create(
                model=self.model,
                input=[self.system_message, {"role": "user", "content": prompt}],
                tools=[{"type": "web_search"}],
                reasoning={"effort": "low"},
                stream=False,
            )
            content = response.output_text
            content = clean_content(content)
            return parse_and_dump_json(content)
        except Exception as e:
            print(e)
            print(f"[ERROR] UnknownException | {default_value}")
            return default_value

# Docs:
# https://platform.openai.com/docs/pricing
# https://platform.openai.com/settings/organization/billing/overview
# https://platform.openai.com/docs/guides/reasoning
