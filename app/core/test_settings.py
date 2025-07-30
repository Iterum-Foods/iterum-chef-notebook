"""
Test-specific configuration settings for the Iterum R&D Chef Notebook API.
These settings override the default settings when running tests.
"""

import os
from typing import Optional

# Database settings
TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_DATABASE_ECHO = False  # Set to True for SQL debugging

# Security settings
TEST_SECRET_KEY = "test-secret-key-not-for-production"
TEST_ALGORITHM = "HS256"
TEST_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# API settings
TEST_API_PREFIX = "/api"
TEST_PROJECT_NAME = "Iterum R&D Chef Notebook API - Test Mode"
TEST_VERSION = "2.0.0-test"
TEST_DEBUG = True

# CORS settings for testing
TEST_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
TEST_ALLOW_CREDENTIALS = True

# File upload settings
TEST_UPLOAD_DIR = "test_uploads"
TEST_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
TEST_ALLOWED_EXTENSIONS = {".xlsx", ".xls", ".csv", ".txt", ".pdf", ".docx"}

# External service settings (use mocks in tests)
TEST_WEBSTAURANT_API_ENABLED = False
TEST_FIREBASE_ENABLED = False
TEST_REDIS_ENABLED = False
TEST_CELERY_ENABLED = False

# Logging settings
TEST_LOG_LEVEL = "INFO"
TEST_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Rate limiting (disabled for tests)
TEST_RATE_LIMIT_ENABLED = False

# Cache settings
TEST_CACHE_TTL = 60  # seconds

# Email settings (mock for tests)
TEST_EMAIL_ENABLED = False
TEST_SMTP_HOST = "localhost"
TEST_SMTP_PORT = 1025  # MailHog default port

# Test data settings
TEST_CREATE_SAMPLE_DATA = True
TEST_CLEANUP_ON_EXIT = True

# Performance testing
TEST_RESPONSE_TIME_THRESHOLD = 1.0  # seconds
TEST_MEMORY_THRESHOLD = 100  # MB

class TestConfig:
    """Test configuration class"""
    
    # Database
    DATABASE_URL: str = TEST_DATABASE_URL
    DATABASE_ECHO: bool = TEST_DATABASE_ECHO
    
    # Security
    SECRET_KEY: str = TEST_SECRET_KEY
    ALGORITHM: str = TEST_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = TEST_ACCESS_TOKEN_EXPIRE_MINUTES
    
    # API
    API_PREFIX: str = TEST_API_PREFIX
    PROJECT_NAME: str = TEST_PROJECT_NAME
    VERSION: str = TEST_VERSION
    DEBUG: bool = TEST_DEBUG
    
    # CORS
    ALLOWED_ORIGINS: list = TEST_ALLOWED_ORIGINS
    ALLOW_CREDENTIALS: bool = TEST_ALLOW_CREDENTIALS
    
    # File uploads
    UPLOAD_DIR: str = TEST_UPLOAD_DIR
    MAX_FILE_SIZE: int = TEST_MAX_FILE_SIZE
    ALLOWED_EXTENSIONS: set = TEST_ALLOWED_EXTENSIONS
    
    # External services
    WEBSTAURANT_API_ENABLED: bool = TEST_WEBSTAURANT_API_ENABLED
    FIREBASE_ENABLED: bool = TEST_FIREBASE_ENABLED
    REDIS_ENABLED: bool = TEST_REDIS_ENABLED
    CELERY_ENABLED: bool = TEST_CELERY_ENABLED
    
    # Logging
    LOG_LEVEL: str = TEST_LOG_LEVEL
    LOG_FORMAT: str = TEST_LOG_FORMAT
    
    # Performance
    RESPONSE_TIME_THRESHOLD: float = TEST_RESPONSE_TIME_THRESHOLD
    MEMORY_THRESHOLD: int = TEST_MEMORY_THRESHOLD
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the test database URL"""
        return cls.DATABASE_URL
    
    @classmethod
    def is_testing(cls) -> bool:
        """Check if we're in testing mode"""
        return True
    
    @classmethod
    def get_upload_dir(cls) -> str:
        """Get the test upload directory"""
        return cls.UPLOAD_DIR
    
    @classmethod
    def cleanup_test_files(cls):
        """Clean up test files and directories"""
        import shutil
        import pathlib
        
        try:
            # Remove test upload directory
            test_upload_path = pathlib.Path(cls.UPLOAD_DIR)
            if test_upload_path.exists():
                shutil.rmtree(test_upload_path)
            
            # Remove test database files
            test_db_files = ["test.db", "test_culinary_data.db"]
            for db_file in test_db_files:
                db_path = pathlib.Path(db_file)
                if db_path.exists():
                    db_path.unlink()
                    
        except Exception as e:
            print(f"Warning: Could not clean up test files: {e}")

# Environment-specific overrides
if os.getenv("PYTEST_CURRENT_TEST"):
    # We're running in pytest
    TestConfig.DEBUG = True
    TestConfig.LOG_LEVEL = "DEBUG"

if os.getenv("CI"):
    # We're running in CI/CD
    TestConfig.RESPONSE_TIME_THRESHOLD = 2.0  # More lenient in CI
    TestConfig.LOG_LEVEL = "WARNING"  # Less verbose logging 