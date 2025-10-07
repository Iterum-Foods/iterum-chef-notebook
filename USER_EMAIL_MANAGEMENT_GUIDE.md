# 📧 User & Email Management Guide

## Current Status: October 7, 2025

---

## 📊 User Management Overview

### Current System Architecture

Your app currently uses a **hybrid user management system** with multiple layers:

#### 1. **Frontend User Storage** (Active)
- **Location:** Browser `localStorage`
- **Type:** Client-side only
- **Users Tracked:**
  - Trial users (new!)
  - Google Sign-In users (Firebase)
  - Email/Password users (Firebase)
  - Local offline profiles

#### 2. **Backend Database** (Available but Not Fully Connected)
- **Location:** SQLite database (`culinary_data.db`)
- **Status:** Backend API exists but not actively used by frontend
- **Models:** `User`, `Recipe`, `Ingredient`, etc.

#### 3. **Firebase Authentication** (Active)
- **Location:** Firebase Cloud
- **Features:** Google Sign-In, Email/Password auth
- **Integration:** Connected to frontend

---

## 👥 User Types & Storage

### 1. Trial Users (NEW - Just Implemented!)

**Storage Location:** `localStorage: trial_users`

**Data Collected:**
```javascript
{
    name: "Chef Name",
    email: "chef@email.com",
    company: "Restaurant Name",
    role: "executive-chef",
    source: "google",
    startDate: "2025-10-07T...",
    endDate: "2025-10-21T...",  // 14 days later
    signedUpAt: "2025-10-07T..."
}
```

**Access:** Trial Dashboard at `/trial_dashboard.html`

**Export Options:**
- CSV export
- JSON export
- View in dashboard

### 2. Firebase Users (Google Sign-In)

**Storage Location:** Firebase Authentication + `localStorage`

**Data Collected:**
```javascript
{
    id: "firebase_uid_xxx",
    userId: "firebase_uid_xxx",
    name: "User Display Name",
    email: "user@gmail.com",
    photoURL: "https://...",
    type: "google",
    createdAt: "2025-10-07T..."
}
```

**Access:** Firebase Console

### 3. Firebase Users (Email/Password)

**Storage Location:** Firebase Authentication + `localStorage`

**Data Collected:**
```javascript
{
    id: "firebase_uid_xxx",
    userId: "firebase_uid_xxx",
    name: "User Name",
    email: "user@email.com",
    type: "email",
    createdAt: "2025-10-07T..."
}
```

**Access:** Firebase Console

### 4. Local Offline Profiles (Legacy)

**Storage Location:** `localStorage: saved_users`

**Data Collected:**
```javascript
{
    id: "local-xxx",
    name: "Chef Name",
    email: "chef@email.com",
    role: "Chef",
    restaurant: "My Kitchen",
    type: "local",
    createdAt: "2025-10-07T..."
}
```

**Access:** Browser localStorage only

---

## 📧 Email Management: CURRENT STATE

### ⚠️ **CRITICAL:** No Email System Currently Active

**Current Status:**
- ❌ No email sending infrastructure configured
- ❌ No SMTP server connected
- ❌ No automated emails being sent
- ❌ Users are NOT receiving welcome/trial emails

**What Exists:**
- ✅ Email templates designed (in `email_templates.html`)
- ✅ User emails being collected and stored
- ✅ Backend email settings placeholders (in `settings.py`)
- ❌ **BUT: Nothing is actually sending emails**

### Email Templates Available (Not Active)

Located in `email_templates.html`:

1. **Welcome Email** - "Welcome to the Culinary Revolution 🍅"
2. **Behind the Scenes** - Development updates
3. **Social Proof** - Testimonials and stats
4. **Feature Deep Dive** - Product education
5. **Urgency Builder** - Launch/conversion email

**Status:** Templates designed but NOT connected to sending system

---

## 🚨 What You Need to Implement

### Priority 1: Email Sending Infrastructure

#### Option A: SendGrid (Recommended)
**Best for:** Production email at scale

```python
# Install
pip install sendgrid

# Configuration needed
SENDGRID_API_KEY=your_key_here
FROM_EMAIL=noreply@iterumfoods.com
```

**Setup Steps:**
1. Create SendGrid account (free tier: 100 emails/day)
2. Verify sender email address
3. Get API key
4. Add to environment variables
5. Implement sending function

#### Option B: AWS SES
**Best for:** High volume, low cost

```python
# Install
pip install boto3

# Configuration needed
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

#### Option C: Mailgun
**Best for:** Developer-friendly API

```python
# Install
pip install requests

# Configuration needed
MAILGUN_API_KEY=your_key
MAILGUN_DOMAIN=mg.yourdomain.com
```

#### Option D: Gmail SMTP (Quick Start)
**Best for:** Testing, small volume

```python
# No install needed (built-in smtplib)

# Configuration needed
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password  # NOT your regular password!
```

---

## 📋 Implementation Roadmap

### Week 1: Email Infrastructure Setup

#### Day 1-2: Choose & Configure Email Service
- [ ] Select email provider (SendGrid recommended)
- [ ] Create account and verify sender
- [ ] Get API credentials
- [ ] Add credentials to environment

#### Day 3-4: Build Email Sending System
- [ ] Create `app/services/email_service.py`
- [ ] Implement send_email function
- [ ] Convert HTML templates to Python
- [ ] Test email sending

#### Day 5: Integrate with Trial System
- [ ] Connect trial sign-up to email trigger
- [ ] Send welcome email on trial start
- [ ] Test end-to-end flow

### Week 2: Automated Email Sequences

#### Day 1-2: Welcome Sequence
- [ ] Day 0: Welcome email (immediate)
- [ ] Day 1: Getting started guide
- [ ] Day 3: Feature highlight #1
- [ ] Day 7: Mid-trial check-in

#### Day 3-4: Trial Ending Sequence
- [ ] Day 10: "4 days left" reminder
- [ ] Day 12: "2 days left" + conversion offer
- [ ] Day 14: "Trial ended" + upgrade link
- [ ] Day 16: "Last chance" re-engagement

#### Day 5: Testing & Monitoring
- [ ] Test all email triggers
- [ ] Set up email analytics
- [ ] Monitor delivery rates
- [ ] Track open/click rates

---

## 🔧 Quick Start: Minimal Email System

Here's the **fastest way** to get emails working (using Gmail):

### Step 1: Create Email Service File

Create `app/services/email_service.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import os

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ):
        """Send an email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Add text version
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    def send_trial_welcome(self, user_name: str, user_email: str):
        """Send trial welcome email"""
        subject = "🎁 Welcome to Your 14-Day Trial!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Welcome to Iterum, {user_name}! 🎉</h2>
            
            <p>Your 14-day free trial is now active!</p>
            
            <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 10px; padding: 16px; margin: 20px 0;">
                <strong>✨ Your Trial Includes:</strong>
                <ul>
                    <li>Unlimited recipe development</li>
                    <li>Unlimited menu creation</li>
                    <li>Full analytics & insights</li>
                    <li>All premium features</li>
                </ul>
            </div>
            
            <p><strong>Trial expires:</strong> {(datetime.now() + timedelta(days=14)).strftime('%B %d, %Y')}</p>
            
            <a href="https://iterum-culinary-app.web.app" 
               style="display: inline-block; background: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin: 20px 0;">
                Start Using Iterum →
            </a>
            
            <p>Questions? Just reply to this email!</p>
            
            <p>The Iterum Team</p>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)

# Global instance
email_service = EmailService()
```

### Step 2: Add Environment Variables

Create or update `.env`:

```bash
# Gmail SMTP (for testing)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password  # NOT your regular Gmail password!
FROM_EMAIL=noreply@iterumfoods.com
```

**Important:** For Gmail, you need an "App Password":
1. Go to Google Account settings
2. Security → 2-Step Verification (enable if not enabled)
3. App Passwords → Generate new app password
4. Use that password (not your regular Gmail password)

### Step 3: Trigger Emails from Frontend

Update `launch.html` trial sign-up to call backend:

```javascript
// After successful trial sign-up
async function notifyBackendOfTrialSignup(user) {
    try {
        const response = await fetch('/api/trial/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: user.name,
                email: user.email,
                company: user.company,
                role: user.role,
                source: user.source
            })
        });
        
        if (response.ok) {
            console.log('✅ Welcome email sent!');
        }
    } catch (error) {
        console.warn('⚠️ Email notification failed:', error);
        // Don't block user - email failure is non-critical
    }
}
```

### Step 4: Create Backend Endpoint

Add to `app/routers/trial.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.email_service import email_service

router = APIRouter()

class TrialSignup(BaseModel):
    name: str
    email: str
    company: str = None
    role: str = None
    source: str = None

@router.post("/trial/signup")
async def trial_signup(signup: TrialSignup):
    """Handle trial signup and send welcome email"""
    try:
        # Send welcome email
        success = email_service.send_trial_welcome(
            signup.name,
            signup.email
        )
        
        if not success:
            # Log error but don't fail the request
            print(f"⚠️ Failed to send email to {signup.email}")
        
        return {
            "success": True,
            "message": "Trial activated",
            "email_sent": success
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 📊 Email Analytics You Should Track

### Delivery Metrics
- **Sent:** Total emails sent
- **Delivered:** Successfully delivered (not bounced)
- **Bounced:** Failed to deliver
- **Spam Reports:** Marked as spam

### Engagement Metrics
- **Open Rate:** % of emails opened
- **Click Rate:** % who clicked links
- **Conversion Rate:** % who became paid users
- **Unsubscribe Rate:** % who opted out

### Trial-Specific Metrics
- **Welcome Email Open Rate** (target: 50%+)
- **Day 7 Email Response Rate** (target: 20%+)
- **Trial End Email Click Rate** (target: 30%+)
- **Email-to-Conversion Rate** (target: 15%+)

---

## 🎯 Recommended Email Sequence for Trial Users

### Day 0 (Immediate): Welcome
**Subject:** 🎁 Welcome to Your 14-Day Trial!
**Goal:** Onboard, set expectations
**CTA:** Start using the app

### Day 1: Getting Started
**Subject:** Ready to create your first recipe?
**Goal:** Drive first action
**CTA:** Create first recipe

### Day 3: Feature Highlight
**Subject:** Did you know you can import recipes?
**Goal:** Increase feature adoption
**CTA:** Try recipe import

### Day 7: Mid-Trial Check-In
**Subject:** You're halfway through your trial!
**Goal:** Re-engage, offer help
**CTA:** Book support call

### Day 10: Urgency Start
**Subject:** ⏰ 4 days left in your trial
**Goal:** Create urgency
**CTA:** View pricing

### Day 12: Strong Urgency
**Subject:** ⚡ Last 2 days - Special offer inside
**Goal:** Drive conversion
**CTA:** Upgrade now (20% off)

### Day 14: Trial Ended
**Subject:** Your trial has ended - Keep your data
**Goal:** Convert or retain
**CTA:** Subscribe to keep access

### Day 16: Last Chance
**Subject:** We'd hate to lose you...
**Goal:** Win back
**CTA:** Reactivate (one-time discount)

---

## 💾 Current User Data Export

### Trial Users
**Location:** Trial Dashboard → Export CSV/JSON
**Fields:** Name, Email, Company, Role, Source, Start Date, End Date, Days Remaining

### Firebase Users
**Location:** Firebase Console → Authentication → Export users
**Fields:** UID, Email, Display Name, Photo URL, Created Date

### All Saved Users
**Location:** Browser DevTools → localStorage → `saved_users`
**Fields:** All user profiles stored locally

---

## ⚠️ Critical Gaps & Priorities

### Immediate (This Week)
1. ❌ **No email system active** - Trial users aren't receiving welcome emails
2. ❌ **No backend sync** - Trial users only in localStorage (can be lost)
3. ❌ **No email nurture** - No automated follow-ups

### Short-Term (Next 2 Weeks)
1. ❌ **No CRM integration** - Can't manage leads at scale
2. ❌ **No analytics** - Don't know email performance
3. ❌ **No segmentation** - Can't target by role/behavior

### Medium-Term (Next Month)
1. ❌ **No payment system** - Can't convert trials to paid
2. ❌ **No subscription management** - No billing system
3. ❌ **No customer portal** - Users can't manage accounts

---

## 🎬 Action Plan: Next 7 Days

### Monday
- [ ] Choose email service (recommend SendGrid)
- [ ] Create account and verify sender
- [ ] Get API credentials

### Tuesday
- [ ] Implement email service in backend
- [ ] Create welcome email template
- [ ] Test email sending

### Wednesday
- [ ] Connect trial sign-up to email trigger
- [ ] Deploy to production
- [ ] Test end-to-end

### Thursday
- [ ] Create Day 7 check-in email
- [ ] Set up email scheduling
- [ ] Test automated sequence

### Friday
- [ ] Create trial expiration emails
- [ ] Set up conversion tracking
- [ ] Monitor first results

### Weekend
- [ ] Review email analytics
- [ ] Optimize email content
- [ ] Plan next week's emails

---

## 📞 Support & Resources

### Email Service Providers
- **SendGrid:** https://sendgrid.com (100 free/day)
- **Mailgun:** https://mailgun.com (5,000 free/month)
- **AWS SES:** https://aws.amazon.com/ses ($0.10/1000 emails)

### Email Template Tools
- **MJML:** Responsive email framework
- **Litmus:** Email testing platform
- **Mail Tester:** Spam score checker

### Analytics & Tracking
- **Google Analytics:** Track email campaign performance
- **Mixpanel:** User behavior tracking
- **Segment:** Unified customer data

---

## ✅ Summary

### What You Have Now
- ✅ Trial user data collection
- ✅ User email addresses stored
- ✅ Email templates designed
- ✅ Trial dashboard for viewing data

### What You Need
- ❌ Email sending infrastructure
- ❌ Automated welcome emails
- ❌ Trial nurture sequence
- ❌ Conversion tracking
- ❌ Backend user sync

### Recommended Priority
1. **Set up SendGrid** (2 hours)
2. **Implement email service** (4 hours)
3. **Connect trial to emails** (2 hours)
4. **Test and deploy** (2 hours)

**Total Time:** ~10 hours to go from zero to working email system

---

**Questions? Next steps? Let me know what you want to tackle first!** 🚀

