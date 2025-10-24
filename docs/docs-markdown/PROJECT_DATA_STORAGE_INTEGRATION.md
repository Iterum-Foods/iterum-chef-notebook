# 🏗️ Project Management Data Storage Integration

## Overview

The Iterum App implements a **hierarchical data storage system** that combines **user-specific file storage** with **project-based organization**. This allows users to organize their culinary work into separate projects (restaurants, catering events, etc.) while maintaining complete data isolation between users.

## 🎯 **How It Works**

### **1. Dual-Layer Storage Architecture**

```
User Layer (user_123_)
├── Project-Aware Files
│   ├── user_123_project_456_menus.json     # Restaurant A menus
│   ├── user_123_project_789_menus.json     # Restaurant B menus
│   ├── user_123_master_menus.json          # Global menus (Full Library)
│   └── user_123_no_project_menus.json     # Fallback storage
└── Global User Files
    ├── user_123_recipe_ideas.json          # Shared across all projects
    ├── user_123_ingredients.json           # Shared ingredient library
    └── user_123_daily_notes.json          # User-wide notes
```

### **2. Project Storage Key Generation**

The system automatically generates storage keys based on the current project context:

```javascript
// For specific projects
window.projectManager.getProjectStorageKey('menus')
// Returns: "data_menus_project_456"

// For master project (Full Library)
window.projectManager.getProjectStorageKey('menus')
// Returns: "data_menus_master"

// For no project context
window.projectManager.getProjectStorageKey('menus')
// Returns: "data_menus_no_project"
```

### **3. Project File Path Generation**

For user-specific file storage, the system generates project-aware filenames:

```javascript
// For specific projects
window.projectManager.getProjectFilePath('menus')
// Returns: "project_456_menus.json"

// For master project (Full Library)
window.projectManager.getProjectFilePath('menus')
// Returns: "master_menus.json"

// For no project context
window.projectManager.getProjectFilePath('menus')
// Returns: "no_project_menus.json"
```

## 🔧 **Implementation Details**

### **Project Management System Methods**

```javascript
class ProjectManagementSystem {
    /**
     * Generate project-specific localStorage key
     */
    getProjectStorageKey(dataType) {
        if (!this.currentProject) {
            return `data_${dataType}_no_project`;
        }
        
        // For master project, use global storage
        if (this.currentProject.id === this.masterProjectId) {
            return `data_${dataType}_master`;
        }
        
        // For specific projects, include project ID in key
        return `data_${dataType}_project_${this.currentProject.id}`;
    }

    /**
     * Generate project-specific file path
     */
    getProjectFilePath(dataType) {
        if (!this.currentProject) {
            return `no_project_${dataType}.json`;
        }
        
        // For master project, use global storage
        if (this.currentProject.id === this.masterProjectId) {
            return `master_${dataType}.json`;
        }
        
        // For specific projects, include project ID in filename
        return `project_${this.currentProject.id}_${dataType}.json`;
    }
}
```

### **Data Manager Integration**

Each data manager (MenuManager, VendorManager, etc.) uses the project system:

```javascript
class MenuManager {
    loadMenusFromStorage() {
        if (!this.currentProject) return;

        // Try to load from user-specific file storage first
        if (window.userDataManager && window.userDataManager.isUserLoggedIn()) {
            const userId = window.userDataManager.getCurrentUserId();
            
            // Use project-aware filename
            let filename;
            if (window.projectManager) {
                filename = `user_${userId}_${window.projectManager.getProjectFilePath('menus')}`;
            } else {
                filename = `user_${userId}_menus.json`;
            }
            
            const loadedMenus = window.userDataManager.loadUserFile(filename);
            if (loadedMenus && Array.isArray(loadedMenus)) {
                this.menus = loadedMenus;
                return;
            }
        }

        // Fallback to project-based localStorage
        const key = window.projectManager ? 
            window.projectManager.getProjectStorageKey('menus') : 
            `menus_${this.getCurrentUser()?.id || 'anonymous'}`;

        const stored = localStorage.getItem(key);
        this.menus = stored ? JSON.parse(stored) : [];
    }
}
```

## 📁 **Data Type Organization**

### **Project-Specific Data** (Stored per project)
- **Menus**: Each project has its own menu collection
- **Equipment Assignments**: Project-specific equipment with quantities/locations
- **Project Recipes**: Recipes created specifically for a project
- **Project Notes**: Project-specific operational notes

### **User-Global Data** (Shared across all projects)
- **Recipe Ideas**: Available to all projects
- **Ingredients Library**: Shared ingredient database
- **Daily Notes**: User-wide operational notes
- **Vendor Information**: Shared vendor contacts
- **Recipe History**: Complete recipe version tracking

### **Master Project Data** (Full Library)
- **All Recipes**: Complete recipe collection
- **All Menus**: Historical menu templates
- **All Equipment**: Complete equipment catalog
- **All Notes**: Comprehensive operational history

## 🔄 **Data Flow Examples**

### **Example 1: Creating a Menu in Restaurant A**

1. **User selects "Restaurant A" project**
2. **System generates storage key**: `data_menus_project_456`
3. **System generates file path**: `project_456_menus.json`
4. **Menu saved to**: `user_123_project_456_menus.json`
5. **Menu only visible in Restaurant A project**

### **Example 2: Accessing Full Library**

1. **User selects "Full Library" project**
2. **System generates storage key**: `data_menus_master`
3. **System generates file path**: `master_menus.json`
4. **System loads from**: `user_123_master_menus.json`
5. **All menus visible across all projects**

### **Example 3: Switching Between Projects**

1. **User in Restaurant A**: Sees only Restaurant A menus
2. **User switches to Restaurant B**: Sees only Restaurant B menus
3. **User switches to Full Library**: Sees all menus
4. **Data isolation maintained**: No cross-contamination

## 🎨 **User Interface Integration**

### **Project Selector Display**
- **Header Dropdown**: Shows current project with statistics
- **Mobile Menu**: Project selection in mobile navigation
- **Project Stats**: Recipe count, menu count, equipment count
- **Color Coding**: Visual project differentiation

### **Data Context Indicators**
- **Page Headers**: Show current project context
- **Data Counters**: Display project-specific statistics
- **Navigation**: Project-aware breadcrumbs
- **Actions**: Project-specific create/edit buttons

## 🔒 **Security & Data Isolation**

### **User Isolation**
- Each user has completely separate data
- No cross-user data access
- User authentication required

### **Project Isolation**
- Project data separated by project ID
- No cross-project data leakage
- Project-specific permissions (future enhancement)

### **Storage Security**
- Files stored in user-specific directories
- Project context embedded in filenames
- Fallback to localStorage for compatibility

## 🚀 **Benefits of This Integration**

### **Professional Organization**
- **Restaurant Management**: Separate data for each venue
- **Catering Events**: Isolated project data
- **Menu Development**: Project-specific menu versions
- **Equipment Tracking**: Location-specific assignments

### **Data Efficiency**
- **Selective Loading**: Only load relevant project data
- **Memory Management**: Reduce memory usage
- **Performance**: Faster data access for current project
- **Scalability**: Handle unlimited projects per user

### **Workflow Support**
- **Multi-Project Work**: Work on multiple restaurants simultaneously
- **Data Sharing**: Share recipes across projects
- **Project Switching**: Seamless context changes
- **Backup & Export**: Project-specific data packages

## 🔮 **Future Enhancements**

### **Advanced Project Features**
- **Project Templates**: Pre-configured project setups
- **Project Sharing**: Collaborative project access
- **Project Archiving**: Long-term project storage
- **Project Analytics**: Project performance metrics

### **Enhanced Data Management**
- **Cross-Project Recipes**: Recipe sharing between projects
- **Project Data Migration**: Move data between projects
- **Project Backup**: Automated project data backup
- **Project Sync**: Cloud synchronization per project

## 📚 **Usage Examples**

### **Setting Up Multiple Restaurants**

1. **Create Restaurant A Project**
   - Name: "Downtown Bistro"
   - Cuisine: "French"
   - Color: Blue theme

2. **Create Restaurant B Project**
   - Name: "Uptown Grill"
   - Cuisine: "American"
   - Color: Green theme

3. **Work Independently**
   - Each restaurant has separate menus
   - Equipment tracked per location
   - Notes specific to each venue

### **Managing Catering Events**

1. **Create Event Project**
   - Name: "Summer Wedding 2024"
   - Type: "Catering Event"
   - Date: "2024-06-15"

2. **Event-Specific Data**
   - Custom menu for the event
   - Equipment needed for outdoor service
   - Special dietary requirements
   - Timeline and logistics notes

### **Full Library Access**

1. **Select Full Library Project**
   - Access all recipes and menus
   - View complete equipment catalog
   - See all operational notes
   - Export comprehensive data

## 🎉 **Summary**

The project management integration provides:

- **🔒 Complete data isolation** between users and projects
- **📁 Professional organization** for multiple venues/events
- **🔄 Seamless project switching** with context awareness
- **💾 Efficient storage** with project-specific data loading
- **📊 Clear data context** with visual project indicators
- **🛡️ Secure data handling** with user and project boundaries

This system transforms the Iterum App from a simple recipe manager into a **professional multi-project culinary management platform** suitable for restaurant groups, catering companies, and culinary teams working across multiple venues and events.
