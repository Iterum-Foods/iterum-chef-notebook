import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass
class ParsedIngredient:
    """Represents a parsed ingredient with amount and unit"""
    name: str
    amount: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    original_text: str = ""

@dataclass
class ParsedRecipe:
    """Represents a parsed recipe with all extracted information"""
    title: Optional[str] = None
    ingredients: List[ParsedIngredient] = None
    instructions: List[str] = None
    allergy_notes: List[str] = None
    pricing_info: Dict[str, float] = None
    yield_info: Optional[str] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    difficulty: Optional[str] = None
    cuisine: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.ingredients is None:
            self.ingredients = []
        if self.instructions is None:
            self.instructions = []
        if self.allergy_notes is None:
            self.allergy_notes = []
        if self.pricing_info is None:
            self.pricing_info = {}
        if self.tags is None:
            self.tags = []

class RecipeParser:
    """Advanced recipe parsing service"""
    
    def __init__(self):
        # Common units for ingredient amounts
        self.units = {
            'volume': ['cup', 'cups', 'tbsp', 'tablespoon', 'tablespoons', 'tsp', 'teaspoon', 'teaspoons', 
                      'ml', 'milliliter', 'milliliters', 'l', 'liter', 'liters', 'fl oz', 'fluid ounce', 
                      'pint', 'pints', 'quart', 'quarts', 'gallon', 'gallons', 'dash', 'pinch'],
            'weight': ['g', 'gram', 'grams', 'kg', 'kilogram', 'kilograms', 'oz', 'ounce', 'ounces', 
                      'lb', 'pound', 'pounds'],
            'count': ['whole', 'piece', 'pieces', 'slice', 'slices', 'clove', 'cloves', 'bunch', 'bunches']
        }
        
        # Allergy keywords
        self.allergy_keywords = [
            'allergen', 'allergy', 'allergic', 'contains', 'may contain', 'processed in facility',
            'gluten', 'wheat', 'dairy', 'milk', 'lactose', 'eggs', 'egg', 'nuts', 'peanuts', 'tree nuts',
            'soy', 'soybean', 'fish', 'shellfish', 'crustacean', 'mollusk', 'sesame', 'sulfites',
            'celery', 'mustard', 'lupin', 'sulfite', 'sulphite'
        ]
        
        # Price indicators
        self.price_indicators = [
            'cost', 'price', 'total cost', 'ingredient cost', 'recipe cost', 'serving cost',
            'per serving', 'per portion', 'total price', 'estimated cost', 'food cost'
        ]
        
        # Common ingredient patterns
        self.ingredient_patterns = [
            r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s+(.+)',  # "2 cups flour"
            r'(\d+(?:\.\d+)?)\s+(.+)',  # "2 flour" (no unit)
            r'([a-zA-Z]+)\s+(.+)',  # "salt to taste"
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s+(.+)',  # "1-2 cups flour"
            r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s+(.+)',  # "1/2 cup flour"
        ]
    
    def parse_recipe_text(self, text: str) -> ParsedRecipe:
        """Parse recipe text and extract structured information"""
        lines = text.split('\n')
        recipe = ParsedRecipe()
        
        # Extract title
        recipe.title = self._extract_title(lines)
        
        # Extract allergy notes
        recipe.allergy_notes = self._extract_allergy_notes(text)
        
        # Extract pricing information
        recipe.pricing_info = self._extract_pricing_info(text)
        
        # Extract ingredients
        recipe.ingredients = self._extract_ingredients(text)
        
        # Extract instructions
        recipe.instructions = self._extract_instructions(lines)
        
        # Extract additional metadata
        recipe.yield_info = self._extract_yield_info(text)
        recipe.prep_time = self._extract_time_info(text, 'prep')
        recipe.cook_time = self._extract_time_info(text, 'cook')
        recipe.difficulty = self._extract_difficulty(text)
        recipe.cuisine = self._extract_cuisine(text)
        recipe.tags = self._extract_tags(text)
        
        return recipe
    
    def _extract_title(self, lines: List[str]) -> Optional[str]:
        """Extract recipe title from the first few lines"""
        for i, line in enumerate(lines[:5]):  # Check first 5 lines
            line = line.strip()
            if line and len(line) > 3 and len(line) < 100:
                # Skip common non-title patterns
                if not any(skip in line.lower() for skip in ['ingredients:', 'directions:', 'prep time:', 'cook time:']):
                    return line
        return None
    
    def _extract_allergy_notes(self, text: str) -> List[str]:
        """Extract allergy and allergen information"""
        allergy_notes = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            # Check for allergy keywords
            if any(keyword in line_lower for keyword in self.allergy_keywords):
                # Clean up the line
                cleaned_line = line.strip()
                if cleaned_line and len(cleaned_line) > 5:
                    allergy_notes.append(cleaned_line)
        
        return allergy_notes
    
    def _extract_pricing_info(self, text: str) -> Dict[str, float]:
        """Extract pricing information from recipe text"""
        pricing_info = {}
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            # Look for price indicators
            if any(indicator in line_lower for indicator in self.price_indicators):
                # Extract currency amounts
                currency_patterns = [
                    r'\$(\d+(?:\.\d{2})?)',  # $10.50
                    r'(\d+(?:\.\d{2})?)\s*dollars?',  # 10.50 dollars
                    r'(\d+(?:\.\d{2})?)\s*usd',  # 10.50 USD
                ]
                
                for pattern in currency_patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    for match in matches:
                        try:
                            amount = float(match)
                            # Try to identify what this price refers to
                            if 'per serving' in line_lower or 'serving' in line_lower:
                                pricing_info['per_serving'] = amount
                            elif 'total' in line_lower:
                                pricing_info['total_cost'] = amount
                            elif 'ingredient' in line_lower:
                                pricing_info['ingredient_cost'] = amount
                            else:
                                pricing_info['estimated_cost'] = amount
                        except ValueError:
                            continue
        
        return pricing_info
    
    def _extract_ingredients(self, text: str) -> List[ParsedIngredient]:
        """Extract ingredients with amounts and units"""
        ingredients = []
        lines = text.split('\n')
        
        in_ingredients_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            # Detect ingredients section
            if any(section in line_lower for section in ['ingredients:', 'ingredient list:', 'for the']):
                in_ingredients_section = True
                continue
            
            # End ingredients section when we hit instructions
            if any(section in line_lower for section in ['directions:', 'instructions:', 'method:', 'steps:']):
                in_ingredients_section = False
                continue
            
            if in_ingredients_section or self._looks_like_ingredient(line):
                ingredient = self._parse_ingredient_line(line)
                if ingredient:
                    ingredients.append(ingredient)
        
        return ingredients
    
    def _looks_like_ingredient(self, line: str) -> bool:
        """Check if a line looks like an ingredient"""
        line_lower = line.lower()
        
        # Skip if it's clearly not an ingredient
        if any(skip in line_lower for skip in ['prep time:', 'cook time:', 'servings:', 'yield:', 'difficulty:']):
            return False
        
        # Check for common ingredient patterns
        ingredient_indicators = [
            r'\d+',  # Contains numbers (amounts)
            r'\b(cup|tbsp|tsp|oz|lb|g|kg|ml|l|pound|ounce|gram|kilogram)\b',  # Contains units
            r'\b(salt|pepper|flour|sugar|butter|oil|garlic|onion|egg|milk|cream)\b',  # Common ingredients
        ]
        
        return any(re.search(pattern, line_lower) for pattern in ingredient_indicators)
    
    def _parse_ingredient_line(self, line: str) -> Optional[ParsedIngredient]:
        """Parse a single ingredient or menu item line, extracting quantity if present"""
        original_line = line
        # Remove common prefixes
        line = re.sub(r'^[\d\-•*]\s*', '', line)

        # --- NEW: Menu item quantity patterns ---
        menu_qty_patterns = [
            r'^(?P<qty>\d+)\s*[xX]\s*(?P<item>.+)$',                # 3x Chicken Sandwich
            r'^(?P<item>.+?)\s*[xX]\s*(?P<qty>\d+)$',                # Chicken Sandwich x3
            r'^(?P<item>.+?)\s*[-–]\s*(?P<qty>\d+)$',                # Chicken Sandwich - 3
            r'^(?P<qty>\d+)\s+(.+)$',                                 # 3 Chicken Sandwiches
            r'^(?P<item>.+?)\s*\((?P<qty>\d+)\)$',                  # Chicken Sandwich (3)
        ]
        for pattern in menu_qty_patterns:
            match = re.match(pattern, line.strip())
            if match:
                item = match.groupdict().get('item') or match.groups()[-1]
                qty = match.groupdict().get('qty') or match.groups()[0]
                try:
                    qty_val = float(qty)
                except Exception:
                    qty_val = None
                return ParsedIngredient(
                    name=item.strip(),
                    amount=qty_val,
                    unit=None,
                    original_text=original_line
                )

        # --- Existing ingredient patterns ---
        for pattern in self.ingredient_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 3:  # "2 cups flour"
                    amount_str, unit, name = groups
                    amount = self._parse_amount(amount_str)
                    return ParsedIngredient(
                        name=name.strip(),
                        amount=amount,
                        unit=unit.strip().lower(),
                        original_text=original_line
                    )
                elif len(groups) == 2:  # "2 flour" or "salt to taste"
                    first, second = groups
                    amount = self._parse_amount(first)
                    if amount is not None:
                        return ParsedIngredient(
                            name=second.strip(),
                            amount=amount,
                            original_text=original_line
                        )
                    else:
                        return ParsedIngredient(
                            name=line.strip(),
                            notes=line.strip(),
                            original_text=original_line
                        )
        # If no pattern matches, treat as ingredient/menu item name only
        return ParsedIngredient(
            name=line.strip(),
            original_text=original_line
        )
    
    def _parse_amount(self, amount_str: str) -> Optional[float]:
        """Parse amount string to float"""
        try:
            # Handle fractions
            if '/' in amount_str:
                parts = amount_str.split('/')
                if len(parts) == 2:
                    numerator = float(parts[0])
                    denominator = float(parts[1])
                    return numerator / denominator
            
            # Handle mixed numbers like "1 1/2"
            mixed_pattern = r'(\d+)\s+(\d+)/(\d+)'
            match = re.match(mixed_pattern, amount_str)
            if match:
                whole, num, denom = match.groups()
                return float(whole) + (float(num) / float(denom))
            
            # Handle ranges like "1-2"
            range_pattern = r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)'
            match = re.match(range_pattern, amount_str)
            if match:
                min_val, max_val = match.groups()
                return (float(min_val) + float(max_val)) / 2  # Return average
            
            return float(amount_str)
        except (ValueError, ZeroDivisionError):
            return None
    
    def _extract_instructions(self, lines: List[str]) -> List[str]:
        """Extract cooking instructions"""
        instructions = []
        in_instructions_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            # Detect instructions section
            if any(section in line_lower for section in ['directions:', 'instructions:', 'method:', 'steps:', 'procedure:']):
                in_instructions_section = True
                continue
            
            # End instructions section when we hit other sections
            if any(section in line_lower for section in ['ingredients:', 'notes:', 'tips:', 'nutrition:']):
                in_instructions_section = False
                continue
            
            if in_instructions_section:
                # Clean up instruction line
                cleaned_line = re.sub(r'^\d+\.?\s*', '', line)  # Remove step numbers
                if cleaned_line and len(cleaned_line) > 5:
                    instructions.append(cleaned_line)
        
        return instructions
    
    def _extract_yield_info(self, text: str) -> Optional[str]:
        """Extract yield/servings information"""
        yield_patterns = [
            r'yield:\s*(.+)',
            r'servings:\s*(.+)',
            r'makes\s+(.+)',
            r'serves\s+(.+)',
        ]
        
        for pattern in yield_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_time_info(self, text: str, time_type: str) -> Optional[str]:
        """Extract prep or cook time information"""
        time_patterns = [
            rf'{time_type}\s*time:\s*(.+)',
            rf'{time_type}:\s*(.+)',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_difficulty(self, text: str) -> Optional[str]:
        """Extract difficulty level"""
        difficulty_patterns = [
            r'difficulty:\s*(easy|medium|hard|intermediate|beginner|advanced)',
            r'level:\s*(easy|medium|hard|intermediate|beginner|advanced)',
        ]
        
        for pattern in difficulty_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        
        return None
    
    def _extract_cuisine(self, text: str) -> Optional[str]:
        """Extract cuisine type"""
        cuisine_keywords = [
            'italian', 'french', 'chinese', 'japanese', 'indian', 'mexican', 'thai', 'greek',
            'mediterranean', 'american', 'southern', 'cajun', 'creole', 'spanish', 'portuguese',
            'german', 'russian', 'korean', 'vietnamese', 'lebanese', 'turkish', 'moroccan'
        ]
        
        text_lower = text.lower()
        for cuisine in cuisine_keywords:
            if cuisine in text_lower:
                return cuisine.title()
        
        return None
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract recipe tags"""
        tags = []
        
        # Common recipe tags
        tag_keywords = [
            'vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'low-carb', 'keto', 'paleo',
            'quick', 'easy', 'healthy', 'comfort food', 'dessert', 'appetizer', 'main course',
            'breakfast', 'lunch', 'dinner', 'snack', 'beverage', 'soup', 'salad', 'pasta',
            'grilled', 'baked', 'fried', 'roasted', 'slow cooker', 'instant pot', 'air fryer'
        ]
        
        text_lower = text.lower()
        for tag in tag_keywords:
            if tag in text_lower:
                tags.append(tag)
        
        return tags
    
    def to_dict(self, recipe: ParsedRecipe) -> Dict:
        """Convert parsed recipe to dictionary format"""
        return {
            'title': recipe.title,
            'ingredients': [
                {
                    'name': ing.name,
                    'amount': ing.amount,
                    'unit': ing.unit,
                    'notes': ing.notes,
                    'original_text': ing.original_text
                }
                for ing in recipe.ingredients
            ],
            'instructions': recipe.instructions,
            'allergy_notes': recipe.allergy_notes,
            'pricing_info': recipe.pricing_info,
            'yield_info': recipe.yield_info,
            'prep_time': recipe.prep_time,
            'cook_time': recipe.cook_time,
            'difficulty': recipe.difficulty,
            'cuisine': recipe.cuisine,
            'tags': recipe.tags
        } 