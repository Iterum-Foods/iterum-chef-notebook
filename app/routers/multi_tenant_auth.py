"""
Multi-Tenant Authentication Router
Handles organization-aware login and context switching
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from app.database import get_db
from app.models.multi_tenant import Organization, Restaurant, User, UserRole, ResourceScope
from app.core.settings import settings

router = APIRouter(prefix="/api/auth/v2", tags=["Multi-Tenant Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic Models

class LoginRequest(BaseModel):
    organization_slug: str
    username: str
    password: str
    restaurant_id: Optional[str] = None

class OrganizationInfo(BaseModel):
    id: str
    name: str
    slug: str
    subscription_type: str
    max_restaurants: int
    max_users: int

class RestaurantInfo(BaseModel):
    id: str
    name: str
    slug: str
    cuisine_type: Optional[str]
    location: Optional[str]
    menu_style: Optional[str]

class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    role: str
    can_manage_organization: bool
    can_switch_restaurants: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo
    organization: OrganizationInfo
    current_restaurant: Optional[RestaurantInfo]
    accessible_restaurants: List[RestaurantInfo]

class RestaurantSwitchRequest(BaseModel):
    restaurant_id: str

# Authentication Functions

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, organization_slug: str, username: str, password: str):
    """Authenticate user within an organization context"""
    
    # First, find the organization
    organization = db.query(Organization).filter(
        Organization.slug == organization_slug,
        Organization.is_active == True
    ).first()
    
    if not organization:
        return None
    
    # Check if organization subscription is valid
    if organization.expires_at and organization.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization subscription has expired"
        )
    
    # Find user within this organization
    user = db.query(User).filter(
        User.username == username,
        User.organization_id == organization.id,
        User.is_active == True
    ).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user, organization

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token with organization and restaurant context"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_user_accessible_restaurants(user: User, db: Session) -> List[Restaurant]:
    """Get list of restaurants the user can access"""
    if user.role == UserRole.org_admin:
        # Org admins can access all restaurants in their organization
        return db.query(Restaurant).filter(
            Restaurant.organization_id == user.organization_id,
            Restaurant.is_active == True
        ).all()
    else:
        # Other users can only access their assigned restaurant
        if user.restaurant_id:
            restaurant = db.query(Restaurant).filter(
                Restaurant.id == user.restaurant_id,
                Restaurant.is_active == True
            ).first()
            return [restaurant] if restaurant else []
        return []

# API Endpoints

@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Multi-tenant login with organization context
    
    Login format: organization_slug + username + password
    Example: "sunset-group" + "john.doe" + "password123"
    """
    
    try:
        # Authenticate user within organization
        auth_result = authenticate_user(
            db, 
            login_request.organization_slug, 
            login_request.username, 
            login_request.password
        )
        
        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid organization, username, or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user, organization = auth_result
        
        # Get accessible restaurants
        accessible_restaurants = get_user_accessible_restaurants(user, db)
        
        # Determine current restaurant
        current_restaurant = None
        if login_request.restaurant_id:
            # User specified a restaurant
            for restaurant in accessible_restaurants:
                if str(restaurant.id) == login_request.restaurant_id:
                    current_restaurant = restaurant
                    break
            if not current_restaurant:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to specified restaurant"
                )
        elif user.restaurant_id:
            # Use user's default restaurant
            current_restaurant = db.query(Restaurant).filter(
                Restaurant.id == user.restaurant_id
            ).first()
        elif accessible_restaurants:
            # Use first accessible restaurant
            current_restaurant = accessible_restaurants[0]
        
        # Create JWT token with context
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub": user.username,
            "user_id": str(user.id),
            "organization_id": str(organization.id),
            "organization_slug": organization.slug,
            "restaurant_id": str(current_restaurant.id) if current_restaurant else None,
            "role": user.role.value,
            "scopes": get_user_scopes(user)
        }
        
        access_token = create_access_token(
            data=token_data, 
            expires_delta=access_token_expires
        )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Prepare response
        return LoginResponse(
            access_token=access_token,
            user=UserInfo(
                id=str(user.id),
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                role=user.role.value,
                can_manage_organization=user.can_manage_organization(),
                can_switch_restaurants=(user.role == UserRole.org_admin)
            ),
            organization=OrganizationInfo(
                id=str(organization.id),
                name=organization.name,
                slug=organization.slug,
                subscription_type=organization.subscription_type.value,
                max_restaurants=organization.max_restaurants,
                max_users=organization.max_users
            ),
            current_restaurant=RestaurantInfo(
                id=str(current_restaurant.id),
                name=current_restaurant.name,
                slug=current_restaurant.slug,
                cuisine_type=current_restaurant.cuisine_type,
                location=current_restaurant.location,
                menu_style=current_restaurant.menu_style.value if current_restaurant.menu_style else None
            ) if current_restaurant else None,
            accessible_restaurants=[
                RestaurantInfo(
                    id=str(r.id),
                    name=r.name,
                    slug=r.slug,
                    cuisine_type=r.cuisine_type,
                    location=r.location,
                    menu_style=r.menu_style.value if r.menu_style else None
                ) for r in accessible_restaurants
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/switch-restaurant")
async def switch_restaurant(
    switch_request: RestaurantSwitchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Switch user's current restaurant context
    Only available to org_admins and users with multi-restaurant access
    """
    
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user can access the requested restaurant
    accessible_restaurants = get_user_accessible_restaurants(user, db)
    target_restaurant = None
    
    for restaurant in accessible_restaurants:
        if str(restaurant.id) == switch_request.restaurant_id:
            target_restaurant = restaurant
            break
    
    if not target_restaurant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to specified restaurant"
        )
    
    # Create new token with updated restaurant context
    token_data = current_user.copy()
    token_data["restaurant_id"] = str(target_restaurant.id)
    
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "current_restaurant": RestaurantInfo(
            id=str(target_restaurant.id),
            name=target_restaurant.name,
            slug=target_restaurant.slug,
            cuisine_type=target_restaurant.cuisine_type,
            location=target_restaurant.location,
            menu_style=target_restaurant.menu_style.value if target_restaurant.menu_style else None
        )
    }

@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user info with organization and restaurant context"""
    
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    organization = db.query(Organization).filter(Organization.id == current_user["organization_id"]).first()
    
    current_restaurant = None
    if current_user.get("restaurant_id"):
        current_restaurant = db.query(Restaurant).filter(
            Restaurant.id == current_user["restaurant_id"]
        ).first()
    
    accessible_restaurants = get_user_accessible_restaurants(user, db)
    
    return {
        "user": UserInfo(
            id=str(user.id),
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            role=user.role.value,
            can_manage_organization=user.can_manage_organization(),
            can_switch_restaurants=(user.role == UserRole.org_admin)
        ),
        "organization": OrganizationInfo(
            id=str(organization.id),
            name=organization.name,
            slug=organization.slug,
            subscription_type=organization.subscription_type.value,
            max_restaurants=organization.max_restaurants,
            max_users=organization.max_users
        ),
        "current_restaurant": RestaurantInfo(
            id=str(current_restaurant.id),
            name=current_restaurant.name,
            slug=current_restaurant.slug,
            cuisine_type=current_restaurant.cuisine_type,
            location=current_restaurant.location,
            menu_style=current_restaurant.menu_style.value if current_restaurant.menu_style else None
        ) if current_restaurant else None,
        "accessible_restaurants": [
            RestaurantInfo(
                id=str(r.id),
                name=r.name,
                slug=r.slug,
                cuisine_type=r.cuisine_type,
                location=r.location,
                menu_style=r.menu_style.value if r.menu_style else None
            ) for r in accessible_restaurants
        ]
    }

# Helper Functions

def get_user_scopes(user: User) -> List[str]:
    """Get list of scopes/permissions for the user"""
    scopes = ["read"]
    
    if user.role in [UserRole.org_admin, UserRole.restaurant_manager, UserRole.head_chef]:
        scopes.extend(["write", "manage"])
    
    if user.role == UserRole.org_admin:
        scopes.extend(["admin", "org_admin"])
    
    return scopes

# Dependencies (to be implemented in app/core/auth.py)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from JWT token"""
    # This would be implemented in the main auth module
    # For now, this is a placeholder
    pass

# OAuth2 scheme
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/v2/login") 