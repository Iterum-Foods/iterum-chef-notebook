"""
Migration: Add Project System
Adds projects table and updates existing tables to support project-based organization
"""

import sqlite3
import json
from datetime import datetime

def migrate_database(db_path: str = "culinary_data.db"):
    """Add project system to database"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Step 1: Create projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                restaurant_name TEXT,
                cuisine_type TEXT,
                location TEXT,
                is_default BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                color_theme TEXT DEFAULT '#3B82F6',
                owner_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        """)
        
        # Step 2: Create project_equipment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                equipment_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                location TEXT,
                notes TEXT,
                is_available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                UNIQUE(project_id, equipment_id)
            )
        """)
        
        # Step 3: Create menus table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                menu_type TEXT DEFAULT 'Regular',
                project_id INTEGER NOT NULL,
                owner_id INTEGER NOT NULL,
                sections TEXT,
                items TEXT,
                pricing TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_published BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        """)
        
        # Step 4: Add project_id to recipes table if it doesn't exist
        cursor.execute("PRAGMA table_info(recipes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'project_id' not in columns:
            cursor.execute("ALTER TABLE recipes ADD COLUMN project_id INTEGER")
            
        # Step 5: Create default "Full Library" projects for existing users
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
        
        for user_id, user_name in users:
            # Create default Full Library project
            cursor.execute("""
                INSERT INTO projects (name, description, is_default, owner_id)
                VALUES (?, ?, ?, ?)
            """, (
                "Full Library",
                f"Complete recipe and menu library for {user_name}",
                True,
                user_id
            ))
            
            default_project_id = cursor.lastrowid
            
            # Update existing recipes to belong to default project
            cursor.execute("""
                UPDATE recipes 
                SET project_id = ? 
                WHERE user_id = ? AND project_id IS NULL
            """, (default_project_id, user_id))
            
            print(f"✅ Created Full Library project for {user_name} (ID: {default_project_id})")
        
        # Step 6: Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_project ON recipes(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_menus_project ON menus(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_project_equipment_project ON project_equipment(project_id)")
        
        conn.commit()
        print("✅ Project system migration completed successfully!")
        
        # Step 7: Show summary
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        print(f"📊 Migration Summary:")
        print(f"   - Created {project_count} projects for {user_count} users")
        print(f"   - Added project support to recipes table")
        print(f"   - Created menus and project_equipment tables")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

def rollback_migration(db_path: str = "culinary_data.db"):
    """Rollback project system migration"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Drop new tables
        cursor.execute("DROP TABLE IF EXISTS menus")
        cursor.execute("DROP TABLE IF EXISTS project_equipment") 
        cursor.execute("DROP TABLE IF EXISTS projects")
        
        # Remove project_id column from recipes (SQLite limitation - recreate table)
        cursor.execute("PRAGMA table_info(recipes)")
        columns = [f"{col[1]} {col[2]}" for col in cursor.fetchall() if col[1] != 'project_id']
        
        if len(columns) > 0:
            cursor.execute("CREATE TABLE recipes_backup AS SELECT * FROM recipes")
            cursor.execute("DROP TABLE recipes")
            cursor.execute(f"CREATE TABLE recipes ({', '.join(columns)})")
            cursor.execute("INSERT INTO recipes SELECT * FROM recipes_backup")
            cursor.execute("DROP TABLE recipes_backup")
        
        conn.commit()
        print("✅ Project system migration rolled back successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Rollback failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback_migration()
    else:
        migrate_database()