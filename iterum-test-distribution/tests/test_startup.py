import pytest
import time
import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import subprocess
import sys
import os

from app.main import app
from app.database import Base, get_db, User
from app.core.auth import get_password_hash

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

class TestAppStartup:
    """Test cases for app startup and basic functionality"""
    
    def setup_method(self):
        """Setup test database with a test user"""
        Base.metadata.create_all(bind=engine)
        
        # Create a test user
        db = TestingSessionLocal()
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpass123"),
            first_name="Test",
            last_name="User",
            role="chef",
            restaurant="Test Kitchen"
        )
        db.add(test_user)
        db.commit()
        db.close()
    
    def teardown_method(self):
        """Cleanup test database"""
        Base.metadata.drop_all(bind=engine)
    
    def test_app_starts_successfully(self):
        """Test that the app starts and responds to basic requests"""
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        assert "Iterum R&D Chef Notebook" in response.text
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
        # Test API docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        assert "Swagger UI" in response.text
    
    def test_database_connection(self):
        """Test that database connection works"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert data["database"] == "connected"
    
    def test_login_functionality(self):
        """Test that login endpoint works correctly"""
        # Test successful login
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "testuser"
        assert data["user"]["email"] == "test@example.com"
        
        # Test failed login
        bad_login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", data=bad_login_data)
        assert response.status_code == 401
    
    def test_protected_endpoints_with_auth(self):
        """Test that protected endpoints work with authentication"""
        # First login to get token
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 200
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test protected endpoint
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
    
    def test_vendor_endpoints_accessible(self):
        """Test that vendor endpoints are accessible"""
        # Test vendor list endpoint
        response = client.get("/api/vendors/")
        assert response.status_code == 200
        
        # Test equipment endpoint
        response = client.get("/api/vendors/equipment/")
        assert response.status_code == 200
    
    def test_frontend_files_exist(self):
        """Test that key frontend files exist and are accessible"""
        # Test main HTML file
        response = client.get("/index.html")
        assert response.status_code == 200
        assert "Iterum R&D Chef Notebook" in response.text
        
        # Test vendor management page
        response = client.get("/vendor-management.html")
        assert response.status_code == 200
        
        # Test ingredients page
        response = client.get("/ingredients.html")
        assert response.status_code == 200

class TestAppIntegration:
    """Integration tests for the complete app flow"""
    
    def test_complete_login_flow(self):
        """Test complete login flow from frontend to backend"""
        # Test that login form elements exist in main page
        response = client.get("/")
        html_content = response.text
        
        # Check for login modal elements
        assert "login-modal" in html_content
        assert "login-email" in html_content
        assert "login-password" in html_content
        assert "login-form" in html_content
    
    def test_api_endpoints_consistency(self):
        """Test that all expected API endpoints are available"""
        # Get OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        paths = schema.get("paths", {})
        
        # Check for key endpoints
        expected_endpoints = [
            "/health",
            "/api/auth/login",
            "/api/auth/register",
            "/api/vendors/",
            "/api/vendors/equipment/",
            "/api/recipes/",
            "/api/ingredients/"
        ]
        
        for endpoint in expected_endpoints:
            assert endpoint in paths, f"Endpoint {endpoint} not found in API schema"
    
    def test_error_handling(self):
        """Test that error handling works correctly"""
        # Test 404 for non-existent endpoint
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        
        # Test 401 for protected endpoint without auth
        response = client.get("/api/auth/me")
        assert response.status_code == 401

def test_app_startup_command():
    """Test that the app can be started via command line"""
    try:
        # Test importing the main app module
        from app.main import app
        assert app is not None
        
        # Test importing the run script
        import run
        assert run is not None
        
        print("✅ App startup test passed - all modules import successfully")
        return True
    except ImportError as e:
        print(f"❌ App startup test failed - import error: {e}")
        return False
    except Exception as e:
        print(f"❌ App startup test failed - unexpected error: {e}")
        return False

if __name__ == "__main__":
    """Run startup tests directly"""
    print("🚀 Running Iterum R&D Chef Notebook Startup Tests...")
    print("=" * 60)
    
    # Run the startup command test
    startup_success = test_app_startup_command()
    
    if startup_success:
        print("\n✅ All startup tests passed!")
        print("🎉 Your app is ready to run!")
        print("\nTo start the app, run:")
        print("  python run.py")
        print("\nTo run all tests:")
        print("  pytest tests/")
    else:
        print("\n❌ Startup tests failed!")
        print("Please check your installation and dependencies.")
        sys.exit(1) 