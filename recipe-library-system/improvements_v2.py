#!/usr/bin/env python3
"""
Recipe System Improvements V2
Quick wins: Better cuisine detection, ingredient parsing, cost database
"""

import re
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class ImprovedCuisineDetector:
    """Enhanced cuisine detection with better accuracy."""
    
    def __init__(self):
        self.cuisine_keywords = {
            'italian': {
                'high': ['pasta', 'risotto', 'pizza', 'lasagna', 'ravioli', 'gnocchi', 'tiramisu', 'panna cotta', 'carbonara', 'bolognese', 'marinara', 'pesto', 'parmesan', 'parmigiano', 'mozzarella', 'prosciutto'],
                'medium': ['basil', 'oregano', 'garlic', 'olive oil', 'tomato', 'balsamic', 'parsley'],
                'low': ['italian', 'rome', 'tuscany', 'sicilian']
            },
            'mexican': {
                'high': ['taco', 'burrito', 'enchilada', 'quesadilla', 'tamale', 'guacamole', 'salsa', 'tortilla', 'fajita', 'nachos', 'churro'],
                'medium': ['cilantro', 'lime', 'cumin', 'chipotle', 'jalapeño', 'avocado', 'queso', 'cotija'],
                'low': ['mexican', 'tex-mex']
            },
            'chinese': {
                'high': ['stir fry', 'dumpling', 'dim sum', 'chow mein', 'kung pao', 'sweet and sour', 'szechuan', 'wonton', 'fried rice'],
                'medium': ['soy sauce', 'ginger', 'sesame', 'hoisin', 'rice vinegar', 'star anise', 'five spice'],
                'low': ['chinese', 'cantonese', 'mandarin']
            },
            'indian': {
                'high': ['curry', 'naan', 'tandoori', 'biryani', 'masala', 'tikka', 'samosa', 'chutney', 'dal', 'paneer'],
                'medium': ['turmeric', 'cumin', 'coriander', 'cardamom', 'garam masala', 'ghee', 'chili', 'lentil'],
                'low': ['indian', 'punjabi', 'bengali']
            },
            'french': {
                'high': ['croissant', 'baguette', 'ratatouille', 'coq au vin', 'bouillabaisse', 'crème brûlée', 'quiche', 'soufflé', 'béarnaise', 'hollandaise'],
                'medium': ['butter', 'cream', 'wine', 'shallot', 'tarragon', 'thyme', 'cognac'],
                'low': ['french', 'parisian', 'provençal']
            },
            'japanese': {
                'high': ['sushi', 'sashimi', 'ramen', 'tempura', 'teriyaki', 'miso', 'udon', 'soba', 'yakitori', 'tonkatsu'],
                'medium': ['soy', 'mirin', 'sake', 'wasabi', 'nori', 'dashi', 'bonito', 'edamame'],
                'low': ['japanese', 'tokyo', 'kyoto']
            },
            'thai': {
                'high': ['pad thai', 'tom yum', 'green curry', 'red curry', 'pad see ew', 'som tam', 'satay', 'thai basil'],
                'medium': ['fish sauce', 'lemongrass', 'galangal', 'kaffir lime', 'coconut milk', 'palm sugar'],
                'low': ['thai', 'bangkok']
            },
            'mediterranean': {
                'high': ['hummus', 'falafel', 'tabbouleh', 'tzatziki', 'baklava', 'moussaka', 'dolma', 'shawarma'],
                'medium': ['olive oil', 'feta', 'za\'atar', 'sumac', 'tahini', 'pomegranate', 'mint', 'lemon'],
                'low': ['mediterranean', 'greek', 'lebanese', 'turkish']
            },
            'american': {
                'high': ['burger', 'hot dog', 'barbecue', 'bbq', 'fried chicken', 'mac and cheese', 'apple pie', 'coleslaw', 'cornbread'],
                'medium': ['ketchup', 'mustard', 'ranch', 'bacon', 'cheddar', 'maple syrup'],
                'low': ['american', 'southern', 'cajun', 'creole']
            }
        }
    
    def detect_cuisine(self, title: str, ingredients: str, method: str = "") -> Tuple[str, float]:
        """
        Detect cuisine with confidence score.
        Returns: (cuisine, confidence)
        """
        text = f"{title} {ingredients} {method}".lower()
        scores = {}
        
        for cuisine, keyword_levels in self.cuisine_keywords.items():
            score = 0.0
            
            # High confidence keywords (title matches)
            for keyword in keyword_levels['high']:
                if keyword in text:
                    # Higher weight if in title
                    if keyword in title.lower():
                        score += 0.40
                    else:
                        score += 0.20
            
            # Medium confidence keywords (ingredients)
            for keyword in keyword_levels['medium']:
                if keyword in text:
                    score += 0.10
            
            # Low confidence keywords (general terms)
            for keyword in keyword_levels['low']:
                if keyword in text:
                    score += 0.05
            
            scores[cuisine] = min(score, 1.0)  # Cap at 1.0
        
        if not scores or max(scores.values()) < 0.15:
            return ('unknown', 0.0)
        
        best_cuisine = max(scores, key=scores.get)
        confidence = scores[best_cuisine]
        
        return (best_cuisine, confidence)


class IngredientParser:
    """Parse ingredient strings into structured data."""
    
    # Common units
    UNITS = [
        # Volume
        'cup', 'cups', 'c',
        'tablespoon', 'tablespoons', 'tbsp', 'tbs', 'T',
        'teaspoon', 'teaspoons', 'tsp', 'ts', 't',
        'gallon', 'gallons', 'gal',
        'quart', 'quarts', 'qt',
        'pint', 'pints', 'pt',
        'fluid ounce', 'fluid ounces', 'fl oz',
        'milliliter', 'milliliters', 'ml',
        'liter', 'liters', 'l',
        # Weight
        'pound', 'pounds', 'lb', 'lbs', '#',
        'ounce', 'ounces', 'oz',
        'gram', 'grams', 'g',
        'kilogram', 'kilograms', 'kg',
        # Count
        'piece', 'pieces', 'pc',
        'each', 'ea',
        'bunch', 'bunches',
        'clove', 'cloves',
        'slice', 'slices',
        'can', 'cans',
        'package', 'packages', 'pkg'
    ]
    
    # Preparation methods
    PREP_METHODS = [
        'diced', 'chopped', 'minced', 'sliced', 'julienned',
        'grated', 'shredded', 'crushed', 'ground',
        'peeled', 'trimmed', 'cleaned',
        'fresh', 'frozen', 'canned', 'dried',
        'whole', 'halved', 'quartered'
    ]
    
    def parse_ingredient(self, ingredient_line: str) -> Dict[str, str]:
        """
        Parse ingredient line into components.
        
        Examples:
        "2 cups flour, sifted" → {quantity: "2", unit: "cups", ingredient: "flour", prep: "sifted"}
        "1 lb onions, diced" → {quantity: "1", unit: "lb", ingredient: "onions", prep: "diced"}
        "3 cloves garlic, minced" → {quantity: "3", unit: "cloves", ingredient: "garlic", prep: "minced"}
        """
        
        result = {
            'quantity': '',
            'unit': '',
            'ingredient': '',
            'prep': '',
            'original': ingredient_line
        }
        
        line = ingredient_line.strip()
        
        # Extract quantity (number or fraction at start)
        quantity_pattern = r'^(\d+\.?\d*|\d+\/\d+|\d+\s+\d+\/\d+)'
        quantity_match = re.search(quantity_pattern, line)
        if quantity_match:
            result['quantity'] = quantity_match.group(1)
            line = line[quantity_match.end():].strip()
        
        # Extract unit
        for unit in self.UNITS:
            pattern = r'^\b' + re.escape(unit) + r'\b'
            if re.match(pattern, line, re.IGNORECASE):
                result['unit'] = unit
                line = line[len(unit):].strip()
                break
        
        # Split on comma to separate ingredient from prep
        parts = line.split(',', 1)
        result['ingredient'] = parts[0].strip()
        
        if len(parts) > 1:
            result['prep'] = parts[1].strip()
        
        return result
    
    def parse_ingredient_list(self, ingredients_text: str) -> List[Dict[str, str]]:
        """Parse multiple ingredients from text."""
        lines = ingredients_text.strip().split('\n')
        parsed = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip comments
                parsed.append(self.parse_ingredient(line))
        
        return parsed


class IngredientCostDatabase:
    """Database for storing and retrieving ingredient costs."""
    
    def __init__(self, db_path: str = "recipe_library/ingredient_costs.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the ingredient cost database."""
        Path(self.db_path).parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredient_costs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_name TEXT NOT NULL,
                ap_cost REAL,
                unit TEXT,
                yield_percentage REAL DEFAULT 100.0,
                vendor TEXT,
                last_updated DATE DEFAULT CURRENT_DATE,
                notes TEXT,
                UNIQUE(ingredient_name, vendor)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cost_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_name TEXT NOT NULL,
                ap_cost REAL,
                unit TEXT,
                vendor TEXT,
                date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_or_update_cost(self, ingredient: str, ap_cost: float, unit: str, 
                          yield_pct: float = 100.0, vendor: str = "Default", 
                          notes: str = ""):
        """Add or update ingredient cost."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add to history
        cursor.execute('''
            INSERT INTO cost_history (ingredient_name, ap_cost, unit, vendor)
            VALUES (?, ?, ?, ?)
        ''', (ingredient, ap_cost, unit, vendor))
        
        # Update or insert current cost
        cursor.execute('''
            INSERT INTO ingredient_costs 
            (ingredient_name, ap_cost, unit, yield_percentage, vendor, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(ingredient_name, vendor) 
            DO UPDATE SET 
                ap_cost = excluded.ap_cost,
                unit = excluded.unit,
                yield_percentage = excluded.yield_percentage,
                last_updated = CURRENT_DATE,
                notes = excluded.notes
        ''', (ingredient, ap_cost, unit, yield_pct, vendor, notes))
        
        conn.commit()
        conn.close()
    
    def get_cost(self, ingredient: str, vendor: str = "Default") -> Optional[Dict]:
        """Get current cost for ingredient."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ingredient_name, ap_cost, unit, yield_percentage, vendor, last_updated, notes
            FROM ingredient_costs
            WHERE ingredient_name = ? AND vendor = ?
        ''', (ingredient, vendor))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'ingredient': row[0],
                'ap_cost': row[1],
                'unit': row[2],
                'yield_pct': row[3],
                'vendor': row[4],
                'last_updated': row[5],
                'notes': row[6]
            }
        return None
    
    def search_ingredient(self, search_term: str) -> List[Dict]:
        """Search for ingredients by partial name."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT ingredient_name, ap_cost, unit, yield_percentage
            FROM ingredient_costs
            WHERE ingredient_name LIKE ?
            ORDER BY ingredient_name
        ''', (f'%{search_term}%',))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'ingredient': row[0],
                'ap_cost': row[1],
                'unit': row[2],
                'yield_pct': row[3]
            })
        
        conn.close()
        return results
    
    def get_price_history(self, ingredient: str) -> List[Dict]:
        """Get price history for an ingredient."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, ap_cost, unit, vendor
            FROM cost_history
            WHERE ingredient_name = ?
            ORDER BY date DESC
        ''', (ingredient,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'date': row[0],
                'ap_cost': row[1],
                'unit': row[2],
                'vendor': row[3]
            })
        
        conn.close()
        return history
    
    def populate_common_ingredients(self):
        """Populate database with common ingredient costs (examples)."""
        common_costs = [
            # Produce
            ('onions, yellow', 1.50, 'lb', 90.0),
            ('onions, red', 1.75, 'lb', 90.0),
            ('garlic', 3.00, 'lb', 85.0),
            ('tomatoes', 2.50, 'lb', 95.0),
            ('potatoes', 0.80, 'lb', 85.0),
            ('carrots', 1.20, 'lb', 90.0),
            ('celery', 1.50, 'lb', 75.0),
            ('bell peppers', 3.00, 'lb', 85.0),
            
            # Dairy
            ('butter', 4.50, 'lb', 100.0),
            ('cream, heavy', 5.00, 'quart', 100.0),
            ('milk, whole', 3.50, 'gallon', 100.0),
            ('cheese, cheddar', 5.00, 'lb', 100.0),
            ('cheese, parmesan', 12.00, 'lb', 100.0),
            ('eggs', 3.00, 'dozen', 88.0),
            
            # Pantry
            ('flour, all-purpose', 0.60, 'lb', 100.0),
            ('sugar, granulated', 0.70, 'lb', 100.0),
            ('sugar, brown', 0.90, 'lb', 100.0),
            ('salt, kosher', 1.50, 'lb', 100.0),
            ('pepper, black', 8.00, 'lb', 100.0),
            ('oil, olive', 15.00, 'liter', 100.0),
            ('oil, canola', 4.00, 'gallon', 100.0),
            ('oil, vegetable', 3.50, 'gallon', 100.0),
            
            # Proteins
            ('chicken breast', 4.50, 'lb', 90.0),
            ('chicken thigh', 3.00, 'lb', 85.0),
            ('beef, ground', 5.50, 'lb', 90.0),
            ('pork, chop', 4.00, 'lb', 85.0),
            ('salmon', 12.00, 'lb', 70.0),
            ('shrimp', 10.00, 'lb', 75.0),
        ]
        
        for ingredient, cost, unit, yield_pct in common_costs:
            self.add_or_update_cost(ingredient, cost, unit, yield_pct, "Default", 
                                  "Example cost - update with actual prices")


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("           RECIPE SYSTEM IMPROVEMENTS V2")
    print("=" * 80)
    
    # Test cuisine detection
    print("\n1. Enhanced Cuisine Detection")
    print("-" * 80)
    detector = ImprovedCuisineDetector()
    
    test_recipes = [
        ("Spaghetti Carbonara", "pasta, eggs, bacon, parmesan, black pepper"),
        ("Chicken Tacos", "chicken, tortillas, cilantro, lime, avocado"),
        ("Pad Thai", "rice noodles, fish sauce, tamarind, peanuts"),
        ("Butter Chicken", "chicken, butter, cream, garam masala, tomato"),
    ]
    
    for title, ingredients in test_recipes:
        cuisine, confidence = detector.detect_cuisine(title, ingredients)
        print(f"\n{title}")
        print(f"  Detected: {cuisine.upper()} (confidence: {confidence:.1%})")
    
    # Test ingredient parsing
    print("\n\n2. Ingredient Parsing")
    print("-" * 80)
    parser = IngredientParser()
    
    test_ingredients = [
        "2 cups flour, sifted",
        "1 lb onions, diced",
        "3 cloves garlic, minced",
        "1/2 cup olive oil",
        "4 oz butter",
    ]
    
    for ing in test_ingredients:
        parsed = parser.parse_ingredient(ing)
        print(f"\n'{ing}'")
        print(f"  > Qty: {parsed['quantity']}, Unit: {parsed['unit']}, " 
              f"Ingredient: {parsed['ingredient']}, Prep: {parsed['prep']}")
    
    # Test cost database
    print("\n\n3. Ingredient Cost Database")
    print("-" * 80)
    cost_db = IngredientCostDatabase()
    cost_db.populate_common_ingredients()
    
    print("\nPopulated database with common ingredients")
    print("\nSample costs:")
    for ingredient in ['onions, yellow', 'butter', 'flour, all-purpose', 'chicken breast']:
        cost_data = cost_db.get_cost(ingredient)
        if cost_data:
            ep_cost = cost_data['ap_cost'] / (cost_data['yield_pct'] / 100)
            print(f"  {ingredient}:")
            print(f"    AP Cost: ${cost_data['ap_cost']:.2f}/{cost_data['unit']}")
            print(f"    Yield: {cost_data['yield_pct']}%")
            print(f"    EP Cost: ${ep_cost:.2f}/{cost_data['unit']}")
    
    print("\n" + "=" * 80)
    print("Improvements ready to integrate into main system!")
    print("=" * 80)

