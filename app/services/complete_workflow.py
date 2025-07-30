"""
Complete Recipe Workflow Service
Combines recipe finding, sorting, and uploading to Iterum app in one seamless process.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

from .recipe_finder import RecipeFinder
from .recipe_uploader import RecipeUploader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteRecipeWorkflow:
    """Complete workflow for finding, organizing, and uploading recipes"""
    
    def __init__(self, 
                 source_folder: str = "uploads",
                 backend_url: str = "http://localhost:8000",
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        
        self.source_folder = source_folder
        self.backend_url = backend_url
        self.username = username
        self.password = password
        
        # Initialize components
        self.recipe_finder = RecipeFinder(source_folder)
        self.recipe_uploader = RecipeUploader(backend_url, username, password)
        
        # Workflow state
        self.workflow_state = {
            'step': 'initialized',
            'start_time': None,
            'end_time': None,
            'current_step': None,
            'progress': 0,
            'errors': [],
            'warnings': []
        }

    def run_complete_workflow(self, 
                            output_folder: str = "sorted_recipes",
                            archive_after_upload: bool = True,
                            generate_reports: bool = True) -> Dict:
        """Run the complete workflow from start to finish"""
        
        self.workflow_state['start_time'] = datetime.now().isoformat()
        self.workflow_state['step'] = 'started'
        
        try:
            logger.info("🍳 Starting Complete Recipe Workflow")
            logger.info("=" * 60)
            
            # Step 1: Check backend status
            self.workflow_state['current_step'] = 'checking_backend'
            self.workflow_state['progress'] = 10
            
            if not self.recipe_uploader.check_backend_status():
                raise Exception("Backend is not accessible")
            
            logger.info("✅ Backend is running and accessible")
            
            # Step 2: Authenticate (if credentials provided)
            self.workflow_state['current_step'] = 'authenticating'
            self.workflow_state['progress'] = 20
            
            if self.username and self.password:
                if not self.recipe_uploader.authenticate():
                    raise Exception("Authentication failed")
                logger.info("✅ Authentication successful")
            else:
                logger.info("ℹ️  No credentials provided, proceeding without authentication")
            
            # Step 3: Find and analyze recipe files
            self.workflow_state['current_step'] = 'finding_recipes'
            self.workflow_state['progress'] = 30
            
            logger.info("🔍 Step 1: Finding and Analyzing Recipe Files")
            logger.info("-" * 40)
            
            recipe_files = self.recipe_finder.scan_folder()
            
            if not recipe_files:
                raise Exception("No recipe files found in source folder")
            
            logger.info(f"✅ Found {len(recipe_files)} recipe files")
            
            # Step 4: Organize files by category and cuisine
            self.workflow_state['current_step'] = 'organizing_files'
            self.workflow_state['progress'] = 50
            
            logger.info("📁 Step 2: Organizing Files by Category and Cuisine")
            logger.info("-" * 40)
            
            organized_files = self.recipe_finder.organize_files(recipe_files, output_folder)
            
            # Generate organization report
            if generate_reports:
                organization_report = self.recipe_finder.generate_report(recipe_files, organized_files)
                report_file = self.recipe_finder.save_report(organization_report, output_folder)
                logger.info(f"📊 Organization report saved: {report_file}")
            
            # Step 5: Upload organized recipes to backend
            self.workflow_state['current_step'] = 'uploading_recipes'
            self.workflow_state['progress'] = 70
            
            logger.info("📤 Step 3: Uploading Recipes to Backend")
            logger.info("-" * 40)
            
            upload_summary = self.recipe_uploader.upload_organized_recipes(organized_files)
            
            # Generate upload report
            if generate_reports:
                upload_report = self.recipe_uploader.generate_upload_report(upload_summary)
                upload_report_file = self.recipe_uploader.save_upload_report(upload_report, output_folder)
                logger.info(f"📊 Upload report saved: {upload_report_file}")
            
            # Step 6: Archive uploaded files (optional)
            self.workflow_state['current_step'] = 'archiving_files'
            self.workflow_state['progress'] = 90
            
            if archive_after_upload:
                logger.info("📦 Step 4: Archiving Uploaded Files")
                logger.info("-" * 40)
                
                if self.recipe_uploader.archive_uploaded_files(organized_files):
                    logger.info("✅ Files archived successfully")
                else:
                    logger.warning("⚠️  Some files could not be archived")
                    self.workflow_state['warnings'].append("Some files could not be archived")
            
            # Step 7: Generate final summary
            self.workflow_state['current_step'] = 'generating_summary'
            self.workflow_state['progress'] = 100
            
            logger.info("📋 Step 5: Generating Final Summary")
            logger.info("-" * 40)
            
            final_summary = self.generate_final_summary(recipe_files, organized_files, upload_summary)
            
            if generate_reports:
                summary_file = self.save_final_summary(final_summary, output_folder)
                logger.info(f"📊 Final summary saved: {summary_file}")
            
            # Complete workflow
            self.workflow_state['step'] = 'completed'
            self.workflow_state['end_time'] = datetime.now().isoformat()
            
            logger.info("🎉 Complete Recipe Workflow Finished Successfully!")
            logger.info("=" * 60)
            
            return final_summary
            
        except Exception as e:
            self.workflow_state['step'] = 'failed'
            self.workflow_state['end_time'] = datetime.now().isoformat()
            self.workflow_state['errors'].append(str(e))
            
            logger.error(f"❌ Workflow failed: {e}")
            raise

    def generate_final_summary(self, recipe_files: List, organized_files: Dict, upload_summary: Dict) -> Dict:
        """Generate a comprehensive final summary of the workflow"""
        
        # Calculate timing
        start_time = datetime.fromisoformat(self.workflow_state['start_time'])
        end_time = datetime.fromisoformat(self.workflow_state['end_time'])
        duration = (end_time - start_time).total_seconds()
        
        # File analysis summary
        total_files = len(recipe_files)
        recipes = [f for f in recipe_files if f.category == 'recipe']
        menus = [f for f in recipe_files if f.category == 'menu']
        uncategorized = [f for f in recipe_files if f.category == 'uncategorized']
        
        # Cuisine breakdown
        cuisine_stats = {}
        for recipe in recipes:
            cuisine = recipe.cuisine
            if cuisine not in cuisine_stats:
                cuisine_stats[cuisine] = 0
            cuisine_stats[cuisine] += 1
        
        # Upload summary
        total_uploaded = upload_summary['total_uploaded']
        total_failed = upload_summary['total_failed']
        success_rate = (total_uploaded / (total_uploaded + total_failed) * 100) if (total_uploaded + total_failed) > 0 else 0
        
        # Performance metrics
        files_per_minute = (total_files / duration * 60) if duration > 0 else 0
        uploads_per_minute = (total_uploaded / duration * 60) if duration > 0 else 0
        
        summary = {
            'workflow_info': {
                'start_time': self.workflow_state['start_time'],
                'end_time': self.workflow_state['end_time'],
                'duration_seconds': round(duration, 2),
                'status': self.workflow_state['step'],
                'errors': self.workflow_state['errors'],
                'warnings': self.workflow_state['warnings']
            },
            'file_analysis': {
                'total_files_processed': total_files,
                'recipes_found': len(recipes),
                'menus_found': len(menus),
                'uncategorized_files': len(uncategorized),
                'cuisine_breakdown': cuisine_stats,
                'file_types': {
                    ext: len([f for f in recipe_files if f.file_type == ext])
                    for ext in set(f.file_type for f in recipe_files)
                }
            },
            'organization_results': {
                'recipes_by_cuisine': {
                    cuisine: len(files) for cuisine, files in organized_files.get('recipes', {}).items()
                },
                'menus_organized': len(organized_files.get('menus', {})),
                'uncategorized_files': len(organized_files.get('uncategorized', []))
            },
            'upload_results': {
                'total_uploaded': total_uploaded,
                'total_failed': total_failed,
                'success_rate': round(success_rate, 2),
                'uploads_per_minute': round(uploads_per_minute, 2)
            },
            'performance_metrics': {
                'files_per_minute': round(files_per_minute, 2),
                'uploads_per_minute': round(uploads_per_minute, 2),
                'average_processing_time_per_file': round(duration / total_files, 2) if total_files > 0 else 0
            },
            'sample_files': [
                {
                    'name': f.file_name,
                    'category': f.category,
                    'cuisine': f.cuisine,
                    'confidence': f.confidence_score,
                    'upload_success': any(
                        r.file_name == f.file_name and r.success 
                        for cuisine_results in upload_summary.get('recipes', {}).values() 
                        for r in cuisine_results
                    )
                }
                for f in recipe_files[:10]  # First 10 files as sample
            ]
        }
        
        return summary

    def save_final_summary(self, summary: Dict, output_folder: str) -> str:
        """Save the final summary to JSON file"""
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        summary_file = output_path / f"workflow_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Final summary saved to: {summary_file}")
        return str(summary_file)

    def get_workflow_status(self) -> Dict:
        """Get current workflow status"""
        return self.workflow_state.copy()

    def run_step_by_step(self, steps: List[str] = None) -> Dict:
        """Run workflow step by step with user control"""
        
        if steps is None:
            steps = ['find', 'organize', 'upload', 'archive']
        
        results = {}
        
        for step in steps:
            logger.info(f"Running step: {step}")
            
            if step == 'find':
                recipe_files = self.recipe_finder.scan_folder()
                results['find'] = {
                    'files_found': len(recipe_files),
                    'files': recipe_files
                }
                
            elif step == 'organize':
                if 'find' not in results:
                    raise Exception("Must run 'find' step before 'organize'")
                
                organized_files = self.recipe_finder.organize_files(
                    results['find']['files'], 
                    "sorted_recipes"
                )
                results['organize'] = {
                    'organized_files': organized_files
                }
                
            elif step == 'upload':
                if 'organize' not in results:
                    raise Exception("Must run 'organize' step before 'upload'")
                
                upload_summary = self.recipe_uploader.upload_organized_recipes(
                    results['organize']['organized_files']
                )
                results['upload'] = {
                    'upload_summary': upload_summary
                }
                
            elif step == 'archive':
                if 'organize' not in results:
                    raise Exception("Must run 'organize' step before 'archive'")
                
                archived = self.recipe_uploader.archive_uploaded_files(
                    results['organize']['organized_files']
                )
                results['archive'] = {
                    'archived': archived
                }
        
        return results

    def validate_workflow_prerequisites(self) -> Tuple[bool, List[str]]:
        """Validate that all prerequisites are met for the workflow"""
        errors = []
        
        # Check source folder
        if not Path(self.source_folder).exists():
            errors.append(f"Source folder does not exist: {self.source_folder}")
        
        # Check backend connectivity
        if not self.recipe_uploader.check_backend_status():
            errors.append("Backend is not accessible")
        
        # Check authentication (if credentials provided)
        if self.username and self.password:
            if not self.recipe_uploader.authenticate():
                errors.append("Authentication failed")
        
        # Check file permissions
        try:
            test_folder = Path("test_workflow_permissions")
            test_folder.mkdir(exist_ok=True)
            test_file = test_folder / "test.txt"
            test_file.write_text("test")
            test_file.unlink()
            test_folder.rmdir()
        except Exception as e:
            errors.append(f"File permission issues: {e}")
        
        return len(errors) == 0, errors

    def cleanup_workflow_files(self, output_folder: str = "sorted_recipes") -> bool:
        """Clean up temporary workflow files"""
        try:
            output_path = Path(output_folder)
            
            if output_path.exists():
                import shutil
                shutil.rmtree(output_path)
                logger.info(f"Cleaned up workflow files: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error cleaning up workflow files: {e}")
            return False 