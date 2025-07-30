from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import json

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)  # Chef, Sous Chef, etc.
    restaurant = Column(String)  # Restaurant/kitchen name
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    recipes = relationship("Recipe", back_populates="author", foreign_keys="[Recipe.author_id]")
    versions = relationship("RecipeVersion", back_populates="author", foreign_keys="[RecipeVersion.author_id]")


class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    cuisine_type = Column(String, index=True)
    difficulty_level = Column(String)  # Easy, Medium, Hard
    prep_time = Column(Integer)  # in minutes
    cook_time = Column(Integer)  # in minutes
    servings = Column(Integer)
    tags = Column(JSON)  # Store as JSON array
    dietary_restrictions = Column(JSON)  # Store as JSON array
    allergens = Column(JSON)  # Store as JSON array
    equipment_needed = Column(JSON)  # Store as JSON array
    status = Column(String, default="draft")  # draft, testing, published
    kitchen_type = Column(String, default="home")  # home, commercial
    type = Column(String, default="dish")  # dish, prep, other
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Review and import fields
    review_status = Column(String, default="pending")  # pending, approved, rejected
    imported_at = Column(DateTime)
    reviewed_at = Column(DateTime)
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    source = Column(String)  # Store original file path
    
    # Relationships
    author = relationship("User", foreign_keys=[author_id], back_populates="recipes")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    versions = relationship("RecipeVersion", back_populates="recipe", cascade="all, delete-orphan")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("RecipeInstruction", back_populates="recipe", cascade="all, delete-orphan")


class RecipeVersion(Base):
    __tablename__ = "recipe_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    version_number = Column(String, index=True)  # e.g., "1.0", "2.1"
    version_name = Column(String)  # e.g., "Initial version", "Improved with roasted tomatoes"
    change_notes = Column(Text)
    testing_notes = Column(Text)
    ratings = Column(JSON)  # Store ratings as JSON
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    recipe = relationship("Recipe", back_populates="versions")
    author = relationship("User", back_populates="versions")
    ingredients = relationship("VersionIngredient", back_populates="version", cascade="all, delete-orphan")
    instructions = relationship("VersionInstruction", back_populates="version", cascade="all, delete-orphan")


class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    default_unit = Column(String)
    description = Column(Text)
    nutritional_info = Column(JSON)  # Store nutritional data as JSON
    allergens = Column(JSON)  # Store allergens as JSON array
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=True)
    prep_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)  # FK to prep recipe
    quantity = Column(Float)
    unit = Column(String)
    notes = Column(String)
    is_prep = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    
    # Relationships
    recipe = relationship("Recipe", foreign_keys=[recipe_id], back_populates="ingredients")
    ingredient = relationship("Ingredient", foreign_keys=[ingredient_id])
    prep_recipe = relationship("Recipe", foreign_keys=[prep_recipe_id])


class VersionIngredient(Base):
    __tablename__ = "version_ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("recipe_versions.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float)
    unit = Column(String)
    notes = Column(Text)
    order_index = Column(Integer)
    
    # Relationships
    version = relationship("RecipeVersion", back_populates="ingredients")
    ingredient = relationship("Ingredient")


class RecipeInstruction(Base):
    __tablename__ = "recipe_instructions"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    step_number = Column(Integer)
    instruction = Column(Text)
    tips = Column(Text)
    time_estimate = Column(Integer)  # in minutes
    temperature = Column(Float)  # in Celsius
    equipment = Column(String)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="instructions")


class VersionInstruction(Base):
    __tablename__ = "version_instructions"
    
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("recipe_versions.id"))
    step_number = Column(Integer)
    instruction = Column(Text)
    tips = Column(Text)
    time_estimate = Column(Integer)  # in minutes
    temperature = Column(Float)  # in Celsius
    equipment = Column(String)
    
    # Relationships
    version = relationship("RecipeVersion", back_populates="instructions")


class RecipeUpload(Base):
    __tablename__ = "recipe_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    original_filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    mime_type = Column(String)
    upload_status = Column(String, default="pending")  # pending, processing, completed, failed
    ocr_text = Column(Text)
    parsed_data = Column(JSON)  # Store parsed recipe data as JSON
    error_message = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    processed_at = Column(DateTime)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 