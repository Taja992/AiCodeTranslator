from enum import Enum

class ModelTask(Enum):
    """
    Enum defining different tasks that require specialized models.
    Each task will be mapped to a specific Ollama model.
    """
    CODE_GENERATION = "code_generation"  # For generating new code
    CODE_TRANSLATION = "code_translation"  # For translating between languages
    CODE_EXPLANATION = "code_explanation"  # For explaining existing code