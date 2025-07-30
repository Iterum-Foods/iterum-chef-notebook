from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db, Recipe, RecipeVersion, VersionIngredient, VersionInstruction, User
from app.schemas import RecipeVersionCreate, RecipeVersionUpdate, RecipeVersion, VersionListResponse
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/{recipe_id}/versions", response_model=RecipeVersion)
async def create_recipe_version(
    recipe_id: int,
    version: RecipeVersionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new version of a recipe"""
    
    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if user owns the recipe
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create versions for this recipe")
    
    # Check if version number already exists
    existing_version = db.query(RecipeVersion).filter(
        RecipeVersion.recipe_id == recipe_id,
        RecipeVersion.version_number == version.version_number
    ).first()
    
    if existing_version:
        raise HTTPException(
            status_code=400,
            detail=f"Version {version.version_number} already exists for this recipe"
        )
    
    # Create the version
    db_version = RecipeVersion(
        recipe_id=recipe_id,
        version_number=version.version_number,
        version_name=version.version_name,
        change_notes=version.change_notes,
        testing_notes=version.testing_notes,
        ratings=version.ratings,
        is_published=version.is_published,
        author_id=current_user.id
    )
    
    if version.is_published:
        db_version.published_at = datetime.utcnow()
    
    db.add(db_version)
    db.flush()  # Get the version ID
    
    # Add version ingredients
    for i, ingredient_data in enumerate(version.ingredients):
        db_ingredient = VersionIngredient(
            version_id=db_version.id,
            ingredient_id=ingredient_data.ingredient_id,
            quantity=ingredient_data.quantity,
            unit=ingredient_data.unit,
            notes=ingredient_data.notes,
            order_index=i
        )
        db.add(db_ingredient)
    
    # Add version instructions
    for i, instruction_data in enumerate(version.instructions):
        db_instruction = VersionInstruction(
            version_id=db_version.id,
            step_number=i + 1,
            instruction=instruction_data.instruction,
            tips=instruction_data.tips,
            time_estimate=instruction_data.time_estimate,
            temperature=instruction_data.temperature,
            equipment=instruction_data.equipment
        )
        db.add(db_instruction)
    
    db.commit()
    db.refresh(db_version)
    
    return db_version


@router.get("/{recipe_id}/versions", response_model=VersionListResponse)
async def get_recipe_versions(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all versions of a recipe"""
    
    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    versions = db.query(RecipeVersion).filter(
        RecipeVersion.recipe_id == recipe_id
    ).order_by(RecipeVersion.version_number).all()
    
    return VersionListResponse(versions=versions, total=len(versions))


@router.get("/{recipe_id}/versions/{version_id}", response_model=RecipeVersion)
async def get_recipe_version(
    recipe_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific version of a recipe"""
    
    version = db.query(RecipeVersion).filter(
        RecipeVersion.id == version_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    if not version:
        raise HTTPException(status_code=404, detail="Recipe version not found")
    
    return version


@router.put("/{recipe_id}/versions/{version_id}", response_model=RecipeVersion)
async def update_recipe_version(
    recipe_id: int,
    version_id: int,
    version_update: RecipeVersionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a recipe version"""
    
    # Check if version exists
    db_version = db.query(RecipeVersion).filter(
        RecipeVersion.id == version_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    if not db_version:
        raise HTTPException(status_code=404, detail="Recipe version not found")
    
    # Check if user owns the version
    if db_version.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this version")
    
    # Update fields
    update_data = version_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "is_published" and value and not db_version.is_published:
            # Set published_at when publishing for the first time
            setattr(db_version, "published_at", datetime.utcnow())
        setattr(db_version, field, value)
    
    db.commit()
    db.refresh(db_version)
    
    return db_version


@router.delete("/{recipe_id}/versions/{version_id}")
async def delete_recipe_version(
    recipe_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a recipe version"""
    
    # Check if version exists
    db_version = db.query(RecipeVersion).filter(
        RecipeVersion.id == version_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    if not db_version:
        raise HTTPException(status_code=404, detail="Recipe version not found")
    
    # Check if user owns the version
    if db_version.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this version")
    
    db.delete(db_version)
    db.commit()
    
    return {"message": "Recipe version deleted successfully"}


@router.post("/{recipe_id}/versions/{version_id}/publish")
async def publish_recipe_version(
    recipe_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Publish a recipe version"""
    
    # Check if version exists
    db_version = db.query(RecipeVersion).filter(
        RecipeVersion.id == version_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    if not db_version:
        raise HTTPException(status_code=404, detail="Recipe version not found")
    
    # Check if user owns the version
    if db_version.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to publish this version")
    
    db_version.is_published = True
    db_version.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_version)
    
    return {"message": "Recipe version published successfully", "version": db_version}


@router.post("/{recipe_id}/versions/{version_id}/add-rating")
async def add_version_rating(
    recipe_id: int,
    version_id: int,
    rating: dict,  # {"taste": 5, "texture": 4, "overall": 4.5}
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a rating to a recipe version"""
    
    # Check if version exists
    db_version = db.query(RecipeVersion).filter(
        RecipeVersion.id == version_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    if not db_version:
        raise HTTPException(status_code=404, detail="Recipe version not found")
    
    # Initialize ratings if None
    if db_version.ratings is None:
        db_version.ratings = {}
    
    # Add new rating
    db_version.ratings.update(rating)
    
    db.commit()
    db.refresh(db_version)
    
    return {"message": "Rating added successfully", "ratings": db_version.ratings}


@router.get("/{recipe_id}/versions/compare")
async def compare_recipe_versions(
    recipe_id: int,
    version1_id: int,
    version2_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compare two versions of a recipe"""
    
    # Get both versions
    version1 = db.query(RecipeVersion).filter(
        RecipeVersion.id == version1_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    version2 = db.query(RecipeVersion).filter(
        RecipeVersion.id == version2_id,
        RecipeVersion.recipe_id == recipe_id
    ).first()
    
    if not version1 or not version2:
        raise HTTPException(status_code=404, detail="One or both versions not found")
    
    # Compare versions
    comparison = {
        "version1": {
            "id": version1.id,
            "version_number": version1.version_number,
            "version_name": version1.version_name,
            "change_notes": version1.change_notes,
            "testing_notes": version1.testing_notes,
            "ratings": version1.ratings,
            "ingredients": version1.ingredients,
            "instructions": version1.instructions
        },
        "version2": {
            "id": version2.id,
            "version_number": version2.version_number,
            "version_name": version2.version_name,
            "change_notes": version2.change_notes,
            "testing_notes": version2.testing_notes,
            "ratings": version2.ratings,
            "ingredients": version2.ingredients,
            "instructions": version2.instructions
        }
    }
    
    return comparison 