# This makes the tools module accessible when importing from app.llm
from .tools import CodeLanguageDetectionTool, CodeComplexityAnalysisTool
from .chains import ExplainCodeChain, GenerateCodeChain, TranslateCodeChain
from .agents import CodeAssistantAgent

# Initialize the agent for easy import
code_assistant = CodeAssistantAgent()