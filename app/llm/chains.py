from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any
import time

from .modelRegistry import get_model_for_task
from .modelTask import ModelTask
from .tools import CodeLanguageDetectionTool

# Initialize language detection tool for code analysis
language_detector = CodeLanguageDetectionTool()

def create_code_explanation_chain() -> LLMChain:
    """
    Creates a chain for explaining code.
    
    This chain takes code as input and provides a detailed explanation
    of how the code works in natural language.
    
    Returns:
        LLMChain: A chain for code explanation
    """
    llm = get_model_for_task(ModelTask.CODE_EXPLANATION)
    
    prompt = PromptTemplate(
        template="""
        # System: You are an expert programming teacher and code explainer.
        
        # Task: Explain the following code in a clear, organized manner.
        
        # Input:
        ```{language}
        {code}
        ```
        
        # Instructions:
        1. First, explain the overall purpose of the code
        2. Break down the key components and how they work together
        3. Explain any important algorithms, patterns, or techniques used
        4. Note any potential issues, optimizations, or best practices relevant to this code
        5. Keep your explanation concise but thorough
        6. Suggest possible debugger code where it may help
        
        # Output your explanation:
        """,
        input_variables=["code", "language"],
    )
    
    from langchain_core.output_parsers import StrOutputParser
    from operator import itemgetter

    chain = prompt | llm | StrOutputParser()
    return lambda inputs: {"explanation": chain.invoke(inputs)}

def create_code_generation_chain():
    """Creates a chain for generating code based on text descriptions"""
    llm = get_model_for_task(ModelTask.CODE_GENERATION)
    
    prompt_template = """# System: You are an expert programmer. Generate code in the exact programming language requested.

# Task: Write code in {language} that accomplishes the following:
{description}

# Requirements:
1. Use ONLY {language} syntax
2. Include helpful comments
3. Ensure the code is complete and working
4. Do not include markdown code blocks or language tags

# Response (write only the code):
"""
    
    def generate_code(inputs: Dict[str, Any]) -> Dict[str, str]:
        try:
            formatted_prompt = prompt_template.format(
                language=inputs.get("language", "python"),
                description=inputs.get("description", "")
            )
            
            # Try to get response from model
            result = llm.invoke(formatted_prompt)
            print(f"Debug: Raw response:\n{result}")
            
            if result and len(result.strip()) > 0:
                return {"code": result.strip()}
            
            return {"code": "// Error: No code generated"}
                
        except Exception as e:
            print(f"Error in code generation: {str(e)}")
            return {"code": f"// Error generating code: {str(e)}"}
    
    return generate_code

def create_code_translation_chain():
    """Creates a chain for translating code between programming languages"""
    llm = get_model_for_task(ModelTask.CODE_TRANSLATION)
    detector = CodeLanguageDetectionTool()
    
    prompt = PromptTemplate(
        template="""# System: You are an expert code translator.

# Task: Translate the following code from {source_language} to {target_language}.

Original code ({source_language}):
{code}

# Requirements:
1. Write ONLY the translated code in {target_language}
2. Maintain the same functionality
3. Use idiomatic {target_language} patterns
4. Include equivalent comments
5. Do not include markdown code blocks or language tags

# Write the {target_language} code now:""",
        input_variables=["code", "source_language", "target_language"]
    )
    
    def translate(inputs: Dict[str, Any]) -> Dict[str, str]:
        try:
            # Detect source language
            source_language = detector._run(inputs["code"])
            
            # Format prompt with correct source and target languages
            result = llm.invoke(prompt.format(
                code=inputs["code"],
                source_language=source_language,
                target_language=inputs["target_language"]  # Use the requested target language
            ))
            
            if result and len(result.strip()) > 0:
                return {"translated_code": result.strip()}
            
            return {"translated_code": "# Error: No translation generated"}
                
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return {"translated_code": f"# Error: {str(e)}"}
    
    return translate
