"""
AI Enhancement Endpoints for Iterum R&D Chef Notebook
Provides AI-powered recipe and menu parsing, creation, and analysis
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any
import logging
import json
import uuid
import os
from pathlib import Path

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.ai_recipe_parser import AIRecipeParser, ParsedRecipe
from app.services.ai_menu_parser import AIMenuParser, ParsedMenu
from app.services.ai_recipe_creator import AIRecipeCreator, RecipeSuggestion, RecipeVariation
from app.core.ai_config import get_ai_settings, validate_ai_configuration, AIFeatures

router = APIRouter(prefix="/api/ai", tags=["ai-enhancements"])
logger = logging.getLogger(__name__)

# Initialize AI services
ai_recipe_parser = AIRecipeParser()
ai_menu_parser = AIMenuParser()
ai_recipe_creator = AIRecipeCreator()

@router.get("/status")
async def get_ai_status():
    """Get AI system status and configuration"""
    try:
        config_status = validate_ai_configuration()
        settings = get_ai_settings()
        
        return {
            "ai_enabled": settings.enable_ai_features,
            "configuration": config_status,
            "features": {
                "recipe_parsing": AIFeatures.recipe_parsing_enabled(),
                "menu_parsing": AIFeatures.menu_parsing_enabled(),
                "ingredient_ai": AIFeatures.ingredient_ai_enabled(),
                "chef_assistant": AIFeatures.chef_assistant_enabled(),
                "nutritional_analysis": AIFeatures.nutritional_analysis_enabled(),
                "cost_estimation": AIFeatures.cost_estimation_enabled()
            },
            "providers": {
                "openai": bool(settings.openai_api_key),
                "anthropic": bool(settings.anthropic_api_key),
                "google": bool(settings.google_api_key),
                "azure": bool(settings.azure_api_key)
            }
        }
    except Exception as e:
        logger.error(f"AI status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI status check failed: {str(e)}")

@router.post("/recipe/parse-text")
async def ai_parse_recipe_text(
    text_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Parse recipe text using AI for enhanced accuracy"""
    try:
        if not AIFeatures.recipe_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI recipe parsing is disabled")
        
        recipe_text = text_data.get("text", "")
        image_url = text_data.get("image_url")
        
        if not recipe_text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        # Parse with AI
        parsed_recipe = await ai_recipe_parser.parse_recipe_with_ai(recipe_text, image_url)
        
        # Convert to dict format
        result = ai_recipe_parser._parsed_recipe_to_dict(parsed_recipe)
        
        return {
            "success": True,
            "recipe": result,
            "ai_enhanced": True,
            "confidence": parsed_recipe.confidence
        }
        
    except Exception as e:
        logger.error(f"AI recipe parsing failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI recipe parsing failed: {str(e)}")

@router.post("/recipe/enhance")
async def ai_enhance_recipe(
    recipe_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Enhance existing recipe with AI insights"""
    try:
        if not AIFeatures.recipe_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI recipe enhancement is disabled")
        
        # Enhance recipe with AI
        enhanced_recipe = await ai_recipe_parser.enhance_existing_recipe(recipe_data)
        
        return {
            "success": True,
            "enhanced_recipe": enhanced_recipe,
            "improvements": {
                "ingredients_standardized": True,
                "techniques_analyzed": True,
                "nutrition_estimated": True,
                "cost_estimated": True
            }
        }
        
    except Exception as e:
        logger.error(f"AI recipe enhancement failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI recipe enhancement failed: {str(e)}")

@router.post("/menu/parse-text")
async def ai_parse_menu_text(
    text_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Parse menu text using AI for enhanced accuracy"""
    try:
        if not AIFeatures.menu_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI menu parsing is disabled")
        
        menu_text = text_data.get("text", "")
        image_url = text_data.get("image_url")
        
        if not menu_text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        # Parse with AI
        parsed_menu = await ai_menu_parser.parse_menu_with_ai(menu_text, image_url)
        
        # Convert to dict format
        result = ai_menu_parser.parsed_menu_to_dict(parsed_menu)
        
        return {
            "success": True,
            "menu": result,
            "ai_enhanced": True,
            "confidence": parsed_menu.confidence
        }
        
    except Exception as e:
        logger.error(f"AI menu parsing failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI menu parsing failed: {str(e)}")

@router.post("/recipe/create-from-ingredients")
async def ai_create_recipe_from_ingredients(
    ingredients: List[str] = Form(...),
    cuisine: str = Form("Any"),
    difficulty: str = Form("Medium"),
    servings: int = Form(4),
    dietary: str = Form("None"),
    cook_time: str = Form("30-45 minutes"),
    current_user: User = Depends(get_current_user)
):
    """Create a recipe using specified ingredients"""
    try:
        if not AIFeatures.recipe_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI recipe creation is disabled")
        
        preferences = {
            "cuisine": cuisine,
            "difficulty": difficulty,
            "servings": servings,
            "dietary": dietary,
            "cook_time": cook_time
        }
        
        # Create recipe with AI
        recipe_suggestion = await ai_recipe_creator.create_recipe_from_ingredients(ingredients, preferences)
        
        # Convert to dict format
        result = {
            "title": recipe_suggestion.title,
            "description": recipe_suggestion.description,
            "cuisine": recipe_suggestion.cuisine,
            "difficulty": recipe_suggestion.difficulty,
            "prep_time": recipe_suggestion.prep_time,
            "cook_time": recipe_suggestion.cook_time,
            "servings": recipe_suggestion.servings,
            "ingredients": recipe_suggestion.ingredients,
            "instructions": recipe_suggestion.instructions,
            "tags": recipe_suggestion.tags,
            "confidence": recipe_suggestion.confidence,
            "ai_generated": True
        }
        
        return {
            "success": True,
            "recipe": result,
            "ai_enhanced": True
        }
        
    except Exception as e:
        logger.error(f"AI recipe creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI recipe creation failed: {str(e)}")

@router.post("/recipe/create-from-concept")
async def ai_create_recipe_from_concept(
    concept: str = Form(...),
    cuisine: str = Form("Any"),
    difficulty: str = Form("Medium"),
    servings: int = Form(4),
    dietary: str = Form("None"),
    cook_time: str = Form("30-45 minutes"),
    current_user: User = Depends(get_current_user)
):
    """Create a recipe from a concept or idea"""
    try:
        if not AIFeatures.recipe_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI recipe creation is disabled")
        
        preferences = {
            "cuisine": cuisine,
            "difficulty": difficulty,
            "servings": servings,
            "dietary": dietary,
            "cook_time": cook_time
        }
        
        # Create recipe with AI
        recipe_suggestion = await ai_recipe_creator.create_recipe_from_concept(concept, preferences)
        
        # Convert to dict format
        result = {
            "title": recipe_suggestion.title,
            "description": recipe_suggestion.description,
            "cuisine": recipe_suggestion.cuisine,
            "difficulty": recipe_suggestion.difficulty,
            "prep_time": recipe_suggestion.prep_time,
            "cook_time": recipe_suggestion.cook_time,
            "servings": recipe_suggestion.servings,
            "ingredients": recipe_suggestion.ingredients,
            "instructions": recipe_suggestion.instructions,
            "tags": recipe_suggestion.tags,
            "confidence": recipe_suggestion.confidence,
            "ai_generated": True
        }
        
        return {
            "success": True,
            "recipe": result,
            "ai_enhanced": True
        }
        
    except Exception as e:
        logger.error(f"AI recipe creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI recipe creation failed: {str(e)}")

@router.post("/recipe/generate-variations")
async def ai_generate_recipe_variations(
    recipe_data: dict,
    variation_types: List[str] = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Generate variations of an existing recipe"""
    try:
        if not AIFeatures.recipe_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI recipe variation is disabled")
        
        # Generate variations with AI
        variations = await ai_recipe_creator.generate_recipe_variations(recipe_data, variation_types)
        
        # Convert to dict format
        result = []
        for variation in variations:
            result.append({
                "variation_type": variation.variation_type,
                "title": variation.title,
                "description": variation.description,
                "changes": variation.changes,
                "new_ingredients": variation.new_ingredients,
                "modified_instructions": variation.modified_instructions,
                "confidence": variation.confidence,
                "ai_generated": True
            })
        
        return {
            "success": True,
            "variations": result,
            "ai_enhanced": True
        }
        
    except Exception as e:
        logger.error(f"AI recipe variation failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI recipe variation failed: {str(e)}")

@router.post("/recipe/suggest-improvements")
async def ai_suggest_recipe_improvements(
    recipe_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Suggest improvements for an existing recipe"""
    try:
        if not AIFeatures.recipe_parsing_enabled():
            raise HTTPException(status_code=400, detail="AI recipe improvement is disabled")
        
        # Get improvement suggestions with AI
        improvements = await ai_recipe_creator.suggest_recipe_improvements(recipe_data)
        
        return {
            "success": True,
            "improvements": improvements,
            "ai_enhanced": True
        }
        
    except Exception as e:
        logger.error(f"AI recipe improvement failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI recipe improvement failed: {str(e)}")

@router.post("/upload/ai-enhanced")
async def ai_enhanced_upload(
    file: UploadFile = File(...),
    file_type: str = Form("recipe"),  # "recipe" or "menu"
    current_user: User = Depends(get_current_user)
):
    """AI-enhanced file upload with intelligent parsing"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Save uploaded file temporarily
        temp_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_path = Path("uploads") / temp_filename
        temp_path.parent.mkdir(exist_ok=True)
        
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Extract text using existing OCR
        from app.services.ocr_processor import OCRProcessor
        ocr_processor = OCRProcessor()
        
        ocr_result = ocr_processor.extract_text_from_file(str(temp_path), file.content_type)
        
        if not ocr_result['success']:
            raise HTTPException(status_code=500, detail="Text extraction failed")
        
        extracted_text = ocr_result['text']
        
        # Process with AI based on file type
        if file_type == "recipe":
            if not AIFeatures.recipe_parsing_enabled():
                raise HTTPException(status_code=400, detail="AI recipe parsing is disabled")
            
            parsed_result = await ai_recipe_parser.parse_recipe_with_ai(extracted_text)
            result = ai_recipe_parser._parsed_recipe_to_dict(parsed_result)
            
        elif file_type == "menu":
            if not AIFeatures.menu_parsing_enabled():
                raise HTTPException(status_code=400, detail="AI menu parsing is disabled")
            
            parsed_result = await ai_menu_parser.parse_menu_with_ai(extracted_text)
            result = ai_menu_parser.parsed_menu_to_dict(parsed_result)
            
        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Use 'recipe' or 'menu'")
        
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass
        
        return {
            "success": True,
            "file_type": file_type,
            "original_filename": file.filename,
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "parsed_data": result,
            "ai_enhanced": True,
            "confidence": result.get("confidence", 0.0)
        }
        
    except Exception as e:
        logger.error(f"AI-enhanced upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI-enhanced upload failed: {str(e)}")

@router.get("/chef-assistant/insights")
async def get_chef_insights(
    recipe_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Get professional chef insights for a recipe"""
    try:
        if not AIFeatures.chef_assistant_enabled():
            raise HTTPException(status_code=400, detail="Chef assistant is disabled")
        
        # This would integrate with the chef assistant service
        # For now, return a placeholder response
        insights = {
            "technique_analysis": "Professional technique analysis would go here",
            "flavor_profile": "Flavor balance analysis would go here",
            "presentation_tips": "Plating and presentation suggestions would go here",
            "wine_pairing": "Wine pairing recommendations would go here",
            "scaling_advice": "Commercial scaling recommendations would go here",
            "cost_optimization": "Cost reduction suggestions would go here"
        }
        
        return {
            "success": True,
            "insights": insights,
            "ai_enhanced": True
        }
        
    except Exception as e:
        logger.error(f"Chef assistant insights failed: {e}")
        raise HTTPException(status_code=500, detail=f"Chef assistant insights failed: {str(e)}")

@router.post("/test-connection")
async def test_ai_connection():
    """Test AI service connection"""
    try:
        # Test with a simple prompt
        test_prompt = "Hello, this is a test. Please respond with 'AI connection successful'."
        
        # Try to call AI service
        if AIFeatures.recipe_parsing_enabled():
            response = await ai_recipe_parser._call_ai_service(test_prompt)
            return {
                "success": True,
                "message": "AI connection successful",
                "response": response[:100] + "..." if len(response) > 100 else response
            }
        else:
            return {
                "success": False,
                "message": "AI features are disabled"
            }
            
    except Exception as e:
        logger.error(f"AI connection test failed: {e}")
        return {
            "success": False,
            "message": f"AI connection failed: {str(e)}"
        }
