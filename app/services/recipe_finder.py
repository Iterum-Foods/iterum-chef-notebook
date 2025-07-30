"""
Recipe Finder Service
Automatically scans folders for recipe files, analyzes content, and categorizes them.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RecipeFile:
    """Represents a recipe file with metadata"""
    file_path: str
    file_name: str
    file_size: int
    file_type: str
    category: str  # 'recipe', 'menu', 'uncategorized'
    cuisine: str
    confidence_score: float
    metadata: Dict
    content_preview: str
    tags: List[str]
    detected_ingredients: List[str]
    cooking_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: str = 'medium'

class RecipeFinder:
    """Automated recipe finding and categorization service"""
    
    def __init__(self, source_folder: str = "uploads"):
        self.source_folder = Path(source_folder)
        self.recipe_extensions = {'.xlsx', '.xls', '.docx', '.doc', '.pdf', '.txt', '.csv', '.md'}
        
        # Cuisine detection keywords
        self.cuisine_types = {
            'italian': ['pasta', 'pizza', 'risotto', 'bruschetta', 'tiramisu', 'gnocchi', 'parmesan', 'basil', 'oregano', 'prosciutto'],
            'mexican': ['taco', 'enchilada', 'guacamole', 'salsa', 'queso', 'cilantro', 'lime', 'jalapeño', 'tortilla', 'mole'],
            'chinese': ['stir-fry', 'dim sum', 'wonton', 'dumpling', 'soy sauce', 'ginger', 'sesame', 'bok choy', 'rice wine'],
            'indian': ['curry', 'naan', 'tandoori', 'masala', 'garam', 'cardamom', 'cumin', 'turmeric', 'basmati'],
            'french': ['sauce', 'beurre', 'roux', 'bouillon', 'herbes', 'shallot', 'dijon', 'bordeaux', 'coq au vin'],
            'japanese': ['sushi', 'miso', 'tempura', 'teriyaki', 'wasabi', 'nori', 'dashi', 'mirin', 'sake'],
            'mediterranean': ['olive oil', 'feta', 'hummus', 'falafel', 'tabbouleh', 'tzatziki', 'oregano', 'lemon'],
            'american': ['burger', 'hot dog', 'barbecue', 'mac and cheese', 'apple pie', 'cornbread', 'clam chowder'],
            'thai': ['pad thai', 'tom yum', 'green curry', 'fish sauce', 'lemongrass', 'kaffir lime', 'coconut milk'],
            'greek': ['moussaka', 'spanakopita', 'souvlaki', 'feta', 'olive', 'oregano', 'lemon', 'yogurt']
        }
        
        # Recipe indicators
        self.recipe_keywords = {
            'ingredients': ['ingredients', 'ingredient', 'materials', 'supplies', 'items needed'],
            'instructions': ['instructions', 'directions', 'steps', 'method', 'procedure', 'how to'],
            'cooking': ['cook', 'bake', 'fry', 'grill', 'roast', 'simmer', 'boil', 'steam', 'sauté'],
            'measurements': ['cup', 'tablespoon', 'teaspoon', 'ounce', 'pound', 'gram', 'ml', 'tbsp', 'tsp'],
            'prep': ['preheat', 'prepare', 'chop', 'dice', 'mince', 'slice', 'grate', 'peel']
        }
        
        # Menu indicators
        self.menu_keywords = {
            'menu': ['menu', 'entrée', 'appetizer', 'dessert', 'main course', 'side dish'],
            'restaurant': ['restaurant', 'cafe', 'bistro', 'dining', 'service'],
            'meal': ['breakfast', 'lunch', 'dinner', 'brunch', 'snack', 'meal']
        }

    def scan_folder(self, folder_path: Optional[str] = None) -> List[RecipeFile]:
        """Scan a folder for recipe files and analyze them"""
        scan_path = Path(folder_path) if folder_path else self.source_folder
        
        if not scan_path.exists():
            logger.error(f"Folder not found: {scan_path}")
            return []
        
        logger.info(f"Scanning folder: {scan_path}")
        recipe_files = []
        
        for file_path in scan_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.recipe_extensions:
                try:
                    recipe_file = self.analyze_file(file_path)
                    if recipe_file:
                        recipe_files.append(recipe_file)
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")
        
        logger.info(f"Found {len(recipe_files)} recipe files")
        return recipe_files

    def analyze_file(self, file_path: Path) -> Optional[RecipeFile]:
        """Analyze a single file and extract recipe information"""
        try:
            # Basic file info
            file_name = file_path.name
            file_size = file_path.stat().st_size
            file_type = file_path.suffix.lower()
            
            # Skip files larger than 50MB
            if file_size > 50 * 1024 * 1024:
                logger.warning(f"Skipping large file: {file_name} ({file_size / 1024 / 1024:.1f}MB)")
                return None
            
            # Extract content preview
            content_preview = self.extract_content_preview(file_path)
            if not content_preview:
                return None
            
            # Analyze content
            category = self.categorize_content(content_preview)
            cuisine = self.detect_cuisine(content_preview)
            confidence_score = self.calculate_confidence(content_preview, category)
            metadata = self.extract_metadata(content_preview)
            tags = self.extract_tags(content_preview)
            detected_ingredients = self.extract_ingredients(content_preview)
            
            return RecipeFile(
                file_path=str(file_path),
                file_name=file_name,
                file_size=file_size,
                file_type=file_type,
                category=category,
                cuisine=cuisine,
                confidence_score=confidence_score,
                metadata=metadata,
                content_preview=content_preview[:500],  # Truncate for storage
                tags=tags,
                detected_ingredients=detected_ingredients,
                cooking_time=metadata.get('cooking_time'),
                servings=metadata.get('servings'),
                difficulty=metadata.get('difficulty', 'medium')
            )
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return None

    def extract_content_preview(self, file_path: Path) -> str:
        """Extract text content from various file types"""
        try:
            file_type = file_path.suffix.lower()
            
            if file_type in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(10000)  # Read first 10KB
            
            elif file_type in ['.csv']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(5000)
            
            elif file_type in ['.xlsx', '.xls']:
                try:
                    import pandas as pd
                    df = pd.read_excel(file_path, nrows=50)  # Read first 50 rows
                    return df.to_string()
                except ImportError:
                    logger.warning("pandas not available for Excel files")
                    return ""
            
            elif file_type in ['.docx', '.doc']:
                try:
                    from docx import Document
                    doc = Document(file_path)
                    return ' '.join([paragraph.text for paragraph in doc.paragraphs[:50]])
                except ImportError:
                    logger.warning("python-docx not available for Word files")
                    return ""
            
            elif file_type == '.pdf':
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages[:3]:  # First 3 pages
                            text += page.extract_text()
                        return text
                except ImportError:
                    logger.warning("PyPDF2 not available for PDF files")
                    return ""
            
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting content from {file_path}: {e}")
            return ""

    def categorize_content(self, content: str) -> str:
        """Categorize content as recipe, menu, or uncategorized"""
        content_lower = content.lower()
        
        # Count keyword matches
        recipe_score = 0
        menu_score = 0
        
        # Recipe indicators
        for category, keywords in self.recipe_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    recipe_score += 1
        
        # Menu indicators
        for category, keywords in self.menu_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    menu_score += 1
        
        # Decision logic
        if recipe_score >= 3:
            return 'recipe'
        elif menu_score >= 2:
            return 'menu'
        else:
            return 'uncategorized'

    def detect_cuisine(self, content: str) -> str:
        """Detect cuisine type from content"""
        content_lower = content.lower()
        cuisine_scores = {}
        
        for cuisine, keywords in self.cuisine_types.items():
            score = 0
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
            if score > 0:
                cuisine_scores[cuisine] = score
        
        if cuisine_scores:
            return max(cuisine_scores, key=cuisine_scores.get)
        else:
            return 'unknown'

    def calculate_confidence(self, content: str, category: str) -> float:
        """Calculate confidence score for recipe detection"""
        content_lower = content.lower()
        score = 0.0
        
        # Base score for category
        if category == 'recipe':
            score += 0.3
        elif category == 'menu':
            score += 0.2
        else:
            score += 0.1
        
        # Recipe keyword density
        recipe_keywords_found = 0
        total_keywords = 0
        for category_keywords in self.recipe_keywords.values():
            for keyword in category_keywords:
                total_keywords += 1
                if keyword in content_lower:
                    recipe_keywords_found += 1
        
        if total_keywords > 0:
            score += (recipe_keywords_found / total_keywords) * 0.4
        
        # Measurement indicators
        measurement_patterns = [r'\d+\s*(cup|tbsp|tsp|oz|lb|g|ml)', r'\d+\s*-\s*\d+', r'serves\s*\d+']
        for pattern in measurement_patterns:
            if re.search(pattern, content_lower):
                score += 0.1
        
        # Instruction indicators
        instruction_patterns = [r'\d+\.', r'step\s*\d+', r'first', r'then', r'next', r'finally']
        for pattern in instruction_patterns:
            if re.search(pattern, content_lower):
                score += 0.05
        
        return min(score, 1.0)

    def extract_metadata(self, content: str) -> Dict:
        """Extract metadata from content"""
        metadata = {}
        content_lower = content.lower()
        
        # Cooking time
        time_patterns = [
            r'(\d+)\s*(?:min|minute|minutes)',
            r'(\d+)\s*(?:hr|hour|hours)',
            r'prep.*?(\d+)\s*(?:min|minute|minutes)',
            r'cook.*?(\d+)\s*(?:min|minute|minutes)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, content_lower)
            if match:
                metadata['cooking_time'] = int(match.group(1))
                break
        
        # Servings
        serving_patterns = [
            r'serves\s*(\d+)',
            r'(\d+)\s*servings',
            r'(\d+)\s*people',
            r'(\d+)\s*portions'
        ]
        
        for pattern in serving_patterns:
            match = re.search(pattern, content_lower)
            if match:
                metadata['servings'] = int(match.group(1))
                break
        
        # Difficulty
        if any(word in content_lower for word in ['easy', 'simple', 'quick', 'basic']):
            metadata['difficulty'] = 'easy'
        elif any(word in content_lower for word in ['hard', 'complex', 'advanced', 'challenging']):
            metadata['difficulty'] = 'hard'
        else:
            metadata['difficulty'] = 'medium'
        
        return metadata

    def extract_tags(self, content: str) -> List[str]:
        """Extract tags from content"""
        tags = []
        content_lower = content.lower()
        
        # Meal types
        meal_types = ['breakfast', 'lunch', 'dinner', 'dessert', 'snack', 'appetizer']
        for meal in meal_types:
            if meal in content_lower:
                tags.append(meal)
        
        # Dietary restrictions
        dietary = ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'keto', 'paleo']
        for diet in dietary:
            if diet in content_lower:
                tags.append(diet)
        
        # Cooking methods
        methods = ['baked', 'fried', 'grilled', 'roasted', 'steamed', 'sautéed']
        for method in methods:
            if method in content_lower:
                tags.append(method)
        
        return tags

    def extract_ingredients(self, content: str) -> List[str]:
        """Extract ingredient names from content"""
        ingredients = []
        
        # Common ingredient patterns
        ingredient_patterns = [
            r'(\d+(?:\.\d+)?)\s*(cup|tbsp|tsp|oz|lb|g|ml)\s+([a-zA-Z\s]+)',
            r'([a-zA-Z\s]+)\s+(\d+(?:\.\d+)?)\s*(cup|tbsp|tsp|oz|lb|g|ml)',
            r'([a-zA-Z\s]+)\s*,\s*(\d+(?:\.\d+)?)',
        ]
        
        for pattern in ingredient_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) >= 3:
                    ingredient_name = match[2].strip()
                elif len(match) >= 1:
                    ingredient_name = match[0].strip()
                else:
                    continue
                
                if len(ingredient_name) > 2 and ingredient_name not in ingredients:
                    ingredients.append(ingredient_name)
        
        return ingredients[:20]  # Limit to 20 ingredients

    def organize_files(self, recipe_files: List[RecipeFile], output_folder: str = "sorted_recipes") -> Dict:
        """Organize recipe files into folders by category and cuisine"""
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        # Create folder structure
        folders = {
            'recipes': output_path / 'recipes',
            'menus': output_path / 'menus',
            'uncategorized': output_path / 'uncategorized'
        }
        
        for folder in folders.values():
            folder.mkdir(exist_ok=True)
        
        # Organize files
        organized_files = {
            'recipes': {},
            'menus': {},
            'uncategorized': []
        }
        
        for recipe_file in recipe_files:
            source_path = Path(recipe_file.file_path)
            
            if recipe_file.category == 'recipe':
                cuisine_folder = folders['recipes'] / recipe_file.cuisine
                cuisine_folder.mkdir(exist_ok=True)
                
                if recipe_file.cuisine not in organized_files['recipes']:
                    organized_files['recipes'][recipe_file.cuisine] = []
                
                # Copy file to organized location
                dest_path = cuisine_folder / recipe_file.file_name
                try:
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    organized_files['recipes'][recipe_file.cuisine].append(recipe_file)
                except Exception as e:
                    logger.error(f"Error copying {source_path}: {e}")
            
            elif recipe_file.category == 'menu':
                dest_path = folders['menus'] / recipe_file.file_name
                try:
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    organized_files['menus'][recipe_file.file_name] = recipe_file
                except Exception as e:
                    logger.error(f"Error copying {source_path}: {e}")
            
            else:
                dest_path = folders['uncategorized'] / recipe_file.file_name
                try:
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    organized_files['uncategorized'].append(recipe_file)
                except Exception as e:
                    logger.error(f"Error copying {source_path}: {e}")
        
        return organized_files

    def generate_report(self, recipe_files: List[RecipeFile], organized_files: Dict) -> Dict:
        """Generate a comprehensive analysis report"""
        total_files = len(recipe_files)
        recipes = [f for f in recipe_files if f.category == 'recipe']
        menus = [f for f in recipe_files if f.category == 'menu']
        uncategorized = [f for f in recipe_files if f.category == 'uncategorized']
        
        # Cuisine breakdown
        cuisine_stats = {}
        for recipe in recipes:
            cuisine = recipe.cuisine
            if cuisine not in cuisine_stats:
                cuisine_stats[cuisine] = 0
            cuisine_stats[cuisine] += 1
        
        # File type breakdown
        file_types = {}
        for file in recipe_files:
            file_type = file.file_type
            if file_type not in file_types:
                file_types[file_type] = 0
            file_types[file_type] += 1
        
        # Confidence score distribution
        confidence_ranges = {
            'high': len([f for f in recipe_files if f.confidence_score >= 0.7]),
            'medium': len([f for f in recipe_files if 0.4 <= f.confidence_score < 0.7]),
            'low': len([f for f in recipe_files if f.confidence_score < 0.4])
        }
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': total_files,
                'recipes': len(recipes),
                'menus': len(menus),
                'uncategorized': len(uncategorized)
            },
            'cuisine_breakdown': cuisine_stats,
            'file_types': file_types,
            'confidence_distribution': confidence_ranges,
            'organized_files': {
                'recipes_by_cuisine': {k: len(v) for k, v in organized_files['recipes'].items()},
                'menus': len(organized_files['menus']),
                'uncategorized': len(organized_files['uncategorized'])
            },
            'sample_files': [
                {
                    'name': f.file_name,
                    'category': f.category,
                    'cuisine': f.cuisine,
                    'confidence': f.confidence_score,
                    'tags': f.tags
                }
                for f in recipe_files[:10]  # First 10 files as sample
            ]
        }
        
        return report

    def save_report(self, report: Dict, output_folder: str = "sorted_recipes") -> str:
        """Save the analysis report to JSON file"""
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        report_file = output_path / f"recipe_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report saved to: {report_file}")
        return str(report_file) 