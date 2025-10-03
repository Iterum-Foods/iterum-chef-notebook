import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

PROFILES_DIR = os.path.join(os.path.dirname(__file__), '../../profiles')
PROFILES_DIR = os.path.abspath(PROFILES_DIR)

if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

router = APIRouter(tags=["profiles"])

class ProfileData(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    role: Optional[str] = None
    restaurant: Optional[str] = None
    avatar: Optional[str] = None
    isGoogleUser: Optional[bool] = False
    recipes: Optional[list] = []
    ingredients: Optional[list] = []
    equipment: Optional[list] = []
    lastUpdated: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    role: Optional[str] = None
    restaurant: Optional[str] = None

class LoginResponse(BaseModel):
    user: ProfileData
    token: str

@router.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    """Simple login endpoint that creates or finds a user profile"""
    # For now, we'll create a simple profile based on email
    # In a real app, you'd want proper password hashing and validation
    
    # Create a simple user ID from email
    user_id = str(hash(login_request.email))[-8:]  # Simple hash-based ID
    
    # Check if profile exists
    fpath = os.path.join(PROFILES_DIR, f"{user_id}.json")
    
    if os.path.exists(fpath):
        # Load existing profile
        with open(fpath, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
    else:
        # Create new profile
        profile_data = {
            'id': user_id,
            'name': login_request.name or login_request.email.split('@')[0],  # Use provided name or email prefix
            'email': login_request.email,
            'role': login_request.role or 'Chef',
            'restaurant': login_request.restaurant or 'My Kitchen',
            'avatar': None,
            'isGoogleUser': False,
            'recipes': [],
            'ingredients': [],
            'equipment': [],
            'lastUpdated': datetime.now().isoformat()
        }
        # Save the new profile
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)
    
    # Create a simple token (in real app, use JWT)
    token = f"token_{user_id}_{datetime.now().timestamp()}"
    
    return LoginResponse(
        user=ProfileData(**profile_data),
        token=token
    )

@router.post("/offline", response_model=LoginResponse)
def continue_offline():
    """Create a local offline profile for users who want to continue without login"""
    # Create a simple offline user ID
    user_id = f"offline_{datetime.now().timestamp()}"
    
    profile_data = {
        'id': user_id,
        'name': 'Local User',
        'email': 'local@offline.com',
        'role': 'Chef',
        'restaurant': 'My Kitchen',
        'avatar': None,
        'isGoogleUser': False,
        'recipes': [],
        'ingredients': [],
        'equipment': [],
        'lastUpdated': datetime.now().isoformat()
    }
    
    # Create a simple token
    token = f"offline_token_{user_id}"
    
    return LoginResponse(
        user=ProfileData(**profile_data),
        token=token
    )

@router.get("/", response_model=List[dict])
def list_profiles():
    profiles = []
    for fname in os.listdir(PROFILES_DIR):
        if fname.endswith('.json'):
            try:
                with open(os.path.join(PROFILES_DIR, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Only summary info
                    profiles.append({
                        'id': data.get('id'),
                        'name': data.get('name'),
                        'email': data.get('email'),
                        'role': data.get('role'),
                        'restaurant': data.get('restaurant'),
                        'avatar': data.get('avatar'),
                        'isGoogleUser': data.get('isGoogleUser', False),
                        'lastUpdated': data.get('lastUpdated')
                    })
            except Exception as e:
                continue
    return profiles

@router.get("/{profile_id}", response_model=ProfileData)
def get_profile(profile_id: str):
    fpath = os.path.join(PROFILES_DIR, f"{profile_id}.json")
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="Profile not found")
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

@router.post("/", response_model=ProfileData)
def save_profile(profile: ProfileData):
    fpath = os.path.join(PROFILES_DIR, f"{profile.id}.json")
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(profile.dict(), f, ensure_ascii=False, indent=2)
    return profile

@router.delete("/{profile_id}")
def delete_profile(profile_id: str):
    fpath = os.path.join(PROFILES_DIR, f"{profile_id}.json")
    if not os.path.exists(fpath):
        raise HTTPException(status_code=404, detail="Profile not found")
    os.remove(fpath)
    return JSONResponse(content={"detail": "Profile deleted"}) 