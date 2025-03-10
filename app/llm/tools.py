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


class CodeComplexityAnalysisTool(BaseTool):
    name = "code_complexity_analysis"
    description = "Analyzes the complexity of a code snippet and provides recommendations"
    
    def _run(self, code_snippet: str) -> str:
        """
        Analyze code complexity by counting:
        - Lines of code
        - Number of functions/methods
        - Nesting depth
        - Basic cyclomatic complexity indicators
        
        This is a simplified version - a real implementation would use AST parsing
        """
        lines = code_snippet.split('\n')
        num_lines = len([line for line in lines if line.strip()])
        
        # Simple approximation of functions/methods count
        function_keywords = ['def ', 'function ', 'method ', 'sub ', 'proc ', 'procedure ']
        num_functions = sum(1 for line in lines if any(keyword in line.lower() for keyword in function_keywords))
        
        # Simple approximation of nesting depth
        indentation_levels = []
        for line in lines:
            if line.strip():
                indentation = len(line) - len(line.lstrip())
                indentation_levels.append(indentation)
        
        max_nesting = 0
        if indentation_levels:
            max_nesting = max(indentation_levels) // 2  # Assuming 2 spaces per indent level
        
        # Simple approximation of complexity
        complexity_indicators = ['if ', 'for ', 'while ', 'switch ', 'catch ', 'case ']
        complexity_count = sum(1 for line in lines if any(indicator in line.lower() for indicator in complexity_indicators))
        
        # Generate analysis
        result = {
            "lines_of_code": num_lines,
            "function_count": num_functions,
            "max_nesting_depth": max_nesting,
            "complexity_indicators": complexity_count,
        }
        
        # Generate recommendations
        recommendations = []
        if num_lines > 100:
            recommendations.append("Consider breaking down this code into smaller modules")
        if max_nesting > 3:
            recommendations.append("High nesting depth detected. Consider refactoring to reduce complexity")
        if complexity_count > 10:
            recommendations.append("High cyclomatic complexity. Consider simplifying conditional logic")
            
        result["recommendations"] = recommendations if recommendations else ["No specific recommendations. Code complexity appears reasonable."]
        
        return str(result)
        
    async def _arun(self, code_snippet: str) -> str:
        return self._run(code_snippet)