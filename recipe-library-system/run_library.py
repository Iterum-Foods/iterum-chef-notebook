#!/usr/bin/env python3
"""
Simple interface for the Recipe Library System
"""

from recipe_library_system import RecipeLibrary
import os

def main():
    print("📚 Recipe Library System")
    print("=" * 50)
    print("A library-style system for organizing recipes")
    print("=" * 50)
    
    # Initialize library
    library = RecipeLibrary()
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Scan and import recipes")
        print("2. Search recipes")
        print("3. Browse by cuisine")
        print("4. Browse by category")
        print("5. Browse by difficulty")
        print("6. Show library statistics")
        print("7. Export library")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            # Scan and import
            print("\n🔍 Scanning and importing recipes...")
            recipes = library.scan_and_import()
            print(f"✅ Imported {len(recipes)} recipes to library")
            
        elif choice == "2":
            # Search recipes
            print("\n🔍 Search Recipes")
            search_text = input("Enter search terms: ").strip()
            if search_text:
                recipes = library.search_recipes(search_text=search_text)
                print(f"\nFound {len(recipes)} recipes:")
                for i, recipe in enumerate(recipes, 1):
                    print(f"  {i}. {recipe.title}")
                    print(f"     Cuisine: {recipe.cuisine_type}, Difficulty: {recipe.difficulty}")
                    print(f"     Tags: {', '.join(recipe.tags)}")
                    print()
            else:
                print("❌ Please enter search terms")
                
        elif choice == "3":
            # Browse by cuisine
            print("\n🌍 Browse by Cuisine")
            cuisines = ['italian', 'mexican', 'chinese', 'indian', 'french', 'japanese', 
                       'mediterranean', 'american', 'thai', 'greek', 'unknown']
            
            print("Available cuisines:")
            for i, cuisine in enumerate(cuisines, 1):
                print(f"  {i}. {cuisine.capitalize()}")
            
            cuisine_choice = input("\nSelect cuisine (1-11): ").strip()
            try:
                cuisine_index = int(cuisine_choice) - 1
                if 0 <= cuisine_index < len(cuisines):
                    selected_cuisine = cuisines[cuisine_index]
                    recipes = library.search_recipes(cuisine=selected_cuisine)
                    print(f"\nFound {len(recipes)} {selected_cuisine} recipes:")
                    for i, recipe in enumerate(recipes, 1):
                        print(f"  {i}. {recipe.title} ({recipe.difficulty})")
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == "4":
            # Browse by category
            print("\n📂 Browse by Category")
            categories = ['recipe', 'menu', 'uncategorized']
            
            print("Available categories:")
            for i, category in enumerate(categories, 1):
                print(f"  {i}. {category.capitalize()}")
            
            category_choice = input("\nSelect category (1-3): ").strip()
            try:
                category_index = int(category_choice) - 1
                if 0 <= category_index < len(categories):
                    selected_category = categories[category_index]
                    recipes = library.search_recipes(category=selected_category)
                    print(f"\nFound {len(recipes)} {selected_category} files:")
                    for i, recipe in enumerate(recipes, 1):
                        print(f"  {i}. {recipe.title} ({recipe.cuisine_type})")
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == "5":
            # Browse by difficulty
            print("\n⚡ Browse by Difficulty")
            difficulties = ['easy', 'medium', 'hard', 'unknown']
            
            print("Available difficulties:")
            for i, difficulty in enumerate(difficulties, 1):
                print(f"  {i}. {difficulty.capitalize()}")
            
            difficulty_choice = input("\nSelect difficulty (1-4): ").strip()
            try:
                difficulty_index = int(difficulty_choice) - 1
                if 0 <= difficulty_index < len(difficulties):
                    selected_difficulty = difficulties[difficulty_index]
                    recipes = library.search_recipes(difficulty=selected_difficulty)
                    print(f"\nFound {len(recipes)} {selected_difficulty} recipes:")
                    for i, recipe in enumerate(recipes, 1):
                        print(f"  {i}. {recipe.title} ({recipe.cuisine_type})")
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == "6":
            # Show statistics
            print("\n📊 Library Statistics:")
            stats = library.get_library_stats()
            print(f"Total recipes: {stats['total_recipes']}")
            print()
            print("By category:")
            for category, count in stats['by_category'].items():
                print(f"  {category.capitalize()}: {count}")
            print()
            print("By cuisine:")
            for cuisine, count in stats['by_cuisine'].items():
                if cuisine != 'unknown':
                    print(f"  {cuisine.capitalize()}: {count}")
            print()
            print("By difficulty:")
            for difficulty, count in stats['by_difficulty'].items():
                if difficulty != 'unknown':
                    print(f"  {difficulty.capitalize()}: {count}")
            print()
            print("Popular tags:")
            for tag, count in list(stats['popular_tags'].items())[:10]:
                print(f"  {tag}: {count}")
                
        elif choice == "7":
            # Export library
            print("\n📄 Exporting library...")
            export_path = library.export_library()
            print(f"✅ Library exported to: {export_path}")
            
        elif choice == "8":
            # Exit
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 