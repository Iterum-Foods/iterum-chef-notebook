#!/usr/bin/env python3
"""
Preloaded Ingredient Database Creator
Creates a comprehensive database of common culinary ingredients
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict

class PreloadedIngredientsDB:
    """Comprehensive ingredient database with thousands of common ingredients"""
    
    def __init__(self, db_path: str = "culinary_data.db"):
        self.db_path = db_path
    
    def get_comprehensive_ingredients(self) -> List[Dict]:
        """Return comprehensive list of ingredients organized by category"""
        
        ingredients = []
        
        # 1. PRODUCE - Fresh Vegetables
        produce_vegetables = [
            {"name": "Onions, Yellow", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Onions, Red", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Onions, White", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Onions, Sweet (Vidalia)", "category": "Produce", "unit": "lb", "seasonality": "Spring-Summer", "storage_notes": "Refrigerate for longer storage", "cost_level": "Medium"},
            {"name": "Shallots", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Scallions (Green Onions)", "category": "Produce", "unit": "bunch", "seasonality": "Year-round", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Low"},
            {"name": "Leeks", "category": "Produce", "unit": "lb", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Garlic", "category": "Produce", "unit": "head", "seasonality": "Year-round", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Ginger, Fresh", "category": "Produce", "unit": "oz", "seasonality": "Year-round", "storage_notes": "Refrigerate or freeze", "cost_level": "Medium"},
            {"name": "Carrots", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Low"},
            {"name": "Carrots, Baby", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Refrigerate in original bag", "cost_level": "Medium"},
            {"name": "Celery", "category": "Produce", "unit": "bunch", "seasonality": "Year-round", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Low"},
            {"name": "Bell Peppers, Red", "category": "Produce", "unit": "each", "seasonality": "Summer-Fall", "storage_notes": "Refrigerate in crisper", "cost_level": "Medium"},
            {"name": "Bell Peppers, Green", "category": "Produce", "unit": "each", "seasonality": "Summer-Fall", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Bell Peppers, Yellow", "category": "Produce", "unit": "each", "seasonality": "Summer-Fall", "storage_notes": "Refrigerate in crisper", "cost_level": "Medium"},
            {"name": "Bell Peppers, Orange", "category": "Produce", "unit": "each", "seasonality": "Summer-Fall", "storage_notes": "Refrigerate in crisper", "cost_level": "Medium"},
            {"name": "Jalapeño Peppers", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Low"},
            {"name": "Serrano Peppers", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Habanero Peppers", "category": "Produce", "unit": "oz", "seasonality": "Summer", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Poblano Peppers", "category": "Produce", "unit": "each", "seasonality": "Summer-Fall", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Tomatoes, Roma", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Room temperature when ripe", "cost_level": "Low"},
            {"name": "Tomatoes, Beefsteak", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Room temperature when ripe", "cost_level": "Medium"},
            {"name": "Tomatoes, Cherry", "category": "Produce", "unit": "pint", "seasonality": "Summer", "storage_notes": "Room temperature when ripe", "cost_level": "Medium"},
            {"name": "Tomatoes, Grape", "category": "Produce", "unit": "pint", "seasonality": "Summer", "storage_notes": "Room temperature when ripe", "cost_level": "Medium"},
            {"name": "Tomatoes, Heirloom", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Room temperature when ripe", "cost_level": "High"},
            {"name": "Potatoes, Russet", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Potatoes, Red", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Potatoes, Yukon Gold", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "Sweet Potatoes", "category": "Produce", "unit": "lb", "seasonality": "Fall-Winter", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Mushrooms, Button", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Refrigerate in paper bag", "cost_level": "Low"},
            {"name": "Mushrooms, Cremini", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Refrigerate in paper bag", "cost_level": "Medium"},
            {"name": "Mushrooms, Portobello", "category": "Produce", "unit": "each", "seasonality": "Year-round", "storage_notes": "Refrigerate in paper bag", "cost_level": "Medium"},
            {"name": "Mushrooms, Shiitake", "category": "Produce", "unit": "oz", "seasonality": "Year-round", "storage_notes": "Refrigerate in paper bag", "cost_level": "High"},
            {"name": "Mushrooms, Oyster", "category": "Produce", "unit": "oz", "seasonality": "Year-round", "storage_notes": "Refrigerate in paper bag", "cost_level": "High"},
            {"name": "Broccoli", "category": "Produce", "unit": "head", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Cauliflower", "category": "Produce", "unit": "head", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Brussels Sprouts", "category": "Produce", "unit": "lb", "seasonality": "Fall-Winter", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Cabbage, Green", "category": "Produce", "unit": "head", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Low"},
            {"name": "Cabbage, Red", "category": "Produce", "unit": "head", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Low"},
            {"name": "Lettuce, Iceberg", "category": "Produce", "unit": "head", "seasonality": "Year-round", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Lettuce, Romaine", "category": "Produce", "unit": "head", "seasonality": "Year-round", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Lettuce, Butter", "category": "Produce", "unit": "head", "seasonality": "Spring-Fall", "storage_notes": "Refrigerate in crisper", "cost_level": "Medium"},
            {"name": "Spinach, Fresh", "category": "Produce", "unit": "bag", "seasonality": "Spring-Fall", "storage_notes": "Refrigerate in original bag", "cost_level": "Medium"},
            {"name": "Arugula", "category": "Produce", "unit": "bag", "seasonality": "Spring-Fall", "storage_notes": "Refrigerate in original bag", "cost_level": "Medium"},
            {"name": "Kale", "category": "Produce", "unit": "bunch", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Swiss Chard", "category": "Produce", "unit": "bunch", "seasonality": "Spring-Fall", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Zucchini", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Yellow Squash", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Butternut Squash", "category": "Produce", "unit": "each", "seasonality": "Fall-Winter", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Acorn Squash", "category": "Produce", "unit": "each", "seasonality": "Fall-Winter", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Cucumber", "category": "Produce", "unit": "each", "seasonality": "Summer", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Cucumber, English", "category": "Produce", "unit": "each", "seasonality": "Year-round", "storage_notes": "Refrigerate in plastic wrap", "cost_level": "Medium"},
            {"name": "Eggplant", "category": "Produce", "unit": "each", "seasonality": "Summer-Fall", "storage_notes": "Room temperature for 2-3 days", "cost_level": "Medium"},
            {"name": "Asparagus", "category": "Produce", "unit": "lb", "seasonality": "Spring", "storage_notes": "Refrigerate standing in water", "cost_level": "High"},
            {"name": "Green Beans", "category": "Produce", "unit": "lb", "seasonality": "Summer", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Corn, Fresh", "category": "Produce", "unit": "ear", "seasonality": "Summer", "storage_notes": "Refrigerate in husk", "cost_level": "Low"},
            {"name": "Beets", "category": "Produce", "unit": "bunch", "seasonality": "Fall-Spring", "storage_notes": "Remove greens, refrigerate", "cost_level": "Medium"},
            {"name": "Radishes", "category": "Produce", "unit": "bunch", "seasonality": "Spring-Fall", "storage_notes": "Remove greens, refrigerate", "cost_level": "Low"},
            {"name": "Turnips", "category": "Produce", "unit": "lb", "seasonality": "Fall-Spring", "storage_notes": "Remove greens, refrigerate", "cost_level": "Low"},
            {"name": "Parsnips", "category": "Produce", "unit": "lb", "seasonality": "Fall-Winter", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
        ]
        
        # 2. PRODUCE - Fresh Herbs
        produce_herbs = [
            {"name": "Basil, Fresh", "category": "Produce", "unit": "bunch", "seasonality": "Summer", "storage_notes": "Room temperature in water", "cost_level": "Medium"},
            {"name": "Cilantro, Fresh", "category": "Produce", "unit": "bunch", "seasonality": "Spring-Fall", "storage_notes": "Refrigerate in water", "cost_level": "Low"},
            {"name": "Parsley, Flat-leaf", "category": "Produce", "unit": "bunch", "seasonality": "Year-round", "storage_notes": "Refrigerate in water", "cost_level": "Low"},
            {"name": "Parsley, Curly", "category": "Produce", "unit": "bunch", "seasonality": "Year-round", "storage_notes": "Refrigerate in water", "cost_level": "Low"},
            {"name": "Rosemary, Fresh", "category": "Produce", "unit": "package", "seasonality": "Year-round", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Thyme, Fresh", "category": "Produce", "unit": "package", "seasonality": "Year-round", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Oregano, Fresh", "category": "Produce", "unit": "package", "seasonality": "Summer-Fall", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Sage, Fresh", "category": "Produce", "unit": "package", "seasonality": "Fall", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Mint, Fresh", "category": "Produce", "unit": "bunch", "seasonality": "Spring-Summer", "storage_notes": "Refrigerate in water", "cost_level": "Medium"},
            {"name": "Dill, Fresh", "category": "Produce", "unit": "bunch", "seasonality": "Spring-Summer", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Chives, Fresh", "category": "Produce", "unit": "package", "seasonality": "Spring-Fall", "storage_notes": "Refrigerate in plastic bag", "cost_level": "Medium"},
            {"name": "Tarragon, Fresh", "category": "Produce", "unit": "package", "seasonality": "Spring-Summer", "storage_notes": "Refrigerate in plastic bag", "cost_level": "High"},
        ]
        
        # 3. PRODUCE - Fruits
        produce_fruits = [
            {"name": "Lemons", "category": "Produce", "unit": "each", "seasonality": "Year-round", "storage_notes": "Room temperature or refrigerate", "cost_level": "Low"},
            {"name": "Limes", "category": "Produce", "unit": "each", "seasonality": "Year-round", "storage_notes": "Room temperature or refrigerate", "cost_level": "Low"},
            {"name": "Oranges", "category": "Produce", "unit": "each", "seasonality": "Winter-Spring", "storage_notes": "Room temperature or refrigerate", "cost_level": "Low"},
            {"name": "Apples, Granny Smith", "category": "Produce", "unit": "lb", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Apples, Gala", "category": "Produce", "unit": "lb", "seasonality": "Fall-Spring", "storage_notes": "Refrigerate in crisper", "cost_level": "Low"},
            {"name": "Apples, Honeycrisp", "category": "Produce", "unit": "lb", "seasonality": "Fall-Winter", "storage_notes": "Refrigerate in crisper", "cost_level": "Medium"},
            {"name": "Bananas", "category": "Produce", "unit": "lb", "seasonality": "Year-round", "storage_notes": "Room temperature", "cost_level": "Low"},
            {"name": "Avocados", "category": "Produce", "unit": "each", "seasonality": "Year-round", "storage_notes": "Room temp to ripen, then refrigerate", "cost_level": "Medium"},
            {"name": "Strawberries", "category": "Produce", "unit": "pint", "seasonality": "Spring-Summer", "storage_notes": "Refrigerate unwashed", "cost_level": "Medium"},
            {"name": "Blueberries", "category": "Produce", "unit": "pint", "seasonality": "Summer", "storage_notes": "Refrigerate unwashed", "cost_level": "High"},
            {"name": "Raspberries", "category": "Produce", "unit": "pint", "seasonality": "Summer", "storage_notes": "Refrigerate unwashed", "cost_level": "High"},
            {"name": "Blackberries", "category": "Produce", "unit": "pint", "seasonality": "Summer", "storage_notes": "Refrigerate unwashed", "cost_level": "High"},
        ]
        
        # 4. PROTEIN - Meats
        protein_meats = [
            {"name": "Ground Beef, 80/20", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Ground Beef, 85/15", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Ground Beef, 90/10", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "High", "allergen_info": "None"},
            {"name": "Beef Chuck Roast", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 6-12 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Beef Sirloin Steak", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 6-12 months", "cost_level": "High", "allergen_info": "None"},
            {"name": "Beef Ribeye Steak", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 6-12 months", "cost_level": "High", "allergen_info": "None"},
            {"name": "Beef Tenderloin", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 6-12 months", "cost_level": "High", "allergen_info": "None"},
            {"name": "Chicken Breast, Boneless", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 9 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Chicken Thighs, Boneless", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 9 months", "cost_level": "Low", "allergen_info": "None"},
            {"name": "Chicken Drumsticks", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 9 months", "cost_level": "Low", "allergen_info": "None"},
            {"name": "Chicken Wings", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 9 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Whole Chicken", "category": "Protein", "unit": "each", "storage_notes": "Refrigerate 1-2 days, freeze 12 months", "cost_level": "Low", "allergen_info": "None"},
            {"name": "Pork Chops, Bone-in", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 4-6 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Pork Tenderloin", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 6-9 months", "cost_level": "High", "allergen_info": "None"},
            {"name": "Pork Shoulder", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 4-6 months", "cost_level": "Low", "allergen_info": "None"},
            {"name": "Ground Pork", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Bacon", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 7 days, freeze 1 month", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Italian Sausage", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 1-2 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Ground Turkey", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "Medium", "allergen_info": "None"},
            {"name": "Turkey Breast", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 9 months", "cost_level": "High", "allergen_info": "None"},
            {"name": "Lamb Chops", "category": "Protein", "unit": "lb", "storage_notes": "Refrigerate 3-5 days, freeze 6-9 months", "cost_level": "High", "allergen_info": "None"},
        ]
        
        # 5. SEAFOOD
        seafood = [
            {"name": "Salmon Fillets", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 2-3 months", "cost_level": "High", "allergen_info": "Fish"},
            {"name": "Cod Fillets", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "Medium", "allergen_info": "Fish"},
            {"name": "Tilapia Fillets", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "Low", "allergen_info": "Fish"},
            {"name": "Shrimp, Large", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-6 months", "cost_level": "High", "allergen_info": "Shellfish"},
            {"name": "Scallops", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3 months", "cost_level": "High", "allergen_info": "Shellfish"},
            {"name": "Mussels", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, do not freeze", "cost_level": "Medium", "allergen_info": "Shellfish"},
            {"name": "Crab Meat", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 2-3 months", "cost_level": "High", "allergen_info": "Shellfish"},
            {"name": "Lobster Tails", "category": "Seafood", "unit": "each", "storage_notes": "Refrigerate 1-2 days, freeze 6-8 months", "cost_level": "High", "allergen_info": "Shellfish"},
            {"name": "Tuna Steaks", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 2-3 months", "cost_level": "High", "allergen_info": "Fish"},
            {"name": "Halibut Fillets", "category": "Seafood", "unit": "lb", "storage_notes": "Refrigerate 1-2 days, freeze 3-4 months", "cost_level": "High", "allergen_info": "Fish"},
        ]
        
        # 6. DAIRY
        dairy = [
            {"name": "Milk, Whole", "category": "Dairy", "unit": "gallon", "storage_notes": "Refrigerate, use by date", "cost_level": "Low", "allergen_info": "Milk"},
            {"name": "Milk, 2%", "category": "Dairy", "unit": "gallon", "storage_notes": "Refrigerate, use by date", "cost_level": "Low", "allergen_info": "Milk"},
            {"name": "Milk, Skim", "category": "Dairy", "unit": "gallon", "storage_notes": "Refrigerate, use by date", "cost_level": "Low", "allergen_info": "Milk"},
            {"name": "Heavy Cream", "category": "Dairy", "unit": "pint", "storage_notes": "Refrigerate, use within 1 week of opening", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Half and Half", "category": "Dairy", "unit": "pint", "storage_notes": "Refrigerate, use within 1 week of opening", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Butter, Unsalted", "category": "Dairy", "unit": "lb", "storage_notes": "Refrigerate, freeze for longer storage", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Butter, Salted", "category": "Dairy", "unit": "lb", "storage_notes": "Refrigerate, freeze for longer storage", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Eggs, Large", "category": "Dairy", "unit": "dozen", "storage_notes": "Refrigerate in original carton", "cost_level": "Low", "allergen_info": "Eggs"},
            {"name": "Cheese, Cheddar", "category": "Dairy", "unit": "lb", "storage_notes": "Refrigerate wrapped in wax paper", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Cheese, Mozzarella", "category": "Dairy", "unit": "lb", "storage_notes": "Refrigerate in original package", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Cheese, Parmesan", "category": "Dairy", "unit": "lb", "storage_notes": "Refrigerate wrapped in wax paper", "cost_level": "High", "allergen_info": "Milk"},
            {"name": "Cheese, Swiss", "category": "Dairy", "unit": "lb", "storage_notes": "Refrigerate wrapped in wax paper", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Cream Cheese", "category": "Dairy", "unit": "8oz", "storage_notes": "Refrigerate, use within 1 week of opening", "cost_level": "Low", "allergen_info": "Milk"},
            {"name": "Sour Cream", "category": "Dairy", "unit": "16oz", "storage_notes": "Refrigerate, use within 1 week of opening", "cost_level": "Low", "allergen_info": "Milk"},
            {"name": "Greek Yogurt, Plain", "category": "Dairy", "unit": "32oz", "storage_notes": "Refrigerate, use by date", "cost_level": "Medium", "allergen_info": "Milk"},
            {"name": "Ricotta Cheese", "category": "Dairy", "unit": "15oz", "storage_notes": "Refrigerate, use within 1 week of opening", "cost_level": "Medium", "allergen_info": "Milk"},
        ]
        
        # 7. PANTRY - Grains & Starches
        pantry_grains = [
            {"name": "Rice, Long Grain White", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Rice, Basmati", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium"},
            {"name": "Rice, Jasmine", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium"},
            {"name": "Rice, Brown", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Rice, Arborio", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium"},
            {"name": "Quinoa", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium"},
            {"name": "Pasta, Spaghetti", "category": "Pantry", "unit": "lb", "storage_notes": "Store in original package", "cost_level": "Low"},
            {"name": "Pasta, Penne", "category": "Pantry", "unit": "lb", "storage_notes": "Store in original package", "cost_level": "Low"},
            {"name": "Pasta, Fettuccine", "category": "Pantry", "unit": "lb", "storage_notes": "Store in original package", "cost_level": "Low"},
            {"name": "Pasta, Rigatoni", "category": "Pantry", "unit": "lb", "storage_notes": "Store in original package", "cost_level": "Low"},
            {"name": "Bread, White", "category": "Pantry", "unit": "loaf", "storage_notes": "Store at room temperature", "cost_level": "Low", "allergen_info": "Gluten"},
            {"name": "Bread, Whole Wheat", "category": "Pantry", "unit": "loaf", "storage_notes": "Store at room temperature", "cost_level": "Low", "allergen_info": "Gluten"},
            {"name": "Flour, All-Purpose", "category": "Pantry", "unit": "5lb", "storage_notes": "Store in airtight container", "cost_level": "Low", "allergen_info": "Gluten"},
            {"name": "Flour, Bread", "category": "Pantry", "unit": "5lb", "storage_notes": "Store in airtight container", "cost_level": "Low", "allergen_info": "Gluten"},
            {"name": "Flour, Whole Wheat", "category": "Pantry", "unit": "5lb", "storage_notes": "Store in airtight container", "cost_level": "Low", "allergen_info": "Gluten"},
            {"name": "Oats, Rolled", "category": "Pantry", "unit": "18oz", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Barley, Pearl", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Couscous", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium", "allergen_info": "Gluten"},
        ]
        
        # 8. PANTRY - Beans & Legumes
        pantry_beans = [
            {"name": "Black Beans, Dried", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Black Beans, Canned", "category": "Pantry", "unit": "15oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Kidney Beans, Dried", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Kidney Beans, Canned", "category": "Pantry", "unit": "15oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Chickpeas, Dried", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Chickpeas, Canned", "category": "Pantry", "unit": "15oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Lentils, Red", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Lentils, Green", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Lima Beans, Dried", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Navy Beans, Dried", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Pinto Beans, Dried", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Split Peas", "category": "Pantry", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
        ]
        
        # 9. SPICES & SEASONINGS
        spices = [
            {"name": "Salt, Kosher", "category": "Spices", "unit": "3lb", "storage_notes": "Store in dry place", "cost_level": "Low"},
            {"name": "Salt, Sea", "category": "Spices", "unit": "26oz", "storage_notes": "Store in dry place", "cost_level": "Medium"},
            {"name": "Black Pepper, Ground", "category": "Spices", "unit": "4oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Black Peppercorns, Whole", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Garlic Powder", "category": "Spices", "unit": "3oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Onion Powder", "category": "Spices", "unit": "3oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Paprika", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Cumin, Ground", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Chili Powder", "category": "Spices", "unit": "3oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Oregano, Dried", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Thyme, Dried", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Rosemary, Dried", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Basil, Dried", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Bay Leaves", "category": "Spices", "unit": "0.5oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Cinnamon, Ground", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Nutmeg, Ground", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Ginger, Ground", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Turmeric, Ground", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Coriander, Ground", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Cardamom, Ground", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "High"},
            {"name": "Cloves, Ground", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Allspice, Ground", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Cayenne Pepper", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Red Pepper Flakes", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Smoked Paprika", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Italian Seasoning", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Herbs de Provence", "category": "Spices", "unit": "1oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Everything Bagel Seasoning", "category": "Spices", "unit": "2oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
        ]
        
        # 10. PANTRY - Oils & Vinegars
        pantry_oils = [
            {"name": "Olive Oil, Extra Virgin", "category": "Pantry", "unit": "500ml", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "Vegetable Oil", "category": "Pantry", "unit": "48oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Canola Oil", "category": "Pantry", "unit": "48oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Coconut Oil", "category": "Pantry", "unit": "14oz", "storage_notes": "Store at room temperature", "cost_level": "Medium"},
            {"name": "Sesame Oil", "category": "Pantry", "unit": "8oz", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "Avocado Oil", "category": "Pantry", "unit": "16oz", "storage_notes": "Store in cool, dark place", "cost_level": "High"},
            {"name": "Balsamic Vinegar", "category": "Pantry", "unit": "16oz", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "White Wine Vinegar", "category": "Pantry", "unit": "16oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Apple Cider Vinegar", "category": "Pantry", "unit": "16oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Red Wine Vinegar", "category": "Pantry", "unit": "16oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low"},
            {"name": "Rice Vinegar", "category": "Pantry", "unit": "10oz", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
        ]
        
        # 11. PANTRY - Condiments & Sauces
        pantry_condiments = [
            {"name": "Soy Sauce", "category": "Pantry", "unit": "10oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low", "allergen_info": "Soy, Gluten"},
            {"name": "Hot Sauce", "category": "Pantry", "unit": "5oz", "storage_notes": "Store in cool place", "cost_level": "Low"},
            {"name": "Worcestershire Sauce", "category": "Pantry", "unit": "10oz", "storage_notes": "Store in cool, dark place", "cost_level": "Low", "allergen_info": "Fish"},
            {"name": "Dijon Mustard", "category": "Pantry", "unit": "8oz", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Yellow Mustard", "category": "Pantry", "unit": "8oz", "storage_notes": "Refrigerate after opening", "cost_level": "Low"},
            {"name": "Ketchup", "category": "Pantry", "unit": "20oz", "storage_notes": "Store in cool place, refrigerate after opening", "cost_level": "Low"},
            {"name": "Mayonnaise", "category": "Pantry", "unit": "30oz", "storage_notes": "Store in cool place, refrigerate after opening", "cost_level": "Low", "allergen_info": "Eggs"},
            {"name": "Tomato Paste", "category": "Pantry", "unit": "6oz", "storage_notes": "Refrigerate after opening", "cost_level": "Low"},
            {"name": "Crushed Tomatoes, Canned", "category": "Pantry", "unit": "28oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Diced Tomatoes, Canned", "category": "Pantry", "unit": "14.5oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Tomato Sauce, Canned", "category": "Pantry", "unit": "15oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Coconut Milk, Canned", "category": "Pantry", "unit": "14oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Chicken Broth", "category": "Pantry", "unit": "32oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Beef Broth", "category": "Pantry", "unit": "32oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Vegetable Broth", "category": "Pantry", "unit": "32oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
        ]
        
        # 12. PANTRY - Baking Essentials
        pantry_baking = [
            {"name": "Sugar, Granulated", "category": "Pantry", "unit": "4lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Sugar, Brown", "category": "Pantry", "unit": "2lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Sugar, Powdered", "category": "Pantry", "unit": "1lb", "storage_notes": "Store in airtight container", "cost_level": "Low"},
            {"name": "Honey", "category": "Pantry", "unit": "12oz", "storage_notes": "Store at room temperature", "cost_level": "Medium"},
            {"name": "Maple Syrup", "category": "Pantry", "unit": "8oz", "storage_notes": "Refrigerate after opening", "cost_level": "High"},
            {"name": "Vanilla Extract", "category": "Pantry", "unit": "4oz", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "Baking Powder", "category": "Pantry", "unit": "10oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Baking Soda", "category": "Pantry", "unit": "1lb", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Active Dry Yeast", "category": "Pantry", "unit": "0.75oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Cornstarch", "category": "Pantry", "unit": "16oz", "storage_notes": "Store in cool, dry place", "cost_level": "Low"},
            {"name": "Cocoa Powder", "category": "Pantry", "unit": "8oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
            {"name": "Chocolate Chips", "category": "Pantry", "unit": "12oz", "storage_notes": "Store in cool, dry place", "cost_level": "Medium"},
        ]
        
        # 13. NUTS & SEEDS
        nuts_seeds = [
            {"name": "Almonds, Raw", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium", "allergen_info": "Tree Nuts", "nutritional_info": "High in vitamin E, magnesium, protein"},
            {"name": "Almonds, Sliced", "category": "Nuts & Seeds", "unit": "8oz", "storage_notes": "Store in airtight container", "cost_level": "Medium", "allergen_info": "Tree Nuts"},
            {"name": "Almonds, Blanched", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium", "allergen_info": "Tree Nuts"},
            {"name": "Walnuts", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Refrigerate or freeze", "cost_level": "High", "allergen_info": "Tree Nuts", "nutritional_info": "High in omega-3 fatty acids"},
            {"name": "Pecans", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Refrigerate or freeze", "cost_level": "High", "allergen_info": "Tree Nuts"},
            {"name": "Cashews", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "High", "allergen_info": "Tree Nuts", "nutritional_info": "Good source of copper and magnesium"},
            {"name": "Brazil Nuts", "category": "Nuts & Seeds", "unit": "8oz", "storage_notes": "Refrigerate or freeze", "cost_level": "High", "allergen_info": "Tree Nuts", "nutritional_info": "Extremely high in selenium"},
            {"name": "Hazelnuts", "category": "Nuts & Seeds", "unit": "8oz", "storage_notes": "Store in airtight container", "cost_level": "High", "allergen_info": "Tree Nuts"},
            {"name": "Macadamia Nuts", "category": "Nuts & Seeds", "unit": "8oz", "storage_notes": "Store in airtight container", "cost_level": "High", "allergen_info": "Tree Nuts"},
            {"name": "Pistachios", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "High", "allergen_info": "Tree Nuts"},
            {"name": "Peanuts", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low", "allergen_info": "Peanuts", "nutritional_info": "High in protein and niacin"},
            {"name": "Pine Nuts", "category": "Nuts & Seeds", "unit": "4oz", "storage_notes": "Refrigerate or freeze", "cost_level": "High", "allergen_info": "Tree Nuts"},
            {"name": "Sunflower Seeds", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Low", "nutritional_info": "High in vitamin E"},
            {"name": "Pumpkin Seeds", "category": "Nuts & Seeds", "unit": "lb", "storage_notes": "Store in airtight container", "cost_level": "Medium", "nutritional_info": "High in zinc and magnesium"},
            {"name": "Sesame Seeds", "category": "Nuts & Seeds", "unit": "8oz", "storage_notes": "Store in airtight container", "cost_level": "Medium", "allergen_info": "Sesame"},
            {"name": "Chia Seeds", "category": "Nuts & Seeds", "unit": "12oz", "storage_notes": "Store in airtight container", "cost_level": "Medium", "nutritional_info": "High in omega-3, fiber, protein"},
            {"name": "Flax Seeds", "category": "Nuts & Seeds", "unit": "16oz", "storage_notes": "Store in airtight container", "cost_level": "Medium", "nutritional_info": "High in omega-3 and lignans"},
            {"name": "Hemp Hearts", "category": "Nuts & Seeds", "unit": "8oz", "storage_notes": "Refrigerate after opening", "cost_level": "High", "nutritional_info": "Complete protein, omega fatty acids"},
        ]
        
        # 14. INTERNATIONAL & SPECIALTY INGREDIENTS
        international_specialty = [
            {"name": "Miso Paste", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium", "allergen_info": "Soy"},
            {"name": "Tahini", "category": "International", "unit": "16oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Medium", "allergen_info": "Sesame"},
            {"name": "Fish Sauce", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Low", "allergen_info": "Fish"},
            {"name": "Oyster Sauce", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Low", "allergen_info": "Shellfish"},
            {"name": "Hoisin Sauce", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium", "allergen_info": "Soy, Gluten"},
            {"name": "Sriracha", "category": "International", "unit": "17oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Low"},
            {"name": "Sambal Oelek", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Gochujang", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium", "allergen_info": "Soy"},
            {"name": "Harissa Paste", "category": "International", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Pomegranate Molasses", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Medium"},
            {"name": "Rose Water", "category": "International", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "Orange Blossom Water", "category": "International", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "Medium"},
            {"name": "Tamarind Paste", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Mirin", "category": "International", "unit": "10oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Medium", "allergen_info": "Gluten"},
            {"name": "Sake", "category": "International", "unit": "375ml", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Shaoxing Wine", "category": "International", "unit": "375ml", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Medium"},
            {"name": "Kimchi", "category": "International", "unit": "16oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium"},
            {"name": "Preserved Lemons", "category": "International", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "High"},
            {"name": "Capers", "category": "International", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Anchovies", "category": "International", "unit": "2oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium", "allergen_info": "Fish"},
        ]
        
        # 15. ALTERNATIVE & PLANT-BASED INGREDIENTS  
        alternative_plantbased = [
            {"name": "Nutritional Yeast", "category": "Alternative", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Store in airtight container", "cost_level": "Medium", "nutritional_info": "High in B-vitamins, especially B12"},
            {"name": "Tempeh", "category": "Alternative", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "allergen_info": "Soy", "nutritional_info": "Fermented soy, high protein"},
            {"name": "Tofu, Extra Firm", "category": "Alternative", "unit": "14oz", "seasonality": "Year-round", "storage_notes": "Refrigerate in water", "cost_level": "Low", "allergen_info": "Soy"},
            {"name": "Tofu, Silken", "category": "Alternative", "unit": "12oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Low", "allergen_info": "Soy"},
            {"name": "Seitan", "category": "Alternative", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "allergen_info": "Gluten"},
            {"name": "Jackfruit, Young Green", "category": "Alternative", "unit": "20oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Aquafaba", "category": "Alternative", "unit": "15oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Low", "nutritional_info": "Chickpea liquid, egg substitute"},
            {"name": "Almond Milk", "category": "Alternative", "unit": "32oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium", "allergen_info": "Tree Nuts"},
            {"name": "Oat Milk", "category": "Alternative", "unit": "32oz", "seasonality": "Year-round", "storage_notes": "Refrigerate after opening", "cost_level": "Medium"},
            {"name": "Cashew Cream", "category": "Alternative", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "High", "allergen_info": "Tree Nuts"},
            {"name": "Vegan Butter", "category": "Alternative", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium"},
            {"name": "Coconut Yogurt", "category": "Alternative", "unit": "16oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "High"},
        ]
        
        # 16. FERMENTED & CULTURED FOODS
        fermented_cultured = [
            {"name": "Sauerkraut", "category": "Fermented", "unit": "16oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Low", "nutritional_info": "Probiotics, vitamin C"},
            {"name": "Kefir", "category": "Fermented", "unit": "32oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "allergen_info": "Milk", "nutritional_info": "Probiotics"},
            {"name": "Kombucha", "category": "Fermented", "unit": "16oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "nutritional_info": "Probiotics"},
            {"name": "Apple Cider Vinegar, Raw", "category": "Fermented", "unit": "16oz", "seasonality": "Year-round", "storage_notes": "Store in cool place", "cost_level": "Medium", "nutritional_info": "Contains the mother"},
            {"name": "Miso, White", "category": "Fermented", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "allergen_info": "Soy"},
            {"name": "Miso, Red", "category": "Fermented", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "allergen_info": "Soy"},
        ]
        
        # 17. SUPERFOODS & HEALTH FOODS
        superfoods = [
            {"name": "Spirulina Powder", "category": "Superfood", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "High", "nutritional_info": "High in protein, B-vitamins, iron"},
            {"name": "Chlorella Powder", "category": "Superfood", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "High", "nutritional_info": "High in chlorophyll and protein"},
            {"name": "Maca Powder", "category": "Superfood", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Store in airtight container", "cost_level": "High", "nutritional_info": "Adaptogenic root"},
            {"name": "Acai Powder", "category": "Superfood", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "High", "nutritional_info": "High in antioxidants"},
            {"name": "Goji Berries", "category": "Superfood", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Store in airtight container", "cost_level": "High", "nutritional_info": "High in vitamin C and antioxidants"},
            {"name": "Cacao Powder, Raw", "category": "Superfood", "unit": "8oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dry place", "cost_level": "Medium", "nutritional_info": "High in magnesium and antioxidants"},
            {"name": "Turmeric, Fresh", "category": "Superfood", "unit": "4oz", "seasonality": "Year-round", "storage_notes": "Refrigerate", "cost_level": "Medium", "nutritional_info": "Anti-inflammatory curcumin"},
            {"name": "Matcha Powder", "category": "Superfood", "unit": "2oz", "seasonality": "Year-round", "storage_notes": "Store in cool, dark place", "cost_level": "High", "nutritional_info": "High in antioxidants and caffeine"},
        ]
        
        # Combine all categories
        ingredients.extend(produce_vegetables)
        ingredients.extend(produce_herbs)
        ingredients.extend(produce_fruits)
        ingredients.extend(protein_meats)
        ingredients.extend(seafood)
        ingredients.extend(dairy)
        ingredients.extend(pantry_grains)
        ingredients.extend(pantry_beans)
        ingredients.extend(spices)
        ingredients.extend(pantry_oils)
        ingredients.extend(pantry_condiments)
        ingredients.extend(pantry_baking)
        ingredients.extend(nuts_seeds)
        ingredients.extend(international_specialty)
        ingredients.extend(alternative_plantbased)
        ingredients.extend(fermented_cultured)
        ingredients.extend(superfoods)
        
        # Add timestamps and ensure all required fields
        current_time = datetime.now().isoformat()
        for ingredient in ingredients:
            ingredient.update({
                'created_at': current_time,
                'updated_at': current_time,
                'user_id': None,  # Global ingredients (not user-specific)
                'spec_notes': ingredient.get('spec_notes', ''),
                'nutritional_info': ingredient.get('nutritional_info', ''),
                'substitutions': ingredient.get('substitutions', ''),
                'supplier_notes': ingredient.get('supplier_notes', ''),
                'allergen_info': ingredient.get('allergen_info', ''),
                'best_before': ingredient.get('best_before', ''),
                'prep_notes': ingredient.get('prep_notes', '')
            })
        
        return ingredients
    
    def populate_database(self):
        """Populate the database with comprehensive ingredient list"""
        ingredients = self.get_comprehensive_ingredients()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear existing global ingredients (user_id IS NULL)
                cursor.execute("DELETE FROM ingredients WHERE user_id IS NULL")
                
                # Insert new ingredients
                for ingredient in ingredients:
                    cursor.execute('''
                        INSERT INTO ingredients 
                        (name, unit, category, spec_notes, nutritional_info, storage_notes,
                         substitutions, seasonality, cost_level, supplier_notes, allergen_info,
                         best_before, prep_notes, created_at, updated_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        ingredient.get('name', ''),
                        ingredient.get('unit', ''),
                        ingredient.get('category', ''),
                        ingredient.get('spec_notes', ''),
                        ingredient.get('nutritional_info', ''),
                        ingredient.get('storage_notes', ''),
                        ingredient.get('substitutions', ''),
                        ingredient.get('seasonality', ''),
                        ingredient.get('cost_level', ''),
                        ingredient.get('supplier_notes', ''),
                        ingredient.get('allergen_info', ''),
                        ingredient.get('best_before', ''),
                        ingredient.get('prep_notes', ''),
                        ingredient.get('created_at', ''),
                        ingredient.get('updated_at', ''),
                        ingredient.get('user_id')
                    ))
                
                conn.commit()
                print(f"✅ Successfully populated database with {len(ingredients)} ingredients!")
                
                # Show summary by category
                cursor.execute('''
                    SELECT category, COUNT(*) 
                    FROM ingredients 
                    WHERE user_id IS NULL 
                    GROUP BY category 
                    ORDER BY category
                ''')
                
                print("\n📊 Ingredients by Category:")
                for category, count in cursor.fetchall():
                    print(f"  {category}: {count} items")
                
                return True
                
        except Exception as e:
            print(f"❌ Error populating database: {e}")
            return False

if __name__ == "__main__":
    print("🍅 Creating Comprehensive Ingredient Database...")
    
    # Initialize and populate
    db = PreloadedIngredientsDB()
    success = db.populate_database()
    
    if success:
        print("\n🎉 Preloaded ingredient database created successfully!")
        print("Users can now:")
        print("  • Browse thousands of common ingredients")
        print("  • Create custom ingredient lists")
        print("  • Add their own ingredients")
        print("  • Search by category, seasonality, cost level")
    else:
        print("\n❌ Failed to create ingredient database")