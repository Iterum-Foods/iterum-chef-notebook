# 🔄 Backend Signup - Update Needed

## ✅ What You Already Have

Your backend **already has** a working signup system!

### **Existing Endpoint:**
```python
POST /api/auth/register
```

### **Current Accepts:**
- username
- email
- password
- first_name (optional)
- last_name (optional)
- industry (optional)

### **What It Does:**
✅ Creates user account  
✅ Hashes password securely  
✅ Checks for duplicate usernames/emails  
✅ Awards initial 25 XP  
✅ Returns JWT token  
✅ Auto-login after signup  

---

## ⚠️ What Needs Updating

Your **NEW signup flow** captures more data:
- ❌ **craft** (instead of generic "industry")
- ❌ **craftIcon** (emoji for the craft)
- ❌ **interests** (array of learning topics)

These aren't saved yet!

---

## 🔧 How to Fix It

### **Option 1: Update User Model (Recommended)**

Add new fields to capture craft and interests:

**File:** `Skills App/backend/models_usta.py`

```python
class User(db.Model):
    # ... existing fields ...
    
    # Professional Info (UPDATE THIS SECTION)
    primary_industry = db.Column(db.String(50))      # Keep for backward compatibility
    primary_craft = db.Column(db.String(50))         # NEW: Specific craft (Welding, Culinary, etc)
    craft_icon = db.Column(db.String(10))            # NEW: Emoji icon
    learning_interests = db.Column(db.Text)          # NEW: JSON array of interests
    specializations = db.Column(db.Text)             # Existing
```

### **Option 2: Update Auth Route**

Accept new fields in registration:

**File:** `Skills App/backend/routes/auth.py`

```python
@auth.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    
    # Validate input
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user with NEW fields
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        primary_industry=data.get('industry'),           # Old field
        primary_craft=data.get('craft'),                 # NEW
        craft_icon=data.get('craftIcon'),                # NEW
        learning_interests=json.dumps(data.get('interests', [])),  # NEW - store as JSON
        level=UserLevel.NOVICE,
        role=UserRole.USER
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Award first signup XP
    from backend.utils.xp_system import award_xp
    award_xp(user.id, 25, 'account_created')
    
    # Create token
    token = create_token(user.id)
    
    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': user.to_dict()
    }), 201
```

### **Option 3: Update User.to_dict()**

Include new fields in API responses:

```python
def to_dict(self):
    """Convert user to dictionary"""
    import json
    
    return {
        'id': self.id,
        'username': self.username,
        'email': self.email,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'bio': self.bio,
        'avatar_url': self.avatar_url,
        'location': self.location,
        
        # Craft info (NEW)
        'craft': self.primary_craft,
        'craft_icon': self.craft_icon,
        'interests': json.loads(self.learning_interests) if self.learning_interests else [],
        
        # Progression
        'level': self.level.value,
        'total_xp': self.total_xp,
        'current_streak': self.current_streak,
        
        # ... rest of fields ...
    }
```

---

## 📝 Complete Updated Files

Would you like me to:
1. **Update the User model** to add craft & interests fields?
2. **Update the register endpoint** to accept these fields?
3. **Update the to_dict method** to return them?
4. **Create database migration** to add new columns?

---

## 🎯 What This Enables

Once updated, your backend will:

✅ **Save craft selection** → Know user's profession  
✅ **Store learning interests** → Personalize content  
✅ **Enable filtering** → Show relevant challenges  
✅ **Community matching** → Connect users by craft  
✅ **Better recommendations** → Suggest relevant Ustas  

---

## 🔄 Migration Needed

After updating the model, you'll need to:

1. **Delete old database** (development only):
   ```bash
   rm usta.db
   ```

2. **Restart backend** (creates new tables):
   ```bash
   python backend/app_usta.py
   ```

3. **Re-seed data**:
   ```bash
   python backend/seed_data.py
   ```

OR use proper migrations with Flask-Migrate (production):
```bash
flask db migrate -m "Add craft and interests fields"
flask db upgrade
```

---

## 🧪 Testing Updated Signup

### **Frontend sends:**
```javascript
POST /api/auth/register
{
  "username": "mike_welder",
  "email": "mike@example.com",
  "password": "secure123",
  "first_name": "Mike",
  "last_name": "Wilson",
  "craft": "Welding",              // NEW
  "craftIcon": "🔧",                // NEW
  "interests": [                    // NEW
    "Basic Techniques",
    "Safety Practices",
    "Certifications"
  ]
}
```

### **Backend returns:**
```javascript
{
  "message": "User created successfully",
  "token": "eyJ0eXAi...",
  "user": {
    "id": 1,
    "username": "mike_welder",
    "email": "mike@example.com",
    "craft": "Welding",             // NEW
    "craft_icon": "🔧",              // NEW
    "interests": [                   // NEW
      "Basic Techniques",
      "Safety Practices",
      "Certifications"
    ],
    "level": "novice",
    "total_xp": 25,
    ...
  }
}
```

---

## ✅ Summary

**Current State:**
- ✅ Backend signup EXISTS
- ✅ JWT authentication works
- ✅ Password hashing secure
- ✅ Basic validation in place

**What's Missing:**
- ❌ Craft field not saved
- ❌ Craft icon not saved
- ❌ Learning interests not saved

**Next Step:**
Update 3 files to capture the new data!

---

**Want me to make these updates now?** 🔧

