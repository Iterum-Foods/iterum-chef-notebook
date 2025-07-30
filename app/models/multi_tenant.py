"""
Multi-Tenant Database Models for Iterum R&D Chef Notebook
Supports Organizations → Restaurants → Users hierarchy
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

Base = declarative_base()

class SubscriptionType(enum.Enum):
    basic = "basic"
    professional = "professional"
    enterprise = "enterprise"

class UserRole(enum.Enum):
    org_admin = "org_admin"
    restaurant_manager = "restaurant_manager"
    head_chef = "head_chef"
    sous_chef = "sous_chef"
    line_cook = "line_cook"
    staff = "staff"

class MenuStyle(enum.Enum):
    fine_dining = "fine_dining"
    casual = "casual"
    fast_casual = "fast_casual"
    quick_service = "quick_service"

class ResourceScope(enum.Enum):
    organization = "organization"
    restaurant = "restaurant"
    private = "private"

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    license_key = Column(String(255), unique=True, nullable=False)
    
    # Subscription Details
    subscription_type = Column(Enum(SubscriptionType), default=SubscriptionType.basic)
    max_restaurants = Column(Integer, default=5)
    max_users = Column(Integer, default=50)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Contact & Billing
    contact_name = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    billing_address = Column(Text)
    
    # Configuration
    settings = Column(JSON, default=dict)
    features = Column(JSON, default=dict)
    
    # Relationships
    restaurants = relationship("Restaurant", back_populates="organization", cascade="all, delete-orphan")
    users = relationship("User", back_populates="organization")
    recipes = relationship("Recipe", back_populates="organization")
    ingredients = relationship("Ingredient", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(name='{self.name}', slug='{self.slug}')>"

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    
    # Restaurant Details
    cuisine_type = Column(String(100))
    location = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    
    # Operational Settings
    seating_capacity = Column(Integer)
    operating_hours = Column(JSON)
    menu_style = Column(Enum(MenuStyle))
    
    # System Settings
    is_active = Column(Boolean, default=True)
    settings = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="restaurants")
    users = relationship("User", back_populates="restaurant")
    recipes = relationship("Recipe", back_populates="restaurant")
    ingredients = relationship("Ingredient", back_populates="restaurant")
    
    def __repr__(self):
        return f"<Restaurant(name='{self.name}', organization='{self.organization.name if self.organization else None}')>"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=True)
    
    # User Details
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    # Role & Permissions
    role = Column(Enum(UserRole), default=UserRole.staff)
    permissions = Column(JSON, default=dict)
    
    # System Fields
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    restaurant = relationship("Restaurant", back_populates="users")
    recipes = relationship("Recipe", back_populates="created_by")
    ingredients = relationship("Ingredient", back_populates="created_by")
    
    def __repr__(self):
        return f"<User(username='{self.username}', organization='{self.organization.name if self.organization else None}')>"
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def can_access_restaurant(self, restaurant_id):
        """Check if user can access a specific restaurant"""
        if self.role == UserRole.org_admin:
            return True
        return str(self.restaurant_id) == str(restaurant_id)
    
    def can_manage_organization(self):
        """Check if user can manage organization settings"""
        return self.role == UserRole.org_admin
    
    def can_manage_restaurant(self, restaurant_id=None):
        """Check if user can manage restaurant settings"""
        restaurant_id = restaurant_id or self.restaurant_id
        if self.role == UserRole.org_admin:
            return True
        if self.role == UserRole.restaurant_manager and str(self.restaurant_id) == str(restaurant_id):
            return True
        return False

# Extended models for resources with multi-tenant support

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Recipe Content
    name = Column(String(255), nullable=False)
    description = Column(Text)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    
    # Metadata
    scope = Column(Enum(ResourceScope), default=ResourceScope.private)
    cuisine_type = Column(String(100))
    difficulty = Column(String(50))
    prep_time = Column(Integer)  # minutes
    cook_time = Column(Integer)  # minutes
    servings = Column(Integer)
    
    # System Fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="recipes")
    restaurant = relationship("Restaurant", back_populates="recipes")
    created_by = relationship("User", back_populates="recipes")

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Ingredient Details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    unit = Column(String(50))
    cost_per_unit = Column(String(20))  # Store as string to handle currency
    
    # Nutritional Information
    nutrition_info = Column(JSON)
    allergens = Column(JSON)
    
    # Sourcing Information
    preferred_vendor = Column(String(255))
    vendor_sku = Column(String(100))
    
    # Metadata
    scope = Column(Enum(ResourceScope), default=ResourceScope.private)
    
    # System Fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="ingredients")
    restaurant = relationship("Restaurant", back_populates="ingredients")
    created_by = relationship("User", back_populates="ingredients")

# Migration helper functions

def create_organization_for_existing_user(user_data):
    """Create an organization for an existing user during migration"""
    from sqlalchemy.orm import sessionmaker
    from app.database import engine
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create organization
        org = Organization(
            name=f"{user_data.get('name', 'User')}'s Organization",
            slug=generate_slug(user_data.get('name', 'user')),
            license_key=generate_license_key(),
            subscription_type=SubscriptionType.professional,
            max_restaurants=10,
            max_users=25,
            contact_name=user_data.get('name'),
            contact_email=user_data.get('email')
        )
        session.add(org)
        session.flush()  # Get the ID
        
        # Create default restaurant
        restaurant = Restaurant(
            organization_id=org.id,
            name=user_data.get('restaurant', 'Main Kitchen'),
            slug='main',
            location='Primary Location',
            menu_style=MenuStyle.casual
        )
        session.add(restaurant)
        session.flush()
        
        session.commit()
        return org.id, restaurant.id
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def generate_slug(name):
    """Generate a URL-friendly slug from a name"""
    import re
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
    slug = re.sub(r'[\s-]+', '-', slug)
    return slug.strip('-')

def generate_license_key():
    """Generate a unique license key"""
    import secrets
    import string
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(16)) 