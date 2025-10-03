"""
AI Configuration and Settings for Iterum R&D Chef Notebook
Handles AI provider configuration, API keys, and feature toggles
"""

from pydantic import BaseSettings
from typing import Optional, Dict, Any
import os
from enum import Enum

class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"

class AISettings(BaseSettings):
    """AI configuration settings"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    azure_api_key: Optional[str] = None
    azure_endpoint: Optional[str] = None
    
    # Feature Toggles
    enable_ai_features: bool = True
    enable_recipe_ai: bool = True
    enable_menu_ai: bool = True
    enable_ingredient_ai: bool = True
    enable_chef_assistant: bool = True
    
    # AI Model Settings
    default_llm_model: str = "gpt-4"
    fallback_llm_model: str = "gpt-3.5-turbo"
    vision_model: str = "gpt-4-vision-preview"
    
    # Performance Settings
    ai_confidence_threshold: float = 0.8
    max_tokens: int = 4000
    temperature: float = 0.1
    timeout_seconds: int = 30
    
    # Cost Management
    max_cost_per_request: float = 0.50
    daily_cost_limit: float = 10.0
    enable_cost_tracking: bool = True
    
    # Recipe AI Settings
    recipe_parsing_enhancement: bool = True
    ingredient_standardization: bool = True
    nutritional_analysis: bool = True
    cost_estimation: bool = True
    technique_analysis: bool = True
    
    # Menu AI Settings
    menu_structure_analysis: bool = True
    price_analysis: bool = True
    profit_margin_estimation: bool = True
    popularity_prediction: bool = True
    
    # Chef Assistant Settings
    professional_insights: bool = True
    technique_optimization: bool = True
    flavor_analysis: bool = True
    presentation_suggestions: bool = True
    wine_pairing: bool = True
    
    class Config:
        env_file = ".env"
        env_prefix = "AI_"
        case_sensitive = False

# Global AI settings instance
ai_settings = AISettings()

def get_ai_settings() -> AISettings:
    """Get AI settings instance"""
    return ai_settings

def is_ai_enabled() -> bool:
    """Check if AI features are enabled"""
    return ai_settings.enable_ai_features

def get_primary_ai_provider() -> AIProvider:
    """Get the primary AI provider based on available API keys"""
    if ai_settings.openai_api_key:
        return AIProvider.OPENAI
    elif ai_settings.anthropic_api_key:
        return AIProvider.ANTHROPIC
    elif ai_settings.google_api_key:
        return AIProvider.GOOGLE
    elif ai_settings.azure_api_key:
        return AIProvider.AZURE
    else:
        return AIProvider.OPENAI  # Default fallback

def get_ai_provider_config(provider: AIProvider) -> Dict[str, Any]:
    """Get configuration for specific AI provider"""
    configs = {
        AIProvider.OPENAI: {
            "api_key": ai_settings.openai_api_key,
            "model": ai_settings.default_llm_model,
            "temperature": ai_settings.temperature,
            "max_tokens": ai_settings.max_tokens
        },
        AIProvider.ANTHROPIC: {
            "api_key": ai_settings.anthropic_api_key,
            "model": "claude-3-sonnet-20240229",
            "temperature": ai_settings.temperature,
            "max_tokens": ai_settings.max_tokens
        },
        AIProvider.GOOGLE: {
            "api_key": ai_settings.google_api_key,
            "model": "gemini-pro",
            "temperature": ai_settings.temperature
        },
        AIProvider.AZURE: {
            "api_key": ai_settings.azure_api_key,
            "endpoint": ai_settings.azure_endpoint,
            "model": "gpt-4",
            "temperature": ai_settings.temperature
        }
    }
    return configs.get(provider, {})

def validate_ai_configuration() -> Dict[str, bool]:
    """Validate AI configuration and return status"""
    validation = {
        "ai_enabled": ai_settings.enable_ai_features,
        "openai_configured": bool(ai_settings.openai_api_key),
        "anthropic_configured": bool(ai_settings.anthropic_api_key),
        "google_configured": bool(ai_settings.google_api_key),
        "azure_configured": bool(ai_settings.azure_api_key),
        "has_any_provider": any([
            ai_settings.openai_api_key,
            ai_settings.anthropic_api_key,
            ai_settings.google_api_key,
            ai_settings.azure_api_key
        ])
    }
    return validation

# AI Feature Flags
class AIFeatures:
    """AI feature flags for easy toggling"""
    
    @staticmethod
    def recipe_parsing_enabled() -> bool:
        return ai_settings.enable_ai_features and ai_settings.enable_recipe_ai
    
    @staticmethod
    def menu_parsing_enabled() -> bool:
        return ai_settings.enable_ai_features and ai_settings.enable_menu_ai
    
    @staticmethod
    def ingredient_ai_enabled() -> bool:
        return ai_settings.enable_ai_features and ai_settings.enable_ingredient_ai
    
    @staticmethod
    def chef_assistant_enabled() -> bool:
        return ai_settings.enable_ai_features and ai_settings.enable_chef_assistant
    
    @staticmethod
    def nutritional_analysis_enabled() -> bool:
        return ai_settings.enable_ai_features and ai_settings.nutritional_analysis
    
    @staticmethod
    def cost_estimation_enabled() -> bool:
        return ai_settings.enable_ai_features and ai_settings.cost_estimation
