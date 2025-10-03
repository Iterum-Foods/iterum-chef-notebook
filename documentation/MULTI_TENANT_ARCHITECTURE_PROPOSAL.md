# 🏢 Multi-Tenant Architecture Proposal
## Iterum R&D Chef Notebook - Organization & Restaurant Management

---

## 🎯 **Business Model Requirements**

### **Current Challenge:**
- You sell software to organizations
- Organizations need to create large shared archives 
- Multiple restaurants within each organization need individual profiles
- Each restaurant needs specific menus and recipes organized together
- Need data isolation and proper access control

### **Proposed Solution:**
**3-Tier Hierarchical System**: `Organization → Restaurant → User`

---

## 🏗️ **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    ORGANIZATION                             │
│  (The Purchaser - e.g., "Sunset Restaurant Group")        │
│                                                             │
│  📚 SHARED RESOURCES (Organization-wide):                  │
│  • Master Recipe Archive                                   │
│  • Ingredient Database                                     │
│  • Equipment Inventory                                     │
│  • Vendor Relationships                                    │
│  • Corporate Standards                                     │
│                                                             │
│  ┌─────────────────┬─────────────────┬─────────────────┐   │
│  │   RESTAURANT A  │   RESTAURANT B  │   RESTAURANT C  │   │
│  │   "Downtown"    │   "Westside"    │   "Airport"     │   │
│  │                 │                 │                 │   │
│  │  🍽️ SPECIFIC:   │  🍽️ SPECIFIC:   │  🍽️ SPECIFIC:   │   │
│  │  • Custom Menu  │  • Custom Menu  │  • Custom Menu  │   │
│  │  • Local Recipes│  • Local Recipes│  • Local Recipes│   │
│  │  • Staff Prefs  │  • Staff Prefs  │  • Staff Prefs  │   │
│  │  • Inventory    │  • Inventory    │  • Inventory    │   │
│  │                 │                 │                 │   │
│  │  👥 USERS:      │  👥 USERS:      │  👥 USERS:      │   │
│  │  • Head Chef    │  • Head Chef    │  • Head Chef    │   │
│  │  • Sous Chef    │  • Sous Chef    │  • Sous Chef    │   │
│  │  • Kitchen Staff│  • Kitchen Staff│  • Kitchen Staff│   │
│  └─────────────────┴─────────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ **Database Schema Changes**

### **New Tables:**

#### **1. Organizations**
```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    license_key VARCHAR(255) UNIQUE NOT NULL,
    subscription_type ENUM('basic', 'professional', 'enterprise'),
    max_restaurants INTEGER DEFAULT 5,
    max_users INTEGER DEFAULT 50,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    
    -- Billing & Contact
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    billing_address TEXT,
    
    -- Settings
    settings JSONB DEFAULT '{}',
    features JSONB DEFAULT '{}'
);
```

#### **2. Restaurants** 
```sql
CREATE TABLE restaurants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    
    -- Restaurant Details
    cuisine_type VARCHAR(100),
    location VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    
    -- Operational Settings
    seating_capacity INTEGER,
    operating_hours JSONB,
    menu_style ENUM('fine_dining', 'casual', 'fast_casual', 'quick_service'),
    
    -- System Settings
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(organization_id, slug)
);
```

#### **3. Updated Users Table**
```sql
ALTER TABLE users ADD COLUMN organization_id UUID REFERENCES organizations(id);
ALTER TABLE users ADD COLUMN restaurant_id UUID REFERENCES restaurants(id);
ALTER TABLE users ADD COLUMN role ENUM('org_admin', 'restaurant_manager', 'head_chef', 'sous_chef', 'line_cook', 'staff') DEFAULT 'staff';
ALTER TABLE users ADD COLUMN permissions JSONB DEFAULT '{}';
```

#### **4. Resource Scope Management**
```sql
-- Add scope columns to existing tables
ALTER TABLE recipes ADD COLUMN organization_id UUID REFERENCES organizations(id);
ALTER TABLE recipes ADD COLUMN restaurant_id UUID REFERENCES restaurants(id);
ALTER TABLE recipes ADD COLUMN scope ENUM('organization', 'restaurant', 'private') DEFAULT 'private';

ALTER TABLE ingredients ADD COLUMN organization_id UUID REFERENCES organizations(id);
ALTER TABLE ingredients ADD COLUMN restaurant_id UUID REFERENCES restaurants(id);
ALTER TABLE ingredients ADD COLUMN scope ENUM('organization', 'restaurant', 'private') DEFAULT 'private';

-- Similar for equipment, vendors, etc.
```

---

## 🔐 **Authentication & Access Control**

### **Login Flow:**
```
1. User enters: organization_slug + username + password
   Example: "sunset-group/john.doe" + password
   
2. System validates organization exists and is active
3. System authenticates user within that organization
4. User selects which restaurant to work with (if multiple access)
5. System sets context: organization + restaurant + user
```

### **Permission Levels:**

| Role | Organization Access | Restaurant Access | Can Switch Restaurants |
|------|-------------------|------------------|----------------------|
| **org_admin** | Full management | All restaurants | Yes |
| **restaurant_manager** | View shared resources | Full restaurant management | Limited |
| **head_chef** | View shared resources | Full kitchen operations | No |
| **sous_chef** | View shared resources | Limited kitchen operations | No |
| **line_cook** | View shared resources | Recipe execution only | No |

### **Resource Access Rules:**
- **Organization Scope**: Accessible by all users in the organization
- **Restaurant Scope**: Accessible only by users assigned to that restaurant
- **Private Scope**: Accessible only by the creator

---

## 🔄 **Data Flow & API Changes**

### **New API Endpoints:**

#### **Organization Management:**
```
GET    /api/organizations/{org_id}                    # Get organization details
PUT    /api/organizations/{org_id}                    # Update organization
GET    /api/organizations/{org_id}/restaurants        # List restaurants
POST   /api/organizations/{org_id}/restaurants        # Create restaurant
GET    /api/organizations/{org_id}/users              # List organization users
```

#### **Restaurant Management:**
```
GET    /api/restaurants/{restaurant_id}               # Get restaurant details
PUT    /api/restaurants/{restaurant_id}               # Update restaurant
GET    /api/restaurants/{restaurant_id}/users         # List restaurant users
POST   /api/restaurants/{restaurant_id}/users         # Add user to restaurant
GET    /api/restaurants/{restaurant_id}/menu          # Get restaurant menu
```

#### **Enhanced Resource APIs:**
```
GET    /api/recipes?scope=organization                # Get organization recipes
GET    /api/recipes?scope=restaurant&restaurant_id=X  # Get restaurant recipes
GET    /api/recipes?scope=all                         # Get all accessible recipes
POST   /api/recipes                                   # Create recipe (auto-scoped)
```

### **Authentication Headers:**
```javascript
// Every API request includes:
{
  "Authorization": "Bearer <jwt_token>",
  "X-Organization-ID": "uuid",
  "X-Restaurant-ID": "uuid"  // Optional, for restaurant-specific operations
}
```

---

## 🎨 **UI/UX Changes**

### **1. Enhanced Login Screen:**
```html
<!-- Organization-aware login -->
<input placeholder="Organization (e.g., sunset-group)" name="organization" />
<input placeholder="Username" name="username" />
<input placeholder="Password" name="password" type="password" />
```

### **2. Organization/Restaurant Switcher:**
```html
<!-- Header includes organization and restaurant selector -->
<div class="org-context">
  <select id="org-selector">
    <option value="sunset-group">Sunset Restaurant Group</option>
  </select>
  <select id="restaurant-selector">
    <option value="">All Restaurants</option>
    <option value="downtown">Downtown Location</option>
    <option value="westside">Westside Location</option>
    <option value="airport">Airport Location</option>
  </select>
</div>
```

### **3. Resource Scope Indicators:**
```html
<!-- Visual indicators for resource scope -->
<div class="recipe-card">
  <span class="scope-badge scope-organization">🏢 Shared</span>
  <span class="scope-badge scope-restaurant">🍽️ Restaurant</span>
  <span class="scope-badge scope-private">👤 Private</span>
</div>
```

### **4. Enhanced Navigation:**
```html
<!-- Context-aware navigation -->
<nav>
  <a href="/dashboard">Dashboard</a>
  <a href="/recipes?scope=organization">Shared Recipes</a>
  <a href="/recipes?scope=restaurant">Restaurant Recipes</a>
  <a href="/recipes?scope=private">My Recipes</a>
  <a href="/menu-builder">Menu Builder</a>
</nav>
```

---

## 🚀 **Implementation Plan**

### **Phase 1: Database Migration (Week 1)**
1. Create organization and restaurant tables
2. Add scope columns to existing tables
3. Create migration scripts for existing data
4. Update database models

### **Phase 2: Authentication Overhaul (Week 2)**
1. Implement organization-aware authentication
2. Add JWT claims for organization/restaurant context
3. Update permission checking middleware
4. Create organization/restaurant management APIs

### **Phase 3: API Enhancement (Week 3)**
1. Update all resource APIs to support scoping
2. Add organization and restaurant management endpoints
3. Implement resource access control
4. Add data migration tools

### **Phase 4: Frontend Updates (Week 4)**
1. Update login interface
2. Add organization/restaurant switchers
3. Update resource displays with scope indicators
4. Add organization and restaurant management interfaces

### **Phase 5: Testing & Migration (Week 5)**
1. Comprehensive testing of multi-tenant features
2. Data migration from current system
3. User acceptance testing
4. Documentation and training materials

---

## 💰 **Business Benefits**

### **For You (Iterum):**
- **Higher Revenue**: Sell organization licenses vs individual users
- **Better Retention**: Organizations less likely to churn than individuals
- **Scalable Pricing**: Charge based on restaurants/users/features
- **Enterprise Sales**: Bigger deals with restaurant groups

### **For Customers (Organizations):**
- **Centralized Management**: One system for all locations
- **Shared Knowledge**: Organization-wide recipe and ingredient database
- **Cost Effective**: One license for multiple restaurants
- **Standardization**: Consistent processes across locations
- **Flexibility**: Restaurant-specific customization when needed

---

## 🔧 **Migration Strategy**

### **Existing Users:**
1. **Auto-create organizations** for existing users
2. **Set them as org_admin** with full access
3. **Convert their data** to organization-scoped resources
4. **Provide upgrade path** to add more restaurants

### **Data Migration:**
```python
def migrate_existing_users():
    for user in existing_users:
        # Create organization for each user
        org = Organization.create(
            name=f"{user.name}'s Organization",
            slug=generate_slug(user.name),
            license_key=generate_license()
        )
        
        # Create default restaurant
        restaurant = Restaurant.create(
            organization_id=org.id,
            name=user.restaurant or "Main Kitchen",
            slug="main"
        )
        
        # Update user
        user.update(
            organization_id=org.id,
            restaurant_id=restaurant.id,
            role='org_admin'
        )
        
        # Migrate user's data to organization scope
        migrate_user_resources(user, org, restaurant)
```

---

## 📊 **Success Metrics**

- **Customer Satisfaction**: Organization admins can manage multiple restaurants
- **Data Isolation**: Proper separation between organizations
- **Performance**: System handles multiple organizations efficiently
- **Scalability**: Easy to add new restaurants and users
- **Revenue Growth**: Higher value sales to restaurant groups

This architecture positions Iterum as an **enterprise-ready solution** for restaurant groups while maintaining the simplicity that individual users love! 