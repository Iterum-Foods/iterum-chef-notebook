"""
AI Recipe Creator for Iterum R&D Chef Notebook
Uses AI to generate new recipes, variations, and creative suggestions
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import asyncio
from app.core.ai_config import get_ai_settings, get_primary_ai_provider, get_ai_provider_config, AIFeatures

logger = logging.getLogger(__name__)

@dataclass
class RecipeSuggestion:
    """AI-generated recipe suggestion"""
    title: str
    description: str
    cuisine: str
    difficulty: str
    prep_time: str
    cook_time: str
    servings: int
    ingredients: List[Dict[str, Any]]
    instructions: List[str]
    tags: List[str]
    confidence: float = 0.0

@dataclass
class RecipeVariation:
    """Recipe variation suggestion"""
    variation_type: str  # dietary, technique, fusion, seasonal, etc.
    title: str
    description: str
    changes: List[str]
    new_ingredients: List[str]
    modified_instructions: List[str]
    confidence: float = 0.0

class AIRecipeCreator:
    """AI-powered recipe creation and enhancement"""
    
    def __init__(self):
        self.settings = get_ai_settings()
        self.provider = get_primary_ai_provider()
        self.config = get_ai_provider_config(self.provider)
    
    async def create_recipe_from_ingredients(self, ingredients: List[str], preferences: Dict[str, Any] = None) -> RecipeSuggestion:
        """Create a recipe using specified ingredients"""
        
        if not AIFeatures.recipe_parsing_enabled():
            logger.warning("AI recipe creation is disabled")
            return self._fallback_recipe()
        
        try:
            prompt = self._create_ingredient_based_prompt(ingredients, preferences)
            ai_response = await self._call_ai_service(prompt)
            return self._parse_recipe_suggestion(ai_response)
            
        except Exception as e:
            logger.error(f"AI recipe creation failed: {e}")
            return self._fallback_recipe()
    
    async def create_recipe_from_concept(self, concept: str, preferences: Dict[str, Any] = None) -> RecipeSuggestion:
        """Create a recipe from a concept or idea"""
        
        if not AIFeatures.recipe_parsing_enabled():
            logger.warning("AI recipe creation is disabled")
            return self._fallback_recipe()
        
        try:
            prompt = self._create_concept_based_prompt(concept, preferences)
            ai_response = await self._call_ai_service(prompt)
            return self._parse_recipe_suggestion(ai_response)
            
        except Exception as e:
            logger.error(f"AI recipe creation failed: {e}")
            return self._fallback_recipe()
    
    async def generate_recipe_variations(self, base_recipe: Dict[str, Any], variation_types: List[str] = None) -> List[RecipeVariation]:
        """Generate variations of an existing recipe"""
        
        if not AIFeatures.recipe_parsing_enabled():
            logger.warning("AI recipe variation is disabled")
            return []
        
        if not variation_types:
            variation_types = ["dietary", "technique", "fusion", "seasonal"]
        
        variations = []
        
        for variation_type in variation_types:
            try:
                prompt = self._create_variation_prompt(base_recipe, variation_type)
                ai_response = await self._call_ai_service(prompt)
                variation = self._parse_recipe_variation(ai_response, variation_type)
                variations.append(variation)
                
            except Exception as e:
                logger.error(f"AI variation generation failed for {variation_type}: {e}")
                continue
        
        return variations
    
    async def suggest_recipe_improvements(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest improvements for an existing recipe"""
        
        if not AIFeatures.recipe_parsing_enabled():
            logger.warning("AI recipe improvement is disabled")
            return {"improvements": [], "confidence": 0.0}
        
        try:
            prompt = self._create_improvement_prompt(recipe)
            ai_response = await self._call_ai_service(prompt)
            return self._parse_improvement_suggestions(ai_response)
            
        except Exception as e:
            logger.error(f"AI recipe improvement failed: {e}")
            return {"improvements": [], "confidence": 0.0}
    
    def _create_ingredient_based_prompt(self, ingredients: List[str], preferences: Dict[str, Any] = None) -> str:
        """Create prompt for ingredient-based recipe creation"""
        
        if not preferences:
            preferences = {}
        
        prompt = f"""
You are a professional chef and recipe developer. Create a complete recipe using these ingredients:

INGREDIENTS: {', '.join(ingredients)}

PREFERENCES:
- Cuisine: {preferences.get('cuisine', 'Any')}
- Difficulty: {preferences.get('difficulty', 'Medium')}
- Servings: {preferences.get('servings', 4)}
- Dietary: {preferences.get('dietary', 'None')}
- Cooking time: {preferences.get('cook_time', '30-45 minutes')}

Create a professional, well-balanced recipe that:
1. Uses all the provided ingredients effectively
2. Has clear, detailed instructions
3. Includes proper seasoning and technique
4. Is appropriate for the specified difficulty level
5. Follows the cuisine style if specified

Return in this JSON format:
{{
    "title": "Recipe Title",
    "description": "Brief description of the dish",
    "cuisine": "Cuisine type",
    "difficulty": "Easy/Medium/Hard",
    "prep_time": "15 minutes",
    "cook_time": "30 minutes",
    "servings": 4,
    "ingredients": [
        {{
            "name": "ingredient name",
            "amount": "2",
            "unit": "cups",
            "preparation": "chopped",
            "notes": "optional notes"
        }}
    ],
    "instructions": [
        "Step 1: Detailed instruction",
        "Step 2: Next step",
        "Continue with all steps"
    ],
    "tags": ["tag1", "tag2", "tag3"],
    "confidence": 0.95
}}

Be creative but practical. Ensure the recipe is achievable and delicious.
"""
        
        return prompt
    
    def _create_concept_based_prompt(self, concept: str, preferences: Dict[str, Any] = None) -> str:
        """Create prompt for concept-based recipe creation"""
        
        if not preferences:
            preferences = {}
        
        prompt = f"""
You are a professional chef and recipe developer. Create a complete recipe based on this concept:

CONCEPT: {concept}

PREFERENCES:
- Cuisine: {preferences.get('cuisine', 'Any')}
- Difficulty: {preferences.get('difficulty', 'Medium')}
- Servings: {preferences.get('servings', 4)}
- Dietary: {preferences.get('dietary', 'None')}
- Cooking time: {preferences.get('cook_time', '30-45 minutes')}

Create a professional, innovative recipe that:
1. Fulfills the concept creatively
2. Uses appropriate techniques and ingredients
3. Has clear, detailed instructions
4. Is balanced in flavors and nutrition
5. Is achievable for the specified difficulty level

Return in this JSON format:
{{
    "title": "Recipe Title",
    "description": "Brief description of the dish",
    "cuisine": "Cuisine type",
    "difficulty": "Easy/Medium/Hard",
    "prep_time": "15 minutes",
    "cook_time": "30 minutes",
    "servings": 4,
    "ingredients": [
        {{
            "name": "ingredient name",
            "amount": "2",
            "unit": "cups",
            "preparation": "chopped",
            "notes": "optional notes"
        }}
    ],
    "instructions": [
        "Step 1: Detailed instruction",
        "Step 2: Next step",
        "Continue with all steps"
    ],
    "tags": ["tag1", "tag2", "tag3"],
    "confidence": 0.95
}}

Be innovative and creative while maintaining practicality.
"""
        
        return prompt
    
    def _create_variation_prompt(self, base_recipe: Dict[str, Any], variation_type: str) -> str:
        """Create prompt for recipe variation generation"""
        
        recipe_text = f"""
Title: {base_recipe.get('title', '')}
Description: {base_recipe.get('description', '')}
Ingredients: {[f"{ing.get('amount', '')} {ing.get('unit', '')} {ing.get('name', '')}" for ing in base_recipe.get('ingredients', [])]}
Instructions: {base_recipe.get('instructions', [])}
"""
        
        variation_instructions = {
            "dietary": "Create a dietary variation (vegetarian, vegan, gluten-free, keto, etc.)",
            "technique": "Create a variation using different cooking techniques",
            "fusion": "Create a fusion variation combining different cuisines",
            "seasonal": "Create a seasonal variation with seasonal ingredients",
            "healthy": "Create a healthier version with reduced calories/fat",
            "premium": "Create an upscale/premium version with luxury ingredients",
            "budget": "Create a budget-friendly version with cost-effective ingredients"
        }
        
        instruction = variation_instructions.get(variation_type, "Create a creative variation")
        
        prompt = f"""
You are a professional chef. {instruction} of this recipe:

BASE RECIPE:
{recipe_text}

Create a variation that:
1. Maintains the essence of the original recipe
2. Incorporates the requested variation type
3. Has clear, detailed instructions
4. Uses appropriate ingredients and techniques
5. Is practical and achievable

Return in this JSON format:
{{
    "variation_type": "{variation_type}",
    "title": "Variation Title",
    "description": "Brief description of the variation",
    "changes": [
        "Change 1: Description of what changed",
        "Change 2: Another change made"
    ],
    "new_ingredients": [
        "new ingredient 1",
        "new ingredient 2"
    ],
    "modified_instructions": [
        "Modified step 1",
        "Modified step 2",
        "Continue with all modified steps"
    ],
    "confidence": 0.90
}}

Be creative but practical in your variations.
"""
        
        return prompt
    
    def _create_improvement_prompt(self, recipe: Dict[str, Any]) -> str:
        """Create prompt for recipe improvement suggestions"""
        
        recipe_text = f"""
Title: {recipe.get('title', '')}
Description: {recipe.get('description', '')}
Ingredients: {[f"{ing.get('amount', '')} {ing.get('unit', '')} {ing.get('name', '')}" for ing in recipe.get('ingredients', [])]}
Instructions: {recipe.get('instructions', [])}
"""
        
        prompt = f"""
You are a professional chef and recipe consultant. Analyze this recipe and suggest improvements:

RECIPE:
{recipe_text}

Provide professional suggestions for:
1. Flavor enhancement
2. Technique improvement
3. Ingredient optimization
4. Presentation ideas
5. Nutritional improvements
6. Cost optimization
7. Time efficiency
8. Storage and serving suggestions

Return in this JSON format:
{{
    "overall_score": 7,
    "improvements": [
        {{
            "category": "Flavor",
            "suggestion": "Add a pinch of smoked paprika for depth",
            "priority": "High",
            "reasoning": "Will enhance the overall flavor profile"
        }},
        {{
            "category": "Technique",
            "suggestion": "Sear the meat first for better texture",
            "priority": "Medium",
            "reasoning": "Creates better caramelization and flavor"
        }}
    ],
    "strengths": [
        "Good ingredient balance",
        "Clear instructions"
    ],
    "weaknesses": [
        "Missing seasoning",
        "Could use more color"
    ],
    "confidence": 0.88
}}

Be constructive and specific in your suggestions.
"""
        
        return prompt
    
    async def _call_ai_service(self, prompt: str) -> str:
        """Call the appropriate AI service based on configuration"""
        
        if self.provider == "openai":
            return await self._call_openai(prompt)
        elif self.provider == "anthropic":
            return await self._call_anthropic(prompt)
        elif self.provider == "google":
            return await self._call_google(prompt)
        elif self.provider == "azure":
            return await self._call_azure(prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        import openai
        
        client = openai.AsyncOpenAI(api_key=self.config["api_key"])
        
        response = await client.chat.completions.create(
            model=self.config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        
        return response.choices[0].message.content
    
    async def _call_anthropic(self, prompt: str) -> str:
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
    
    async def _call_google(self, prompt: str) -> str:
        """Call Google Gemini API"""
        import google.generativeai as genai
        
        genai.configure(api_key=self.config["api_key"])
        model = genai.GenerativeModel(self.config["model"])
        
        response = await model.generate_content_async(prompt)
        return response.text
    
    async def _call_azure(self, prompt: str) -> str:
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
    
    def _parse_recipe_suggestion(self, ai_response: str) -> RecipeSuggestion:
        """Parse AI response into RecipeSuggestion"""
        try:
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in AI response")
            
            json_str = ai_response[json_start:json_end]
            data = json.loads(json_str)
            
            return RecipeSuggestion(
                title=data.get("title", ""),
                description=data.get("description", ""),
                cuisine=data.get("cuisine", ""),
                difficulty=data.get("difficulty", "Medium"),
                prep_time=data.get("prep_time", ""),
                cook_time=data.get("cook_time", ""),
                servings=data.get("servings", 4),
                ingredients=data.get("ingredients", []),
                instructions=data.get("instructions", []),
                tags=data.get("tags", []),
                confidence=data.get("confidence", 0.0)
            )
            
        except Exception as e:
            logger.error(f"Failed to parse recipe suggestion: {e}")
            return self._fallback_recipe()
    
    def _parse_recipe_variation(self, ai_response: str, variation_type: str) -> RecipeVariation:
        """Parse AI response into RecipeVariation"""
        try:
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in AI response")
            
            json_str = ai_response[json_start:json_end]
            data = json.loads(json_str)
            
            return RecipeVariation(
                variation_type=variation_type,
                title=data.get("title", ""),
                description=data.get("description", ""),
                changes=data.get("changes", []),
                new_ingredients=data.get("new_ingredients", []),
                modified_instructions=data.get("modified_instructions", []),
                confidence=data.get("confidence", 0.0)
            )
            
        except Exception as e:
            logger.error(f"Failed to parse recipe variation: {e}")
            return RecipeVariation(
                variation_type=variation_type,
                title="Variation",
                description="AI variation generation failed",
                changes=[],
                new_ingredients=[],
                modified_instructions=[],
                confidence=0.0
            )
    
    def _parse_improvement_suggestions(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response into improvement suggestions"""
        try:
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in AI response")
            
            json_str = ai_response[json_start:json_end]
            data = json.loads(json_str)
            
            return {
                "overall_score": data.get("overall_score", 5),
                "improvements": data.get("improvements", []),
                "strengths": data.get("strengths", []),
                "weaknesses": data.get("weaknesses", []),
                "confidence": data.get("confidence", 0.0)
            }
            
        except Exception as e:
            logger.error(f"Failed to parse improvement suggestions: {e}")
            return {
                "overall_score": 5,
                "improvements": [],
                "strengths": [],
                "weaknesses": [],
                "confidence": 0.0
            }
    
    def _fallback_recipe(self) -> RecipeSuggestion:
        """Fallback recipe when AI is not available"""
        return RecipeSuggestion(
            title="AI Recipe Creation Unavailable",
            description="AI recipe creation is currently disabled",
            cuisine="Unknown",
            difficulty="Medium",
            prep_time="Unknown",
            cook_time="Unknown",
            servings=4,
            ingredients=[],
            instructions=[],
            tags=[],
            confidence=0.0
        )
