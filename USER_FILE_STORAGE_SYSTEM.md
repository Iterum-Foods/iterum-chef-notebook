# 💾 User-Specific File Storage System

## Overview

The Recipe Developer now implements a **comprehensive user-specific file storage system** that ensures all user data is stored separately and persistently on their computer, rather than in the browser's localStorage which can be shared across users or lost when browser data is cleared.

## 🎯 Key Benefits

### **User Data Isolation**
- Each user's recipes and ideas are stored in separate files
- No data sharing between different users
- Complete privacy and data separation

### **Persistent Storage**
- Data survives browser restarts and updates
- No risk of losing recipes due to browser data clearing
- Long-term data preservation

### **Professional Workflow**
- Suitable for professional kitchen environments
- Multiple chefs can work on the same system
- Data backup and export capabilities

### **Complete Data Coverage**
- All recipe-related data is stored consistently
- Includes sketches, nutrition, history, and metadata
- Comprehensive data export and backup

## 🗂️ File Structure

```
user_data/
├── user_123/
│   ├── recipe_ideas.json          # User's recipe ideas
│   ├── recipes_in_progress.json   # In-progress recipes
│   ├── sketch_data.json          # Recipe sketches and notes
│   ├── nutrition_data.json       # Nutritional calculations
│   └── recipe_history.json       # Recipe version history
├── user_456/
│   ├── recipe_ideas.json
│   ├── recipes_in_progress.json
│   ├── sketch_data.json
│   ├── nutrition_data.json
│   └── recipe_history.json
└── guest/
    ├── recipe_ideas.json
    ├── recipes_in_progress.json
    ├── sketch_data.json
    ├── nutrition_data.json
    └── recipe_history.json
```

## 🔧 How It Works

### **1. User Authentication**
- System detects when a user logs in or switches
- Automatically creates user-specific data paths
- Loads user's existing data from their files

### **2. Data Storage**
- Recipe ideas saved to `user_[ID]_recipe_ideas.json`
- In-progress recipes saved to `user_[ID]_recipes_in_progress.json`
- Sketch data saved to `user_[ID]_sketch_data.json`
- Nutrition data saved to `user_[ID]_nutrition_data.json`
- Recipe history saved to `user_[ID]_recipe_history.json`

### **3. Data Loading**
- On page load, system attempts to load from user files
- Falls back to localStorage if files not accessible
- Automatically refreshes data when user switches

### **4. User Switching**
- When switching users, old data is cleared
- New user's data is loaded from their files
- Complete data isolation maintained

### **5. Additional Data Types**
- Daily notes saved to `user_[ID]_daily_notes.json`
- Ingredients library saved to `user_[ID]_ingredients.json`
- Vendor data saved to `user_[ID]_vendors.json`
- Menu data saved to `user_[ID]_menus.json`
- Calendar events saved to `user_[ID]_journal_entries.json`, `user_[ID]_recipe_changes.json`, `user_[ID]_maintenance_log.json`
- HACCP data saved to `user_[ID]_haccp_temperature.json`, `user_[ID]_haccp_sanitizer.json`, `user_[ID]_haccp_dishwasher.json`
- Inventory data saved to `user_[ID]_inventory.json`
- Error logs saved to `user_[ID]_errors.json`

## 📁 File Formats

### **Recipe Ideas File** (`recipe_ideas.json`)
```json
[
  {
    "id": "idea_1234567890",
    "title": "Spicy Mango Salsa",
    "description": "Fresh mango with jalapeño and lime",
    "cuisine": "Mexican",
    "difficulty": "easy",
    "status": "idea",
    "createdAt": "2024-01-15T10:30:00.000Z",
    "userId": "user_123",
    "userName": "Chef Maria"
  }
]
```

### **In-Progress Recipes File** (`recipes_in_progress.json`)
```json
[
  {
    "id": "recipe_1234567890",
    "title": "Spicy Mango Salsa",
    "category": "appetizer",
    "cuisine": "Mexican",
    "servings": 4,
    "ingredients": [
      {
        "name": "Mango",
        "amount": "2",
        "unit": "piece",
        "notes": "Ripe but firm"
      }
    ],
    "instructions": [
      "Dice mango into small cubes",
      "Finely chop jalapeño"
    ],
    "status": "in-progress",
    "lastUpdated": "2024-01-15T10:30:00.000Z",
    "userId": "user_123",
    "userName": "Chef Maria",
    "notes": "Sketch notes and additional information",
    "sketchData": {
      "hasSketch": true,
      "labelCount": 3,
      "lastSketchUpdate": "2024-01-15T10:30:00.000Z"
    },
    "nutritionData": {
      "calories": "150",
      "protein": "2g",
      "carbs": "35g",
      "fat": "1g",
      "fiber": "3g",
      "sugar": "30g"
    },
    "metadata": {
      "createdFromIdea": true,
      "totalIngredients": 5,
      "totalInstructions": 4,
      "complexity": 2,
      "estimatedPrepTime": 25,
      "tags": ["appetizer", "mexican", "spicy", "beginner"]
    }
  }
]
```

### **Sketch Data File** (`sketch_data.json`)
```json
{
  "canvasData": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "notes": "Plating idea with mango in center, jalapeño garnish",
  "ingredientLabels": [
    {
      "x": 150,
      "y": 200,
      "ingredient": "Mango",
      "timestamp": "2024-01-15T10:30:00.000Z"
    }
  ],
  "recipeId": "recipe_1234567890",
  "userId": "user_123",
  "userName": "Chef Maria",
  "savedAt": "2024-01-15T10:30:00.000Z"
}
```

### **Nutrition Data File** (`nutrition_data.json`)
```json
{
  "calories": 150,
  "protein": 2,
  "carbs": 35,
  "fat": 1,
  "fiber": 3,
  "sugar": 30,
  "recipeId": "recipe_1234567890",
  "userId": "user_123",
  "userName": "Chef Maria",
  "calculatedAt": "2024-01-15T10:30:00.000Z",
  "ingredients": [
    {
      "name": "Mango",
      "amount": "2",
      "unit": "piece"
    }
  ]
}
```

### **Recipe History File** (`recipe_history.json`)
```json
[
  {
    "recipeId": "recipe_1234567890",
    "title": "Spicy Mango Salsa",
    "action": "saved",
    "timestamp": "2024-01-15T10:30:00.000Z",
    "userId": "user_123",
    "userName": "Chef Maria",
    "version": 1,
    "changes": {
      "ingredients": 5,
      "instructions": 4,
      "hasSketch": true,
      "hasNutrition": true
    }
  }
]
```

## 🚀 Implementation Details

### **File Storage Functions**

#### `initializeUserFileStorage()`
- Sets up user-specific data paths
- Initializes storage for current user
- Called on page load and user switch

#### `saveUserFile(filename, data)`
- Saves data to user-specific file
- Creates backup in localStorage
- Returns success/failure status

#### `loadUserFile(filename)`
- Loads data from user-specific file
- Handles file access errors gracefully
- Falls back to localStorage if needed

### **Data Type Management**

#### **Recipe Data**
- Complete recipe information with metadata
- Automatic complexity calculation
- Prep time estimation
- Smart tag generation

#### **Sketch Data**
- Canvas drawing data
- Ingredient labels
- Sketch notes
- Recipe association

#### **Nutrition Data**
- Calculated nutritional values
- Ingredient-based calculations
- Recipe association
- Timestamp tracking

#### **Recipe History**
- Version tracking
- Change logging
- User activity monitoring
- Automatic cleanup (max 100 versions per recipe)

### **User Event Handling**

#### User Login
```javascript
document.addEventListener('userLoggedIn', function(event) {
    initializeUserFileStorage();
    loadRecipeIdeasFromFiles();
    loadNutritionData();
    updateUserInfo();
});
```

#### User Switch
```javascript
document.addEventListener('userSwitched', function(event) {
    initializeUserFileStorage();
    loadRecipeIdeasFromFiles();
    loadNutritionData();
    clearRecipeForm();
    updateUserInfo();
});
```

#### User Logout
```javascript
document.addEventListener('userLoggedOut', function(event) {
    currentUser = null;
    userDataPath = null;
    clearRecipeForm();
    loadRecipeIdeasFromFiles();
    updateUserInfo();
});
```

## 📤 Export Functionality

### **Individual Recipe Export**
- Export single recipe as JSON file
- Includes all recipe data and metadata
- Filename: `[recipe_name]_recipe.json`

### **Complete User Data Export**
- Export all user's recipes and ideas
- Comprehensive data package with metadata
- Includes sketches, nutrition, and history
- Filename: `[username]_complete_recipe_data_[date].json`

### **Export Data Structure**
```json
{
  "userId": "user_123",
  "userName": "Chef Maria",
  "exportedAt": "2024-01-15T10:30:00.000Z",
  "exportVersion": "2.0",
  "dataTypes": {
    "recipeIdeas": 5,
    "inProgressRecipes": 3,
    "sketchData": 2,
    "nutritionData": 3,
    "recipeHistory": 15
  },
  "recipeIdeas": [...],
  "inProgressRecipes": [...],
  "sketchData": [...],
  "nutritionData": [...],
  "recipeHistory": [...],
  "metadata": {
    "totalDataSize": 15420,
    "userCreatedAt": "2024-01-01T00:00:00.000Z",
    "lastActivity": "2024-01-15T10:30:00.000Z",
    "systemInfo": {
      "userAgent": "Mozilla/5.0...",
      "platform": "Win32",
      "language": "en-US"
    }
  }
}
```

## 🔒 Security & Privacy

### **Data Isolation**
- Each user's data is completely separate
- No cross-user data access
- User authentication required for data operations

### **File Access Control**
- Files stored in user-specific directories
- No shared access between users
- Secure data handling

## 🛠️ Technical Requirements

### **Browser Support**
- Modern browsers with File System Access API support
- Fallback to localStorage for older browsers
- Progressive enhancement approach

### **File System Integration**
- Uses File System Access API when available
- Falls back to localStorage for compatibility
- Automatic data migration between systems

## 📱 User Interface

### **Sidebar Information Display**
- Shows current user's data path
- Displays user name and status
- Real-time updates on user changes

### **History View**
- Toggle between ideas and history
- Recipe version tracking
- Change history visualization
- Modal-based detailed view

### **Export Buttons**
- Individual recipe export
- Complete user data export
- Clear feedback on export success

## 🔄 Data Migration

### **From localStorage**
- Existing data automatically migrated
- No data loss during transition
- Seamless user experience

### **To File System**
- Gradual migration as files are accessed
- Automatic backup creation
- Data integrity maintained

## 🚨 Troubleshooting

### **Common Issues**

#### File Access Denied
- Check browser permissions
- Ensure user is logged in
- Verify file system access

#### Data Not Loading
- Refresh page and try again
- Check user authentication status
- Verify file paths are correct

#### Export Failures
- Ensure recipe is saved first
- Check browser download settings
- Verify sufficient disk space

### **Fallback Behavior**
- System automatically falls back to localStorage
- User notified of fallback mode
- Data integrity maintained

## 🔮 Future Enhancements

### **Planned Features**
- Cloud sync integration
- Automatic backup scheduling
- Data versioning and history
- Collaborative recipe editing
- Advanced export formats (PDF, Word)

### **Integration Possibilities**
- Recipe management software
- Kitchen display systems
- Inventory management
- Cost calculation tools
- Nutritional analysis

## 📚 Usage Examples

### **Creating a New Recipe**
1. User logs in to system
2. System loads their existing recipes
3. User creates new recipe
4. Recipe automatically saved to user file
5. Data persists across sessions

### **Switching Between Users**
1. User A saves their work
2. User B logs in
3. User A's data is cleared from form
4. User B's data is loaded
5. Complete data isolation maintained

### **Exporting User Data**
1. User clicks "Export All Data"
2. System collects all user's recipes and ideas
3. Creates comprehensive JSON package
4. Downloads file to user's computer
5. Data can be imported to other systems

### **Viewing Recipe History**
1. User clicks "History" button in sidebar
2. System displays recipe version history
3. User clicks on specific recipe
4. Detailed history modal appears
5. Shows all versions and changes

## 🎉 Benefits Summary

- **🔒 Complete user data isolation**
- **💾 Persistent storage across sessions**
- **📁 Professional file organization**
- **🔄 Seamless user switching**
- **📤 Easy data export and backup**
- **🛡️ Enhanced data security**
- **📱 Modern browser compatibility**
- **🔄 Automatic fallback systems**
- **📚 Complete recipe history tracking**
- **🎨 Sketch data preservation**
- **📊 Nutrition data storage**
- **🏷️ Smart metadata generation**

This comprehensive system transforms the Recipe Developer from a simple web app into a professional, multi-user recipe management system suitable for commercial kitchens and culinary teams, with complete data coverage and persistent storage.
