from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
from pydantic import BaseModel

from app.database import get_db, User
from app.schemas import UserCreate, User as UserSchema
from app.core.auth import (
    authenticate_user, get_password_hash, create_access_token,
    get_current_active_user, get_current_user
)
from app.core.config import settings

router = APIRouter()


class UserRegister(BaseModel):
    username: str
    email: str
    password: Optional[str] = None  # Optional for local development
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    restaurant: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: str


class TokenVerify(BaseModel):
    token: str


@router.post("/register", response_model=UserSchema)
async def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user with enhanced profile information"""
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    # Use provided password or default for local development
    password_to_hash = user.password if user.password else "localdev123"
    hashed_password = get_password_hash(password_to_hash)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role or "chef",  # Default role
        restaurant=user.restaurant or "My Kitchen"  # Default restaurant
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Return user info along with token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "restaurant": user.restaurant
        }
    }


@router.post("/verify")
async def verify_token(
    current_user: User = Depends(get_current_user)
):
    """Verify if the current token is valid"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "name": f"{current_user.first_name or ''} {current_user.last_name or ''}".strip() or current_user.username,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "role": current_user.role,
            "restaurant": current_user.restaurant
        }
    }


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Send password reset email (placeholder implementation)"""
    
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # In a real implementation, you would:
    # 1. Generate a password reset token
    # 2. Send an email with the reset link
    # 3. Store the token with expiration
    
    # For now, just return success message
    return {"message": "If the email exists, a password reset link has been sent"}


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_current_user(
    user_update: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    
    # Update allowed fields
    allowed_fields = ['first_name', 'last_name', 'role', 'restaurant']
    
    for field in allowed_fields:
        if field in user_update:
            setattr(current_user, field, user_update[field])
    
    db.commit()
    db.refresh(current_user)
    
    return current_user 