"""
Recipe Scaling API with Baker's Percentage Support
Provides professional recipe scaling for larger batches
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import json
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recipe-scaling", tags=["recipe-scaling"])

class Ingredient(BaseModel):
    """Model for recipe ingredient"""
    name: str = Field(..., description="Ingredient name")
    amount: float = Field(..., description="Amount in original units")
    unit: str = Field(..., description="Unit of measurement")
    category: str = Field(default="other", description="Ingredient category")
    percentage: Optional[float] = Field(None, description="Baker's percentage")
    weight_grams: Optional[float] = Field(None, description="Weight in grams")

class Recipe(BaseModel):
    """Model for complete recipe"""
    name: str = Field(..., description="Recipe name")
    description: Optional[str] = Field(None, description="Recipe description")
    base_ingredient: str = Field(..., description="Base ingredient name (100%)")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients")
    yield_info: Optional[Dict[str, Any]] = Field(None, description="Yield information")
    created_by: Optional[str] = Field(None, description="User who created recipe")

class ScalingRequest(BaseModel):
    """Model for recipe scaling request"""
    recipe_id: Optional[str] = Field(None, description="Recipe ID to scale")
    recipe: Optional[Recipe] = Field(None, description="Recipe to scale")
    scaling_method: str = Field(..., description="Scaling method: percentage, factor, target_amount, batch_count")
    scaling_value: float = Field(..., description="Scaling value")
    target_unit: str = Field(default="g", description="Target unit for scaling")

class ScaledRecipe(BaseModel):
    """Model for scaled recipe result"""
    original_recipe: Recipe
    scaled_ingredients: List[Dict[str, Any]]
    scale_factor: float
    total_weight: float
    yield_info: Dict[str, Any]
    validation: Dict[str, Any]

class BakersPercentageRequest(BaseModel):
    """Model for baker's percentage calculation"""
    ingredients: List[Ingredient]
    base_ingredient: str

# Conversion factors to grams
CONVERSION_FACTORS = {
    'g': 1,
    'kg': 1000,
    'oz': 28.3495,
    'lb': 453.592,
    'cup_flour': 120,
    'cup_sugar': 200,
    'cup_butter': 227,
    'cup_liquid': 240,
    'tbsp': 15,
    'tsp': 5
}

# In-memory storage for demo (use database in production)
recipe_storage = {}
scaling_history = []

def convert_to_grams(amount: float, unit: str) -> float:
    """Convert ingredient amount to grams"""
    factor = CONVERSION_FACTORS.get(unit.lower(), 1)
    return amount * factor

def convert_from_grams(grams: float, target_unit: str) -> float:
    """Convert grams back to specified unit"""
    factor = CONVERSION_FACTORS.get(target_unit.lower(), 1)
    return grams / factor

def calculate_bakers_percentage(ingredients: List[Ingredient], base_ingredient: str) -> List[Dict[str, Any]]:
    """Calculate baker's percentage for ingredients"""
    # Find base ingredient weight
    base_weight = 0
    for ingredient in ingredients:
        if ingredient.name.lower() == base_ingredient.lower():
            base_weight = convert_to_grams(ingredient.amount, ingredient.unit)
            break
    
    if base_weight == 0:
        raise HTTPException(status_code=400, detail="Base ingredient not found or has zero weight")
    
    # Calculate percentages
    result = []
    for ingredient in ingredients:
        weight_grams = convert_to_grams(ingredient.amount, ingredient.unit)
        percentage = (weight_grams / base_weight) * 100
        
        result.append({
            "name": ingredient.name,
            "original_amount": ingredient.amount,
            "original_unit": ingredient.unit,
            "weight_grams": weight_grams,
            "percentage": percentage,
            "category": ingredient.category,
            "is_base": ingredient.name.lower() == base_ingredient.lower()
        })
    
    return result

def validate_recipe(ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate recipe proportions and provide feedback"""
    validation = {
        "valid": True,
        "warnings": [],
        "suggestions": [],
        "hydration": None,
        "salt_percentage": None,
        "yeast_percentage": None
    }
    
    # Get key ingredient percentages
    flour_pct = 0
    water_pct = 0
    salt_pct = 0
    yeast_pct = 0
    
    for ing in ingredients:
        name_lower = ing["name"].lower()
        if "flour" in name_lower:
            flour_pct += ing["percentage"]
        elif "water" in name_lower or "liquid" in ing["category"]:
            water_pct += ing["percentage"]
        elif "salt" in name_lower:
            salt_pct += ing["percentage"]
        elif "yeast" in name_lower:
            yeast_pct += ing["percentage"]
    
    # Calculate hydration for bread recipes
    if flour_pct > 0 and water_pct > 0:
        hydration = (water_pct / flour_pct) * 100
        validation["hydration"] = hydration
        
        if hydration < 50:
            validation["warnings"].append("Low hydration: Consider adding more liquid for better texture")
        elif hydration > 85:
            validation["warnings"].append("High hydration: Dough may be difficult to handle")
    
    # Check salt percentage
    if salt_pct > 0:
        validation["salt_percentage"] = salt_pct
        if salt_pct < 1.5:
            validation["warnings"].append("Low salt content: Consider increasing for better flavor")
        elif salt_pct > 3:
            validation["warnings"].append("High salt content: May inhibit yeast activity")
    
    # Check yeast percentage
    if yeast_pct > 0:
        validation["yeast_percentage"] = yeast_pct
        if yeast_pct < 0.5:
            validation["suggestions"].append("Low yeast: Longer fermentation time needed")
        elif yeast_pct > 3:
            validation["warnings"].append("High yeast content: May cause over-proofing")
    
    # Set overall validity
    validation["valid"] = len(validation["warnings"]) == 0
    
    return validation

@router.post("/calculate-percentage", response_model=List[Dict[str, Any]])
async def calculate_percentage(request: BakersPercentageRequest):
    """
    Calculate baker's percentage for a list of ingredients
    """
    try:
        result = calculate_bakers_percentage(request.ingredients, request.base_ingredient)
        logger.info(f"Calculated baker's percentage for {len(request.ingredients)} ingredients")
        return result
    except Exception as e:
        logger.error(f"Failed to calculate baker's percentage: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate percentage")

@router.post("/scale-recipe", response_model=ScaledRecipe)
async def scale_recipe(request: ScalingRequest):
    """
    Scale a recipe using various methods
    """
    try:
        # Use provided recipe or fetch from storage
        recipe = request.recipe
        if not recipe and request.recipe_id:
            recipe = recipe_storage.get(request.recipe_id)
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
        
        if not recipe:
            raise HTTPException(status_code=400, detail="No recipe provided")
        
        # Calculate baker's percentage first
        ingredients_with_percentage = calculate_bakers_percentage(
            recipe.ingredients, 
            recipe.base_ingredient
        )
        
        # Determine scale factor
        base_weight = next(
            (ing["weight_grams"] for ing in ingredients_with_percentage if ing["is_base"]), 
            0
        )
        
        if base_weight == 0:
            raise HTTPException(status_code=400, detail="Base ingredient not found")
        
        scale_factor = 1.0
        
        if request.scaling_method == "percentage":
            scale_factor = request.scaling_value / 100
        elif request.scaling_method == "factor":
            scale_factor = request.scaling_value
        elif request.scaling_method == "target_amount":
            target_weight = convert_to_grams(request.scaling_value, request.target_unit)
            scale_factor = target_weight / base_weight
        elif request.scaling_method == "batch_count":
            scale_factor = request.scaling_value
        else:
            raise HTTPException(status_code=400, detail="Invalid scaling method")
        
        # Scale all ingredients
        scaled_ingredients = []
        total_scaled_weight = 0
        
        for ing in ingredients_with_percentage:
            scaled_weight = ing["weight_grams"] * scale_factor
            scaled_amount = convert_from_grams(scaled_weight, ing["original_unit"])
            total_scaled_weight += scaled_weight
            
            scaled_ingredients.append({
                **ing,
                "scaled_amount": scaled_amount,
                "scaled_weight": scaled_weight,
                "scale_factor": scale_factor
            })
        
        # Calculate yield info
        yield_info = {
            "total_weight": total_scaled_weight,
            "scale_factor": scale_factor,
            "portions": {
                "individual": int(total_scaled_weight / 100),  # 100g portions
                "bread_loaves": int(total_scaled_weight / 500),  # 500g loaves
                "pizza_dough": int(total_scaled_weight / 250),  # 250g pizza dough
                "pastry_shells": int(total_scaled_weight / 50)  # 50g pastry shells
            }
        }
        
        # Validate scaled recipe
        validation = validate_recipe(scaled_ingredients)
        
        # Create scaled recipe result
        scaled_recipe = ScaledRecipe(
            original_recipe=recipe,
            scaled_ingredients=scaled_ingredients,
            scale_factor=scale_factor,
            total_weight=total_scaled_weight,
            yield_info=yield_info,
            validation=validation
        )
        
        # Store in history
        scaling_history.append({
            "recipe_name": recipe.name,
            "scale_factor": scale_factor,
            "method": request.scaling_method,
            "timestamp": datetime.now().isoformat(),
            "total_weight": total_scaled_weight
        })
        
        logger.info(f"Scaled recipe '{recipe.name}' by factor {scale_factor}")
        return scaled_recipe
        
    except Exception as e:
        logger.error(f"Failed to scale recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to scale recipe: {str(e)}")

@router.post("/save-recipe")
async def save_recipe(recipe: Recipe):
    """
    Save a recipe to storage
    """
    try:
        recipe_id = f"recipe_{len(recipe_storage) + 1}_{int(datetime.now().timestamp())}"
        recipe_storage[recipe_id] = recipe
        
        logger.info(f"Saved recipe: {recipe.name}")
        return {
            "success": True,
            "recipe_id": recipe_id,
            "message": f"Recipe '{recipe.name}' saved successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to save recipe: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save recipe")

@router.get("/recipes")
async def list_recipes():
    """
    List all saved recipes
    """
    try:
        recipes = []
        for recipe_id, recipe in recipe_storage.items():
            recipes.append({
                "id": recipe_id,
                "name": recipe.name,
                "description": recipe.description,
                "base_ingredient": recipe.base_ingredient,
                "ingredient_count": len(recipe.ingredients),
                "created_by": recipe.created_by
            })
        
        return {
            "success": True,
            "recipes": recipes,
            "total": len(recipes)
        }
        
    except Exception as e:
        logger.error(f"Failed to list recipes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list recipes")

@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str):
    """
    Get a specific recipe by ID
    """
    try:
        recipe = recipe_storage.get(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        return {
            "success": True,
            "recipe": recipe
        }
        
    except Exception as e:
        logger.error(f"Failed to get recipe: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get recipe")

@router.get("/scaling-history")
async def get_scaling_history(limit: int = 50):
    """
    Get recent scaling history
    """
    try:
        # Get most recent entries
        recent_history = sorted(
            scaling_history, 
            key=lambda x: x["timestamp"], 
            reverse=True
        )[:limit]
        
        return {
            "success": True,
            "history": recent_history,
            "total": len(scaling_history)
        }
        
    except Exception as e:
        logger.error(f"Failed to get scaling history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get scaling history")

@router.get("/conversion-factors")
async def get_conversion_factors():
    """
    Get available unit conversion factors
    """
    return {
        "success": True,
        "conversion_factors": CONVERSION_FACTORS,
        "supported_units": list(CONVERSION_FACTORS.keys())
    }

@router.post("/validate-recipe")
async def validate_recipe_endpoint(request: BakersPercentageRequest):
    """
    Validate a recipe and provide feedback
    """
    try:
        ingredients_with_percentage = calculate_bakers_percentage(
            request.ingredients, 
            request.base_ingredient
        )
        
        validation = validate_recipe(ingredients_with_percentage)
        
        return {
            "success": True,
            "validation": validation,
            "ingredients": ingredients_with_percentage
        }
        
    except Exception as e:
        logger.error(f"Failed to validate recipe: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to validate recipe")

# Health check for recipe scaling system
@router.get("/health")
async def scaling_health():
    """
    Health check for recipe scaling system
    """
    return {
        "status": "healthy",
        "service": "recipe-scaling",
        "total_recipes": len(recipe_storage),
        "scaling_operations": len(scaling_history),
        "features": {
            "bakers_percentage": True,
            "recipe_scaling": True,
            "recipe_validation": True,
            "conversion_support": True
        }
    }