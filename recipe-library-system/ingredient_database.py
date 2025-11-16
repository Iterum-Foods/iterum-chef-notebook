#!/usr/bin/env python3
"""
Comprehensive Ingredient Database
Pre-built database of common ingredients with properties, costs, and metadata
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngredientDatabase:
    """Comprehensive ingredient database with pre-populated common ingredients."""
    
    def __init__(self, db_path: str = "recipe_library/ingredient_database.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
        self.populate_default_ingredients()
    
    def init_database(self):
        """Initialize the ingredient database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main ingredients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                subcategory TEXT,
                default_unit TEXT NOT NULL,
                common_units TEXT,  -- JSON array
                typical_yield_pct REAL DEFAULT 100.0,
                typical_ap_cost REAL,
                cost_unit TEXT,
                storage_notes TEXT,
                shelf_life_days INTEGER,
                allergens TEXT,  -- JSON array
                dietary_tags TEXT,  -- JSON array
                substitutes TEXT,  -- JSON array
                notes TEXT,
                source_url TEXT,  -- URL to product page or vendor page
                created_date TEXT,
                updated_date TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Vendor prices table - multiple vendors per ingredient
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendor_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER NOT NULL,
                vendor_name TEXT NOT NULL,
                ap_cost REAL NOT NULL,
                cost_unit TEXT NOT NULL,
                vendor_url TEXT,
                last_updated TEXT,
                is_preferred BOOLEAN DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (ingredient_id) REFERENCES ingredients (id),
                UNIQUE(ingredient_id, vendor_name)
            )
        ''')
        
        # Cost history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER,
                ap_cost REAL,
                cost_unit TEXT,
                vendor TEXT,
                date TEXT,
                notes TEXT,
                FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
            )
        ''')
        
        # Indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON ingredients(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON ingredients(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_active ON ingredients(is_active)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendor_ingredient ON vendor_prices(ingredient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendor_name ON vendor_prices(vendor_name)')
        
        conn.commit()
        conn.close()
        logger.info("Ingredient database initialized")
    
    def populate_default_ingredients(self):
        """Populate database with comprehensive list of common ingredients."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already populated
        cursor.execute("SELECT COUNT(*) FROM ingredients")
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.close()
            logger.info(f"Database already has {count} ingredients")
            return
        
        ingredients = self.get_default_ingredients()
        
        for ing in ingredients:
            try:
                cursor.execute('''
                    INSERT INTO ingredients (
                        name, category, subcategory, default_unit, common_units,
                        typical_yield_pct, typical_ap_cost, cost_unit,
                        storage_notes, shelf_life_days, allergens, dietary_tags,
                        substitutes, notes, source_url, created_date, updated_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ing['name'],
                    ing['category'],
                    ing.get('subcategory'),
                    ing['default_unit'],
                    json.dumps(ing.get('common_units', [])),
                    ing.get('typical_yield_pct', 100.0),
                    ing.get('typical_ap_cost'),
                    ing.get('cost_unit'),
                    ing.get('storage_notes'),
                    ing.get('shelf_life_days'),
                    json.dumps(ing.get('allergens', [])),
                    json.dumps(ing.get('dietary_tags', [])),
                    json.dumps(ing.get('substitutes', [])),
                    ing.get('notes'),
                    ing.get('source_url'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
            except sqlite3.IntegrityError:
                # Already exists, skip
                pass
        
        conn.commit()
        conn.close()
        logger.info(f"Populated database with {len(ingredients)} default ingredients")
    
    def get_default_ingredients(self) -> List[Dict[str, Any]]:
        """Get comprehensive list of default ingredients."""
        return [
            # PRODUCE - Vegetables
            {
                'name': 'Onions, Yellow',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each', 'cup'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 30,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free'],
                'substitutes': ['Onions, Red', 'Onions, White', 'Shallots']
            },
            {
                'name': 'Onions, Red',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each', 'cup'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 1.75,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 30,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Garlic',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'clove', 'head'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 3.00,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 60,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Tomatoes, Roma',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each', 'cup'],
                'typical_yield_pct': 95.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store at room temperature until ripe, then refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Tomatoes, Cherry',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'pint', 'cup', 'each'],
                'typical_yield_pct': 98.0,
                'typical_ap_cost': 3.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store at room temperature',
                'shelf_life_days': 5,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Potatoes, Russet',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 0.80,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dark, dry place',
                'shelf_life_days': 60,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Carrots',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each', 'cup'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 1.20,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate in plastic bag',
                'shelf_life_days': 14,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Celery',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'lb', 'oz', 'stalk', 'cup'],
                'typical_yield_pct': 75.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate in plastic bag',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Bell Peppers, Red',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'each', 'cup'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 3.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Bell Peppers, Green',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'each', 'cup'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Lettuce, Romaine',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'head',
                'common_units': ['head', 'lb', 'oz', 'cup'],
                'typical_yield_pct': 80.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'head',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Spinach, Fresh',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'bunch', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 3.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 5,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Mushrooms, Button',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 4.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate in paper bag',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Zucchini',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'each', 'cup'],
                'typical_yield_pct': 95.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Eggplant',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'each'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store at room temperature',
                'shelf_life_days': 5,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Broccoli',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'head', 'cup', 'floret'],
                'typical_yield_pct': 70.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Cauliflower',
                'category': 'Produce',
                'subcategory': 'Vegetables',
                'default_unit': 'lb',
                'common_units': ['lb', 'head', 'cup', 'floret'],
                'typical_yield_pct': 70.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            
            # PRODUCE - Fruits
            {
                'name': 'Lemons',
                'category': 'Produce',
                'subcategory': 'Fruits',
                'default_unit': 'lb',
                'common_units': ['lb', 'each', 'cup'],
                'typical_yield_pct': 60.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store at room temperature or refrigerate',
                'shelf_life_days': 14,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Limes',
                'category': 'Produce',
                'subcategory': 'Fruits',
                'default_unit': 'lb',
                'common_units': ['lb', 'each', 'cup'],
                'typical_yield_pct': 60.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store at room temperature or refrigerate',
                'shelf_life_days': 14,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Avocados',
                'category': 'Produce',
                'subcategory': 'Fruits',
                'default_unit': 'each',
                'common_units': ['each', 'lb', 'cup'],
                'typical_yield_pct': 75.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'each',
                'storage_notes': 'Ripen at room temperature, refrigerate when ripe',
                'shelf_life_days': 5,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            
            # PROTEINS
            {
                'name': 'Chicken Breast, Boneless Skinless',
                'category': 'Proteins',
                'subcategory': 'Poultry',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 4.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 9 months',
                'shelf_life_days': 2,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo'],
                'substitutes': ['Turkey Breast', 'Pork Tenderloin']
            },
            {
                'name': 'Chicken Thighs, Boneless Skinless',
                'category': 'Proteins',
                'subcategory': 'Poultry',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 3.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 9 months',
                'shelf_life_days': 2,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Chicken, Whole',
                'category': 'Proteins',
                'subcategory': 'Poultry',
                'default_unit': 'lb',
                'common_units': ['lb', 'each'],
                'typical_yield_pct': 65.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 12 months',
                'shelf_life_days': 2,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Beef, Ground (80/20)',
                'category': 'Proteins',
                'subcategory': 'Beef',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 5.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 3 months',
                'shelf_life_days': 2,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Beef, Ground (90/10)',
                'category': 'Proteins',
                'subcategory': 'Beef',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 6.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 3 months',
                'shelf_life_days': 2,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Beef, Chuck Roast',
                'category': 'Proteins',
                'subcategory': 'Beef',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz'],
                'typical_yield_pct': 70.0,
                'typical_ap_cost': 7.99,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 3-5 days, freeze up to 12 months',
                'shelf_life_days': 4,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Beef, Sirloin',
                'category': 'Proteins',
                'subcategory': 'Beef',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 9.99,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 3-5 days, freeze up to 12 months',
                'shelf_life_days': 4,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Pork, Chop',
                'category': 'Proteins',
                'subcategory': 'Pork',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 4.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 3-5 days, freeze up to 6 months',
                'shelf_life_days': 4,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Pork, Shoulder',
                'category': 'Proteins',
                'subcategory': 'Pork',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz'],
                'typical_yield_pct': 70.0,
                'typical_ap_cost': 3.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 3-5 days, freeze up to 6 months',
                'shelf_life_days': 4,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Salmon, Fillet',
                'category': 'Proteins',
                'subcategory': 'Seafood',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each'],
                'typical_yield_pct': 70.0,
                'typical_ap_cost': 12.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 3 months',
                'shelf_life_days': 2,
                'allergens': ['fish'],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Shrimp, Raw',
                'category': 'Proteins',
                'subcategory': 'Seafood',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'each'],
                'typical_yield_pct': 75.0,
                'typical_ap_cost': 10.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate 1-2 days, freeze up to 3 months',
                'shelf_life_days': 2,
                'allergens': ['shellfish'],
                'dietary_tags': ['gluten-free', 'dairy-free', 'keto', 'paleo']
            },
            {
                'name': 'Eggs, Large',
                'category': 'Proteins',
                'subcategory': 'Eggs',
                'default_unit': 'dozen',
                'common_units': ['dozen', 'each', 'cup'],
                'typical_yield_pct': 88.0,
                'typical_ap_cost': 3.00,
                'cost_unit': 'dozen',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 30,
                'allergens': ['eggs'],
                'dietary_tags': ['vegetarian', 'gluten-free', 'dairy-free', 'keto']
            },
            
            # DAIRY
            {
                'name': 'Butter, Unsalted',
                'category': 'Dairy',
                'subcategory': 'Fats',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'tbsp', 'stick'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 4.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 90,
                'allergens': ['dairy'],
                'dietary_tags': ['vegetarian', 'gluten-free', 'keto'],
                'substitutes': ['Margarine', 'Coconut Oil', 'Olive Oil']
            },
            {
                'name': 'Cream, Heavy',
                'category': 'Dairy',
                'subcategory': 'Cream',
                'default_unit': 'quart',
                'common_units': ['quart', 'cup', 'pint', 'fl oz'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 5.00,
                'cost_unit': 'quart',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': ['dairy'],
                'dietary_tags': ['vegetarian', 'gluten-free', 'keto']
            },
            {
                'name': 'Milk, Whole',
                'category': 'Dairy',
                'subcategory': 'Milk',
                'default_unit': 'gallon',
                'common_units': ['gallon', 'quart', 'cup', 'fl oz'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 3.50,
                'cost_unit': 'gallon',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 7,
                'allergens': ['dairy'],
                'dietary_tags': ['vegetarian', 'gluten-free']
            },
            {
                'name': 'Cheese, Cheddar',
                'category': 'Dairy',
                'subcategory': 'Cheese',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'shredded'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 5.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 30,
                'allergens': ['dairy'],
                'dietary_tags': ['vegetarian', 'gluten-free', 'keto']
            },
            {
                'name': 'Cheese, Parmesan',
                'category': 'Dairy',
                'subcategory': 'Cheese',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'grated'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 12.00,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 60,
                'allergens': ['dairy'],
                'dietary_tags': ['vegetarian', 'gluten-free', 'keto']
            },
            {
                'name': 'Cheese, Mozzarella',
                'category': 'Dairy',
                'subcategory': 'Cheese',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'shredded'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 4.50,
                'cost_unit': 'lb',
                'storage_notes': 'Refrigerate',
                'shelf_life_days': 14,
                'allergens': ['dairy'],
                'dietary_tags': ['vegetarian', 'gluten-free', 'keto']
            },
            
            # PANTRY - Grains & Flours
            {
                'name': 'Flour, All-Purpose',
                'category': 'Pantry',
                'subcategory': 'Grains & Flours',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'kg'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.60,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 365,
                'allergens': ['gluten'],
                'dietary_tags': ['vegetarian', 'vegan'],
                'substitutes': ['Flour, Bread', 'Flour, Cake']
            },
            {
                'name': 'Flour, Bread',
                'category': 'Pantry',
                'subcategory': 'Grains & Flours',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.75,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 365,
                'allergens': ['gluten'],
                'dietary_tags': ['vegetarian', 'vegan']
            },
            {
                'name': 'Rice, White Long Grain',
                'category': 'Pantry',
                'subcategory': 'Grains & Flours',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'kg'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 1.20,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Pasta, Spaghetti',
                'category': 'Pantry',
                'subcategory': 'Grains & Flours',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'box'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': ['gluten'],
                'dietary_tags': ['vegetarian', 'vegan']
            },
            
            # PANTRY - Sweeteners
            {
                'name': 'Sugar, Granulated',
                'category': 'Pantry',
                'subcategory': 'Sweeteners',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'kg'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.70,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1825,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Sugar, Brown',
                'category': 'Pantry',
                'subcategory': 'Sweeteners',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.90,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1825,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Honey',
                'category': 'Pantry',
                'subcategory': 'Sweeteners',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'tbsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 6.00,
                'cost_unit': 'lb',
                'storage_notes': 'Store at room temperature',
                'shelf_life_days': 1825,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            
            # PANTRY - Oils & Fats
            {
                'name': 'Oil, Olive',
                'category': 'Pantry',
                'subcategory': 'Oils & Fats',
                'default_unit': 'liter',
                'common_units': ['liter', 'cup', 'fl oz', 'tbsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 15.00,
                'cost_unit': 'liter',
                'storage_notes': 'Store in cool, dark place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'keto']
            },
            {
                'name': 'Oil, Canola',
                'category': 'Pantry',
                'subcategory': 'Oils & Fats',
                'default_unit': 'gallon',
                'common_units': ['gallon', 'cup', 'fl oz', 'tbsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 4.00,
                'cost_unit': 'gallon',
                'storage_notes': 'Store in cool, dark place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'keto']
            },
            {
                'name': 'Oil, Vegetable',
                'category': 'Pantry',
                'subcategory': 'Oils & Fats',
                'default_unit': 'gallon',
                'common_units': ['gallon', 'cup', 'fl oz', 'tbsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 3.50,
                'cost_unit': 'gallon',
                'storage_notes': 'Store in cool, dark place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'keto']
            },
            
            # PANTRY - Spices & Seasonings
            {
                'name': 'Salt, Kosher',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'cup', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1825,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Pepper, Black Ground',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'lb',
                'common_units': ['lb', 'oz', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 8.00,
                'cost_unit': 'lb',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Garlic Powder',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.50,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Onion Powder',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.50,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Paprika',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.75,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Cumin, Ground',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.80,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Oregano, Dried',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.60,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Basil, Dried',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.70,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Thyme, Dried',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.75,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Rosemary, Dried',
                'category': 'Pantry',
                'subcategory': 'Spices & Seasonings',
                'default_unit': 'oz',
                'common_units': ['oz', 'lb', 'tbsp', 'tsp'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 0.80,
                'cost_unit': 'oz',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 1095,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            
            # PANTRY - Canned & Preserved
            {
                'name': 'Tomatoes, Canned Crushed',
                'category': 'Pantry',
                'subcategory': 'Canned & Preserved',
                'default_unit': 'can',
                'common_units': ['can', 'oz', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'can',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Tomatoes, Canned Diced',
                'category': 'Pantry',
                'subcategory': 'Canned & Preserved',
                'default_unit': 'can',
                'common_units': ['can', 'oz', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'can',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Beans, Black Canned',
                'category': 'Pantry',
                'subcategory': 'Canned & Preserved',
                'default_unit': 'can',
                'common_units': ['can', 'oz', 'cup'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 1.25,
                'cost_unit': 'can',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Chicken Stock',
                'category': 'Pantry',
                'subcategory': 'Canned & Preserved',
                'default_unit': 'quart',
                'common_units': ['quart', 'cup', 'fl oz', 'can'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'quart',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free']
            },
            {
                'name': 'Beef Stock',
                'category': 'Pantry',
                'subcategory': 'Canned & Preserved',
                'default_unit': 'quart',
                'common_units': ['quart', 'cup', 'fl oz', 'can'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'quart',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['gluten-free', 'dairy-free']
            },
            {
                'name': 'Vegetable Stock',
                'category': 'Pantry',
                'subcategory': 'Canned & Preserved',
                'default_unit': 'quart',
                'common_units': ['quart', 'cup', 'fl oz', 'can'],
                'typical_yield_pct': 100.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'quart',
                'storage_notes': 'Store in cool, dry place',
                'shelf_life_days': 730,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            
            # HERBS - Fresh
            {
                'name': 'Basil, Fresh',
                'category': 'Herbs',
                'subcategory': 'Fresh',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'oz', 'cup', 'tbsp'],
                'typical_yield_pct': 95.0,
                'typical_ap_cost': 2.50,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate, store like flowers',
                'shelf_life_days': 5,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Parsley, Fresh',
                'category': 'Herbs',
                'subcategory': 'Fresh',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'oz', 'cup', 'tbsp'],
                'typical_yield_pct': 90.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate, store like flowers',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Cilantro, Fresh',
                'category': 'Herbs',
                'subcategory': 'Fresh',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'oz', 'cup', 'tbsp'],
                'typical_yield_pct': 85.0,
                'typical_ap_cost': 1.50,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate, store like flowers',
                'shelf_life_days': 5,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Thyme, Fresh',
                'category': 'Herbs',
                'subcategory': 'Fresh',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'oz', 'tbsp', 'tsp'],
                'typical_yield_pct': 95.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate, store like flowers',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Rosemary, Fresh',
                'category': 'Herbs',
                'subcategory': 'Fresh',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'oz', 'tbsp', 'tsp'],
                'typical_yield_pct': 95.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate, store like flowers',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
            {
                'name': 'Oregano, Fresh',
                'category': 'Herbs',
                'subcategory': 'Fresh',
                'default_unit': 'bunch',
                'common_units': ['bunch', 'oz', 'tbsp', 'tsp'],
                'typical_yield_pct': 95.0,
                'typical_ap_cost': 2.00,
                'cost_unit': 'bunch',
                'storage_notes': 'Refrigerate, store like flowers',
                'shelf_life_days': 7,
                'allergens': [],
                'dietary_tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free']
            },
        ]
    
    def add_ingredient(self, ingredient_data: Dict[str, Any]) -> int:
        """Add a new ingredient to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ingredients (
                name, category, subcategory, default_unit, common_units,
                typical_yield_pct, typical_ap_cost, cost_unit,
                storage_notes, shelf_life_days, allergens, dietary_tags,
                substitutes, notes, source_url, created_date, updated_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ingredient_data['name'],
            ingredient_data.get('category', 'Other'),
            ingredient_data.get('subcategory'),
            ingredient_data.get('default_unit', 'lb'),
            json.dumps(ingredient_data.get('common_units', [])),
            ingredient_data.get('typical_yield_pct', 100.0),
            ingredient_data.get('typical_ap_cost'),
            ingredient_data.get('cost_unit'),
            ingredient_data.get('storage_notes'),
            ingredient_data.get('shelf_life_days'),
            json.dumps(ingredient_data.get('allergens', [])),
            json.dumps(ingredient_data.get('dietary_tags', [])),
            json.dumps(ingredient_data.get('substitutes', [])),
            ingredient_data.get('notes'),
            ingredient_data.get('source_url'),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        ingredient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return ingredient_id
    
    def update_ingredient(self, ingredient_id: int, ingredient_data: Dict[str, Any]):
        """Update an existing ingredient."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE ingredients SET
                name = ?, category = ?, subcategory = ?, default_unit = ?,
                common_units = ?, typical_yield_pct = ?, typical_ap_cost = ?,
                cost_unit = ?, storage_notes = ?, shelf_life_days = ?,
                allergens = ?, dietary_tags = ?, substitutes = ?, notes = ?,
                source_url = ?, updated_date = ?
            WHERE id = ?
        ''', (
            ingredient_data['name'],
            ingredient_data.get('category', 'Other'),
            ingredient_data.get('subcategory'),
            ingredient_data.get('default_unit', 'lb'),
            json.dumps(ingredient_data.get('common_units', [])),
            ingredient_data.get('typical_yield_pct', 100.0),
            ingredient_data.get('typical_ap_cost'),
            ingredient_data.get('cost_unit'),
            ingredient_data.get('storage_notes'),
            ingredient_data.get('shelf_life_days'),
            json.dumps(ingredient_data.get('allergens', [])),
            json.dumps(ingredient_data.get('dietary_tags', [])),
            json.dumps(ingredient_data.get('substitutes', [])),
            ingredient_data.get('notes'),
            ingredient_data.get('source_url'),
            datetime.now().isoformat(),
            ingredient_id
        ))
        
        conn.commit()
        conn.close()
    
    def get_ingredient(self, ingredient_id: int) -> Optional[Dict[str, Any]]:
        """Get ingredient by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def search_ingredients(self, search_term: str = "", category: str = "") -> List[Dict[str, Any]]:
        """Search ingredients by name or category."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM ingredients WHERE is_active = 1"
        params = []
        
        if search_term:
            query += " AND name LIKE ?"
            params.append(f"%{search_term}%")
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY category, name"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_categories(self) -> List[str]:
        """Get all ingredient categories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM ingredients WHERE is_active = 1 ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return categories
    
    def get_ingredient_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get ingredient by exact name."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ingredients WHERE name = ? AND is_active = 1", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """Convert database row to dictionary."""
        return {
            'id': row['id'],
            'name': row['name'],
            'category': row['category'],
            'subcategory': row['subcategory'],
            'default_unit': row['default_unit'],
            'common_units': json.loads(row['common_units']) if row['common_units'] else [],
            'typical_yield_pct': row['typical_yield_pct'],
            'typical_ap_cost': row['typical_ap_cost'],
            'cost_unit': row['cost_unit'],
            'storage_notes': row['storage_notes'],
            'shelf_life_days': row['shelf_life_days'],
            'allergens': json.loads(row['allergens']) if row['allergens'] else [],
            'dietary_tags': json.loads(row['dietary_tags']) if row['dietary_tags'] else [],
            'substitutes': json.loads(row['substitutes']) if row['substitutes'] else [],
            'notes': row['notes'],
            'source_url': row['source_url'],
            'created_date': row['created_date'],
            'updated_date': row['updated_date']
        }
    
    def delete_ingredient(self, ingredient_id: int, soft_delete: bool = True):
        """Delete or deactivate an ingredient."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if soft_delete:
            cursor.execute("UPDATE ingredients SET is_active = 0 WHERE id = ?", (ingredient_id,))
        else:
            cursor.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ingredients WHERE is_active = 1")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM ingredients WHERE is_active = 1 GROUP BY category")
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_ingredients': total,
            'by_category': by_category
        }


def main():
    """CLI interface for ingredient database."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Ingredient Database Manager')
    parser.add_argument('--search', '-s', help='Search ingredients')
    parser.add_argument('--category', '-c', help='Filter by category')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    db = IngredientDatabase()
    
    if args.stats:
        stats = db.get_statistics()
        print(f"\n📊 Ingredient Database Statistics")
        print("=" * 50)
        print(f"Total Ingredients: {stats['total_ingredients']}")
        print("\nBy Category:")
        for category, count in stats['by_category'].items():
            print(f"  • {category}: {count}")
    
    elif args.search or args.category:
        results = db.search_ingredients(args.search or "", args.category or "")
        print(f"\n🔍 Found {len(results)} ingredients:\n")
        for ing in results:
            print(f"{ing['name']} ({ing['category']})")
            print(f"  Unit: {ing['default_unit']}, Yield: {ing['typical_yield_pct']}%")
            if ing['typical_ap_cost']:
                print(f"  Cost: ${ing['typical_ap_cost']:.2f}/{ing['cost_unit']}")
            print()
    else:
        stats = db.get_statistics()
        print(f"\n✅ Ingredient Database Ready!")
        print(f"   Total ingredients: {stats['total_ingredients']}")
        print(f"\nUse --search or --category to find ingredients")
        print(f"Use --stats to see full statistics")


if __name__ == '__main__':
    main()

