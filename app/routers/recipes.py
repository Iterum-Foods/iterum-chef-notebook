from fastapi import APIRouter, Depends, HTTPException, Query, File, Form, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from typing import Optional, List
import json
from datetime import datetime
from pathlib import Path
from fastapi import status as http_status

from app.database import get_db, Recipe, RecipeIngredient, RecipeInstruction, User
from app.schemas import (
    RecipeCreate, RecipeUpdate, Recipe, RecipeListResponse,
    RecipeSearch, RecipeScaling
)
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=Recipe)
async def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe with ingredients and instructions"""
    
    # Create the recipe
    db_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        cuisine_type=recipe.cuisine_type,
        difficulty_level=recipe.difficulty_level,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        servings=recipe.servings,
        tags=recipe.tags,
        dietary_restrictions=recipe.dietary_restrictions,
        allergens=recipe.allergens,
        equipment_needed=recipe.equipment_needed,
        status=recipe.status,
        kitchen_type=recipe.kitchen_type,
        type=recipe.type if hasattr(recipe, 'type') and recipe.type else "dish",
        author_id=current_user.id
    )
    
    db.add(db_recipe)
    db.flush()  # Get the recipe ID
    
    # Add ingredients
    for i, ingredient_data in enumerate(recipe.ingredients):
        db_ingredient = RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ingredient_data.ingredient_id,
            quantity=ingredient_data.quantity,
            unit=ingredient_data.unit,
            notes=ingredient_data.notes,
            order_index=i
        )
        db.add(db_ingredient)
    
    # Add instructions
    for i, instruction_data in enumerate(recipe.instructions):
        db_instruction = RecipeInstruction(
            recipe_id=db_recipe.id,
            step_number=i + 1,
            instruction=instruction_data.instruction,
            tips=instruction_data.tips,
            time_estimate=instruction_data.time_estimate,
            temperature=instruction_data.temperature,
            equipment=instruction_data.equipment
        )
        db.add(db_instruction)
    
    db.commit()
    db.refresh(db_recipe)
    
    return db_recipe


@router.get("/", response_model=RecipeListResponse)
async def get_recipes(
    name: Optional[str] = Query(None, description="Search by recipe name/title"),
    description: Optional[str] = Query(None, description="Search by description"),
    ingredient: Optional[str] = Query(None, description="Search by ingredient name (includes prep recipes)"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags (comma-separated)"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine type"),
    type: Optional[str] = Query(None, description="Filter by recipe type (dish, prep, other)"),
    allergens: Optional[List[str]] = Query(None, description="Exclude recipes with these allergens (comma-separated)"),
    exclude_ingredient: Optional[str] = Query(None, description="Exclude recipes with this ingredient (or prep recipe)"),
    status: Optional[str] = Query(None, description="Filter by status (published, pending, draft, etc.)"),
    sort_by: str = Query("name", description="Sort by: name, date, popularity, etc."),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Advanced search and filtering for recipes."""
    query = db.query(Recipe)
    is_admin = getattr(current_user, 'is_admin', False)
    if not is_admin and (not status or status != "published"):
        query = query.filter(Recipe.author_id == current_user.id)
    if name:
        query = query.filter(Recipe.title.ilike(f"%{name}%"))
    if description:
        query = query.filter(Recipe.description.ilike(f"%{description}%"))
    if tags:
        for tag in tags:
            if tag:
                query = query.filter(func.json_extract(Recipe.tags, '$').contains(tag))
    if cuisine:
        query = query.filter(Recipe.cuisine_type == cuisine)
    if type:
        query = query.filter(Recipe.type == type)
    if status:
        query = query.filter(Recipe.status == status)
    if allergens:
        for allergen in allergens:
            if allergen:
                query = query.filter(~func.json_extract(Recipe.allergens, '$').contains(allergen))
    from app.database import RecipeIngredient
    from sqlalchemy import select
    # Ingredient search (by ingredient_name)
    if ingredient:
        subq = select(RecipeIngredient.recipe_id).where(RecipeIngredient.ingredient_name.ilike(f"%{ingredient}%"))
        query = query.filter(Recipe.id.in_(subq))
    if exclude_ingredient:
        subq = select(RecipeIngredient.recipe_id).where(RecipeIngredient.ingredient_name.ilike(f"%{exclude_ingredient}%"))
        query = query.filter(~Recipe.id.in_(subq))
    if sort_by == "name":
        order_col = Recipe.title
    elif sort_by == "date":
        order_col = Recipe.created_at
    else:
        order_col = Recipe.title
    if sort_order == "desc":
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())
    total = query.count()
    offset = (page - 1) * limit
    recipes = query.offset(offset).limit(limit).all()
    for recipe in recipes:
        if recipe.type == "dish":
            ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe.id).all()
            expanded_ingredients = expand_ingredients_with_prep(db, ingredients)
            recipe.ingredients = expanded_ingredients
    return RecipeListResponse(
        recipes=recipes,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific recipe by ID, expanding prep recipe components if type='dish'"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Expand ingredients if dish
    if recipe.type == "dish":
        ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe.id).all()
        expanded_ingredients = expand_ingredients_with_prep(db, ingredients)
        recipe.ingredients = expanded_ingredients
    
    return recipe


@router.put("/{recipe_id}", response_model=Recipe)
async def update_recipe(
    recipe_id: int,
    recipe_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a recipe with ingredients and instructions"""
    
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if user owns the recipe
    if db_recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this recipe")
    
    try:
        # Update basic recipe fields
        basic_fields = ['title', 'description', 'cuisine_type', 'difficulty_level', 
                       'prep_time', 'cook_time', 'servings', 'tags', 'dietary_restrictions', 
                       'allergens', 'equipment_needed', 'status', 'kitchen_type']
        
        for field in basic_fields:
            if field in recipe_update:
                setattr(db_recipe, field, recipe_update[field])
        
        # Update ingredients if provided
        if 'ingredients' in recipe_update:
            # Remove existing ingredients
            db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).delete()
            
            # Add new ingredients
            for i, ingredient_data in enumerate(recipe_update['ingredients']):
                db_ingredient = RecipeIngredient(
                    recipe_id=recipe_id,
                    ingredient_id=1,  # Default ingredient ID
                    quantity=ingredient_data.get('amount', 0),
                    unit=ingredient_data.get('unit', ''),
                    notes=ingredient_data.get('name', ''),
                    order_index=i
                )
                db.add(db_ingredient)
        
        # Update instructions if provided
        if 'instructions' in recipe_update:
            # Remove existing instructions
            db.query(RecipeInstruction).filter(RecipeInstruction.recipe_id == recipe_id).delete()
            
            # Add new instructions
            for i, instruction_data in enumerate(recipe_update['instructions']):
                db_instruction = RecipeInstruction(
                    recipe_id=recipe_id,
                    step_number=i + 1,
                    instruction=instruction_data.get('instruction', ''),
                    tips=instruction_data.get('tips', ''),
                    time_estimate=instruction_data.get('time_estimate', None),
                    temperature=instruction_data.get('temperature', None),
                    equipment=instruction_data.get('equipment', None)
                )
                db.add(db_instruction)
        
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating recipe: {str(e)}")


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a recipe"""
    
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if user owns the recipe
    if db_recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this recipe")
    
    db.delete(db_recipe)
    db.commit()
    
    return {"message": "Recipe deleted successfully"}


@router.post("/{recipe_id}/scale")
async def scale_recipe(
    recipe_id: int,
    scaling: RecipeScaling,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Scale a recipe to different serving sizes with intelligent unit conversion"""
    
    # Get the recipe
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Get recipe ingredients
    recipe_ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()
    
    # Calculate scaling factor
    scaling_factor = scaling.target_servings / scaling.current_servings
    
    # Scale ingredients with unit conversion
    scaled_ingredients = []
    for ingredient in recipe_ingredients:
        original_quantity = float(ingredient.quantity or 0.0)
        original_unit = str(ingredient.unit or "")
        
        # Scale the quantity
        scaled_quantity = original_quantity * scaling_factor
        
        # Convert units if requested
        if scaling.convert_units:
            converted = convert_units(scaled_quantity, original_unit)
            final_quantity = converted['quantity']
            final_unit = converted['unit']
        else:
            final_quantity = round(scaled_quantity, scaling.round_decimals)
            final_unit = original_unit
        
        scaled_ingredient = {
            "ingredient_name": ingredient.notes or "Unknown",
            "original_quantity": original_quantity,
            "original_unit": original_unit,
            "scaled_quantity": final_quantity,
            "scaled_unit": final_unit,
            "notes": ingredient.notes,
            "scaling_factor": scaling_factor
        }
        scaled_ingredients.append(scaled_ingredient)
    
    # Scale timing if applicable
    scaled_prep_time = None
    scaled_cook_time = None
    
    if recipe.prep_time and scaling.preserve_ratios:
        scaled_prep_time = round(recipe.prep_time * scaling_factor)
    
    if recipe.cook_time and scaling.preserve_ratios:
        scaled_cook_time = round(recipe.cook_time * scaling_factor)
    
    # Get recipe instructions
    recipe_instructions = db.query(RecipeInstruction).filter(RecipeInstruction.recipe_id == recipe_id).order_by(RecipeInstruction.step_number).all()
    
    return {
        "recipe_title": recipe.title,
        "original_servings": scaling.current_servings,
        "target_servings": scaling.target_servings,
        "scaling_factor": scaling_factor,
        "scaled_ingredients": scaled_ingredients,
        "scaled_prep_time": scaled_prep_time,
        "scaled_cook_time": scaled_cook_time,
        "instructions": [inst.instruction for inst in recipe_instructions],
        "kitchen_type": scaling.kitchen_type,
        "scaling_timestamp": datetime.now().isoformat()
    }


def convert_units(quantity: float, unit: str) -> dict:
    """Convert units to more practical measurements"""
    unit = unit.lower()
    
    # Weight conversions
    if unit == 'g':
        if quantity >= 1000:
            return {'quantity': round(quantity / 1000, 2), 'unit': 'kg'}
        elif quantity >= 453.592:
            return {'quantity': round(quantity / 453.592, 2), 'unit': 'lb'}
        else:
            return {'quantity': round(quantity, 1), 'unit': 'g'}
    
    elif unit == 'kg':
        if quantity >= 2.20462:
            return {'quantity': round(quantity * 2.20462, 2), 'unit': 'lb'}
        else:
            return {'quantity': round(quantity, 2), 'unit': 'kg'}
    
    elif unit == 'lb':
        if quantity >= 16:
            return {'quantity': round(quantity * 16, 2), 'unit': 'oz'}
        else:
            return {'quantity': round(quantity, 2), 'unit': 'lb'}
    
    # Volume conversions
    elif unit == 'ml':
        if quantity >= 1000:
            return {'quantity': round(quantity / 1000, 2), 'unit': 'L'}
        elif quantity >= 236.588:
            return {'quantity': round(quantity / 236.588, 2), 'unit': 'cup'}
        elif quantity >= 14.7868:
            return {'quantity': round(quantity / 14.7868, 2), 'unit': 'tbsp'}
        elif quantity >= 4.92892:
            return {'quantity': round(quantity / 4.92892, 2), 'unit': 'tsp'}
        else:
            return {'quantity': round(quantity, 1), 'unit': 'ml'}
    
    elif unit == 'l':
        if quantity >= 4.22675:
            return {'quantity': round(quantity * 4.22675, 2), 'unit': 'cup'}
        else:
            return {'quantity': round(quantity, 2), 'unit': 'L'}
    
    elif unit == 'cup':
        if quantity >= 16:
            return {'quantity': round(quantity * 16, 2), 'unit': 'tbsp'}
        elif quantity >= 48:
            return {'quantity': round(quantity * 48, 2), 'unit': 'tsp'}
        else:
            return {'quantity': round(quantity, 2), 'unit': 'cup'}
    
    elif unit == 'tbsp':
        if quantity >= 3:
            return {'quantity': round(quantity / 3, 2), 'unit': 'tbsp'}
        else:
            return {'quantity': round(quantity, 1), 'unit': 'tbsp'}
    
    elif unit == 'tsp':
        if quantity >= 3:
            return {'quantity': round(quantity / 3, 2), 'unit': 'tbsp'}
        else:
            return {'quantity': round(quantity, 1), 'unit': 'tsp'}
    
    # Default: return original
    return {'quantity': round(quantity, 2), 'unit': unit}


@router.get("/{recipe_id}/versions")
async def get_recipe_versions(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all versions of a recipe"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # For now, just return the recipe itself as there's no versioning system yet
    versions = [recipe]
    
    return {
        "recipe": recipe,
        "versions": versions
    }


@router.post("/{recipe_id}/publish")
async def publish_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Publish a recipe (change status to published)"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to publish this recipe")
    
    recipe.status = "published"
    db.commit()
    db.refresh(recipe)
    
    return {"message": "Recipe published successfully", "recipe": recipe} 


@router.get("/{recipe_id}/scaling-history")
async def get_scaling_history(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get scaling history for a recipe"""
    
    # Get the recipe
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # For now, return empty history (you could implement a scaling_history table)
    # In a real implementation, you'd store scaling operations in a database table
    return {
        "recipe_id": recipe_id,
        "recipe_title": recipe.title,
        "scaling_history": []
    }


@router.post("/scale-batch")
async def scale_multiple_recipes(
    scaling_data: List[RecipeScaling],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Scale multiple recipes at once"""
    
    results = []
    
    for scaling in scaling_data:
        try:
            # Get the recipe
            recipe = db.query(Recipe).filter(Recipe.id == scaling.recipe_id).first()
            if not recipe:
                results.append({
                    "recipe_id": scaling.recipe_id,
                    "success": False,
                    "error": "Recipe not found"
                })
                continue
            
            # Get recipe ingredients
            recipe_ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == scaling.recipe_id).all()
            
            # Calculate scaling factor
            scaling_factor = scaling.target_servings / scaling.current_servings
            
            # Scale ingredients
            scaled_ingredients = []
            for ingredient in recipe_ingredients:
                original_quantity = float(ingredient.quantity or 0.0)
                original_unit = str(ingredient.unit or "")
                scaled_quantity = original_quantity * scaling_factor
                
                if scaling.convert_units:
                    converted = convert_units(scaled_quantity, original_unit)
                    final_quantity = converted['quantity']
                    final_unit = converted['unit']
                else:
                    final_quantity = round(scaled_quantity, scaling.round_decimals)
                    final_unit = original_unit
                
                scaled_ingredients.append({
                    "ingredient_name": ingredient.notes or "Unknown",
                    "original_quantity": original_quantity,
                    "original_unit": original_unit,
                    "scaled_quantity": final_quantity,
                    "scaled_unit": final_unit
                })
            
            results.append({
                "recipe_id": scaling.recipe_id,
                "recipe_title": recipe.title,
                "success": True,
                "scaling_factor": scaling_factor,
                "scaled_ingredients": scaled_ingredients
            })
            
        except Exception as e:
            results.append({
                "recipe_id": scaling.recipe_id,
                "success": False,
                "error": str(e)
            })
    
    return {
        "batch_results": results,
        "total_recipes": len(scaling_data),
        "successful_scales": len([r for r in results if r["success"]])
    } 


@router.post("/bulk-upload")
async def bulk_upload_recipes(
    files: List[UploadFile] = File(...),
    default_category: str = Form("Imported"),
    default_cuisine: str = Form("Unknown"),
    default_servings: int = Form(4),
    auto_tag: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bulk upload multiple recipe files"""
    
    results = []
    
    for file in files:
        try:
            # Parse recipe based on file type
            recipe_data = await parse_recipe_file(file, default_category, default_cuisine, default_servings, auto_tag)
            
            if recipe_data:
                # Create recipe in database
                db_recipe = Recipe(
                    title=recipe_data["name"],
                    description=recipe_data.get("description", ""),
                    cuisine_type=recipe_data.get("cuisine", default_cuisine),
                    difficulty_level=recipe_data.get("difficulty", "Medium"),
                    prep_time=recipe_data.get("prep_time", 0),
                    cook_time=recipe_data.get("cook_time", 0),
                    servings=recipe_data.get("servings", default_servings),
                    tags=recipe_data.get("tags", []),
                    status="draft",
                    kitchen_type="home",
                    type=recipe_data.get("type", "dish"),
                    author_id=current_user.id
                )
                
                db.add(db_recipe)
                db.flush()  # Get the recipe ID
                
                # Add ingredients
                for i, ingredient_data in enumerate(recipe_data.get("ingredients", [])):
                    db_ingredient = RecipeIngredient(
                        recipe_id=db_recipe.id,
                        ingredient_id=1,  # Default ingredient ID
                        quantity=ingredient_data.get("amount", 0),
                        unit=ingredient_data.get("unit", ""),
                        notes=ingredient_data.get("name", ""),
                        order_index=i
                    )
                    db.add(db_ingredient)
                
                # Add instructions
                for i, instruction in enumerate(recipe_data.get("instructions", [])):
                    db_instruction = RecipeInstruction(
                        recipe_id=db_recipe.id,
                        step_number=i + 1,
                        instruction=instruction
                    )
                    db.add(db_instruction)
                
                results.append({
                    "filename": file.filename,
                    "success": True,
                    "recipe_id": db_recipe.id,
                    "recipe_title": db_recipe.title
                })
            else:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Could not parse recipe data"
                })
                
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    db.commit()
    
    return {
        "total_files": len(files),
        "successful_uploads": len([r for r in results if r["success"]]),
        "failed_uploads": len([r for r in results if not r["success"]]),
        "results": results
    }


async def parse_recipe_file(file: UploadFile, default_category: str, default_cuisine: str, default_servings: int, auto_tag: bool) -> Optional[dict]:
    """Parse recipe file based on its type"""
    
    content = await file.read()
    filename = file.filename.lower() if file.filename else "unknown"
    
    # Basic recipe structure
    recipe_data = {
        "name": file.filename.split('.')[0] if file.filename else "Unknown Recipe",
        "description": f"Imported from {file.filename}" if file.filename else "Imported recipe",
        "category": default_category,
        "cuisine": default_cuisine,
        "servings": default_servings,
        "prep_time": 0,
        "cook_time": 0,
        "difficulty": "Medium",
        "ingredients": [],
        "instructions": [],
        "tags": ["Imported"] if auto_tag else []
    }
    
    try:
        if filename.endswith('.pdf'):
            # PDF parsing requires additional libraries (PyPDF2, pdfplumber)
            recipe_data["description"] += " (PDF import - text parsing not yet implemented)"
            
        elif filename.endswith(('.xlsx', '.xls')):
            # Excel parsing requires pandas or openpyxl
            recipe_data["description"] += " (Excel import - structured parsing not yet implemented)"
            
        elif filename.endswith(('.docx', '.doc')):
            # Word document parsing requires python-docx
            recipe_data["description"] += " (Word document import - text extraction not yet implemented)"
            
        elif filename.endswith('.txt'):
            # Text parsing
            text_content = content.decode('utf-8')
            recipe_data.update(parse_text_recipe(text_content, recipe_data))
            
        elif filename.endswith('.csv'):
            # CSV parsing
            csv_content = content.decode('utf-8')
            recipe_data.update(parse_csv_recipe(csv_content, recipe_data))
            
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return None
    
    return recipe_data


def parse_text_recipe(text: str, base_recipe: dict) -> dict:
    """Parse text file for recipe data"""
    
    lines = text.split('\n')
    recipe = base_recipe.copy()
    
    in_ingredients = False
    in_instructions = False
    ingredients = []
    instructions = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        line_lower = line.lower()
        
        if 'ingredients' in line_lower:
            in_ingredients = True
            in_instructions = False
            continue
            
        if 'instructions' in line_lower or 'directions' in line_lower:
            in_ingredients = False
            in_instructions = True
            continue
            
        if in_ingredients:
            # Simple ingredient parsing
            ingredients.append({
                "name": line,
                "amount": 0,
                "unit": ""
            })
        elif in_instructions:
            instructions.append(line)
        else:
            # Try to extract recipe name from first few lines
            if not recipe["name"] or recipe["name"] == base_recipe["name"]:
                if len(line) > 3 and len(line) < 100:
                    recipe["name"] = line
    
    recipe["ingredients"] = ingredients
    recipe["instructions"] = instructions
    
    return recipe


def parse_csv_recipe(csv_content: str, base_recipe: dict) -> dict:
    """Parse CSV file for recipe data"""
    
    lines = csv_content.split('\n')
    recipe = base_recipe.copy()
    
    if len(lines) < 2:
        return recipe
    
    # Assume first row is headers
    headers = lines[0].split(',')
    data = lines[1].split(',')
    
    # Map CSV columns to recipe fields
    for i, header in enumerate(headers):
        header = header.strip().lower()
        if i < len(data):
            value = data[i].strip()
            
            if 'name' in header or 'title' in header:
                recipe["name"] = value
            elif 'description' in header:
                recipe["description"] = value
            elif 'category' in header:
                recipe["category"] = value
            elif 'cuisine' in header:
                recipe["cuisine"] = value
            elif 'servings' in header:
                try:
                    recipe["servings"] = int(value)
                except:
                    pass
            elif 'prep' in header:
                try:
                    recipe["prep_time"] = int(value)
                except:
                    pass
            elif 'cook' in header:
                try:
                    recipe["cook_time"] = int(value)
                except:
                    pass
    
    return recipe 


@router.get("/library")
async def get_recipe_library(
    search: str = Query(None),
    category: str = Query(None),
    cuisine: str = Query(None),
    difficulty: str = Query(None),
    sort_by: str = Query("name"),
    sort_order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipe library with filtering and pagination - shows only current user's recipes"""
    
    query = db.query(Recipe).filter(Recipe.author_id == current_user.id)
    
    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Recipe.title.ilike(search_term),
                Recipe.description.ilike(search_term),
                Recipe.cuisine_type.ilike(search_term)
            )
        )
    
    if cuisine:
        query = query.filter(Recipe.cuisine_type == cuisine)
    
    if difficulty:
        query = query.filter(Recipe.difficulty_level == difficulty)
    
    # Apply sorting
    if sort_by == "name":
        order_col = Recipe.title
    elif sort_by == "cuisine":
        order_col = Recipe.cuisine_type
    elif sort_by == "servings":
        order_col = Recipe.servings
    elif sort_by == "time":
        # Handle nullable fields for time calculation
        order_col = func.coalesce(Recipe.prep_time, 0) + func.coalesce(Recipe.cook_time, 0)
    elif sort_by == "date":
        order_col = Recipe.created_at
    else:
        order_col = Recipe.title
    
    if sort_order == "desc":
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())
    
    # Apply pagination
    total = query.count()
    recipes = query.offset((page - 1) * limit).limit(limit).all()
    
    # Convert to response format
    recipe_list = []
    for recipe in recipes:
        recipe_data = {
            "id": recipe.id,
            "name": recipe.title,
            "description": recipe.description,
            "cuisine": recipe.cuisine_type,
            "servings": recipe.servings,
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "difficulty": recipe.difficulty_level,
            "tags": recipe.tags or [],
            "status": recipe.status,
            "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
            "updated_at": recipe.updated_at.isoformat() if recipe.updated_at else None
        }
        
        # Get ingredients
        ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe.id).all()
        recipe_data["ingredients"] = [
            {
                "name": ing.notes or "Unknown ingredient",
                "amount": ing.quantity,
                "unit": ing.unit
            }
            for ing in ingredients
        ]
        
        # Get instructions
        instructions = db.query(RecipeInstruction).filter(RecipeInstruction.recipe_id == recipe.id).order_by(RecipeInstruction.step_number).all()
        recipe_data["instructions"] = [inst.instruction for inst in instructions]
        
        recipe_list.append(recipe_data)
    
    return {
        "recipes": recipe_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        },
        "filters": {
            "search": search,
            "category": category,
            "cuisine": cuisine,
            "difficulty": difficulty,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
    } 

# --- Helper: Serialize Recipe to Dict ---
def recipe_to_dict(recipe):
    return {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "cuisine_type": recipe.cuisine_type,
        "difficulty_level": recipe.difficulty_level,
        "prep_time": recipe.prep_time,
        "cook_time": recipe.cook_time,
        "servings": recipe.servings,
        "tags": recipe.tags,
        "status": recipe.status,
        "type": recipe.type,
        "author_id": recipe.author_id,
        "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
        "updated_at": recipe.updated_at.isoformat() if recipe.updated_at else None
    }

# --- Helper: Expand prep recipe components in ingredients ---
def expand_ingredients_with_prep(db, ingredients):
    expanded = []
    for ing in ingredients:
        ing_dict = {
            "id": ing.id,
            "ingredient_id": ing.ingredient_id,
            "prep_recipe_id": ing.prep_recipe_id,
            "quantity": ing.quantity,
            "unit": ing.unit,
            "notes": ing.notes,
            "is_prep": ing.is_prep,
            "order_index": ing.order_index
        }
        if ing.is_prep and ing.prep_recipe_id:
            prep_recipe = db.query(Recipe).filter(Recipe.id == ing.prep_recipe_id).first()
            if prep_recipe:
                ing_dict["prep_recipe"] = recipe_to_dict(prep_recipe)
        expanded.append(ing_dict)
    return expanded

@router.get("/review/pending")
async def get_pending_reviews(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recipes pending review (admin: all, user: own)"""
    offset = (page - 1) * limit
    # If admin, show all pending; else, only own
    is_admin = getattr(current_user, 'is_admin', False)
    query = db.query(Recipe).filter(Recipe.status == "pending")
    if not is_admin:
        query = query.filter(Recipe.author_id == current_user.id)
    total = query.count()
    recipes = query.offset(offset).limit(limit).all()
    return {
        "recipes": [recipe_to_dict(r) for r in recipes],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.post("/{recipe_id}/review")
async def review_recipe(
    recipe_id: int,
    review_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Review a recipe (approve/reject)"""
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.created_by == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe.review_status = review_data.get("status", "approved")
    recipe.reviewed_at = datetime.utcnow()
    recipe.reviewed_by = current_user.id
    
    if review_data.get("notes"):
        recipe.notes = review_data["notes"]
    
    db.commit()
    
    return {"message": f"Recipe {recipe.review_status}", "recipe_id": recipe_id}


@router.post("/review/batch")
async def batch_review_recipes(
    recipe_ids: List[int] = Form(...),
    action: str = Form(...),  # "approve" or "reject"
    notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Batch review multiple recipes"""
    
    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")
    
    results = []
    
    for recipe_id in recipe_ids:
        try:
            recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
            if not recipe:
                results.append({"recipe_id": recipe_id, "success": False, "error": "Recipe not found"})
                continue
            
            if recipe.author_id != current_user.id:
                results.append({"recipe_id": recipe_id, "success": False, "error": "Not authorized"})
                continue
            
            # Update review status
            if action == "approve":
                recipe.status = "published"
            else:
                recipe.status = "rejected"
            
            if notes:
                recipe.description = f"{recipe.description or ''}\n\nReview Notes: {notes}"
            
            results.append({"recipe_id": recipe_id, "success": True})
            
        except Exception as e:
            results.append({"recipe_id": recipe_id, "success": False, "error": str(e)})
    
    db.commit()
    
    successful = len([r for r in results if r["success"]])
    failed = len(results) - successful
    
    return {
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "results": results
    } 


@router.get("/{recipe_id}/original-file")
async def get_original_file_content(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the original file content for a recipe"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this recipe")
    
    # For now, return recipe data as file content since we don't have source file tracking
    return {
        "content": f"Recipe: {recipe.title}\n\nDescription: {recipe.description or 'No description'}\n\nThis is the parsed recipe data since the original file is not available.",
        "filename": f"{recipe.title}.txt",
        "file_type": "text"
    }


@router.get("/{recipe_id}/download-original")
async def download_original_file(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download the original file for a recipe"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this recipe")
    
    # For now, create a text file from recipe data since we don't have original files
    recipe_content = f"""Recipe: {recipe.title}

Description: {recipe.description or 'No description'}

Ingredients:
"""
    
    # Get ingredients
    ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe_id).all()
    for ing in ingredients:
        recipe_content += f"- {ing.quantity} {ing.unit} {ing.notes or 'Unknown ingredient'}\n"
    
    recipe_content += "\nInstructions:\n"
    
    # Get instructions
    instructions = db.query(RecipeInstruction).filter(RecipeInstruction.recipe_id == recipe_id).order_by(RecipeInstruction.step_number).all()
    for i, inst in enumerate(instructions, 1):
        recipe_content += f"{i}. {inst.instruction}\n"
    
    from fastapi.responses import Response
    return Response(
        content=recipe_content.encode('utf-8'),
        media_type='text/plain',
        headers={
            "Content-Disposition": f"attachment; filename={recipe.title}.txt"
        }
    ) 

# --- Admin Endpoints ---
from fastapi import HTTPException

def require_admin(user):
    if not getattr(user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Admin privileges required.")

@router.get("/admin/recipes")
async def admin_list_recipes(
    page: int = 1,
    limit: int = 20,
    status: str = None,
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    query = db.query(Recipe)
    if status:
        query = query.filter(Recipe.status == status)
    if user_id:
        query = query.filter(Recipe.author_id == user_id)
    total = query.count()
    recipes = query.offset((page-1)*limit).limit(limit).all()
    return {
        "recipes": [recipe_to_dict(r) for r in recipes],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.post("/admin/recipes/{recipe_id}/approve")
async def admin_approve_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe.status = "published"
    db.commit()
    return {"message": "Recipe approved and published", "recipe_id": recipe_id}

@router.post("/admin/recipes/{recipe_id}/reject")
async def admin_reject_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe.status = "rejected"
    db.commit()
    return {"message": "Recipe rejected", "recipe_id": recipe_id}

@router.post("/admin/recipes/bulk-action")
async def admin_bulk_action(
    action: str,
    recipe_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    valid_actions = {"approve": "published", "reject": "rejected", "publish": "published", "unpublish": "draft"}
    if action not in valid_actions:
        raise HTTPException(status_code=400, detail=f"Invalid action: {action}")
    status_value = valid_actions[action]
    updated = 0
    for rid in recipe_ids:
        recipe = db.query(Recipe).filter(Recipe.id == rid).first()
        if recipe:
            recipe.status = status_value
            updated += 1
    db.commit()
    return {"message": f"{action.title()}d {updated} recipes.", "updated": updated} 