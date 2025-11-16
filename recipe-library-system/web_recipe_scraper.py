#!/usr/bin/env python3
"""
Web Recipe Scraper
Scrapes recipes from websites and imports them into the recipe library
Supports Schema.org Recipe markup, HTML parsing, and common recipe site formats
"""

import sys
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import urlparse, urljoin
import logging

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)

# Add RecipeLibrarySystem to path
sys.path.insert(0, str(Path(__file__).parent / "RecipeLibrarySystem"))
from recipe_library_system import RecipeLibrary, RecipeEntry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebRecipeScraper:
    """Scrape recipes from websites and import to library."""
    
    def __init__(self, library_path: str = "recipe_library"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(exist_ok=True)
        self.library = RecipeLibrary(library_path=library_path)
        
        # User agent to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Common recipe site patterns
        self.recipe_indicators = [
            'recipe', 'ingredient', 'instruction', 'direction',
            'prep time', 'cook time', 'servings', 'yield',
            'preheat', 'oven', 'bake', 'cook', 'simmer'
        ]
    
    def scrape_recipe(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a recipe from a URL.
        
        Args:
            url: URL of the recipe page
            
        Returns:
            Dictionary with recipe data or None if failed
        """
        try:
            logger.info(f"Scraping recipe from: {url}")
            
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different extraction methods
            recipe_data = None
            
            # Method 1: Schema.org JSON-LD (most reliable)
            recipe_data = self._extract_schema_org(soup, url)
            
            # Method 2: Schema.org microdata
            if not recipe_data:
                recipe_data = self._extract_microdata(soup, url)
            
            # Method 3: Common HTML patterns
            if not recipe_data:
                recipe_data = self._extract_html_patterns(soup, url)
            
            if recipe_data:
                logger.info(f"Successfully extracted recipe: {recipe_data.get('title', 'Unknown')}")
                return recipe_data
            else:
                logger.warning(f"Could not extract recipe data from: {url}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error scraping recipe from {url}: {e}")
            return None
    
    def _extract_schema_org(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract recipe from Schema.org JSON-LD markup."""
        try:
            # Find JSON-LD scripts
            scripts = soup.find_all('script', type='application/ld+json')
            
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    
                    # Handle both single objects and arrays
                    if isinstance(data, list):
                        for item in data:
                            if item.get('@type') == 'Recipe' or 'Recipe' in item.get('@type', []):
                                return self._parse_schema_recipe(item, url)
                    elif isinstance(data, dict):
                        if data.get('@type') == 'Recipe' or 'Recipe' in data.get('@type', []):
                            return self._parse_schema_recipe(data, url)
                        # Check for @graph
                        if '@graph' in data:
                            for item in data['@graph']:
                                if item.get('@type') == 'Recipe' or 'Recipe' in item.get('@type', []):
                                    return self._parse_schema_recipe(item, url)
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            logger.debug(f"Error extracting Schema.org JSON-LD: {e}")
        
        return None
    
    def _parse_schema_recipe(self, data: Dict, url: str) -> Dict[str, Any]:
        """Parse Schema.org Recipe data structure."""
        recipe = {
            'title': self._get_nested_value(data, ['name', 'headline']),
            'description': self._get_nested_value(data, ['description']),
            'url': url,
            'ingredients': [],
            'instructions': [],
            'prep_time': self._parse_duration(self._get_nested_value(data, ['prepTime'])),
            'cook_time': self._parse_duration(self._get_nested_value(data, ['cookTime'])),
            'total_time': self._parse_duration(self._get_nested_value(data, ['totalTime'])),
            'servings': self._get_nested_value(data, ['recipeYield', 'yield']),
            'author': self._get_nested_value(data, ['author', 'name']),
            'image': self._get_nested_value(data, ['image']),
            'cuisine': self._get_nested_value(data, ['recipeCuisine']),
            'category': self._get_nested_value(data, ['recipeCategory']),
            'keywords': self._get_nested_value(data, ['keywords']),
        }
        
        # Extract ingredients
        ingredients = data.get('recipeIngredient', [])
        if isinstance(ingredients, list):
            recipe['ingredients'] = [str(ing) for ing in ingredients]
        
        # Extract instructions
        instructions = data.get('recipeInstructions', [])
        if isinstance(instructions, list):
            recipe['instructions'] = []
            for step in instructions:
                if isinstance(step, dict):
                    recipe['instructions'].append(step.get('text', step.get('name', '')))
                else:
                    recipe['instructions'].append(str(step))
        elif isinstance(instructions, str):
            recipe['instructions'] = [instructions]
        
        # Handle image (can be string or object)
        if isinstance(recipe['image'], dict):
            recipe['image'] = recipe['image'].get('url', '')
        elif isinstance(recipe['image'], list) and recipe['image']:
            recipe['image'] = recipe['image'][0] if isinstance(recipe['image'][0], str) else recipe['image'][0].get('url', '')
        
        return recipe
    
    def _extract_microdata(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract recipe from Schema.org microdata."""
        try:
            recipe_elem = soup.find(itemtype=re.compile(r'.*Recipe'))
            if not recipe_elem:
                return None
            
            recipe = {
                'title': self._get_itemprop(recipe_elem, 'name'),
                'description': self._get_itemprop(recipe_elem, 'description'),
                'url': url,
                'ingredients': [],
                'instructions': [],
                'prep_time': self._parse_duration(self._get_itemprop(recipe_elem, 'prepTime')),
                'cook_time': self._parse_duration(self._get_itemprop(recipe_elem, 'cookTime')),
                'servings': self._get_itemprop(recipe_elem, 'recipeYield'),
                'image': self._get_itemprop(recipe_elem, 'image'),
            }
            
            # Extract ingredients
            ingredients = recipe_elem.find_all(itemprop='recipeIngredient')
            recipe['ingredients'] = [ing.get_text(strip=True) for ing in ingredients]
            
            # Extract instructions
            instructions = recipe_elem.find_all(itemprop='recipeInstructions')
            recipe['instructions'] = [inst.get_text(strip=True) for inst in instructions]
            
            if recipe['title'] and (recipe['ingredients'] or recipe['instructions']):
                return recipe
                
        except Exception as e:
            logger.debug(f"Error extracting microdata: {e}")
        
        return None
    
    def _extract_html_patterns(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, Any]]:
        """Extract recipe using common HTML patterns."""
        try:
            recipe = {
                'title': '',
                'description': '',
                'url': url,
                'ingredients': [],
                'instructions': [],
                'prep_time': '',
                'cook_time': '',
                'servings': '',
            }
            
            # Try to find title
            title_selectors = [
                'h1.recipe-title', 'h1[class*="recipe"]', 'h1[class*="title"]',
                '.recipe-title', '.recipe-name', 'h1'
            ]
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    recipe['title'] = title_elem.get_text(strip=True)
                    break
            
            # Try to find ingredients
            ingredient_selectors = [
                '.ingredients', '.ingredient-list', '.recipe-ingredients',
                '[class*="ingredient"]', 'ul.ingredients', 'ol.ingredients'
            ]
            for selector in ingredient_selectors:
                ing_elem = soup.select_one(selector)
                if ing_elem:
                    items = ing_elem.find_all('li')
                    recipe['ingredients'] = [item.get_text(strip=True) for item in items]
                    if recipe['ingredients']:
                        break
            
            # Try to find instructions
            instruction_selectors = [
                '.instructions', '.directions', '.recipe-instructions',
                '.method', '[class*="instruction"]', '[class*="direction"]',
                'ol.instructions', 'ul.instructions'
            ]
            for selector in instruction_selectors:
                inst_elem = soup.select_one(selector)
                if inst_elem:
                    items = inst_elem.find_all(['li', 'p'])
                    recipe['instructions'] = [item.get_text(strip=True) for item in items if item.get_text(strip=True)]
                    if recipe['instructions']:
                        break
            
            # Try to find servings, times, etc.
            text_content = soup.get_text().lower()
            
            # Servings
            servings_match = re.search(r'servings?[:\s]+(\d+)', text_content, re.IGNORECASE)
            if servings_match:
                recipe['servings'] = servings_match.group(1)
            
            # Prep time
            prep_match = re.search(r'prep(?:aration)?\s*time[:\s]+(\d+)\s*(min|hour)', text_content, re.IGNORECASE)
            if prep_match:
                recipe['prep_time'] = f"{prep_match.group(1)} {prep_match.group(2)}"
            
            # Cook time
            cook_match = re.search(r'cook(?:ing)?\s*time[:\s]+(\d+)\s*(min|hour)', text_content, re.IGNORECASE)
            if cook_match:
                recipe['cook_time'] = f"{cook_match.group(1)} {cook_match.group(2)}"
            
            if recipe['title'] and (recipe['ingredients'] or recipe['instructions']):
                return recipe
                
        except Exception as e:
            logger.debug(f"Error extracting HTML patterns: {e}")
        
        return None
    
    def _get_nested_value(self, data: Dict, keys: List[str]) -> Optional[str]:
        """Get value from nested dictionary using multiple possible keys."""
        for key in keys:
            if key in data:
                value = data[key]
                if isinstance(value, dict) and 'name' in value:
                    return value['name']
                return str(value) if value else None
        return None
    
    def _get_itemprop(self, elem, prop: str) -> Optional[str]:
        """Get itemprop value from element."""
        item = elem.find(itemprop=prop)
        if item:
            if item.name in ['time', 'meta']:
                return item.get('content', '')
            return item.get_text(strip=True)
        return None
    
    def _parse_duration(self, duration: Optional[str]) -> Optional[str]:
        """Parse ISO 8601 duration to readable format."""
        if not duration:
            return None
        
        # ISO 8601 format: PT30M, PT1H30M, etc.
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?', duration)
        if match:
            hours = match.group(1) or '0'
            minutes = match.group(2) or '0'
            parts = []
            if int(hours) > 0:
                parts.append(f"{hours} hour{'s' if int(hours) != 1 else ''}")
            if int(minutes) > 0:
                parts.append(f"{minutes} min")
            return ' '.join(parts) if parts else None
        
        return duration
    
    def save_recipe_to_library(self, recipe_data: Dict[str, Any], source_url: str) -> Optional[RecipeEntry]:
        """Save scraped recipe to library."""
        try:
            # Create markdown file with recipe data
            content = self._format_recipe_markdown(recipe_data)
            
            # Generate hash from URL and title
            hash_input = f"{source_url}_{recipe_data.get('title', '')}"
            file_hash = hashlib.md5(hash_input.encode()).hexdigest()
            
            # Save to library
            library_file_path = self.library_path / f"{file_hash}.md"
            
            with open(library_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Saved recipe to: {library_file_path}")
            
            # Import to library system
            recipe_entry = self.library.analyze_and_import_file(library_file_path)
            
            if recipe_entry:
                # Update with URL source in database
                import sqlite3
                conn = sqlite3.connect(self.library.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE recipes 
                    SET file_path = ? 
                    WHERE id = ?
                """, (source_url, recipe_entry.id))
                conn.commit()
                conn.close()
                
                return recipe_entry
            
        except Exception as e:
            logger.error(f"Error saving recipe to library: {e}")
        
        return None
    
    def _format_recipe_markdown(self, recipe_data: Dict[str, Any]) -> str:
        """Format recipe data as markdown."""
        lines = []
        
        # Title
        if recipe_data.get('title'):
            lines.append(f"# {recipe_data['title']}\n")
        
        # Metadata
        if recipe_data.get('description'):
            lines.append(f"{recipe_data['description']}\n")
        
        lines.append("\n## Metadata\n")
        if recipe_data.get('servings'):
            lines.append(f"- **Servings:** {recipe_data['servings']}")
        if recipe_data.get('prep_time'):
            lines.append(f"- **Prep Time:** {recipe_data['prep_time']}")
        if recipe_data.get('cook_time'):
            lines.append(f"- **Cook Time:** {recipe_data['cook_time']}")
        if recipe_data.get('total_time'):
            lines.append(f"- **Total Time:** {recipe_data['total_time']}")
        if recipe_data.get('cuisine'):
            lines.append(f"- **Cuisine:** {recipe_data['cuisine']}")
        if recipe_data.get('category'):
            lines.append(f"- **Category:** {recipe_data['category']}")
        if recipe_data.get('url'):
            lines.append(f"- **Source URL:** {recipe_data['url']}")
        
        # Ingredients
        if recipe_data.get('ingredients'):
            lines.append("\n## Ingredients\n")
            for ingredient in recipe_data['ingredients']:
                lines.append(f"- {ingredient}")
        
        # Instructions
        if recipe_data.get('instructions'):
            lines.append("\n## Instructions\n")
            for i, instruction in enumerate(recipe_data['instructions'], 1):
                lines.append(f"{i}. {instruction}")
        
        return '\n'.join(lines)
    
    def scrape_and_import(self, url: str) -> Optional[RecipeEntry]:
        """Scrape recipe from URL and import to library."""
        recipe_data = self.scrape_recipe(url)
        
        if recipe_data:
            return self.save_recipe_to_library(recipe_data, url)
        
        return None
    
    def scrape_multiple(self, urls: List[str]) -> Dict[str, Any]:
        """Scrape multiple recipes from URLs."""
        results = {
            'success': [],
            'failed': [],
            'total': len(urls)
        }
        
        for url in urls:
            try:
                recipe_entry = self.scrape_and_import(url)
                if recipe_entry:
                    results['success'].append({
                        'url': url,
                        'title': recipe_entry.title,
                        'id': recipe_entry.id
                    })
                else:
                    results['failed'].append({
                        'url': url,
                        'reason': 'Could not extract recipe data'
                    })
            except Exception as e:
                results['failed'].append({
                    'url': url,
                    'reason': str(e)
                })
        
        return results


def main():
    """CLI interface for web recipe scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape recipes from websites')
    parser.add_argument('url', nargs='?', help='URL of recipe to scrape')
    parser.add_argument('--file', '-f', help='File containing URLs (one per line)')
    parser.add_argument('--library', '-l', default='recipe_library', help='Library path')
    
    args = parser.parse_args()
    
    scraper = WebRecipeScraper(library_path=args.library)
    
    if args.file:
        # Read URLs from file
        urls = []
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"\n📥 Scraping {len(urls)} recipes from file...\n")
        results = scraper.scrape_multiple(urls)
        
        print(f"\n✅ Successfully scraped: {len(results['success'])}")
        print(f"❌ Failed: {len(results['failed'])}")
        
        if results['success']:
            print("\n📋 Successfully scraped recipes:")
            for item in results['success']:
                print(f"  • {item['title']} - {item['url']}")
        
        if results['failed']:
            print("\n⚠️  Failed recipes:")
            for item in results['failed']:
                print(f"  • {item['url']} - {item['reason']}")
    
    elif args.url:
        # Single URL
        print(f"\n📥 Scraping recipe from: {args.url}\n")
        recipe_entry = scraper.scrape_and_import(args.url)
        
        if recipe_entry:
            print(f"✅ Successfully scraped and imported: {recipe_entry.title}")
            print(f"   ID: {recipe_entry.id}")
            print(f"   Library path: {recipe_entry.library_path}")
        else:
            print("❌ Failed to scrape recipe from URL")
            sys.exit(1)
    
    else:
        # Interactive mode
        print("\n🌐 Web Recipe Scraper")
        print("=" * 50)
        print("\nEnter recipe URLs (one per line, empty line to finish):\n")
        
        urls = []
        while True:
            url = input("URL (or press Enter to finish): ").strip()
            if not url:
                break
            urls.append(url)
        
        if urls:
            print(f"\n📥 Scraping {len(urls)} recipes...\n")
            results = scraper.scrape_multiple(urls)
            
            print(f"\n✅ Successfully scraped: {len(results['success'])}")
            print(f"❌ Failed: {len(results['failed'])}")
        else:
            print("No URLs provided.")


if __name__ == '__main__':
    main()

