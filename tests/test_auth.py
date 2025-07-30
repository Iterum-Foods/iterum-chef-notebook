"""
Authentication and authorization tests for Iterum R&D Chef Notebook.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.core.auth import create_access_token, verify_token, get_password_hash, verify_password


@pytest.mark.auth
@pytest.mark.unit
class TestAuthCore:
    """Unit tests for authentication core functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        
        # Should fail with wrong password
        assert verify_password("wrongpassword", hashed) is False
    
    def test_access_token_creation(self):
        """Test JWT token creation and verification"""
        user_data = {"sub": "testuser", "email": "test@example.com"}
        token = create_access_token(data=user_data)
        
        # Token should be a string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Should be able to verify token
        payload = verify_token(token)
        assert payload["sub"] == "testuser"
        assert payload["email"] == "test@example.com"
    
    def test_token_expiration(self):
        """Test token expiration handling"""
        import time
        from app.core.auth import create_access_token
        
        # Create token with very short expiration
        user_data = {"sub": "testuser"}
        token = create_access_token(data=user_data, expires_delta_minutes=0.01)  # 0.6 seconds
        
        # Should work immediately
        payload = verify_token(token)
        assert payload["sub"] == "testuser"
        
        # Wait for expiration
        time.sleep(1)
        
        # Should fail after expiration
        with pytest.raises(Exception):
            verify_token(token)


@pytest.mark.auth
@pytest.mark.api
class TestAuthEndpoints:
    """Integration tests for authentication endpoints"""
    
    def test_register_new_user(self, client):
        """Test user registration"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "first_name": "New",
            "last_name": "User",
            "role": "chef",
            "restaurant": "Test Restaurant"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data  # Should not return password
    
    def test_register_duplicate_user(self, client, test_user):
        """Test registration with duplicate username/email"""
        user_data = {
            "username": test_user.username,
            "email": test_user.email,
            "password": "securepassword123",
            "first_name": "Duplicate",
            "last_name": "User",
            "role": "chef",
            "restaurant": "Test Restaurant"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"].lower()
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        login_data = {
            "username": test_user.username,
            "password": "testpass123"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == test_user.username
        assert data["user"]["email"] == test_user.email
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username"""
        login_data = {
            "username": "nonexistentuser",
            "password": "testpass123"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_missing_credentials(self, client):
        """Test login with missing credentials"""
        # Missing password
        response = client.post("/api/auth/login", data={"username": "testuser"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Missing username
        response = client.post("/api/auth/login", data={"password": "testpass123"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Empty data
        response = client.post("/api/auth/login", data={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.auth
@pytest.mark.integration
class TestProtectedEndpoints:
    """Test protected endpoints requiring authentication"""
    
    def test_access_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without authentication"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "not authenticated" in response.json()["detail"].lower()
    
    def test_access_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_protected_endpoint_with_expired_token(self, client):
        """Test accessing protected endpoint with expired token"""
        # Create expired token
        from app.core.auth import create_access_token
        import time
        
        user_data = {"sub": "testuser"}
        token = create_access_token(data=user_data, expires_delta_minutes=-1)  # Expired
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_protected_endpoint_with_valid_token(self, authenticated_client, test_user):
        """Test accessing protected endpoint with valid authentication"""
        response = authenticated_client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email
        assert data["role"] == test_user.role


@pytest.mark.auth
@pytest.mark.integration
@pytest.mark.slow
class TestUserSessions:
    """Test user session management"""
    
    def test_user_profile_update(self, authenticated_client, test_user):
        """Test updating user profile"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "restaurant": "New Restaurant"
        }
        
        response = authenticated_client.put("/api/auth/profile", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
        assert data["restaurant"] == "New Restaurant"
    
    def test_password_change(self, authenticated_client, test_user):
        """Test password change functionality"""
        password_data = {
            "current_password": "testpass123",
            "new_password": "newsecurepassword456",
            "confirm_password": "newsecurepassword456"
        }
        
        response = authenticated_client.post("/api/auth/change-password", json=password_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Password updated successfully"
    
    def test_password_change_wrong_current_password(self, authenticated_client):
        """Test password change with wrong current password"""
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newsecurepassword456",
            "confirm_password": "newsecurepassword456"
        }
        
        response = authenticated_client.post("/api/auth/change-password", json=password_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "current password" in response.json()["detail"].lower()
    
    def test_password_change_mismatch_confirmation(self, authenticated_client):
        """Test password change with mismatched confirmation"""
        password_data = {
            "current_password": "testpass123",
            "new_password": "newsecurepassword456",
            "confirm_password": "differentpassword"
        }
        
        response = authenticated_client.post("/api/auth/change-password", json=password_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "passwords do not match" in response.json()["detail"].lower() 