"""
Migration: Add Firebase authentication fields to users table
"""

from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.sql import text
from datetime import datetime
import os

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./culinary_data.db")

def migrate():
    """Add Firebase fields to users table"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("🔄 Starting migration: Add Firebase fields...")
        
        try:
            # Add firebase_uid column
            conn.execute(text("""
                ALTER TABLE users ADD COLUMN firebase_uid VARCHAR(255)
            """))
            print("✅ Added firebase_uid column")
        except Exception as e:
            print(f"⚠️ firebase_uid column may already exist: {e}")
        
        try:
            # Add auth_provider column
            conn.execute(text("""
                ALTER TABLE users ADD COLUMN auth_provider VARCHAR(50) DEFAULT 'local'
            """))
            print("✅ Added auth_provider column")
        except Exception as e:
            print(f"⚠️ auth_provider column may already exist: {e}")
        
        try:
            # Add photo_url column
            conn.execute(text("""
                ALTER TABLE users ADD COLUMN photo_url VARCHAR(512)
            """))
            print("✅ Added photo_url column")
        except Exception as e:
            print(f"⚠️ photo_url column may already exist: {e}")
        
        try:
            # Add last_login column
            conn.execute(text("""
                ALTER TABLE users ADD COLUMN last_login DATETIME
            """))
            print("✅ Added last_login column")
        except Exception as e:
            print(f"⚠️ last_login column may already exist: {e}")
        
        # Commit the changes
        conn.commit()
        
        print("✅ Migration complete!")

if __name__ == "__main__":
    migrate()

