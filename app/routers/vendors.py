from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
import csv
import io

from ..schemas import (
    Vendor, VendorCreate, VendorUpdate, VendorListResponse, VendorSearch,
    Equipment, EquipmentCreate, EquipmentUpdate, EquipmentListResponse, EquipmentSearch,
    VendorIngredient, VendorIngredientCreate, VendorIngredientUpdate, VendorIngredientListResponse,
    VendorEquipment, VendorEquipmentCreate, VendorEquipmentUpdate, VendorEquipmentListResponse
)
from ..sqlite_database import db

router = APIRouter(prefix="/vendors", tags=["vendors"])

# Vendor endpoints
@router.post("/", response_model=Vendor)
async def create_vendor(vendor: VendorCreate):
    """Create a new vendor."""
    vendor_data = vendor.dict()
    vendor_id = db.save_vendor(vendor_data)
    if vendor_id is None:
        raise HTTPException(status_code=400, detail="Failed to create vendor")
    
    created_vendor = db.get_vendor(vendor_id)
    if created_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found after creation")
    
    return Vendor(**created_vendor)


@router.get("/", response_model=VendorListResponse)
async def get_vendors(
    search: Optional[str] = Query(None, description="Search vendors by name, company, or email"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all vendors with optional search."""
    vendors_data = db.get_vendors(limit=limit, offset=offset, search=search)
    vendors = [Vendor(**vendor) for vendor in vendors_data]
    
    return VendorListResponse(
        vendors=vendors,
        total=len(vendors),
        limit=limit,
        offset=offset
    )


@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor(vendor_id: int):
    """Get a specific vendor by ID."""
    vendor_data = db.get_vendor(vendor_id)
    if vendor_data is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    return Vendor(**vendor_data)


@router.put("/{vendor_id}", response_model=Vendor)
async def update_vendor(vendor_id: int, vendor_update: VendorUpdate):
    """Update a vendor."""
    # Get existing vendor
    existing_vendor = db.get_vendor(vendor_id)
    if existing_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # Update only provided fields
    update_data = vendor_update.dict(exclude_unset=True)
    if not update_data:
        return Vendor(**existing_vendor)
    
    # Merge with existing data
    updated_data = {**existing_vendor, **update_data}
    
    success = db.update_vendor(vendor_id, updated_data)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update vendor")
    
    updated_vendor = db.get_vendor(vendor_id)
    return Vendor(**updated_vendor)


@router.delete("/{vendor_id}")
async def delete_vendor(vendor_id: int):
    """Delete a vendor."""
    success = db.delete_vendor(vendor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    return {"message": "Vendor deleted successfully"}


# Equipment endpoints - Using different path to avoid conflicts
@router.post("/equipment/", response_model=Equipment)
async def create_equipment(equipment: EquipmentCreate):
    """Create new equipment."""
    equipment_data = equipment.dict()
    equipment_id = db.save_equipment(equipment_data)
    if equipment_id is None:
        raise HTTPException(status_code=400, detail="Failed to create equipment")
    
    created_equipment = db.get_equipment_by_id(equipment_id)
    if created_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found after creation")
    
    return Equipment(**created_equipment)


@router.get("/equipment/", response_model=EquipmentListResponse)
async def get_equipment(
    search: Optional[str] = Query(None, description="Search equipment by name, category, or description"),
    limit: int = Query(20, ge=1, le=100, description="Number of equipment to return"),
    offset: int = Query(0, ge=0, description="Number of equipment to skip")
):
    """Get all equipment with optional search. All parameters are required for this endpoint."""
    if limit is None or offset is None:
        raise HTTPException(status_code=422, detail="'limit' and 'offset' query parameters are required.")
    try:
        equipment_data = db.get_equipment(limit=limit, offset=offset, search=search)
        equipment_list = [Equipment(**eq) for eq in equipment_data]
        return EquipmentListResponse(
            equipment=equipment_list,
            total=len(equipment_list),
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching equipment: {str(e)}")


@router.get("/equipment/{equipment_id}", response_model=Equipment)
async def get_equipment_by_id(equipment_id: int):
    """Get a specific equipment by ID."""
    equipment_data = db.get_equipment_by_id(equipment_id)
    if equipment_data is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return Equipment(**equipment_data)


@router.put("/equipment/{equipment_id}", response_model=Equipment)
async def update_equipment(equipment_id: int, equipment_update: EquipmentUpdate):
    """Update equipment."""
    # Get existing equipment
    existing_equipment = db.get_equipment_by_id(equipment_id)
    if existing_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Update only provided fields
    update_data = equipment_update.dict(exclude_unset=True)
    if not update_data:
        return Equipment(**existing_equipment)
    
    # Merge with existing data
    updated_data = {**existing_equipment, **update_data}
    
    success = db.update_equipment(equipment_id, updated_data)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update equipment")
    
    updated_equipment = db.get_equipment_by_id(equipment_id)
    return Equipment(**updated_equipment)


@router.delete("/equipment/{equipment_id}")
async def delete_equipment(equipment_id: int):
    """Delete equipment."""
    success = db.delete_equipment(equipment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return {"message": "Equipment deleted successfully"}


# Vendor-Ingredient relationship endpoints
@router.post("/{vendor_id}/ingredients", response_model=VendorIngredient)
async def add_vendor_ingredient(vendor_id: int, vendor_ingredient: VendorIngredientCreate):
    """Add an ingredient to a vendor."""
    # Verify vendor exists
    vendor = db.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # Verify ingredient exists
    ingredients = db.get_ingredients()
    ingredient_exists = any(ing['name'] == vendor_ingredient.ingredient_id for ing in ingredients)
    if not ingredient_exists:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    vendor_ingredient_data = vendor_ingredient.dict()
    vendor_ingredient_data['vendor_id'] = vendor_id
    
    relationship_id = db.save_vendor_ingredient(vendor_ingredient_data)
    if relationship_id is None:
        raise HTTPException(status_code=400, detail="Failed to create vendor-ingredient relationship")
    
    # Get the created relationship
    relationships = db.get_vendor_ingredients(vendor_id=vendor_id)
    created_relationship = next((rel for rel in relationships if rel['id'] == relationship_id), None)
    
    if created_relationship is None:
        raise HTTPException(status_code=404, detail="Vendor-ingredient relationship not found after creation")
    
    return VendorIngredient(**created_relationship)


@router.get("/{vendor_id}/ingredients", response_model=VendorIngredientListResponse)
async def get_vendor_ingredients(vendor_id: int):
    """Get all ingredients for a vendor."""
    # Verify vendor exists
    vendor = db.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    relationships = db.get_vendor_ingredients(vendor_id=vendor_id)
    vendor_ingredients = [VendorIngredient(**rel) for rel in relationships]
    
    return VendorIngredientListResponse(
        vendor_ingredients=vendor_ingredients,
        total=len(vendor_ingredients),
        limit=len(vendor_ingredients),
        offset=0
    )


# Vendor-Equipment relationship endpoints
@router.post("/{vendor_id}/equipment", response_model=VendorEquipment)
async def add_vendor_equipment(vendor_id: int, vendor_equipment: VendorEquipmentCreate):
    """Add equipment to a vendor."""
    # Verify vendor exists
    vendor = db.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # Verify equipment exists
    equipment = db.get_equipment_by_id(vendor_equipment.equipment_id)
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    vendor_equipment_data = vendor_equipment.dict()
    vendor_equipment_data['vendor_id'] = vendor_id
    
    relationship_id = db.save_vendor_equipment(vendor_equipment_data)
    if relationship_id is None:
        raise HTTPException(status_code=400, detail="Failed to create vendor-equipment relationship")
    
    # Get the created relationship
    relationships = db.get_vendor_equipment(vendor_id=vendor_id)
    created_relationship = next((rel for rel in relationships if rel['id'] == relationship_id), None)
    
    if created_relationship is None:
        raise HTTPException(status_code=404, detail="Vendor-equipment relationship not found after creation")
    
    return VendorEquipment(**created_relationship)


@router.get("/{vendor_id}/equipment", response_model=VendorEquipmentListResponse)
async def get_vendor_equipment(vendor_id: int):
    """Get all equipment for a vendor."""
    # Verify vendor exists
    vendor = db.get_vendor(vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    relationships = db.get_vendor_equipment(vendor_id=vendor_id)
    vendor_equipment = [VendorEquipment(**rel) for rel in relationships]
    
    return VendorEquipmentListResponse(
        vendor_equipment=vendor_equipment,
        total=len(vendor_equipment),
        limit=len(vendor_equipment),
        offset=0
    )


# CSV Import endpoint
@router.post("/import-csv")
async def import_vendors_from_csv(csv_content: str):
    """Import vendors from CSV content."""
    try:
        # Parse CSV content
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        imported_count = 0
        errors = []
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
            try:
                # Map CSV columns to vendor fields
                vendor_data = {
                    'name': row.get('Name', '').strip(),
                    'company': row.get('Company', '').strip(),
                    'email': row.get('Email', '').strip(),
                    'phone': row.get('Phone', '').strip(),
                    'mobile': row.get('Mobile', '').strip(),
                    'fax': row.get('Fax', '').strip(),
                    'website': row.get('Website', '').strip(),
                    'street': row.get('Street', '').strip(),
                    'city': row.get('City', '').strip(),
                    'state': row.get('State', '').strip(),
                    'zip_code': row.get('ZIP', '').strip(),
                    'specialties': [],  # Could be parsed from a specific column if needed
                    'notes': '',
                    'is_active': True
                }
                
                # Skip empty rows
                if not vendor_data['name'] and not vendor_data['company']:
                    continue
                
                # Save vendor
                vendor_id = db.save_vendor(vendor_data)
                if vendor_id:
                    imported_count += 1
                else:
                    errors.append(f"Row {row_num}: Failed to save vendor")
                    
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        return {
            "message": f"Import completed. {imported_count} vendors imported successfully.",
            "imported_count": imported_count,
            "errors": errors
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")


# Search endpoints
@router.get("/search/vendors", response_model=VendorListResponse)
async def search_vendors(
    query: Optional[str] = Query(None, description="Search query"),
    company: Optional[str] = Query(None, description="Filter by company"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Search vendors with filters."""
    # For now, use the basic search functionality
    # In a more sophisticated implementation, you'd add filtering logic
    vendors_data = db.get_vendors(limit=limit, offset=offset, search=query)
    vendors = [Vendor(**vendor) for vendor in vendors_data]
    
    return VendorListResponse(
        vendors=vendors,
        total=len(vendors),
        limit=limit,
        offset=offset
    )


@router.get("/search/equipment", response_model=EquipmentListResponse)
async def search_equipment(
    query: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Search equipment with filters."""
    # For now, use the basic search functionality
    # In a more sophisticated implementation, you'd add filtering logic
    equipment_data = db.get_equipment(limit=limit, offset=offset, search=query)
    equipment_list = [Equipment(**eq) for eq in equipment_data]
    
    return EquipmentListResponse(
        equipment=equipment_list,
        total=len(equipment_list),
        limit=limit,
        offset=offset
    ) 