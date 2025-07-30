#!/usr/bin/env python3
"""
Clear All Users Script for Iterum R&D Chef Notebook

This script safely removes all users from both database systems:
1. Main authentication database (SQLAlchemy)
2. Culinary data database (SQLite)

Usage: python clear_users.py [--confirm]
"""

import os
import sys
import sqlite3
from sqlalchemy.orm import Session
from sqlalchemy import text
from pathlib import Path

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.database import SessionLocal, User, Recipe, RecipeVersion, engine
from app.sqlite_database import CulinaryDatabase
from app.core.config import settings


def clear_sqlalchemy_users(db: Session) -> int:
    """Clear all users and related data from the main SQLAlchemy database."""
    try:
        # Get count before deletion
        user_count = db.query(User).count()
        recipe_count = db.query(Recipe).count()
        version_count = db.query(RecipeVersion).count()
        
        print(f"Found {user_count} users, {recipe_count} recipes, {version_count} recipe versions")
        
        if user_count == 0:
            print("No users found in SQLAlchemy database.")
            return 0
        
        # Delete in order to respect foreign key constraints
        # First delete recipe versions
        if version_count > 0:
            db.query(RecipeVersion).delete()
            print(f"Deleted {version_count} recipe versions")
        
        # Then delete recipes
        if recipe_count > 0:
            db.query(Recipe).delete()
            print(f"Deleted {recipe_count} recipes")
        
        # Finally delete users
        db.query(User).delete()
        print(f"Deleted {user_count} users from SQLAlchemy database")
        
        # Commit all changes
        db.commit()
        
        return user_count
        
    except Exception as e:
        print(f"Error clearing SQLAlchemy users: {e}")
        db.rollback()
        return 0


def clear_sqlite_users() -> int:
    """Clear all users from the SQLite culinary database."""
    try:
        db = CulinaryDatabase()
        
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            
            # Get count before deletion
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                print("No users found in SQLite database.")
                return 0
            
            # Delete all users
            cursor.execute("DELETE FROM users")
            
            # Also clear user-specific data from other tables
            tables_to_clear = [
                "ingredients",
                "recipes", 
                "pantry_items",
                "menus",
                "equipment",
                "vendors"
            ]
            
            for table in tables_to_clear:
                try:
                    # Check if table exists and has user_id column
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    if 'user_id' in columns:
                        cursor.execute(f"DELETE FROM {table} WHERE user_id IS NOT NULL")
                        affected = cursor.rowcount
                        if affected > 0:
                            print(f"Cleared {affected} user-specific records from {table}")
                            
                except sqlite3.OperationalError:
                    # Table doesn't exist, skip
                    pass
            
            conn.commit()
            print(f"Deleted {user_count} users from SQLite database")
            
            return user_count
            
    except Exception as e:
        print(f"Error clearing SQLite users: {e}")
        return 0


def reset_database_sequences():
    """Reset auto-increment sequences for a clean start."""
    try:
        with SessionLocal() as db:
            # Reset SQLAlchemy sequences
            db.execute(text("DELETE FROM sqlite_sequence WHERE name='users'"))
            db.execute(text("DELETE FROM sqlite_sequence WHERE name='recipes'"))
            db.execute(text("DELETE FROM sqlite_sequence WHERE name='recipe_versions'"))
            db.commit()
            print("Reset SQLAlchemy auto-increment sequences")
            
    except Exception as e:
        print(f"Note: Could not reset sequences: {e}")


def backup_databases():
    """Create backup copies of databases before clearing."""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup SQLAlchemy database
    if "sqlite" in settings.DATABASE_URL:
        db_file = settings.DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_file):
            backup_file = f"{db_file}.backup_{timestamp}"
            shutil.copy2(db_file, backup_file)
            print(f"Backed up main database to: {backup_file}")
    
    # Backup culinary database
    culinary_db = "culinary_data.db"
    if os.path.exists(culinary_db):
        backup_file = f"{culinary_db}.backup_{timestamp}"
        shutil.copy2(culinary_db, backup_file)
        print(f"Backed up culinary database to: {backup_file}")


def main():
    """Main function to clear all users."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clear all users from the system")
    parser.add_argument("--confirm", action="store_true", 
                       help="Skip confirmation prompt and proceed with clearing")
    parser.add_argument("--no-backup", action="store_true",
                       help="Skip creating backup files")
    args = parser.parse_args()
    
    print("=" * 60)
    print("CLEAR ALL USERS - Iterum R&D Chef Notebook")
    print("=" * 60)
    print()
    
    # Check if databases exist
    databases_found = []
    
    if "sqlite" in settings.DATABASE_URL:
        db_file = settings.DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_file):
            databases_found.append(f"Main database: {db_file}")
    
    if os.path.exists("culinary_data.db"):
        databases_found.append("Culinary database: culinary_data.db")
    
    if not databases_found:
        print("No databases found. Nothing to clear.")
        return
    
    print("Databases found:")
    for db in databases_found:
        print(f"  • {db}")
    print()
    
    # Get user counts
    total_users = 0
    
    try:
        with SessionLocal() as db:
            sqlalchemy_users = db.query(User).count()
            total_users += sqlalchemy_users
            if sqlalchemy_users > 0:
                print(f"SQLAlchemy database: {sqlalchemy_users} users")
    except Exception as e:
        print(f"Could not check SQLAlchemy users: {e}")
    
    try:
        db = CulinaryDatabase()
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            sqlite_users = cursor.fetchone()[0]
            total_users += sqlite_users
            if sqlite_users > 0:
                print(f"SQLite database: {sqlite_users} users")
    except Exception as e:
        print(f"Could not check SQLite users: {e}")
    
    if total_users == 0:
        print("\nNo users found in any database. Nothing to clear.")
        return
    
    print(f"\nTotal users to be cleared: {total_users}")
    print()
    
    # Confirmation
    if not args.confirm:
        print("⚠️  WARNING: This will permanently delete ALL users and their data!")
        print("   This includes recipes, profiles, and all user-specific content.")
        print()
        response = input("Are you sure you want to continue? (yes/no): ").lower().strip()
        
        if response not in ['yes', 'y']:
            print("Operation cancelled.")
            return
    
    # Create backups
    if not args.no_backup:
        print("\nCreating backups...")
        backup_databases()
        print()
    
    # Clear users
    print("Clearing users...")
    print("-" * 40)
    
    cleared_count = 0
    
    # Clear SQLAlchemy users
    try:
        with SessionLocal() as db:
            cleared_count += clear_sqlalchemy_users(db)
    except Exception as e:
        print(f"Error with SQLAlchemy database: {e}")
    
    # Clear SQLite users
    try:
        cleared_count += clear_sqlite_users()
    except Exception as e:
        print(f"Error with SQLite database: {e}")
    
    # Reset sequences
    print("\nResetting database sequences...")
    reset_database_sequences()
    
    print("-" * 40)
    print(f"✅ Successfully cleared {cleared_count} users from the system!")
    print()
    print("The application is now ready for fresh user registrations.")
    print("All user data has been cleared and the system is in a clean state.")


if __name__ == "__main__":
    main() 