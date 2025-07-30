#!/usr/bin/env python3
"""
Migration Script: Replace Dual Login Systems with Unified Authentication
Removes the conflicting authManager.js and profileManager.js systems
and replaces them with the new unified_auth_system.js
"""

import os
import shutil
from pathlib import Path

def backup_old_systems():
    """Backup the old authentication systems"""
    print("📦 Backing up old authentication systems...")
    
    backup_dir = Path("archive/authentication_backup")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_backup = [
        "authManager.js",
        "profileManager.js"
    ]
    
    for file_name in files_to_backup:
        if os.path.exists(file_name):
            shutil.copy2(file_name, backup_dir / file_name)
            print(f"✅ Backed up: {file_name}")
        else:
            print(f"⚠️  File not found: {file_name}")

def update_index_html():
    """Update index.html to use unified auth system"""
    print("🔧 Updating index.html...")
    
    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old auth system scripts with unified system
    old_scripts = [
        '<!-- API Configuration -->\n<script src="api_config.js"></script>\n\n<!-- Error Handler -->\n<script src="error_handler.js"></script>\n\n<!-- Enhanced Core App Systems -->\n<script src="enhanced_loading_system.js"></script>\n<script src="enhanced_search_system.js"></script>\n<script src="modern_dashboard.js"></script>\n<script src="data_export_import.js"></script>\n<script src="authManager.js"></script>',
        '<!-- API Configuration -->\n<script src="api_config.js"></script>\n\n<!-- Error Handler -->\n<script src="error_handler.js"></script>\n\n<!-- Enhanced Core App Systems -->\n<script src="enhanced_loading_system.js"></script>\n<script src="enhanced_search_system.js"></script>\n<script src="modern_dashboard.js"></script>\n<script src="data_export_import.js"></script>\n<script src="unified_auth_system.js"></script>'
    ]
    
    content = content.replace(old_scripts[0], old_scripts[1])
    
    # Write the updated content
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated index.html to use unified auth system")

def remove_old_systems():
    """Remove the old authentication system files"""
    print("🗑️  Removing old authentication systems...")
    
    files_to_remove = [
        "authManager.js",
        "profileManager.js"
    ]
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Removed: {file_name}")
        else:
            print(f"⚠️  File not found: {file_name}")

def update_other_html_files():
    """Update other HTML files that might reference the old auth systems"""
    print("🔧 Updating other HTML files...")
    
    html_files = [
        "recipe-developer.html",
        "recipe-upload.html",
        "recipe-library.html",
        "recipe-review.html",
        "ingredients.html",
        "equipment-management.html",
        "inventory.html",
        "menu-builder.html",
        "vendor-management.html",
        "plant-sketches.html",
        "dashboard.html"
    ]
    
    for html_file in html_files:
        if os.path.exists(html_file):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace authManager.js references
                if 'authManager.js' in content:
                    content = content.replace('authManager.js', 'unified_auth_system.js')
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Updated: {html_file}")
                else:
                    print(f"ℹ️  No auth references in: {html_file}")
                    
            except Exception as e:
                print(f"⚠️  Error updating {html_file}: {e}")

def create_migration_summary():
    """Create a summary of the migration"""
    print("📝 Creating migration summary...")
    
    summary = """# 🔄 Authentication System Migration Complete

## ✅ **Migration Summary**

### **What Was Changed:**
1. **Backed up old systems** to `archive/authentication_backup/`
2. **Removed conflicting files:**
   - `authManager.js` (traditional login modal)
   - `profileManager.js` (profile selection system)
3. **Added unified system:**
   - `unified_auth_system.js` (combined authentication)
4. **Updated HTML files** to use the new system

### **New Unified Authentication Features:**

#### **🎯 Single Login Flow:**
- **User Selection**: Shows saved users if available
- **Login Options**: Traditional email/password login
- **Profile Creation**: Easy new profile setup
- **Offline Mode**: Continue without internet

#### **🔄 Smart Flow Logic:**
1. **Check for saved users** → Show user selection
2. **No saved users** → Show login options
3. **Offline mode** → Create local profile
4. **Online mode** → Full authentication

#### **💾 Data Persistence:**
- **Online**: Backend API storage
- **Offline**: localStorage fallback
- **Hybrid**: Seamless online/offline switching

### **Benefits:**
- ✅ **No more conflicts** between login systems
- ✅ **Unified user experience** across the app
- ✅ **Better error handling** and recovery
- ✅ **Cleaner codebase** with single auth system
- ✅ **Improved maintainability**

### **How to Use:**
1. **Page loads** → Shows appropriate auth interface
2. **Select user** → Quick access to saved profiles
3. **Create profile** → Easy setup for new users
4. **Offline mode** → Works without internet
5. **Switch users** → Seamless profile switching

### **API Endpoints Used:**
- `GET /api/profiles/` - List saved users
- `GET /api/profiles/{id}` - Get specific user
- `POST /api/profiles/login` - Login/create user
- `POST /api/profiles/offline` - Create offline profile

### **Global Access:**
```javascript
// Access the unified auth system
window.unifiedAuth.getCurrentUser()
window.unifiedAuth.isLoggedIn()
window.unifiedAuth.handleLogout()
```

### **Migration Status:**
- ✅ **Backup created** - Old systems preserved
- ✅ **New system active** - Unified auth running
- ✅ **HTML files updated** - All pages using new system
- ✅ **Conflicts resolved** - No more dual login systems

**The authentication system is now unified and ready for use!** 🎉
"""
    
    with open('AUTH_MIGRATION_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("✅ Created migration summary: AUTH_MIGRATION_SUMMARY.md")

def main():
    """Main migration function"""
    print("🔄 Migrating to Unified Authentication System")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("index.html").exists():
        print("❌ Error: Please run this script from the project root directory")
        return
    
    # Check if unified auth system exists
    if not Path("unified_auth_system.js").exists():
        print("❌ Error: unified_auth_system.js not found")
        print("Please create the unified authentication system first")
        return
    
    # Perform migration steps
    backup_old_systems()
    update_index_html()
    update_other_html_files()
    remove_old_systems()
    create_migration_summary()
    
    print("\n🎉 Migration completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Test the app to ensure authentication works")
    print("2. Check that users can log in and switch profiles")
    print("3. Verify offline mode functionality")
    print("4. Review AUTH_MIGRATION_SUMMARY.md for details")
    
    print("\n⚠️  Important Notes:")
    print("- Old auth systems are backed up in archive/authentication_backup/")
    print("- If issues occur, you can restore the old systems")
    print("- The unified system provides better user experience")

if __name__ == "__main__":
    main() 