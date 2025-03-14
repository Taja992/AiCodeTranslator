# AI Code Translator

A powerful tool for generating, translating, and explaining code using LLMs with a user-friendly interface.

## Features

- **Code Translation**: Translate code between different programming languages
- **Code Explanation**: Get detailed explanations of code functionality
- **Code Generation**: Generate code from natural language descriptions
- **Customizable Style**: Set your code style preferences for generated and translated code

## Prerequisites

- Python 3.9 or higher
- [Ollama](https://ollama.ai/) installed on your system

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Install required Ollama models:
   ```bash
   ollama pull codellama:7b-instruct
   ollama pull wizardcoder:7b-python
   ```

6. Run the application:
   ```bash
   python main.py
   ```

This will automatically open the Flet UI application window on your desktop.

7. You can check your connection with ollama here: http://localhost:8000/api/test_llm

## Usage

1. **Translate Code**: Paste code in the source language and select the target language
2. **Explain Code**: Paste code to get a detailed explanation of its functionality
3. **Generate Code**: Describe what you want the code to do and select a language
4. **Settings**: Customize code style preferences such as indentation and naming conventions

## Project Structure

- `app/api/` - FastAPI routes and API definitions
- `app/llm/` - LLM models, chains, and tools
- `app/ui/` - Flet UI components
- `app/utils/` - Utility functions and classes

## Technologies Used

- **LangChain** - For LLM orchestration
- **Ollama** - For running local LLMs
- **FastAPI** - For API endpoints
- **Flet** - For the user interface
- **Pygments** - For language detection
