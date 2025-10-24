#!/usr/bin/env python3
"""
Recipe Source Tracker - Find recipes by date and original location
Track which restaurant, project, or folder recipes came from
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

def get_source_folder(file_path):
    """Extract the immediate parent folder from a file path."""
    try:
        path = Path(file_path)
        # Get parent folder name (the folder containing the recipe)
        if path.parent.name:
            return path.parent.name
        return "Root"
    except:
        return "Unknown"

def get_project_name(file_path):
    """
    Extract project/restaurant name from file path.
    Looks for meaningful folder names in the path.
    """
    try:
        path = Path(file_path)
        parts = path.parts
        
        # Skip generic folder names
        skip_folders = {'uploads', 'documents', 'files', 'recipes', 'downloads', 
                       'desktop', 'onedrive', 'users', 'c:', 'd:'}
        
        # Find meaningful folder names
        meaningful = [p for p in parts if p.lower() not in skip_folders and len(p) > 2]
        
        if meaningful:
            # Return the most specific folder (usually the last one before filename)
            return meaningful[-1] if len(meaningful) > 0 else meaningful[0]
        
        return path.parent.name
    except:
        return "Unknown"

def search_by_date_range(start_date=None, end_date=None, date_field='modified_date'):
    """
    Search recipes by date range.
    
    Args:
        start_date: Start date (YYYY-MM-DD) or None for no limit
        end_date: End date (YYYY-MM-DD) or None for no limit
        date_field: 'created_date' or 'modified_date'
    """
    conn = sqlite3.connect('recipe_library/recipe_library.db')
    cursor = conn.cursor()
    
    query = f"SELECT title, file_path, created_date, modified_date, cuisine_type, category FROM recipes"
    conditions = []
    params = []
    
    if start_date:
        conditions.append(f"{date_field} >= ?")
        params.append(start_date)
    
    if end_date:
        conditions.append(f"{date_field} <= ?")
        params.append(end_date)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += f" ORDER BY {date_field} DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return results

def search_by_location(location_pattern):
    """
    Search recipes by original file path.
    
    Args:
        location_pattern: Text to search for in file path (e.g., "Restaurant", "Italian Project")
    """
    conn = sqlite3.connect('recipe_library/recipe_library.db')
    cursor = conn.cursor()
    
    query = "SELECT title, file_path, created_date, modified_date, cuisine_type, category FROM recipes WHERE file_path LIKE ? ORDER BY modified_date DESC"
    cursor.execute(query, (f"%{location_pattern}%",))
    results = cursor.fetchall()
    conn.close()
    
    return results

def group_by_source():
    """Group all recipes by their source folder/project."""
    conn = sqlite3.connect('recipe_library/recipe_library.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, file_path, created_date, modified_date, cuisine_type FROM recipes ORDER BY file_path")
    results = cursor.fetchall()
    conn.close()
    
    # Group by source
    by_source = defaultdict(list)
    
    for recipe in results:
        title, file_path, created, modified, cuisine = recipe
        project = get_project_name(file_path)
        by_source[project].append({
            'title': title,
            'path': file_path,
            'created': created,
            'modified': modified,
            'cuisine': cuisine
        })
    
    return by_source

def show_all_sources():
    """Show all unique source locations."""
    print("\n" + "=" * 80)
    print("           ALL RECIPE SOURCES")
    print("=" * 80)
    
    by_source = group_by_source()
    
    print(f"\nFound {len(by_source)} different sources:\n")
    
    for source, recipes in sorted(by_source.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n[{source}]")
        print(f"   {len(recipes)} recipes")
        print(f"   Sample: {recipes[0]['title']}")
        if len(recipes) > 1:
            print(f"           {recipes[1]['title']}")
        print("   " + "-" * 70)

def show_recipes_by_source(source_name):
    """Show all recipes from a specific source."""
    by_source = group_by_source()
    
    # Find matching sources (case insensitive)
    matches = {k: v for k, v in by_source.items() if source_name.lower() in k.lower()}
    
    if not matches:
        print(f"\n[!] No recipes found from source: {source_name}")
        return
    
    print("\n" + "=" * 80)
    print(f"           RECIPES FROM: {source_name.upper()}")
    print("=" * 80)
    
    for source, recipes in matches.items():
        print(f"\nSource Folder: {source}")
        print(f"   Total Recipes: {len(recipes)}")
        print("=" * 80)
        
        for i, recipe in enumerate(recipes, 1):
            print(f"\n{i}. {recipe['title']}")
            print(f"   Cuisine: {recipe['cuisine']}")
            print(f"   Modified: {recipe['modified'][:10]}")
            print(f"   Path: {recipe['path']}")

def show_recipes_by_date(year=None, month=None):
    """Show recipes by year and optionally month."""
    print("\n" + "=" * 80)
    print(f"           RECIPES FROM {month}/{year if month else year}")
    print("=" * 80)
    
    if year and month:
        start_date = f"{year}-{month:02d}-01"
        # Simple end date calculation
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
    elif year:
        start_date = f"{year}-01-01"
        end_date = f"{year + 1}-01-01"
    else:
        print("[!] Please provide at least a year")
        return
    
    results = search_by_date_range(start_date, end_date)
    
    if not results:
        print(f"\n[!] No recipes found for {year}/{month if month else 'all'}")
        return
    
    print(f"\nFound {len(results)} recipes:\n")
    
    for i, recipe in enumerate(results, 1):
        title, file_path, created, modified, cuisine, category = recipe
        project = get_project_name(file_path)
        print(f"{i}. {title}")
        print(f"   From: {project}")
        print(f"   Cuisine: {cuisine}")
        print(f"   Modified: {modified[:10]}")
        print()

def interactive_menu():
    """Interactive menu for tracking recipe sources."""
    while True:
        print("\n" + "=" * 80)
        print("           RECIPE SOURCE TRACKER")
        print("=" * 80)
        print("\n1. View all source locations (restaurants/projects)")
        print("2. View recipes from specific location")
        print("3. Search by date (year/month)")
        print("4. Search by location keyword")
        print("5. Export source report")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            show_all_sources()
        
        elif choice == '2':
            source = input("\nEnter source name: ").strip()
            if source:
                show_recipes_by_source(source)
        
        elif choice == '3':
            year = input("\nEnter year (YYYY): ").strip()
            month = input("Enter month (MM, or leave blank for whole year): ").strip()
            
            try:
                year_int = int(year)
                month_int = int(month) if month else None
                show_recipes_by_date(year_int, month_int)
            except ValueError:
                print("[!] Invalid date format")
        
        elif choice == '4':
            keyword = input("\nEnter location keyword: ").strip()
            if keyword:
                results = search_by_location(keyword)
                print(f"\nFound {len(results)} recipes with '{keyword}' in path:\n")
                for i, recipe in enumerate(results, 1):
                    title, file_path, created, modified, cuisine, category = recipe
                    print(f"{i}. {title}")
                    print(f"   Path: {file_path}")
                    print(f"   Modified: {modified[:10]}")
                    print()
        
        elif choice == '5':
            export_source_report()
        
        elif choice == '6':
            print("\nGoodbye!")
            break

def export_source_report():
    """Export a detailed source report."""
    import json
    
    by_source = group_by_source()
    
    report = {
        'generated': datetime.now().isoformat(),
        'total_sources': len(by_source),
        'total_recipes': sum(len(recipes) for recipes in by_source.values()),
        'sources': {}
    }
    
    for source, recipes in by_source.items():
        report['sources'][source] = {
            'count': len(recipes),
            'recipes': [
                {
                    'title': r['title'],
                    'path': r['path'],
                    'modified': r['modified'],
                    'cuisine': r['cuisine']
                }
                for r in recipes
            ]
        }
    
    output_file = 'recipe_sources_report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n[OK] Report exported to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'sources':
            show_all_sources()
        elif command == 'date' and len(sys.argv) > 2:
            year = int(sys.argv[2])
            month = int(sys.argv[3]) if len(sys.argv) > 3 else None
            show_recipes_by_date(year, month)
        elif command == 'location' and len(sys.argv) > 2:
            show_recipes_by_source(sys.argv[2])
        else:
            print("Usage: py track_recipe_sources.py [sources|date|location]")
    else:
        interactive_menu()

