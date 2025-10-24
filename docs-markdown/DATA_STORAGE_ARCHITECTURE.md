# 💾 Complete Data Storage Architecture

## Overview
Your Iterum Chef Notebook uses a **hybrid storage system** - browser localStorage for instant access + backend database for sync and backup.

---

## 📍 **Primary Storage: Browser localStorage**

### **Why localStorage?**
```
✅ Instant access (no network needed)
✅ Works offline
✅ Fast performance
✅ No server costs for storage
✅ Privacy (data on your device)
✅ Easy to manage
```

---

## 🗂️ **Complete Storage Map**

### **1. User & Authentication** 👤
```javascript
// Current user session
localStorage['current_user'] = {
  "userId": "ABC123...",
  "email": "chef@example.com",
  "displayName": "Chef Name",
  "photoURL": "...",
  "emailVerified": true
}

// Session active flag
localStorage['session_active'] = "true"

// Firebase auth tokens (managed by Firebase)
localStorage['firebase:authUser:...'] = {...}
```

### **2. Projects** 📋
```javascript
// All projects (user-specific)
localStorage['iterum_projects_user_ABC123'] = [
  {
    "id": "master",
    "name": "Master Project",
    "description": "All data",
    "type": "master",
    "createdAt": "2025-10-17T..."
  },
  {
    "id": "project_123",
    "name": "Fall Menu 2025",
    "description": "Seasonal menu development",
    "type": "restaurant",
    "color": "#667eea",
    "icon": "🍽️",
    "isPrivate": true,
    "createdBy": "ABC123",
    "createdAt": "2025-10-17T..."
  }
]

// Current selected project (user-specific)
localStorage['iterum_current_project_user_ABC123'] = "project_123"
```

### **3. Recipes** 📚
```javascript
// All recipes (cross-project)
localStorage['recipes'] = [
  {
    "id": "recipe_456",
    "name": "Grilled Salmon",
    "title": "Grilled Salmon",
    "description": "Fresh Atlantic salmon...",
    "category": "Seafood",
    "cuisine": "American",
    "difficulty": "Medium",
    "servings": 4,
    "prepTime": 10,
    "cookTime": 12,
    "totalTime": 22,
    "ingredients": [
      {
        "name": "salmon fillet",
        "amount": "2",
        "unit": "lb",
        "notes": ""
      }
    ],
    "instructions": [
      "Preheat grill...",
      "Season salmon...",
      "Grill for 5-6 minutes..."
    ],
    "tags": ["seafood", "grilled", "quick"],
    "status": "draft",
    "projectId": "project_123",
    "source": "Manual Entry",
    "createdAt": "2025-10-17T...",
    "updatedAt": "2025-10-17T..."
  }
]

// Recipe stubs (from menu builder)
localStorage['recipe_stubs'] = [...]

// Recipe ideas
localStorage['recipe_ideas'] = [
  {
    "title": "Spicy Thai Curry",
    "description": "Coconut milk based...",
    "cuisine": "asian",
    "difficulty": "medium",
    "createdAt": "2025-10-17T..."
  }
]
```

### **4. Menus** 🍽️
```javascript
// Menu data (per project)
localStorage['menu_data_project_123'] = {
  "menu": {
    "id": "menu_789",
    "name": "Fall Menu 2025",
    "description": "Seasonal offerings",
    "version": "1.0",
    "createdAt": "2025-10-17T..."
  },
  "items": [
    {
      "id": "item_001",
      "name": "Grilled Salmon",
      "description": "Fresh Atlantic salmon...",
      "category": "Main Courses",
      "price": 28.00,
      "recipeId": "recipe_456",
      "allergens": ["fish"],
      "dietaryInfo": ["gluten-free"],
      "createdAt": "2025-10-17T..."
    }
  ]
}

// Menu-recipe links
localStorage['menu_recipe_links'] = {
  "item_001": {
    "recipeId": "recipe_456",
    "linkedAt": "2025-10-17T..."
  }
}
```

### **5. Ingredients** 🥬
```javascript
// Main ingredient database
localStorage['ingredients_database'] = [
  {
    "name": "Salmon Fillet",
    "category": "Seafood",
    "unit": "lb",
    "cost": 12.99,
    "vendor": "Fresh Fish Co",
    "nutritionalInfo": {...}
  }
]

// Custom user ingredients
localStorage['custom_ingredients'] = [
  {
    "name": "Chef's Special Spice Mix",
    "category": "Spices",
    "notes": "My secret blend"
  }
]
```

### **6. Vendors** 🏪
```javascript
// All vendors (user-specific if available)
localStorage['iterum_vendors'] = [
  {
    "id": 1,
    "name": "John Smith",
    "company": "Fresh Foods Inc",
    "email": "john@freshfoods.com",
    "phone": "555-1234",
    "city": "Boston",
    "state": "MA",
    "specialties": ["produce", "dairy"],
    "is_active": true,
    "created_at": "2025-10-17T..."
  }
]
```

### **7. Equipment** 🔧
```javascript
// Equipment inventory
localStorage['equipment_list'] = [
  {
    "id": "equip_001",
    "name": "Stand Mixer",
    "category": "Mixers",
    "brand": "KitchenAid",
    "model": "Professional 600",
    "status": "active"
  }
]
```

### **8. Photos** 📸
```javascript
// All photos
localStorage['recipe_photos'] = [
  {
    "id": "photo_123",
    "type": "recipe",
    "recipeId": "recipe_456",
    "filename": "grilled-salmon.jpg",
    "dataUrl": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "mimeType": "image/jpeg",
    "size": 845000,
    "caption": "Final plated dish",
    "isPrimary": true,
    "uploadedAt": "2025-10-17T..."
  },
  {
    "id": "photo_124",
    "type": "step",
    "recipeId": "recipe_456",
    "stepNumber": 3,
    "filename": "grilling-step.jpg",
    "dataUrl": "data:image/jpeg;base64,...",
    "uploadedAt": "2025-10-17T..."
  },
  {
    "id": "photo_125",
    "type": "ingredient",
    "ingredientId": "salmon",
    "filename": "salmon-reference.jpg",
    "dataUrl": "data:image/jpeg;base64,...",
    "uploadedAt": "2025-10-17T..."
  }
]
```

### **9. Daily Notes** 📝
```javascript
// Daily journal entries
localStorage['daily_notes'] = {
  "2025-10-17": "Great day testing new salmon recipe. Customer feedback was excellent!",
  "2025-10-16": "Need to order more thyme from Fresh Foods Inc...",
  "2025-10-15": "Perfected the chocolate ganache technique"
}
```

---

## 🔄 **Secondary Storage: Backend Database**

### **Location:**
```
Database File: culinary_data.db (SQLite)
Server: FastAPI backend
Sync: Automatic when authenticated
```

### **What's in Backend:**

#### **Users Table:**
```sql
users:
- id (primary key)
- email
- firebase_uid
- display_name
- auth_provider
- photo_url
- last_login
- created_at
```

#### **Recipes Table:**
```sql
recipes:
- id
- title
- description
- cuisine_type
- difficulty_level
- prep_time
- cook_time
- servings
- tags (JSON)
- dietary_restrictions (JSON)
- allergens (JSON)
- status (draft/published)
- author_id (foreign key → users)
- created_at
- updated_at
```

#### **Ingredients Table:**
```sql
recipe_ingredients:
- id
- recipe_id (foreign key)
- ingredient_name
- quantity
- unit
- notes
- order_index
```

#### **Instructions Table:**
```sql
recipe_instructions:
- id
- recipe_id (foreign key)
- step_number
- instruction
- created_at
```

#### **Vendors Table:**
```sql
vendors:
- id
- name
- company
- email
- phone
- website
- city
- state
- specialties (JSON)
- is_active
- user_id
- created_at
```

#### **Projects Table:**
```sql
projects:
- id
- name
- description
- restaurant_name
- cuisine_type
- location
- is_default
- is_active
- color_theme
- owner_id (foreign key → users)
- created_at
- updated_at
```

---

## 🔄 **Data Sync Flow**

### **How It Works:**
```
1. User Action (e.g., create recipe)
   ↓
2. Save to localStorage (instant)
   ↓
3. Display updated (immediate)
   ↓
4. Sync to backend API (background)
   ↓
5. Backend saves to database
   ↓
6. Confirmation (optional)

Result: Instant UI + persistent backup
```

### **Example: Creating a Recipe**
```javascript
// Step 1: Save locally
localStorage['recipes'].push(newRecipe);

// Step 2: Display immediately
refreshRecipeList();

// Step 3: Sync to backend (async)
if (authManager.isAuthenticated()) {
  authApiHelper.post('/api/recipes', recipeData)
    .then(response => {
      console.log('✅ Synced to backend');
      newRecipe.backendId = response.id;
    })
    .catch(error => {
      console.warn('⚠️ Sync failed, data safe locally');
    });
}
```

---

## 📊 **Storage Size Estimates**

### **Typical Usage:**
```
Projects (3 projects): ~5 KB
Recipes (50 recipes): ~500 KB
Ingredients (1000 items): ~200 KB
Menus (5 menus): ~50 KB
Vendors (20 vendors): ~20 KB
Photos (20 photos): ~8 MB
Daily Notes (30 days): ~10 KB

Total: ~9 MB

Browser Limit: ~10 MB (localStorage)
Recommended: Keep photos under 20 total
```

### **If You Hit Limits:**
```
Solution 1: Delete old photos
Solution 2: Export and clear old projects
Solution 3: Archive old menus
Solution 4: Use backend-only storage (future)
```

---

## 🔍 **How to View Your Data**

### **Method 1: Browser DevTools**
```
1. Press F12 (open DevTools)
2. Go to "Application" or "Storage" tab
3. Click "Local Storage"
4. Click your domain
5. See all keys and values
```

### **Method 2: Console Commands**
```javascript
// View recipes
console.log(JSON.parse(localStorage.getItem('recipes')));

// View projects
console.log(JSON.parse(localStorage.getItem('iterum_projects_user_' + window.authManager.currentUser.userId)));

// View current project
console.log(localStorage.getItem('iterum_current_project_user_' + window.authManager.currentUser.userId));

// View menu data
console.log(JSON.parse(localStorage.getItem('menu_data_project_123')));

// View photos
console.log(JSON.parse(localStorage.getItem('recipe_photos')));

// View vendors
console.log(JSON.parse(localStorage.getItem('iterum_vendors')));

// View ingredients
console.log(JSON.parse(localStorage.getItem('ingredients_database')));

// View storage usage
console.log(window.photoManager.getStorageInfo());
```

### **Method 3: Export Data**
```javascript
// Export everything
const allData = {};
for (let i = 0; i < localStorage.length; i++) {
  const key = localStorage.key(i);
  allData[key] = localStorage.getItem(key);
}
console.log(JSON.stringify(allData, null, 2));

// Or download as file
const blob = new Blob([JSON.stringify(allData, null, 2)], {type: 'application/json'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'iterum-backup-' + new Date().toISOString() + '.json';
a.click();
```

---

## 🔑 **Storage Keys Reference**

### **User-Specific Keys:**
```
iterum_projects_user_{userId}
iterum_current_project_user_{userId}
user_{userId}_vendors.json
user_{userId}_equipment.json
user_{userId}_daily_notes.json
```

### **Global Keys:**
```
recipes
recipe_ideas
recipe_stubs
recipe_photos
ingredients_database
custom_ingredients
iterum_vendors
equipment_list
menu_data_{projectId}
menu_recipe_links
daily_notes
current_user
session_active
```

---

## 🔒 **Data Privacy**

### **What's Private:**
```
✅ Each user's projects (separate storage keys)
✅ User-specific settings
✅ Private projects (marked isPrivate: true)
✅ Authentication tokens (secure)
```

### **What's Shared:**
```
⚠️ Ingredient database (shared reference)
⚠️ Equipment catalog (if using shared)
⚠️ Master project (your default workspace)
```

---

## 💾 **Backup Strategies**

### **Manual Backup:**
```javascript
// 1. Export all localStorage
function backupAllData() {
  const backup = {};
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key.startsWith('iterum_') || 
        key === 'recipes' || 
        key === 'ingredients_database' ||
        key === 'recipe_photos') {
      backup[key] = localStorage.getItem(key);
    }
  }
  
  const blob = new Blob([JSON.stringify(backup, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `iterum-backup-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// Run in console to backup
backupAllData();
```

### **Restore from Backup:**
```javascript
// Upload backup file
function restoreFromBackup(file) {
  const reader = new FileReader();
  reader.onload = function(e) {
    const data = JSON.parse(e.target.result);
    for (const [key, value] of Object.entries(data)) {
      localStorage.setItem(key, value);
    }
    alert('✅ Data restored! Refresh page.');
    location.reload();
  };
  reader.readAsText(file);
}

// Usage:
// 1. Create file input: <input type="file" onchange="restoreFromBackup(this.files[0])">
// 2. Select your backup JSON file
// 3. All data restored
```

### **Automatic Backend Sync:**
```
When authenticated:
✅ Recipes → /api/recipes
✅ Projects → /api/projects
✅ Vendors → /api/vendors
✅ Equipment → /api/equipment

Sync is automatic when:
- Creating new items
- Updating existing items
- Deleting items

Offline mode:
- Data saved locally
- Syncs when back online
```

---

## 📍 **Backend Database Location**

### **Database File:**
```
Path: c:\Users\chefm\my-culinary-app\Iterum App\culinary_data.db
Type: SQLite database
Size: Grows with use

Tables:
- users
- recipes
- recipe_ingredients
- recipe_instructions
- recipe_versions
- recipe_uploads
- projects
- menus
- menu_items
- vendors
- equipment
- project_equipment
```

### **Access Backend Data:**
```
Via API endpoints:
GET  /api/recipes        - Get all your recipes
GET  /api/recipes/{id}   - Get specific recipe
POST /api/recipes        - Create recipe
PUT  /api/recipes/{id}   - Update recipe

GET  /api/projects       - Get your projects
POST /api/projects       - Create project

GET  /api/vendors        - Get vendors
POST /api/vendors        - Create vendor

And more...
```

---

## 🔄 **Data Migration Between Storage**

### **localStorage → Backend:**
```javascript
// Sync all local recipes to backend
async function syncAllRecipesToBackend() {
  const recipes = JSON.parse(localStorage.getItem('recipes') || '[]');
  
  for (const recipe of recipes) {
    if (!recipe.backendId) {
      try {
        const response = await window.authApiHelper.post('/api/recipes', {
          title: recipe.title,
          description: recipe.description,
          // ... other fields
        });
        
        recipe.backendId = response.id;
        console.log('✅ Synced:', recipe.title);
      } catch (error) {
        console.error('❌ Sync failed:', recipe.title, error);
      }
    }
  }
  
  // Update localStorage with backend IDs
  localStorage.setItem('recipes', JSON.stringify(recipes));
}
```

### **Backend → localStorage:**
```javascript
// Pull all recipes from backend
async function pullRecipesFromBackend() {
  try {
    const response = await window.authApiHelper.get('/api/recipes');
    const backendRecipes = response.recipes || [];
    
    // Merge with local (prefer backend)
    const localRecipes = JSON.parse(localStorage.getItem('recipes') || '[]');
    const merged = [...backendRecipes];
    
    // Add local-only recipes
    localRecipes.forEach(local => {
      if (!local.backendId && !merged.some(r => r.id === local.id)) {
        merged.push(local);
      }
    });
    
    localStorage.setItem('recipes', JSON.stringify(merged));
    console.log('✅ Synced from backend:', merged.length, 'recipes');
  } catch (error) {
    console.error('❌ Pull failed:', error);
  }
}
```

---

## 🛡️ **Data Safety**

### **Your Data is Safe:**
```
✅ localStorage = On your device (not server)
✅ Backend = Encrypted database
✅ Authentication = Firebase (Google-grade security)
✅ HTTPS = All traffic encrypted
✅ No third-party access
✅ You control everything
```

### **Data Persistence:**
```
✅ localStorage: Until you clear browser data
✅ Backend: Permanent (unless you delete)
✅ Photos: Compressed and efficient
✅ Projects: User-specific (privacy)
```

### **What Happens If:**

#### **Clear Browser Cache:**
```
→ localStorage cleared
→ Backend data intact
→ Re-login and pull from backend
→ Most data restored
→ Photos may be lost (not in backend yet)
```

#### **Change Devices:**
```
→ Sign in on new device
→ Backend syncs your recipes
→ Projects sync
→ Vendors sync
→ Ready to work!
```

#### **Offline Work:**
```
→ Everything saved locally
→ Works without internet
→ Syncs when back online
→ No data loss
```

---

## 📦 **Storage Best Practices**

### **Recommendations:**
```
1. ✅ Keep photos under 20 total (or ~8MB)
2. ✅ Archive old projects regularly
3. ✅ Export backup monthly
4. ✅ Delete unused vendors/equipment
5. ✅ Clear old daily notes (>60 days)
```

### **Cleanup Commands:**
```javascript
// Clear old photos
function clearOldPhotos(daysOld = 90) {
  const photos = JSON.parse(localStorage.getItem('recipe_photos') || '[]');
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - daysOld);
  
  const filtered = photos.filter(p => new Date(p.uploadedAt) > cutoff);
  localStorage.setItem('recipe_photos', JSON.stringify(filtered));
  
  console.log(`🗑️ Cleared ${photos.length - filtered.length} old photos`);
}

// Clear old daily notes
function clearOldNotes(daysOld = 60) {
  const notes = JSON.parse(localStorage.getItem('daily_notes') || '{}');
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - daysOld);
  
  const filtered = {};
  for (const [date, note] of Object.entries(notes)) {
    if (new Date(date) > cutoff) {
      filtered[date] = note;
    }
  }
  
  localStorage.setItem('daily_notes', JSON.stringify(filtered));
  console.log(`🗑️ Cleared ${Object.keys(notes).length - Object.keys(filtered).length} old notes`);
}
```

---

## 📍 **Quick Reference**

### **Essential Commands:**
```javascript
// View all storage keys
Object.keys(localStorage)

// View specific data
JSON.parse(localStorage.getItem('recipes'))
JSON.parse(localStorage.getItem('iterum_projects_user_' + window.authManager.currentUser.userId))

// Export backup
backupAllData() // See code above

// Check storage size
console.log(window.photoManager.getStorageInfo())

// Clear specific data
localStorage.removeItem('recipe_photos')

// Clear all Iterum data
Object.keys(localStorage).forEach(key => {
  if (key.startsWith('iterum_') || key === 'recipes') {
    localStorage.removeItem(key);
  }
});
```

---

## 🎯 **Summary**

### **Your Data Lives In:**
```
1️⃣ Browser localStorage (primary)
   - Instant access
   - Works offline
   - ~9 MB typical usage

2️⃣ Backend database (backup/sync)
   - culinary_data.db
   - Permanent storage
   - Accessible via API

3️⃣ Firebase (authentication only)
   - User accounts
   - Login sessions
   - Security tokens
```

### **Access Points:**
```
Local: Browser DevTools → Application → Local Storage
Backend: Database file or API endpoints
Export: Backup JSON files
```

---

## ✅ **You're All Set!**

**Your data is:**
- ✅ Safe on your device
- ✅ Backed up to server (when online)
- ✅ User-specific and private
- ✅ Easy to export/backup
- ✅ Accessible across devices (via sync)

**Need to backup?** Run `backupAllData()` in console!  
**Need to view data?** Check DevTools → Application → Local Storage!  
**Need to sync?** Just sign in - automatic!

