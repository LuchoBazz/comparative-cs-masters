from google import genai
from dotenv import load_dotenv

from base_llm_model import BaseLLMModel
from providers import GoogleGeminiModels
from utils import clean_content, parse_and_dump_json

load_dotenv()


class GoogleGemini(BaseLLMModel):

    def __init__(self):
        self.model = None
        self.client = None
        self.system_content = None

    def initialize(self, model: str, system_content: str):
        self.model = model
        self.client = genai.Client()
        self.system_content = system_content

    def run(self, prompt: str, default_value: str) -> str:
        try:
            full_prompt = f"{self.system_content}\n\n{prompt}"

            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
            )
            content = response.text
            content = clean_content(content)
            return parse_and_dump_json(content)
        except Exception as e:
            print(e)
            print(f"[ERROR] UnknownException | {default_value}")
            return default_value
