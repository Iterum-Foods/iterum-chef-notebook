from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import pandas as pd

from app.database import get_db, Ingredient
from app.schemas import IngredientCreate, IngredientUpdate, Ingredient, IngredientListResponse
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=Ingredient)
async def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new ingredient"""
    
    # Check if ingredient already exists
    existing_ingredient = db.query(Ingredient).filter(
        Ingredient.name.ilike(ingredient.name)
    ).first()
    
    if existing_ingredient:
        raise HTTPException(
            status_code=400,
            detail="Ingredient already exists"
        )
    
    db_ingredient = Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient


@router.get("/", response_model=IngredientListResponse)
async def get_ingredients(
    search: Optional[str] = Query(None, description="Search ingredients by name or category"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, le=100, description="Number of ingredients to return"),
    offset: int = Query(0, description="Number of ingredients to skip"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get ingredients with search and filtering"""
    
    query = db.query(Ingredient).filter(Ingredient.is_active == True)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Ingredient.name.ilike(search_term),
                Ingredient.category.ilike(search_term),
                Ingredient.description.ilike(search_term)
            )
        )
    
    if category:
        query = query.filter(Ingredient.category == category)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    ingredients = query.offset(offset).limit(limit).all()
    
    return IngredientListResponse(
        ingredients=ingredients,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{ingredient_id}", response_model=Ingredient)
async def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific ingredient by ID"""
    
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    return ingredient


@router.put("/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(
    ingredient_id: int,
    ingredient_update: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an ingredient"""
    
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Update fields
    update_data = ingredient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ingredient, field, value)
    
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient


@router.delete("/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Soft delete an ingredient (set is_active to False)"""
    
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    db_ingredient.is_active = False
    db.commit()
    
    return {"message": "Ingredient deleted successfully"}


@router.get("/categories/list")
async def get_ingredient_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all ingredient categories"""
    
    categories = db.query(Ingredient.category).filter(
        Ingredient.is_active == True,
        Ingredient.category.isnot(None)
    ).distinct().all()
    
    return {"categories": [cat[0] for cat in categories]}


@router.post("/import-csv")
async def import_ingredients_from_csv(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Import ingredients from CSV file (placeholder for future implementation)"""
    
    # This would read from your existing CSV file
    # For now, return a placeholder response
    return {
        "message": "CSV import functionality will be implemented",
        "note": "This will import from your existing Ingredient Database-Sheet1.csv.txt file"
    } 