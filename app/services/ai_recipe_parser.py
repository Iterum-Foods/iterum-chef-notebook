"""
AI-Enhanced Recipe Parser for Iterum R&D Chef Notebook
Uses Large Language Models to intelligently parse and enhance recipe data
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
import httpx
from app.core.ai_config import get_ai_settings, get_primary_ai_provider, get_ai_provider_config, AIFeatures

logger = logging.getLogger(__name__)

@dataclass
class ParsedIngredient:
    """Structured ingredient data"""
    name: str
    amount: Optional[str] = None
    unit: Optional[str] = None
    preparation: Optional[str] = None
    notes: Optional[str] = None
    confidence: float = 0.0

@dataclass
class ParsedInstruction:
    """Structured instruction data"""
    step_number: int
    instruction: str
    technique: Optional[str] = None
    temperature: Optional[str] = None
    time: Optional[str] = None
    confidence: float = 0.0

@dataclass
class ParsedRecipe:
    """Complete parsed recipe structure"""
    title: str
    description: Optional[str] = None
    servings: Optional[int] = None
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    total_time: Optional[str] = None
    difficulty: Optional[str] = None
    cuisine: Optional[str] = None
    category: Optional[str] = None
    ingredients: List[ParsedIngredient] = None
    instructions: List[ParsedInstruction] = None
    nutrition: Optional[Dict] = None
    allergens: List[str] = None
    tags: List[str] = None
    confidence: float = 0.0

class AIRecipeParser:
    """AI-powered recipe parsing and enhancement"""
    
    def __init__(self):
        self.settings = get_ai_settings()
        self.provider = get_primary_ai_provider()
        self.config = get_ai_provider_config(self.provider)
        
    async def parse_recipe_with_ai(self, recipe_text: str, image_url: Optional[str] = None) -> ParsedRecipe:
        """Parse recipe text using AI for enhanced accuracy"""
        
        if not AIFeatures.recipe_parsing_enabled():
            logger.warning("AI recipe parsing is disabled")
            return self._fallback_parse(recipe_text)
        
        try:
            # Create AI prompt for recipe parsing
            prompt = self._create_recipe_parsing_prompt(recipe_text, image_url)
            
            # Call AI service
            ai_response = await self._call_ai_service(prompt, image_url)
            
            # Parse AI response into structured data
            parsed_recipe = self._parse_ai_response(ai_response)
            
            # Enhance with additional AI analysis
            if self.settings.technique_analysis:
                parsed_recipe = await self._analyze_cooking_techniques(parsed_recipe)
            
            if self.settings.nutritional_analysis:
                parsed_recipe = await self._analyze_nutrition(parsed_recipe)
            
            if self.settings.cost_estimation:
                parsed_recipe = await self._estimate_costs(parsed_recipe)
            
            return parsed_recipe
            
        except Exception as e:
            logger.error(f"AI recipe parsing failed: {e}")
            return self._fallback_parse(recipe_text)
    
    def _create_recipe_parsing_prompt(self, recipe_text: str, image_url: Optional[str] = None) -> str:
        """Create comprehensive prompt for AI recipe parsing"""
        
        prompt = f"""
You are a professional chef and recipe analyst. Parse the following recipe text with maximum accuracy and provide structured data.

RECIPE TEXT:
{recipe_text}

Please extract and structure the following information:

1. BASIC INFORMATION:
   - Recipe title (clear, descriptive)
   - Description (brief summary of the dish)
   - Servings/yield
   - Prep time, cook time, total time
   - Difficulty level (Easy/Medium/Hard)
   - Cuisine type
   - Category (Appetizer, Main Course, Dessert, etc.)

2. INGREDIENTS (for each ingredient):
   - Name (standardized)
   - Amount (exact measurement)
   - Unit (cups, ounces, grams, etc.)
   - Preparation method (chopped, diced, minced, etc.)
   - Special notes or instructions

3. INSTRUCTIONS (step by step):
   - Step number
   - Clear, detailed instruction
   - Cooking technique used
   - Temperature (if applicable)
   - Time (if specified)

4. ADDITIONAL ANALYSIS:
   - Allergen information
   - Dietary restrictions (vegetarian, vegan, gluten-free, etc.)
   - Cooking techniques identified
   - Flavor profile
   - Suggested tags for categorization

5. PROFESSIONAL INSIGHTS:
   - Recipe completeness score (1-10)
   - Potential improvements
   - Scaling recommendations
   - Storage and serving suggestions

Return the data in this exact JSON format:
{{
    "title": "Recipe Title",
    "description": "Brief description",
    "servings": 4,
    "prep_time": "15 minutes",
    "cook_time": "30 minutes",
    "total_time": "45 minutes",
    "difficulty": "Medium",
    "cuisine": "Italian",
    "category": "Main Course",
    "ingredients": [
        {{
            "name": "ingredient name",
            "amount": "2",
            "unit": "cups",
            "preparation": "chopped",
            "notes": "optional notes",
            "confidence": 0.95
        }}
    ],
    "instructions": [
        {{
            "step_number": 1,
            "instruction": "detailed step",
            "technique": "sautéing",
            "temperature": "medium heat",
            "time": "5 minutes",
            "confidence": 0.90
        }}
    ],
    "nutrition": {{
        "calories_per_serving": 350,
        "protein": "25g",
        "carbs": "30g",
        "fat": "15g"
    }},
    "allergens": ["gluten", "dairy"],
    "tags": ["comfort food", "family dinner", "one-pot"],
    "confidence": 0.92,
    "professional_insights": {{
        "completeness_score": 8,
        "improvements": ["Add salt to taste", "Consider adding herbs"],
        "scaling_notes": "Doubles well for larger groups",
        "storage_notes": "Refrigerate for up to 3 days"
    }}
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
    
    def _parse_ai_response(self, ai_response: str) -> ParsedRecipe:
        """Parse AI response into structured recipe data"""
        try:
            # Extract JSON from response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in AI response")
            
            json_str = ai_response[json_start:json_end]
            data = json.loads(json_str)
            
            # Parse ingredients
            ingredients = []
            for ing_data in data.get("ingredients", []):
                ingredients.append(ParsedIngredient(
                    name=ing_data.get("name", ""),
                    amount=ing_data.get("amount"),
                    unit=ing_data.get("unit"),
                    preparation=ing_data.get("preparation"),
                    notes=ing_data.get("notes"),
                    confidence=ing_data.get("confidence", 0.0)
                ))
            
            # Parse instructions
            instructions = []
            for inst_data in data.get("instructions", []):
                instructions.append(ParsedInstruction(
                    step_number=inst_data.get("step_number", 0),
                    instruction=inst_data.get("instruction", ""),
                    technique=inst_data.get("technique"),
                    temperature=inst_data.get("temperature"),
                    time=inst_data.get("time"),
                    confidence=inst_data.get("confidence", 0.0)
                ))
            
            # Create parsed recipe
            recipe = ParsedRecipe(
                title=data.get("title", ""),
                description=data.get("description"),
                servings=data.get("servings"),
                prep_time=data.get("prep_time"),
                cook_time=data.get("cook_time"),
                total_time=data.get("total_time"),
                difficulty=data.get("difficulty"),
                cuisine=data.get("cuisine"),
                category=data.get("category"),
                ingredients=ingredients,
                instructions=instructions,
                nutrition=data.get("nutrition"),
                allergens=data.get("allergens", []),
                tags=data.get("tags", []),
                confidence=data.get("confidence", 0.0)
            )
            
            return recipe
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            raise ValueError(f"Invalid AI response format: {e}")
    
    async def _analyze_cooking_techniques(self, recipe: ParsedRecipe) -> ParsedRecipe:
        """Analyze cooking techniques used in the recipe"""
        if not recipe.instructions:
            return recipe
        
        technique_prompt = f"""
Analyze the cooking techniques used in this recipe and provide professional insights:

Recipe: {recipe.title}
Instructions: {[inst.instruction for inst in recipe.instructions]}

Identify:
1. Primary cooking techniques (sautéing, roasting, braising, etc.)
2. Skill level required
3. Equipment needed
4. Temperature control requirements
5. Timing considerations
6. Professional tips for each technique

Return as JSON:
{{
    "techniques": ["technique1", "technique2"],
    "skill_level": "intermediate",
    "equipment": ["equipment1", "equipment2"],
    "tips": ["tip1", "tip2"]
}}
"""
        
        try:
            ai_response = await self._call_ai_service(technique_prompt)
            technique_data = json.loads(ai_response)
            
            # Add technique analysis to recipe
            recipe.tags.extend(technique_data.get("techniques", []))
            
        except Exception as e:
            logger.warning(f"Technique analysis failed: {e}")
        
        return recipe
    
    async def _analyze_nutrition(self, recipe: ParsedRecipe) -> ParsedRecipe:
        """Analyze nutritional content of the recipe"""
        if not recipe.ingredients:
            return recipe
        
        nutrition_prompt = f"""
Analyze the nutritional content of this recipe:

Recipe: {recipe.title}
Ingredients: {[f"{ing.amount} {ing.unit} {ing.name}" for ing in recipe.ingredients]}
Servings: {recipe.servings or 1}

Provide nutritional analysis per serving:
{{
    "calories": 350,
    "protein": "25g",
    "carbohydrates": "30g",
    "fat": "15g",
    "fiber": "5g",
    "sugar": "8g",
    "sodium": "600mg",
    "vitamins": ["Vitamin A", "Vitamin C"],
    "minerals": ["Iron", "Calcium"],
    "health_benefits": ["High protein", "Rich in fiber"],
    "dietary_notes": ["Gluten-free", "Low sodium option available"]
}}
"""
        
        try:
            ai_response = await self._call_ai_service(nutrition_prompt)
            nutrition_data = json.loads(ai_response)
            recipe.nutrition = nutrition_data
            
        except Exception as e:
            logger.warning(f"Nutrition analysis failed: {e}")
        
        return recipe
    
    async def _estimate_costs(self, recipe: ParsedRecipe) -> ParsedRecipe:
        """Estimate ingredient costs for the recipe"""
        if not recipe.ingredients:
            return recipe
        
        cost_prompt = f"""
Estimate the ingredient costs for this recipe:

Recipe: {recipe.title}
Ingredients: {[f"{ing.amount} {ing.unit} {ing.name}" for ing in recipe.ingredients]}
Servings: {recipe.servings or 1}

Provide cost analysis:
{{
    "total_cost": 12.50,
    "cost_per_serving": 3.13,
    "ingredient_costs": [
        {{"ingredient": "chicken breast", "cost": 4.00, "unit_cost": "8.00/lb"}},
        {{"ingredient": "rice", "cost": 1.50, "unit_cost": "3.00/lb"}}
    ],
    "cost_breakdown": {{
        "protein": 4.00,
        "vegetables": 3.00,
        "grains": 1.50,
        "seasonings": 1.00,
        "other": 3.00
    }},
    "cost_optimization": [
        "Use seasonal vegetables to reduce costs",
        "Buy in bulk for frequently used ingredients"
    ]
}}
"""
        
        try:
            ai_response = await self._call_ai_service(cost_prompt)
            cost_data = json.loads(ai_response)
            
            # Add cost data to recipe
            if not recipe.nutrition:
                recipe.nutrition = {}
            recipe.nutrition["cost_analysis"] = cost_data
            
        except Exception as e:
            logger.warning(f"Cost estimation failed: {e}")
        
        return recipe
    
    def _fallback_parse(self, recipe_text: str) -> ParsedRecipe:
        """Fallback parsing when AI is not available"""
        logger.info("Using fallback recipe parsing")
        
        # Basic parsing logic here
        lines = recipe_text.split('\n')
        title = lines[0] if lines else "Untitled Recipe"
        
        return ParsedRecipe(
            title=title,
            description="Parsed without AI enhancement",
            confidence=0.5
        )
    
    async def enhance_existing_recipe(self, recipe_data: Dict) -> Dict:
        """Enhance existing recipe data with AI insights"""
        
        if not AIFeatures.recipe_parsing_enabled():
            return recipe_data
        
        try:
            # Convert recipe to text for AI processing
            recipe_text = self._recipe_to_text(recipe_data)
            
            # Parse with AI
            enhanced_recipe = await self.parse_recipe_with_ai(recipe_text)
            
            # Convert back to dict format
            return self._parsed_recipe_to_dict(enhanced_recipe)
            
        except Exception as e:
            logger.error(f"Recipe enhancement failed: {e}")
            return recipe_data
    
    def _recipe_to_text(self, recipe_data: Dict) -> str:
        """Convert recipe dict to text for AI processing"""
        text = f"Title: {recipe_data.get('title', '')}\n\n"
        
        if recipe_data.get('description'):
            text += f"Description: {recipe_data['description']}\n\n"
        
        if recipe_data.get('ingredients'):
            text += "Ingredients:\n"
            for ing in recipe_data['ingredients']:
                text += f"- {ing.get('amount', '')} {ing.get('unit', '')} {ing.get('name', '')}\n"
            text += "\n"
        
        if recipe_data.get('instructions'):
            text += "Instructions:\n"
            for i, inst in enumerate(recipe_data['instructions'], 1):
                text += f"{i}. {inst.get('instruction', '')}\n"
        
        return text
    
    def _parsed_recipe_to_dict(self, parsed_recipe: ParsedRecipe) -> Dict:
        """Convert ParsedRecipe to dict format"""
        return {
            "title": parsed_recipe.title,
            "description": parsed_recipe.description,
            "servings": parsed_recipe.servings,
            "prep_time": parsed_recipe.prep_time,
            "cook_time": parsed_recipe.cook_time,
            "total_time": parsed_recipe.total_time,
            "difficulty": parsed_recipe.difficulty,
            "cuisine": parsed_recipe.cuisine,
            "category": parsed_recipe.category,
            "ingredients": [
                {
                    "name": ing.name,
                    "amount": ing.amount,
                    "unit": ing.unit,
                    "preparation": ing.preparation,
                    "notes": ing.notes,
                    "confidence": ing.confidence
                }
                for ing in parsed_recipe.ingredients or []
            ],
            "instructions": [
                {
                    "step_number": inst.step_number,
                    "instruction": inst.instruction,
                    "technique": inst.technique,
                    "temperature": inst.temperature,
                    "time": inst.time,
                    "confidence": inst.confidence
                }
                for inst in parsed_recipe.instructions or []
            ],
            "nutrition": parsed_recipe.nutrition,
            "allergens": parsed_recipe.allergens or [],
            "tags": parsed_recipe.tags or [],
            "confidence": parsed_recipe.confidence,
            "ai_enhanced": True
        }
