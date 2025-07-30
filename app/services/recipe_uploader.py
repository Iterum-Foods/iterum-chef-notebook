"""
Recipe Uploader Service
Uploads organized recipe files to the Iterum app backend with progress tracking.
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UploadResult:
    """Represents the result of a file upload"""
    file_path: str
    file_name: str
    success: bool
    recipe_id: Optional[int] = None
    error_message: Optional[str] = None
    upload_time: Optional[float] = None

class RecipeUploader:
    """Service for uploading recipe files to the Iterum app backend"""
    
    def __init__(self, backend_url: str = "http://localhost:8000", username: Optional[str] = None, password: Optional[str] = None):
        self.backend_url = backend_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.auth_token = None
        self.upload_results = []
        
        # Configure session
        self.session.headers.update({
            'User-Agent': 'Iterum-Recipe-Uploader/1.0',
            'Accept': 'application/json'
        })

    def authenticate(self) -> bool:
        """Authenticate with the backend"""
        if not self.username or not self.password:
            logger.info("No credentials provided, proceeding without authentication")
            return True
        
        try:
            auth_url = f"{self.backend_url}/api/profiles/login"
            auth_data = {
                "email": self.username,
                "password": self.password
            }
            
            response = self.session.post(auth_url, json=auth_data)
            
            if response.status_code == 200:
                auth_response = response.json()
                if 'access_token' in auth_response:
                    self.auth_token = auth_response['access_token']
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.auth_token}'
                    })
                    logger.info("Authentication successful")
                    return True
                else:
                    logger.error("No access token in response")
                    return False
            else:
                logger.error(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False

    def check_backend_status(self) -> bool:
        """Check if the backend is running and accessible"""
        try:
            response = self.session.get(f"{self.backend_url}/health")
            if response.status_code == 200:
                logger.info("Backend is running and accessible")
                return True
            else:
                logger.error(f"Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Backend connection error: {e}")
            return False

    def upload_file(self, file_path: str, default_category: str = "Imported", default_cuisine: str = "Unknown", default_servings: int = 4) -> UploadResult:
        """Upload a single recipe file to the backend"""
        start_time = time.time()
        
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return UploadResult(
                    file_path=file_path,
                    file_name=file_path_obj.name,
                    success=False,
                    error_message="File not found"
                )
            
            # Prepare upload data
            upload_url = f"{self.backend_url}/api/recipes/bulk-upload"
            
            with open(file_path, 'rb') as f:
                files = {'files': (file_path_obj.name, f, 'application/octet-stream')}
                data = {
                    'default_category': default_category,
                    'default_cuisine': default_cuisine,
                    'default_servings': str(default_servings),
                    'auto_tag': 'true'
                }
                
                response = self.session.post(upload_url, files=files, data=data)
            
            upload_time = time.time() - start_time
            
            if response.status_code == 200:
                result_data = response.json()
                if 'recipes' in result_data and len(result_data['recipes']) > 0:
                    recipe_id = result_data['recipes'][0].get('id')
                    return UploadResult(
                        file_path=file_path,
                        file_name=file_path_obj.name,
                        success=True,
                        recipe_id=recipe_id,
                        upload_time=upload_time
                    )
                else:
                    return UploadResult(
                        file_path=file_path,
                        file_name=file_path_obj.name,
                        success=False,
                        error_message="No recipes created from file",
                        upload_time=upload_time
                    )
            else:
                return UploadResult(
                    file_path=file_path,
                    file_name=file_path_obj.name,
                    success=False,
                    error_message=f"Upload failed: {response.status_code} - {response.text}",
                    upload_time=upload_time
                )
                
        except Exception as e:
            upload_time = time.time() - start_time
            return UploadResult(
                file_path=file_path,
                file_name=Path(file_path).name,
                success=False,
                error_message=str(e),
                upload_time=upload_time
            )

    def upload_folder(self, folder_path: str, default_category: str = "Imported", default_cuisine: str = "Unknown", default_servings: int = 4, max_concurrent: int = 3) -> List[UploadResult]:
        """Upload all recipe files in a folder"""
        folder_path_obj = Path(folder_path)
        if not folder_path_obj.exists():
            logger.error(f"Folder not found: {folder_path}")
            return []
        
        # Find all recipe files
        recipe_extensions = {'.xlsx', '.xls', '.docx', '.doc', '.pdf', '.txt', '.csv', '.md'}
        recipe_files = []
        
        for file_path in folder_path_obj.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in recipe_extensions:
                recipe_files.append(str(file_path))
        
        logger.info(f"Found {len(recipe_files)} recipe files to upload")
        
        # Upload files
        results = []
        for i, file_path in enumerate(recipe_files):
            logger.info(f"Uploading {i+1}/{len(recipe_files)}: {Path(file_path).name}")
            result = self.upload_file(file_path, default_category, default_cuisine, default_servings)
            results.append(result)
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.5)
        
        self.upload_results = results
        return results

    def upload_organized_recipes(self, organized_files: Dict, default_category: str = "Imported") -> Dict:
        """Upload organized recipe files by category and cuisine"""
        upload_summary = {
            'recipes': {},
            'menus': {},
            'uncategorized': [],
            'total_uploaded': 0,
            'total_failed': 0,
            'start_time': datetime.now().isoformat(),
            'end_time': None
        }
        
        # Upload recipes by cuisine
        for cuisine, files in organized_files.get('recipes', {}).items():
            logger.info(f"Uploading {len(files)} recipes for cuisine: {cuisine}")
            cuisine_results = []
            
            for recipe_file in files:
                result = self.upload_file(
                    recipe_file.file_path,
                    default_category=default_category,
                    default_cuisine=cuisine,
                    default_servings=recipe_file.servings or 4
                )
                cuisine_results.append(result)
                
                if result.success:
                    upload_summary['total_uploaded'] += 1
                else:
                    upload_summary['total_failed'] += 1
            
            upload_summary['recipes'][cuisine] = cuisine_results
        
        # Upload menus
        for menu_name, menu_file in organized_files.get('menus', {}).items():
            logger.info(f"Uploading menu: {menu_name}")
            result = self.upload_file(
                menu_file.file_path,
                default_category="Menu",
                default_cuisine="Unknown",
                default_servings=4
            )
            upload_summary['menus'][menu_name] = result
            
            if result.success:
                upload_summary['total_uploaded'] += 1
            else:
                upload_summary['total_failed'] += 1
        
        # Upload uncategorized files
        for uncat_file in organized_files.get('uncategorized', []):
            logger.info(f"Uploading uncategorized file: {uncat_file.file_name}")
            result = self.upload_file(
                uncat_file.file_path,
                default_category="Uncategorized",
                default_cuisine="Unknown",
                default_servings=4
            )
            upload_summary['uncategorized'].append(result)
            
            if result.success:
                upload_summary['total_uploaded'] += 1
            else:
                upload_summary['total_failed'] += 1
        
        upload_summary['end_time'] = datetime.now().isoformat()
        return upload_summary

    def archive_uploaded_files(self, organized_files: Dict, archive_folder: str = "uploaded_recipes") -> bool:
        """Move successfully uploaded files to archive folder"""
        try:
            archive_path = Path(archive_folder)
            archive_path.mkdir(exist_ok=True)
            
            # Create timestamped archive subfolder
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_subfolder = archive_path / f"upload_{timestamp}"
            archive_subfolder.mkdir(exist_ok=True)
            
            archived_count = 0
            
            # Archive recipes
            for cuisine, files in organized_files.get('recipes', {}).items():
                cuisine_archive = archive_subfolder / 'recipes' / cuisine
                cuisine_archive.mkdir(parents=True, exist_ok=True)
                
                for recipe_file in files:
                    source_path = Path(recipe_file.file_path)
                    dest_path = cuisine_archive / recipe_file.file_name
                    
                    try:
                        import shutil
                        shutil.move(str(source_path), str(dest_path))
                        archived_count += 1
                    except Exception as e:
                        logger.error(f"Error archiving {source_path}: {e}")
            
            # Archive menus
            menus_archive = archive_subfolder / 'menus'
            menus_archive.mkdir(exist_ok=True)
            
            for menu_name, menu_file in organized_files.get('menus', {}).items():
                source_path = Path(menu_file.file_path)
                dest_path = menus_archive / menu_file.file_name
                
                try:
                    import shutil
                    shutil.move(str(source_path), str(dest_path))
                    archived_count += 1
                except Exception as e:
                    logger.error(f"Error archiving {source_path}: {e}")
            
            # Archive uncategorized
            uncat_archive = archive_subfolder / 'uncategorized'
            uncat_archive.mkdir(exist_ok=True)
            
            for uncat_file in organized_files.get('uncategorized', []):
                source_path = Path(uncat_file.file_path)
                dest_path = uncat_archive / uncat_file.file_name
                
                try:
                    import shutil
                    shutil.move(str(source_path), str(dest_path))
                    archived_count += 1
                except Exception as e:
                    logger.error(f"Error archiving {source_path}: {e}")
            
            logger.info(f"Archived {archived_count} files to {archive_subfolder}")
            return True
            
        except Exception as e:
            logger.error(f"Error during archiving: {e}")
            return False

    def generate_upload_report(self, upload_summary: Dict) -> Dict:
        """Generate a comprehensive upload report"""
        total_files = upload_summary['total_uploaded'] + upload_summary['total_failed']
        success_rate = (upload_summary['total_uploaded'] / total_files * 100) if total_files > 0 else 0
        
        # Calculate timing
        start_time = datetime.fromisoformat(upload_summary['start_time'])
        end_time = datetime.fromisoformat(upload_summary['end_time'])
        duration = (end_time - start_time).total_seconds()
        
        # Detailed breakdown
        cuisine_breakdown = {}
        for cuisine, results in upload_summary['recipes'].items():
            successful = len([r for r in results if r.success])
            failed = len([r for r in results if not r.success])
            cuisine_breakdown[cuisine] = {
                'total': len(results),
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / len(results) * 100) if len(results) > 0 else 0
            }
        
        # Error analysis
        errors = {}
        for category, results in upload_summary.items():
            if isinstance(results, list):
                for result in results:
                    if not result.success and result.error_message:
                        error_type = result.error_message.split(':')[0] if ':' in result.error_message else 'Unknown'
                        if error_type not in errors:
                            errors[error_type] = 0
                        errors[error_type] += 1
            elif isinstance(results, dict):
                for sub_results in results.values():
                    if isinstance(sub_results, list):
                        for result in sub_results:
                            if not result.success and result.error_message:
                                error_type = result.error_message.split(':')[0] if ':' in result.error_message else 'Unknown'
                                if error_type not in errors:
                                    errors[error_type] = 0
                                errors[error_type] += 1
        
        report = {
            'upload_summary': {
                'total_files': total_files,
                'successful_uploads': upload_summary['total_uploaded'],
                'failed_uploads': upload_summary['total_failed'],
                'success_rate': round(success_rate, 2),
                'duration_seconds': round(duration, 2),
                'files_per_minute': round((total_files / duration * 60), 2) if duration > 0 else 0
            },
            'cuisine_breakdown': cuisine_breakdown,
            'menu_uploads': {
                'total': len(upload_summary['menus']),
                'successful': len([r for r in upload_summary['menus'].values() if r.success]),
                'failed': len([r for r in upload_summary['menus'].values() if not r.success])
            },
            'uncategorized_uploads': {
                'total': len(upload_summary['uncategorized']),
                'successful': len([r for r in upload_summary['uncategorized'] if r.success]),
                'failed': len([r for r in upload_summary['uncategorized'] if not r.success])
            },
            'error_analysis': errors,
            'timestamp': datetime.now().isoformat()
        }
        
        return report

    def save_upload_report(self, report: Dict, output_folder: str = "uploaded_recipes") -> str:
        """Save the upload report to JSON file"""
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        report_file = output_path / f"upload_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Upload report saved to: {report_file}")
        return str(report_file)

    def get_upload_progress(self) -> Dict:
        """Get current upload progress"""
        if not self.upload_results:
            return {'status': 'no_uploads'}
        
        total = len(self.upload_results)
        successful = len([r for r in self.upload_results if r.success])
        failed = len([r for r in self.upload_results if not r.success])
        
        return {
            'status': 'completed',
            'total_files': total,
            'successful': successful,
            'failed': failed,
            'progress_percent': 100,
            'success_rate': round((successful / total * 100), 2) if total > 0 else 0
        } 