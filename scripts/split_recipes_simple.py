#!/usr/bin/env python3
"""
Simple Recipe Splitter - Quick version for immediate use
"""

from docx import Document
import re
import os
import json
from pathlib import Path

def extract_text_from_docx(file_path):
    """Extract text from Word document"""
    doc = Document(file_path)
    text_content = []
    
    for paragraph in doc.paragraphs:
        text_content.append(paragraph.text)
    
    return "\n".join(text_content)

def simple_split_recipes(text):
    """Simple recipe splitting logic"""
    
    # Split by common patterns
    patterns = [
        r'\n\s*Recipe\s*\d+',  # "Recipe 1", "Recipe 2"
        r'\n\s*\d+\.\s*[A-Z]',  # "1. RECIPE NAME"
        r'\n\s*[A-Z][A-Z\s]{10,}',  # Long ALL CAPS titles
        r'\n\s*={3,}',  # ===
        r'\n\s*-{3,}',  # ---
    ]
    
    for pattern in patterns:
        splits = re.split(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if len(splits) > 1:
            print(f"Found {len(splits)} sections using pattern")
            return [section.strip() for section in splits if section.strip() and len(section.strip()) > 50]
    
    # If no patterns work, try to split by empty lines and long text blocks
    sections = text.split('\n\n\n')  # Triple line breaks
    if len(sections) > 1:
        return [section.strip() for section in sections if len(section.strip()) > 100]
    
    # Last resort: split by double line breaks if text is very long
    if len(text) > 2000:
        sections = text.split('\n\n')
        substantial_sections = [s.strip() for s in sections if len(s.strip()) > 200]
        if len(substantial_sections) > 1:
            return substantial_sections
    
    return [text]  # Return as single recipe if no splitting possible

def process_word_document(file_path):
    """Process Word document and extract recipes"""
    
    print(f"📄 Processing: {file_path}")
    
    # Extract text
    full_text = extract_text_from_docx(file_path)
    print(f"📝 Extracted {len(full_text)} characters")
    
    # Split into recipes
    recipe_texts = simple_split_recipes(full_text)
    print(f"🔄 Found {len(recipe_texts)} potential recipes")
    
    # Create output directory
    base_name = Path(file_path).stem
    output_dir = f"extracted_recipes_{base_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each recipe
    recipes = []
    for i, recipe_text in enumerate(recipe_texts, 1):
        
        # Create basic recipe structure
        lines = recipe_text.split('\n')
        title = lines[0].strip() if lines else f"Recipe {i}"
        
        # Clean title
        if len(title) > 100:
            title = title[:100] + "..."
        
        recipe = {
            'title': title,
            'raw_text': recipe_text,
            'source_document': os.path.basename(file_path),
            'recipe_number': i,
            'character_count': len(recipe_text)
        }
        
        # Save to file
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)[:50]
        filename = f"{base_name}_{i:02d}_{safe_title}.json"
        
        file_path_out = os.path.join(output_dir, filename)
        with open(file_path_out, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)
        
        recipes.append(recipe)
        print(f"✅ Recipe {i}: {title[:50]}...")
        print(f"   💾 Saved as: {filename}")
    
    print(f"\n🎉 Extracted {len(recipes)} recipes to '{output_dir}'")
    return recipes, output_dir

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python split_recipes_simple.py <word_document.docx>")
        print("Example: python split_recipes_simple.py my_recipes.docx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    try:
        recipes, output_dir = process_word_document(file_path)
        
        print(f"\n📋 Summary:")
        for recipe in recipes:
            print(f"   • {recipe['title'][:60]}... ({recipe['character_count']} chars)")
        
        print(f"\n💡 Next steps:")
        print(f"   1. Review files in '{output_dir}'")
        print(f"   2. Upload individual recipes to Iterum Chef Notebook")
        print(f"   3. Edit and refine as needed")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
