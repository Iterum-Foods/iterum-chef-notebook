"""
Menu Sync Router - Backend endpoints for menu data synchronization
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user

router = APIRouter()


# Pydantic models
class MenuItem(BaseModel):
    name: str
    description: Optional[str] = ""
    category: str
    price: float
    allergens: List[str] = []
    dietary_info: List[str] = []


class MenuData(BaseModel):
    project_id: str
    items: List[MenuItem]
    categories: List[str] = []
    metadata: Optional[dict] = {}


class MenuSyncRequest(BaseModel):
    project_id: str
    menu_data: dict


class MenuResponse(BaseModel):
    id: int
    user_id: int
    project_id: str
    menu_data: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Database model
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import json


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(String, index=True, nullable=False)
    menu_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


@router.post("/sync", response_model=MenuResponse)
async def sync_menu(
    menu_sync: MenuSyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sync menu data to backend
    """
    try:
        # Check if menu already exists for this project
        existing_menu = db.query(Menu).filter(
            Menu.user_id == current_user.id,
            Menu.project_id == menu_sync.project_id
        ).first()

        if existing_menu:
            # Update existing menu
            existing_menu.menu_data = json.dumps(menu_sync.menu_data)
            existing_menu.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_menu)
            
            return MenuResponse(
                id=existing_menu.id,
                user_id=existing_menu.user_id,
                project_id=existing_menu.project_id,
                menu_data=json.loads(existing_menu.menu_data),
                created_at=existing_menu.created_at,
                updated_at=existing_menu.updated_at
            )
        else:
            # Create new menu
            new_menu = Menu(
                user_id=current_user.id,
                project_id=menu_sync.project_id,
                menu_data=json.dumps(menu_sync.menu_data)
            )
            db.add(new_menu)
            db.commit()
            db.refresh(new_menu)
            
            return MenuResponse(
                id=new_menu.id,
                user_id=new_menu.user_id,
                project_id=new_menu.project_id,
                menu_data=json.loads(new_menu.menu_data),
                created_at=new_menu.created_at,
                updated_at=new_menu.updated_at
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project/{project_id}", response_model=Optional[MenuResponse])
async def get_menu_by_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get menu for a specific project
    """
    menu = db.query(Menu).filter(
        Menu.user_id == current_user.id,
        Menu.project_id == project_id
    ).first()

    if not menu:
        return None

    return MenuResponse(
        id=menu.id,
        user_id=menu.user_id,
        project_id=menu.project_id,
        menu_data=json.loads(menu.menu_data),
        created_at=menu.created_at,
        updated_at=menu.updated_at
    )


@router.get("/all", response_model=List[MenuResponse])
async def get_all_menus(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all menus for the current user
    """
    menus = db.query(Menu).filter(Menu.user_id == current_user.id).all()

    return [
        MenuResponse(
            id=menu.id,
            user_id=menu.user_id,
            project_id=menu.project_id,
            menu_data=json.loads(menu.menu_data),
            created_at=menu.created_at,
            updated_at=menu.updated_at
        )
        for menu in menus
    ]


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a menu
    """
    menu = db.query(Menu).filter(
        Menu.id == menu_id,
        Menu.user_id == current_user.id
    ).first()

    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    db.delete(menu)
    db.commit()

    return {"message": "Menu deleted successfully"}

