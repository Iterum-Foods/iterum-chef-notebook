#!/usr/bin/env python3
"""
Quick script to scan any folder for recipe files
"""

import sys
from pathlib import Path

# Import the RecipeLibrary class
sys.path.insert(0, str(Path(__file__).parent / "RecipeLibrarySystem"))
from recipe_library_system import RecipeLibrary

def scan_folder(folder_path):
    """Scan a specific folder for recipe files."""
    print(f"🔍 Scanning: {folder_path}")
    print("=" * 60)
    
    # Initialize library with custom source folder
    library = RecipeLibrary(source_folder=folder_path)
    
    # Scan and import
    recipes = library.scan_and_import()
    
    print(f"\n✅ Found {len(recipes)} recipe files!")
    print("\n📋 Recipe Summary:")
    print("-" * 60)
    
    for i, recipe in enumerate(recipes, 1):
        print(f"\n{i}. {recipe.title}")
        print(f"   Cuisine: {recipe.cuisine_type}")
        print(f"   Difficulty: {recipe.difficulty}")
        print(f"   Category: {recipe.category}")
        print(f"   Confidence: {recipe.confidence_score:.2f}")
        print(f"   Tags: {', '.join(recipe.tags) if recipe.tags else 'None'}")
        print(f"   File: {recipe.file_name}")
    
    return recipes

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("\n📁 Enter the folder path to scan: ").strip('"')
    
    if not Path(folder).exists():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)
    
    recipes = scan_folder(folder)
    
    print(f"\n\n🎉 Complete! {len(recipes)} recipes added to your library.")
    print(f"📚 Library location: recipe_library/")

