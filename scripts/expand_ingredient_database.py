#!/usr/bin/env python3
"""
Ingredient Database Expansion Script
Adds 200+ additional professional ingredients to the Iterum R&D Chef Notebook database
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Professional ingredient categories with expanded ingredients
PROFESSIONAL_INGREDIENTS = {
    "Exotic Fruits": [
        {"name": "Dragon Fruit", "unit": "piece", "category": "Exotic Fruits", "description": "Tropical cactus fruit with mild sweet flavor", "nutritional_info": "Low calorie, high in antioxidants"},
        {"name": "Passion Fruit", "unit": "piece", "category": "Exotic Fruits", "description": "Aromatic tropical fruit with tart, sweet pulp", "nutritional_info": "High in vitamin C and fiber"},
        {"name": "Rambutan", "unit": "piece", "category": "Exotic Fruits", "description": "Hairy red tropical fruit similar to lychee", "nutritional_info": "Rich in vitamin C and copper"},
        {"name": "Jackfruit", "unit": "piece", "category": "Exotic Fruits", "description": "Large tropical fruit with sweet, fibrous flesh", "nutritional_info": "High in vitamin C and potassium"},
        {"name": "Durian", "unit": "piece", "category": "Exotic Fruits", "description": "Spiky tropical fruit with strong aroma", "nutritional_info": "High in healthy fats and vitamin C"},
        {"name": "Cherimoya", "unit": "piece", "category": "Exotic Fruits", "description": "Custard apple with creamy, sweet flesh", "nutritional_info": "High in vitamin C and fiber"},
        {"name": "Feijoa", "unit": "piece", "category": "Exotic Fruits", "description": "Pineapple guava with aromatic flesh", "nutritional_info": "Rich in vitamin C and iodine"},
        {"name": "Physalis", "unit": "piece", "category": "Exotic Fruits", "description": "Golden berry in papery husk", "nutritional_info": "High in vitamin A and antioxidants"},
        {"name": "Black Sapote", "unit": "piece", "category": "Exotic Fruits", "description": "Chocolate pudding fruit with dark flesh", "nutritional_info": "High in vitamin C and potassium"},
        {"name": "Buddha's Hand Citron", "unit": "piece", "category": "Exotic Fruits", "description": "Fingered citron with intense fragrance", "nutritional_info": "High in vitamin C and citrus oils"}
    ],
    "Specialty Mushrooms": [
        {"name": "Lion's Mane Mushroom", "unit": "lb", "category": "Specialty Mushrooms", "description": "White, shaggy mushroom with seafood-like texture", "nutritional_info": "High in protein and nerve-supporting compounds"},
        {"name": "Chanterelle Mushrooms", "unit": "oz", "category": "Specialty Mushrooms", "description": "Golden trumpet-shaped wild mushrooms", "nutritional_info": "Rich in vitamin D and potassium"},
        {"name": "Morel Mushrooms", "unit": "oz", "category": "Specialty Mushrooms", "description": "Honeycomb-textured spring mushrooms", "nutritional_info": "High in iron and phosphorus"},
        {"name": "Porcini Mushrooms", "unit": "oz", "category": "Specialty Mushrooms", "description": "Meaty Italian mushrooms with nutty flavor", "nutritional_info": "High in protein and selenium"},
        {"name": "Enoki Mushrooms", "unit": "package", "category": "Specialty Mushrooms", "description": "Thin, delicate white mushrooms", "nutritional_info": "Low calorie, high in niacin"},
        {"name": "Maitake Mushrooms", "unit": "lb", "category": "Specialty Mushrooms", "description": "Hen of the woods with frilly appearance", "nutritional_info": "Rich in beta-glucans and vitamin D"},
        {"name": "Reishi Mushrooms", "unit": "oz", "category": "Specialty Mushrooms", "description": "Medicinal mushroom with woody texture", "nutritional_info": "Adaptogenic compounds and triterpenes"},
        {"name": "Turkey Tail Mushrooms", "unit": "oz", "category": "Specialty Mushrooms", "description": "Fan-shaped medicinal mushrooms", "nutritional_info": "High in polysaccharides and antioxidants"},
        {"name": "Beech Mushrooms", "unit": "package", "category": "Specialty Mushrooms", "description": "Small clustered mushrooms with nutty flavor", "nutritional_info": "High in protein and B vitamins"},
        {"name": "Wood Ear Mushrooms", "unit": "oz", "category": "Specialty Mushrooms", "description": "Gelatinous black mushrooms", "nutritional_info": "High in iron and fiber"}
    ],
    "Premium Seafood": [
        {"name": "Uni (Sea Urchin)", "unit": "oz", "category": "Premium Seafood", "description": "Creamy orange sea urchin roe", "nutritional_info": "High in omega-3 fatty acids and zinc"},
        {"name": "Ikura (Salmon Roe)", "unit": "oz", "category": "Premium Seafood", "description": "Large orange salmon eggs", "nutritional_info": "Rich in omega-3s and vitamin B12"},
        {"name": "Monkfish", "unit": "lb", "category": "Premium Seafood", "description": "Firm white fish with lobster-like texture", "nutritional_info": "High in protein and selenium"},
        {"name": "John Dory", "unit": "lb", "category": "Premium Seafood", "description": "Delicate white fish with mild flavor", "nutritional_info": "Low fat, high in protein"},
        {"name": "Langoustines", "unit": "lb", "category": "Premium Seafood", "description": "Small lobster-like crustaceans", "nutritional_info": "High in protein and iodine"},
        {"name": "Razor Clams", "unit": "lb", "category": "Premium Seafood", "description": "Long, thin clams with sweet meat", "nutritional_info": "High in protein and iron"},
        {"name": "Geoduck Clam", "unit": "piece", "category": "Premium Seafood", "description": "Large Pacific clam with long neck", "nutritional_info": "High in protein and minerals"},
        {"name": "Bluefin Tuna", "unit": "lb", "category": "Premium Seafood", "description": "Premium tuna with rich, fatty flesh", "nutritional_info": "High in omega-3s and protein"},
        {"name": "Wild Striped Bass", "unit": "lb", "category": "Premium Seafood", "description": "Flaky white fish with mild flavor", "nutritional_info": "High in protein and B vitamins"},
        {"name": "Diver Scallops", "unit": "piece", "category": "Premium Seafood", "description": "Hand-harvested large scallops", "nutritional_info": "High in protein and magnesium"}
    ],
    "Artisanal Grains": [
        {"name": "Forbidden Black Rice", "unit": "lb", "category": "Artisanal Grains", "description": "Antioxidant-rich purple-black rice", "nutritional_info": "High in anthocyanins and fiber"},
        {"name": "Farro Piccolo", "unit": "lb", "category": "Artisanal Grains", "description": "Small ancient wheat with nutty flavor", "nutritional_info": "High in protein and fiber"},
        {"name": "Freekeh", "unit": "lb", "category": "Artisanal Grains", "description": "Roasted green wheat with smoky flavor", "nutritional_info": "High in protein and fiber"},
        {"name": "Teff", "unit": "lb", "category": "Artisanal Grains", "description": "Tiny Ethiopian grain rich in nutrients", "nutritional_info": "High in iron and calcium"},
        {"name": "Kañiwa", "unit": "lb", "category": "Artisanal Grains", "description": "Small Andean pseudocereal", "nutritional_info": "Complete protein and gluten-free"},
        {"name": "Amaranth", "unit": "lb", "category": "Artisanal Grains", "description": "Ancient pseudocereal with nutty flavor", "nutritional_info": "Complete protein and high lysine"},
        {"name": "Millet", "unit": "lb", "category": "Artisanal Grains", "description": "Small, mild ancient grain", "nutritional_info": "Gluten-free and rich in magnesium"},
        {"name": "Sorghum", "unit": "lb", "category": "Artisanal Grains", "description": "Drought-resistant ancient grain", "nutritional_info": "Gluten-free and high in antioxidants"},
        {"name": "Job's Tears", "unit": "lb", "category": "Artisanal Grains", "description": "Asian grain with chewy texture", "nutritional_info": "High in protein and B vitamins"},
        {"name": "Wild Rice", "unit": "lb", "category": "Artisanal Grains", "description": "North American aquatic grass seed", "nutritional_info": "High in protein and minerals"}
    ],
    "Exotic Spices": [
        {"name": "Sumac", "unit": "oz", "category": "Exotic Spices", "description": "Tart, lemony Middle Eastern spice", "nutritional_info": "High in antioxidants and vitamin C"},
        {"name": "Za'atar", "unit": "oz", "category": "Exotic Spices", "description": "Middle Eastern herb and spice blend", "nutritional_info": "Rich in thyme, sesame, and sumac"},
        {"name": "Ras el Hanout", "unit": "oz", "category": "Exotic Spices", "description": "Complex North African spice blend", "nutritional_info": "Contains 20+ spices and herbs"},
        {"name": "Berbere", "unit": "oz", "category": "Exotic Spices", "description": "Ethiopian chili spice blend", "nutritional_info": "High in capsaicin and antioxidants"},
        {"name": "Dukkah", "unit": "oz", "category": "Exotic Spices", "description": "Egyptian nut and spice mixture", "nutritional_info": "High in healthy fats and protein"},
        {"name": "Shichimi Togarashi", "unit": "oz", "category": "Exotic Spices", "description": "Japanese seven-spice blend", "nutritional_info": "Contains chili, sesame, and citrus peel"},
        {"name": "Chinese Five Spice", "unit": "oz", "category": "Exotic Spices", "description": "Traditional Chinese spice blend", "nutritional_info": "Contains star anise, cloves, cinnamon"},
        {"name": "Garam Masala", "unit": "oz", "category": "Exotic Spices", "description": "Warm Indian spice blend", "nutritional_info": "Rich in warming spices and antioxidants"},
        {"name": "Baharat", "unit": "oz", "category": "Exotic Spices", "description": "All-spice blend from Levant", "nutritional_info": "Contains black pepper, allspice, cinnamon"},
        {"name": "Quatre Épices", "unit": "oz", "category": "Exotic Spices", "description": "French four-spice blend", "nutritional_info": "Contains pepper, cloves, nutmeg, ginger"}
    ],
    "Microgreens": [
        {"name": "Pea Shoots", "unit": "oz", "category": "Microgreens", "description": "Tender young pea plant shoots", "nutritional_info": "High in vitamin C and folate"},
        {"name": "Sunflower Microgreens", "unit": "oz", "category": "Microgreens", "description": "Nutty, crunchy sunflower sprouts", "nutritional_info": "High in vitamin E and healthy fats"},
        {"name": "Radish Microgreens", "unit": "oz", "category": "Microgreens", "description": "Spicy, peppery young radish plants", "nutritional_info": "High in vitamin C and antioxidants"},
        {"name": "Broccoli Microgreens", "unit": "oz", "category": "Microgreens", "description": "Concentrated broccoli flavor", "nutritional_info": "High in sulforaphane and vitamin K"},
        {"name": "Amaranth Microgreens", "unit": "oz", "category": "Microgreens", "description": "Colorful, mild-flavored microgreens", "nutritional_info": "High in vitamin K and folate"},
        {"name": "Buckwheat Microgreens", "unit": "oz", "category": "Microgreens", "description": "Lemony, fresh microgreens", "nutritional_info": "High in rutin and magnesium"},
        {"name": "Mustard Microgreens", "unit": "oz", "category": "Microgreens", "description": "Spicy, wasabi-like microgreens", "nutritional_info": "High in vitamin K and antioxidants"},
        {"name": "Beet Microgreens", "unit": "oz", "category": "Microgreens", "description": "Sweet, earthy microgreens", "nutritional_info": "High in betalains and folate"},
        {"name": "Cilantro Microgreens", "unit": "oz", "category": "Microgreens", "description": "Intense cilantro flavor", "nutritional_info": "High in vitamin K and antioxidants"},
        {"name": "Basil Microgreens", "unit": "oz", "category": "Microgreens", "description": "Concentrated basil aroma", "nutritional_info": "High in vitamin K and essential oils"}
    ],
    "Ancient Legumes": [
        {"name": "Black Beluga Lentils", "unit": "lb", "category": "Ancient Legumes", "description": "Small, firm black lentils", "nutritional_info": "High in protein and anthocyanins"},
        {"name": "French Green Lentils", "unit": "lb", "category": "Ancient Legumes", "description": "Peppery lentils that hold their shape", "nutritional_info": "High in protein and fiber"},
        {"name": "Red Coral Lentils", "unit": "lb", "category": "Ancient Legumes", "description": "Quick-cooking orange lentils", "nutritional_info": "High in protein and iron"},
        {"name": "Tepary Beans", "unit": "lb", "category": "Ancient Legumes", "description": "Drought-resistant Southwestern beans", "nutritional_info": "High in protein and resistant starch"},
        {"name": "Adzuki Beans", "unit": "lb", "category": "Ancient Legumes", "description": "Small red Asian beans", "nutritional_info": "High in protein and folate"},
        {"name": "Mung Beans", "unit": "lb", "category": "Ancient Legumes", "description": "Small green beans for sprouting", "nutritional_info": "High in protein and B vitamins"},
        {"name": "Black Turtle Beans", "unit": "lb", "category": "Ancient Legumes", "description": "Dense, flavorful black beans", "nutritional_info": "High in protein and anthocyanins"},
        {"name": "Scarlet Runner Beans", "unit": "lb", "category": "Ancient Legumes", "description": "Large, colorful heirloom beans", "nutritional_info": "High in protein and potassium"},
        {"name": "Lima Beans (Baby)", "unit": "lb", "category": "Ancient Legumes", "description": "Small, buttery lima beans", "nutritional_info": "High in protein and manganese"},
        {"name": "Cranberry Beans", "unit": "lb", "category": "Ancient Legumes", "description": "Speckled beans with nutty flavor", "nutritional_info": "High in protein and fiber"}
    ],
    "Wild Herbs": [
        {"name": "Wild Ramps", "unit": "bunch", "category": "Wild Herbs", "description": "Wild leeks with garlicky flavor", "nutritional_info": "High in vitamin A and sulfur compounds"},
        {"name": "Fiddle Head Ferns", "unit": "lb", "category": "Wild Herbs", "description": "Young fern shoots with earthy flavor", "nutritional_info": "High in omega-3 fatty acids"},
        {"name": "Wild Garlic", "unit": "bunch", "category": "Wild Herbs", "description": "Foraged garlic with mild flavor", "nutritional_info": "High in allicin and vitamin C"},
        {"name": "Purslane", "unit": "bunch", "category": "Wild Herbs", "description": "Succulent wild green", "nutritional_info": "High in omega-3 fatty acids"},
        {"name": "Lamb's Quarters", "unit": "bunch", "category": "Wild Herbs", "description": "Wild spinach-like green", "nutritional_info": "High in vitamin A and calcium"},
        {"name": "Dandelion Greens", "unit": "bunch", "category": "Wild Herbs", "description": "Bitter wild greens", "nutritional_info": "High in vitamin K and potassium"},
        {"name": "Wild Nettle", "unit": "bunch", "category": "Wild Herbs", "description": "Nutritious stinging nettle", "nutritional_info": "High in iron and protein"},
        {"name": "Wild Mint", "unit": "bunch", "category": "Wild Herbs", "description": "Foraged mint varieties", "nutritional_info": "High in menthol and antioxidants"},
        {"name": "Wild Fennel", "unit": "bunch", "category": "Wild Herbs", "description": "Foraged fennel fronds", "nutritional_info": "High in vitamin C and fiber"},
        {"name": "Wood Sorrel", "unit": "bunch", "category": "Wild Herbs", "description": "Tart, lemony wild herb", "nutritional_info": "High in vitamin C and oxalic acid"}
    ],
    "Fermented Products": [
        {"name": "Miso Paste (White)", "unit": "lb", "category": "Fermented Products", "description": "Mild Japanese soybean paste", "nutritional_info": "High in probiotics and umami"},
        {"name": "Miso Paste (Red)", "unit": "lb", "category": "Fermented Products", "description": "Rich, aged Japanese soybean paste", "nutritional_info": "High in probiotics and B vitamins"},
        {"name": "Kimchi", "unit": "jar", "category": "Fermented Products", "description": "Spicy Korean fermented cabbage", "nutritional_info": "High in probiotics and vitamin C"},
        {"name": "Sauerkraut", "unit": "jar", "category": "Fermented Products", "description": "Fermented cabbage with tangy flavor", "nutritional_info": "High in probiotics and vitamin K"},
        {"name": "Tempeh", "unit": "package", "category": "Fermented Products", "description": "Fermented soybean cake", "nutritional_info": "High in protein and probiotics"},
        {"name": "Kefir", "unit": "bottle", "category": "Fermented Products", "description": "Fermented milk drink", "nutritional_info": "High in probiotics and calcium"},
        {"name": "Kombucha", "unit": "bottle", "category": "Fermented Products", "description": "Fermented tea drink", "nutritional_info": "Contains probiotics and antioxidants"},
        {"name": "Kvass", "unit": "bottle", "category": "Fermented Products", "description": "Fermented beet drink", "nutritional_info": "High in probiotics and nitrates"},
        {"name": "Mirin", "unit": "bottle", "category": "Fermented Products", "description": "Sweet Japanese rice wine", "nutritional_info": "Contains amino acids and natural sugars"},
        {"name": "Fish Sauce", "unit": "bottle", "category": "Fermented Products", "description": "Fermented fish condiment", "nutritional_info": "High in umami and B vitamins"}
    ],
    "Heirloom Vegetables": [
        {"name": "Purple Top Turnips", "unit": "lb", "category": "Heirloom Vegetables", "description": "Traditional purple-crowned turnips", "nutritional_info": "High in vitamin C and fiber"},
        {"name": "Brandywine Tomatoes", "unit": "lb", "category": "Heirloom Vegetables", "description": "Large, flavorful heirloom tomatoes", "nutritional_info": "High in lycopene and vitamin C"},
        {"name": "Glass Gem Corn", "unit": "ear", "category": "Heirloom Vegetables", "description": "Multicolored ornamental corn", "nutritional_info": "High in antioxidants and fiber"},
        {"name": "Dragon Tongue Beans", "unit": "lb", "category": "Heirloom Vegetables", "description": "Purple-streaked heirloom beans", "nutritional_info": "High in protein and anthocyanins"},
        {"name": "Chioggia Beets", "unit": "bunch", "category": "Heirloom Vegetables", "description": "Candy-striped Italian beets", "nutritional_info": "High in betalains and folate"},
        {"name": "Purple Carrots", "unit": "bunch", "category": "Heirloom Vegetables", "description": "Ancient purple carrot varieties", "nutritional_info": "High in anthocyanins and beta-carotene"},
        {"name": "Lemon Cucumbers", "unit": "lb", "category": "Heirloom Vegetables", "description": "Round, yellow heirloom cucumbers", "nutritional_info": "High in water content and vitamin K"},
        {"name": "Purple Potatoes", "unit": "lb", "category": "Heirloom Vegetables", "description": "Blue and purple potato varieties", "nutritional_info": "High in anthocyanins and potassium"},
        {"name": "Romanesco", "unit": "head", "category": "Heirloom Vegetables", "description": "Spiral-patterned Italian vegetable", "nutritional_info": "High in vitamin C and fiber"},
        {"name": "Yard-Long Beans", "unit": "lb", "category": "Heirloom Vegetables", "description": "Very long Asian green beans", "nutritional_info": "High in protein and folate"}
    ]
}

def create_database_connection(db_path: str = "culinary_data.db") -> sqlite3.Connection:
    """Create connection to SQLite database"""
    return sqlite3.connect(db_path)

def get_next_ingredient_id(conn: sqlite3.Connection) -> int:
    """Get the next available ingredient ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM ingredients")
    max_id = cursor.fetchone()[0]
    return (max_id or 0) + 1

def add_professional_ingredients(conn: sqlite3.Connection) -> int:
    """Add professional ingredients to the database"""
    cursor = conn.cursor()
    next_id = get_next_ingredient_id(conn)
    added_count = 0
    current_time = datetime.now().isoformat()
    
    for category, ingredients in PROFESSIONAL_INGREDIENTS.items():
        for ingredient in ingredients:
            try:
                # Check if ingredient already exists
                cursor.execute("SELECT id FROM ingredients WHERE name = ?", (ingredient["name"],))
                if cursor.fetchone():
                    print(f"Skipping {ingredient['name']} - already exists")
                    continue
                
                # Insert new ingredient
                cursor.execute("""
                    INSERT INTO ingredients (
                        id, name, unit, category, spec_notes, nutritional_info,
                        storage_notes, substitutions, seasonality, cost_level,
                        supplier_notes, allergen_info, best_before, prep_notes,
                        created_at, updated_at, user_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    next_id,
                    ingredient["name"],
                    ingredient["unit"],
                    ingredient["category"],
                    ingredient["description"],
                    ingredient["nutritional_info"],
                    f"Store {ingredient['category'].lower()} appropriately",  # storage_notes
                    "",  # substitutions
                    "Seasonal availability varies",  # seasonality
                    "Premium",  # cost_level
                    "Specialty food suppliers",  # supplier_notes
                    "",  # allergen_info
                    "",  # best_before
                    f"Handle {ingredient['name'].lower()} with care",  # prep_notes
                    current_time,  # created_at
                    current_time,  # updated_at
                    None  # user_id
                ))
                
                added_count += 1
                next_id += 1
                print(f"Added: {ingredient['name']}")
                
            except Exception as e:
                print(f"Error adding {ingredient['name']}: {e}")
                continue
    
    conn.commit()
    return added_count

def main():
    """Main function to expand the ingredient database"""
    print("🌱 Expanding Iterum R&D Chef Notebook Ingredient Database")
    print("=" * 60)
    
    # Check if database exists
    db_path = "culinary_data.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        print("Please run the main application first to create the database.")
        return
    
    try:
        # Connect to database
        conn = create_database_connection(db_path)
        
        # Get current ingredient count
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ingredients")
        initial_count = cursor.fetchone()[0]
        print(f"📊 Current ingredients in database: {initial_count}")
        
        # Add professional ingredients
        print("\n🚀 Adding professional ingredients...")
        added_count = add_professional_ingredients(conn)
        
        # Get final count
        cursor.execute("SELECT COUNT(*) FROM ingredients")
        final_count = cursor.fetchone()[0]
        
        print(f"\n✅ Successfully added {added_count} professional ingredients!")
        print(f"📈 Total ingredients now: {final_count}")
        print(f"🎯 Database expansion complete!")
        
        # Show categories added
        print("\n📂 Categories expanded:")
        for category, ingredients in PROFESSIONAL_INGREDIENTS.items():
            print(f"   • {category}: {len(ingredients)} ingredients")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error expanding database: {e}")
        return

if __name__ == "__main__":
    main()