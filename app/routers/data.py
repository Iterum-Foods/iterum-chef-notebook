from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from fastapi.responses import FileResponse
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import csv
import io
from app.sqlite_database import CulinaryDatabase


router = APIRouter(tags=["data"])

# Database file path
DB_PATH = "culinary_data.db"

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ALLOWED_JSON_TYPES = {"recipes", "ingredients", "pantry", "menus", "users"}

def init_database():
    """Initialize database tables if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT NOT NULL
            )
        ''')
        
        # Ingredients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                unit TEXT,
                category TEXT,
                spec_notes TEXT,
                nutritional_info TEXT,
                storage_notes TEXT,
                substitutions TEXT,
                seasonality TEXT,
                cost_level TEXT,
                supplier_notes TEXT,
                allergen_info TEXT,
                best_before TEXT,
                prep_notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                type TEXT,
                instructions TEXT,
                tags TEXT,
                servings INTEGER,
                prep_time INTEGER,
                cook_time INTEGER,
                difficulty_level TEXT,
                status TEXT,
                author_id TEXT,
                author_name TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Recipe ingredients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                ingredient_name TEXT,
                amount REAL,
                unit TEXT,
                is_prep BOOLEAN DEFAULT FALSE,
                prep_recipe_id INTEGER,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')
        
        # Pantry table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pantry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                ingredient_name TEXT,
                quantity REAL,
                unit TEXT,
                last_updated TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Recipe drafts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipe_drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                step INTEGER DEFAULT 1,
                data TEXT,
                sketch_data TEXT,
                sketch_notes TEXT,
                ingredient_labels TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()

# Initialize database on startup
init_database()

def get_json_path(datatype: str) -> Path:
    return DATA_DIR / f"{datatype}.json"

@router.post("/users")
async def save_user(user_data: Dict[str, Any]):
    """Save or update a user and copy global data if new."""
    db = CulinaryDatabase()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (id, name, created_at, last_login)
                VALUES (?, ?, ?, ?)
            ''', (
                user_data['id'],
                user_data['name'],
                user_data['created_at'],
                user_data['last_login']
            ))
            conn.commit()
        # After user is created, copy global data if this is a new user
        db.copy_global_data_to_user(user_data['id'])
        return {"success": True, "message": "User saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")

@router.get("/users")
async def get_users():
    """Get all users."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, created_at, last_login FROM users')
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'created_at': row[2],
                    'last_login': row[3]
                }
                for row in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting users: {str(e)}")

@router.post("/ingredients")
async def save_ingredients(ingredients: List[Dict[str, Any]]):
    """Save multiple ingredients."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for ingredient in ingredients:
                cursor.execute('''
                    INSERT OR REPLACE INTO ingredients 
                    (name, unit, category, spec_notes, nutritional_info, storage_notes,
                     substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                     best_before, prep_notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ingredient.get('name'),
                    ingredient.get('unit'),
                    ingredient.get('category'),
                    ingredient.get('specNotes'),
                    ingredient.get('nutritionalInfo'),
                    ingredient.get('storageNotes'),
                    ingredient.get('substitutions'),
                    ingredient.get('seasonality'),
                    ingredient.get('costLevel'),
                    ingredient.get('supplierNotes'),
                    ingredient.get('allergenInfo'),
                    ingredient.get('bestBefore'),
                    ingredient.get('prepNotes'),
                    ingredient.get('created_at', datetime.now().isoformat()),
                    ingredient.get('updated_at', datetime.now().isoformat())
                ))
            conn.commit()
            return {"success": True, "message": f"Saved {len(ingredients)} ingredients"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving ingredients: {str(e)}")

@router.get("/ingredients")
async def get_ingredients(
    user_id: Optional[str] = None,
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name"),
    limit: int = Query(100, le=500, description="Number of ingredients to return"),
    offset: int = Query(0, description="Number of ingredients to skip")
):
    """Get ingredients for recipe/menu creation with filtering and search"""
    try:
        db = CulinaryDatabase()
        all_ingredients = db.get_ingredients(user_id=user_id)
        
        # Apply filters
        filtered_ingredients = all_ingredients
        
        if category:
            filtered_ingredients = [ing for ing in filtered_ingredients if ing.get('category') == category]
        
        if search:
            search_lower = search.lower()
            filtered_ingredients = [
                ing for ing in filtered_ingredients 
                if search_lower in ing.get('name', '').lower() or 
                   search_lower in ing.get('category', '').lower()
            ]
        
        # Sort by name for consistency
        filtered_ingredients.sort(key=lambda x: x.get('name', ''))
        
        # Apply pagination
        total = len(filtered_ingredients)
        paginated_ingredients = filtered_ingredients[offset:offset + limit]
        
        # Get unique categories for filtering UI
        all_categories = sorted(list(set(ing.get('category', '') for ing in all_ingredients if ing.get('category'))))
        
        return {
            "success": True,
            "ingredients": paginated_ingredients,
            "total": total,
            "limit": limit,
            "offset": offset,
            "categories": all_categories
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ingredients: {str(e)}")

@router.get("/ingredients/search")
async def search_ingredients_for_recipes(
    q: str = Query(..., description="Search query"),
    user_id: Optional[str] = Query(None, description="User ID for user-specific ingredients"),
    limit: int = Query(20, le=100, description="Number of results to return")
):
    """Search ingredients specifically for recipe creation with enhanced info"""
    try:
        db = CulinaryDatabase()
        all_ingredients = db.get_ingredients(user_id=user_id)
        
        # Search logic
        search_lower = q.lower()
        matches = []
        
        for ingredient in all_ingredients:
            name = ingredient.get('name', '').lower()
            category = ingredient.get('category', '').lower()
            
            # Calculate relevance score
            score = 0
            if search_lower in name:
                if name.startswith(search_lower):
                    score = 100  # Exact start match
                else:
                    score = 80   # Contains match
            elif search_lower in category:
                score = 50   # Category match
            
            if score > 0:
                matches.append({
                    **ingredient,
                    'search_score': score,
                    'display_name': ingredient.get('name', ''),
                    'subtitle': f"{ingredient.get('category', '')} • {ingredient.get('unit', '')}",
                    'info': {
                        'category': ingredient.get('category', ''),
                        'unit': ingredient.get('unit', ''),
                        'seasonality': ingredient.get('seasonality', ''),
                        'cost_level': ingredient.get('cost_level', ''),
                        'allergen_info': ingredient.get('allergen_info', ''),
                        'storage_notes': ingredient.get('storage_notes', '')
                    }
                })
        
        # Sort by relevance score then name
        matches.sort(key=lambda x: (-x['search_score'], x.get('name', '')))
        
        return {
            "success": True,
            "query": q,
            "results": matches[:limit],
            "total_found": len(matches)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching ingredients: {str(e)}")

@router.get("/ingredients/categories")
async def get_ingredient_categories(user_id: Optional[str] = None):
    """Get all available ingredient categories"""
    try:
        db = CulinaryDatabase()
        all_ingredients = db.get_ingredients(user_id=user_id)
        
        # Count ingredients per category
        category_counts = {}
        for ingredient in all_ingredients:
            category = ingredient.get('category', 'Other')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Create category list with counts
        categories = [
            {
                'name': category,
                'count': count,
                'display_name': category
            }
            for category, count in sorted(category_counts.items())
        ]
        
        return {
            "success": True,
            "categories": categories,
            "total_categories": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories: {str(e)}")

@router.post("/recipes")
async def save_recipe(recipe_data: Dict[str, Any]):
    """Save a recipe."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes 
                (name, description, type, instructions, tags, servings, prep_time,
                 cook_time, difficulty_level, status, author_id, author_name, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe_data.get('name'),
                recipe_data.get('description'),
                recipe_data.get('type', 'dish'),
                recipe_data.get('instructions'),
                recipe_data.get('tags'),
                recipe_data.get('servings'),
                recipe_data.get('prep_time'),
                recipe_data.get('cook_time'),
                recipe_data.get('difficulty_level'),
                recipe_data.get('status'),
                recipe_data.get('author_id'),
                recipe_data.get('author_name'),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            recipe_id = cursor.lastrowid
            
            # Save recipe ingredients
            if recipe_data.get('ingredients'):
                for ingredient in recipe_data['ingredients']:
                    cursor.execute('''
                        INSERT INTO recipe_ingredients 
                        (recipe_id, ingredient_name, amount, unit, is_prep, prep_recipe_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        recipe_id,
                        ingredient.get('name'),
                        ingredient.get('amount'),
                        ingredient.get('unit'),
                        ingredient.get('isPrep', False),
                        ingredient.get('prepRecipeId')
                    ))
            
            conn.commit()
            return {"success": True, "recipe_id": recipe_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving recipe: {str(e)}")

@router.get("/recipes")
async def get_recipes(user_id: Optional[str] = None):
    """Get recipes - shows only current user's recipes by default, or all if user_id is 'all'."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if user_id and user_id != 'all':
                cursor.execute('''
                    SELECT id, name, description, type, instructions, tags, servings,
                           prep_time, cook_time, difficulty_level, status, author_id,
                           author_name, created_at, updated_at
                    FROM recipes
                    WHERE author_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))
            elif user_id == 'all':
                # Show all published recipes from all users
                cursor.execute('''
                    SELECT id, name, description, type, instructions, tags, servings,
                           prep_time, cook_time, difficulty_level, status, author_id,
                           author_name, created_at, updated_at
                    FROM recipes
                    WHERE status = 'published'
                    ORDER BY created_at DESC
                ''')
            else:
                # Default: show only current user's recipes
                # Note: This endpoint doesn't have current_user context, so it shows all
                # The frontend should pass the user_id parameter
                cursor.execute('''
                    SELECT id, name, description, type, instructions, tags, servings,
                           prep_time, cook_time, difficulty_level, status, author_id,
                           author_name, created_at, updated_at
                    FROM recipes
                    ORDER BY created_at DESC
                ''')
            
            rows = cursor.fetchall()
            recipes = []
            for row in rows:
                recipe = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'type': row[3],
                    'instructions': row[4],
                    'tags': row[5],
                    'servings': row[6],
                    'prep_time': row[7],
                    'cook_time': row[8],
                    'difficulty_level': row[9],
                    'status': row[10],
                    'author_id': row[11],
                    'author_name': row[12],
                    'created_at': row[13],
                    'updated_at': row[14]
                }
                
                # Get ingredients for this recipe
                cursor.execute('''
                    SELECT ingredient_name, amount, unit, is_prep, prep_recipe_id
                    FROM recipe_ingredients
                    WHERE recipe_id = ?
                ''', (recipe['id'],))
                ingredients = [
                    {
                        'name': ing[0],
                        'amount': ing[1],
                        'unit': ing[2],
                        'isPrep': bool(ing[3]),
                        'prepRecipeId': ing[4]
                    }
                    for ing in cursor.fetchall()
                ]
                recipe['ingredients'] = ingredients
                recipes.append(recipe)
            
            return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recipes: {str(e)}")

@router.post("/pantry")
async def save_pantry_item(user_id: str, pantry_data: Dict[str, Any]):
    """Save a pantry item."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO pantry 
                (user_id, ingredient_name, quantity, unit, last_updated)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                pantry_data['name'],
                pantry_data['quantity'],
                pantry_data['unit'],
                datetime.now().isoformat()
            ))
            conn.commit()
            return {"success": True, "message": "Pantry item saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving pantry item: {str(e)}")

@router.get("/pantry/{user_id}")
async def get_pantry(user_id: str):
    """Get pantry items for a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ingredient_name, quantity, unit, last_updated
                FROM pantry
                WHERE user_id = ?
                ORDER BY ingredient_name
            ''', (user_id,))
            rows = cursor.fetchall()
            return [
                {
                    'name': row[0],
                    'quantity': row[1],
                    'unit': row[2],
                    'last_updated': row[3]
                }
                for row in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting pantry: {str(e)}")

@router.post("/drafts")
async def save_recipe_draft(user_id: str, draft_data: Dict[str, Any]):
    """Save a recipe draft."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO recipe_drafts 
                (id, user_id, step, data, sketch_data, sketch_notes, ingredient_labels, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                draft_data.get('id'),
                user_id,
                draft_data.get('step', 1),
                json.dumps(draft_data.get('data', {})),
                draft_data.get('sketch_data'),
                draft_data.get('sketch_notes'),
                json.dumps(draft_data.get('ingredient_labels', [])),
                draft_data.get('created_at', datetime.now().isoformat()),
                datetime.now().isoformat()
            ))
            
            draft_id = cursor.lastrowid if not draft_data.get('id') else draft_data['id']
            conn.commit()
            return {"success": True, "draft_id": draft_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving draft: {str(e)}")

@router.get("/drafts/{user_id}")
async def get_recipe_drafts(user_id: str):
    """Get all recipe drafts for a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, step, data, sketch_data, sketch_notes, ingredient_labels, created_at, updated_at
                FROM recipe_drafts
                WHERE user_id = ?
                ORDER BY updated_at DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'step': row[1],
                    'data': json.loads(row[2]) if row[2] else {},
                    'sketch_data': row[3],
                    'sketch_notes': row[4],
                    'ingredient_labels': json.loads(row[5]) if row[5] else [],
                    'created_at': row[6],
                    'updated_at': row[7]
                }
                for row in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting drafts: {str(e)}")

@router.delete("/drafts/{draft_id}")
async def delete_recipe_draft(draft_id: int):
    """Delete a recipe draft."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recipe_drafts WHERE id = ?', (draft_id,))
            conn.commit()
            return {"success": True, "message": "Draft deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting draft: {str(e)}")

@router.post("/export")
async def export_data():
    """Export all data to a JSON file."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Get all data
            data = {}
            
            # Users
            cursor.execute('SELECT id, name, created_at, last_login FROM users')
            data['users'] = [
                {
                    'id': row[0],
                    'name': row[1],
                    'created_at': row[2],
                    'last_login': row[3]
                }
                for row in cursor.fetchall()
            ]
            
            # Ingredients
            cursor.execute('''
                SELECT name, unit, category, spec_notes, nutritional_info, storage_notes,
                       substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                       best_before, prep_notes, created_at, updated_at
                FROM ingredients
                ORDER BY name
            ''')
            data['ingredients'] = [
                {
                    'name': row[0],
                    'unit': row[1],
                    'category': row[2],
                    'specNotes': row[3],
                    'nutritionalInfo': row[4],
                    'storageNotes': row[5],
                    'substitutions': row[6],
                    'seasonality': row[7],
                    'costLevel': row[8],
                    'supplierNotes': row[9],
                    'allergenInfo': row[10],
                    'bestBefore': row[11],
                    'prepNotes': row[12],
                    'created_at': row[13],
                    'updated_at': row[14]
                }
                for row in cursor.fetchall()
            ]
            
            # Recipes
            cursor.execute('''
                SELECT id, name, description, type, instructions, tags, servings,
                       prep_time, cook_time, difficulty_level, status, author_id,
                       author_name, created_at, updated_at
                FROM recipes
                ORDER BY created_at DESC
            ''')
            recipes = []
            for row in cursor.fetchall():
                recipe = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'type': row[3],
                    'instructions': row[4],
                    'tags': row[5],
                    'servings': row[6],
                    'prep_time': row[7],
                    'cook_time': row[8],
                    'difficulty_level': row[9],
                    'status': row[10],
                    'author_id': row[11],
                    'author_name': row[12],
                    'created_at': row[13],
                    'updated_at': row[14]
                }
                
                # Get ingredients for this recipe
                cursor.execute('''
                    SELECT ingredient_name, amount, unit, is_prep, prep_recipe_id
                    FROM recipe_ingredients
                    WHERE recipe_id = ?
                ''', (recipe['id'],))
                recipe['ingredients'] = [
                    {
                        'name': ing[0],
                        'amount': ing[1],
                        'unit': ing[2],
                        'isPrep': bool(ing[3]),
                        'prepRecipeId': ing[4]
                    }
                    for ing in cursor.fetchall()
                ]
                recipes.append(recipe)
            data['recipes'] = recipes
            
            # Pantry and drafts per user
            data['pantry'] = {}
            data['drafts'] = {}
            for user in data['users']:
                # Pantry
                cursor.execute('''
                    SELECT ingredient_name, quantity, unit, last_updated
                    FROM pantry
                    WHERE user_id = ?
                    ORDER BY ingredient_name
                ''', (user['id'],))
                data['pantry'][user['id']] = [
                    {
                        'name': row[0],
                        'quantity': row[1],
                        'unit': row[2],
                        'last_updated': row[3]
                    }
                    for row in cursor.fetchall()
                ]
                
                # Drafts
                cursor.execute('''
                    SELECT id, step, data, sketch_data, sketch_notes, ingredient_labels, created_at, updated_at
                    FROM recipe_drafts
                    WHERE user_id = ?
                    ORDER BY updated_at DESC
                ''', (user['id'],))
                data['drafts'][user['id']] = [
                    {
                        'id': row[0],
                        'step': row[1],
                        'data': json.loads(row[2]) if row[2] else {},
                        'sketch_data': row[3],
                        'sketch_notes': row[4],
                        'ingredient_labels': json.loads(row[5]) if row[5] else [],
                        'created_at': row[6],
                        'updated_at': row[7]
                    }
                    for row in cursor.fetchall()
                ]
        
        # Save to file
        export_path = f"culinary_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(export_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return FileResponse(export_path, filename=export_path, media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")

@router.post("/import")
async def import_data(file: UploadFile = File(...)):
    """Import data from a JSON file."""
    try:
        # Read uploaded file
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Import users
            for user in data.get('users', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO users (id, name, created_at, last_login)
                    VALUES (?, ?, ?, ?)
                ''', (user['id'], user['name'], user['created_at'], user['last_login']))
            
            # Import ingredients
            for ingredient in data.get('ingredients', []):
                cursor.execute('''
                    INSERT OR REPLACE INTO ingredients 
                    (name, unit, category, spec_notes, nutritional_info, storage_notes,
                     substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                     best_before, prep_notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ingredient.get('name'),
                    ingredient.get('unit'),
                    ingredient.get('category'),
                    ingredient.get('specNotes'),
                    ingredient.get('nutritionalInfo'),
                    ingredient.get('storageNotes'),
                    ingredient.get('substitutions'),
                    ingredient.get('seasonality'),
                    ingredient.get('costLevel'),
                    ingredient.get('supplierNotes'),
                    ingredient.get('allergenInfo'),
                    ingredient.get('bestBefore'),
                    ingredient.get('prepNotes'),
                    ingredient.get('created_at'),
                    ingredient.get('updated_at')
                ))
            
            # Import recipes
            for recipe in data.get('recipes', []):
                cursor.execute('''
                    INSERT INTO recipes 
                    (id, name, description, type, instructions, tags, servings, prep_time,
                     cook_time, difficulty_level, status, author_id, author_name, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    recipe.get('id'),
                    recipe.get('name'),
                    recipe.get('description'),
                    recipe.get('type'),
                    recipe.get('instructions'),
                    recipe.get('tags'),
                    recipe.get('servings'),
                    recipe.get('prep_time'),
                    recipe.get('cook_time'),
                    recipe.get('difficulty_level'),
                    recipe.get('status'),
                    recipe.get('author_id'),
                    recipe.get('author_name'),
                    recipe.get('created_at'),
                    recipe.get('updated_at')
                ))
                
                # Import recipe ingredients
                for ingredient in recipe.get('ingredients', []):
                    cursor.execute('''
                        INSERT INTO recipe_ingredients 
                        (recipe_id, ingredient_name, amount, unit, is_prep, prep_recipe_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        recipe.get('id'),
                        ingredient.get('name'),
                        ingredient.get('amount'),
                        ingredient.get('unit'),
                        ingredient.get('isPrep', False),
                        ingredient.get('prepRecipeId')
                    ))
            
            # Import pantry items
            for user_id, pantry_items in data.get('pantry', {}).items():
                for item in pantry_items:
                    cursor.execute('''
                        INSERT OR REPLACE INTO pantry 
                        (user_id, ingredient_name, quantity, unit, last_updated)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        user_id,
                        item['name'],
                        item['quantity'],
                        item['unit'],
                        item['last_updated']
                    ))
            
            # Import drafts
            for user_id, drafts in data.get('drafts', {}).items():
                for draft in drafts:
                    cursor.execute('''
                        INSERT OR REPLACE INTO recipe_drafts 
                        (id, user_id, step, data, sketch_data, sketch_notes, ingredient_labels, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        draft.get('id'),
                        user_id,
                        draft.get('step', 1),
                        json.dumps(draft.get('data', {})),
                        draft.get('sketch_data'),
                        draft.get('sketch_notes'),
                        json.dumps(draft.get('ingredient_labels', [])),
                        draft.get('created_at'),
                        draft.get('updated_at')
                    ))
            
            conn.commit()
        
        return {"success": True, "message": "Data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing data: {str(e)}")

@router.get("/json/{datatype}")
async def get_json_data(datatype: str):
    if datatype not in ALLOWED_JSON_TYPES:
        raise HTTPException(status_code=400, detail="Invalid data type")
    path = get_json_path(datatype)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.post("/json/{datatype}")
async def save_json_data(datatype: str, request: Request):
    if datatype not in ALLOWED_JSON_TYPES:
        raise HTTPException(status_code=400, detail="Invalid data type")
    data = await request.json()
    path = get_json_path(datatype)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"success": True, "message": f"Saved {datatype} data"} 

@router.get("/json/ingredients")
async def get_ingredients_json():
    """Return all ingredients as JSON."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, unit, category FROM ingredients
            ''')
            rows = cursor.fetchall()
            ingredients = [
                {"id": row[0], "name": row[1], "unit": row[2], "category": row[3]}
                for row in rows
            ]
            return {"ingredients": ingredients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ingredients: {str(e)}")

@router.get("/vendors")
async def get_vendors(user_id: Optional[str] = None, limit: int = 100, offset: int = 0, search: Optional[str] = None):
    db = CulinaryDatabase()
    return db.get_vendors(user_id=user_id, limit=limit, offset=offset, search=search)

@router.get("/equipment")
async def get_equipment(user_id: Optional[str] = None, limit: int = 100, offset: int = 0, search: Optional[str] = None):
    try:
        db = CulinaryDatabase()
        equipment_data = db.get_equipment(user_id=user_id, limit=limit, offset=offset, search=search)
        return {
            "success": True,
            "data": equipment_data,
            "count": len(equipment_data)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": []
        }

@router.get("/equipment-database")
async def get_equipment_database():
    """Get the equipment database as JSON."""
    try:
        # Read the CSV file
        csv_path = Path("equipment_database.csv")
        if not csv_path.exists():
            return {"error": "Equipment database not found"}
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_content = file.read()
        
        # Parse CSV to JSON
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        equipment_data = list(csv_reader)
        
        return {
            "success": True,
            "count": len(equipment_data),
            "data": equipment_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading equipment database: {str(e)}") 