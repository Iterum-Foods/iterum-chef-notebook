"""
Notes Sync Router - Backend endpoints for daily notes synchronization
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user

router = APIRouter()


# Pydantic models
class NotesSyncRequest(BaseModel):
    date: str  # Format: YYYY-MM-DD
    notes_data: dict  # { category: content }


class NotesResponse(BaseModel):
    id: int
    user_id: int
    date: str
    notes_data: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Database model
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import json


class DailyNote(Base):
    __tablename__ = "daily_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, index=True, nullable=False)
    notes_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


@router.post("/sync", response_model=NotesResponse)
async def sync_notes(
    notes_sync: NotesSyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sync daily notes to backend
    """
    try:
        # Parse date
        note_date = datetime.strptime(notes_sync.date, "%Y-%m-%d").date()

        # Check if note already exists for this date
        existing_note = db.query(DailyNote).filter(
            DailyNote.user_id == current_user.id,
            DailyNote.date == note_date
        ).first()

        if existing_note:
            # Update existing note
            existing_note.notes_data = json.dumps(notes_sync.notes_data)
            existing_note.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_note)
            
            return NotesResponse(
                id=existing_note.id,
                user_id=existing_note.user_id,
                date=existing_note.date.isoformat(),
                notes_data=json.loads(existing_note.notes_data),
                created_at=existing_note.created_at,
                updated_at=existing_note.updated_at
            )
        else:
            # Create new note
            new_note = DailyNote(
                user_id=current_user.id,
                date=note_date,
                notes_data=json.dumps(notes_sync.notes_data)
            )
            db.add(new_note)
            db.commit()
            db.refresh(new_note)
            
            return NotesResponse(
                id=new_note.id,
                user_id=new_note.user_id,
                date=new_note.date.isoformat(),
                notes_data=json.loads(new_note.notes_data),
                created_at=new_note.created_at,
                updated_at=new_note.updated_at
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/date/{date}", response_model=Optional[NotesResponse])
async def get_notes_by_date(
    date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notes for a specific date
    """
    try:
        note_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    note = db.query(DailyNote).filter(
        DailyNote.user_id == current_user.id,
        DailyNote.date == note_date
    ).first()

    if not note:
        return None

    return NotesResponse(
        id=note.id,
        user_id=note.user_id,
        date=note.date.isoformat(),
        notes_data=json.loads(note.notes_data),
        created_at=note.created_at,
        updated_at=note.updated_at
    )


@router.get("/all")
async def get_all_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all notes for the current user
    """
    notes = db.query(DailyNote).filter(
        DailyNote.user_id == current_user.id
    ).order_by(DailyNote.date.desc()).all()

    return [
        NotesResponse(
            id=note.id,
            user_id=note.user_id,
            date=note.date.isoformat(),
            notes_data=json.loads(note.notes_data),
            created_at=note.created_at,
            updated_at=note.updated_at
        )
        for note in notes
    ]


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a note
    """
    note = db.query(DailyNote).filter(
        DailyNote.id == note_id,
        DailyNote.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}

