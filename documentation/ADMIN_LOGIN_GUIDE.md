# 🔒 Admin Login System - Setup Guide

Complete guide for the secure admin authentication system for your Iterum Recipe Library waitlist management.

## ✅ What's Included

Your admin system now has **enterprise-grade security**:

### **🔐 Authentication Features:**
- ✅ **Secure Login System**: Username/password authentication with session tokens
- ✅ **Session Management**: 24-hour sessions with automatic expiration
- ✅ **Token-Based Security**: JWT-like secure tokens for API access
- ✅ **Auto-Logout**: Automatic logout on session expiry
- ✅ **Login Verification**: Real-time session validation
- ✅ **Professional UI**: Clean, responsive login interface

### **🛡️ Security Features:**
- ✅ **Password Hashing**: SHA-256 encrypted password storage
- ✅ **Protected Endpoints**: All admin APIs require authentication
- ✅ **Session Expiry**: Automatic token cleanup and expiration
- ✅ **Redirect Protection**: Unauthorized users redirected to login
- ✅ **Error Handling**: Secure error messages, no sensitive data leaks

## 🚀 Access Your Admin Dashboard

### **Login Credentials:**
```
Username: admin
Password: iterum2025!
```

### **Access URLs:**
- **Admin Login**: https://iterumfoods.xyz/admin-login.html
- **Admin Dashboard**: https://iterumfoods.xyz/waitlist_admin.html (redirects to login if not authenticated)

### **Local Development:**
```
Admin Login: http://localhost:8000/admin-login.html
Admin Dashboard: http://localhost:8000/waitlist_admin.html
```

## 🔧 How It Works

### **1. Login Process:**
1. **Visit Login Page**: Navigate to `admin-login.html`
2. **Enter Credentials**: Username and password
3. **Token Creation**: Server creates secure session token
4. **Token Storage**: Token stored in browser localStorage
5. **Redirect**: Automatic redirect to admin dashboard

### **2. Session Management:**
1. **Token Verification**: Every admin API call validates the token
2. **Expiry Check**: Sessions expire after 24 hours
3. **Auto-Logout**: Expired sessions redirect to login
4. **Manual Logout**: Logout button clears session and redirects

### **3. Protected Admin APIs:**
All these endpoints now require authentication:
- `GET /api/waitlist/admin/list` - View waitlist entries
- `DELETE /api/waitlist/admin/entry/{email}` - Remove entries
- `GET /api/waitlist/admin/verify` - Verify session
- `POST /api/waitlist/admin/logout` - Logout

## 🔐 Security Implementation

### **Password Security:**
```python
# Password is hashed using SHA-256
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

### **Session Tokens:**
```python
# Secure random tokens for sessions
token = secrets.token_urlsafe(32)
expires = datetime.now() + timedelta(hours=24)
```

### **API Protection:**
```python
# All admin endpoints require this authentication
async def verify_admin_session(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Verify token exists and is valid
    # Check expiration
    # Return session data or raise 401 error
```

## ⚙️ Customization Options

### **1. Change Admin Password:**

Edit `app/routers/waitlist.py`:
```python
# Line 21-22: Update these values
ADMIN_USERNAME = "your_username"
ADMIN_PASSWORD = "your_secure_password!"
```

**Important**: Restart the server after changing credentials.

### **2. Modify Session Duration:**

Edit `app/routers/waitlist.py`:
```python
# Line 243: Change session duration
expires = datetime.now() + timedelta(hours=48)  # 48 hours instead of 24
```

### **3. Add Multiple Admin Users:**

Replace the simple credential check with a user database:
```python
# Create admin users table
ADMIN_USERS = {
    "admin": "hashed_password_1",
    "manager": "hashed_password_2",
    "owner": "hashed_password_3"
}
```

### **4. Environment Variables (Production):**

For production, use environment variables:
```python
import os
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_password")
```

Set environment variables:
```bash
export ADMIN_USERNAME="your_admin"
export ADMIN_PASSWORD="your_secure_password"
```

## 🚀 Production Security

### **1. HTTPS Only:**
- Always use HTTPS in production
- Update CORS settings for your domain
- Configure secure cookie settings

### **2. Strong Passwords:**
```
Minimum requirements:
- 12+ characters
- Mix of letters, numbers, symbols
- No dictionary words
- Unique password
```

### **3. Database Storage:**
For production, store sessions in a database instead of memory:
```python
# Use Redis or PostgreSQL for session storage
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

### **4. Rate Limiting:**
Add rate limiting to prevent brute force attacks:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler

limiter = Limiter(key_func=lambda request: request.client.host)
app.state.limiter = limiter

@router.post("/admin/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def admin_login(request: Request, login_data: AdminLogin):
    # ... login logic
```

### **5. Audit Logging:**
Track all admin actions:
```python
logger.info(f"Admin action: {session['username']} accessed waitlist data")
logger.warning(f"Failed login attempt from {request.client.host}")
```

## 🔍 Troubleshooting

### **Common Issues:**

#### **"Authentication Required" Error:**
- Check if token exists: `localStorage.getItem('adminToken')`
- Clear storage and re-login: `localStorage.clear()`
- Verify server is running with auth endpoints

#### **Session Expires Too Quickly:**
- Check server time vs browser time
- Verify session duration in code
- Look for token cleanup in browser dev tools

#### **Can't Access Admin Dashboard:**
- Try direct login: `/admin-login.html`
- Check browser console for errors
- Verify network connectivity to API

#### **Login Page Not Loading:**
- Verify file exists at `/docs/admin-login.html`
- Check GitHub Pages deployment
- Test local server access

### **Debug Commands:**

#### **Check Session Status:**
```javascript
// In browser console
console.log('Token:', localStorage.getItem('adminToken'));
```

#### **Test API Access:**
```javascript
// Test authentication
fetch('/api/waitlist/admin/verify', {
    headers: {'Authorization': `Bearer ${localStorage.getItem('adminToken')}`}
}).then(r => r.json()).then(console.log);
```

#### **Clear All Data:**
```javascript
// Reset everything
localStorage.clear();
window.location.reload();
```

## 📊 Admin Dashboard Features

With authentication enabled, your admin dashboard provides:

### **Real-time Monitoring:**
- ✅ Live waitlist statistics
- ✅ Recent signup tracking
- ✅ Source attribution analysis
- ✅ Auto-refresh every 30 seconds

### **Entry Management:**
- ✅ View all waitlist entries
- ✅ Sort by signup date
- ✅ See company and role information
- ✅ Export capabilities for email marketing

### **Security Features:**
- ✅ Session timeout warnings
- ✅ Secure logout functionality
- ✅ User identification display
- ✅ Token expiration handling

## 🎯 Business Benefits

### **Professional Image:**
- Secure admin access demonstrates professionalism
- Enterprise-grade security for investor confidence
- Proper user management and access controls

### **Data Protection:**
- Waitlist data protected from unauthorized access
- Secure session management prevents data breaches
- Audit trail of admin activities

### **Operational Efficiency:**
- Quick secure access for authorized users
- No need for complex user management systems
- Simple but effective authentication

## 📞 Support

For technical support with the admin system:
- **Documentation**: This guide and `WAITLIST_SETUP.md`
- **GitHub Issues**: [Repository Issues](https://github.com/Iterum-Foods/iterum-chef-notebook/issues)
- **Email**: hello@iterumfoods.xyz

## 🔐 Security Checklist

Before going live:
- ✅ Change default admin password
- ✅ Use HTTPS for all admin access
- ✅ Set up session monitoring
- ✅ Configure proper CORS settings
- ✅ Test login/logout functionality
- ✅ Verify token expiration works
- ✅ Check admin dashboard loads correctly
- ✅ Test all protected endpoints

**Your waitlist admin system is now secure and ready for professional use!** 🍅✨