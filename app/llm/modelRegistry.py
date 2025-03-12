from .modelConfiguration import OllamaModelConfig
from .modelTask import ModelTask
from langchain_community.llms import Ollama
from typing import Dict

# Define model configurations for each task
MODEL_REGISTRY: Dict[ModelTask, OllamaModelConfig] = {
    ModelTask.CODE_GENERATION: OllamaModelConfig(
        name="codellama:7b-instruct",  # Using CodeLlama for generation tasks
        temperature=0.4,  # Lower temperature for more precise code generation
        stop=[
            "```",          # Stop if model tries to end the code block with backticks
            "</code>",      # Stop if model tries to use HTML code closing tag
            "```python",    # Stop if model tries to start new code blocks
            "```javascript", # These prevent the model from generating multiple
            "```java",      # code blocks or switching languages within
            "```cpp",       # a single generation
        ],
    ),
    ModelTask.CODE_TRANSLATION: OllamaModelConfig(
        name="wizardcoder:7b-python",  # Using WizardCoder for translation tasks
        temperature=0.3,  # Lower temperature for accurate translations
        stop=[
            "```",          # Prevents adding markdown code block endings
            "</code>",      # Prevents HTML code tag closures
            "```python",    # These prevent the model from adding examples
            "```javascript", # in different languages after completing
            "```java",      # the primary translation task
            "```cpp",       # Keeps output focused on just the translated code
        ],
    ),
    ModelTask.CODE_EXPLANATION: OllamaModelConfig(
        name="wizardcoder:7b-python",  # WizardCoder is good for explanations too
        temperature=0.3,  # Slightly higher temperature for natural explanations
        stop=[
            "```"           # Stops the model from including code examples in explanation
                            # This keeps explanations as natural language only
        ]
    )
}

def get_model_for_task(task: ModelTask) -> Ollama:
    """
    Get the appropriate LLM model for a specific task.
    """
    # Simple debug print without changing functionality
    print(f"Getting model for task: {task.name}")
    
    if task not in MODEL_REGISTRY:
        raise KeyError(f"No model configured for task: {task}")
    
    config = MODEL_REGISTRY[task]
    model = config.create_model()
    
    # Print just the model name
    print(f"Using model: {config.name}")
    return model