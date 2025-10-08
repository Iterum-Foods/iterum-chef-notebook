"""
Trial User Management API
Handles trial signups, tracking, and email notifications
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import sqlite3
import json
import logging

# Import email service
try:
    from app.services.email_service import email_service
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    logging.warning("⚠️ Email service not available")

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trial", tags=["trial"])


class TrialSignup(BaseModel):
    """Trial signup data"""
    name: str
    email: EmailStr
    company: Optional[str] = None
    role: Optional[str] = None
    source: Optional[str] = None


class TrialUser(BaseModel):
    """Trial user data"""
    id: str
    name: str
    email: str
    company: Optional[str]
    role: Optional[str]
    source: Optional[str]
    trial_start_date: str
    trial_end_date: str
    days_remaining: int
    status: str  # active, expiring, expired
    created_at: str


def init_trial_db():
    """Initialize trial users database"""
    try:
        conn = sqlite3.connect('trial_users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trial_users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                company TEXT,
                role TEXT,
                source TEXT,
                trial_start_date TEXT NOT NULL,
                trial_end_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_email_sent TEXT,
                email_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_email ON trial_users(email)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_trial_end ON trial_users(trial_end_date)
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Trial database initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize trial database: {e}")


# Initialize database on startup
init_trial_db()


def send_welcome_email_async(name: str, email: str):
    """Send welcome email in background"""
    if EMAIL_AVAILABLE:
        try:
            success = email_service.send_trial_welcome(name, email)
            if success:
                logger.info(f"✅ Welcome email sent to {email}")
            else:
                logger.warning(f"⚠️ Failed to send welcome email to {email}")
        except Exception as e:
            logger.error(f"❌ Error sending welcome email: {e}")
    else:
        logger.info(f"📧 Email service not configured - would send welcome email to {email}")


@router.post("/signup")
async def trial_signup(
    signup: TrialSignup,
    background_tasks: BackgroundTasks
):
    """
    Handle trial signup and send welcome email
    
    This endpoint:
    1. Saves trial user to database
    2. Sends welcome email in background
    3. Returns success response
    """
    try:
        # Generate trial dates
        trial_start = datetime.now()
        trial_end = trial_start + timedelta(days=14)
        user_id = f"trial_{int(trial_start.timestamp() * 1000)}"
        
        # Save to database
        conn = sqlite3.connect('trial_users.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO trial_users 
                (id, name, email, company, role, source, trial_start_date, trial_end_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                signup.name,
                signup.email,
                signup.company,
                signup.role,
                signup.source,
                trial_start.isoformat(),
                trial_end.isoformat(),
                trial_start.isoformat()
            ))
            conn.commit()
            logger.info(f"✅ Trial user saved: {signup.email}")
        except sqlite3.IntegrityError:
            # User already exists - update instead
            cursor.execute('''
                UPDATE trial_users 
                SET name = ?, company = ?, role = ?, source = ?
                WHERE email = ?
            ''', (signup.name, signup.company, signup.role, signup.source, signup.email))
            conn.commit()
            logger.info(f"✅ Trial user updated: {signup.email}")
        finally:
            conn.close()
        
        # Send welcome email in background
        background_tasks.add_task(send_welcome_email_async, signup.name, signup.email)
        
        return {
            "success": True,
            "message": "Trial activated successfully",
            "user_id": user_id,
            "trial_end_date": trial_end.isoformat(),
            "days_remaining": 14,
            "email_will_be_sent": EMAIL_AVAILABLE
        }
        
    except Exception as e:
        logger.error(f"❌ Trial signup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process trial signup: {str(e)}")


@router.get("/users")
async def get_trial_users():
    """
    Get all trial users with calculated status
    """
    try:
        conn = sqlite3.connect('trial_users.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM trial_users ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        now = datetime.now()
        users = []
        
        for row in rows:
            trial_end = datetime.fromisoformat(row['trial_end_date'])
            days_remaining = (trial_end - now).days
            
            # Determine status
            if days_remaining > 3:
                status = "active"
            elif days_remaining > 0:
                status = "expiring"
            else:
                status = "expired"
            
            users.append({
                "id": row['id'],
                "name": row['name'],
                "email": row['email'],
                "company": row['company'],
                "role": row['role'],
                "source": row['source'],
                "trial_start_date": row['trial_start_date'],
                "trial_end_date": row['trial_end_date'],
                "days_remaining": max(0, days_remaining),
                "status": status,
                "created_at": row['created_at'],
                "email_count": row['email_count']
            })
        
        return {
            "success": True,
            "count": len(users),
            "users": users
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get trial users: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_trial_stats():
    """
    Get trial user statistics
    """
    try:
        conn = sqlite3.connect('trial_users.db')
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM trial_users')
        total_users = cursor.fetchone()[0]
        
        # Active trials (not expired)
        now = datetime.now().isoformat()
        cursor.execute('SELECT COUNT(*) FROM trial_users WHERE trial_end_date > ?', (now,))
        active_trials = cursor.fetchone()[0]
        
        # Expiring soon (next 3 days)
        soon = (datetime.now() + timedelta(days=3)).isoformat()
        cursor.execute(
            'SELECT COUNT(*) FROM trial_users WHERE trial_end_date > ? AND trial_end_date <= ?',
            (now, soon)
        )
        expiring_soon = cursor.fetchone()[0]
        
        # Expired
        cursor.execute('SELECT COUNT(*) FROM trial_users WHERE trial_end_date <= ?', (now,))
        expired = cursor.fetchone()[0]
        
        # This week signups
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM trial_users WHERE created_at >= ?', (week_ago,))
        this_week = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "success": True,
            "stats": {
                "total_users": total_users,
                "active_trials": active_trials,
                "expiring_soon": expiring_soon,
                "expired": expired,
                "signups_this_week": this_week,
                "conversion_rate": 0  # TODO: Calculate from payment data
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get trial stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-reminder/{email}")
async def send_trial_reminder(email: str, background_tasks: BackgroundTasks):
    """
    Manually send trial reminder email
    """
    if not EMAIL_AVAILABLE:
        raise HTTPException(status_code=503, detail="Email service not configured")
    
    try:
        conn = sqlite3.connect('trial_users.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM trial_users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="Trial user not found")
        
        trial_end = datetime.fromisoformat(user['trial_end_date'])
        days_remaining = (trial_end - datetime.now()).days
        
        # Update email count
        cursor.execute(
            'UPDATE trial_users SET email_count = email_count + 1, last_email_sent = ? WHERE email = ?',
            (datetime.now().isoformat(), email)
        )
        conn.commit()
        conn.close()
        
        # Send appropriate email based on days remaining
        if days_remaining == 7:
            background_tasks.add_task(
                email_service.send_trial_reminder_day7,
                user['name'],
                user['email']
            )
        elif days_remaining <= 4:
            background_tasks.add_task(
                email_service.send_trial_expiring_soon,
                user['name'],
                user['email'],
                days_remaining
            )
        elif days_remaining <= 0:
            background_tasks.add_task(
                email_service.send_trial_expired,
                user['name'],
                user['email']
            )
        else:
            # Send day 7 reminder as default
            background_tasks.add_task(
                email_service.send_trial_reminder_day7,
                user['name'],
                user['email']
            )
        
        return {
            "success": True,
            "message": f"Reminder email will be sent to {email}",
            "days_remaining": days_remaining
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to send reminder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-email/{email}")
async def test_email(email: str, background_tasks: BackgroundTasks):
    """
    Test email sending with a welcome email
    """
    if not EMAIL_AVAILABLE:
        raise HTTPException(status_code=503, detail="Email service not configured")
    
    background_tasks.add_task(
        email_service.send_trial_welcome,
        "Test User",
        email
    )
    
    return {
        "success": True,
        "message": f"Test email will be sent to {email}",
        "note": "Check your inbox in a few moments"
    }

