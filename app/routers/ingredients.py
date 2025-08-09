from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict, Any
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

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
    """Import ingredients from CSV file - requires implementation with file upload"""
    
    # Implementation requires:
    # 1. File upload parameter
    # 2. CSV parsing with pandas
    # 3. Ingredient validation and bulk insert
    return {
        "message": "CSV import requires file upload parameter and CSV parsing implementation",
        "status": "not_implemented",
        "required_libraries": ["pandas", "csv"]
    }


@router.post("/import-from-url")
async def import_ingredient_from_url(
    url: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Import ingredient data from a URL by scraping the content"""
    
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Scrape ingredient data
        ingredient_data = await scrape_ingredient_from_url(url)
        
        if not ingredient_data.get('name'):
            raise HTTPException(
                status_code=400,
                detail="Could not extract ingredient name from URL"
            )
        
        # Check if ingredient already exists
        existing_ingredient = db.query(Ingredient).filter(
            Ingredient.name.ilike(ingredient_data['name'])
        ).first()
        
        if existing_ingredient:
            return {
                "success": False,
                "message": f"Ingredient '{ingredient_data['name']}' already exists",
                "existing_ingredient": {
                    "id": existing_ingredient.id,
                    "name": existing_ingredient.name,
                    "category": existing_ingredient.category
                },
                "scraped_data": ingredient_data
            }
        
        # Create new ingredient
        ingredient_create = IngredientCreate(
            name=ingredient_data['name'],
            category=ingredient_data.get('category', 'Imported'),
            default_unit=ingredient_data.get('default_unit', 'piece'),
            description=ingredient_data.get('description', ''),
            nutritional_info=ingredient_data.get('nutritional_info'),
            allergens=ingredient_data.get('allergens', [])
        )
        
        db_ingredient = Ingredient(**ingredient_create.dict())
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)
        
        return {
            "success": True,
            "message": f"Successfully imported ingredient '{ingredient_data['name']}' from URL",
            "ingredient": {
                "id": db_ingredient.id,
                "name": db_ingredient.name,
                "category": db_ingredient.category,
                "description": db_ingredient.description
            },
            "source_url": url,
            "scraped_data": ingredient_data
        }
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch URL: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error importing ingredient: {str(e)}"
        )


async def scrape_ingredient_from_url(url: str) -> Dict[str, Any]:
    """Scrape ingredient information from various sources"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize result
    ingredient_data = {
        'name': '',
        'description': '',
        'category': 'Imported',
        'default_unit': 'piece',
        'nutritional_info': {},
        'allergens': []
    }
    
    # Extract based on domain/source
    domain = urlparse(url).netloc.lower()
    
    if 'wikipedia' in domain:
        ingredient_data = scrape_wikipedia_ingredient(soup, url)
    elif 'usda' in domain or 'nutrition' in domain:
        ingredient_data = scrape_nutrition_database(soup, url)
    else:
        ingredient_data = scrape_generic_ingredient(soup, url)
    
    return ingredient_data


def scrape_wikipedia_ingredient(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Scrape ingredient data from Wikipedia"""
    
    ingredient_data = {
        'name': '',
        'description': '',
        'category': 'Imported',
        'default_unit': 'piece',
        'nutritional_info': {},
        'allergens': []
    }
    
    # Get title (ingredient name)
    title_elem = soup.find('h1', class_='firstHeading') or soup.find('h1')
    if title_elem:
        ingredient_data['name'] = title_elem.get_text().strip()
    
    # Get first paragraph as description
    first_para = soup.find('div', class_='mw-parser-output')
    if first_para:
        para = first_para.find('p')
        if para:
            # Clean up the description
            description = para.get_text().strip()
            # Remove reference brackets [1], [2], etc.
            description = re.sub(r'\[\d+\]', '', description)
            ingredient_data['description'] = description[:500] + '...' if len(description) > 500 else description
    
    # Try to determine category from categories or infobox
    categories = soup.find_all('div', class_='mw-normal-catlinks')
    for cat_div in categories:
        cat_links = cat_div.find_all('a')
        for link in cat_links:
            cat_text = link.get_text().lower()
            if any(word in cat_text for word in ['fruit', 'vegetable', 'herb', 'spice', 'grain', 'meat', 'dairy', 'seafood']):
                ingredient_data['category'] = cat_text.title()
                break
    
    # Look for nutrition infobox
    infobox = soup.find('table', class_='infobox')
    if infobox:
        nutrition_info = {}
        rows = infobox.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if th and td:
                key = th.get_text().strip().lower()
                value = td.get_text().strip()
                if any(nutrient in key for nutrient in ['calorie', 'protein', 'fat', 'carb', 'fiber', 'sugar']):
                    nutrition_info[key] = value
        
        if nutrition_info:
            ingredient_data['nutritional_info'] = nutrition_info
    
    return ingredient_data


def scrape_nutrition_database(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Scrape ingredient data from nutrition databases"""
    
    ingredient_data = {
        'name': '',
        'description': '',
        'category': 'Nutrition Database',
        'default_unit': 'gram',
        'nutritional_info': {},
        'allergens': []
    }
    
    # Get ingredient name from title or h1
    title_elem = soup.find('h1') or soup.find('title')
    if title_elem:
        ingredient_data['name'] = title_elem.get_text().strip()
    
    # Look for nutrition facts tables
    nutrition_tables = soup.find_all('table')
    nutrition_info = {}
    
    for table in nutrition_tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                nutrient = cells[0].get_text().strip().lower()
                value = cells[1].get_text().strip()
                if any(n in nutrient for n in ['calorie', 'protein', 'fat', 'carb', 'fiber', 'sugar', 'sodium']):
                    nutrition_info[nutrient] = value
    
    if nutrition_info:
        ingredient_data['nutritional_info'] = nutrition_info
    
    return ingredient_data


def scrape_generic_ingredient(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Generic scraping for unknown sources"""
    
    ingredient_data = {
        'name': '',
        'description': '',
        'category': 'Web Import',
        'default_unit': 'piece',
        'nutritional_info': {},
        'allergens': []
    }
    
    # Try to get name from title, h1, or meta tags
    title_elem = soup.find('h1') or soup.find('title')
    if title_elem:
        ingredient_data['name'] = title_elem.get_text().strip()
    
    # Try to get description from meta description or first paragraph
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        ingredient_data['description'] = meta_desc.get('content', '')
    else:
        # Get first paragraph
        para = soup.find('p')
        if para:
            ingredient_data['description'] = para.get_text().strip()[:300] + '...'
    
    return ingredient_data


@router.post("/preview-url")
async def preview_ingredient_from_url(
    url: str,
    current_user = Depends(get_current_user)
):
    """Preview ingredient data from URL without saving to database"""
    
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Scrape ingredient data
        ingredient_data = await scrape_ingredient_from_url(url)
        
        return {
            "success": True,
            "preview_data": ingredient_data,
            "source_url": url,
            "message": "Preview generated successfully"
        }
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch URL: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error previewing ingredient: {str(e)}"
        ) 