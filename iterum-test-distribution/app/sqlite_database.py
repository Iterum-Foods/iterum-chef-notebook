import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class CulinaryDatabase:
    def __init__(self, db_path: str = "culinary_data.db"):
        """Initialize the culinary database with SQLite backend."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
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
                    updated_at TEXT NOT NULL,
                    user_id TEXT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
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
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES users (id)
                )
            ''')
            
            # Recipe ingredients (many-to-many relationship)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipe_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id INTEGER,
                    ingredient_name TEXT,
                    amount REAL,
                    unit TEXT,
                    is_prep BOOLEAN DEFAULT FALSE,
                    prep_recipe_id INTEGER,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
                    FOREIGN KEY (prep_recipe_id) REFERENCES recipes (id)
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
                    data TEXT,  -- JSON data for all form fields
                    sketch_data TEXT,  -- Base64 encoded sketch image
                    sketch_notes TEXT,
                    ingredient_labels TEXT,  -- JSON array of label objects
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Vendors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    company TEXT,
                    email TEXT,
                    phone TEXT,
                    mobile TEXT,
                    fax TEXT,
                    website TEXT,
                    street TEXT,
                    city TEXT,
                    state TEXT,
                    zip_code TEXT,
                    specialties TEXT,  -- JSON array
                    notes TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    user_id TEXT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Equipment table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    description TEXT,
                    specifications TEXT,  -- JSON object
                    maintenance_notes TEXT,
                    purchase_date TEXT,
                    warranty_info TEXT,
                    location TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    user_id TEXT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Vendor ingredients (many-to-many relationship)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendor_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vendor_id INTEGER,
                    ingredient_id INTEGER,
                    price REAL,
                    unit TEXT,
                    availability TEXT,
                    minimum_order REAL,
                    lead_time_days INTEGER,
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    FOREIGN KEY (vendor_id) REFERENCES vendors (id),
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
                )
            ''')
            
            # Vendor equipment (many-to-many relationship)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendor_equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vendor_id INTEGER,
                    equipment_id INTEGER,
                    price REAL,
                    availability TEXT,
                    warranty_offered TEXT,
                    service_support TEXT,
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT,
                    FOREIGN KEY (vendor_id) REFERENCES vendors (id),
                    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
                )
            ''')
            
            conn.commit()
    
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        """Save or update a user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
                return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
            print(f"Error getting users: {e}")
            return []
    
    def save_ingredients(self, ingredients: List[Dict[str, Any]]) -> bool:
        """Save multiple ingredients."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for ingredient in ingredients:
                    cursor.execute('''
                        INSERT OR REPLACE INTO ingredients 
                        (name, unit, category, spec_notes, nutritional_info, storage_notes,
                         substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                         best_before, prep_notes, created_at, updated_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                        ingredient.get('updated_at', datetime.now().isoformat()),
                        ingredient.get('user_id')
                    ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving ingredients: {e}")
            return False
    
    def get_ingredients(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all ingredients for a user (global + user-specific)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if user_id:
                    cursor.execute('''
                        SELECT name, unit, category, spec_notes, nutritional_info, storage_notes,
                               substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                               best_before, prep_notes, created_at, updated_at
                        FROM ingredients
                        WHERE user_id IS NULL OR user_id = ?
                        ORDER BY name
                    ''', (user_id,))
                else:
                    cursor.execute('''
                        SELECT name, unit, category, spec_notes, nutritional_info, storage_notes,
                               substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                               best_before, prep_notes, created_at, updated_at
                        FROM ingredients
                        ORDER BY name
                    ''')
                rows = cursor.fetchall()
                return [
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
                    for row in rows
                ]
        except Exception as e:
            print(f"Error getting ingredients: {e}")
            return []
    
    def save_recipe(self, recipe_data: Dict[str, Any]) -> Optional[int]:
        """Save a recipe and return its ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO recipes 
                    (name, description, type, instructions, tags, servings, prep_time,
                     cook_time, difficulty_level, status, author_id, author_name, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    recipe_data.get('name'),
                    recipe_data.get('description'),
                    recipe_data.get('type'),
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
                            ingredient.get('prepRecipeId') # Assuming prep_recipe_id is passed
                        ))
                
                conn.commit()
                return recipe_id
        except Exception as e:
            print(f"Error saving recipe: {e}")
            return None
    
    def get_recipes(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get recipes - shows only user's recipes by default, or all if user_id is 'all'."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
                    # Note: This method doesn't have current_user context, so it shows all
                    # The calling code should pass the user_id parameter
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
                        SELECT ri.id, ri.ingredient_name, ri.amount, ri.unit, ri.is_prep, ri.prep_recipe_id,
                               i.name as ingredient_name_full, i.unit as ingredient_unit, i.category, i.spec_notes, i.nutritional_info, i.storage_notes,
                               i.substitutions, i.seasonality, i.cost_level, i.supplier_notes, i.allergen_info, i.best_before, i.prep_notes, i.created_at, i.updated_at
                        FROM recipe_ingredients ri
                        LEFT JOIN ingredients i ON ri.ingredient_name = i.name
                        WHERE ri.recipe_id = ?
                    ''', (recipe['id'],))
                    ingredients = []
                    for ing in cursor.fetchall():
                        ingredient_data = {
                            'id': ing[0],
                            'name': ing[6],
                            'amount': ing[2],
                            'unit': ing[7],
                            'isPrep': bool(ing[4]),
                            'prepRecipeId': ing[5]
                        }
                        if ing[6] != ing[7]: # Only add if it's a different name/unit
                            ingredient_data['fullName'] = ing[6]
                        if ing[7] != ing[8]: # Only add if it's a different unit
                            ingredient_data['fullUnit'] = ing[7]
                        if ing[9] != ing[10]: # Only add if it's a different category
                            ingredient_data['fullCategory'] = ing[9]
                        if ing[11] != ing[12]: # Only add if it's a different spec_notes
                            ingredient_data['fullSpecNotes'] = ing[11]
                        if ing[13] != ing[14]: # Only add if it's a different nutritional_info
                            ingredient_data['fullNutritionalInfo'] = ing[13]
                        if ing[15] != ing[16]: # Only add if it's a different storage_notes
                            ingredient_data['fullStorageNotes'] = ing[15]
                        if ing[17] != ing[18]: # Only add if it's a different substitutions
                            ingredient_data['fullSubstitutions'] = ing[17]
                        if ing[19] != ing[20]: # Only add if it's a different seasonality
                            ingredient_data['fullSeasonality'] = ing[19]
                        if ing[21] != ing[22]: # Only add if it's a different cost_level
                            ingredient_data['fullCostLevel'] = ing[21]
                        if ing[23] != ing[24]: # Only add if it's a different supplier_notes
                            ingredient_data['fullSupplierNotes'] = ing[23]
                        if ing[25] != ing[26]: # Only add if it's a different allergen_info
                            ingredient_data['fullAllergenInfo'] = ing[25]
                        if ing[27] != ing[28]: # Only add if it's a different best_before
                            ingredient_data['fullBestBefore'] = ing[27]
                        if ing[29] != ing[30]: # Only add if it's a different prep_notes
                            ingredient_data['fullPrepNotes'] = ing[29]
                        if ing[31] != ing[32]: # Only add if it's a different created_at
                            ingredient_data['fullCreatedAt'] = ing[31]
                        if ing[33] != ing[34]: # Only add if it's a different updated_at
                            ingredient_data['fullUpdatedAt'] = ing[33]
                        ingredients.append(ingredient_data)
                    recipe['ingredients'] = ingredients
                    recipes.append(recipe)
                
                return recipes
        except Exception as e:
            print(f"Error getting recipes: {e}")
            return []
    
    def save_pantry_item(self, user_id: str, pantry_data: Dict[str, Any]) -> bool:
        """Save a pantry item."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
                return True
        except Exception as e:
            print(f"Error saving pantry item: {e}")
            return False
    
    def get_pantry(self, user_id: str) -> List[Dict[str, Any]]:
        """Get pantry items for a user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
            print(f"Error getting pantry: {e}")
            return []
    
    def save_recipe_draft(self, user_id: str, draft_data: Dict[str, Any]) -> Optional[int]:
        """Save a recipe draft and return its ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
                return draft_id
        except Exception as e:
            print(f"Error saving recipe draft: {e}")
            return None
    
    def get_recipe_drafts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all recipe drafts for a user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
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
            print(f"Error getting recipe drafts: {e}")
            return []
    
    def delete_recipe_draft(self, draft_id: int) -> bool:
        """Delete a recipe draft."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM recipe_drafts WHERE id = ?', (draft_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting recipe draft: {e}")
            return False
    
    def export_data(self, export_path: str) -> bool:
        """Export all data to a JSON file."""
        try:
            data = {
                'users': self.get_users(),
                'ingredients': self.get_ingredients(),
                'recipes': self.get_recipes(),
                'pantry': {},  # Will be populated per user
                'drafts': {}   # Will be populated per user
            }
            
            # Get pantry and drafts for each user
            for user in data['users']:
                data['pantry'][user['id']] = self.get_pantry(user['id'])
                data['drafts'][user['id']] = self.get_recipe_drafts(user['id'])
            
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """Import data from a JSON file."""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            
            # Import users
            for user in data.get('users', []):
                self.save_user(user)
            
            # Import ingredients
            if data.get('ingredients'):
                self.save_ingredients(data['ingredients'])
            
            # Import recipes
            for recipe in data.get('recipes', []):
                self.save_recipe(recipe)
            
            # Import pantry items
            for user_id, pantry_items in data.get('pantry', {}).items():
                for item in pantry_items:
                    self.save_pantry_item(user_id, item)
            
            # Import drafts
            for user_id, drafts in data.get('drafts', {}).items():
                for draft in drafts:
                    self.save_recipe_draft(user_id, draft)
            
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False

    # Vendor methods
    def save_vendor(self, vendor_data: Dict[str, Any]) -> Optional[int]:
        """Save a vendor and return its ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO vendors 
                    (name, company, email, phone, mobile, fax, website, street, city, state, zip_code,
                     specialties, notes, is_active, created_at, updated_at, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vendor_data.get('name'),
                    vendor_data.get('company'),
                    vendor_data.get('email'),
                    vendor_data.get('phone'),
                    vendor_data.get('mobile'),
                    vendor_data.get('fax'),
                    vendor_data.get('website'),
                    vendor_data.get('street'),
                    vendor_data.get('city'),
                    vendor_data.get('state'),
                    vendor_data.get('zip_code'),
                    json.dumps(vendor_data.get('specialties', [])),
                    vendor_data.get('notes'),
                    vendor_data.get('is_active', True),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    vendor_data.get('user_id')
                ))
                vendor_id = cursor.lastrowid
                conn.commit()
                return vendor_id
        except Exception as e:
            print(f"Error saving vendor: {e}")
            return None

    def get_vendors(self, user_id: Optional[str] = None, limit: int = 100, offset: int = 0, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all vendors for a user (global + user-specific) with optional search."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = '''
                    SELECT id, name, company, email, phone, mobile, fax, website, street, city, state, zip_code,
                           specialties, notes, is_active, created_at, updated_at
                    FROM vendors
                '''
                params = []
                where_clauses = []
                if user_id:
                    where_clauses.append('(user_id IS NULL OR user_id = ?)')
                    params.append(user_id)
                if search:
                    where_clauses.append('(name LIKE ? OR company LIKE ? OR email LIKE ?)')
                    search_term = f'%{search}%'
                    params.extend([search_term, search_term, search_term])
                if where_clauses:
                    query += ' WHERE ' + ' AND '.join(where_clauses)
                query += ' ORDER BY name LIMIT ? OFFSET ?'
                params.extend([limit, offset])
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [
                    {
                        'id': row[0],
                        'name': row[1],
                        'company': row[2],
                        'email': row[3],
                        'phone': row[4],
                        'mobile': row[5],
                        'fax': row[6],
                        'website': row[7],
                        'street': row[8],
                        'city': row[9],
                        'state': row[10],
                        'zip_code': row[11],
                        'specialties': json.loads(row[12]) if row[12] else [],
                        'notes': row[13],
                        'is_active': bool(row[14]),
                        'created_at': row[15],
                        'updated_at': row[16]
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"Error getting vendors: {e}")
            return []

    def get_vendor(self, vendor_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific vendor by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, company, email, phone, mobile, fax, website, street, city, state, zip_code,
                           specialties, notes, is_active, created_at, updated_at
                    FROM vendors
                    WHERE id = ?
                ''', (vendor_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'company': row[2],
                        'email': row[3],
                        'phone': row[4],
                        'mobile': row[5],
                        'fax': row[6],
                        'website': row[7],
                        'street': row[8],
                        'city': row[9],
                        'state': row[10],
                        'zip_code': row[11],
                        'specialties': json.loads(row[12]) if row[12] else [],
                        'notes': row[13],
                        'is_active': bool(row[14]),
                        'created_at': row[15],
                        'updated_at': row[16]
                    }
                return None
        except Exception as e:
            print(f"Error getting vendor: {e}")
            return None

    def update_vendor(self, vendor_id: int, vendor_data: Dict[str, Any]) -> bool:
        """Update a vendor."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE vendors 
                    SET name = ?, company = ?, email = ?, phone = ?, mobile = ?, fax = ?, website = ?,
                        street = ?, city = ?, state = ?, zip_code = ?, specialties = ?, notes = ?, 
                        is_active = ?, updated_at = ?
                    WHERE id = ?
                ''', (
                    vendor_data.get('name'),
                    vendor_data.get('company'),
                    vendor_data.get('email'),
                    vendor_data.get('phone'),
                    vendor_data.get('mobile'),
                    vendor_data.get('fax'),
                    vendor_data.get('website'),
                    vendor_data.get('street'),
                    vendor_data.get('city'),
                    vendor_data.get('state'),
                    vendor_data.get('zip_code'),
                    json.dumps(vendor_data.get('specialties', [])),
                    vendor_data.get('notes'),
                    vendor_data.get('is_active', True),
                    datetime.now().isoformat(),
                    vendor_id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating vendor: {e}")
            return False

    def delete_vendor(self, vendor_id: int) -> bool:
        """Delete a vendor."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting vendor: {e}")
            return False

    # Equipment methods
    def save_equipment(self, equipment_data: Dict[str, Any]) -> Optional[int]:
        """Save equipment and return its ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO equipment 
                    (name, category, description, specifications, maintenance_notes, purchase_date,
                     warranty_info, location, status, created_at, updated_at, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    equipment_data.get('name'),
                    equipment_data.get('category'),
                    equipment_data.get('description'),
                    json.dumps(equipment_data.get('specifications', {})),
                    equipment_data.get('maintenance_notes'),
                    equipment_data.get('purchase_date'),
                    equipment_data.get('warranty_info'),
                    equipment_data.get('location'),
                    equipment_data.get('status', 'active'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    equipment_data.get('user_id')
                ))
                equipment_id = cursor.lastrowid
                conn.commit()
                return equipment_id
        except Exception as e:
            print(f"Error saving equipment: {e}")
            return None

    def get_equipment(self, user_id: Optional[str] = None, limit: int = 100, offset: int = 0, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all equipment for a user (global + user-specific) with optional search."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = '''
                    SELECT id, name, category, description, specifications, maintenance_notes, purchase_date,
                           warranty_info, location, status, created_at, updated_at
                    FROM equipment
                '''
                params = []
                where_clauses = []
                if user_id:
                    where_clauses.append('(user_id IS NULL OR user_id = ?)')
                    params.append(user_id)
                if search:
                    where_clauses.append('(name LIKE ? OR category LIKE ? OR description LIKE ?)')
                    search_term = f'%{search}%'
                    params.extend([search_term, search_term, search_term])
                if where_clauses:
                    query += ' WHERE ' + ' AND '.join(where_clauses)
                query += ' ORDER BY name LIMIT ? OFFSET ?'
                params.extend([limit, offset])
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [
                    {
                        'id': row[0],
                        'name': row[1],
                        'category': row[2],
                        'description': row[3],
                        'specifications': self._parse_specifications(row[4]),
                        'maintenance_notes': row[5],
                        'purchase_date': row[6],
                        'warranty_info': row[7],
                        'location': row[8],
                        'status': row[9],
                        'created_at': row[10],
                        'updated_at': row[11]
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"Error getting equipment: {e}")
            return []

    def _parse_specifications(self, spec_data):
        """Safely parse specifications field - handles both JSON and plain text."""
        if not spec_data:
            return {}
        
        # Try to parse as JSON first
        try:
            return json.loads(spec_data)
        except (json.JSONDecodeError, TypeError):
            # If it's plain text, convert to a simple dict
            if isinstance(spec_data, str):
                # Split by common delimiters and create key-value pairs
                parts = spec_data.split(', ')
                specs = {}
                for i, part in enumerate(parts):
                    if ':' in part:
                        key, value = part.split(':', 1)
                        specs[key.strip()] = value.strip()
                    else:
                        specs[f'spec_{i+1}'] = part.strip()
                return specs
            return {'description': str(spec_data)}

    def get_equipment_by_id(self, equipment_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific equipment by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, category, description, specifications, maintenance_notes, purchase_date,
                           warranty_info, location, status, created_at, updated_at
                    FROM equipment
                    WHERE id = ?
                ''', (equipment_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'category': row[2],
                        'description': row[3],
                        'specifications': self._parse_specifications(row[4]),
                        'maintenance_notes': row[5],
                        'purchase_date': row[6],
                        'warranty_info': row[7],
                        'location': row[8],
                        'status': row[9],
                        'created_at': row[10],
                        'updated_at': row[11]
                    }
                return None
        except Exception as e:
            print(f"Error getting equipment: {e}")
            return None

    def update_equipment(self, equipment_id: int, equipment_data: Dict[str, Any]) -> bool:
        """Update equipment."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE equipment 
                    SET name = ?, category = ?, description = ?, specifications = ?, maintenance_notes = ?,
                        purchase_date = ?, warranty_info = ?, location = ?, status = ?, updated_at = ?
                    WHERE id = ?
                ''', (
                    equipment_data.get('name'),
                    equipment_data.get('category'),
                    equipment_data.get('description'),
                    json.dumps(equipment_data.get('specifications', {})),
                    equipment_data.get('maintenance_notes'),
                    equipment_data.get('purchase_date'),
                    equipment_data.get('warranty_info'),
                    equipment_data.get('location'),
                    equipment_data.get('status'),
                    datetime.now().isoformat(),
                    equipment_id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating equipment: {e}")
            return False

    def delete_equipment(self, equipment_id: int) -> bool:
        """Delete equipment."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM equipment WHERE id = ?', (equipment_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting equipment: {e}")
            return False

    # Vendor relationship methods
    def save_vendor_ingredient(self, vendor_ingredient_data: Dict[str, Any]) -> Optional[int]:
        """Save vendor-ingredient relationship."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO vendor_ingredients 
                    (vendor_id, ingredient_id, price, unit, availability, minimum_order, lead_time_days, notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vendor_ingredient_data.get('vendor_id'),
                    vendor_ingredient_data.get('ingredient_id'),
                    vendor_ingredient_data.get('price'),
                    vendor_ingredient_data.get('unit'),
                    vendor_ingredient_data.get('availability'),
                    vendor_ingredient_data.get('minimum_order'),
                    vendor_ingredient_data.get('lead_time_days'),
                    vendor_ingredient_data.get('notes'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                relationship_id = cursor.lastrowid
                conn.commit()
                return relationship_id
        except Exception as e:
            print(f"Error saving vendor ingredient: {e}")
            return None

    def get_vendor_ingredients(self, vendor_id: Optional[int] = None, ingredient_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get vendor-ingredient relationships."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = '''
                    SELECT vi.id, vi.vendor_id, vi.ingredient_id, vi.price, vi.unit, vi.availability,
                           vi.minimum_order, vi.lead_time_days, vi.notes, vi.created_at, vi.updated_at,
                           v.name as vendor_name, i.name as ingredient_name
                    FROM vendor_ingredients vi
                    JOIN vendors v ON vi.vendor_id = v.id
                    JOIN ingredients i ON vi.ingredient_id = i.id
                '''
                params = []
                
                if vendor_id:
                    query += ' WHERE vi.vendor_id = ?'
                    params.append(vendor_id)
                elif ingredient_id:
                    query += ' WHERE vi.ingredient_id = ?'
                    params.append(ingredient_id)
                
                query += ' ORDER BY v.name, i.name'
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [
                    {
                        'id': row[0],
                        'vendor_id': row[1],
                        'ingredient_id': row[2],
                        'price': row[3],
                        'unit': row[4],
                        'availability': row[5],
                        'minimum_order': row[6],
                        'lead_time_days': row[7],
                        'notes': row[8],
                        'created_at': row[9],
                        'updated_at': row[10],
                        'vendor_name': row[11],
                        'ingredient_name': row[12]
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"Error getting vendor ingredients: {e}")
            return []

    def save_vendor_equipment(self, vendor_equipment_data: Dict[str, Any]) -> Optional[int]:
        """Save vendor-equipment relationship."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO vendor_equipment 
                    (vendor_id, equipment_id, price, availability, warranty_offered, service_support, notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vendor_equipment_data.get('vendor_id'),
                    vendor_equipment_data.get('equipment_id'),
                    vendor_equipment_data.get('price'),
                    vendor_equipment_data.get('availability'),
                    vendor_equipment_data.get('warranty_offered'),
                    vendor_equipment_data.get('service_support'),
                    vendor_equipment_data.get('notes'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                relationship_id = cursor.lastrowid
                conn.commit()
                return relationship_id
        except Exception as e:
            print(f"Error saving vendor equipment: {e}")
            return None

    def get_vendor_equipment(self, vendor_id: Optional[int] = None, equipment_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get vendor-equipment relationships."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = '''
                    SELECT ve.id, ve.vendor_id, ve.equipment_id, ve.price, ve.availability,
                           ve.warranty_offered, ve.service_support, ve.notes, ve.created_at, ve.updated_at,
                           v.name as vendor_name, e.name as equipment_name
                    FROM vendor_equipment ve
                    JOIN vendors v ON ve.vendor_id = v.id
                    JOIN equipment e ON ve.equipment_id = e.id
                '''
                params = []
                
                if vendor_id:
                    query += ' WHERE ve.vendor_id = ?'
                    params.append(vendor_id)
                elif equipment_id:
                    query += ' WHERE ve.equipment_id = ?'
                    params.append(equipment_id)
                
                query += ' ORDER BY v.name, e.name'
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [
                    {
                        'id': row[0],
                        'vendor_id': row[1],
                        'equipment_id': row[2],
                        'price': row[3],
                        'availability': row[4],
                        'warranty_offered': row[5],
                        'service_support': row[6],
                        'notes': row[7],
                        'created_at': row[8],
                        'updated_at': row[9],
                        'vendor_name': row[10],
                        'equipment_name': row[11]
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"Error getting vendor equipment: {e}")
            return []

    def copy_global_data_to_user(self, user_id: str):
        """Copy all global ingredients, vendors, and equipment to the new user's library."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Copy global ingredients
                cursor.execute('SELECT name, unit, category, spec_notes, nutritional_info, storage_notes, substitutions, seasonality, cost_level, supplier_notes, allergen_info, best_before, prep_notes, created_at, updated_at FROM ingredients WHERE user_id IS NULL')
                for row in cursor.fetchall():
                    cursor.execute('''
                        INSERT INTO ingredients (name, unit, category, spec_notes, nutritional_info, storage_notes, substitutions, seasonality, cost_level, supplier_notes, allergen_info, best_before, prep_notes, created_at, updated_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (*row, user_id))
                # Copy global vendors
                cursor.execute('SELECT name, company, email, phone, mobile, fax, website, street, city, state, zip_code, specialties, notes, is_active, created_at, updated_at FROM vendors WHERE user_id IS NULL')
                for row in cursor.fetchall():
                    cursor.execute('''
                        INSERT INTO vendors (name, company, email, phone, mobile, fax, website, street, city, state, zip_code, specialties, notes, is_active, created_at, updated_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (*row, user_id))
                # Copy global equipment
                cursor.execute('SELECT name, category, description, specifications, maintenance_notes, purchase_date, warranty_info, location, status, created_at, updated_at FROM equipment WHERE user_id IS NULL')
                for row in cursor.fetchall():
                    cursor.execute('''
                        INSERT INTO equipment (name, category, description, specifications, maintenance_notes, purchase_date, warranty_info, location, status, created_at, updated_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (*row, user_id))
                conn.commit()
        except Exception as e:
            print(f"Error copying global data to user: {e}")

# Global database instance
db = CulinaryDatabase() 