from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Base schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Recipe schemas
class RecipeIngredientBase(BaseModel):
    ingredient_id: Optional[int] = None
    prep_recipe_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    is_prep: bool = False
    order_index: Optional[int] = 0


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredient(RecipeIngredientBase):
    id: int
    ingredient_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class RecipeInstructionBase(BaseModel):
    step_number: int
    instruction: str
    tips: Optional[str] = None
    time_estimate: Optional[int] = None
    temperature: Optional[float] = None
    equipment: Optional[str] = None


class RecipeInstructionCreate(RecipeInstructionBase):
    pass


class RecipeInstruction(RecipeInstructionBase):
    id: int
    
    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    tags: Optional[List[str]] = []
    dietary_restrictions: Optional[List[str]] = []
    allergens: Optional[List[str]] = []
    equipment_needed: Optional[List[str]] = []
    status: str = "draft"
    kitchen_type: str = "home"
    type: str = "dish"  # dish, prep, other


class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = []
    instructions: List[RecipeInstructionCreate] = []


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    tags: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    equipment_needed: Optional[List[str]] = None
    status: Optional[str] = None
    kitchen_type: Optional[str] = None
    type: Optional[str] = None


class Recipe(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    tags: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    equipment_needed: Optional[List[str]] = None
    status: str = "draft"
    kitchen_type: str = "home"
    type: str = "dish"
    review_status: str = "pending"  # pending, approved, rejected
    imported_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    source: Optional[str] = None  # Original file path
    author_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Version schemas
class RecipeVersionBase(BaseModel):
    version_number: str
    version_name: Optional[str] = None
    change_notes: Optional[str] = None
    testing_notes: Optional[str] = None
    ratings: Optional[Dict[str, Any]] = {}
    is_published: bool = False


class RecipeVersionCreate(RecipeVersionBase):
    ingredients: List[RecipeIngredientCreate] = []
    instructions: List[RecipeInstructionCreate] = []


class RecipeVersionUpdate(BaseModel):
    version_name: Optional[str] = None
    change_notes: Optional[str] = None
    testing_notes: Optional[str] = None
    ratings: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None


class RecipeVersion(RecipeVersionBase):
    id: int
    recipe_id: int
    author_id: int
    created_at: datetime
    published_at: Optional[datetime] = None
    ingredients: List[RecipeIngredient] = []
    instructions: List[RecipeInstruction] = []
    
    class Config:
        from_attributes = True


# Ingredient schemas
class IngredientBase(BaseModel):
    name: str
    category: Optional[str] = None
    default_unit: Optional[str] = None
    description: Optional[str] = None
    nutritional_info: Optional[Dict[str, Any]] = {}
    allergens: Optional[List[str]] = []


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    default_unit: Optional[str] = None
    description: Optional[str] = None
    nutritional_info: Optional[Dict[str, Any]] = None
    allergens: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Ingredient(IngredientBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Upload schemas
class RecipeUploadBase(BaseModel):
    original_filename: str
    file_size: int
    mime_type: str


class RecipeUploadCreate(RecipeUploadBase):
    pass


class RecipeUpload(RecipeUploadBase):
    id: int
    filename: str
    file_path: str
    upload_status: str
    ocr_text: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    uploaded_by: int
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Search and filter schemas
class RecipeSearch(BaseModel):
    query: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    status: Optional[str] = None
    kitchen_type: Optional[str] = None
    tags: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    author_id: Optional[int] = None
    limit: int = 20
    offset: int = 0


class RecipeScaling(BaseModel):
    recipe_id: int
    version_id: Optional[int] = None
    current_servings: int
    target_servings: int
    kitchen_type: str = "home"
    preserve_ratios: bool = True
    round_decimals: int = 2
    convert_units: bool = True


class UnitConversion(BaseModel):
    quantity: float
    from_unit: str
    to_unit: str
    ingredient_name: Optional[str] = None


# Response schemas
class RecipeListResponse(BaseModel):
    recipes: List[Recipe]
    total: int
    limit: int
    offset: int


class VersionListResponse(BaseModel):
    versions: List[RecipeVersion]
    total: int


class IngredientListResponse(BaseModel):
    ingredients: List[Ingredient]
    total: int
    limit: int
    offset: int


# Update forward references
Recipe.model_rebuild()
RecipeVersion.model_rebuild() 

# Vendor schemas
class VendorBase(BaseModel):
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    fax: Optional[str] = None
    website: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    specialties: Optional[List[str]] = []
    notes: Optional[str] = None
    is_active: bool = True


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    fax: Optional[str] = None
    website: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    specialties: Optional[List[str]] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class Vendor(VendorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Equipment schemas
class EquipmentBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = {}
    maintenance_notes: Optional[str] = None
    purchase_date: Optional[datetime] = None
    warranty_info: Optional[str] = None
    location: Optional[str] = None
    status: str = "active"  # active, maintenance, retired


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    maintenance_notes: Optional[str] = None
    purchase_date: Optional[datetime] = None
    warranty_info: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


class Equipment(EquipmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Vendor relationships schemas
class VendorIngredientBase(BaseModel):
    vendor_id: int
    ingredient_id: int
    price: Optional[float] = None
    unit: Optional[str] = None
    availability: Optional[str] = None
    minimum_order: Optional[float] = None
    lead_time_days: Optional[int] = None
    notes: Optional[str] = None


class VendorIngredientCreate(VendorIngredientBase):
    pass


class VendorIngredientUpdate(BaseModel):
    price: Optional[float] = None
    unit: Optional[str] = None
    availability: Optional[str] = None
    minimum_order: Optional[float] = None
    lead_time_days: Optional[int] = None
    notes: Optional[str] = None


class VendorIngredient(VendorIngredientBase):
    id: int
    ingredient_name: Optional[str] = None
    vendor_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class VendorEquipmentBase(BaseModel):
    vendor_id: int
    equipment_id: int
    price: Optional[float] = None
    availability: Optional[str] = None
    warranty_offered: Optional[str] = None
    service_support: Optional[str] = None
    notes: Optional[str] = None


class VendorEquipmentCreate(VendorEquipmentBase):
    pass


class VendorEquipmentUpdate(BaseModel):
    price: Optional[float] = None
    availability: Optional[str] = None
    warranty_offered: Optional[str] = None
    service_support: Optional[str] = None
    notes: Optional[str] = None


class VendorEquipment(VendorEquipmentBase):
    id: int
    equipment_name: Optional[str] = None
    vendor_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# List response schemas
class VendorListResponse(BaseModel):
    vendors: List[Vendor]
    total: int
    limit: int
    offset: int


class EquipmentListResponse(BaseModel):
    equipment: List[Equipment]
    total: int
    limit: int
    offset: int


class VendorIngredientListResponse(BaseModel):
    vendor_ingredients: List[VendorIngredient]
    total: int
    limit: int
    offset: int


class VendorEquipmentListResponse(BaseModel):
    vendor_equipment: List[VendorEquipment]
    total: int
    limit: int
    offset: int


# Search schemas
class VendorSearch(BaseModel):
    query: Optional[str] = None
    company: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    specialties: Optional[List[str]] = None
    is_active: Optional[bool] = None
    limit: int = 20
    offset: int = 0


class EquipmentSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    limit: int = 20
    offset: int = 0 