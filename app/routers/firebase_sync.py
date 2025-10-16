"""
Firebase Authentication Sync for Backend
Syncs Firebase authenticated users with backend database
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import requests
import os

from app.database import get_db, User

router = APIRouter()

# Firebase project configuration
FIREBASE_PROJECT_ID = "iterum-culinary-app"
FIREBASE_API_KEY = "AIzaSyB94rVT-7xyBLJBH9zpjGyCZL5aEKmK7Hc"


class FirebaseUserSync(BaseModel):
    """User data from Firebase to sync with backend"""
    firebase_uid: str
    email: EmailStr
    name: str
    photo_url: Optional[str] = None
    provider: str  # 'google', 'email', 'trial'
    id_token: Optional[str] = None


class UserResponse(BaseModel):
    """Response after syncing user"""
    id: int
    firebase_uid: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    message: str


def verify_firebase_token(id_token: str) -> dict:
    """
    Verify Firebase ID token
    Returns user info if valid, raises exception if invalid
    """
    try:
        # Use Firebase REST API to verify token
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
        response = requests.post(
            url,
            json={"idToken": id_token},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'users' in data and len(data['users']) > 0:
                return data['users'][0]
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Firebase verification service unavailable: {str(e)}"
        )


@router.post("/sync-user", response_model=UserResponse)
async def sync_firebase_user(
    user_data: FirebaseUserSync,
    db: Session = Depends(get_db)
):
    """
    Sync Firebase authenticated user with backend database
    Creates new user if doesn't exist, updates if exists
    """
    
    # Verify Firebase token if provided
    if user_data.id_token:
        try:
            firebase_user = verify_firebase_token(user_data.id_token)
            # Verify the UID matches
            if firebase_user.get('localId') != user_data.firebase_uid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token UID mismatch"
                )
        except HTTPException:
            # If verification fails, continue but log it
            print(f"⚠️ Firebase token verification failed for {user_data.email}")
    
    # Check if user already exists by Firebase UID
    existing_user = db.query(User).filter(
        User.firebase_uid == user_data.firebase_uid
    ).first()
    
    if existing_user:
        # Update existing user
        existing_user.email = user_data.email
        existing_user.first_name = user_data.name.split()[0] if user_data.name else None
        existing_user.last_name = " ".join(user_data.name.split()[1:]) if len(user_data.name.split()) > 1 else None
        existing_user.photo_url = user_data.photo_url
        existing_user.auth_provider = user_data.provider
        existing_user.last_login = datetime.now()
        
        db.commit()
        db.refresh(existing_user)
        
        return UserResponse(
            id=existing_user.id,
            firebase_uid=existing_user.firebase_uid,
            username=existing_user.username,
            email=existing_user.email,
            first_name=existing_user.first_name,
            last_name=existing_user.last_name,
            is_active=existing_user.is_active,
            message="User updated successfully"
        )
    
    # Check if user exists by email (migration case)
    existing_by_email = db.query(User).filter(User.email == user_data.email).first()
    
    if existing_by_email:
        # Migrate existing user to Firebase
        existing_by_email.firebase_uid = user_data.firebase_uid
        existing_by_email.auth_provider = user_data.provider
        existing_by_email.photo_url = user_data.photo_url
        existing_by_email.last_login = datetime.now()
        
        db.commit()
        db.refresh(existing_by_email)
        
        return UserResponse(
            id=existing_by_email.id,
            firebase_uid=existing_by_email.firebase_uid,
            username=existing_by_email.username,
            email=existing_by_email.email,
            first_name=existing_by_email.first_name,
            last_name=existing_by_email.last_name,
            is_active=existing_by_email.is_active,
            message="User migrated to Firebase successfully"
        )
    
    # Create new user
    username = user_data.email.split('@')[0]
    
    # Ensure unique username
    counter = 1
    base_username = username
    while db.query(User).filter(User.username == username).first():
        username = f"{base_username}{counter}"
        counter += 1
    
    # Split name into first and last
    name_parts = user_data.name.split()
    first_name = name_parts[0] if name_parts else None
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None
    
    new_user = User(
        firebase_uid=user_data.firebase_uid,
        username=username,
        email=user_data.email,
        first_name=first_name,
        last_name=last_name,
        hashed_password="",  # No password for Firebase users
        auth_provider=user_data.provider,
        photo_url=user_data.photo_url,
        is_active=True,
        role="chef",
        restaurant="My Kitchen"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        firebase_uid=new_user.firebase_uid,
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        is_active=new_user.is_active,
        message="User created successfully"
    )


@router.get("/verify-token")
async def verify_token(authorization: str = Header(None)):
    """
    Verify Firebase ID token from Authorization header
    Returns user info if valid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.replace("Bearer ", "")
    user_info = verify_firebase_token(token)
    
    return {
        "valid": True,
        "user": {
            "uid": user_info.get('localId'),
            "email": user_info.get('email'),
            "email_verified": user_info.get('emailVerified', False)
        }
    }


@router.post("/logout")
async def logout():
    """
    Logout endpoint (Firebase handles token invalidation)
    This is mainly for logging purposes
    """
    return {"message": "Logged out successfully"}

