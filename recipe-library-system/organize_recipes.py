#!/usr/bin/env python3
"""
Organize Recipes - Consolidate all recipes into one library
Options: Copy (safe) or Move (consolidate)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "RecipeLibrarySystem"))
from recipe_library_system import RecipeLibrary

def organize_recipes(source_folder, move_files=False):
    """
    Organize all recipes from a folder into the library.
    
    Args:
        source_folder: Path to folder containing recipes
        move_files: If True, moves files. If False, copies files (default)
    """
    print("=" * 70)
    print("           📚 RECIPE LIBRARY ORGANIZER")
    print("=" * 70)
    print(f"\n🔍 Source Folder: {source_folder}")
    print(f"📦 Library Location: recipe_library/")
    print(f"{'🚚 Mode: MOVE (files will be relocated)' if move_files else '📋 Mode: COPY (originals preserved)'}")
    print("=" * 70)
    
    # Ask for confirmation if moving files
    if move_files:
        print("\n⚠️  WARNING: Files will be MOVED (not copied)")
        print("   Original files will be removed from their current location!")
        confirm = input("\n   Type 'YES' to confirm: ").strip().upper()
        if confirm != 'YES':
            print("❌ Operation cancelled.")
            return
    
    print("\n🔄 Scanning for recipe files...")
    
    # Initialize library
    library = RecipeLibrary(source_folder=source_folder)
    
    # Modify behavior to move instead of copy if requested
    if move_files:
        import shutil
        original_copy_method = library.copy_to_library
        
        def move_to_library(source_path, file_hash):
            """Move file to library instead of copying."""
            extension = source_path.suffix
            library_filename = f"{file_hash}{extension}"
            library_file_path = library.library_path / library_filename
            
            if not library_file_path.exists():
                shutil.move(str(source_path), str(library_file_path))
                print(f"   ✓ Moved: {source_path.name} → {library_filename}")
            else:
                print(f"   ⊘ Duplicate skipped: {source_path.name}")
                # Delete the duplicate since it's already in library
                source_path.unlink()
            
            return library_file_path
        
        library.copy_to_library = move_to_library
    
    # Scan and import
    recipes = library.scan_and_import()
    
    print("\n" + "=" * 70)
    print(f"✅ SUCCESS! Organized {len(recipes)} recipes")
    print("=" * 70)
    
    # Show statistics
    stats = library.get_library_stats()
    print(f"\n📊 Library Statistics:")
    print(f"   Total recipes: {stats['total_recipes']}")
    
    print(f"\n📂 By Category:")
    for category, count in stats['by_category'].items():
        print(f"   • {category.capitalize()}: {count}")
    
    print(f"\n🌍 By Cuisine:")
    for cuisine, count in sorted(stats['by_cuisine'].items(), key=lambda x: x[1], reverse=True)[:5]:
        if cuisine != 'unknown':
            print(f"   • {cuisine.capitalize()}: {count}")
    
    print(f"\n📍 Library Location: {Path('recipe_library').absolute()}")
    print(f"💾 Database: recipe_library/recipe_library.db")
    
    return recipes

def main():
    print("\n" + "=" * 70)
    print("           🍳 RECIPE ORGANIZER")
    print("=" * 70)
    
    # Get source folder
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        print("\nThis tool will scan a folder and organize all recipes into one library.")
        source_folder = input("\n📁 Enter folder path to organize: ").strip('"')
    
    if not Path(source_folder).exists():
        print(f"\n❌ ERROR: Folder not found: {source_folder}")
        return
    
    # Ask if user wants to move or copy
    print("\n" + "=" * 70)
    print("Choose organization mode:")
    print("=" * 70)
    print("\n1. COPY mode (safer - keeps original files)")
    print("   • Original files stay in place")
    print("   • Copies are stored in library")
    print("   • Safe for testing")
    
    print("\n2. MOVE mode (consolidate - relocates files)")
    print("   • Files are moved to library")
    print("   • Original location will be empty")
    print("   • Consolidates everything in one place")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    move_files = (choice == '2')
    
    # Organize
    recipes = organize_recipes(source_folder, move_files=move_files)
    
    if recipes:
        print("\n" + "=" * 70)
        print("🎉 COMPLETE!")
        print("=" * 70)
        print("\nYou can now:")
        print("  • Search recipes: py run_library.py")
        print("  • View dashboard: py recipe_dashboard.py")
        print("  • Browse library folder: recipe_library/")

if __name__ == "__main__":
    main()

