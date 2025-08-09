"""
Configuration management for Iterum R&D Chef Notebook
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    # App settings
    app_name: str = "Iterum R&D Chef Notebook"
    app_version: str = "2.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    frontend_port: int = Field(default=8080, env="FRONTEND_PORT")
    
    # Database settings
    database_url: str = Field(default="sqlite:///./culinary_data.db", env="DATABASE_URL")
    
    # Security settings
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # File upload settings
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_file_types: str = Field(default=".pdf,.docx,.xlsx,.txt", env="ALLOWED_FILE_TYPES")
    
    # Recipe processing settings
    auto_process_uploads: bool = Field(default=True, env="AUTO_PROCESS_UPLOADS")
    folder_watcher_enabled: bool = Field(default=True, env="FOLDER_WATCHER_ENABLED")
    incoming_recipes_dir: str = Field(default="./incoming_recipes", env="INCOMING_RECIPES_DIR")
    
    # Equipment database settings
    equipment_database_path: str = Field(default="./equipment_database.csv", env="EQUIPMENT_DATABASE_PATH")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/iterum_app.log", env="LOG_FILE")
    
    # Firebase settings (optional)
    firebase_config_path: Optional[str] = Field(default=None, env="FIREBASE_CONFIG_PATH")
    
    # HTTPS/SSL settings
    https_enabled: bool = Field(default=False, env="HTTPS_ENABLED")
    ssl_cert_path: str = Field(default="./certs/localhost.pem", env="SSL_CERT_PATH")
    ssl_key_path: str = Field(default="./certs/localhost-key.pem", env="SSL_KEY_PATH")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.debug or os.getenv("ENVIRONMENT", "development").lower() == "development"
    
    @property
    def allowed_extensions(self) -> list[str]:
        """Get list of allowed file extensions"""
        return [ext.strip() for ext in self.allowed_file_types.split(",")]

# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get or create settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 