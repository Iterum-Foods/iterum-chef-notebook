#!/usr/bin/env python3
"""
Cleanup Script for Consolidated Files
Removes or archives redundant files that have been consolidated
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class ConsolidationCleanup:
    def __init__(self):
        self.archive_dir = Path("archive/consolidated")
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.removed_files = []
        self.archived_files = []
        
    def log_action(self, action, file_path, reason):
        """Log cleanup actions"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {action}: {file_path} - {reason}")
        
    def safe_remove(self, file_path, reason):
        """Safely remove a file with logging"""
        try:
            if Path(file_path).exists():
                os.remove(file_path)
                self.removed_files.append(str(file_path))
                self.log_action("REMOVED", file_path, reason)
                return True
            else:
                self.log_action("SKIP", file_path, "File not found")
                return False
        except Exception as e:
            self.log_action("ERROR", file_path, f"Failed to remove: {e}")
            return False
    
    def safe_archive(self, file_path, reason):
        """Safely archive a file with logging"""
        try:
            source = Path(file_path)
            if source.exists():
                dest = self.archive_dir / source.name
                shutil.move(str(source), str(dest))
                self.archived_files.append(str(file_path))
                self.log_action("ARCHIVED", file_path, reason)
                return True
            else:
                self.log_action("SKIP", file_path, "File not found")
                return False
        except Exception as e:
            self.log_action("ERROR", file_path, f"Failed to archive: {e}")
            return False
    
    def cleanup_testing_files(self):
        """Remove redundant testing files (consolidated into test_unified.bat)"""
        print("\n🧪 Cleaning up redundant testing files...")
        
        files_to_remove = [
            ("test_quick.bat", "Consolidated into test_unified.bat"),
            ("test_full.bat", "Consolidated into test_unified.bat"),
            ("test_ci.bat", "Consolidated into test_unified.bat"),
            ("test_working.bat", "Superseded by test_unified.bat"),
            ("fix_python_path.bat", "Fixed Python path issues resolved"),
            ("start_app.bat", "Replaced by start.bat"),
        ]
        
        for file_path, reason in files_to_remove:
            self.safe_remove(file_path, reason)
    
    def cleanup_documentation_files(self):
        """Archive redundant documentation files (consolidated into COMPREHENSIVE_README.md)"""
        print("\n📚 Cleaning up redundant documentation files...")
        
        files_to_archive = [
            ("README_quickstart.txt", "Content merged into COMPREHENSIVE_README.md"),
            ("PROJECT_CLEANUP_SUMMARY.md", "Content merged into COMPREHENSIVE_README.md"),
            ("AUTOMATED_WORKFLOW_README.md", "Content merged into COMPREHENSIVE_README.md"),
            ("AUTH_MIGRATION_SUMMARY.md", "Outdated migration documentation"),
            ("DUAL_LOGIN_FIX.md", "Fixed - content preserved in archive"),
            ("IMPROVEMENTS_SUMMARY.md", "Superseded by COMPREHENSIVE_README.md"),
            ("IMPROVEMENT_PLAN.md", "Completed improvements documented"),
            ("FEATURE_MAP.md", "Features documented in COMPREHENSIVE_README.md"),
            ("CONFIGURATION.md", "Configuration info in COMPREHENSIVE_README.md"),
            ("FIREBASE_SETUP.md", "Firebase features not currently used"),
            ("PLANT_SKETCHES_INTEGRATION.md", "Feature-specific documentation"),
            ("VENDOR_MANAGEMENT_GUIDE.md", "Content merged into COMPREHENSIVE_README.md"),
            ("AUTOMATED_UPLOAD_GUIDE.md", "Functionality documented in main README"),
            ("ARCHIVE_COMPLETE.md", "Archiving process documentation"),
            ("TESTING_GUIDE.md", "Testing info in COMPREHENSIVE_README.md"),
            ("README_TESTING.md", "Testing info in COMPREHENSIVE_README.md"),
        ]
        
        for file_path, reason in files_to_archive:
            self.safe_archive(file_path, reason)
    
    def cleanup_launcher_files(self):
        """Archive redundant launcher files (consolidated into app_launcher.py and launch_unified.bat)"""
        print("\n🚀 Cleaning up redundant launcher files...")
        
        files_to_archive = [
            ("start_full_app.py", "Consolidated into app_launcher.py"),
            ("serve_frontend.py", "Functionality merged into app_launcher.py"),
            ("launch-notebook.py", "Functionality merged into app_launcher.py"),
            ("launch-notebook.bat", "Replaced by launch_unified.bat"),
            ("start_app.bat", "Superseded by launch_unified.bat"),
            ("archive_project.bat", "Archiving functionality complete"),
            ("start_automated_workflow.py", "Workflow functionality integrated"),
        ]
        
        for file_path, reason in files_to_archive:
            self.safe_archive(file_path, reason)
    
    def cleanup_utility_files(self):
        """Clean up miscellaneous utility files"""
        print("\n🔧 Cleaning up utility files...")
        
        files_to_archive = [
            ("migrate_to_unified_auth.py", "Migration completed"),
            ("archive_project.py", "Archiving process complete"),
            ("google-test.html", "Test file no longer needed"),
            ("test_app.py", "Superseded by comprehensive test suite"),
            ("start_folder_watcher.py", "Folder watching integrated"),
            ("recipe_folder_watcher.py", "Functionality integrated"),
        ]
        
        for file_path, reason in files_to_archive:
            self.safe_archive(file_path, reason)
    
    def create_consolidation_summary(self):
        """Create a summary of the consolidation process"""
        summary_content = f"""# File Consolidation Summary

## 📅 Consolidation Date
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🎯 Consolidation Goals Achieved

### ✅ **Unified Testing System**
- **Replaced**: `test_quick.bat`, `test_full.bat`, `test_ci.bat`
- **With**: `test_unified.bat` - Single test launcher with interactive menu
- **Benefits**: Simplified testing, reduced file count, consistent interface

### ✅ **Comprehensive Documentation**
- **Replaced**: Multiple README files, project summaries, feature guides
- **With**: `COMPREHENSIVE_README.md` - Complete application guide
- **Benefits**: Single source of truth, reduced documentation fragmentation

### ✅ **Unified Application Launcher**
- **Replaced**: `start_full_app.py`, `serve_frontend.py`, `launch-notebook.py/bat`
- **With**: `app_launcher.py` + `launch_unified.bat` - Flexible launcher system
- **Benefits**: Multiple launch modes, consistent error handling, modular design

## 📊 **Files Processed**

### 🗑️ **Removed Files** ({len(self.removed_files)} files)
"""
        
        for file_path in self.removed_files:
            summary_content += f"- {file_path}\n"
        
        summary_content += f"""
### 📁 **Archived Files** ({len(self.archived_files)} files)
"""
        
        for file_path in self.archived_files:
            summary_content += f"- {file_path}\n"
        
        summary_content += f"""
## 🏗️ **New Consolidated Files**

### **Testing System**
- `test_unified.bat` - Unified test launcher with menu options
  - Quick tests (essential only)
  - Full tests (comprehensive with coverage)
  - CI tests (automated pipeline)
  - Interactive menu for ease of use

### **Documentation**
- `COMPREHENSIVE_README.md` - Complete application guide
  - Quick start instructions
  - Feature overview
  - Testing and development
  - Troubleshooting
  - Advanced configuration

### **Application Launcher**
- `app_launcher.py` - Python launcher with multiple modes
  - Full application (backend + frontend)
  - Backend only (API development)
  - Frontend only (UI development)
  - Quiet mode (no browser opening)
- `launch_unified.bat` - Windows batch interface
  - Interactive menu
  - Command line options
  - Error handling

## 🎉 **Benefits Achieved**

### **Reduced Complexity**
- **Before**: {len(self.removed_files) + len(self.archived_files)} redundant files
- **After**: 3 main consolidated files
- **Reduction**: {((len(self.removed_files) + len(self.archived_files)) / (len(self.removed_files) + len(self.archived_files) + 3) * 100):.1f}% fewer files to maintain

### **Improved User Experience**
- Single entry points for common tasks
- Interactive menus for guidance
- Consistent error handling
- Better documentation structure

### **Enhanced Maintainability**
- Centralized functionality
- Reduced code duplication
- Clearer separation of concerns
- Simplified troubleshooting

## 🔄 **Rollback Information**

If you need to restore any consolidated files:
1. Check `archive/consolidated/` directory for archived files
2. Use git history to restore removed files if needed
3. The original functionality is preserved in the new consolidated files

## 📝 **Next Steps**

1. Test the new unified systems
2. Update any external references to old file names
3. Train users on the new simplified interfaces
4. Consider further consolidation opportunities

---

**Consolidation completed successfully!** 🎉
All original functionality has been preserved while significantly reducing file complexity.
"""
        
        # Write summary to file
        summary_path = "CONSOLIDATION_SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"\n📝 Consolidation summary written to: {summary_path}")
    
    def run_cleanup(self):
        """Run the complete cleanup process"""
        print("🧹 Starting File Consolidation Cleanup")
        print("=" * 50)
        
        self.cleanup_testing_files()
        self.cleanup_documentation_files()
        self.cleanup_launcher_files()
        self.cleanup_utility_files()
        
        print(f"\n📊 Cleanup Summary:")
        print(f"   • Removed files: {len(self.removed_files)}")
        print(f"   • Archived files: {len(self.archived_files)}")
        print(f"   • Archive location: {self.archive_dir}")
        
        self.create_consolidation_summary()
        
        print("\n✅ File consolidation cleanup completed!")
        print("\nNew consolidated files to use:")
        print("   • test_unified.bat - For all testing needs")
        print("   • launch_unified.bat - For launching the application")
        print("   • COMPREHENSIVE_README.md - For complete documentation")
        print("   • app_launcher.py - For programmatic application launching")

def main():
    """Main execution function"""
    print("File Consolidation Cleanup")
    print("This will remove/archive redundant files that have been consolidated.")
    print()
    
    choice = input("Proceed with cleanup? (y/N): ").strip().lower()
    if choice not in ['y', 'yes']:
        print("Cleanup cancelled.")
        return
    
    cleanup = ConsolidationCleanup()
    cleanup.run_cleanup()

if __name__ == "__main__":
    main() 