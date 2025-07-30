from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from PIL import Image
import io
from datetime import datetime

from app.database import get_db, Recipe, Ingredient, User
from app.core.auth import get_current_user
from app.core.config import settings

router = APIRouter()

# Ensure image directories exist
IMAGES_DIR = os.path.join("static", "images")
RECIPE_IMAGES_DIR = os.path.join(IMAGES_DIR, "recipes")
INGREDIENT_IMAGES_DIR = os.path.join(IMAGES_DIR, "ingredients")

for directory in [IMAGES_DIR, RECIPE_IMAGES_DIR, INGREDIENT_IMAGES_DIR]:
    os.makedirs(directory, exist_ok=True)

def validate_image_file(file: UploadFile) -> bool:
    """Validate that the uploaded file is an image"""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    return file.content_type in allowed_types

def resize_image(image_data: bytes, max_size: tuple = (1920, 1080)) -> bytes:
    """Resize image while maintaining aspect ratio"""
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
    except Exception:
        # Return original if resize fails
        return image_data

def create_thumbnail(image_data: bytes, size: tuple = (300, 300)) -> bytes:
    """Create a thumbnail from image data"""
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=80, optimize=True)
            return output.getvalue()
    except Exception:
        return image_data

@router.post("/recipe/{recipe_id}/primary")
async def upload_recipe_primary_image(
    recipe_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload primary image for a recipe"""
    
    # Validate file
    if not validate_image_file(file):
        raise HTTPException(status_code=400, detail="File must be an image (JPEG, PNG, GIF, WebP)")
    
    # Check if recipe exists and user has permission
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this recipe")
    
    try:
        # Read and process image
        content = await file.read()
        
        # Resize image
        resized_content = resize_image(content)
        
        # Generate unique filename
        file_extension = ".jpg"  # Always save as JPG after processing
        unique_filename = f"recipe_{recipe_id}_primary_{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(RECIPE_IMAGES_DIR, unique_filename)
        
        # Save resized image
        with open(file_path, "wb") as f:
            f.write(resized_content)
        
        # Create thumbnail
        thumbnail_content = create_thumbnail(content)
        thumbnail_filename = f"recipe_{recipe_id}_primary_thumb_{uuid.uuid4().hex}{file_extension}"
        thumbnail_path = os.path.join(RECIPE_IMAGES_DIR, thumbnail_filename)
        
        with open(thumbnail_path, "wb") as f:
            f.write(thumbnail_content)
        
        # Remove old primary image if exists
        if recipe.primary_image:
            old_file_path = os.path.join(RECIPE_IMAGES_DIR, recipe.primary_image)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        # Update recipe with new image
        recipe.primary_image = unique_filename
        db.commit()
        
        return {
            "filename": unique_filename,
            "thumbnail": thumbnail_filename,
            "url": f"/api/images/recipe/{unique_filename}",
            "thumbnail_url": f"/api/images/recipe/{thumbnail_filename}",
            "message": "Primary image uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@router.post("/recipe/{recipe_id}/gallery")
async def upload_recipe_gallery_images(
    recipe_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload multiple images to recipe gallery"""
    
    # Check if recipe exists and user has permission
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this recipe")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed in gallery")
    
    uploaded_images = []
    current_gallery = recipe.gallery_images or []
    
    try:
        for file in files:
            if not validate_image_file(file):
                continue
            
            content = await file.read()
            resized_content = resize_image(content)
            
            unique_filename = f"recipe_{recipe_id}_gallery_{uuid.uuid4().hex}.jpg"
            file_path = os.path.join(RECIPE_IMAGES_DIR, unique_filename)
            
            with open(file_path, "wb") as f:
                f.write(resized_content)
            
            # Create thumbnail
            thumbnail_content = create_thumbnail(content)
            thumbnail_filename = f"recipe_{recipe_id}_gallery_thumb_{uuid.uuid4().hex}.jpg"
            thumbnail_path = os.path.join(RECIPE_IMAGES_DIR, thumbnail_filename)
            
            with open(thumbnail_path, "wb") as f:
                f.write(thumbnail_content)
            
            uploaded_images.append({
                "filename": unique_filename,
                "thumbnail": thumbnail_filename,
                "url": f"/api/images/recipe/{unique_filename}",
                "thumbnail_url": f"/api/images/recipe/{thumbnail_filename}"
            })
            
            current_gallery.append(unique_filename)
        
        # Update recipe gallery
        recipe.gallery_images = current_gallery
        db.commit()
        
        return {
            "uploaded_images": uploaded_images,
            "total_gallery_images": len(current_gallery),
            "message": f"Uploaded {len(uploaded_images)} images to gallery"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload gallery images: {str(e)}")

@router.post("/recipe/{recipe_id}/step/{step_number}")
async def upload_recipe_step_image(
    recipe_id: int,
    step_number: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload image for a specific recipe step"""
    
    if not validate_image_file(file):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Check if recipe exists and user has permission
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this recipe")
    
    try:
        content = await file.read()
        resized_content = resize_image(content)
        
        unique_filename = f"recipe_{recipe_id}_step_{step_number}_{uuid.uuid4().hex}.jpg"
        file_path = os.path.join(RECIPE_IMAGES_DIR, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(resized_content)
        
        # Update step images
        step_images = recipe.step_images or {}
        
        # Remove old step image if exists
        if str(step_number) in step_images:
            old_file_path = os.path.join(RECIPE_IMAGES_DIR, step_images[str(step_number)])
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        step_images[str(step_number)] = unique_filename
        recipe.step_images = step_images
        db.commit()
        
        return {
            "filename": unique_filename,
            "step_number": step_number,
            "url": f"/api/images/recipe/{unique_filename}",
            "message": f"Step {step_number} image uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload step image: {str(e)}")

@router.post("/ingredient/{ingredient_id}/primary")
async def upload_ingredient_primary_image(
    ingredient_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload primary image for an ingredient"""
    
    if not validate_image_file(file):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Check if ingredient exists
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    try:
        content = await file.read()
        resized_content = resize_image(content, max_size=(800, 600))  # Smaller for ingredients
        
        unique_filename = f"ingredient_{ingredient_id}_primary_{uuid.uuid4().hex}.jpg"
        file_path = os.path.join(INGREDIENT_IMAGES_DIR, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(resized_content)
        
        # Create thumbnail
        thumbnail_content = create_thumbnail(content, size=(200, 200))
        thumbnail_filename = f"ingredient_{ingredient_id}_primary_thumb_{uuid.uuid4().hex}.jpg"
        thumbnail_path = os.path.join(INGREDIENT_IMAGES_DIR, thumbnail_filename)
        
        with open(thumbnail_path, "wb") as f:
            f.write(thumbnail_content)
        
        # Remove old primary image if exists
        if ingredient.primary_image:
            old_file_path = os.path.join(INGREDIENT_IMAGES_DIR, ingredient.primary_image)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        # Update ingredient with new image
        ingredient.primary_image = unique_filename
        db.commit()
        
        return {
            "filename": unique_filename,
            "thumbnail": thumbnail_filename,
            "url": f"/api/images/ingredient/{unique_filename}",
            "thumbnail_url": f"/api/images/ingredient/{thumbnail_filename}",
            "message": "Ingredient image uploaded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload ingredient image: {str(e)}")

@router.get("/recipe/{filename}")
async def get_recipe_image(filename: str):
    """Serve recipe image"""
    file_path = os.path.join(RECIPE_IMAGES_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@router.get("/ingredient/{filename}")
async def get_ingredient_image(filename: str):
    """Serve ingredient image"""
    file_path = os.path.join(INGREDIENT_IMAGES_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@router.delete("/recipe/{recipe_id}/gallery/{filename}")
async def delete_recipe_gallery_image(
    recipe_id: int,
    filename: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete image from recipe gallery"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this recipe")
    
    # Remove from gallery
    gallery_images = recipe.gallery_images or []
    if filename in gallery_images:
        gallery_images.remove(filename)
        recipe.gallery_images = gallery_images
        
        # Delete file
        file_path = os.path.join(RECIPE_IMAGES_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.commit()
        return {"message": "Image deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Image not found in gallery")

@router.get("/recipe/{recipe_id}/images")
async def get_recipe_images(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """Get all images for a recipe"""
    
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    images = {
        "primary_image": None,
        "gallery_images": [],
        "step_images": {}
    }
    
    if recipe.primary_image:
        images["primary_image"] = {
            "filename": recipe.primary_image,
            "url": f"/api/images/recipe/{recipe.primary_image}"
        }
    
    if recipe.gallery_images:
        for img in recipe.gallery_images:
            images["gallery_images"].append({
                "filename": img,
                "url": f"/api/images/recipe/{img}"
            })
    
    if recipe.step_images:
        for step, img in recipe.step_images.items():
            images["step_images"][step] = {
                "filename": img,
                "url": f"/api/images/recipe/{img}"
            }
    
    return images 