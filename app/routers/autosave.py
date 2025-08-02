"""
Auto-save API endpoints for Iterum R&D Chef Notebook
Handles automatic saving of user work across different screens
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import json
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/autosave", tags=["autosave"])

class AutoSaveData(BaseModel):
    """Model for auto-save data"""
    forms: Dict[str, Dict[str, Any]] = Field(..., description="Form data by form ID")
    timestamp: int = Field(..., description="Timestamp when data was saved")
    pageId: str = Field(..., description="Page identifier")
    url: str = Field(..., description="Page URL")
    userId: Optional[str] = Field(None, description="User ID if authenticated")

class AutoSaveResponse(BaseModel):
    """Response model for auto-save operations"""
    success: bool
    message: str
    saveId: Optional[str] = None
    timestamp: Optional[int] = None

# In-memory storage for demo purposes
# In production, you'd use a database
autosave_storage = {}

@router.post("/save", response_model=AutoSaveResponse)
async def save_autosave_data(data: AutoSaveData):
    """
    Save auto-save data for a user session
    """
    try:
        # Generate a unique save ID
        save_id = f"{data.pageId}_{data.timestamp}"
        
        # Store the data
        autosave_storage[save_id] = {
            "data": data.dict(),
            "created_at": datetime.now(),
            "page_id": data.pageId,
            "url": data.url
        }
        
        logger.info(f"Auto-saved data for page: {data.pageId}")
        
        return AutoSaveResponse(
            success=True,
            message="Data auto-saved successfully",
            saveId=save_id,
            timestamp=data.timestamp
        )
        
    except Exception as e:
        logger.error(f"Failed to save auto-save data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save data")

@router.get("/load/{page_id}")
async def load_autosave_data(page_id: str):
    """
    Load the most recent auto-save data for a page
    """
    try:
        # Find the most recent save for this page
        page_saves = [
            (save_id, save_data) for save_id, save_data in autosave_storage.items()
            if save_data["page_id"] == page_id
        ]
        
        if not page_saves:
            return {"success": True, "data": None, "message": "No auto-saved data found"}
        
        # Get the most recent save
        most_recent = max(page_saves, key=lambda x: x[1]["created_at"])
        save_id, save_data = most_recent
        
        return {
            "success": True,
            "data": save_data["data"],
            "saveId": save_id,
            "message": "Auto-saved data loaded successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to load auto-save data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load data")

@router.delete("/clear/{page_id}")
async def clear_autosave_data(page_id: str):
    """
    Clear auto-save data for a specific page
    """
    try:
        # Remove all saves for this page
        keys_to_remove = [
            save_id for save_id, save_data in autosave_storage.items()
            if save_data["page_id"] == page_id
        ]
        
        for key in keys_to_remove:
            del autosave_storage[key]
        
        logger.info(f"Cleared auto-save data for page: {page_id}")
        
        return AutoSaveResponse(
            success=True,
            message=f"Cleared {len(keys_to_remove)} auto-save entries for page: {page_id}"
        )
        
    except Exception as e:
        logger.error(f"Failed to clear auto-save data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear data")

@router.get("/list")
async def list_autosave_data():
    """
    List all auto-saved data (for debugging)
    """
    try:
        saves_summary = []
        for save_id, save_data in autosave_storage.items():
            saves_summary.append({
                "saveId": save_id,
                "pageId": save_data["page_id"],
                "url": save_data["url"],
                "createdAt": save_data["created_at"].isoformat(),
                "formCount": len(save_data["data"]["forms"])
            })
        
        return {
            "success": True,
            "saves": saves_summary,
            "totalSaves": len(saves_summary)
        }
        
    except Exception as e:
        logger.error(f"Failed to list auto-save data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list data")

@router.post("/cleanup")
async def cleanup_old_autosave_data(days_old: int = 7):
    """
    Clean up auto-save data older than specified days
    """
    try:
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        keys_to_remove = [
            save_id for save_id, save_data in autosave_storage.items()
            if save_data["created_at"] < cutoff_date
        ]
        
        for key in keys_to_remove:
            del autosave_storage[key]
        
        logger.info(f"Cleaned up {len(keys_to_remove)} old auto-save entries")
        
        return AutoSaveResponse(
            success=True,
            message=f"Cleaned up {len(keys_to_remove)} entries older than {days_old} days"
        )
        
    except Exception as e:
        logger.error(f"Failed to cleanup auto-save data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cleanup data")

# Health check for auto-save system
@router.get("/health")
async def autosave_health():
    """
    Health check for auto-save system
    """
    return {
        "status": "healthy",
        "service": "autosave",
        "totalSaves": len(autosave_storage),
        "features": {
            "save": True,
            "load": True,
            "clear": True,
            "cleanup": True
        }
    }