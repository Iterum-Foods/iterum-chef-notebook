#!/usr/bin/env python3
"""
Google Drive Integration for Recipe Management System
Upload, download, sync, and share recipes via Google Drive
"""

import os
import sys
import pickle
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Google Drive libraries not installed. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveRecipeManager:
    """Manage recipes in Google Drive."""
    
    def __init__(self, library_path="recipe_library"):
        self.library_path = Path(library_path)
        self.db_path = self.library_path / "recipe_library.db"
        self.creds = None
        self.service = None
        self.drive_folder_id = None
        
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google Drive libraries not installed")
        
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Drive."""
        token_path = 'token.pickle'
        
        # Check if we have saved credentials
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If credentials are invalid or don't exist, authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("\n" + "=" * 80)
                    print("GOOGLE DRIVE SETUP REQUIRED")
                    print("=" * 80)
                    print("\nYou need to set up Google Drive API access:")
                    print("\n1. Go to: https://console.cloud.google.com/")
                    print("2. Create a new project (or select existing)")
                    print("3. Enable Google Drive API")
                    print("4. Create OAuth 2.0 credentials")
                    print("5. Download credentials as 'credentials.json'")
                    print("6. Place credentials.json in this folder")
                    print("\nSee: GOOGLE_DRIVE_SETUP.md for detailed instructions")
                    print("=" * 80)
                    raise FileNotFoundError("credentials.json not found")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('drive', 'v3', credentials=self.creds)
        print("[OK] Authenticated with Google Drive")
    
    def get_or_create_folder(self, folder_name="Recipe Library"):
        """Get or create the main recipe folder in Google Drive."""
        if self.drive_folder_id:
            return self.drive_folder_id
        
        try:
            # Search for existing folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                self.drive_folder_id = folders[0]['id']
                print(f"[OK] Found existing folder: {folder_name}")
            else:
                # Create new folder
                file_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(
                    body=file_metadata,
                    fields='id'
                ).execute()
                self.drive_folder_id = folder.get('id')
                print(f"[OK] Created new folder: {folder_name}")
            
            return self.drive_folder_id
        
        except HttpError as error:
            print(f"[ERROR] An error occurred: {error}")
            return None
    
    def upload_recipe(self, file_path: Path, recipe_title: str = None) -> Optional[str]:
        """Upload a single recipe to Google Drive."""
        try:
            folder_id = self.get_or_create_folder()
            
            if recipe_title is None:
                recipe_title = file_path.stem
            
            file_metadata = {
                'name': f"{recipe_title}{file_path.suffix}",
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(
                str(file_path),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # Check if file already exists
            query = f"name='{file_metadata['name']}' and '{folder_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields='files(id, name)').execute()
            existing_files = results.get('files', [])
            
            if existing_files:
                # Update existing file
                file_id = existing_files[0]['id']
                file = self.service.files().update(
                    fileId=file_id,
                    media_body=media
                ).execute()
                print(f"   [UPDATED] {recipe_title}")
            else:
                # Create new file
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id, webViewLink'
                ).execute()
                print(f"   [UPLOADED] {recipe_title}")
            
            return file.get('id')
        
        except HttpError as error:
            print(f"   [ERROR] Failed to upload {recipe_title}: {error}")
            return None
    
    def upload_all_recipes(self):
        """Upload all recipes from the library to Google Drive."""
        print("\n" + "=" * 80)
        print("           UPLOADING RECIPES TO GOOGLE DRIVE")
        print("=" * 80)
        
        # Get all recipes from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title, library_path FROM recipes")
        recipes = cursor.fetchall()
        conn.close()
        
        print(f"\nFound {len(recipes)} recipes to upload\n")
        
        uploaded = 0
        errors = 0
        
        for title, lib_path in recipes:
            file_id = self.upload_recipe(Path(lib_path), title)
            if file_id:
                uploaded += 1
                # Update database with Google Drive file ID
                self.update_drive_id(title, file_id)
            else:
                errors += 1
        
        print("\n" + "=" * 80)
        print(f"[OK] Uploaded: {uploaded} recipes")
        if errors:
            print(f"[ERROR] Failed: {errors} recipes")
        print("=" * 80)
    
    def update_drive_id(self, recipe_title: str, drive_id: str):
        """Store Google Drive file ID in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE recipes ADD COLUMN drive_file_id TEXT")
        except:
            pass
        
        cursor.execute(
            "UPDATE recipes SET drive_file_id = ? WHERE title = ?",
            (drive_id, recipe_title)
        )
        conn.commit()
        conn.close()
    
    def download_recipe(self, file_id: str, destination_path: Path):
        """Download a recipe from Google Drive."""
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            with open(destination_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
            
            return True
        
        except HttpError as error:
            print(f"[ERROR] Download failed: {error}")
            return False
    
    def list_drive_recipes(self) -> List[Dict]:
        """List all recipes in Google Drive."""
        folder_id = self.get_or_create_folder()
        
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields='files(id, name, modifiedTime, size, webViewLink)',
                orderBy='name'
            ).execute()
            
            files = results.get('files', [])
            return files
        
        except HttpError as error:
            print(f"[ERROR] Failed to list files: {error}")
            return []
    
    def sync_to_drive(self):
        """Sync local recipes to Google Drive (upload new/modified)."""
        print("\n" + "=" * 80)
        print("           SYNCING TO GOOGLE DRIVE")
        print("=" * 80)
        
        # Get local recipes
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title, library_path, modified_date FROM recipes")
        local_recipes = cursor.fetchall()
        conn.close()
        
        # Get Drive recipes
        drive_recipes = self.list_drive_recipes()
        drive_dict = {f['name'].rsplit('.', 1)[0]: f for f in drive_recipes}
        
        print(f"\nLocal recipes: {len(local_recipes)}")
        print(f"Drive recipes: {len(drive_recipes)}\n")
        
        uploaded = 0
        skipped = 0
        
        for title, lib_path, modified_date in local_recipes:
            local_file = Path(lib_path)
            
            if title in drive_dict:
                # Compare modification times
                drive_file = drive_dict[title]
                drive_modified = datetime.fromisoformat(
                    drive_file['modifiedTime'].replace('Z', '+00:00')
                )
                local_modified = datetime.fromisoformat(modified_date)
                
                if local_modified > drive_modified.replace(tzinfo=None):
                    # Local is newer, upload
                    self.upload_recipe(local_file, title)
                    uploaded += 1
                else:
                    skipped += 1
            else:
                # New recipe, upload
                self.upload_recipe(local_file, title)
                uploaded += 1
        
        print("\n" + "=" * 80)
        print(f"[OK] Uploaded/Updated: {uploaded} recipes")
        print(f"[OK] Already up-to-date: {skipped} recipes")
        print("=" * 80)
    
    def sync_from_drive(self):
        """Sync from Google Drive to local (download new/modified)."""
        print("\n" + "=" * 80)
        print("           SYNCING FROM GOOGLE DRIVE")
        print("=" * 80)
        
        drive_recipes = self.list_drive_recipes()
        
        # Get local recipes
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM recipes")
        local_titles = {row[0] for row in cursor.fetchall()}
        conn.close()
        
        print(f"\nDrive recipes: {len(drive_recipes)}")
        print(f"Local recipes: {len(local_titles)}\n")
        
        downloaded = 0
        
        for drive_file in drive_recipes:
            title = drive_file['name'].rsplit('.', 1)[0]
            
            if title not in local_titles:
                # New recipe, download
                dest_path = self.library_path / drive_file['name']
                if self.download_recipe(drive_file['id'], dest_path):
                    print(f"   [DOWNLOADED] {title}")
                    downloaded += 1
        
        print("\n" + "=" * 80)
        print(f"[OK] Downloaded: {downloaded} new recipes")
        print("=" * 80)
    
    def get_share_link(self, recipe_title: str) -> Optional[str]:
        """Get shareable link for a recipe."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT drive_file_id FROM recipes WHERE title = ?", (recipe_title,))
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            file_id = row[0]
            try:
                # Make file shareable (anyone with link can view)
                permission = {
                    'type': 'anyone',
                    'role': 'reader'
                }
                self.service.permissions().create(
                    fileId=file_id,
                    body=permission
                ).execute()
                
                # Get the link
                file = self.service.files().get(
                    fileId=file_id,
                    fields='webViewLink'
                ).execute()
                
                return file.get('webViewLink')
            
            except HttpError as error:
                print(f"[ERROR] Failed to get share link: {error}")
                return None
        
        return None
    
    def create_backup(self):
        """Create a complete backup of all recipes to Google Drive."""
        print("\n" + "=" * 80)
        print("           CREATING GOOGLE DRIVE BACKUP")
        print("=" * 80)
        
        # Create backup folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder_name = f"Recipe_Backup_{timestamp}"
        
        file_metadata = {
            'name': backup_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.get_or_create_folder()]
        }
        
        backup_folder = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        backup_folder_id = backup_folder.get('id')
        print(f"\n[OK] Created backup folder: {backup_folder_name}")
        
        # Upload all recipe files
        recipe_files = list(self.library_path.glob("*.xlsx"))
        
        print(f"\nBacking up {len(recipe_files)} files...\n")
        
        for recipe_file in recipe_files:
            file_metadata = {
                'name': recipe_file.name,
                'parents': [backup_folder_id]
            }
            
            media = MediaFileUpload(str(recipe_file))
            
            self.service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
            
            print(f"   [BACKED UP] {recipe_file.name}")
        
        # Also backup database
        db_metadata = {
            'name': 'recipe_library.db',
            'parents': [backup_folder_id]
        }
        
        db_media = MediaFileUpload(str(self.db_path))
        self.service.files().create(
            body=db_metadata,
            media_body=db_media
        ).execute()
        
        print(f"   [BACKED UP] recipe_library.db")
        
        print("\n" + "=" * 80)
        print(f"[OK] Backup complete: {backup_folder_name}")
        print("=" * 80)


def main():
    """Main menu for Google Drive integration."""
    if not GOOGLE_AVAILABLE:
        print("\n[ERROR] Google Drive libraries not installed")
        print("Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return
    
    try:
        manager = GoogleDriveRecipeManager()
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize: {e}")
        return
    
    while True:
        print("\n" + "=" * 80)
        print("           GOOGLE DRIVE INTEGRATION")
        print("=" * 80)
        print("\n1. Upload all recipes to Google Drive")
        print("2. Sync to Google Drive (upload new/modified)")
        print("3. Sync from Google Drive (download new)")
        print("4. List recipes in Google Drive")
        print("5. Get share link for a recipe")
        print("6. Create full backup")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            manager.upload_all_recipes()
        
        elif choice == '2':
            manager.sync_to_drive()
        
        elif choice == '3':
            manager.sync_from_drive()
        
        elif choice == '4':
            recipes = manager.list_drive_recipes()
            print(f"\n{len(recipes)} recipes in Google Drive:\n")
            for i, recipe in enumerate(recipes, 1):
                size_mb = int(recipe.get('size', 0)) / 1024 / 1024
                print(f"{i}. {recipe['name']} ({size_mb:.2f} MB)")
                print(f"   Link: {recipe['webViewLink']}")
        
        elif choice == '5':
            title = input("\nEnter recipe title: ").strip()
            link = manager.get_share_link(title)
            if link:
                print(f"\n[OK] Share link: {link}")
            else:
                print("\n[ERROR] Recipe not found or not uploaded to Drive")
        
        elif choice == '6':
            manager.create_backup()
        
        elif choice == '7':
            print("\nGoodbye!")
            break
        
        else:
            print("\n[ERROR] Invalid choice")


if __name__ == "__main__":
    main()

