# Testing Guide - Iterum R&D Chef Notebook

This guide covers all aspects of testing for the Iterum R&D Chef Notebook application, including setup, running tests, and contributing new tests.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Coverage Reports](#coverage-reports)
- [Writing New Tests](#writing-new-tests)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (optional, for frontend tests)
- Git

### Setup

1. **Clone and navigate to the project:**
```bash
git clone <repository-url>
cd "Iterum App"
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
npm install  # Optional, for frontend tests
```

### Running Quick Tests

```bash
# Windows
test_quick.bat

# Or directly with Python
python run_tests.py --type fast --skip-lint --skip-perf
```

## 🏗️ Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_startup.py          # Application startup tests
├── test_recipes.py          # Recipe functionality tests
├── test_auth.py             # Authentication/authorization tests
├── test_api.py              # API endpoint tests
└── test_integration.py      # Integration tests (if needed)

Configuration Files:
├── pytest.ini              # Pytest configuration
├── jest.config.js           # Jest configuration for frontend
├── .coveragerc              # Coverage reporting configuration
└── conftest.py              # Shared test fixtures
```

## 🏃‍♂️ Running Tests

### Command Line Options

#### Basic Test Commands

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --type unit
python run_tests.py --type integration
python run_tests.py --type auth
python run_tests.py --type recipes
python run_tests.py --type api

# Run fast tests (exclude slow tests)
python run_tests.py --type fast

# Verbose output
python run_tests.py --verbose
```

#### Test Execution Options

```bash
# Skip specific test categories
python run_tests.py --skip-js        # Skip JavaScript tests
python run_tests.py --skip-lint      # Skip linting
python run_tests.py --skip-perf      # Skip performance tests

# Combine options
python run_tests.py --type unit --skip-lint --verbose
```

#### Direct Pytest Commands

```bash
# Run all tests with pytest
pytest

# Run specific test files
pytest tests/test_recipes.py
pytest tests/test_auth.py -v

# Run specific test classes
pytest tests/test_auth.py::TestAuthCore

# Run specific test methods
pytest tests/test_auth.py::TestAuthCore::test_password_hashing

# Run with markers
pytest -m unit
pytest -m "auth and not slow"
pytest -m "not external"
```

### Batch Scripts (Windows)

```bash
# Quick tests (fast, no linting)
test_quick.bat

# Full test suite
test_full.bat

# CI/CD tests
test_ci.bat
```

## 🏷️ Test Categories

Tests are organized using pytest markers:

### Core Markers

- **`@pytest.mark.unit`** - Unit tests for individual functions/classes
- **`@pytest.mark.integration`** - Integration tests for component interaction
- **`@pytest.mark.api`** - API endpoint tests
- **`@pytest.mark.slow`** - Tests that take longer to run

### Feature Markers

- **`@pytest.mark.auth`** - Authentication/authorization tests
- **`@pytest.mark.recipes`** - Recipe functionality tests
- **`@pytest.mark.frontend`** - Frontend JavaScript tests
- **`@pytest.mark.database`** - Database-related tests
- **`@pytest.mark.external`** - Tests requiring external services

### Running Specific Categories

```bash
# Run only unit tests
pytest -m unit

# Run integration tests excluding slow ones
pytest -m "integration and not slow"

# Run auth-related tests
pytest -m auth

# Run everything except external service tests
pytest -m "not external"
```

## 📊 Coverage Reports

### Generating Coverage Reports

```bash
# Python coverage with HTML report
pytest --cov=app --cov-report=html:test_coverage/python

# Python coverage with terminal output
pytest --cov=app --cov-report=term-missing

# Combined coverage (Python + JavaScript)
python run_tests.py --verbose
```

### Viewing Reports

- **Python Coverage**: Open `test_coverage/python/index.html`
- **JavaScript Coverage**: Open `test_coverage/frontend/index.html`
- **Combined Report**: Check `test_coverage/test_report.json`

### Coverage Thresholds

- **Minimum Coverage**: 60%
- **Target Coverage**: 80%
- **High-Quality Coverage**: 90%+

## ✍️ Writing New Tests

### Test File Structure

```python
"""
Module description for your tests.
"""

import pytest
from fastapi import status
# ... other imports

@pytest.mark.category_name
@pytest.mark.test_type
class TestFeatureName:
    """Test class for specific feature"""
    
    def test_specific_functionality(self, client):
        """Test description"""
        # Arrange
        test_data = {"key": "value"}
        
        # Act
        response = client.post("/api/endpoint", json=test_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["key"] == "value"
```

### Available Fixtures (from conftest.py)

- **`client`** - FastAPI test client
- **`test_db`** - Test database session
- **`test_user`** - Pre-created test user
- **`authenticated_client`** - Client with authentication token
- **`sample_recipe`** - Sample recipe data for testing
- **`mock_recipe_file`** - Mock file upload data

### Test Naming Conventions

- **Test files**: `test_*.py`
- **Test classes**: `TestFeatureName`
- **Test methods**: `test_specific_behavior`
- **Use descriptive names**: `test_login_with_invalid_password`

### Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One assertion per test** (when possible)
3. **Use descriptive test names**
4. **Test edge cases and error conditions**
5. **Use appropriate markers**
6. **Clean up test data** (handled by fixtures)
7. **Mock external dependencies**

### Example: Adding a New Test

```python
@pytest.mark.recipes
@pytest.mark.integration
def test_recipe_scaling_calculation(self, authenticated_client, sample_recipe):
    """Test that recipe scaling correctly adjusts ingredient quantities"""
    # Create a recipe
    response = authenticated_client.post("/api/recipes/", json=sample_recipe)
    recipe_id = response.json()["id"]
    
    # Scale recipe from 4 to 8 servings
    scale_data = {"servings": 8}
    response = authenticated_client.post(f"/api/recipes/{recipe_id}/scale", json=scale_data)
    
    assert response.status_code == status.HTTP_200_OK
    scaled_recipe = response.json()
    
    # Verify scaling factor applied correctly
    original_flour = 2.0  # from sample_recipe
    expected_flour = 4.0  # doubled for 8 servings
    assert scaled_recipe["ingredients"][0]["quantity"] == expected_flour
```

## 🔄 CI/CD Integration

### GitHub Actions (Example)

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python run_tests.py --type all --verbose
```

### Local CI Testing

```bash
# Simulate CI environment
test_ci.bat

# Or with environment variable
set CI=1
python run_tests.py --type all --no-cleanup
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in the project root and virtual environment is activated
cd "Iterum App"
venv\Scripts\activate  # Windows
python -m pytest
```

#### 2. Database Connection Errors

```bash
# Error: Database connection failed
# Solution: Tests should use in-memory database automatically
# Check conftest.py configuration
```

#### 3. Authentication Test Failures

```bash
# Error: 401 Unauthorized in tests
# Solution: Use authenticated_client fixture or verify test_user creation
def test_protected_endpoint(self, authenticated_client):
    response = authenticated_client.get("/api/protected")
    # Should work with authentication
```

#### 4. Slow Test Performance

```bash
# Solution: Use fast test category
python run_tests.py --type fast

# Or exclude slow tests
pytest -m "not slow"
```

#### 5. Coverage Too Low

```bash
# Check which files need more tests
pytest --cov=app --cov-report=term-missing

# Focus on files with low coverage
pytest --cov=app/routers --cov-report=html
```

### Debugging Tests

```bash
# Run single test with verbose output
pytest tests/test_auth.py::TestAuthCore::test_password_hashing -v -s

# Run with Python debugger
pytest tests/test_auth.py --pdb

# Run with print statements (use -s flag)
pytest tests/test_auth.py -s
```

### Performance Testing

```bash
# Run performance tests only
python run_tests.py --type all --skip-js --skip-lint

# Check test execution time
pytest --durations=10
```

## 📈 Continuous Improvement

### Adding New Test Categories

1. Add marker to `pytest.ini`:
```ini
markers =
    new_feature: tests for new feature
```

2. Use in tests:
```python
@pytest.mark.new_feature
def test_new_functionality():
    pass
```

3. Run category:
```bash
pytest -m new_feature
```

### Measuring Test Quality

- **Coverage percentage** (aim for 80%+)
- **Test execution time** (keep under 30 seconds for fast tests)
- **Test reliability** (no flaky tests)
- **Code quality** (linting passes)

### Regular Maintenance

- Review and update test data monthly
- Remove obsolete tests for deprecated features
- Add tests for new features immediately
- Monitor test performance and optimize slow tests
- Update documentation as the codebase evolves

---

## 📞 Support

For questions about testing:

1. Check this guide first
2. Review existing test files for examples
3. Run tests with `--verbose` for detailed output
4. Check the test report at `test_coverage/test_report.json`

Happy testing! 🧪✨ 