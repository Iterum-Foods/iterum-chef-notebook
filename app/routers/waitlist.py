"""
Waitlist management router for the landing page
"""
from fastapi import APIRouter, HTTPException, Depends, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import sqlite3
import logging
from datetime import datetime, timedelta
import json
import secrets
import hashlib

router = APIRouter()
logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)

# Simple admin credentials (in production, use environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "iterum2025!"  # Change this in production
ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()

# Simple session store (in production, use Redis or database)
active_sessions = {}

class WaitlistEntry(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None
    source: str = "landing_page"
    interests: Optional[List[str]] = []

class WaitlistResponse(BaseModel):
    success: bool
    message: str
    position: Optional[int] = None

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None

def init_waitlist_db():
    """Initialize the waitlist database"""
    try:
        conn = sqlite3.connect('waitlist.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS waitlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                company TEXT,
                role TEXT,
                source TEXT DEFAULT 'landing_page',
                interests TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_email ON waitlist(email);
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_created_at ON waitlist(created_at);
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Waitlist database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize waitlist database: {e}")
        raise

@router.post("/signup", response_model=WaitlistResponse)
async def join_waitlist(entry: WaitlistEntry):
    """Add a new entry to the waitlist"""
    try:
        # Initialize database if not exists
        init_waitlist_db()
        
        conn = sqlite3.connect('waitlist.db')
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM waitlist WHERE email = ?", (entry.email,))
        existing = cursor.fetchone()
        
        if existing:
            conn.close()
            raise HTTPException(
                status_code=409, 
                detail="Email already registered on waitlist"
            )
        
        # Insert new entry
        current_time = datetime.now().isoformat()
        interests_json = json.dumps(entry.interests) if entry.interests else "[]"
        
        cursor.execute('''
            INSERT INTO waitlist (
                email, name, company, role, source, interests, 
                created_at, updated_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.email,
            entry.name,
            entry.company,
            entry.role,
            entry.source,
            interests_json,
            current_time,
            current_time,
            'active'
        ))
        
        # Get position in waitlist
        cursor.execute("SELECT COUNT(*) FROM waitlist WHERE status = 'active'")
        position = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ New waitlist signup: {entry.email} (position: {position})")
        
        return WaitlistResponse(
            success=True,
            message="Successfully joined the waitlist!",
            position=position
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Waitlist signup failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to join waitlist. Please try again."
        )

@router.get("/stats")
async def get_waitlist_stats():
    """Get waitlist statistics (public endpoint)"""
    try:
        init_waitlist_db()
        
        conn = sqlite3.connect('waitlist.db')
        cursor = conn.cursor()
        
        # Total signups
        cursor.execute("SELECT COUNT(*) FROM waitlist WHERE status = 'active'")
        total_signups = cursor.fetchone()[0]
        
        # Signups by source
        cursor.execute('''
            SELECT source, COUNT(*) 
            FROM waitlist 
            WHERE status = 'active' 
            GROUP BY source
        ''')
        by_source = dict(cursor.fetchall())
        
        # Recent signups (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) 
            FROM waitlist 
            WHERE status = 'active' 
            AND datetime(created_at) >= datetime('now', '-7 days')
        ''')
        recent_signups = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "success": True,
            "stats": {
                "total_signups": total_signups,
                "by_source": by_source,
                "recent_signups": recent_signups
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get waitlist stats: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve statistics"
        )

def verify_admin_session(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin session token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    token = credentials.credentials
    if token not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    # Check if session is expired
    session = active_sessions[token]
    if datetime.now() > session['expires']:
        del active_sessions[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )
    
    return session

@router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(login_data: AdminLogin):
    """Admin login for waitlist management"""
    try:
        # Verify credentials
        password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
        
        if login_data.username != ADMIN_USERNAME or password_hash != ADMIN_PASSWORD_HASH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Create session token
        token = secrets.token_urlsafe(32)
        expires = datetime.now() + timedelta(hours=24)
        
        active_sessions[token] = {
            'username': login_data.username,
            'expires': expires,
            'created': datetime.now()
        }
        
        logger.info(f"✅ Admin login successful: {login_data.username}")
        
        return AdminLoginResponse(
            success=True,
            message="Login successful",
            token=token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Admin login failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Login failed"
        )

@router.post("/admin/logout")
async def admin_logout(session: dict = Depends(verify_admin_session)):
    """Admin logout"""
    try:
        # Find and remove the session
        for token, sess in list(active_sessions.items()):
            if sess['username'] == session['username']:
                del active_sessions[token]
                break
        
        logger.info(f"✅ Admin logout: {session['username']}")
        
        return {"success": True, "message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"❌ Admin logout failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Logout failed"
        )

@router.get("/admin/verify")
async def verify_admin_session_endpoint(session: dict = Depends(verify_admin_session)):
    """Verify if admin session is valid"""
    return {
        "success": True,
        "username": session['username'],
        "expires": session['expires'].isoformat()
    }

@router.get("/admin/list")
async def get_waitlist_entries(
    limit: int = 100,
    offset: int = 0,
    status: str = "active",
    session: dict = Depends(verify_admin_session)
):
    """Admin endpoint to view waitlist entries (requires authentication)"""
    try:
        init_waitlist_db()
        
        conn = sqlite3.connect('waitlist.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, name, company, role, source, 
                   created_at, status, interests
            FROM waitlist 
            WHERE status = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (status, limit, offset))
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                "id": row[0],
                "email": row[1],
                "name": row[2],
                "company": row[3],
                "role": row[4],
                "source": row[5],
                "created_at": row[6],
                "status": row[7],
                "interests": json.loads(row[8]) if row[8] else []
            })
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM waitlist WHERE status = ?", (status,))
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "success": True,
            "entries": entries,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get waitlist entries: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve waitlist entries"
        )

@router.delete("/admin/entry/{email}")
async def remove_from_waitlist(email: str, session: dict = Depends(verify_admin_session)):
    """Admin endpoint to remove entry from waitlist (requires authentication)"""
    try:
        init_waitlist_db()
        
        conn = sqlite3.connect('waitlist.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE waitlist SET status = 'removed', updated_at = ? WHERE email = ?",
            (datetime.now().isoformat(), email)
        )
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Email not found in waitlist")
        
        conn.commit()
        conn.close()
        
        logger.info(f"🗑️ Removed from waitlist: {email}")
        
        return {
            "success": True,
            "message": f"Successfully removed {email} from waitlist"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to remove from waitlist: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to remove from waitlist"
        )

# Initialize database when router is imported
try:
    init_waitlist_db()
except Exception as e:
    logger.warning(f"⚠️ Could not initialize waitlist database: {e}")