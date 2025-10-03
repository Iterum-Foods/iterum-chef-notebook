#!/usr/bin/env python3
"""
Project Archiving Script
Moves unnecessary files to archive and cleans up the project structure.
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectArchiver:
    def __init__(self):
        self.project_root = Path(".")
        self.archive_dir = Path("archive")
        self.archive_dir.mkdir(exist_ok=True)
        
        # Create timestamped archive folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_archive = self.archive_dir / f"archive_{timestamp}"
        self.current_archive.mkdir(exist_ok=True)
        
        # Files to archive (old/duplicate files)
        self.files_to_archive = [
            # Test files directory (old workflow files)
            "Test files",
            
            # Old/duplicate files
            "App - Copy.js",
            "index2.html.txt",
            "index.html.txt",
            "iterum-app2.0.py",
            "iterum-app2.0.txt",
            "iterum_app.py.txt",
            "firebaseConfig.txt",
            "culinary innovation hubv2.txt",
            "culinary innovaction hubv1.py",
            "culinary innovaction hub.pyt.txt",
            "iterum_culinary_studiov2.py",
            
            # Old batch files and scripts
            "complete_workflow.bat",
            "upload_recipes.bat",
            "find_recipes.bat",
            "complete_recipe_workflow.py",
            "run_uploader.py",
            "recipe_uploader.py",
            "run_recipe_finder.py",
            "recipe_menu_finder.py",
            
            # Old documentation
            "LIBRARY_SYSTEM_SUMMARY.md",
            "COMPLETE_WORKFLOW_README.md",
            "RECIPE_FINDER_SUMMARY.md",
            
            # Old logs
            "recipe_uploader.log",
            "recipe_finder.log",
            
            # Old workspace files
            "Iterum App 7.7.25.code-workspace",
            
            # Old backup files
            "calendarManager.js",
            "data_export_import.js",
            "enhanced_loading_system.js",
            "enhanced_search_system.js",
            "equipmentManager.js",
            "error_handler.js",
            "haccpManager.js",
            "ingredientLibrary.js",
            "inventoryManager.js",
            "modern_dashboard.js",
            "recipeImportExport.js",
            "recipeLibrary.js",
            "recipeReview.js",
            "recipeScaling.js",
            "userDataManager.js",
            
            # Old HTML files that are replaced
            "google-test.html",
            
            # Old documentation files
            "AUTH_MIGRATION_SUMMARY.md",
            "AUTOMATED_UPLOAD_GUIDE.md",
            "CONFIGURATION.md",
            "DUAL_LOGIN_FIX.md",
            "FEATURE_MAP.md",
            "FIREBASE_SETUP.md",
            "IMPROVEMENT_PLAN.md",
            "IMPROVEMENTS_SUMMARY.md",
            "PLANT_SKETCHES_INTEGRATION.md",
            "RECIPE_LIBRARY_GUIDE.md",
            "VENDOR_MANAGEMENT_GUIDE.md",
            
            # Old migration files
            "migrate_to_unified_auth.py",
            "migrations/",
            
            # Old test files
            "test_app.py",
            "tests/",
            
            # Old requirements files
            "requirements-simple.txt",
            
            # Old launch scripts
            "launch-notebook.bat",
            "launch-notebook.py",
            "serve_frontend.py",
            "start_app.bat",
            "start_folder_watcher.py",
            
            # Old database files (keep current ones)
            "iterum_rnd.db",
            
            # Old profile files (keep current ones)
            "profiles/",
            
            # Old log files
            "logs/",
            
            # Old template files
            "templates/",
            
            # Old backup directories
            "backup/",
        ]
        
        # Files to keep (current active files)
        self.files_to_keep = [
            # Core app files
            "app/",
            "index.html",
            "main.js",
            "unified_auth_system.js",
            
            # Current HTML pages
            "automated-workflow.html",
            "dashboard.html",
            "equipment-management.html",
            "ingredients.html",
            "inventory.html",
            "menu-builder.html",
            "plant-sketches.html",
            "recipe-developer.html",
            "recipe-library.html",
            "recipe-review.html",
            "recipe-upload.html",
            "vendor-management.html",
            
            # Current JavaScript files
            "calendarManager.js",
            "data_export_import.js",
            "enhanced_loading_system.js",
            "enhanced_search_system.js",
            "equipmentManager.js",
            "error_handler.js",
            "haccpManager.js",
            "ingredientLibrary.js",
            "inventoryManager.js",
            "modern_dashboard.js",
            "recipeImportExport.js",
            "recipeLibrary.js",
            "recipeReview.js",
            "recipeScaling.js",
            "userDataManager.js",
            
            # Current Python files
            "start_automated_workflow.py",
            "recipe_folder_watcher.py",
            
            # Current documentation
            "AUTOMATED_WORKFLOW_README.md",
            "README.md",
            "README_quickstart.txt",
            
            # Current configuration
            "package.json",
            "package-lock.json",
            "requirements.txt",
            
            # Current data files
            "culinary_data.db",
            "equipment_database.csv",
            
            # Current uploads
            "uploads/",
            "incoming_recipes/",
            
            # Current profiles (active users)
            "profiles/",
            
            # Current logs
            "logs/",
        ]

    def archive_files(self):
        """Archive unnecessary files and clean up the project"""
        logger.info(f"Starting project archiving to {self.current_archive}")
        
        archived_files = []
        skipped_files = []
        errors = []
        
        for file_path in self.files_to_archive:
            source_path = self.project_root / file_path
            
            if source_path.exists():
                try:
                    dest_path = self.current_archive / file_path
                    
                    # Create parent directories if needed
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if source_path.is_file():
                        shutil.copy2(source_path, dest_path)
                        source_path.unlink()  # Remove original
                        logger.info(f"Archived file: {file_path}")
                        archived_files.append(file_path)
                    elif source_path.is_dir():
                        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                        shutil.rmtree(source_path)  # Remove original
                        logger.info(f"Archived directory: {file_path}")
                        archived_files.append(file_path)
                        
                except Exception as e:
                    logger.error(f"Error archiving {file_path}: {e}")
                    errors.append((file_path, str(e)))
            else:
                logger.info(f"File not found, skipping: {file_path}")
                skipped_files.append(file_path)
        
        return archived_files, skipped_files, errors

    def create_archive_index(self):
        """Create an index of archived files"""
        archive_index = {
            "archive_date": datetime.now().isoformat(),
            "archive_location": str(self.current_archive),
            "archived_files": [],
            "skipped_files": [],
            "errors": [],
            "project_cleanup_summary": {
                "total_files_archived": 0,
                "total_directories_archived": 0,
                "total_size_archived": 0,
                "errors_count": 0
            }
        }
        
        # Scan archived files
        for root, dirs, files in os.walk(self.current_archive):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.current_archive)
                
                try:
                    file_size = file_path.stat().st_size
                    archive_index["archived_files"].append({
                        "path": str(relative_path),
                        "size_bytes": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })
                    archive_index["project_cleanup_summary"]["total_files_archived"] += 1
                    archive_index["project_cleanup_summary"]["total_size_archived"] += file_size
                except Exception as e:
                    logger.error(f"Error processing archived file {file_path}: {e}")
        
        # Save archive index
        index_file = self.current_archive / "ARCHIVE_INDEX.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(archive_index, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Archive index created: {index_file}")
        return archive_index

    def create_cleanup_report(self, archived_files, skipped_files, errors):
        """Create a cleanup report"""
        report = {
            "cleanup_date": datetime.now().isoformat(),
            "summary": {
                "files_archived": len(archived_files),
                "files_skipped": len(skipped_files),
                "errors": len(errors),
                "archive_location": str(self.current_archive)
            },
            "archived_files": archived_files,
            "skipped_files": skipped_files,
            "errors": errors,
            "current_project_structure": self.get_current_structure()
        }
        
        # Save cleanup report
        report_file = self.project_root / "CLEANUP_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Cleanup report created: {report_file}")
        return report

    def get_current_structure(self):
        """Get current project structure after cleanup"""
        structure = {
            "directories": [],
            "files": [],
            "total_size": 0
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip archive directory
            if "archive" in root:
                continue
                
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                relative_path = dir_path.relative_to(self.project_root)
                structure["directories"].append(str(relative_path))
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                
                try:
                    file_size = file_path.stat().st_size
                    structure["files"].append({
                        "path": str(relative_path),
                        "size_bytes": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    })
                    structure["total_size"] += file_size
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
        
        return structure

    def print_summary(self, archived_files, skipped_files, errors, archive_index):
        """Print a summary of the archiving process"""
        print("\n" + "="*70)
        print("🏗️  PROJECT CLEANUP SUMMARY")
        print("="*70)
        
        print(f"📁 Archive Location: {self.current_archive}")
        print(f"📅 Archive Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("📊 ARCHIVING RESULTS:")
        print(f"✅ Files/Directories Archived: {len(archived_files)}")
        print(f"⏭️  Files Skipped (not found): {len(skipped_files)}")
        print(f"❌ Errors: {len(errors)}")
        print()
        
        if archive_index:
            total_size_mb = round(archive_index["project_cleanup_summary"]["total_size_archived"] / (1024 * 1024), 2)
            print(f"💾 Total Size Archived: {total_size_mb} MB")
            print(f"📄 Total Files Archived: {archive_index['project_cleanup_summary']['total_files_archived']}")
            print()
        
        if archived_files:
            print("📦 ARCHIVED FILES:")
            for file in archived_files[:10]:  # Show first 10
                print(f"   • {file}")
            if len(archived_files) > 10:
                print(f"   ... and {len(archived_files) - 10} more files")
            print()
        
        if errors:
            print("❌ ERRORS:")
            for file, error in errors[:5]:  # Show first 5
                print(f"   • {file}: {error}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more errors")
            print()
        
        print("🎯 CURRENT PROJECT STRUCTURE:")
        current_structure = self.get_current_structure()
        print(f"📁 Directories: {len(current_structure['directories'])}")
        print(f"📄 Files: {len(current_structure['files'])}")
        total_size_mb = round(current_structure['total_size'] / (1024 * 1024), 2)
        print(f"💾 Total Size: {total_size_mb} MB")
        print()
        
        print("✅ CLEANUP COMPLETE!")
        print("Your project has been cleaned up and unnecessary files archived.")
        print("="*70)

def main():
    """Main archiving function"""
    print("🏗️  Iterum Project Cleanup and Archiving")
    print("="*50)
    print("This script will:")
    print("1. Archive old/duplicate files to archive/")
    print("2. Clean up the project structure")
    print("3. Create detailed reports")
    print("4. Preserve all current functionality")
    print("="*50)
    
    # Confirm with user
    response = input("\nDo you want to proceed with archiving? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Archiving cancelled.")
        return
    
    # Create archiver and run cleanup
    archiver = ProjectArchiver()
    
    try:
        # Archive files
        archived_files, skipped_files, errors = archiver.archive_files()
        
        # Create archive index
        archive_index = archiver.create_archive_index()
        
        # Create cleanup report
        cleanup_report = archiver.create_cleanup_report(archived_files, skipped_files, errors)
        
        # Print summary
        archiver.print_summary(archived_files, skipped_files, errors, archive_index)
        
        print("\n📋 NEXT STEPS:")
        print("1. Review the archived files in: archive/")
        print("2. Check CLEANUP_REPORT.json for details")
        print("3. Test your app to ensure everything works")
        print("4. Delete archive/ if you're satisfied with the cleanup")
        
    except Exception as e:
        logger.error(f"Error during archiving: {e}")
        print(f"❌ Archiving failed: {e}")

if __name__ == "__main__":
    main() 