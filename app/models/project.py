"""
Project model for multi-project organization
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    restaurant_name = Column(String(200), nullable=True)
    cuisine_type = Column(String(100), nullable=True)
    location = Column(String(200), nullable=True)
    
    # Project metadata
    is_default = Column(Boolean, default=False)  # Full Library project
    is_active = Column(Boolean, default=True)
    color_theme = Column(String(7), default="#3B82F6")  # Hex color
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    recipes = relationship("Recipe", back_populates="project")
    menus = relationship("Menu", back_populates="project") 
    equipment_assignments = relationship("ProjectEquipment", back_populates="project")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"


class ProjectEquipment(Base):
    __tablename__ = "project_equipment"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    
    # Project-specific equipment data
    quantity = Column(Integer, default=1)
    location = Column(String(100), nullable=True)  # Kitchen station, storage, etc.
    notes = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="equipment_assignments")
    equipment = relationship("Equipment")
    
    def __repr__(self):
        return f"<ProjectEquipment(project_id={self.project_id}, equipment_id={self.equipment_id})>"


class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    menu_type = Column(String(50), default="Regular")  # Regular, Seasonal, Special Event, etc.
    
    # Project association
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Menu data - stored as JSON
    sections = Column(Text, nullable=True)  # JSON string of menu sections
    items = Column(Text, nullable=True)     # JSON string of menu items
    pricing = Column(Text, nullable=True)   # JSON string of pricing data
    
    # Status
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="menus")
    owner = relationship("User")
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', project_id={self.project_id})>"