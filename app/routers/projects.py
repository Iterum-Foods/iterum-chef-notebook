"""
Project management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.core.auth import get_current_user
from app.models.project import Project, ProjectEquipment, Menu
from app.schemas import User

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    restaurant_name: Optional[str] = None
    cuisine_type: Optional[str] = None
    location: Optional[str] = None
    color_theme: Optional[str] = "#3B82F6"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    restaurant_name: Optional[str] = None
    cuisine_type: Optional[str] = None
    location: Optional[str] = None
    color_theme: Optional[str] = None
    is_active: Optional[bool] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    restaurant_name: Optional[str]
    cuisine_type: Optional[str]
    location: Optional[str]
    is_default: bool
    is_active: bool
    color_theme: str
    owner_id: int
    created_at: str
    updated_at: Optional[str]
    
    # Counts for dashboard
    recipe_count: Optional[int] = 0
    menu_count: Optional[int] = 0
    equipment_count: Optional[int] = 0

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProjectResponse])
async def get_user_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects for the current user"""
    
    projects = db.query(Project).filter(
        Project.owner_id == current_user.id,
        Project.is_active == True
    ).order_by(Project.is_default.desc(), Project.name).all()
    
    # Add counts for each project
    project_responses = []
    for project in projects:
        # Count recipes
        recipe_count = db.query(Recipe).filter(Recipe.project_id == project.id).count()
        
        # Count menus
        menu_count = db.query(Menu).filter(Menu.project_id == project.id).count()
        
        # Count equipment
        equipment_count = db.query(ProjectEquipment).filter(
            ProjectEquipment.project_id == project.id
        ).count()
        
        project_data = ProjectResponse.from_orm(project)
        project_data.recipe_count = recipe_count
        project_data.menu_count = menu_count
        project_data.equipment_count = equipment_count
        
        project_responses.append(project_data)
    
    return project_responses


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project"""
    
    # Check if user already has too many projects (optional limit)
    project_count = db.query(Project).filter(
        Project.owner_id == current_user.id,
        Project.is_active == True
    ).count()
    
    if project_count >= 50:  # Reasonable limit
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum number of projects reached (50)"
        )
    
    # Create new project
    project = Project(
        name=project_data.name,
        description=project_data.description,
        restaurant_name=project_data.restaurant_name,
        cuisine_type=project_data.cuisine_type,
        location=project_data.location,
        color_theme=project_data.color_theme,
        owner_id=current_user.id,
        is_default=False
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Return with initial counts (all zero for new project)
    project_response = ProjectResponse.from_orm(project)
    project_response.recipe_count = 0
    project_response.menu_count = 0
    project_response.equipment_count = 0
    
    return project_response


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific project"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Add counts
    recipe_count = db.query(Recipe).filter(Recipe.project_id == project.id).count()
    menu_count = db.query(Menu).filter(Menu.project_id == project.id).count()
    equipment_count = db.query(ProjectEquipment).filter(
        ProjectEquipment.project_id == project.id
    ).count()
    
    project_response = ProjectResponse.from_orm(project)
    project_response.recipe_count = recipe_count
    project_response.menu_count = menu_count
    project_response.equipment_count = equipment_count
    
    return project_response


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a project"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Don't allow deactivating the default project
    if project.is_default and project_data.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate the Full Library project"
        )
    
    # Update fields
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return ProjectResponse.from_orm(project)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project (soft delete - mark as inactive)"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Don't allow deleting the default project
    if project.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the Full Library project"
        )
    
    # Soft delete by marking as inactive
    project.is_active = False
    db.commit()
    
    return {"message": f"Project '{project.name}' has been deactivated"}


@router.get("/{project_id}/summary")
async def get_project_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed summary of project contents"""
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get detailed counts and recent activity
    from app.models import Recipe
    
    recipes = db.query(Recipe).filter(Recipe.project_id == project.id).limit(5).all()
    menus = db.query(Menu).filter(Menu.project_id == project.id).limit(5).all()
    equipment = db.query(ProjectEquipment).filter(
        ProjectEquipment.project_id == project.id
    ).limit(5).all()
    
    return {
        "project": ProjectResponse.from_orm(project),
        "recent_recipes": [{"id": r.id, "name": r.name} for r in recipes],
        "recent_menus": [{"id": m.id, "name": m.name} for m in menus],
        "equipment_summary": [{"id": e.equipment_id, "quantity": e.quantity} for e in equipment],
        "total_counts": {
            "recipes": db.query(Recipe).filter(Recipe.project_id == project.id).count(),
            "menus": db.query(Menu).filter(Menu.project_id == project.id).count(),
            "equipment": db.query(ProjectEquipment).filter(ProjectEquipment.project_id == project.id).count()
        }
    }


# Import Recipe here to avoid circular import
try:
    from app.models import Recipe
except ImportError:
    Recipe = None