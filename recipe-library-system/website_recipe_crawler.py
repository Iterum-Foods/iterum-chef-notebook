#!/usr/bin/env python3
"""
Website Recipe Crawler
Crawls an entire website to find all recipe pages, extracts recipes, and exports to JSON or PDF
"""

import sys
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from datetime import datetime
from urllib.parse import urlparse, urljoin, urlunparse
from urllib.robotparser import RobotFileParser
import logging

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("WARNING: PDF export not available. Install reportlab: pip install reportlab")

# Import the web scraper
sys.path.insert(0, str(Path(__file__).parent))
from web_recipe_scraper import WebRecipeScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteRecipeCrawler:
    """Crawl a website to find and extract all recipes."""
    
    def __init__(self, base_url: str, max_pages: int = 100, delay: float = 1.0):
        """
        Initialize the crawler.
        
        Args:
            base_url: Base URL of the website to crawl
            max_pages: Maximum number of pages to crawl
            delay: Delay between requests (seconds)
        """
        self.base_url = base_url.rstrip('/')
        self.parsed_base = urlparse(self.base_url)
        self.max_pages = max_pages
        self.delay = delay
        
        # Track visited URLs
        self.visited_urls: Set[str] = set()
        self.recipe_urls: List[str] = []
        self.failed_urls: List[Dict[str, str]] = []
        
        # User agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Recipe indicators in URLs and content
        self.recipe_url_patterns = [
            r'/recipe',
            r'/recipes',
            r'/dish',
            r'/dish/',
            r'/cooking',
            r'/food',
            r'/meal',
        ]
        
        self.recipe_content_indicators = [
            'recipe',
            'ingredient',
            'instruction',
            'prep time',
            'cook time',
            'servings',
            'yield',
        ]
        
        # Initialize scraper
        self.scraper = WebRecipeScraper()
        
        # Check robots.txt
        self.robots_parser = self._check_robots_txt()
    
    def _check_robots_txt(self) -> Optional[RobotFileParser]:
        """Check and parse robots.txt if available."""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp
        except Exception as e:
            logger.debug(f"Could not parse robots.txt: {e}")
            return None
    
    def _is_same_domain(self, url: str) -> bool:
        """Check if URL is from the same domain."""
        try:
            parsed = urlparse(url)
            return parsed.netloc == self.parsed_base.netloc
        except:
            return False
    
    def _is_recipe_url(self, url: str) -> bool:
        """Check if URL likely contains a recipe."""
        url_lower = url.lower()
        for pattern in self.recipe_url_patterns:
            if re.search(pattern, url_lower):
                return True
        return False
    
    def _is_recipe_page(self, soup: BeautifulSoup, url: str) -> bool:
        """Check if page content indicates it's a recipe."""
        # Check for Schema.org Recipe markup
        if soup.find('script', type='application/ld+json'):
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        for item in data:
                            if item.get('@type') == 'Recipe' or 'Recipe' in item.get('@type', []):
                                return True
                    elif isinstance(data, dict):
                        if data.get('@type') == 'Recipe' or 'Recipe' in data.get('@type', []):
                            return True
                except:
                    continue
        
        # Check for microdata
        if soup.find(itemtype=re.compile(r'.*Recipe')):
            return True
        
        # Check for recipe indicators in content
        text_content = soup.get_text().lower()
        indicator_count = sum(1 for indicator in self.recipe_content_indicators if indicator in text_content)
        
        # If multiple indicators found, likely a recipe
        if indicator_count >= 3:
            return True
        
        # Check for common recipe HTML patterns
        if (soup.find(class_=re.compile(r'ingredient', re.I)) and 
            soup.find(class_=re.compile(r'instruction|direction', re.I))):
            return True
        
        return False
    
    def _extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract all links from a page."""
        links = []
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(current_url, href)
            # Remove fragments
            parsed = urlparse(absolute_url)
            clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))
            
            # Only include same-domain URLs
            if self._is_same_domain(clean_url):
                links.append(clean_url)
        
        return links
    
    def crawl(self) -> Dict[str, Any]:
        """
        Crawl the website to find all recipe pages.
        
        Returns:
            Dictionary with crawl results
        """
        logger.info(f"Starting crawl of {self.base_url}")
        logger.info(f"Max pages: {self.max_pages}, Delay: {self.delay}s")
        
        # Start with base URL
        urls_to_visit = [self.base_url]
        
        while urls_to_visit and len(self.visited_urls) < self.max_pages:
            current_url = urls_to_visit.pop(0)
            
            # Skip if already visited
            if current_url in self.visited_urls:
                continue
            
            # Check robots.txt
            if self.robots_parser and not self.robots_parser.can_fetch(self.headers['User-Agent'], current_url):
                logger.debug(f"Skipping {current_url} (blocked by robots.txt)")
                continue
            
            # Mark as visited
            self.visited_urls.add(current_url)
            
            try:
                logger.info(f"Crawling: {current_url} ({len(self.visited_urls)}/{self.max_pages})")
                
                # Fetch page
                response = requests.get(current_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check if this is a recipe page
                if self._is_recipe_page(soup, current_url):
                    logger.info(f"  ✓ Found recipe: {current_url}")
                    self.recipe_urls.append(current_url)
                else:
                    # Extract links to continue crawling
                    links = self._extract_links(soup, current_url)
                    
                    # Prioritize recipe URLs
                    recipe_links = [link for link in links if self._is_recipe_url(link)]
                    other_links = [link for link in links if link not in recipe_links]
                    
                    # Add recipe links first, then others
                    for link in recipe_links + other_links:
                        if link not in self.visited_urls and link not in urls_to_visit:
                            urls_to_visit.append(link)
                
                # Respect delay
                if self.delay > 0:
                    time.sleep(self.delay)
                    
            except requests.RequestException as e:
                logger.warning(f"  ✗ Error fetching {current_url}: {e}")
                self.failed_urls.append({'url': current_url, 'error': str(e)})
            except Exception as e:
                logger.error(f"  ✗ Error processing {current_url}: {e}")
                self.failed_urls.append({'url': current_url, 'error': str(e)})
        
        logger.info(f"\nCrawl complete!")
        logger.info(f"  Visited: {len(self.visited_urls)} pages")
        logger.info(f"  Found: {len(self.recipe_urls)} recipe pages")
        logger.info(f"  Failed: {len(self.failed_urls)} pages")
        
        return {
            'base_url': self.base_url,
            'total_pages_visited': len(self.visited_urls),
            'recipes_found': len(self.recipe_urls),
            'failed_pages': len(self.failed_urls),
            'recipe_urls': self.recipe_urls,
            'failed_urls': self.failed_urls
        }
    
    def scrape_all_recipes(self) -> List[Dict[str, Any]]:
        """Scrape all found recipe URLs."""
        logger.info(f"\nScraping {len(self.recipe_urls)} recipes...")
        
        recipes = []
        for i, url in enumerate(self.recipe_urls, 1):
            logger.info(f"Scraping {i}/{len(self.recipe_urls)}: {url}")
            
            recipe_data = self.scraper.scrape_recipe(url)
            if recipe_data:
                recipe_data['source_url'] = url
                recipe_data['scraped_date'] = datetime.now().isoformat()
                recipes.append(recipe_data)
                logger.info(f"  ✓ Success: {recipe_data.get('title', 'Unknown')}")
            else:
                logger.warning(f"  ✗ Failed to scrape: {url}")
                self.failed_urls.append({'url': url, 'error': 'Could not extract recipe data'})
            
            # Respect delay
            if self.delay > 0:
                time.sleep(self.delay)
        
        logger.info(f"\nScraping complete!")
        logger.info(f"  Successfully scraped: {len(recipes)} recipes")
        logger.info(f"  Failed: {len(self.recipe_urls) - len(recipes)} recipes")
        
        return recipes
    
    def export_to_json(self, recipes: List[Dict[str, Any]], output_file: str = None) -> str:
        """Export recipes to JSON file."""
        if output_file is None:
            domain = self.parsed_base.netloc.replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"recipes_{domain}_{timestamp}.json"
        
        output_path = Path(output_file)
        
        export_data = {
            'export_info': {
                'base_url': self.base_url,
                'export_date': datetime.now().isoformat(),
                'total_recipes': len(recipes),
                'crawler_version': '1.0'
            },
            'recipes': recipes
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(recipes)} recipes to: {output_path}")
        return str(output_path)
    
    def export_to_pdf(self, recipes: List[Dict[str, Any]], output_file: str = None) -> Optional[str]:
        """Export recipes to PDF file."""
        if not PDF_AVAILABLE:
            logger.error("PDF export not available. Install reportlab: pip install reportlab")
            return None
        
        if output_file is None:
            domain = self.parsed_base.netloc.replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"recipes_{domain}_{timestamp}.pdf"
        
        output_path = Path(output_file)
        
        # Create PDF
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2c3e50',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            textColor='#34495e',
            spaceAfter=12,
            spaceBefore=20
        )
        normal_style = styles['Normal']
        
        # Title page
        story.append(Paragraph("Recipe Collection", title_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"From: {self.base_url}", styles['Heading3']))
        story.append(Paragraph(f"Exported: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
        story.append(Paragraph(f"Total Recipes: {len(recipes)}", normal_style))
        story.append(PageBreak())
        
        # Add each recipe
        for i, recipe in enumerate(recipes, 1):
            # Recipe title
            title = recipe.get('title', f'Recipe {i}')
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata
            if recipe.get('description'):
                story.append(Paragraph(f"<i>{recipe['description']}</i>", normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            meta_parts = []
            if recipe.get('servings'):
                meta_parts.append(f"<b>Servings:</b> {recipe['servings']}")
            if recipe.get('prep_time'):
                meta_parts.append(f"<b>Prep Time:</b> {recipe['prep_time']}")
            if recipe.get('cook_time'):
                meta_parts.append(f"<b>Cook Time:</b> {recipe['cook_time']}")
            if recipe.get('cuisine'):
                meta_parts.append(f"<b>Cuisine:</b> {recipe['cuisine']}")
            
            if meta_parts:
                story.append(Paragraph(" | ".join(meta_parts), normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            # Ingredients
            if recipe.get('ingredients'):
                story.append(Paragraph("Ingredients", heading_style))
                for ingredient in recipe['ingredients']:
                    story.append(Paragraph(f"• {ingredient}", normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            # Instructions
            if recipe.get('instructions'):
                story.append(Paragraph("Instructions", heading_style))
                for j, instruction in enumerate(recipe['instructions'], 1):
                    story.append(Paragraph(f"{j}. {instruction}", normal_style))
                story.append(Spacer(1, 0.2*inch))
            
            # Source URL
            if recipe.get('source_url'):
                story.append(Paragraph(f"<i>Source: {recipe['source_url']}</i>", 
                                     ParagraphStyle('Source', parent=normal_style, fontSize=8, textColor='#7f8c8d')))
            
            # Page break (except for last recipe)
            if i < len(recipes):
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        logger.info(f"Exported {len(recipes)} recipes to PDF: {output_path}")
        return str(output_path)
    
    def crawl_and_export(self, format: str = 'json', output_file: str = None) -> Dict[str, Any]:
        """
        Complete workflow: crawl, scrape, and export.
        
        Args:
            format: Export format ('json' or 'pdf')
            output_file: Output file path (optional)
        
        Returns:
            Dictionary with results
        """
        # Step 1: Crawl website
        crawl_results = self.crawl()
        
        if not self.recipe_urls:
            logger.warning("No recipes found on website!")
            return {
                'success': False,
                'error': 'No recipes found',
                'crawl_results': crawl_results
            }
        
        # Step 2: Scrape all recipes
        recipes = self.scrape_all_recipes()
        
        if not recipes:
            logger.warning("No recipes successfully scraped!")
            return {
                'success': False,
                'error': 'No recipes successfully scraped',
                'crawl_results': crawl_results,
                'recipes': []
            }
        
        # Step 3: Export
        if format.lower() == 'json':
            output_path = self.export_to_json(recipes, output_file)
        elif format.lower() == 'pdf':
            output_path = self.export_to_pdf(recipes, output_file)
            if not output_path:
                return {
                    'success': False,
                    'error': 'PDF export failed (reportlab not installed)',
                    'crawl_results': crawl_results,
                    'recipes': recipes
                }
        else:
            return {
                'success': False,
                'error': f'Unknown format: {format}',
                'crawl_results': crawl_results,
                'recipes': recipes
            }
        
        return {
            'success': True,
            'output_file': output_path,
            'crawl_results': crawl_results,
            'recipes_count': len(recipes),
            'format': format
        }


def main():
    """CLI interface for website crawler."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Crawl website and extract all recipes')
    parser.add_argument('url', help='Base URL of website to crawl')
    parser.add_argument('--format', '-f', choices=['json', 'pdf'], default='json',
                       help='Export format (default: json)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--max-pages', '-m', type=int, default=100,
                       help='Maximum pages to crawl (default: 100)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--crawl-only', action='store_true',
                       help='Only crawl, do not scrape recipes')
    
    args = parser.parse_args()
    
    print(f"\n🌐 Website Recipe Crawler")
    print("=" * 60)
    print(f"URL: {args.url}")
    print(f"Max pages: {args.max_pages}")
    print(f"Delay: {args.delay}s")
    print(f"Format: {args.format}")
    print("=" * 60 + "\n")
    
    crawler = WebsiteRecipeCrawler(
        base_url=args.url,
        max_pages=args.max_pages,
        delay=args.delay
    )
    
    if args.crawl_only:
        results = crawler.crawl()
        print(f"\n✓ Found {len(crawler.recipe_urls)} recipe pages")
        print("\nRecipe URLs:")
        for url in crawler.recipe_urls:
            print(f"  • {url}")
    else:
        results = crawler.crawl_and_export(format=args.format, output_file=args.output)
        
        if results['success']:
            print(f"\n✅ Success!")
            print(f"   Recipes found: {results['crawl_results']['recipes_found']}")
            print(f"   Recipes scraped: {results['recipes_count']}")
            print(f"   Output file: {results['output_file']}")
        else:
            print(f"\n❌ Error: {results.get('error', 'Unknown error')}")
            sys.exit(1)


if __name__ == '__main__':
    main()

