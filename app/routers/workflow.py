"""
Automated Recipe Workflow Router
Provides API endpoints for the complete recipe workflow system.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, List
import json
from datetime import datetime
from pathlib import Path

from app.database import get_db, User
from app.core.auth import get_current_user
from app.services.recipe_finder import RecipeFinder
from app.services.recipe_uploader import RecipeUploader
from app.services.complete_workflow import CompleteRecipeWorkflow

router = APIRouter()

# Global workflow instances (in production, use proper state management)
workflow_instances = {}

@router.post("/workflow/start")
async def start_workflow(
    source_folder: str = Query("uploads", description="Source folder to scan"),
    backend_url: str = Query("http://localhost:8000", description="Backend URL"),
    username: Optional[str] = Query(None, description="Username for authentication"),
    password: Optional[str] = Query(None, description="Password for authentication"),
    output_folder: str = Query("sorted_recipes", description="Output folder for organized files"),
    archive_after_upload: bool = Query(True, description="Archive files after upload"),
    generate_reports: bool = Query(True, description="Generate detailed reports"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start the complete recipe workflow"""
    
    try:
        # Create workflow instance
        workflow = CompleteRecipeWorkflow(
            source_folder=source_folder,
            backend_url=backend_url,
            username=username,
            password=password
        )
        
        # Validate prerequisites
        is_valid, errors = workflow.validate_workflow_prerequisites()
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Workflow prerequisites not met: {', '.join(errors)}")
        
        # Store workflow instance
        workflow_id = f"workflow_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        workflow_instances[workflow_id] = workflow
        
        # Start workflow in background
        if background_tasks:
            background_tasks.add_task(
                run_workflow_background,
                workflow_id,
                output_folder,
                archive_after_upload,
                generate_reports
            )
        
        return {
            "workflow_id": workflow_id,
            "status": "started",
            "message": "Workflow started successfully",
            "source_folder": source_folder,
            "output_folder": output_folder
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start workflow: {str(e)}")

async def run_workflow_background(workflow_id: str, output_folder: str, archive_after_upload: bool, generate_reports: bool):
    """Run workflow in background"""
    try:
        workflow = workflow_instances.get(workflow_id)
        if workflow:
            result = workflow.run_complete_workflow(
                output_folder=output_folder,
                archive_after_upload=archive_after_upload,
                generate_reports=generate_reports
            )
            # Store result in workflow instance
            workflow.workflow_result = result
    except Exception as e:
        # Store error in workflow instance
        if workflow_id in workflow_instances:
            workflow_instances[workflow_id].workflow_state['errors'].append(str(e))

@router.get("/workflow/{workflow_id}/status")
async def get_workflow_status(
    workflow_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get the status of a running workflow"""
    
    workflow = workflow_instances.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    status = workflow.get_workflow_status()
    
    # Add result if workflow is completed
    if status['step'] == 'completed' and hasattr(workflow, 'workflow_result'):
        status['result'] = workflow.workflow_result
    
    return status

@router.get("/workflow/list")
async def list_workflows(
    current_user: User = Depends(get_current_user)
):
    """List all workflows for the current user"""
    
    user_workflows = {}
    for workflow_id, workflow in workflow_instances.items():
        if workflow_id.startswith(f"workflow_{current_user.id}_"):
            status = workflow.get_workflow_status()
            user_workflows[workflow_id] = {
                "status": status['step'],
                "current_step": status.get('current_step'),
                "progress": status.get('progress', 0),
                "start_time": status.get('start_time'),
                "errors": status.get('errors', [])
            }
    
    return {
        "workflows": user_workflows,
        "total": len(user_workflows)
    }

@router.post("/workflow/find-recipes")
async def find_recipes(
    source_folder: str = Query("uploads", description="Source folder to scan"),
    current_user: User = Depends(get_current_user)
):
    """Find and analyze recipe files without organizing or uploading"""
    
    try:
        finder = RecipeFinder(source_folder)
        recipe_files = finder.scan_folder()
        
        # Convert to serializable format
        files_data = []
        for file in recipe_files:
            files_data.append({
                "file_path": file.file_path,
                "file_name": file.file_name,
                "file_size": file.file_size,
                "file_type": file.file_type,
                "category": file.category,
                "cuisine": file.cuisine,
                "confidence_score": file.confidence_score,
                "tags": file.tags,
                "detected_ingredients": file.detected_ingredients,
                "cooking_time": file.cooking_time,
                "servings": file.servings,
                "difficulty": file.difficulty
            })
        
        return {
            "files_found": len(recipe_files),
            "files": files_data,
            "summary": {
                "recipes": len([f for f in recipe_files if f.category == 'recipe']),
                "menus": len([f for f in recipe_files if f.category == 'menu']),
                "uncategorized": len([f for f in recipe_files if f.category == 'uncategorized'])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find recipes: {str(e)}")

@router.post("/workflow/organize-recipes")
async def organize_recipes(
    source_folder: str = Query("uploads", description="Source folder to scan"),
    output_folder: str = Query("sorted_recipes", description="Output folder for organized files"),
    current_user: User = Depends(get_current_user)
):
    """Find and organize recipe files by category and cuisine"""
    
    try:
        finder = RecipeFinder(source_folder)
        recipe_files = finder.scan_folder()
        
        if not recipe_files:
            raise HTTPException(status_code=404, detail="No recipe files found")
        
        organized_files = finder.organize_files(recipe_files, output_folder)
        
        # Generate report
        report = finder.generate_report(recipe_files, organized_files)
        report_file = finder.save_report(report, output_folder)
        
        return {
            "files_processed": len(recipe_files),
            "organized_files": {
                "recipes_by_cuisine": {k: len(v) for k, v in organized_files.get('recipes', {}).items()},
                "menus": len(organized_files.get('menus', {})),
                "uncategorized": len(organized_files.get('uncategorized', []))
            },
            "report_file": report_file,
            "summary": report
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to organize recipes: {str(e)}")

@router.post("/workflow/upload-recipes")
async def upload_recipes(
    source_folder: str = Query("sorted_recipes", description="Folder containing organized recipes"),
    backend_url: str = Query("http://localhost:8000", description="Backend URL"),
    username: Optional[str] = Query(None, description="Username for authentication"),
    password: Optional[str] = Query(None, description="Password for authentication"),
    current_user: User = Depends(get_current_user)
):
    """Upload organized recipe files to the backend"""
    
    try:
        uploader = RecipeUploader(backend_url, username, password)
        
        # Check backend status
        if not uploader.check_backend_status():
            raise HTTPException(status_code=503, detail="Backend is not accessible")
        
        # Authenticate if credentials provided
        if username and password:
            if not uploader.authenticate():
                raise HTTPException(status_code=401, detail="Authentication failed")
        
        # Upload files
        results = uploader.upload_folder(source_folder)
        
        # Generate upload report
        upload_summary = {
            'total_uploaded': len([r for r in results if r.success]),
            'total_failed': len([r for r in results if not r.success]),
            'results': [
                {
                    'file_name': r.file_name,
                    'success': r.success,
                    'recipe_id': r.recipe_id,
                    'error_message': r.error_message,
                    'upload_time': r.upload_time
                }
                for r in results
            ]
        }
        
        upload_report = uploader.generate_upload_report(upload_summary)
        report_file = uploader.save_upload_report(upload_report, source_folder)
        
        return {
            "files_uploaded": upload_summary['total_uploaded'],
            "files_failed": upload_summary['total_failed'],
            "success_rate": round((upload_summary['total_uploaded'] / len(results) * 100), 2) if results else 0,
            "report_file": report_file,
            "results": upload_summary['results']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload recipes: {str(e)}")

@router.get("/workflow/validate")
async def validate_workflow_prerequisites(
    source_folder: str = Query("uploads", description="Source folder to validate"),
    backend_url: str = Query("http://localhost:8000", description="Backend URL to validate"),
    username: Optional[str] = Query(None, description="Username for authentication"),
    password: Optional[str] = Query(None, description="Password for authentication"),
    current_user: User = Depends(get_current_user)
):
    """Validate workflow prerequisites"""
    
    try:
        workflow = CompleteRecipeWorkflow(
            source_folder=source_folder,
            backend_url=backend_url,
            username=username,
            password=password
        )
        
        is_valid, errors = workflow.validate_workflow_prerequisites()
        
        return {
            "valid": is_valid,
            "errors": errors,
            "source_folder": source_folder,
            "backend_url": backend_url,
            "has_credentials": bool(username and password)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.delete("/workflow/{workflow_id}")
async def cleanup_workflow(
    workflow_id: str,
    output_folder: str = Query("sorted_recipes", description="Output folder to clean up"),
    current_user: User = Depends(get_current_user)
):
    """Clean up workflow files and remove workflow instance"""
    
    try:
        workflow = workflow_instances.get(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Clean up files
        cleaned = workflow.cleanup_workflow_files(output_folder)
        
        # Remove workflow instance
        del workflow_instances[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "cleaned": cleaned,
            "message": "Workflow cleaned up successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cleanup workflow: {str(e)}")

@router.get("/workflow/statistics")
async def get_workflow_statistics(
    current_user: User = Depends(get_current_user)
):
    """Get statistics about workflows"""
    
    user_workflows = [
        w for workflow_id, w in workflow_instances.items()
        if workflow_id.startswith(f"workflow_{current_user.id}_")
    ]
    
    total_workflows = len(user_workflows)
    completed_workflows = len([w for w in user_workflows if w.workflow_state['step'] == 'completed'])
    failed_workflows = len([w for w in user_workflows if w.workflow_state['step'] == 'failed'])
    running_workflows = len([w for w in user_workflows if w.workflow_state['step'] in ['started', 'running']])
    
    return {
        "total_workflows": total_workflows,
        "completed_workflows": completed_workflows,
        "failed_workflows": failed_workflows,
        "running_workflows": running_workflows,
        "success_rate": round((completed_workflows / total_workflows * 100), 2) if total_workflows > 0 else 0
    } 