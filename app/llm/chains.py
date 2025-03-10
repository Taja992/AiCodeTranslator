from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel
from typing import Dict, List, Any, Optional

# You'll need to set OPENAI_API_KEY in your environment variables
# or pass it explicitly when initializing the LLM

# Define two different LLMs
DEFAULT_LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
CODE_SPECIALIZED_LLM = ChatOpenAI(model_name="gpt-4", temperature=0.2)


class ExplainCodeChain(LLMChain):
    """Chain for explaining code snippets in natural language."""
    
    @classmethod
    def from_llm(
        cls,
        llm: Optional[BaseLanguageModel] = None,
        verbose: bool = False
    ) -> LLMChain:
        if llm is None:
            llm = DEFAULT_LLM
            
        prompt = PromptTemplate(
            input_variables=["code", "language"],
            template="""
            You are an expert programmer and teacher. Explain the following {language} code in detail:
            
            ```{language}
            {code}
            ```
            
            In your explanation, please:
            1. Summarize what the code does at a high level
            2. Explain each significant part of the code step by step
            3. Identify any potential edge cases, bugs, or inefficiencies
            4. Suggest any improvements that could be made
            
            Format your response in markdown, with clear sections and code examples where appropriate.
            """
        )
        
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class GenerateCodeChain(LLMChain):
    """Chain for generating code from natural language descriptions."""
    
    @classmethod
    def from_llm(
        cls,
        llm: Optional[BaseLanguageModel] = None,
        verbose: bool = False
    ) -> LLMChain:
        if llm is None:
            llm = CODE_SPECIALIZED_LLM
            
        prompt = PromptTemplate(
            input_variables=["description", "language"],
            template="""
            You are an expert programmer with deep knowledge of {language}. 
            Create a clean, efficient, and well-documented implementation based on this description:
            
            Description: {description}
            
            Please follow these guidelines:
            1. Use idiomatic {language} code that follows best practices
            2. Include helpful comments to explain complex parts
            3. Handle potential edge cases
            4. Use efficient algorithms and data structures
            5. Organize the code logically with proper structure
            
            Return ONLY the code without explanations before or after.
            
            ```{language}
            """
        )
        
        return cls(prompt=prompt, llm=llm, verbose=verbose)


class TranslateCodeChain(LLMChain):
    """Chain for translating code between programming languages."""
    
    @classmethod
    def from_llm(
        cls,
        llm: Optional[BaseLanguageModel] = None,
        verbose: bool = False
    ) -> LLMChain:
        if llm is None:
            llm = CODE_SPECIALIZED_LLM
            
        prompt = PromptTemplate(
            input_variables=["code", "source_language", "target_language"],
            template="""
            You are an expert polyglot programmer who is fluent in many programming languages.
            Translate the following {source_language} code to equivalent {target_language} code:
            
            ```{source_language}
            {code}
            ```
            
            Your translation should:
            1. Maintain the same functionality as the original code
            2. Use idiomatic patterns in the target language
            3. Follow best practices for the target language
            4. Preserve the logic and structure where appropriate
            5. Use equivalent libraries/functions in the target language
            
            Return ONLY the translated code without explanations before or after.
            
            ```{target_language}
            """
        )
        
        return cls(prompt=prompt, llm=llm, verbose=verbose)