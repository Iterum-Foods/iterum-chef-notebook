"""
API endpoint tests for Iterum R&D Chef Notebook.
Tests all main API endpoints for proper functionality, validation, and error handling.
"""

import pytest
from fastapi import status
import json


@pytest.mark.api
@pytest.mark.unit
class TestHealthEndpoints:
    """Test health check and system status endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns app information"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "Iterum R&D Chef Notebook" in data["message"]
        assert data["version"] == "2.0.0"
        assert data["status"] == "running"
    
    def test_health_endpoint(self, client):
        """Test basic health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "iterum-rnd-api"
    
    def test_detailed_health_endpoint(self, client):
        """Test detailed health check with system information"""
        response = client.get("/health/detailed")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "checks" in data
        assert "system_resources" in data["checks"]
        assert "database" in data["checks"]


@pytest.mark.api
@pytest.mark.integration
class TestRecipeEndpoints:
    """Test recipe management API endpoints"""
    
    def test_get_recipes_list(self, authenticated_client):
        """Test retrieving list of recipes"""
        response = authenticated_client.get("/api/recipes/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_recipe(self, authenticated_client, sample_recipe):
        """Test creating a new recipe"""
        response = authenticated_client.post("/api/recipes/", json=sample_recipe)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_recipe["title"]
        assert data["description"] == sample_recipe["description"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_recipe_invalid_data(self, authenticated_client):
        """Test creating recipe with invalid data"""
        invalid_recipe = {
            "title": "",  # Empty title should be invalid
            "servings": -1  # Negative servings should be invalid
        }
        
        response = authenticated_client.post("/api/recipes/", json=invalid_recipe)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_recipe_by_id(self, authenticated_client, sample_recipe):
        """Test retrieving a specific recipe by ID"""
        # First create a recipe
        create_response = authenticated_client.post("/api/recipes/", json=sample_recipe)
        created_recipe = create_response.json()
        recipe_id = created_recipe["id"]
        
        # Then retrieve it
        response = authenticated_client.get(f"/api/recipes/{recipe_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == recipe_id
        assert data["title"] == sample_recipe["title"]
    
    def test_get_nonexistent_recipe(self, authenticated_client):
        """Test retrieving a non-existent recipe"""
        response = authenticated_client.get("/api/recipes/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_recipe(self, authenticated_client, sample_recipe):
        """Test updating an existing recipe"""
        # Create a recipe
        create_response = authenticated_client.post("/api/recipes/", json=sample_recipe)
        created_recipe = create_response.json()
        recipe_id = created_recipe["id"]
        
        # Update it
        update_data = {
            "title": "Updated Recipe Title",
            "description": "Updated description"
        }
        response = authenticated_client.put(f"/api/recipes/{recipe_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Recipe Title"
        assert data["description"] == "Updated description"
    
    def test_delete_recipe(self, authenticated_client, sample_recipe):
        """Test deleting a recipe"""
        # Create a recipe
        create_response = authenticated_client.post("/api/recipes/", json=sample_recipe)
        created_recipe = create_response.json()
        recipe_id = created_recipe["id"]
        
        # Delete it
        response = authenticated_client.delete(f"/api/recipes/{recipe_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's gone
        get_response = authenticated_client.get(f"/api/recipes/{recipe_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.api
@pytest.mark.integration
class TestIngredientEndpoints:
    """Test ingredient management API endpoints"""
    
    def test_get_ingredients_list(self, authenticated_client):
        """Test retrieving list of ingredients"""
        response = authenticated_client.get("/api/ingredients/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_ingredients(self, authenticated_client):
        """Test searching ingredients by name"""
        response = authenticated_client.get("/api/ingredients/search?q=flour")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_ingredient(self, authenticated_client):
        """Test creating a new ingredient"""
        ingredient_data = {
            "name": "Test Ingredient",
            "category": "Pantry",
            "unit": "grams",
            "density": 1.0,
            "allergens": ["gluten"],
            "dietary_info": ["vegetarian"]
        }
        
        response = authenticated_client.post("/api/ingredients/", json=ingredient_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Test Ingredient"
        assert data["category"] == "Pantry"


@pytest.mark.api
@pytest.mark.integration
class TestVendorEndpoints:
    """Test vendor and equipment API endpoints"""
    
    def test_get_vendors_list(self, client):
        """Test retrieving list of vendors"""
        response = client.get("/api/vendors/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_equipment_list(self, client):
        """Test retrieving list of equipment"""
        response = client.get("/api/vendors/equipment/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_vendors(self, client):
        """Test searching vendors"""
        response = client.get("/api/vendors/search?q=restaurant")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.api
@pytest.mark.integration
class TestUploadEndpoints:
    """Test file upload API endpoints"""
    
    def test_upload_recipe_file(self, authenticated_client, mock_recipe_file):
        """Test uploading a recipe file"""
        files = {"file": (mock_recipe_file["filename"], mock_recipe_file["content"], mock_recipe_file["content_type"])}
        
        response = authenticated_client.post("/api/uploads/recipe", files=files)
        
        # Note: This test may fail if the actual upload processing isn't mocked
        # The response code will depend on the implementation
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY]
    
    def test_upload_invalid_file_type(self, authenticated_client):
        """Test uploading an invalid file type"""
        files = {"file": ("test.exe", b"invalid content", "application/octet-stream")}
        
        response = authenticated_client.post("/api/uploads/recipe", files=files)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.api
@pytest.mark.integration
class TestDataEndpoints:
    """Test data export/import API endpoints"""
    
    def test_export_recipes(self, authenticated_client):
        """Test exporting recipes data"""
        response = authenticated_client.get("/api/data/export/recipes")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] in ["application/json", "text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    
    def test_get_statistics(self, authenticated_client):
        """Test getting application statistics"""
        response = authenticated_client.get("/api/data/statistics")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "recipe_count" in data
        assert "ingredient_count" in data


@pytest.mark.api
@pytest.mark.external
class TestIntegrationEndpoints:
    """Test external integration API endpoints"""
    
    def test_webstaurant_search(self, authenticated_client):
        """Test WebstaurantStore integration search"""
        response = authenticated_client.get("/api/integrations/webstaurant/search?q=pan")
        
        # This test requires actual integration to be working
        # Should handle both success and mock responses
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]
    
    def test_integration_health(self, client):
        """Test integration services health check"""
        response = client.get("/api/integrations/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "webstaurant" in data
        assert "firebase" in data


@pytest.mark.api
@pytest.mark.unit
class TestErrorHandling:
    """Test API error handling and validation"""
    
    def test_404_on_invalid_endpoint(self, client):
        """Test 404 response for non-existent endpoints"""
        response = client.get("/api/nonexistent")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_405_on_invalid_method(self, client):
        """Test 405 response for invalid HTTP methods"""
        response = client.delete("/")  # Root endpoint doesn't support DELETE
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_422_on_invalid_json(self, authenticated_client):
        """Test 422 response for invalid JSON data"""
        response = authenticated_client.post(
            "/api/recipes/",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_request_validation_errors(self, authenticated_client):
        """Test validation error responses"""
        # Missing required fields
        invalid_data = {"title": ""}  # Empty title
        response = authenticated_client.post("/api/recipes/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)


@pytest.mark.api
@pytest.mark.slow
class TestRateLimiting:
    """Test API rate limiting (if implemented)"""
    
    @pytest.mark.skip(reason="Rate limiting not implemented yet")
    def test_rate_limit_enforcement(self, client):
        """Test that rate limiting is enforced"""
        # Make many rapid requests
        for _ in range(100):
            response = client.get("/")
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        else:
            pytest.fail("Rate limiting not enforced")
    
    @pytest.mark.skip(reason="Rate limiting not implemented yet")
    def test_rate_limit_reset(self, client):
        """Test that rate limit resets after time period"""
        import time
        
        # Trigger rate limit
        for _ in range(100):
            response = client.get("/")
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        
        # Wait for reset
        time.sleep(60)
        
        # Should work again
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK 