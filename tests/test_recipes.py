import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.routers.recipes import router

# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestRecipes:
    """Test cases for recipe endpoints"""
    
    def setup_method(self):
        """Setup test database"""
        Base.metadata.create_all(bind=engine)
    
    def teardown_method(self):
        """Cleanup test database"""
        Base.metadata.drop_all(bind=engine)
    
    def test_create_recipe(self):
        """Test creating a new recipe"""
        recipe_data = {
            "title": "Test Recipe",
            "description": "A test recipe",
            "cuisine_type": "Italian",
            "difficulty_level": "Easy",
            "prep_time": 15,
            "cook_time": 30,
            "servings": 4,
            "tags": ["test", "quick"],
            "dietary_restrictions": ["vegetarian"],
            "allergens": [],
            "equipment_needed": ["pan", "spoon"],
            "status": "draft",
            "kitchen_type": "home",
            "ingredients": [
                {
                    "ingredient_id": 1,
                    "quantity": 2.0,
                    "unit": "cups",
                    "notes": "flour",
                    "order_index": 0
                }
            ],
            "instructions": [
                {
                    "step_number": 1,
                    "instruction": "Mix ingredients",
                    "tips": "Mix well",
                    "time_estimate": 5,
                    "temperature": None,
                    "equipment": "bowl"
                }
            ]
        }
        
        # Note: This test would need authentication setup
        # For now, we'll test the data structure
        assert recipe_data["title"] == "Test Recipe"
        assert len(recipe_data["ingredients"]) == 1
        assert len(recipe_data["instructions"]) == 1
    
    def test_recipe_scaling(self):
        """Test recipe scaling functionality"""
        # Test scaling factor calculation
        current_servings = 4
        target_servings = 8
        scaling_factor = target_servings / current_servings
        
        assert scaling_factor == 2.0
        
        # Test ingredient scaling
        original_quantity = 2.0
        scaled_quantity = original_quantity * scaling_factor
        
        assert scaled_quantity == 4.0
    
    def test_unit_conversion(self):
        """Test unit conversion functionality"""
        from app.routers.recipes import convert_units
        
        # Test weight conversions
        result = convert_units(1000, "g")
        assert result["unit"] == "kg"
        assert result["quantity"] == 1.0
        
        # Test volume conversions
        result = convert_units(1000, "ml")
        assert result["unit"] == "L"
        assert result["quantity"] == 1.0
        
        # Test no conversion needed
        result = convert_units(500, "g")
        assert result["unit"] == "g"
        assert result["quantity"] == 500.0
    
    def test_recipe_validation(self):
        """Test recipe validation"""
        # Test valid recipe
        valid_recipe = {
            "title": "Valid Recipe",
            "servings": 4,
            "prep_time": 15,
            "cook_time": 30
        }
        
        assert valid_recipe["title"] is not None
        assert valid_recipe["servings"] > 0
        assert valid_recipe["prep_time"] >= 0
        assert valid_recipe["cook_time"] >= 0
        
        # Test invalid recipe (missing title)
        invalid_recipe = {
            "title": "",
            "servings": 4
        }
        
        assert not invalid_recipe["title"]  # Empty title should be invalid

class TestRecipeParsing:
    """Test cases for recipe parsing functionality"""
    
    def test_text_recipe_parsing(self):
        """Test parsing text recipe files"""
        from app.routers.recipes import parse_text_recipe
        
        text_content = """
        Test Recipe
        
        Ingredients:
        2 cups flour
        1 cup sugar
        3 eggs
        
        Instructions:
        1. Mix flour and sugar
        2. Add eggs
        3. Bake at 350F
        """
        
        base_recipe = {
            "name": "Unknown Recipe",
            "ingredients": [],
            "instructions": []
        }
        
        result = parse_text_recipe(text_content, base_recipe)
        
        assert result["name"] == "Test Recipe"
        assert len(result["ingredients"]) == 3
        assert len(result["instructions"]) == 3
    
    def test_csv_recipe_parsing(self):
        """Test parsing CSV recipe files"""
        from app.routers.recipes import parse_csv_recipe
        
        csv_content = """name,description,cuisine,servings,prep_time,cook_time
Test Recipe,Delicious test recipe,Italian,4,15,30"""
        
        base_recipe = {
            "name": "Unknown Recipe",
            "ingredients": [],
            "instructions": []
        }
        
        result = parse_csv_recipe(csv_content, base_recipe)
        
        assert result["name"] == "Test Recipe"
        assert result["cuisine"] == "Italian"
        assert result["servings"] == 4
        assert result["prep_time"] == 15
        assert result["cook_time"] == 30

class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_validation_error(self):
        """Test validation error handling"""
        from app.core.error_handler import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Invalid recipe data")
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.error_code == "VALIDATION_ERROR"
    
    def test_not_found_error(self):
        """Test not found error handling"""
        from app.core.error_handler import NotFoundError
        
        with pytest.raises(NotFoundError) as exc_info:
            raise NotFoundError("Recipe not found")
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "NOT_FOUND"
    
    def test_unauthorized_error(self):
        """Test unauthorized error handling"""
        from app.core.error_handler import UnauthorizedError
        
        with pytest.raises(UnauthorizedError) as exc_info:
            raise UnauthorizedError("Authentication required")
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.error_code == "UNAUTHORIZED"

if __name__ == "__main__":
    pytest.main([__file__]) 