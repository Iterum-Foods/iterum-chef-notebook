"""
Recipe Ideas Sync Router - Backend endpoints for recipe ideas synchronization
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
class RecipeIdeaSync(BaseModel):
    title: str
    description: Optional[str] = ""
    category: Optional[str] = ""
    inspiration: Optional[str] = ""
    tags: List[str] = []
    status: str = "idea"  # idea, planned, in_progress, completed


class RecipeIdeaResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    inspiration: Optional[str]
    tags: List[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Database model
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import json


class RecipeIdea(Base):
    __tablename__ = "recipe_ideas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(String)
    inspiration = Column(Text)
    tags = Column(Text)  # JSON array as string
    status = Column(String, default="idea")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


@router.post("/sync", response_model=RecipeIdeaResponse)
async def sync_idea(
    idea: RecipeIdeaSync,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sync recipe idea to backend
    """
    try:
        # Create new idea
        new_idea = RecipeIdea(
            user_id=current_user.id,
            title=idea.title,
            description=idea.description,
            category=idea.category,
            inspiration=idea.inspiration,
            tags=json.dumps(idea.tags),
            status=idea.status
        )
        db.add(new_idea)
        db.commit()
        db.refresh(new_idea)
        
        return RecipeIdeaResponse(
            id=new_idea.id,
            user_id=new_idea.user_id,
            title=new_idea.title,
            description=new_idea.description,
            category=new_idea.category,
            inspiration=new_idea.inspiration,
            tags=json.loads(new_idea.tags) if new_idea.tags else [],
            status=new_idea.status,
            created_at=new_idea.created_at,
            updated_at=new_idea.updated_at
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=List[RecipeIdeaResponse])
async def get_all_ideas(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all recipe ideas for the current user
    """
    query = db.query(RecipeIdea).filter(RecipeIdea.user_id == current_user.id)
    
    if status:
        query = query.filter(RecipeIdea.status == status)
    
    ideas = query.order_by(RecipeIdea.created_at.desc()).all()

    return [
        RecipeIdeaResponse(
            id=idea.id,
            user_id=idea.user_id,
            title=idea.title,
            description=idea.description,
            category=idea.category,
            inspiration=idea.inspiration,
            tags=json.loads(idea.tags) if idea.tags else [],
            status=idea.status,
            created_at=idea.created_at,
            updated_at=idea.updated_at
        )
        for idea in ideas
    ]


@router.get("/{idea_id}", response_model=RecipeIdeaResponse)
async def get_idea(
    idea_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific recipe idea
    """
    idea = db.query(RecipeIdea).filter(
        RecipeIdea.id == idea_id,
        RecipeIdea.user_id == current_user.id
    ).first()

    if not idea:
        raise HTTPException(status_code=404, detail="Recipe idea not found")

    return RecipeIdeaResponse(
        id=idea.id,
        user_id=idea.user_id,
        title=idea.title,
        description=idea.description,
        category=idea.category,
        inspiration=idea.inspiration,
        tags=json.loads(idea.tags) if idea.tags else [],
        status=idea.status,
        created_at=idea.created_at,
        updated_at=idea.updated_at
    )


@router.put("/{idea_id}", response_model=RecipeIdeaResponse)
async def update_idea(
    idea_id: int,
    idea_update: RecipeIdeaSync,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a recipe idea
    """
    idea = db.query(RecipeIdea).filter(
        RecipeIdea.id == idea_id,
        RecipeIdea.user_id == current_user.id
    ).first()

    if not idea:
        raise HTTPException(status_code=404, detail="Recipe idea not found")

    # Update fields
    idea.title = idea_update.title
    idea.description = idea_update.description
    idea.category = idea_update.category
    idea.inspiration = idea_update.inspiration
    idea.tags = json.dumps(idea_update.tags)
    idea.status = idea_update.status
    idea.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(idea)

    return RecipeIdeaResponse(
        id=idea.id,
        user_id=idea.user_id,
        title=idea.title,
        description=idea.description,
        category=idea.category,
        inspiration=idea.inspiration,
        tags=json.loads(idea.tags) if idea.tags else [],
        status=idea.status,
        created_at=idea.created_at,
        updated_at=idea.updated_at
    )


@router.delete("/{idea_id}")
async def delete_idea(
    idea_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a recipe idea
    """
    idea = db.query(RecipeIdea).filter(
        RecipeIdea.id == idea_id,
        RecipeIdea.user_id == current_user.id
    ).first()

    if not idea:
        raise HTTPException(status_code=404, detail="Recipe idea not found")

    db.delete(idea)
    db.commit()

    return {"message": "Recipe idea deleted successfully"}

