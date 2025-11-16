#!/usr/bin/env python3
"""
Ingredient Web Scraper
Scrapes ingredient information from product/vendor websites
Extracts name, price, description, storage notes, and other metadata
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import urlparse
import logging

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    print("Warning: requests and beautifulsoup4 required for web scraping")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngredientWebScraper:
    """Scrape ingredient information from product/vendor websites."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_ingredient_info(self, url: str) -> Dict[str, Any]:
        """
        Scrape ingredient information from a product/vendor URL.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with extracted ingredient information
        """
        if not WEB_SCRAPING_AVAILABLE:
            return {
                'success': False,
                'error': 'Web scraping libraries not available. Install requests and beautifulsoup4.'
            }
        
        try:
            logger.info(f"Scraping ingredient info from: {url}")
            
            # Fetch page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract information
            info = {
                'success': True,
                'source_url': url,
                'scraped_date': datetime.now().isoformat()
            }
            
            # Try different extraction methods based on site structure
            domain = urlparse(url).netloc.lower()
            
            # Generic extraction (works for most sites)
            info.update(self._extract_generic(soup))
            
            # Site-specific extraction
            if 'zigantetartufi.com' in domain:
                info.update(self._extract_zigante(soup))
            elif 'shopify' in domain or 'bigcommerce' in domain:
                info.update(self._extract_shopify(soup))
            elif 'woocommerce' in domain or 'wordpress' in domain:
                info.update(self._extract_woocommerce(soup))
            
            # Clean and validate extracted data
            info = self._clean_extracted_data(info)
            
            return info
            
        except requests.RequestException as e:
            logger.error(f"Error fetching URL: {e}")
            return {
                'success': False,
                'error': f'Failed to fetch URL: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Error scraping ingredient: {e}")
            return {
                'success': False,
                'error': f'Scraping error: {str(e)}'
            }
    
    def _extract_generic(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Generic extraction that works for most websites."""
        info = {}
        
        # Extract title/name
        title = None
        for selector in ['h1', '.product-title', '.product-name', '[itemprop="name"]', 'title']:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                break
        if title:
            info['name'] = title
        
        # Extract price
        price = None
        price_text = None
        for selector in [
            '.price', '.product-price', '[itemprop="price"]', 
            '.price-current', '.sale-price', '.regular-price'
        ]:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Extract number
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                if price_match:
                    try:
                        price = float(price_match.group())
                        info['price'] = price
                        info['price_text'] = price_text
                        break
                    except:
                        pass
        
        # Extract description
        description = None
        for selector in [
            '.product-description', '.description', '[itemprop="description"]',
            '.product-details', '.product-info'
        ]:
            element = soup.select_one(selector)
            if element:
                description = element.get_text(strip=True)
                if len(description) > 50:  # Only use substantial descriptions
                    info['description'] = description
                    break
        
        # Extract unit/weight
        unit = None
        for text in soup.stripped_strings:
            # Look for weight/unit patterns
            unit_match = re.search(r'(\d+)\s*(g|kg|oz|lb|gram|kilogram|ounce|pound)', text, re.IGNORECASE)
            if unit_match:
                unit = unit_match.group(2).lower()
                if unit in ['gram', 'grams']:
                    unit = 'g'
                elif unit in ['kilogram', 'kilograms']:
                    unit = 'kg'
                elif unit in ['ounce', 'ounces']:
                    unit = 'oz'
                elif unit in ['pound', 'pounds']:
                    unit = 'lb'
                info['unit'] = unit
                info['unit_size'] = unit_match.group(1)
                break
        
        # Extract storage/preservation info
        storage_keywords = ['store', 'storage', 'preserve', 'keep', 'refrigerate', 'freeze', 'shelf']
        for element in soup.find_all(['p', 'div', 'li']):
            text = element.get_text(strip=True).lower()
            if any(keyword in text for keyword in storage_keywords):
                if len(text) > 20 and len(text) < 500:  # Reasonable length
                    if 'storage_notes' not in info:
                        info['storage_notes'] = []
                    info['storage_notes'].append(element.get_text(strip=True))
        
        if 'storage_notes' in info:
            info['storage_notes'] = ' '.join(info['storage_notes'][:3])  # Limit to 3 notes
        
        # Extract serving/usage suggestions
        usage_keywords = ['serve', 'serving', 'use', 'ideal', 'best', 'recommend']
        usage_notes = []
        for element in soup.find_all(['p', 'div', 'li']):
            text = element.get_text(strip=True).lower()
            if any(keyword in text for keyword in usage_keywords):
                if len(text) > 20 and len(text) < 300:
                    usage_notes.append(element.get_text(strip=True))
        
        if usage_notes:
            info['usage_notes'] = ' '.join(usage_notes[:2])
        
        # Extract origin/season info
        origin_keywords = ['origin', 'season', 'from', 'harvest', 'grown']
        for element in soup.find_all(['p', 'div', 'strong']):
            text = element.get_text(strip=True)
            if any(keyword in text.lower() for keyword in origin_keywords):
                if len(text) > 10 and len(text) < 200:
                    if 'origin' not in info:
                        info['origin'] = text
                    break
        
        return info
    
    def _extract_zigante(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract information from Zigante Tartufi website."""
        info = {}
        
        # Product name
        title_elem = soup.select_one('h1')
        if title_elem:
            info['name'] = title_elem.get_text(strip=True)
        
        # Price (Zigante uses specific selectors)
        price_elem = soup.select_one('.price, .sale-price, [class*="price"]')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'€?([\d,]+\.?\d*)', price_text.replace(',', ''))
            if price_match:
                try:
                    info['price'] = float(price_match.group(1))
                    info['price_text'] = price_text
                    info['currency'] = 'EUR'
                except:
                    pass
        
        # Size/Unit
        size_elem = soup.select_one('[class*="size"], [class*="variant"], [class*="weight"]')
        if size_elem:
            size_text = size_elem.get_text(strip=True)
            unit_match = re.search(r'(\d+)\s*(g|kg|oz|lb)', size_text, re.IGNORECASE)
            if unit_match:
                info['unit'] = unit_match.group(2).lower()
                info['unit_size'] = unit_match.group(1)
        
        # Description sections
        desc_sections = soup.select('h3, h4, strong')
        for section in desc_sections:
            text = section.get_text(strip=True)
            
            # Season/Origin
            if 'season' in text.lower() or 'origin' in text.lower():
                next_p = section.find_next('p')
                if next_p:
                    info['origin'] = next_p.get_text(strip=True)
            
            # Storage/Preserving
            if 'preserv' in text.lower() or 'stor' in text.lower():
                storage_text = []
                for sibling in section.find_next_siblings(['p', 'li', 'ul']):
                    if sibling.name == 'ul':
                        for li in sibling.find_all('li'):
                            storage_text.append(li.get_text(strip=True))
                    else:
                        storage_text.append(sibling.get_text(strip=True))
                    if len(storage_text) >= 3:
                        break
                if storage_text:
                    info['storage_notes'] = ' '.join(storage_text[:3])
            
            # Serving suggestions
            if 'serv' in text.lower() or 'us' in text.lower():
                serving_text = []
                for sibling in section.find_next_siblings(['p', 'li', 'ul']):
                    if sibling.name == 'ul':
                        for li in sibling.find_all('li'):
                            serving_text.append(li.get_text(strip=True))
                    else:
                        serving_text.append(sibling.get_text(strip=True))
                    if len(serving_text) >= 2:
                        break
                if serving_text:
                    info['usage_notes'] = ' '.join(serving_text[:2])
        
        # Extract all description text
        desc_elem = soup.select_one('[class*="description"], [class*="product-details"], main, article')
        if desc_elem:
            full_text = desc_elem.get_text(separator=' ', strip=True)
            if len(full_text) > 100:
                info['description'] = full_text[:1000]  # Limit length
        
        return info
    
    def _extract_shopify(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract information from Shopify-based stores."""
        info = {}
        
        # Product name
        title = soup.select_one('h1.product-title, h1[itemprop="name"]')
        if title:
            info['name'] = title.get_text(strip=True)
        
        # Price
        price = soup.select_one('.price, [itemprop="price"]')
        if price:
            price_text = price.get_text(strip=True)
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
            if price_match:
                try:
                    info['price'] = float(price_match.group().replace(',', ''))
                except:
                    pass
        
        # Description
        desc = soup.select_one('.product-description, [itemprop="description"]')
        if desc:
            info['description'] = desc.get_text(strip=True)
        
        return info
    
    def _extract_woocommerce(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract information from WooCommerce stores."""
        info = {}
        
        # Similar to Shopify
        title = soup.select_one('h1.product_title')
        if title:
            info['name'] = title.get_text(strip=True)
        
        price = soup.select_one('.price, .woocommerce-Price-amount')
        if price:
            price_text = price.get_text(strip=True)
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
            if price_match:
                try:
                    info['price'] = float(price_match.group().replace(',', ''))
                except:
                    pass
        
        return info
    
    def _clean_extracted_data(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize extracted data."""
        cleaned = {}
        
        # Name
        if 'name' in info:
            cleaned['name'] = info['name'].strip()
        
        # Price - convert to per unit if needed
        if 'price' in info:
            cleaned['typical_ap_cost'] = info['price']
            if 'unit' in info:
                cleaned['cost_unit'] = info['unit']
            elif 'unit_size' in info:
                # Try to infer unit from size
                size = info.get('unit_size', '')
                if 'g' in str(size).lower() or size and int(size) < 1000:
                    cleaned['cost_unit'] = 'g'
                else:
                    cleaned['cost_unit'] = 'kg'
        
        # Description
        if 'description' in info:
            desc = info['description'].strip()
            if len(desc) > 50:
                cleaned['notes'] = desc[:500]  # Limit to 500 chars
        
        # Storage notes
        if 'storage_notes' in info:
            cleaned['storage_notes'] = info['storage_notes'].strip()
        
        # Usage notes - add to notes
        if 'usage_notes' in info:
            usage = info['usage_notes'].strip()
            if 'notes' in cleaned:
                cleaned['notes'] += f"\n\nUsage: {usage}"
            else:
                cleaned['notes'] = f"Usage: {usage}"
        
        # Origin - add to notes
        if 'origin' in info:
            origin = info['origin'].strip()
            if 'notes' in cleaned:
                cleaned['notes'] = f"Origin: {origin}\n\n{cleaned['notes']}"
            else:
                cleaned['notes'] = f"Origin: {origin}"
        
        # Unit
        if 'unit' in info:
            cleaned['default_unit'] = info['unit']
        
        # Source URL
        if 'source_url' in info:
            cleaned['source_url'] = info['source_url']
        
        # Keep raw data for reference
        cleaned['_raw_scraped_data'] = info
        
        return cleaned


def main():
    """CLI interface for ingredient scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape ingredient information from URL')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    scraper = IngredientWebScraper()
    result = scraper.scrape_ingredient_info(args.url)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get('success'):
            print("\n✅ Scraped Ingredient Information:\n")
            print(f"Name: {result.get('name', 'N/A')}")
            print(f"Price: {result.get('typical_ap_cost', 'N/A')} {result.get('cost_unit', '')}")
            print(f"Unit: {result.get('default_unit', 'N/A')}")
            print(f"Storage: {result.get('storage_notes', 'N/A')}")
            print(f"Notes: {result.get('notes', 'N/A')[:200]}...")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == '__main__':
    main()

