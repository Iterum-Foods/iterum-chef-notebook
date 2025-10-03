#!/usr/bin/env python3
"""
Recipe Splitter - Extract individual recipes from Word documents
Splits documents with multiple recipes into separate structured recipes
"""

import os
import sys
from pathlib import Path
from docx import Document
import re
from typing import List, Dict, Any
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.recipe_parser import RecipeParser, ParsedRecipe

class RecipeSplitter:
    def __init__(self):
        self.parser = RecipeParser()
        
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from Word document"""
        try:
            doc = Document(file_path)
            text_content = []
            
            for paragraph in doc.paragraphs:
                text_content.append(paragraph.text)
            
            return "\n".join(text_content)
        except Exception as e:
            raise Exception(f"Failed to read Word document: {str(e)}")
    
    def split_recipes_by_patterns(self, text: str) -> List[str]:
        """Split text into individual recipes using common patterns"""
        
        # Common recipe separators
        separators = [
            r'\n\s*Recipe\s*\d+',  # "Recipe 1", "Recipe 2", etc.
            r'\n\s*\d+\.\s*[A-Z]',  # "1. RECIPE NAME", "2. ANOTHER RECIPE"
            r'\n\s*[A-Z][A-Z\s]{10,}',  # Long ALL CAPS titles
            r'\n\s*={3,}',  # Multiple equals signs
            r'\n\s*-{3,}',  # Multiple dashes
            r'\n\s*\*{3,}',  # Multiple asterisks
            r'\n\s*#{2,}',  # Multiple hash symbols
        ]
        
        # Try different splitting patterns
        for separator in separators:
            splits = re.split(separator, text, flags=re.IGNORECASE | re.MULTILINE)
            if len(splits) > 1:
                print(f"✅ Found {len(splits)} sections using pattern: {separator}")
                return [section.strip() for section in splits if section.strip()]
        
        # If no clear separators, try to split by recipe titles
        return self.split_by_recipe_titles(text)
    
    def split_by_recipe_titles(self, text: str) -> List[str]:
        """Split by detecting recipe titles"""
        lines = text.split('\n')
        recipes = []
        current_recipe = []
        
        for line in lines:
            line = line.strip()
            if not line:
                current_recipe.append(line)
                continue
            
            # Check if this looks like a recipe title
            if self.is_likely_recipe_title(line):
                # Save previous recipe if exists
                if current_recipe:
                    recipe_text = '\n'.join(current_recipe).strip()
                    if len(recipe_text) > 50:  # Only save substantial content
                        recipes.append(recipe_text)
                
                # Start new recipe
                current_recipe = [line]
            else:
                current_recipe.append(line)
        
        # Add the last recipe
        if current_recipe:
            recipe_text = '\n'.join(current_recipe).strip()
            if len(recipe_text) > 50:
                recipes.append(recipe_text)
        
        return recipes
    
    def is_likely_recipe_title(self, line: str) -> bool:
        """Determine if a line is likely a recipe title"""
        line = line.strip()
        
        # Skip empty lines
        if not line:
            return False
        
        # Skip very short lines
        if len(line) < 5:
            return False
        
        # Skip lines that look like ingredients or instructions
        ingredient_indicators = ['cup', 'tsp', 'tbsp', 'oz', 'lb', 'gram', 'ml', 'liter']
        instruction_indicators = ['heat', 'cook', 'bake', 'mix', 'stir', 'add', 'combine', 'step']
        
        line_lower = line.lower()
        if any(indicator in line_lower for indicator in ingredient_indicators + instruction_indicators):
            return False
        
        # Recipe titles are often:
        # - All caps or title case
        # - Standalone lines
        # - Contain food-related keywords
        food_keywords = ['chicken', 'beef', 'soup', 'salad', 'cake', 'bread', 'sauce', 'pasta', 'rice']
        
        # Title case or all caps
        if line.isupper() or line.istitle():
            return True
        
        # Contains food keywords and looks like a title
        if any(keyword in line_lower for keyword in food_keywords):
            return True
        
        return False
    
    def clean_recipe_text(self, text: str) -> str:
        """Clean up recipe text"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Remove empty lines at start/end but keep them in middle
            if line or cleaned_lines:
                cleaned_lines.append(line)
        
        # Remove trailing empty lines
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()
        
        return '\n'.join(cleaned_lines)
    
    def process_document(self, file_path: str, output_dir: str = None) -> List[Dict[str, Any]]:
        """Process Word document and split into individual recipes"""
        
        print(f"📄 Processing document: {file_path}")
        
        # Extract text from document
        full_text = self.extract_text_from_docx(file_path)
        print(f"📝 Extracted {len(full_text)} characters of text")
        
        # Split into individual recipes
        recipe_texts = self.split_recipes_by_patterns(full_text)
        print(f"🔄 Split into {len(recipe_texts)} potential recipes")
        
        # Process each recipe
        processed_recipes = []
        for i, recipe_text in enumerate(recipe_texts, 1):
            print(f"\n📋 Processing Recipe {i}...")
            
            # Clean the text
            cleaned_text = self.clean_recipe_text(recipe_text)
            
            if len(cleaned_text) < 50:
                print(f"⚠️  Skipping Recipe {i} - too short ({len(cleaned_text)} chars)")
                continue
            
            try:
                # Parse the recipe
                parsed_recipe = self.parser.parse_recipe_text(cleaned_text)
                
                # Convert to dictionary
                recipe_dict = self.parser.to_dict(parsed_recipe)
                
                # Add metadata
                recipe_dict['source_document'] = os.path.basename(file_path)
                recipe_dict['recipe_number'] = i
                recipe_dict['raw_text'] = cleaned_text
                
                # If no title was detected, create one
                if not recipe_dict.get('title'):
                    recipe_dict['title'] = f"Recipe {i} from {os.path.basename(file_path)}"
                
                processed_recipes.append(recipe_dict)
                
                print(f"✅ Recipe {i}: {recipe_dict['title']}")
                print(f"   - Ingredients: {len(recipe_dict.get('ingredients', []))}")
                print(f"   - Instructions: {len(recipe_dict.get('instructions', []))}")
                
            except Exception as e:
                print(f"❌ Failed to parse Recipe {i}: {str(e)}")
                
                # Still save the raw text for manual review
                recipe_dict = {
                    'title': f"Recipe {i} from {os.path.basename(file_path)} (Parse Failed)",
                    'raw_text': cleaned_text,
                    'parse_error': str(e),
                    'source_document': os.path.basename(file_path),
                    'recipe_number': i
                }
                processed_recipes.append(recipe_dict)
        
        # Save to output directory if specified
        if output_dir:
            self.save_recipes(processed_recipes, output_dir, os.path.basename(file_path))
        
        return processed_recipes
    
    def save_recipes(self, recipes: List[Dict[str, Any]], output_dir: str, source_filename: str):
        """Save individual recipes to files"""
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        base_name = Path(source_filename).stem
        
        for i, recipe in enumerate(recipes, 1):
            # Create filename
            title = recipe.get('title', f'Recipe_{i}')
            # Clean title for filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{base_name}_{i:02d}_{safe_title}.json"
            
            # Save as JSON
            file_path = output_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(recipe, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved: {filename}")

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Split Word document with multiple recipes')
    parser.add_argument('input_file', help='Path to Word document')
    parser.add_argument('-o', '--output', help='Output directory for individual recipes')
    parser.add_argument('--preview', action='store_true', help='Preview mode - show what would be extracted')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"❌ File not found: {args.input_file}")
        return 1
    
    # Set default output directory
    if not args.output:
        args.output = f"extracted_recipes_{Path(args.input_file).stem}"
    
    try:
        splitter = RecipeSplitter()
        recipes = splitter.process_document(args.input_file, 
                                          None if args.preview else args.output)
        
        print(f"\n🎉 Successfully processed {len(recipes)} recipes!")
        
        if args.preview:
            print("\n📋 PREVIEW - Recipe titles found:")
            for i, recipe in enumerate(recipes, 1):
                print(f"   {i}. {recipe.get('title', 'No title')}")
            print(f"\nTo extract recipes, run without --preview flag")
        else:
            print(f"📁 Recipes saved to: {args.output}")
            print("\n💡 Next steps:")
            print("   1. Review the extracted JSON files")
            print("   2. Upload individual recipes to Iterum Chef Notebook")
            print("   3. Edit and refine as needed")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
