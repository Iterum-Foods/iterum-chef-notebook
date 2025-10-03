"""
AI-Enhanced Menu Parser for Iterum R&D Chef Notebook
Uses AI to intelligently parse restaurant menus and extract structured data
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
from app.core.ai_config import get_ai_settings, get_primary_ai_provider, get_ai_provider_config, AIFeatures

logger = logging.getLogger(__name__)

@dataclass
class MenuItem:
    """Structured menu item data"""
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    category: Optional[str] = None
    ingredients: List[str] = None
    allergens: List[str] = None
    dietary_info: List[str] = None
    preparation_method: Optional[str] = None
    portion_size: Optional[str] = None
    confidence: float = 0.0

@dataclass
class MenuSection:
    """Menu section with items"""
    name: str
    items: List[MenuItem] = None
    description: Optional[str] = None
    confidence: float = 0.0

@dataclass
class ParsedMenu:
    """Complete parsed menu structure"""
    restaurant_name: str
    menu_type: str  # breakfast, lunch, dinner, etc.
    sections: List[MenuSection] = None
    total_items: int = 0
    price_range: Optional[str] = None
    cuisine_type: Optional[str] = None
    business_insights: Optional[Dict] = None
    confidence: float = 0.0

class AIMenuParser:
    """AI-powered menu parsing and analysis"""
    
    def __init__(self):
        self.settings = get_ai_settings()
        self.provider = get_primary_ai_provider()
        self.config = get_ai_provider_config(self.provider)
    
    async def parse_menu_with_ai(self, menu_text: str, image_url: Optional[str] = None) -> ParsedMenu:
        """Parse menu text using AI for enhanced accuracy"""
        
        if not AIFeatures.menu_parsing_enabled():
            logger.warning("AI menu parsing is disabled")
            return self._fallback_parse(menu_text)
        
        try:
            # Create AI prompt for menu parsing
            prompt = self._create_menu_parsing_prompt(menu_text, image_url)
            
            # Call AI service
            ai_response = await self._call_ai_service(prompt, image_url)
            
            # Parse AI response into structured data
            parsed_menu = self._parse_ai_response(ai_response)
            
            # Enhance with business intelligence
            if self.settings.price_analysis:
                parsed_menu = await self._analyze_pricing(parsed_menu)
            
            if self.settings.profit_margin_estimation:
                parsed_menu = await self._analyze_profit_margins(parsed_menu)
            
            if self.settings.popularity_prediction:
                parsed_menu = await self._predict_popularity(parsed_menu)
            
            return parsed_menu
            
        except Exception as e:
            logger.error(f"AI menu parsing failed: {e}")
            return self._fallback_parse(menu_text)
    
    def _create_menu_parsing_prompt(self, menu_text: str, image_url: Optional[str] = None) -> str:
        """Create comprehensive prompt for AI menu parsing"""
        
        prompt = f"""
You are a professional restaurant consultant and menu analyst. Parse the following menu text with maximum accuracy and provide structured data.

MENU TEXT:
{menu_text}

Please extract and structure the following information:

1. RESTAURANT INFORMATION:
   - Restaurant name
   - Menu type (breakfast, lunch, dinner, brunch, etc.)
   - Cuisine type (Italian, Asian, American, etc.)
   - Overall price range ($, $$, $$$, $$$$)

2. MENU SECTIONS (for each section):
   - Section name (Appetizers, Main Courses, Desserts, etc.)
   - Section description (if any)
   - Items in this section

3. MENU ITEMS (for each item):
   - Item name
   - Description
   - Price (if listed)
   - Category/section
   - Key ingredients (main ingredients only)
   - Allergen information
   - Dietary restrictions (vegetarian, vegan, gluten-free, etc.)
   - Preparation method (grilled, fried, baked, etc.)
   - Portion size indication

4. BUSINESS ANALYSIS:
   - Price point analysis
   - Menu balance assessment
   - Ingredient diversity
   - Profit margin potential

Return the data in this exact JSON format:
{{
    "restaurant_name": "Restaurant Name",
    "menu_type": "dinner",
    "cuisine_type": "Italian",
    "price_range": "$$$",
    "sections": [
        {{
            "name": "Appetizers",
            "description": "Start your meal with our delicious appetizers",
            "items": [
                {{
                    "name": "Bruschetta",
                    "description": "Toasted bread with tomatoes, basil, and garlic",
                    "price": "$12",
                    "category": "Appetizers",
                    "ingredients": ["bread", "tomatoes", "basil", "garlic", "olive oil"],
                    "allergens": ["gluten"],
                    "dietary_info": ["vegetarian"],
                    "preparation_method": "grilled",
                    "portion_size": "4 pieces",
                    "confidence": 0.95
                }}
            ],
            "confidence": 0.90
        }}
    ],
    "total_items": 15,
    "business_insights": {{
        "price_analysis": "Mid-range pricing with good value",
        "menu_balance": "Well-balanced with variety",
        "ingredient_diversity": "Good use of seasonal ingredients",
        "profit_potential": "High - good margin items"
    }},
    "confidence": 0.88
}}

Be extremely accurate and thorough. If information is missing, use null values rather than guessing.
"""
        
        return prompt
    
    async def _call_ai_service(self, prompt: str, image_url: Optional[str] = None) -> str:
        """Call the appropriate AI service based on configuration"""
        
        if self.provider == "openai":
            return await self._call_openai(prompt, image_url)
        elif self.provider == "anthropic":
            return await self._call_anthropic(prompt, image_url)
        elif self.provider == "google":
            return await self._call_google(prompt, image_url)
        elif self.provider == "azure":
            return await self._call_azure(prompt, image_url)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    async def _call_openai(self, prompt: str, image_url: Optional[str] = None) -> str:
        """Call OpenAI API"""
        import openai
        
        client = openai.AsyncOpenAI(api_key=self.config["api_key"])
        
        messages = [{"role": "user", "content": prompt}]
        
        if image_url:
            messages[0]["content"] = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        
        response = await client.chat.completions.create(
            model=self.config["model"],
            messages=messages,
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        
        return response.choices[0].message.content
    
    async def _call_anthropic(self, prompt: str, image_url: Optional[str] = None) -> str:
        """Call Anthropic Claude API"""
        import anthropic
        
        client = anthropic.AsyncAnthropic(api_key=self.config["api_key"])
        
        response = await client.messages.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _call_google(self, prompt: str, image_url: Optional[str] = None) -> str:
        """Call Google Gemini API"""
        import google.generativeai as genai
        
        genai.configure(api_key=self.config["api_key"])
        model = genai.GenerativeModel(self.config["model"])
        
        response = await model.generate_content_async(prompt)
        return response.text
    
    async def _call_azure(self, prompt: str, image_url: Optional[str] = None) -> str:
        """Call Azure OpenAI API"""
        import openai
        
        client = openai.AsyncAzureOpenAI(
            api_key=self.config["api_key"],
            azure_endpoint=self.config["endpoint"],
            api_version="2024-02-15-preview"
        )
        
        response = await client.chat.completions.create(
            model=self.config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        
        return response.choices[0].message.content
    
    def _parse_ai_response(self, ai_response: str) -> ParsedMenu:
        """Parse AI response into structured menu data"""
        try:
            # Extract JSON from response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in AI response")
            
            json_str = ai_response[json_start:json_end]
            data = json.loads(json_str)
            
            # Parse sections and items
            sections = []
            for section_data in data.get("sections", []):
                items = []
                for item_data in section_data.get("items", []):
                    items.append(MenuItem(
                        name=item_data.get("name", ""),
                        description=item_data.get("description"),
                        price=item_data.get("price"),
                        category=item_data.get("category"),
                        ingredients=item_data.get("ingredients", []),
                        allergens=item_data.get("allergens", []),
                        dietary_info=item_data.get("dietary_info", []),
                        preparation_method=item_data.get("preparation_method"),
                        portion_size=item_data.get("portion_size"),
                        confidence=item_data.get("confidence", 0.0)
                    ))
                
                sections.append(MenuSection(
                    name=section_data.get("name", ""),
                    items=items,
                    description=section_data.get("description"),
                    confidence=section_data.get("confidence", 0.0)
                ))
            
            # Create parsed menu
            menu = ParsedMenu(
                restaurant_name=data.get("restaurant_name", ""),
                menu_type=data.get("menu_type", ""),
                sections=sections,
                total_items=data.get("total_items", 0),
                price_range=data.get("price_range"),
                cuisine_type=data.get("cuisine_type"),
                business_insights=data.get("business_insights"),
                confidence=data.get("confidence", 0.0)
            )
            
            return menu
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            raise ValueError(f"Invalid AI response format: {e}")
    
    async def _analyze_pricing(self, menu: ParsedMenu) -> ParsedMenu:
        """Analyze menu pricing strategy"""
        if not menu.sections:
            return menu
        
        # Extract all prices
        all_prices = []
        for section in menu.sections:
            for item in section.items:
                if item.price:
                    # Extract numeric value from price string
                    price_str = item.price.replace('$', '').replace(',', '')
                    try:
                        price_val = float(price_str)
                        all_prices.append(price_val)
                    except:
                        pass
        
        if not all_prices:
            return menu
        
        # Calculate pricing statistics
        min_price = min(all_prices)
        max_price = max(all_prices)
        avg_price = sum(all_prices) / len(all_prices)
        
        pricing_analysis = {
            "price_range": f"${min_price:.2f} - ${max_price:.2f}",
            "average_price": f"${avg_price:.2f}",
            "price_distribution": {
                "under_10": len([p for p in all_prices if p < 10]),
                "10_to_20": len([p for p in all_prices if 10 <= p < 20]),
                "20_to_30": len([p for p in all_prices if 20 <= p < 30]),
                "over_30": len([p for p in all_prices if p >= 30])
            },
            "pricing_strategy": self._determine_pricing_strategy(avg_price),
            "value_assessment": self._assess_value_proposition(menu, avg_price)
        }
        
        if not menu.business_insights:
            menu.business_insights = {}
        menu.business_insights["pricing_analysis"] = pricing_analysis
        
        return menu
    
    def _determine_pricing_strategy(self, avg_price: float) -> str:
        """Determine pricing strategy based on average price"""
        if avg_price < 10:
            return "Budget-friendly"
        elif avg_price < 20:
            return "Mid-range"
        elif avg_price < 30:
            return "Upscale"
        else:
            return "Premium"
    
    def _assess_value_proposition(self, menu: ParsedMenu, avg_price: float) -> str:
        """Assess value proposition of the menu"""
        # This would be more sophisticated in a real implementation
        if avg_price < 15:
            return "Good value for money"
        elif avg_price < 25:
            return "Fair pricing for quality"
        else:
            return "Premium pricing - expect high quality"
    
    async def _analyze_profit_margins(self, menu: ParsedMenu) -> ParsedMenu:
        """Analyze potential profit margins for menu items"""
        if not menu.sections:
            return menu
        
        margin_analysis = {
            "high_margin_items": [],
            "low_margin_items": [],
            "profit_optimization": [],
            "overall_margin_estimate": "Unknown"
        }
        
        for section in menu.sections:
            for item in section.items:
                if item.price and item.ingredients:
                    # Estimate margin based on ingredient complexity
                    ingredient_count = len(item.ingredients)
                    price_str = item.price.replace('$', '').replace(',', '')
                    
                    try:
                        price_val = float(price_str)
                        
                        # Simple heuristic: more ingredients = higher cost
                        estimated_cost = ingredient_count * 2.0  # $2 per ingredient
                        estimated_margin = ((price_val - estimated_cost) / price_val) * 100
                        
                        if estimated_margin > 60:
                            margin_analysis["high_margin_items"].append({
                                "name": item.name,
                                "price": item.price,
                                "estimated_margin": f"{estimated_margin:.1f}%"
                            })
                        elif estimated_margin < 30:
                            margin_analysis["low_margin_items"].append({
                                "name": item.name,
                                "price": item.price,
                                "estimated_margin": f"{estimated_margin:.1f}%"
                            })
                    except:
                        pass
        
        if not menu.business_insights:
            menu.business_insights = {}
        menu.business_insights["margin_analysis"] = margin_analysis
        
        return menu
    
    async def _predict_popularity(self, menu: ParsedMenu) -> ParsedMenu:
        """Predict popularity of menu items based on various factors"""
        if not menu.sections:
            return menu
        
        popularity_analysis = {
            "likely_popular": [],
            "niche_items": [],
            "trending_ingredients": [],
            "seasonal_recommendations": []
        }
        
        # Analyze each item for popularity indicators
        for section in menu.sections:
            for item in section.items:
                popularity_score = self._calculate_popularity_score(item)
                
                if popularity_score > 7:
                    popularity_analysis["likely_popular"].append({
                        "name": item.name,
                        "score": popularity_score,
                        "reasons": self._get_popularity_reasons(item)
                    })
                elif popularity_score < 4:
                    popularity_analysis["niche_items"].append({
                        "name": item.name,
                        "score": popularity_score,
                        "reasons": self._get_niche_reasons(item)
                    })
        
        if not menu.business_insights:
            menu.business_insights = {}
        menu.business_insights["popularity_analysis"] = popularity_analysis
        
        return menu
    
    def _calculate_popularity_score(self, item: MenuItem) -> int:
        """Calculate popularity score for a menu item (1-10)"""
        score = 5  # Base score
        
        # Positive factors
        if item.description and len(item.description) > 20:
            score += 1  # Good description
        
        if item.ingredients and len(item.ingredients) <= 5:
            score += 1  # Simple ingredients
        
        if item.dietary_info and any(diet in item.dietary_info for diet in ["vegetarian", "vegan"]):
            score += 1  # Dietary friendly
        
        if item.preparation_method in ["grilled", "roasted", "baked"]:
            score += 1  # Healthy cooking methods
        
        # Negative factors
        if item.allergens and len(item.allergens) > 2:
            score -= 1  # Many allergens
        
        if item.ingredients and len(item.ingredients) > 8:
            score -= 1  # Too complex
        
        return max(1, min(10, score))
    
    def _get_popularity_reasons(self, item: MenuItem) -> List[str]:
        """Get reasons why an item might be popular"""
        reasons = []
        
        if item.description and len(item.description) > 20:
            reasons.append("Well-described")
        
        if item.ingredients and len(item.ingredients) <= 5:
            reasons.append("Simple ingredients")
        
        if item.dietary_info and any(diet in item.dietary_info for diet in ["vegetarian", "vegan"]):
            reasons.append("Dietary-friendly")
        
        return reasons
    
    def _get_niche_reasons(self, item: MenuItem) -> List[str]:
        """Get reasons why an item might be niche"""
        reasons = []
        
        if item.allergens and len(item.allergens) > 2:
            reasons.append("Many allergens")
        
        if item.ingredients and len(item.ingredients) > 8:
            reasons.append("Complex preparation")
        
        if not item.description or len(item.description) < 10:
            reasons.append("Poor description")
        
        return reasons
    
    def _fallback_parse(self, menu_text: str) -> ParsedMenu:
        """Fallback parsing when AI is not available"""
        logger.info("Using fallback menu parsing")
        
        lines = menu_text.split('\n')
        restaurant_name = lines[0] if lines else "Unknown Restaurant"
        
        return ParsedMenu(
            restaurant_name=restaurant_name,
            menu_type="Unknown",
            confidence=0.3
        )
    
    def parsed_menu_to_dict(self, parsed_menu: ParsedMenu) -> Dict:
        """Convert ParsedMenu to dict format"""
        return {
            "restaurant_name": parsed_menu.restaurant_name,
            "menu_type": parsed_menu.menu_type,
            "cuisine_type": parsed_menu.cuisine_type,
            "price_range": parsed_menu.price_range,
            "total_items": parsed_menu.total_items,
            "sections": [
                {
                    "name": section.name,
                    "description": section.description,
                    "items": [
                        {
                            "name": item.name,
                            "description": item.description,
                            "price": item.price,
                            "category": item.category,
                            "ingredients": item.ingredients or [],
                            "allergens": item.allergens or [],
                            "dietary_info": item.dietary_info or [],
                            "preparation_method": item.preparation_method,
                            "portion_size": item.portion_size,
                            "confidence": item.confidence
                        }
                        for item in section.items or []
                    ],
                    "confidence": section.confidence
                }
                for section in parsed_menu.sections or []
            ],
            "business_insights": parsed_menu.business_insights,
            "confidence": parsed_menu.confidence,
            "ai_enhanced": True
        }
