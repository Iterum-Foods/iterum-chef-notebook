"""
Test package for Iterum R&D Chef Notebook application.

This package contains all test modules organized by functionality:
- test_startup.py: Application startup and health checks
- test_recipes.py: Recipe management functionality
- test_auth.py: Authentication and authorization
- test_api.py: API endpoint testing
- test_integration.py: Integration tests
- test_performance.py: Performance testing

Test categories (pytest markers):
- unit: Unit tests for individual functions/classes
- integration: Integration tests for component interaction
- auth: Authentication/authorization related tests
- recipes: Recipe functionality tests
- api: API endpoint tests
- slow: Tests that take longer to run
- external: Tests requiring external services

Usage:
    # Run all tests
    pytest

    # Run specific test categories
    pytest -m unit
    pytest -m "not slow"
    pytest -m "auth and not integration"

    # Run specific test files
    pytest tests/test_recipes.py
    pytest tests/test_auth.py -v

    # Run with coverage
    pytest --cov=app --cov-report=html

Environment:
    Tests use in-memory SQLite database by default.
    External services are mocked unless specifically testing integrations.
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test configuration
TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_SECRET_KEY = "test-secret-key-for-testing-only"

# Mark as test environment
os.environ["TESTING"] = "1" 