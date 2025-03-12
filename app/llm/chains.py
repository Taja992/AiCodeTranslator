from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any

from .modelRegistry import get_model_for_task
from .modelTask import ModelTask
from .tools import CodeLanguageDetectionTool

# Create the language detection tool
language_detector = CodeLanguageDetectionTool()

def create_code_explanation_chain() -> LLMChain:
    """
    Creates a chain for explaining code.
    
    This chain takes code as input and provides a detailed explanation
    of how the code works in natural language.
    
    Returns:
        LLMChain: A chain for code explanation
    """
    # Get the model optimized for code explanation
    llm = get_model_for_task(ModelTask.CODE_EXPLANATION)
    
    # Define the prompt template for code explanation
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
    """
    Creates a chain for generating code.
    """
    # Get the model optimized for code generation
    llm = get_model_for_task(ModelTask.CODE_GENERATION)
    print(f"Code generation model: {type(llm)}")
    
    # Define the prompt template for code generation
    prompt_template = """
    # System: You are an expert programmer who writes clean, efficient, and well-documented code.
    
    # Task: Write code based on the following description.
    
    # Description: {description}
    
    # Target language: {language}
    
    # Style preferences:
    - Indentation: {indentation}
    - Indent size: {indent_size}
    - Max line length: {max_line_length}
    - Naming convention: {naming_convention}
    
    # Instructions:
    1. Write code that meets the description requirements
    2. Follow the specified style preferences exactly
    3. Include appropriate comments and documentation
    4. Use best practices for the target language
    5. Focus on writing efficient, maintainable code
    
    # Output your code (without backticks around it):
    """
    
    def generate_code(inputs: Dict[str, Any]) -> Dict[str, str]:
        try:
            # Format the prompt with input values
            formatted_prompt = prompt_template.format(
                description=inputs.get("description", ""),
                language=inputs.get("language", "python"),
                indentation=inputs.get("indentation", "spaces"),
                indent_size=inputs.get("indent_size", 4),
                max_line_length=inputs.get("max_line_length", 80),
                naming_convention=inputs.get("naming_convention", "snake_case")
            )
            
            # Direct call to the LLM
            print("Sending prompt to LLM:")
            print(formatted_prompt[:200] + "...")  # Print first 200 chars
            
            result = llm.invoke(formatted_prompt)
            print(f"LLM response received. Length: {len(result)}")
            
            if result:
                return {"code": result}
            else:
                return {"code": f"// No code generated for: {inputs.get('description', 'Unknown request')}"}
        except Exception as e:
            print(f"Error in code generation: {str(e)}")
            return {"code": f"// Error generating code: {str(e)}"}
    
    return generate_code

def create_code_translation_chain() -> LLMChain:
    """
    Creates a chain for translating code between programming languages.
    
    This chain takes source code in one language and translates it to
    equivalent code in another language, maintaining the same functionality.
    
    Returns:
        LLMChain: A chain for code translation
    """
    # Get the model optimized for code translation
    llm = get_model_for_task(ModelTask.CODE_TRANSLATION)
    
    # Define the prompt template for code translation
    prompt = PromptTemplate(
        template="""
        # System: You are a specialized code translator that can accurately translate code between programming languages.
        
        # Task: Translate the following code from {source_language} to {target_language}.
        
        # Original code ({source_language}):
        ```{source_language}
        {code}
        ```
        
        # Style preferences:
        - Indentation: {indentation}
        - Indent size: {indent_size}
        - Max line length: {max_line_length}
        - Naming convention: {naming_convention}
        
        # Instructions:
        1. Translate the functionality exactly, preserving all behaviors
        2. Use idiomatic patterns in the target language
        3. Maintain the overall structure where appropriate
        4. Follow the specified style preferences for the target language
        5. Include equivalent comments in the translated code
        
        # Output the translated code in {target_language} (without backticks around it):
        """,
        input_variables=["code", "source_language", "target_language", "indentation", "indent_size", "max_line_length", "naming_convention"],
    )
    
    from langchain_core.output_parsers import StrOutputParser
    from operator import itemgetter

    chain = prompt | llm | StrOutputParser()
    return lambda inputs: {"translated_code": chain.invoke(inputs)}
