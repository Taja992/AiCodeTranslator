from langchain.agents import Tool, AgentExecutor
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.agents.openai_functions_agent import OpenAIFunctionsAgent
from langchain.memory import ConversationBufferMemory

from typing import List, Dict, Any
import json

from .chains import ExplainCodeChain, GenerateCodeChain, TranslateCodeChain, DEFAULT_LLM, CODE_SPECIALIZED_LLM
from .tools import CodeLanguageDetectionTool, CodeComplexityAnalysisTool


class CodeAssistantAgent:
    """Agent that dynamically selects the appropriate chain and tools based on the user's request."""
    
    def __init__(self):
        # Initialize chains
        self.explain_chain = ExplainCodeChain.from_llm(DEFAULT_LLM)
        self.generate_chain = GenerateCodeChain.from_llm(CODE_SPECIALIZED_LLM)
        self.translate_chain = TranslateCodeChain.from_llm(CODE_SPECIALIZED_LLM)
        
        # Initialize tools
        self.language_detector = CodeLanguageDetectionTool()
        self.complexity_analyzer = CodeComplexityAnalysisTool()
        
        # Define the tools available to the agent
        self.tools = [
            Tool(
                name="ExplainCode",
                func=self._explain_code,
                description="Explains a code snippet in detail. Input should be a JSON string with 'code' and optionally 'language'"
            ),
            Tool(
                name="GenerateCode",
                func=self._generate_code,
                description="Generates code from a description. Input should be a JSON string with 'description' and 'language'"
            ),
            Tool(
                name="TranslateCode",
                func=self._translate_code,
                description="Translates code between languages. Input should be a JSON string with 'code', 'source_language', and 'target_language'"
            ),
            Tool(
                name="DetectLanguage",
                func=self.language_detector._run,
                description="Detects the programming language of code. Input should be a code snippet as string"
            ),
            Tool(
                name="AnalyzeComplexity",
                func=self.complexity_analyzer._run,
                description="Analyzes the complexity of code and provides recommendations. Input should be a code snippet as string"
            )
        ]
        
        # Initialize the agent with correct OpenAI functions format
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        
        # Create the system message for the agent
        system_message = SystemMessage(
            content="You are a helpful AI programming assistant. Use the available tools to help the user with their code-related requests."
        )
        
        # Setup memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Create the OpenAI functions agent
        self.agent = OpenAIFunctionsAgent.from_llm_and_tools(
            llm=self.llm,
            tools=self.tools,
            system_message=system_message,
            extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")]
        )
        
        # Initialize the agent executor
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def _explain_code(self, input_str: str) -> str:
        """Handle code explanation using the ExplainCodeChain."""
        try:
            input_data = json.loads(input_str)
            code = input_data.get("code", "")
            language = input_data.get("language")
            
            if not language:
                language = self.language_detector._run(code)
                
            return self.explain_chain.run(code=code, language=language)
        except Exception as e:
            return f"Error explaining code: {str(e)}"
    
    def _generate_code(self, input_str: str) -> str:
        """Handle code generation using the GenerateCodeChain."""
        try:
            input_data = json.loads(input_str)
            description = input_data.get("description", "")
            language = input_data.get("language", "Python")
                
            return self.generate_chain.run(description=description, language=language)
        except Exception as e:
            return f"Error generating code: {str(e)}"
    
    def _translate_code(self, input_str: str) -> str:
        """Handle code translation using the TranslateCodeChain."""
        try:
            input_data = json.loads(input_str)
            code = input_data.get("code", "")
            target_language = input_data.get("target_language", "Python")
            source_language = input_data.get("source_language")
            
            if not source_language:
                source_language = self.language_detector._run(code)
                
            return self.translate_chain.run(
                code=code, 
                source_language=source_language, 
                target_language=target_language
            )
        except Exception as e:
            return f"Error translating code: {str(e)}"
    
    def process_request(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request using the agent."""
        # Convert the query dictionary to a string representation
        query_type = query.get("type", "")
        
        if query_type == "explain":
            code = query.get("code", "")
            language = query.get("language")
            
            if not language:
                language = self.language_detector._run(code)
                
            explanation = self.explain_chain.run(code=code, language=language)
            complexity = self.complexity_analyzer._run(code)
            
            return {
                "explanation": explanation,
                "language": language,
                "complexity_analysis": complexity
            }
            
        elif query_type == "generate":
            description = query.get("description", "")
            language = query.get("language", "Python")
            
            generated_code = self.generate_chain.run(description=description, language=language)
            
            return {
                "code": generated_code,
                "language": language
            }
            
        elif query_type == "translate":
            code = query.get("code", "")
            target_language = query.get("target_language", "Python")
            source_language = query.get("source_language")
            
            if not source_language:
                source_language = self.language_detector._run(code)
                
            translated_code = self.translate_chain.run(
                code=code, 
                source_language=source_language, 
                target_language=target_language
            )
            
            return {
                "code": translated_code,
                "source_language": source_language,
                "target_language": target_language
            }
        
        else:
            # Use the agent for more complex or ambiguous requests
            user_input = str(query.get("input", str(query)))
            result = self.agent_executor.run(input=user_input)
            return {"result": result}