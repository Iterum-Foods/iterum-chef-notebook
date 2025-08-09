"""
Menu Parser Service
Extracts structured menu items with titles, descriptions, and prices from text
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class MenuItem:
    """Represents a single menu item"""
    title: str
    description: str = ""
    price: Optional[float] = None
    price_text: str = ""
    category: str = ""
    dietary_tags: List[str] = None
    spice_level: Optional[str] = None
    
    def __post_init__(self):
        if self.dietary_tags is None:
            self.dietary_tags = []

@dataclass
class MenuSection:
    """Represents a menu section/category"""
    name: str
    items: List[MenuItem]
    description: str = ""

class MenuParser:
    """Parses extracted menu text into structured menu items"""
    
    def __init__(self):
        # Price patterns (various formats)
        self.price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',  # $12.50, $12
            r'(\d+(?:\.\d{2})?)\s*(?:dollars?|USD|\$)',  # 12.50 dollars, 12 USD
            r'(\d+(?:\.\d{2})?)\s*(?:£|pounds?)',  # 12.50 pounds, £12
            r'(\d+(?:\.\d{2})?)\s*(?:€|euros?)',  # 12.50 euros, €12
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:won|₩)',  # Korean won
            r'(\d+(?:\.\d{2})?)\s*(?:yen|¥)',  # Japanese yen
        ]
        
        # Section headers
        self.section_patterns = [
            r'^(APPETIZERS?|STARTERS?|SMALL\s+PLATES?)',
            r'^(SOUPS?|SALADS?)',
            r'^(MAIN\s+COURSES?|ENTREES?|MAINS?)',
            r'^(DESSERTS?|SWEETS?)',
            r'^(BEVERAGES?|DRINKS?)',
            r'^(SIDES?|SIDE\s+DISHES?)',
            r'^(SPECIALS?|CHEF\'?S?\s+SPECIALS?)',
            r'^(LUNCH|DINNER|BREAKFAST|BRUNCH)',
            r'^([A-Z\s&]+)(?:\s*---|\s*–|\s*—|\s*\.\.\.).*$',  # Generic section headers
        ]
        
        # Dietary indicators
        self.dietary_patterns = {
            'vegetarian': r'\b(?:vegetarian|veggie|V\b)',
            'vegan': r'\b(?:vegan|VG\b)',
            'gluten_free': r'\b(?:gluten[\s-]?free|GF\b)',
            'dairy_free': r'\b(?:dairy[\s-]?free|DF\b)',
            'nut_free': r'\b(?:nut[\s-]?free|NF\b)',
            'spicy': r'\b(?:spicy|hot|🌶|♨)',
            'signature': r'\b(?:signature|chef\'?s?\s+special|house\s+special)',
            'popular': r'\b(?:popular|bestseller|customer\s+favorite)',
        }
        
        # Spice level indicators
        self.spice_patterns = {
            'mild': r'\b(?:mild|gentle|light\s+spice)',
            'medium': r'\b(?:medium|moderate\s+spice)',
            'hot': r'\b(?:hot|spicy|very\s+spicy)',
            'extra_hot': r'\b(?:extra\s+hot|extremely\s+spicy|火)'
        }
    
    def parse_menu_text(self, text: str) -> Dict[str, Any]:
        """
        Parse menu text into structured menu data
        
        Args:
            text: Raw menu text
            
        Returns:
            Dictionary with parsed menu structure
        """
        try:
            # Clean and normalize text
            cleaned_text = self.clean_text(text)
            
            # Split into sections
            sections = self.extract_sections(cleaned_text)
            
            # Parse each section
            parsed_sections = []
            total_items = 0
            
            for section_name, section_text in sections:
                menu_items = self.extract_menu_items(section_text)
                if menu_items:
                    parsed_sections.append(MenuSection(
                        name=section_name,
                        items=menu_items
                    ))
                    total_items += len(menu_items)
            
            # If no clear sections found, treat as one section
            if not parsed_sections:
                all_items = self.extract_menu_items(cleaned_text)
                if all_items:
                    parsed_sections.append(MenuSection(
                        name="Menu Items",
                        items=all_items
                    ))
                    total_items = len(all_items)
            
            # Create summary
            summary = self.create_menu_summary(parsed_sections)
            
            return {
                'success': True,
                'sections': [self.section_to_dict(section) for section in parsed_sections],
                'summary': summary,
                'total_items': total_items,
                'total_sections': len(parsed_sections),
                'parsing_info': {
                    'method': 'menu_text_parsing',
                    'confidence': self.calculate_confidence(parsed_sections, text),
                    'status': 'completed'
                }
            }
            
        except Exception as e:
            logger.error(f"Menu parsing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'sections': [],
                'summary': {},
                'total_items': 0,
                'parsing_info': {'status': 'failed', 'method': 'menu_text_parsing'}
            }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize menu text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Fix common OCR errors
        text = text.replace('|', 'I')  # Pipe to I
        text = text.replace('0', 'O')  # Zero to O in some contexts
        
        return text.strip()
    
    def extract_sections(self, text: str) -> List[Tuple[str, str]]:
        """Extract menu sections from text"""
        sections = []
        lines = text.split('\n')
        current_section = "Menu Items"
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            is_section_header = False
            for pattern in self.section_patterns:
                if re.match(pattern, line.upper()):
                    # Save previous section
                    if current_content:
                        sections.append((current_section, '\n'.join(current_content)))
                    
                    # Start new section
                    current_section = self.normalize_section_name(line)
                    current_content = []
                    is_section_header = True
                    break
            
            if not is_section_header:
                current_content.append(line)
        
        # Add final section
        if current_content:
            sections.append((current_section, '\n'.join(current_content)))
        
        return sections
    
    def normalize_section_name(self, section_name: str) -> str:
        """Normalize section names"""
        name = section_name.strip().title()
        name = re.sub(r'[^\w\s]', '', name)  # Remove special characters
        return name
    
    def extract_menu_items(self, text: str) -> List[MenuItem]:
        """Extract individual menu items from section text"""
        items = []
        lines = text.split('\n')
        current_item = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this looks like a menu item (has price or title format)
            price_info = self.extract_price(line)
            
            if price_info['has_price'] or self.looks_like_title(line):
                # Save previous item
                if current_item:
                    items.append(current_item)
                
                # Start new item
                title = self.extract_title(line)
                current_item = MenuItem(
                    title=title,
                    description="",
                    price=price_info['price'],
                    price_text=price_info['text']
                )
                
                # Extract any description from the same line
                remaining_text = line.replace(price_info['text'], '').replace(title, '').strip()
                if remaining_text:
                    current_item.description = remaining_text
                
                # Extract dietary tags and spice level
                current_item.dietary_tags = self.extract_dietary_tags(line)
                current_item.spice_level = self.extract_spice_level(line)
                
            else:
                # This line is likely a description continuation
                if current_item:
                    if current_item.description:
                        current_item.description += " " + line
                    else:
                        current_item.description = line
        
        # Add final item
        if current_item:
            items.append(current_item)
        
        return items
    
    def extract_price(self, text: str) -> Dict[str, Any]:
        """Extract price information from text"""
        for pattern in self.price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    price_str = match.group(1) if match.groups() else match.group(0).replace('$', '')
                    price_value = float(price_str.replace(',', ''))
                    return {
                        'has_price': True,
                        'price': price_value,
                        'text': match.group(0)
                    }
                except ValueError:
                    continue
        
        return {'has_price': False, 'price': None, 'text': ''}
    
    def looks_like_title(self, line: str) -> bool:
        """Check if line looks like a menu item title"""
        # All caps, title case, or specific formatting
        if line.isupper() and len(line) > 3:
            return True
        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', line):
            return True
        if re.match(r'^\d+\.?\s+[A-Z]', line):  # Numbered items
            return True
        return False
    
    def extract_title(self, line: str) -> str:
        """Extract title from menu item line"""
        # Remove price first
        price_info = self.extract_price(line)
        line_without_price = line.replace(price_info['text'], '').strip()
        
        # Remove dietary indicators
        for pattern in self.dietary_patterns.values():
            line_without_price = re.sub(pattern, '', line_without_price, flags=re.IGNORECASE)
        
        # Take first part as title (until description markers)
        title_match = re.match(r'^([^.!?-]+?)(?:\s*[-–—]\s*|\.{2,}|\s{3,})', line_without_price)
        if title_match:
            return title_match.group(1).strip()
        
        # Fallback: take first N words
        words = line_without_price.split()
        if len(words) > 6:
            return ' '.join(words[:6]).strip()
        
        return line_without_price.strip()
    
    def extract_dietary_tags(self, text: str) -> List[str]:
        """Extract dietary restriction tags"""
        tags = []
        for tag_name, pattern in self.dietary_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(tag_name)
        return tags
    
    def extract_spice_level(self, text: str) -> Optional[str]:
        """Extract spice level information"""
        for level, pattern in self.spice_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return level
        return None
    
    def calculate_confidence(self, sections: List[MenuSection], original_text: str) -> float:
        """Calculate parsing confidence score"""
        total_items = sum(len(section.items) for section in sections)
        
        if total_items == 0:
            return 0.0
        
        # Factors that increase confidence
        confidence_factors = []
        
        # Number of items found
        confidence_factors.append(min(total_items / 10, 1.0) * 30)
        
        # Prices found
        items_with_prices = sum(1 for section in sections for item in section.items if item.price)
        price_ratio = items_with_prices / total_items if total_items > 0 else 0
        confidence_factors.append(price_ratio * 40)
        
        # Menu structure (sections)
        if len(sections) > 1:
            confidence_factors.append(20)
        
        # Dietary tags found
        items_with_tags = sum(1 for section in sections for item in section.items if item.dietary_tags)
        tag_ratio = items_with_tags / total_items if total_items > 0 else 0
        confidence_factors.append(tag_ratio * 10)
        
        return min(sum(confidence_factors), 100.0)
    
    def create_menu_summary(self, sections: List[MenuSection]) -> Dict[str, Any]:
        """Create a summary of the parsed menu"""
        total_items = sum(len(section.items) for section in sections)
        items_with_prices = sum(1 for section in sections for item in section.items if item.price)
        
        # Price range
        all_prices = [item.price for section in sections for item in section.items if item.price]
        price_range = {
            'min': min(all_prices) if all_prices else None,
            'max': max(all_prices) if all_prices else None,
            'average': sum(all_prices) / len(all_prices) if all_prices else None
        }
        
        # Most common dietary tags
        all_tags = []
        for section in sections for item in section.items:
            all_tags.extend(item.dietary_tags)
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            'total_sections': len(sections),
            'total_items': total_items,
            'items_with_prices': items_with_prices,
            'price_coverage': (items_with_prices / total_items * 100) if total_items > 0 else 0,
            'price_range': price_range,
            'section_names': [section.name for section in sections],
            'dietary_tags': dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)),
            'average_items_per_section': total_items / len(sections) if sections else 0
        }
    
    def section_to_dict(self, section: MenuSection) -> Dict[str, Any]:
        """Convert MenuSection to dictionary"""
        return {
            'name': section.name,
            'description': section.description,
            'items': [self.item_to_dict(item) for item in section.items],
            'item_count': len(section.items)
        }
    
    def item_to_dict(self, item: MenuItem) -> Dict[str, Any]:
        """Convert MenuItem to dictionary"""
        return {
            'title': item.title,
            'description': item.description,
            'price': item.price,
            'price_text': item.price_text,
            'category': item.category,
            'dietary_tags': item.dietary_tags,
            'spice_level': item.spice_level
        }