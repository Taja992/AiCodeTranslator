from langchain.tools import BaseTool
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from typing import Optional, Type, ClassVar


class CodeLanguageDetectionTool(BaseTool):
    name: ClassVar[str] = "code_language_detection"
    description: ClassVar[str] = "Detects the programming language of a given code snippet"

    def _run(self, code_snippet: str) -> str:
        try:
            lexer = guess_lexer(code_snippet, stripnl=False, stripall=False)
            # Map Pygments lexer names to standardized language identifiers
            language_map = {
                "Python 3": "python",
                "JavaScript": "javascript",
                "TypeScript": "typescript",
                "C++": "cpp",
                "C#": "csharp",
                "Java": "java",
                "HTML": "html",
                "CSS": "css",
                "PHP": "php",
                "Ruby": "ruby",
                "Go": "go",
                "Rust": "rust",
                "Swift": "swift",
                "Kotlin": "kotlin"
            }
            
            detected_language = lexer.name
            return language_map.get(detected_language, detected_language.lower())
            
        except ClassNotFound:
            return "unknown"
        
    async def _arun(self, code_snippet: str) -> str:
        return self._run(code_snippet)