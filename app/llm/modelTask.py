from enum import Enum

class ModelTask(Enum):
    """
    Enum defining different tasks that require specialized models.
    Each task will be mapped to a specific Ollama model.
    """
    CODE_GENERATION = "code_generation"
    CODE_TRANSLATION = "code_translation"
    CODE_EXPLANATION = "code_explanation"