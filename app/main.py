from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.database import engine, Base
from app.routers import recipes, ingredients, versions, uploads, auth, profiles, data, vendors, menu, integrations, workflow, images, waitlist, autosave, recipe_scaling, projects, ai_enhancements, trial, firebase_sync, menu_sync, notes_sync, ideas_sync
from typing import List
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Iterum R&D Chef Notebook Backend...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Iterum R&D Chef Notebook Backend...")


# Create FastAPI app
app = FastAPI(
    title="Iterum R&D Chef Notebook API",
    description="Professional recipe R&D and publishing system for home and commercial kitchens",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(firebase_sync.router, prefix="/api/firebase", tags=["Firebase Sync"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["Recipes"])
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["Ingredients"])
app.include_router(versions.router, prefix="/api/versions", tags=["Version Control"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["Recipe Uploads"])
app.include_router(images.router, prefix="/api/images", tags=["Image Management"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["Profiles"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(vendors.router, prefix="/api", tags=["Vendors"])
app.include_router(menu.router, prefix="/api/menu", tags=["menu"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Automated Workflow"])
app.include_router(autosave.router, tags=["Auto-Save"])
app.include_router(recipe_scaling.router, tags=["Recipe Scaling"])
app.include_router(waitlist.router, prefix="/api/waitlist", tags=["Waitlist"])
app.include_router(projects.router, tags=["Projects"])
app.include_router(ai_enhancements.router, tags=["AI Enhancements"])
app.include_router(trial.router, tags=["Trial Management"])

# New sync routers for long-term storage
app.include_router(menu_sync.router, prefix="/api/menus", tags=["Menu Sync"])
app.include_router(notes_sync.router, prefix="/api/notes", tags=["Notes Sync"])
app.include_router(ideas_sync.router, prefix="/api/ideas", tags=["Recipe Ideas Sync"])

# Health check endpoints
@app.get("/")
async def root():
    return {
        "message": "Iterum R&D Chef Notebook API",
        "version": "2.0.0",
        "status": "running",
        "environment": "development"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iterum-rnd-api"}

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    import psutil
    from pathlib import Path
    
    try:
        # Basic system info
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        
        # Check required directories
        directories = ["uploads", "logs", "profiles", "incoming_recipes"]
        dir_status = {}
        for directory in directories:
            path = Path(directory)
            dir_status[directory] = {
                "exists": path.exists(),
                "writable": path.exists() and path.is_dir()
            }
        
        # Check database
        db_path = Path("culinary_data.db")
        db_status = {
            "exists": db_path.exists(),
            "size_mb": round(db_path.stat().st_size / (1024 * 1024), 2) if db_path.exists() else 0
        }
        
        # Check equipment database
        equipment_path = Path("equipment_database.csv")
        equipment_status = {
            "exists": equipment_path.exists(),
            "size_mb": round(equipment_path.stat().st_size / (1024 * 1024), 2) if equipment_path.exists() else 0
        }
        
        return {
            "timestamp": "2025-07-09T16:00:00Z",
            "status": "healthy",
            "error_count": 0,
            "warning_count": 0,
            "checks": {
                "system_resources": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "disk_percent": round((disk.used / disk.total) * 100, 2)
                },
                "file_system": dir_status,
                "database": db_status,
                "equipment_database": equipment_status
            }
        }
    except Exception as e:
        return {
            "timestamp": "2025-07-09T16:00:00Z",
            "status": "error",
            "error_count": 1,
            "warning_count": 0,
            "error": str(e)
        }

@app.get("/api/search")
def search_files(query: str, folders: List[str] = Query(default=["."], description="Folders to search (default: project root)")):
    """Search for files by name in multiple folders or the entire computer."""
    results = []
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            for file in files:
                if query.lower() in file.lower():
                    results.append(os.path.abspath(os.path.join(root, file)))
    return {"results": results}

@app.get("/api/list_dir")
def list_dir(path: str = "."):
    """List subdirectories for a given path (1 level deep)."""
    import os
    dirs = []
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                # List subdirs (1 level deep)
                subdirs = []
                try:
                    for subentry in os.scandir(entry.path):
                        if subentry.is_dir():
                            subdirs.append({
                                "name": subentry.name,
                                "path": os.path.abspath(subentry.path),
                                "subdirs": []
                            })
                except Exception:
                    pass
                dirs.append({
                    "name": entry.name,
                    "path": os.path.abspath(entry.path),
                    "subdirs": subdirs
                })
    except Exception as e:
        return []
    return dirs


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 