#!/usr/bin/env python3
"""
Vendor Price Importer
Import vendor price lists from Excel files or websites and update ingredient costs
"""

import sys
import re
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging

try:
    import requests
    from bs4 import BeautifulSoup
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False

# Add local modules
sys.path.insert(0, str(Path(__file__).parent))
from ingredient_database import IngredientDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VendorPriceImporter:
    """Import vendor prices from Excel files or websites."""
    
    def __init__(self, ingredient_db: Optional[IngredientDatabase] = None):
        self.ingredient_db = ingredient_db or IngredientDatabase()
        self.vendor_name = ""
        self.import_date = datetime.now().isoformat()
    
    def import_from_excel(self, file_path: str, vendor_name: str = "", 
                         auto_match: bool = True) -> Dict[str, Any]:
        """
        Import vendor prices from Excel file.
        
        Args:
            file_path: Path to Excel file
            vendor_name: Vendor name (extracted from filename if not provided)
            auto_match: Automatically match ingredients to database
            
        Returns:
            Dictionary with import results
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                'success': False,
                'error': f'File not found: {file_path}'
            }
        
        # Extract vendor name from filename if not provided
        if not vendor_name:
            vendor_name = self._extract_vendor_name(file_path.name)
        
        self.vendor_name = vendor_name
        
        try:
            # Try to read Excel file
            logger.info(f"Reading Excel file: {file_path}")
            
            # Try different sheet names or first sheet
            try:
                df = pd.read_excel(file_path, sheet_name=0)
            except:
                # Try reading all sheets
                excel_file = pd.ExcelFile(file_path)
                df = pd.read_excel(excel_file, sheet_name=excel_file.sheet_names[0])
            
            logger.info(f"Found {len(df)} rows in Excel file")
            
            # Detect column structure
            column_map = self._detect_columns(df)
            
            if not column_map:
                return {
                    'success': False,
                    'error': 'Could not detect required columns (Item/Product, Price/Cost)'
                }
            
            # Parse prices
            parsed_items = self._parse_excel_data(df, column_map)
            
            # Match to ingredient database
            matched_items = []
            unmatched_items = []
            
            for item in parsed_items:
                if auto_match:
                    match_result = self._match_to_ingredient(item)
                    if match_result['matched']:
                        item['ingredient_id'] = match_result['ingredient_id']
                        item['ingredient_name'] = match_result['ingredient_name']
                        matched_items.append(item)
                    else:
                        unmatched_items.append(item)
                else:
                    unmatched_items.append(item)
            
            # Update ingredient costs for matched items
            updated_count = 0
            for item in matched_items:
                try:
                    self._update_ingredient_cost(item)
                    updated_count += 1
                except Exception as e:
                    logger.warning(f"Failed to update {item.get('ingredient_name')}: {e}")
            
            return {
                'success': True,
                'vendor': vendor_name,
                'total_items': len(parsed_items),
                'matched': len(matched_items),
                'unmatched': len(unmatched_items),
                'updated': updated_count,
                'matched_items': matched_items[:20],  # First 20 for preview
                'unmatched_items': unmatched_items[:20]  # First 20 for preview
            }
            
        except Exception as e:
            logger.error(f"Error importing Excel file: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_vendor_name(self, filename: str) -> str:
        """Extract vendor name from filename."""
        # Remove extension
        name = Path(filename).stem
        
        # Remove common patterns
        name = re.sub(r'\s*order\s*guide.*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*price\s*list.*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*catalog.*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\d+', '', name)  # Remove numbers
        name = name.strip()
        
        return name or "Unknown Vendor"
    
    def _detect_columns(self, df: pd.DataFrame) -> Optional[Dict[str, str]]:
        """Detect which columns contain item names, prices, units, etc."""
        column_map = {}
        
        # Get column names (normalized)
        columns_lower = {col.lower(): col for col in df.columns}
        
        # Common column name patterns
        name_patterns = [
            'item', 'product', 'ingredient', 'description', 'name',
            'item name', 'product name', 'item description'
        ]
        price_patterns = [
            'price', 'cost', 'ap cost', 'ap$', 'unit price', 'unit cost',
            'each', 'per unit', 'rate'
        ]
        unit_patterns = [
            'unit', 'uom', 'unit of measure', 'pack', 'size', 'package'
        ]
        code_patterns = [
            'code', 'sku', 'item number', 'product code', 'item code'
        ]
        category_patterns = [
            'category', 'department', 'class', 'type'
        ]
        
        # Find name column
        for pattern in name_patterns:
            for col_lower, col_orig in columns_lower.items():
                if pattern in col_lower:
                    column_map['name'] = col_orig
                    break
            if 'name' in column_map:
                break
        
        # Find price column
        for pattern in price_patterns:
            for col_lower, col_orig in columns_lower.items():
                if pattern in col_lower:
                    # Check if it's numeric
                    try:
                        sample = df[col_orig].dropna().head(10)
                        if pd.api.types.is_numeric_dtype(sample) or any(
                            isinstance(val, (int, float)) for val in sample
                        ):
                            column_map['price'] = col_orig
                            break
                    except:
                        pass
            if 'price' in column_map:
                break
        
        # Find unit column
        for pattern in unit_patterns:
            for col_lower, col_orig in columns_lower.items():
                if pattern in col_lower:
                    column_map['unit'] = col_orig
                    break
            if 'unit' in column_map:
                break
        
        # Optional columns
        for pattern in code_patterns:
            for col_lower, col_orig in columns_lower.items():
                if pattern in col_lower:
                    column_map['code'] = col_orig
                    break
            if 'code' in column_map:
                break
        
        for pattern in category_patterns:
            for col_lower, col_orig in columns_lower.items():
                if pattern in col_lower:
                    column_map['category'] = col_orig
                    break
            if 'category' in column_map:
                break
        
        # Must have at least name and price
        if 'name' in column_map and 'price' in column_map:
            return column_map
        
        return None
    
    def _parse_excel_data(self, df: pd.DataFrame, column_map: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse Excel data into structured format."""
        items = []
        
        for idx, row in df.iterrows():
            try:
                # Get item name
                item_name = str(row[column_map['name']]).strip()
                if not item_name or item_name.lower() in ['nan', 'none', '']:
                    continue
                
                # Get price
                price = row[column_map['price']]
                if pd.isna(price):
                    continue
                
                # Convert to float
                try:
                    price = float(price)
                    if price <= 0:
                        continue
                except (ValueError, TypeError):
                    # Try to extract number from string
                    price_match = re.search(r'[\d.]+', str(price))
                    if price_match:
                        price = float(price_match.group())
                    else:
                        continue
                
                item = {
                    'vendor_name': item_name,
                    'price': price,
                    'vendor': self.vendor_name,
                    'import_date': self.import_date
                }
                
                # Get unit if available
                if 'unit' in column_map:
                    unit = str(row[column_map['unit']]).strip()
                    if unit and unit.lower() not in ['nan', 'none', '']:
                        item['unit'] = unit
                
                # Get code if available
                if 'code' in column_map:
                    code = str(row[column_map['code']]).strip()
                    if code and code.lower() not in ['nan', 'none', '']:
                        item['code'] = code
                
                # Get category if available
                if 'category' in column_map:
                    category = str(row[column_map['category']]).strip()
                    if category and category.lower() not in ['nan', 'none', '']:
                        item['category'] = category
                
                items.append(item)
                
            except Exception as e:
                logger.debug(f"Error parsing row {idx}: {e}")
                continue
        
        return items
    
    def _match_to_ingredient(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Match vendor item to ingredient in database."""
        vendor_name = item['vendor_name'].lower()
        
        # Try exact match first
        try:
            ingredient = self.ingredient_db.get_ingredient_by_name(vendor_name)
            if ingredient:
                return {
                    'matched': True,
                    'ingredient_id': ingredient['id'],
                    'ingredient_name': ingredient['name'],
                    'confidence': 1.0
                }
        except:
            pass
        
        # Try fuzzy matching
        # Search for similar names
        search_terms = self._extract_search_terms(vendor_name)
        
        best_match = None
        best_score = 0.0
        
        for term in search_terms:
            results = self.ingredient_db.search_ingredients(term)
            for ingredient in results:
                score = self._calculate_similarity(vendor_name, ingredient['name'].lower())
                if score > best_score and score > 0.7:  # 70% similarity threshold
                    best_score = score
                    best_match = ingredient
        
        if best_match:
            return {
                'matched': True,
                'ingredient_id': best_match['id'],
                'ingredient_name': best_match['name'],
                'confidence': best_score
            }
        
        return {
            'matched': False,
            'confidence': 0.0
        }
    
    def _extract_search_terms(self, text: str) -> List[str]:
        """Extract search terms from vendor item name."""
        # Remove common vendor prefixes/suffixes
        text = re.sub(r'\b(case|pack|box|bag|each|ea|ctn|carton)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d+', '', text)  # Remove numbers
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove special chars
        text = ' '.join(text.split())  # Normalize whitespace
        
        # Split into words
        words = text.split()
        
        # Return key terms (longer words first)
        words.sort(key=len, reverse=True)
        return words[:3]  # Top 3 terms
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings (simple implementation)."""
        # Simple word overlap
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _update_ingredient_cost(self, item: Dict[str, Any]):
        """Update ingredient cost in database - adds to vendor prices."""
        ingredient_id = item['ingredient_id']
        ingredient = self.ingredient_db.get_ingredient(ingredient_id)
        
        if not ingredient:
            return
        
        # Get unit from item or use ingredient default
        unit = item.get('unit') or ingredient['default_unit']
        vendor_name = item['vendor']
        
        # Add/update vendor price (this handles multiple vendors)
        self.ingredient_db.add_vendor_price(
            ingredient_id=ingredient_id,
            vendor_name=vendor_name,
            ap_cost=item['price'],
            cost_unit=unit,
            vendor_url=None,  # Could extract from item if available
            notes=f"Imported from {vendor_name} price list"
        )
        
        # Also update cost history
        self._add_cost_history(ingredient['name'], item['price'], unit, vendor_name)
    
    def _add_cost_history(self, ingredient_name: str, cost: float, unit: str, vendor: str):
        """Add entry to cost history."""
        # This would integrate with cost history if we have that table
        # For now, just log it
        logger.info(f"Updated cost for {ingredient_name}: ${cost:.2f}/{unit} from {vendor}")
    
    def import_from_website(self, url: str, vendor_name: str = "") -> Dict[str, Any]:
        """
        Import vendor prices from website (if supported).
        
        Note: This is more complex and vendor-specific.
        Excel files are generally more reliable.
        """
        if not WEB_SCRAPING_AVAILABLE:
            return {
                'success': False,
                'error': 'Web scraping not available. Install requests and beautifulsoup4.'
            }
        
        if not vendor_name:
            vendor_name = self._extract_vendor_name_from_url(url)
        
        self.vendor_name = vendor_name
        
        # This would need vendor-specific parsing
        # Most vendor websites require login and have complex structures
        return {
            'success': False,
            'error': 'Website import requires vendor-specific implementation. Excel import is recommended.'
        }
    
    def _extract_vendor_name_from_url(self, url: str) -> str:
        """Extract vendor name from URL."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        # Remove www. and common TLDs
        name = re.sub(r'^www\.', '', domain)
        name = re.sub(r'\.(com|net|org|co|us).*$', '', name)
        return name.title() or "Unknown Vendor"
    
    def preview_import(self, file_path: str, vendor_name: str = "", 
                      max_rows: int = 20) -> Dict[str, Any]:
        """Preview what will be imported without actually updating."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                'success': False,
                'error': f'File not found: {file_path}'
            }
        
        try:
            df = pd.read_excel(file_path, sheet_name=0, nrows=max_rows + 10)
            
            column_map = self._detect_columns(df)
            
            if not column_map:
                return {
                    'success': False,
                    'error': 'Could not detect required columns'
                }
            
            parsed_items = self._parse_excel_data(df.head(max_rows), column_map)
            
            return {
                'success': True,
                'columns_detected': column_map,
                'sample_items': parsed_items[:max_rows],
                'total_rows_in_file': len(df)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """CLI interface for vendor price importer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import vendor prices from Excel')
    parser.add_argument('file', help='Path to Excel file')
    parser.add_argument('--vendor', '-v', help='Vendor name')
    parser.add_argument('--preview', '-p', action='store_true', 
                       help='Preview import without updating')
    parser.add_argument('--no-auto-match', action='store_true',
                       help='Do not automatically match to ingredients')
    
    args = parser.parse_args()
    
    importer = VendorPriceImporter()
    
    if args.preview:
        print(f"\n📋 Previewing import from: {args.file}\n")
        result = importer.preview_import(args.file, args.vendor)
        
        if result['success']:
            print("✅ Column Detection:")
            for key, value in result['columns_detected'].items():
                print(f"  {key}: {value}")
            
            print(f"\n📦 Sample Items ({len(result['sample_items'])}):")
            for item in result['sample_items']:
                print(f"  • {item['vendor_name']}: ${item['price']:.2f} {item.get('unit', '')}")
            
            print(f"\nTotal rows in file: {result['total_rows_in_file']}")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print(f"\n📥 Importing prices from: {args.file}\n")
        result = importer.import_from_excel(
            args.file, 
            args.vendor,
            auto_match=not args.no_auto_match
        )
        
        if result['success']:
            print(f"✅ Import Complete!")
            print(f"   Vendor: {result['vendor']}")
            print(f"   Total items: {result['total_items']}")
            print(f"   Matched: {result['matched']}")
            print(f"   Updated: {result['updated']}")
            print(f"   Unmatched: {result['unmatched']}")
            
            if result['unmatched'] > 0:
                print(f"\n⚠️  {result['unmatched']} items could not be matched to ingredients")
                print("   Consider adding them manually or improving matching")
        else:
            print(f"❌ Import failed: {result['error']}")


if __name__ == '__main__':
    main()

