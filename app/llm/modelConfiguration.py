from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from typing import List, Optional
from .modelTask import ModelTask

class OllamaModelConfig(BaseModel):
    """
    Configuration settings for an Ollama model.
    
    This class defines parameters that control model behavior such as
    temperature, top_p, etc., and provides a method to create an
    Ollama model instance with these settings.
    """
    name: str  # Model name in Ollama
    temperature: float = 0.1
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    stop: List[str] = []  # Sequences where the model should stop generating
    
    def create_model(self) -> OllamaLLM:
        """
        Creates and returns an Ollama LLM instance with the configured settings.
        
        Returns:
            OllamaLLM: The configured Ollama LLM instance
        """
        return OllamaLLM(
            model=self.name,
            base_url="http://localhost:11434",  # Add this line
            temperature=self.temperature, 
            top_p=self.top_p,
            top_k=self.top_k,
            repeat_penalty=self.repeat_penalty,
            stop=self.stop
        )