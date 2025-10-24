#!/usr/bin/env python3
"""
Recipe Library System
A library-style system that organizes recipes in a single location using metadata and tags.
"""

import os
import json
import shutil
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import logging
from datetime import datetime
import hashlib
from dataclasses import dataclass, asdict
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recipe_library.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class RecipeEntry:
    """Data class for a recipe entry in the library."""
    id: str
    file_name: str
    file_path: str
    file_extension: str
    file_size: int
    created_date: datetime
    modified_date: datetime
    title: str
    category: str
    cuisine_type: str
    difficulty: str
    cooking_time: str
    servings: str
    tags: List[str]
    confidence_score: float
    content_preview: str
    library_path: str
    is_uploaded: bool = False
    upload_date: Optional[datetime] = None

class RecipeLibrary:
    """Library-style recipe organization system."""
    
    def __init__(self, library_path: str = "recipe_library", source_folder: str = "Iterum App/uploads"):
        self.library_path = Path(library_path)
        self.source_folder = Path(source_folder)
        self.db_path = self.library_path / "recipe_library.db"
        self.metadata_path = self.library_path / "metadata.json"
        self.index_path = self.library_path / "index.json"
        
        # Supported file extensions
        self.recipe_extensions = {
            '.xlsx', '.xls', '.csv', '.pdf', '.txt', '.docx', '.doc', '.json', '.html', '.htm', '.md'
        }
        
        # Recipe keywords for detection
        self.recipe_keywords = {
            'ingredients', 'directions', 'instructions', 'preparation',
            'cooking time', 'prep time', 'servings', 'yield', 'portions',
            'preheat', 'oven', 'stovetop', 'bake', 'cook', 'simmer',
            'season', 'salt', 'pepper', 'garlic', 'onion', 'butter',
            'flour', 'sugar', 'eggs', 'milk', 'cream', 'cheese',
            'chicken', 'beef', 'pork', 'fish', 'vegetables', 'fruits',
            'recipe', 'dish', 'meal', 'cuisine', 'kitchen'
        }
        
        # Cuisine types for categorization
        self.cuisine_types = {
            'italian': ['pasta', 'pizza', 'risotto', 'bruschetta', 'tiramisu', 'parmesan', 'basil'],
            'mexican': ['taco', 'burrito', 'enchilada', 'guacamole', 'salsa', 'cilantro', 'lime'],
            'chinese': ['stir fry', 'dumpling', 'noodle', 'dim sum', 'kung pao', 'soy sauce', 'ginger'],
            'indian': ['curry', 'naan', 'tandoori', 'biryani', 'masala', 'turmeric', 'cumin'],
            'french': ['ratatouille', 'coq au vin', 'beef bourguignon', 'creme brulee', 'herbs de provence'],
            'japanese': ['sushi', 'ramen', 'tempura', 'miso', 'teriyaki', 'wasabi', 'nori'],
            'mediterranean': ['hummus', 'falafel', 'tabbouleh', 'tzatziki', 'olive oil', 'feta'],
            'american': ['burger', 'hot dog', 'apple pie', 'barbecue', 'casserole', 'cornbread'],
            'thai': ['pad thai', 'tom yum', 'green curry', 'mango sticky rice', 'fish sauce'],
            'greek': ['moussaka', 'souvlaki', 'baklava', 'feta', 'olive', 'oregano']
        }
        
        # Difficulty indicators
        self.difficulty_indicators = {
            'easy': ['simple', 'quick', 'basic', 'beginner', 'easy', 'fast'],
            'medium': ['moderate', 'intermediate', 'standard', 'moderate'],
            'hard': ['advanced', 'complex', 'challenging', 'difficult', 'expert', 'elaborate']
        }
        
        self.ensure_library_structure()
        self.init_database()
    
    def ensure_library_structure(self):
        """Create the library directory structure."""
        self.library_path.mkdir(exist_ok=True)
        logger.info(f"Library path: {self.library_path.absolute()}")
    
    def init_database(self):
        """Initialize the SQLite database for recipe metadata."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_extension TEXT,
                file_size INTEGER,
                created_date TEXT,
                modified_date TEXT,
                title TEXT,
                category TEXT,
                cuisine_type TEXT,
                difficulty TEXT,
                cooking_time TEXT,
                servings TEXT,
                tags TEXT,
                confidence_score REAL,
                content_preview TEXT,
                library_path TEXT,
                is_uploaded BOOLEAN DEFAULT FALSE,
                upload_date TEXT,
                UNIQUE(file_path)
            )
        ''')
        
        # Create tags table for better querying
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id TEXT,
                tag TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuisine ON recipes(cuisine_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON recipes(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON recipes(difficulty)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON tags(tag)')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def scan_and_import(self) -> List[RecipeEntry]:
        """Scan source folder and import recipes to library."""
        if not self.source_folder.exists():
            logger.error(f"Source folder does not exist: {self.source_folder}")
            return []
        
        logger.info(f"Scanning {self.source_folder} for recipes...")
        
        recipe_files = []
        total_files = 0
        
        for file_path in self.source_folder.rglob('*'):
            if file_path.is_file():
                total_files += 1
                if file_path.suffix.lower() in self.recipe_extensions:
                    recipe_entry = self.analyze_and_import_file(file_path)
                    if recipe_entry:
                        recipe_files.append(recipe_entry)
                        logger.info(f"Imported: {file_path.name}")
        
        logger.info(f"Scanned {total_files} files, imported {len(recipe_files)} recipes")
        return recipe_files
    
    def analyze_and_import_file(self, file_path: Path) -> Optional[RecipeEntry]:
        """Analyze a file and import it to the library if it's a recipe."""
        try:
            # Get basic file info
            stat = file_path.stat()
            file_name = file_path.name
            file_extension = file_path.suffix.lower()
            file_size = stat.st_size
            
            # Skip files that are too large
            if file_size > 50 * 1024 * 1024:  # 50MB
                return None
            
            # Extract content preview
            content_preview = self.extract_content_preview(file_path)
            
            # Analyze content for recipe indicators
            confidence_score = self.calculate_confidence(content_preview)
            
            if confidence_score < 0.1:  # Low confidence, skip
                return None
            
            # Generate unique ID
            file_hash = hashlib.md5(f"{file_path.absolute()}_{stat.st_mtime}".encode()).hexdigest()
            
            # Determine metadata
            category = self.determine_category(content_preview)
            cuisine_type = self.determine_cuisine(content_preview)
            difficulty = self.determine_difficulty(content_preview)
            cooking_time = self.extract_cooking_time(content_preview)
            servings = self.extract_servings(content_preview)
            tags = self.extract_tags(content_preview)
            title = self.extract_title(file_name, content_preview)
            
            # Copy file to library
            library_file_path = self.copy_to_library(file_path, file_hash)
            
            # Create recipe entry
            recipe_entry = RecipeEntry(
                id=file_hash,
                file_name=file_name,
                file_path=str(file_path),
                file_extension=file_extension,
                file_size=file_size,
                created_date=datetime.fromtimestamp(stat.st_ctime),
                modified_date=datetime.fromtimestamp(stat.st_mtime),
                title=title,
                category=category,
                cuisine_type=cuisine_type,
                difficulty=difficulty,
                cooking_time=cooking_time,
                servings=servings,
                tags=tags,
                confidence_score=confidence_score,
                content_preview=content_preview[:500],
                library_path=str(library_file_path)
            )
            
            # Save to database
            self.save_to_database(recipe_entry)
            
            return recipe_entry
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {str(e)}")
            return None
    
    def copy_to_library(self, source_path: Path, file_hash: str) -> Path:
        """Copy file to library with hash-based naming."""
        extension = source_path.suffix
        library_filename = f"{file_hash}{extension}"
        library_file_path = self.library_path / library_filename
        
        if not library_file_path.exists():
            shutil.copy2(source_path, library_file_path)
            logger.info(f"Copied to library: {library_filename}")
        
        return library_file_path
    
    def extract_content_preview(self, file_path: Path) -> str:
        """Extract a preview of the file content for analysis."""
        try:
            extension = file_path.suffix.lower()
            
            if extension in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(2000)
            
            elif extension in ['.json']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(2000)
            
            elif extension in ['.html', '.htm']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(2000)
                    import re
                    return re.sub(r'<[^>]+>', '', content)
            
            elif extension in ['.xlsx', '.xls', '.csv']:
                try:
                    import pandas as pd
                    if extension == '.csv':
                        df = pd.read_csv(file_path, nrows=10)
                    else:
                        df = pd.read_excel(file_path, nrows=10)
                    return df.to_string()
                except:
                    return f"Excel/CSV file: {file_path.name}"
            
            elif extension in ['.docx', '.doc']:
                return f"Word document: {file_path.name}"
            
            elif extension == '.pdf':
                return f"PDF file: {file_path.name}"
            
            else:
                return f"File: {file_path.name}"
                
        except Exception as e:
            logger.error(f"Error extracting content from {file_path}: {str(e)}")
            return ""
    
    def calculate_confidence(self, content: str) -> float:
        """Calculate confidence score that this is a recipe file."""
        if not content:
            return 0.0
        
        content_lower = content.lower()
        score = 0.0
        
        # Check for recipe keywords
        recipe_matches = sum(1 for keyword in self.recipe_keywords if keyword in content_lower)
        score += recipe_matches * 0.1
        
        # Bonus for having both ingredients and instructions
        if 'ingredients' in content_lower and ('instructions' in content_lower or 'directions' in content_lower):
            score += 0.3
        
        # Bonus for cooking-related terms
        cooking_terms = ['preheat', 'bake', 'cook', 'simmer', 'boil', 'fry', 'grill']
        cooking_matches = sum(1 for term in cooking_terms if term in content_lower)
        score += cooking_matches * 0.05
        
        return min(score, 1.0)
    
    def determine_category(self, content: str) -> str:
        """Determine if this is a recipe or menu."""
        content_lower = content.lower()
        
        menu_keywords = ['menu', 'appetizer', 'entree', 'main course', 'dessert', 'breakfast', 'lunch', 'dinner']
        menu_indicators = sum(1 for keyword in menu_keywords if keyword in content_lower)
        recipe_indicators = sum(1 for keyword in self.recipe_keywords if keyword in content_lower)
        
        if menu_indicators > recipe_indicators:
            return 'menu'
        elif recipe_indicators > 0:
            return 'recipe'
        else:
            return 'uncategorized'
    
    def determine_cuisine(self, content: str) -> str:
        """Determine the cuisine type based on content."""
        content_lower = content.lower()
        
        for cuisine, keywords in self.cuisine_types.items():
            if any(keyword in content_lower for keyword in keywords):
                return cuisine
        
        return 'unknown'
    
    def determine_difficulty(self, content: str) -> str:
        """Determine the difficulty level."""
        content_lower = content.lower()
        
        for difficulty, indicators in self.difficulty_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                return difficulty
        
        return 'unknown'
    
    def extract_cooking_time(self, content: str) -> str:
        """Extract cooking time information."""
        import re
        time_patterns = [
            r'(\d+)\s*(?:min|minutes?)',
            r'(\d+)\s*(?:hr|hour|hours?)',
            r'(\d+)\s*(?:day|days?)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return 'unknown'
    
    def extract_servings(self, content: str) -> str:
        """Extract serving information."""
        import re
        serving_patterns = [
            r'(\d+)\s*(?:servings?|portions?|people)',
            r'serves\s*(\d+)',
            r'yield[s]?\s*(\d+)'
        ]
        
        for pattern in serving_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return 'unknown'
    
    def extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content."""
        tags = []
        content_lower = content.lower()
        
        # Add cuisine tags
        for cuisine, keywords in self.cuisine_types.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(cuisine)
        
        # Add difficulty tags
        for difficulty, indicators in self.difficulty_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                tags.append(difficulty)
        
        # Add meal type tags
        meal_types = ['breakfast', 'lunch', 'dinner', 'dessert', 'appetizer', 'snack']
        for meal_type in meal_types:
            if meal_type in content_lower:
                tags.append(meal_type)
        
        # Add ingredient-based tags
        ingredient_tags = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'spicy', 'sweet', 'savory']
        for tag in ingredient_tags:
            if tag in content_lower:
                tags.append(tag)
        
        return list(set(tags))
    
    def extract_title(self, filename: str, content: str) -> str:
        """Extract or generate a title for the recipe."""
        # Try to extract title from filename first
        title = filename.replace('_', ' ').replace('-', ' ').replace('.xlsx', '').replace('.docx', '')
        
        # Clean up the title
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title
    
    def save_to_database(self, recipe: RecipeEntry):
        """Save recipe entry to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert recipe
            cursor.execute('''
                INSERT OR REPLACE INTO recipes (
                    id, file_name, file_path, file_extension, file_size,
                    created_date, modified_date, title, category, cuisine_type,
                    difficulty, cooking_time, servings, tags, confidence_score,
                    content_preview, library_path, is_uploaded, upload_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe.id, recipe.file_name, recipe.file_path, recipe.file_extension,
                recipe.file_size, recipe.created_date.isoformat(), recipe.modified_date.isoformat(),
                recipe.title, recipe.category, recipe.cuisine_type, recipe.difficulty,
                recipe.cooking_time, recipe.servings, json.dumps(recipe.tags),
                recipe.confidence_score, recipe.content_preview, recipe.library_path,
                recipe.is_uploaded, recipe.upload_date.isoformat() if recipe.upload_date else None
            ))
            
            # Insert tags
            cursor.execute('DELETE FROM tags WHERE recipe_id = ?', (recipe.id,))
            for tag in recipe.tags:
                cursor.execute('INSERT INTO tags (recipe_id, tag) VALUES (?, ?)', (recipe.id, tag))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error saving recipe to database: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def search_recipes(self, 
                      cuisine: Optional[str] = None,
                      category: Optional[str] = None,
                      difficulty: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      search_text: Optional[str] = None,
                      limit: int = 50) -> List[RecipeEntry]:
        """Search recipes in the library."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM recipes WHERE 1=1"
        params = []
        
        if cuisine:
            query += " AND cuisine_type = ?"
            params.append(cuisine)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)
        
        if search_text:
            query += " AND (title LIKE ? OR content_preview LIKE ?)"
            search_pattern = f"%{search_text}%"
            params.extend([search_pattern, search_pattern])
        
        if tags:
            placeholders = ','.join(['?' for _ in tags])
            query += f" AND id IN (SELECT DISTINCT recipe_id FROM tags WHERE tag IN ({placeholders}))"
            params.extend(tags)
        
        query += " ORDER BY confidence_score DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        recipes = []
        for row in cursor.fetchall():
            recipe = self.row_to_recipe_entry(row)
            if recipe:
                recipes.append(recipe)
        
        conn.close()
        return recipes
    
    def row_to_recipe_entry(self, row) -> Optional[RecipeEntry]:
        """Convert database row to RecipeEntry object."""
        try:
            return RecipeEntry(
                id=row[0],
                file_name=row[1],
                file_path=row[2],
                file_extension=row[3],
                file_size=row[4],
                created_date=datetime.fromisoformat(row[5]),
                modified_date=datetime.fromisoformat(row[6]),
                title=row[7],
                category=row[8],
                cuisine_type=row[9],
                difficulty=row[10],
                cooking_time=row[11],
                servings=row[12],
                tags=json.loads(row[13]) if row[13] else [],
                confidence_score=row[14],
                content_preview=row[15],
                library_path=row[16],
                is_uploaded=bool(row[17]),
                upload_date=datetime.fromisoformat(row[18]) if row[18] else None
            )
        except Exception as e:
            logger.error(f"Error converting row to RecipeEntry: {str(e)}")
            return None
    
    def get_library_stats(self) -> Dict[str, Any]:
        """Get statistics about the recipe library."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total recipes
        cursor.execute('SELECT COUNT(*) FROM recipes')
        stats['total_recipes'] = cursor.fetchone()[0]
        
        # By category
        cursor.execute('SELECT category, COUNT(*) FROM recipes GROUP BY category')
        stats['by_category'] = dict(cursor.fetchall())
        
        # By cuisine
        cursor.execute('SELECT cuisine_type, COUNT(*) FROM recipes GROUP BY cuisine_type')
        stats['by_cuisine'] = dict(cursor.fetchall())
        
        # By difficulty
        cursor.execute('SELECT difficulty, COUNT(*) FROM recipes GROUP BY difficulty')
        stats['by_difficulty'] = dict(cursor.fetchall())
        
        # Popular tags
        cursor.execute('SELECT tag, COUNT(*) FROM tags GROUP BY tag ORDER BY COUNT(*) DESC LIMIT 10')
        stats['popular_tags'] = dict(cursor.fetchall())
        
        # Upload status
        cursor.execute('SELECT is_uploaded, COUNT(*) FROM recipes GROUP BY is_uploaded')
        stats['upload_status'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def export_library(self, output_file: str = "recipe_library_export.json") -> str:
        """Export the entire library to JSON."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM recipes')
        rows = cursor.fetchall()
        
        recipes = []
        for row in rows:
            recipe = self.row_to_recipe_entry(row)
            if recipe:
                recipes.append(asdict(recipe))
        
        conn.close()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_recipes': len(recipes),
            'library_path': str(self.library_path),
            'recipes': recipes
        }
        
        export_path = self.library_path / output_file
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Library exported to: {export_path}")
        return str(export_path)
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[RecipeEntry]:
        """Get a specific recipe by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return self.row_to_recipe_entry(row)
        return None

def main():
    """Main function to demonstrate the library system."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Recipe Library System')
    parser.add_argument('--scan', action='store_true', help='Scan and import recipes')
    parser.add_argument('--search', help='Search recipes')
    parser.add_argument('--cuisine', help='Filter by cuisine')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--difficulty', help='Filter by difficulty')
    parser.add_argument('--tags', help='Filter by tags (comma-separated)')
    parser.add_argument('--stats', action='store_true', help='Show library statistics')
    parser.add_argument('--export', action='store_true', help='Export library to JSON')
    
    args = parser.parse_args()
    
    library = RecipeLibrary()
    
    if args.scan:
        print("🔍 Scanning and importing recipes...")
        recipes = library.scan_and_import()
        print(f"✅ Imported {len(recipes)} recipes")
    
    if args.stats:
        print("📊 Library Statistics:")
        stats = library.get_library_stats()
        print(f"Total recipes: {stats['total_recipes']}")
        print(f"By category: {stats['by_category']}")
        print(f"By cuisine: {stats['by_cuisine']}")
        print(f"By difficulty: {stats['by_difficulty']}")
        print(f"Popular tags: {stats['popular_tags']}")
    
    if args.search or args.cuisine or args.category or args.difficulty or args.tags:
        tags = args.tags.split(',') if args.tags else None
        recipes = library.search_recipes(
            cuisine=args.cuisine,
            category=args.category,
            difficulty=args.difficulty,
            tags=tags,
            search_text=args.search
        )
        
        print(f"🔍 Found {len(recipes)} recipes:")
        for recipe in recipes:
            print(f"  - {recipe.title} ({recipe.cuisine_type}, {recipe.difficulty})")
    
    if args.export:
        export_path = library.export_library()
        print(f"📄 Library exported to: {export_path}")

if __name__ == "__main__":
    main() 