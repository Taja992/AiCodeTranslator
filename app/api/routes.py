from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.llm.tools import CodeLanguageDetectionTool
from app.llm.chains import (
    create_code_explanation_chain,
    create_code_generation_chain,
    create_code_translation_chain
)
from app.llm.modelRegistry import get_model_for_task
from app.llm.modelTask import ModelTask
from app.utils.styleManager import StylePreferences, style_manager

router = APIRouter(prefix="/api", tags=["code"])

language_detector = CodeLanguageDetectionTool()

class CodeRequest(BaseModel):
    code: str
    language: str = None

class ExplanationResponse(BaseModel):
    explanation: str
    language: str

class GenerationResponse(BaseModel):
    code: str
    language: str

class TranslationRequest(BaseModel):
    code: str
    target_language: str

class GenerationDescriptionRequest(BaseModel):
    description: str
    language: str

@router.post("/explain_code", response_model=ExplanationResponse)
async def explain_code(request: CodeRequest):
    # Detect language if not provided
    detected_language = request.language
    if not detected_language:
        detected_language = language_detector._run(request.code)

    try:
        explanation_chain = create_code_explanation_chain()
        result = explanation_chain({
            "code": request.code,
            "language": detected_language
        })
        
        return {
            "explanation": result["explanation"],
            "language": detected_language
        }
    except Exception as e:
        return {
            "explanation": f"Explanation for the provided {detected_language} code\nError: {str(e)}", 
            "language": detected_language
        }

@router.get("/generate_code", response_model=GenerationResponse)
async def generate_code(description: str, language: str):
    try:
        # Test model connection before generating code
        llm = get_model_for_task(ModelTask.CODE_GENERATION)
        test_response = llm.invoke("Write a simple hello world in python")
        print(f"Debug: Test response: {test_response}")
        
        generation_chain = create_code_generation_chain()
        result = generation_chain({
            "description": description,
            "language": language,
            **style_manager.get_preferences_dict()
        })
        
        return {
            "code": result["code"],
            "language": language
        }
    except Exception as e:
        print(f"Generation error: {str(e)}")
        return {
            "code": f"// Error: {str(e)}", 
            "language": language
        }

@router.post("/translate_code", response_model=GenerationResponse)
async def translate_code(request: TranslationRequest):
    try:
        translation_chain = create_code_translation_chain()
        result = translation_chain({
            "code": request.code,
            "target_language": request.target_language,
        })
        
        return {
            "code": result.get("translated_code", "// Translation failed"),
            "language": request.target_language
        }
    except Exception as e:
        return {
            "code": f"// Error: {str(e)}",
            "language": request.target_language
        }

@router.post("/style_preferences", response_model=StylePreferences)
async def set_style_preferences(preferences: StylePreferences):
    try:
        style_manager.save_preferences(preferences)
    except Exception:
        pass
    return preferences

@router.get("/style_preferences", response_model=StylePreferences)
async def get_style_preferences():
    try:
        return style_manager.load_preferences()
    except Exception:
        return StylePreferences()

@router.get("/test_llm")
async def test_llm():
    try:
        from app.llm.modelRegistry import get_model_for_task
        from app.llm.modelTask import ModelTask
        
        llm = get_model_for_task(ModelTask.CODE_GENERATION)
        response = llm.invoke("Write a one-line Python print statement saying 'Hello from Ollama'")
        
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}