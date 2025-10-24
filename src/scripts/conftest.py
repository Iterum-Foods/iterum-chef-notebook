import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db, User
from app.core.auth import get_password_hash


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test function."""
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    if get_db in app.dependency_overrides:
        del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def client(test_db) -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def test_user(test_db):
    """Create a test user in the database."""
    db = test_db()
    
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        first_name="Test",
        last_name="User",
        role="chef",
        restaurant="Test Kitchen"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return user


@pytest.fixture(scope="function")
def authenticated_client(client, test_user):
    """Create a test client with an authenticated user."""
    login_data = {
        "username": test_user.username,
        "password": "testpass123"
    }
    response = client.post("/api/auth/login", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client


@pytest.fixture
def sample_recipe():
    """Create sample recipe data for testing."""
    return {
        "title": "Test Recipe",
        "description": "A delicious test recipe",
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
                "notes": "all-purpose flour",
                "order_index": 0
            },
            {
                "ingredient_id": 2,
                "quantity": 1.0,
                "unit": "cup",
                "notes": "sugar",
                "order_index": 1
            }
        ],
        "instructions": [
            {
                "step_number": 1,
                "instruction": "Mix dry ingredients in a large bowl",
                "tips": "Sift flour for better texture",
                "time_estimate": 5,
                "temperature": None,
                "equipment": "bowl"
            },
            {
                "step_number": 2,
                "instruction": "Add wet ingredients and mix until combined",
                "tips": "Don't overmix",
                "time_estimate": 10,
                "temperature": None,
                "equipment": "whisk"
            }
        ]
    }


@pytest.fixture
def mock_recipe_file():
    """Create mock recipe file content for testing uploads."""
    return {
        "filename": "test_recipe.xlsx",
        "content": b"Mock Excel content",
        "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }


# Pytest markers for test organization
pytest_markers = [
    "unit: Unit tests",
    "integration: Integration tests", 
    "slow: Slow running tests",
    "auth: Authentication related tests",
    "recipes: Recipe functionality tests",
    "api: API endpoint tests",
    "frontend: Frontend JavaScript tests",
    "database: Database related tests",
    "external: Tests requiring external services"
] 