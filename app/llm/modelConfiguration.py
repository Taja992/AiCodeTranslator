from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from typing import List

class OllamaModelConfig(BaseModel):
    # Basic model configuration
    name: str
    temperature: float = 0.1
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    stop: List[str] = []
    
    def create_model(self) -> OllamaLLM:
        # Create an Ollama model instance with optimized settings
        return OllamaLLM(
            model=self.name,
            base_url="http://localhost:11434",
            temperature=self.temperature,
            request_timeout=120,
            context_window=4096,
            verbose=True,
        )