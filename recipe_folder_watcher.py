#!/usr/bin/env python3
"""
Recipe Folder Watcher
Automatically uploads new recipe files from a watched folder to the FastAPI backend.
"""

import os
import time
import requests
import json
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from datetime import datetime

# Configuration
WATCH_FOLDER = "incoming_recipes"  # Folder to watch for new files
ARCHIVE_FOLDER = "incoming_recipes/archive"  # Folder to move processed files
BACKEND_URL = "http://localhost:8000/api/recipes/bulk-upload"  # Backend upload endpoint
SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.doc', '.xlsx', '.xls', '.csv'}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recipe_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RecipeFileHandler(FileSystemEventHandler):
    """Handles file system events for recipe uploads."""
    
    def __init__(self):
        self.processing_files = set()
        self.ensure_folders_exist()
    
    def ensure_folders_exist(self):
        """Create necessary folders if they don't exist."""
        Path(WATCH_FOLDER).mkdir(exist_ok=True)
        Path(ARCHIVE_FOLDER).mkdir(exist_ok=True)
        logger.info(f"Watching folder: {os.path.abspath(WATCH_FOLDER)}")
        logger.info(f"Archive folder: {os.path.abspath(ARCHIVE_FOLDER)}")
    
    def on_created(self, event):
        """Handle new file creation."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            logger.info(f"New recipe file detected: {file_path.name}")
            self.process_file(file_path)
    
    def on_moved(self, event):
        """Handle file moves (e.g., drag and drop)."""
        if event.is_directory:
            return
        
        file_path = Path(event.dest_path)
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            logger.info(f"Recipe file moved to watch folder: {file_path.name}")
            self.process_file(file_path)
    
    def process_file(self, file_path):
        """Process a single recipe file."""
        if file_path.name in self.processing_files:
            return
        
        self.processing_files.add(file_path.name)
        
        try:
            # Wait a moment to ensure file is fully written
            time.sleep(1)
            
            if not file_path.exists():
                logger.warning(f"File no longer exists: {file_path.name}")
                return
            
            # Upload the file
            success = self.upload_file(file_path)
            
            if success:
                # Move to archive
                self.archive_file(file_path)
                logger.info(f"Successfully processed: {file_path.name}")
            else:
                logger.error(f"Failed to process: {file_path.name}")
                
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {str(e)}")
        finally:
            self.processing_files.discard(file_path.name)
    
    def upload_file(self, file_path):
        """Upload a single file to the backend."""
        try:
            logger.info(f"Uploading {file_path.name} to backend...")
            
            # Prepare the upload data
            files = {'files': (file_path.name, open(file_path, 'rb'))}
            data = {
                'default_category': 'Imported',
                'default_cuisine': 'Unknown',
                'default_servings': '4',
                'auto_tag': 'true'
            }
            
            # Upload to backend
            response = requests.post(BACKEND_URL, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Upload successful: {result.get('successful_uploads', 0)} recipes imported")
                return True
            else:
                logger.error(f"Upload failed with status {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error uploading {file_path.name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error uploading {file_path.name}: {str(e)}")
            return False
    
    def archive_file(self, file_path):
        """Move processed file to archive folder."""
        try:
            archive_path = Path(ARCHIVE_FOLDER) / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.name}"
            shutil.move(str(file_path), str(archive_path))
            logger.info(f"Archived: {file_path.name} -> {archive_path.name}")
        except Exception as e:
            logger.error(f"Error archiving {file_path.name}: {str(e)}")

def process_existing_files():
    """Process any existing files in the watch folder."""
    watch_path = Path(WATCH_FOLDER)
    if not watch_path.exists():
        return
    
    handler = RecipeFileHandler()
    existing_files = [f for f in watch_path.iterdir() 
                     if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
    
    if existing_files:
        logger.info(f"Found {len(existing_files)} existing files to process")
        for file_path in existing_files:
            handler.process_file(file_path)
            time.sleep(2)  # Small delay between files

def main():
    """Main function to start the file watcher."""
    logger.info("Starting Recipe Folder Watcher...")
    logger.info(f"Backend URL: {BACKEND_URL}")
    logger.info(f"Supported extensions: {', '.join(SUPPORTED_EXTENSIONS)}")
    
    # Process any existing files first
    process_existing_files()
    
    # Start watching for new files
    event_handler = RecipeFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    
    try:
        logger.info("File watcher is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")
        observer.stop()
    
    observer.join()
    logger.info("File watcher stopped.")

if __name__ == "__main__":
    main() 