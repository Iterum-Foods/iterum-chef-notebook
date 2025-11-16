#!/usr/bin/env python3
"""
Populate Ingredients Database
Preloads the database with common culinary ingredients
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal, Ingredient, Base, engine
from sqlalchemy.orm import sessionmaker
import json

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_ingredient_data():
    """Create comprehensive ingredient data"""
    
    ingredients = [
        # Dairy & Eggs
        {
            "name": "Whole Milk",
            "category": "Dairy & Eggs",
            "default_unit": "cup",
            "description": "Fresh whole milk from cows",
            "nutritional_info": {
                "calories": 149,
                "protein": "8g",
                "fat": "8g",
                "carbs": "12g",
                "calcium": "276mg"
            },
            "allergens": ["milk"]
        },
        {
            "name": "Heavy Cream",
            "category": "Dairy & Eggs",
            "default_unit": "cup",
            "description": "High-fat cream for cooking and baking",
            "nutritional_info": {
                "calories": 821,
                "protein": "5g",
                "fat": "88g",
                "carbs": "7g"
            },
            "allergens": ["milk"]
        },
        {
            "name": "Butter",
            "category": "Dairy & Eggs",
            "default_unit": "tbsp",
            "description": "Unsalted butter for cooking and baking",
            "nutritional_info": {
                "calories": 102,
                "protein": "0.1g",
                "fat": "12g",
                "carbs": "0.1g"
            },
            "allergens": ["milk"]
        },
        {
            "name": "Eggs",
            "category": "Dairy & Eggs",
            "default_unit": "large",
            "description": "Fresh large chicken eggs",
            "nutritional_info": {
                "calories": 70,
                "protein": "6g",
                "fat": "5g",
                "carbs": "0.6g"
            },
            "allergens": ["eggs"]
        },
        {
            "name": "Cheese (Cheddar)",
            "category": "Dairy & Eggs",
            "default_unit": "cup",
            "description": "Sharp cheddar cheese, shredded",
            "nutritional_info": {
                "calories": 455,
                "protein": "25g",
                "fat": "37g",
                "carbs": "1.4g",
                "calcium": "721mg"
            },
            "allergens": ["milk"]
        },
        
        # Proteins
        {
            "name": "Chicken Breast",
            "category": "Proteins",
            "default_unit": "lb",
            "description": "Boneless, skinless chicken breast",
            "nutritional_info": {
                "calories": 165,
                "protein": "31g",
                "fat": "3.6g",
                "carbs": "0g"
            },
            "allergens": []
        },
        {
            "name": "Ground Beef",
            "category": "Proteins",
            "default_unit": "lb",
            "description": "80/20 ground beef",
            "nutritional_info": {
                "calories": 332,
                "protein": "26g",
                "fat": "24g",
                "carbs": "0g"
            },
            "allergens": []
        },
        {
            "name": "Salmon",
            "category": "Proteins",
            "default_unit": "lb",
            "description": "Fresh Atlantic salmon fillet",
            "nutritional_info": {
                "calories": 208,
                "protein": "25g",
                "fat": "12g",
                "carbs": "0g",
                "omega3": "2.3g"
            },
            "allergens": ["fish"]
        },
        {
            "name": "Shrimp",
            "category": "Proteins",
            "default_unit": "lb",
            "description": "Large peeled and deveined shrimp",
            "nutritional_info": {
                "calories": 99,
                "protein": "24g",
                "fat": "0.3g",
                "carbs": "0.2g"
            },
            "allergens": ["shellfish"]
        },
        {
            "name": "Tofu",
            "category": "Proteins",
            "default_unit": "block",
            "description": "Firm tofu for cooking",
            "nutritional_info": {
                "calories": 144,
                "protein": "17g",
                "fat": "8g",
                "carbs": "3g",
                "calcium": "421mg"
            },
            "allergens": ["soy"]
        },
        
        # Vegetables
        {
            "name": "Onion",
            "category": "Vegetables",
            "default_unit": "medium",
            "description": "Yellow onion for cooking",
            "nutritional_info": {
                "calories": 44,
                "protein": "1.2g",
                "fat": "0.1g",
                "carbs": "10g",
                "fiber": "1.9g"
            },
            "allergens": []
        },
        {
            "name": "Garlic",
            "category": "Vegetables",
            "default_unit": "clove",
            "description": "Fresh garlic clove",
            "nutritional_info": {
                "calories": 4,
                "protein": "0.2g",
                "fat": "0g",
                "carbs": "1g"
            },
            "allergens": []
        },
        {
            "name": "Tomatoes",
            "category": "Vegetables",
            "default_unit": "medium",
            "description": "Fresh ripe tomatoes",
            "nutritional_info": {
                "calories": 22,
                "protein": "1.1g",
                "fat": "0.2g",
                "carbs": "4.8g",
                "vitamin_c": "16.9mg"
            },
            "allergens": []
        },
        {
            "name": "Bell Peppers",
            "category": "Vegetables",
            "default_unit": "medium",
            "description": "Red bell pepper",
            "nutritional_info": {
                "calories": 31,
                "protein": "1g",
                "fat": "0.3g",
                "carbs": "7g",
                "vitamin_c": "152mg"
            },
            "allergens": []
        },
        {
            "name": "Spinach",
            "category": "Vegetables",
            "default_unit": "cup",
            "description": "Fresh baby spinach leaves",
            "nutritional_info": {
                "calories": 7,
                "protein": "0.9g",
                "fat": "0.1g",
                "carbs": "1.1g",
                "iron": "0.8mg"
            },
            "allergens": []
        },
        
        # Fruits
        {
            "name": "Lemons",
            "category": "Fruits",
            "default_unit": "medium",
            "description": "Fresh lemon for juice and zest",
            "nutritional_info": {
                "calories": 17,
                "protein": "0.6g",
                "fat": "0.2g",
                "carbs": "5.4g",
                "vitamin_c": "30.7mg"
            },
            "allergens": []
        },
        {
            "name": "Limes",
            "category": "Fruits",
            "default_unit": "medium",
            "description": "Fresh lime for juice and zest",
            "nutritional_info": {
                "calories": 20,
                "protein": "0.5g",
                "fat": "0.1g",
                "carbs": "7.1g",
                "vitamin_c": "19.5mg"
            },
            "allergens": []
        },
        {
            "name": "Apples",
            "category": "Fruits",
            "default_unit": "medium",
            "description": "Fresh crisp apple",
            "nutritional_info": {
                "calories": 95,
                "protein": "0.5g",
                "fat": "0.3g",
                "carbs": "25g",
                "fiber": "4.4g"
            },
            "allergens": []
        },
        
        # Grains & Starches
        {
            "name": "All-Purpose Flour",
            "category": "Grains & Starches",
            "default_unit": "cup",
            "description": "Unbleached all-purpose flour",
            "nutritional_info": {
                "calories": 455,
                "protein": "13g",
                "fat": "1.2g",
                "carbs": "95g",
                "fiber": "3.4g"
            },
            "allergens": ["wheat", "gluten"]
        },
        {
            "name": "Rice (White)",
            "category": "Grains & Starches",
            "default_unit": "cup",
            "description": "Long grain white rice",
            "nutritional_info": {
                "calories": 205,
                "protein": "4.3g",
                "fat": "0.4g",
                "carbs": "45g"
            },
            "allergens": []
        },
        {
            "name": "Pasta",
            "category": "Grains & Starches",
            "default_unit": "cup",
            "description": "Dry pasta (spaghetti, penne, etc.)",
            "nutritional_info": {
                "calories": 131,
                "protein": "5g",
                "fat": "1.1g",
                "carbs": "25g"
            },
            "allergens": ["wheat", "gluten"]
        },
        {
            "name": "Potatoes",
            "category": "Grains & Starches",
            "default_unit": "medium",
            "description": "Russet potatoes",
            "nutritional_info": {
                "calories": 161,
                "protein": "4.3g",
                "fat": "0.2g",
                "carbs": "37g",
                "potassium": "897mg"
            },
            "allergens": []
        },
        
        # Herbs & Spices
        {
            "name": "Salt",
            "category": "Herbs & Spices",
            "default_unit": "tsp",
            "description": "Kosher salt for cooking",
            "nutritional_info": {
                "calories": 0,
                "protein": "0g",
                "fat": "0g",
                "carbs": "0g",
                "sodium": "2325mg"
            },
            "allergens": []
        },
        {
            "name": "Black Pepper",
            "category": "Herbs & Spices",
            "default_unit": "tsp",
            "description": "Freshly ground black pepper",
            "nutritional_info": {
                "calories": 6,
                "protein": "0.3g",
                "fat": "0.1g",
                "carbs": "1.5g"
            },
            "allergens": []
        },
        {
            "name": "Basil",
            "category": "Herbs & Spices",
            "default_unit": "cup",
            "description": "Fresh basil leaves",
            "nutritional_info": {
                "calories": 22,
                "protein": "3.2g",
                "fat": "0.6g",
                "carbs": "2.7g",
                "vitamin_a": "5275IU"
            },
            "allergens": []
        },
        {
            "name": "Oregano",
            "category": "Herbs & Spices",
            "default_unit": "tsp",
            "description": "Dried oregano",
            "nutritional_info": {
                "calories": 3,
                "protein": "0.1g",
                "fat": "0.1g",
                "carbs": "0.7g"
            },
            "allergens": []
        },
        
        # Oils & Fats
        {
            "name": "Olive Oil",
            "category": "Oils & Fats",
            "default_unit": "tbsp",
            "description": "Extra virgin olive oil",
            "nutritional_info": {
                "calories": 119,
                "protein": "0g",
                "fat": "14g",
                "carbs": "0g"
            },
            "allergens": []
        },
        {
            "name": "Vegetable Oil",
            "category": "Oils & Fats",
            "default_unit": "tbsp",
            "description": "Neutral vegetable oil for cooking",
            "nutritional_info": {
                "calories": 120,
                "protein": "0g",
                "fat": "14g",
                "carbs": "0g"
            },
            "allergens": []
        },
        
        # Nuts & Seeds
        {
            "name": "Almonds",
            "category": "Nuts & Seeds",
            "default_unit": "cup",
            "description": "Raw almonds",
            "nutritional_info": {
                "calories": 164,
                "protein": "6g",
                "fat": "14g",
                "carbs": "6g",
                "vitamin_e": "7.7mg"
            },
            "allergens": ["tree_nuts"]
        },
        {
            "name": "Walnuts",
            "category": "Nuts & Seeds",
            "default_unit": "cup",
            "description": "Raw walnut halves",
            "nutritional_info": {
                "calories": 185,
                "protein": "4.3g",
                "fat": "18g",
                "carbs": "3.9g",
                "omega3": "2.6g"
            },
            "allergens": ["tree_nuts"]
        },
        
        # Sweeteners
        {
            "name": "Sugar (White)",
            "category": "Sweeteners",
            "default_unit": "cup",
            "description": "Granulated white sugar",
            "nutritional_info": {
                "calories": 774,
                "protein": "0g",
                "fat": "0g",
                "carbs": "200g"
            },
            "allergens": []
        },
        {
            "name": "Honey",
            "category": "Sweeteners",
            "default_unit": "tbsp",
            "description": "Pure natural honey",
            "nutritional_info": {
                "calories": 64,
                "protein": "0.1g",
                "fat": "0g",
                "carbs": "17g"
            },
            "allergens": []
        },
        
        # Condiments & Sauces
        {
            "name": "Soy Sauce",
            "category": "Condiments & Sauces",
            "default_unit": "tbsp",
            "description": "Traditional soy sauce",
            "nutritional_info": {
                "calories": 8,
                "protein": "1.3g",
                "fat": "0g",
                "carbs": "0.8g",
                "sodium": "879mg"
            },
            "allergens": ["soy", "wheat"]
        },
        {
            "name": "Mustard",
            "category": "Condiments & Sauces",
            "default_unit": "tsp",
            "description": "Dijon mustard",
            "nutritional_info": {
                "calories": 3,
                "protein": "0.2g",
                "fat": "0.2g",
                "carbs": "0.3g"
            },
            "allergens": []
        },
        {
            "name": "Ketchup",
            "category": "Condiments & Sauces",
            "default_unit": "tbsp",
            "description": "Tomato ketchup",
            "nutritional_info": {
                "calories": 17,
                "protein": "0.2g",
                "fat": "0g",
                "carbs": "4.5g"
            },
            "allergens": []
        }
    ]
    
    return ingredients

def populate_database():
    """Populate the database with ingredients"""
    
    # Create a new session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🚀 Starting ingredient database population...")
        
        # Get existing ingredients to avoid duplicates
        existing_ingredients = {ing.name.lower() for ing in db.query(Ingredient).all()}
        
        # Create ingredient data
        ingredients_data = create_ingredient_data()
        
        # Counter for new ingredients
        new_count = 0
        skipped_count = 0
        
        for ingredient_data in ingredients_data:
            # Check if ingredient already exists
            if ingredient_data["name"].lower() in existing_ingredients:
                print(f"⏭️  Skipping existing ingredient: {ingredient_data['name']}")
                skipped_count += 1
                continue
            
            # Create new ingredient
            ingredient = Ingredient(
                name=ingredient_data["name"],
                category=ingredient_data["category"],
                default_unit=ingredient_data["default_unit"],
                description=ingredient_data["description"],
                nutritional_info=ingredient_data["nutritional_info"],
                allergens=ingredient_data["allergens"],
                is_active=True
            )
            
            db.add(ingredient)
            new_count += 1
            print(f"✅ Added: {ingredient_data['name']} ({ingredient_data['category']})")
        
        # Commit all changes
        db.commit()
        
        print(f"\n🎉 Database population completed!")
        print(f"📊 New ingredients added: {new_count}")
        print(f"⏭️  Existing ingredients skipped: {skipped_count}")
        print(f"📈 Total ingredients in database: {db.query(Ingredient).count()}")
        
        # Show categories summary
        categories = db.query(Ingredient.category).distinct().all()
        print(f"\n📂 Ingredient categories:")
        for category in categories:
            count = db.query(Ingredient).filter(Ingredient.category == category[0]).count()
            print(f"   • {category[0]}: {count} ingredients")
        
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
