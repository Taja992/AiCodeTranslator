from langchain.tools import BaseTool
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from typing import Optional, Type


class CodeLanguageDetectionTool(BaseTool):
    name = "code_language_detection"
    description = "Detects the programming language of a given code snippet"

    def _run(self, code_snippet: str) -> str:
        try:
            lexer = guess_lexer(code_snippet, stripnl=False, stripall=False)
            # creating a language map of common languages
            language_map = {
                "Python 3": "Python",
                "JavaScript": "JavaScript",
                "TypeScript": "TypeScript",
                "C++": "C++",
                "C#": "C#",
                "Java": "Java",
                "HTML": "HTML",
                "CSS": "CSS",
                "PHP": "PHP",
                "Ruby": "Ruby",
                "Go": "Go",
                "Rust": "Rust",
                "Swift": "Swift",
                "Kotlin": "Kotlin"
            }
            return language_map.get(lexer.name, lexer.name)
        except ClassNotFound:
            return "Unknown"
        
    async def _arun(self, code_snippet: str) -> str:
        return self._run(code_snippet)