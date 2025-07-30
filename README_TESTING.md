# 🧪 Testing Quick Reference

## Quick Commands

```bash
# Quick tests (Windows)
test_quick.bat

# Full test suite (Windows)  
test_full.bat

# Python commands
python run_tests.py --type fast      # Fast tests only
python run_tests.py --type all       # All tests
python run_tests.py --verbose        # Verbose output

# Specific test types
python run_tests.py --type unit      # Unit tests
python run_tests.py --type auth      # Auth tests
python run_tests.py --type recipes   # Recipe tests
python run_tests.py --type api       # API tests

# Direct pytest
pytest                               # All tests
pytest -m unit                       # Unit tests only
pytest -m "not slow"                 # Exclude slow tests
pytest tests/test_auth.py            # Specific file
```

## Test Structure

- `tests/test_startup.py` - App startup tests
- `tests/test_auth.py` - Authentication tests  
- `tests/test_recipes.py` - Recipe functionality tests
- `tests/test_api.py` - API endpoint tests
- `conftest.py` - Shared test fixtures
- `pytest.ini` - Test configuration

## Coverage Reports

```bash
# Generate coverage
pytest --cov=app --cov-report=html

# View coverage report
# Open: test_coverage/python/index.html
```

## Test Categories (Markers)

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.recipes` - Recipe tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.slow` - Slow tests
- `@pytest.mark.external` - External service tests

## Quick Setup

1. Activate virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `test_quick.bat` or `python run_tests.py`

For detailed documentation, see [TESTING_GUIDE.md](TESTING_GUIDE.md) 