from abc import ABC, abstractmethod


class BaseLLMModel(ABC):
    @abstractmethod
    def initialize(self, model: str, system_content: str):
        pass

    @abstractmethod
    def run(self, prompt: str) -> str:
        pass
