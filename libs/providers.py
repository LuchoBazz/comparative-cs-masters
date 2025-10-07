from enum import Enum


class ChatGPTModels(Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    GPT_5_MINI = "gpt-5-mini"


class GoogleGeminiModels(Enum):
    FLASH_2_5 = "gemini-2.5-flash"
    PRO_1_5 = "gemini-1.5-pro"
    FLASH_2_0 = "gemini-2.0-flash"
