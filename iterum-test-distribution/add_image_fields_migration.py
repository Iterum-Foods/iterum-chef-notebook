#!/usr/bin/env python3
"""
Database Migration: Add Image Fields to Recipes and Ingredients

This migration adds image support fields to the recipes and ingredients tables.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from sqlalchemy import create_engine, text
from app.database import Base, engine
from app.core.config import settings

def add_image_fields():
    """Add image fields to existing tables"""
    
    print("🔄 Adding image fields to database tables...")
    
    try:
        with engine.connect() as connection:
            # Add image fields to recipes table
            recipe_fields = [
                "ALTER TABLE recipes ADD COLUMN primary_image VARCHAR",
                "ALTER TABLE recipes ADD COLUMN gallery_images JSON",
                "ALTER TABLE recipes ADD COLUMN step_images JSON"
            ]
            
            # Add image fields to ingredients table  
            ingredient_fields = [
                "ALTER TABLE ingredients ADD COLUMN primary_image VARCHAR",
                "ALTER TABLE ingredients ADD COLUMN gallery_images JSON"
            ]
            
            # Execute recipe table modifications
            print("📸 Adding image fields to recipes table...")
            for sql in recipe_fields:
                try:
                    connection.execute(text(sql))
                    print(f"✅ Executed: {sql}")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"⚠️  Field already exists: {sql}")
                    else:
                        print(f"❌ Error executing {sql}: {e}")
            
            # Execute ingredient table modifications
            print("🥬 Adding image fields to ingredients table...")
            for sql in ingredient_fields:
                try:
                    connection.execute(text(sql))
                    print(f"✅ Executed: {sql}")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"⚠️  Field already exists: {sql}")
                    else:
                        print(f"❌ Error executing {sql}: {e}")
            
            # Commit changes
            connection.commit()
            print("✅ Database migration completed successfully!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    return True

def create_image_directories():
    """Create necessary image storage directories"""
    
    print("📁 Creating image storage directories...")
    
    directories = [
        "static",
        "static/images", 
        "static/images/recipes",
        "static/images/ingredients"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Run the migration"""
    
    print("=" * 60)
    print("ITERUM R&D CHEF NOTEBOOK - IMAGE FIELDS MIGRATION")
    print("=" * 60)
    print()
    
    print("This migration will add image support to your database:")
    print("• Recipes: primary_image, gallery_images, step_images")
    print("• Ingredients: primary_image, gallery_images")
    print("• Create image storage directories")
    print()
    
    response = input("Continue with migration? (y/N): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Migration cancelled.")
        return
    
    print("\n🚀 Starting migration...")
    
    # Create image directories
    create_image_directories()
    
    # Add database fields
    if add_image_fields():
        print("\n🎉 Migration completed successfully!")
        print("\nNew capabilities added:")
        print("• Upload primary images for recipes and ingredients")
        print("• Add multiple gallery images to recipes") 
        print("• Attach images to specific recipe steps")
        print("• Automatic image resizing and thumbnail generation")
        print("• Image management API endpoints")
        print("\nYou can now use the image upload features in:")
        print("• Recipe Developer")
        print("• Ingredients Manager")
        print("• Recipe Creation/Editing")
        
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 