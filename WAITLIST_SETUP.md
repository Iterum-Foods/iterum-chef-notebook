# 🍅 Iterum Recipe Library - Waitlist Setup Guide

Complete guide to set up and manage your waitlist functionality for the Recipe Library platform.

## ✅ What's Included

Your waitlist system is now **fully functional** with:

### **Frontend Features:**
- ✅ **Professional Landing Page** with integrated waitlist form
- ✅ **Real-time Signup Counter** (updates automatically)
- ✅ **Success States** with waitlist position display
- ✅ **Error Handling** for duplicate emails and connection issues
- ✅ **Mobile Responsive** design for all devices

### **Backend API:**
- ✅ **SQLite Database** for storing waitlist entries
- ✅ **FastAPI REST API** with automatic documentation
- ✅ **Admin Endpoints** for viewing and managing signups
- ✅ **Real-time Statistics** and analytics
- ✅ **Duplicate Prevention** and validation

### **Admin Interface:**
- ✅ **Live Dashboard** with real-time stats
- ✅ **Waitlist Entries Table** with search and filtering
- ✅ **Auto-refresh** every 30 seconds
- ✅ **Export Capabilities** for email marketing

## 🚀 Quick Start

### **Option 1: Windows Users**
```bash
# Double-click to start the server
start_waitlist_server.bat
```

### **Option 2: All Platforms**
```bash
# Using Python launcher
python start_waitlist_server.py
```

### **Option 3: Manual Start**
```bash
# Install dependencies
pip install fastapi uvicorn pydantic[email]

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Access Points

Once the server is running:

| Service | URL | Description |
|---------|-----|-------------|
| **Landing Page** | http://localhost:8000/index.html | Main website with waitlist form |
| **Waitlist Admin** | http://localhost:8000/waitlist_admin.html | Admin dashboard for managing signups |
| **API Documentation** | http://localhost:8000/docs | Interactive API documentation |
| **API Stats** | http://localhost:8000/api/waitlist/stats | Public waitlist statistics |

## 📊 API Endpoints

### **Public Endpoints:**

#### **Join Waitlist**
```http
POST /api/waitlist/signup
Content-Type: application/json

{
  "email": "chef@restaurant.com",
  "name": "Chef Smith",
  "company": "Fine Dining Restaurant",
  "role": "Head Chef",
  "source": "landing_page"
}
```

#### **Get Statistics**
```http
GET /api/waitlist/stats

Response:
{
  "success": true,
  "stats": {
    "total_signups": 1247,
    "by_source": {
      "landing_page": 1100,
      "social_media": 147
    },
    "recent_signups": 23
  }
}
```

### **Admin Endpoints:**

#### **List All Entries**
```http
GET /api/waitlist/admin/list?limit=100&offset=0&status=active
```

#### **Remove Entry**
```http
DELETE /api/waitlist/admin/entry/{email}
```

## 🗄️ Database Schema

Waitlist entries are stored in SQLite (`waitlist.db`) with this structure:

```sql
CREATE TABLE waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    company TEXT,
    role TEXT,
    source TEXT DEFAULT 'landing_page',
    interests TEXT,  -- JSON array
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    notes TEXT
);
```

## 🔧 Configuration

### **Environment Variables:**
```bash
# Optional: Configure database location
WAITLIST_DB_PATH=/path/to/waitlist.db

# Optional: Configure server settings
HOST=0.0.0.0
PORT=8000
```

### **Custom Domains:**
For production use with your custom domain, update the CORS settings in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://iterumfoods.xyz", "https://www.iterumfoods.xyz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📈 Analytics & Insights

### **Waitlist Growth Tracking:**
- **Total Signups**: All-time waitlist registrations
- **Recent Activity**: Signups in the last 7 days
- **Source Attribution**: Track where signups come from
- **Conversion Rates**: Landing page to signup ratios

### **Business Metrics:**
- **Target Audience**: Restaurants, catering, private chefs, consultants
- **Professional Validation**: Company and role information
- **Geographic Distribution**: Track by company locations
- **Engagement Patterns**: Peak signup times and trends

## 🚀 Deployment to Production

### **1. Server Deployment:**
```bash
# Install dependencies
pip install fastapi uvicorn pydantic[email] gunicorn

# Run with Gunicorn for production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### **2. Database Backup:**
```bash
# Regular backup of waitlist data
cp waitlist.db waitlist_backup_$(date +%Y%m%d).db
```

### **3. Security Considerations:**
- Add authentication to admin endpoints
- Use HTTPS in production
- Implement rate limiting for signup endpoint
- Regular database backups
- Monitor for spam/abuse

## 📧 Email Integration

### **Mailchimp Integration:**
```python
# Add to your signup endpoint
import mailchimp3

def add_to_mailchimp(email, name, company):
    client = mailchimp3.MailChimp(api_key='your_api_key')
    client.lists.members.create('list_id', {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'FNAME': name,
            'COMPANY': company
        }
    })
```

### **Email Templates:**
Your existing `email_templates.html` includes:
- Welcome email for new signups
- Launch notification templates
- Weekly update formats

## 🎯 Marketing Integration

### **Social Media Tracking:**
Add UTM parameters to track signup sources:
```html
<!-- Facebook -->
<a href="https://iterumfoods.xyz?utm_source=facebook&utm_medium=social&utm_campaign=waitlist">

<!-- Twitter -->
<a href="https://iterumfoods.xyz?utm_source=twitter&utm_medium=social&utm_campaign=waitlist">
```

### **Referral Tracking:**
Extend the waitlist form to include referral codes:
```javascript
// Add to signup data
{
  email: email,
  source: 'referral',
  referral_code: urlParams.get('ref')
}
```

## 🔍 Troubleshooting

### **Common Issues:**

#### **Port Already in Use:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F
```

#### **Database Permissions:**
```bash
# Ensure write permissions
chmod 664 waitlist.db
```

#### **CORS Errors:**
Update allowed origins in `app/main.py` to include your domain.

#### **Form Not Submitting:**
Check browser console for JavaScript errors and verify API endpoint URLs.

## 📞 Support

For technical support:
- **GitHub Issues**: [Your Repository Issues](https://github.com/Iterum-Foods/iterum-chef-notebook/issues)
- **Email**: hello@iterumfoods.xyz
- **Documentation**: This guide and API docs at `/docs`

## 🎉 Success Metrics

Your waitlist is ready to track:
- ✅ **Professional Signups**: Restaurants, caterers, private chefs
- ✅ **Market Validation**: Demand for recipe library platform
- ✅ **Investor Traction**: Real numbers for pitch presentations
- ✅ **Launch Readiness**: Email list for product launch
- ✅ **Business Intelligence**: Customer insights and market research

**Ready to revolutionize professional recipe management!** 🍅✨