#!/usr/bin/env python3
"""
Migration 004: Add OCR Processing Fields
Adds fields needed for OCR processing and recipe creation from uploads
"""

import sqlite3
import logging
from datetime import datetime

def run_migration(db_path: str = "culinary_data.db"):
    """Run migration to add OCR processing fields"""
    
    print("🔄 Running Migration 004: Add OCR Processing Fields")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add new fields to recipe_uploads table
        print("📝 Adding OCR fields to recipe_uploads table...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(recipe_uploads)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        if 'processing_info' not in existing_columns:
            cursor.execute("ALTER TABLE recipe_uploads ADD COLUMN processing_info TEXT")
            print("   ✅ Added processing_info column")
        
        if 'created_recipe_id' not in existing_columns:
            cursor.execute("ALTER TABLE recipe_uploads ADD COLUMN created_recipe_id INTEGER")
            print("   ✅ Added created_recipe_id column")
        
        # Add new fields to recipes table
        print("📝 Adding source field to recipes table...")
        
        cursor.execute("PRAGMA table_info(recipes)")
        existing_recipe_columns = [row[1] for row in cursor.fetchall()]
        
        if 'source' not in existing_recipe_columns:
            cursor.execute("ALTER TABLE recipes ADD COLUMN source TEXT")
            print("   ✅ Added source column to recipes")
        
        # Update upload statuses to include new values
        print("📝 Updating upload status values...")
        
        # Check current statuses and update any that need updating
        cursor.execute("SELECT id, upload_status FROM recipe_uploads")
        uploads = cursor.fetchall()
        
        status_updates = 0
        for upload_id, current_status in uploads:
            if current_status not in ['pending', 'processing', 'completed', 'failed', 'completed_with_warnings', 'recipe_created', 'recipe_creation_failed']:
                cursor.execute("UPDATE recipe_uploads SET upload_status = 'pending' WHERE id = ?", (upload_id,))
                status_updates += 1
        
        if status_updates > 0:
            print(f"   ✅ Updated {status_updates} upload status values")
        
        conn.commit()
        print("✅ Migration 004 completed successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM recipe_uploads")
        upload_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = cursor.fetchone()[0]
        
        print(f"📊 Database Summary:")
        print(f"   • Recipe Uploads: {upload_count}")
        print(f"   • Recipes: {recipe_count}")
        print(f"   • OCR Processing: Ready ✅")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

def rollback_migration(db_path: str = "culinary_data.db"):
    """Rollback migration (remove added fields)"""
    
    print("🔄 Rolling back Migration 004...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQLite doesn't support DROP COLUMN, so we would need to recreate tables
        # For now, just log what would be removed
        print("⚠️  SQLite doesn't support column removal.")
        print("   Fields added: processing_info, created_recipe_id, source")
        print("   To rollback completely, restore from backup before migration.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Rollback failed: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback_migration()
    else:
        run_migration()