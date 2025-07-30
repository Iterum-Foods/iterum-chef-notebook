# Automated Recipe Upload System

## Overview

The Automated Recipe Upload System provides a complete workflow for automatically importing recipes from files and managing them through a review process. This system includes:

1. **Folder Watcher**: Automatically detects and uploads new recipe files
2. **Review Queue**: Manages newly uploaded recipes that need review
3. **Batch Operations**: Approve or reject multiple recipes at once

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend
```bash
python run.py
```

### 3. Start the Folder Watcher
```bash
python start_folder_watcher.py
```

### 4. Add Recipe Files
Simply drag and drop recipe files into the `incoming_recipes/` folder, and they'll be automatically uploaded!

## 📁 Folder Structure

```
Iterum App/
├── incoming_recipes/          # Drop recipe files here
│   ├── archive/              # Processed files are moved here
│   ├── recipe1.txt
│   ├── recipe2.pdf
│   └── recipe3.docx
├── recipe_folder_watcher.py  # Main watcher script
├── start_folder_watcher.py   # Startup script
└── recipe_watcher.log        # Log file
```

## 🔄 How It Works

### 1. File Detection
- The folder watcher monitors the `incoming_recipes/` folder
- When new files are added (via drag & drop, copy, or save), they're automatically detected
- Supported formats: `.pdf`, `.txt`, `.docx`, `.doc`, `.xlsx`, `.xls`, `.csv`

### 2. Automatic Upload
- Each detected file is uploaded to the backend via the `/api/recipes/bulk-upload` endpoint
- Files are processed with default settings:
  - Category: "Imported"
  - Cuisine: "Unknown"
  - Servings: 4
  - Auto-tag: "Imported"

### 3. File Archiving
- After successful upload, files are moved to `incoming_recipes/archive/`
- Archive files are timestamped to prevent conflicts
- Failed uploads remain in the original location for manual review

### 4. Review Process
- Newly uploaded recipes appear in the "Pending Review" queue
- Reviewers can approve or reject recipes individually or in batches
- Approved recipes become available in the main recipe library
- Rejected recipes are marked but remain accessible for reference

## 🎯 Review Workflow

### Accessing the Review Queue
1. Open the Recipe Library section
2. Click the "🔍 Pending Review" button
3. The review modal will open showing all pending recipes

### Review Options

#### Individual Review
- **Approve**: Click "✅ Approve" on any recipe card
- **Reject**: Click "❌ Reject" on any recipe card
- **Add Notes**: Optional review notes can be added

#### Batch Review
- **Select All**: Click "Select All" to select all pending recipes
- **Select Specific**: Check individual recipe checkboxes
- **Approve Selected**: Click "✅ Approve Selected" to approve multiple recipes
- **Reject Selected**: Click "❌ Reject Selected" to reject multiple recipes

### Review Actions
- **Approve**: Recipe moves to main library as "draft" status
- **Reject**: Recipe remains in system but marked as rejected
- **Notes**: Review notes are added to recipe description

## 📊 Monitoring and Logs

### Log File
The system creates `recipe_watcher.log` with detailed information:
```
2024-01-15 10:30:15 - INFO - Starting Recipe Folder Watcher...
2024-01-15 10:30:15 - INFO - Watching folder: C:\Users\chefm\my-culinary-app\Iterum App\incoming_recipes
2024-01-15 10:35:22 - INFO - New recipe file detected: chocolate_cake.txt
2024-01-15 10:35:23 - INFO - Uploading chocolate_cake.txt to backend...
2024-01-15 10:35:25 - INFO - Upload successful: 1 recipes imported
2024-01-15 10:35:25 - INFO - Successfully processed: chocolate_cake.txt
```

### Console Output
Real-time status updates in the terminal:
```
🍳 Recipe Folder Watcher Startup
==============================
✅ All dependencies are installed
✅ Created folder: incoming_recipes
✅ Created folder: incoming_recipes/archive
✅ Backend is running

🚀 Starting Recipe Folder Watcher...
==================================================
File watcher is running. Press Ctrl+C to stop.
```

## ⚙️ Configuration

### Backend URL
Edit `recipe_folder_watcher.py` to change the backend URL:
```python
BACKEND_URL = "http://localhost:8000/api/recipes/bulk-upload"
```

### Watch Folder
Change the folder to monitor:
```python
WATCH_FOLDER = "incoming_recipes"  # Change this path
```

### Supported File Types
Add or remove supported file extensions:
```python
SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.doc', '.xlsx', '.xls', '.csv'}
```

### Upload Settings
Modify default upload parameters:
```python
data = {
    'default_category': 'Imported',
    'default_cuisine': 'Unknown',
    'default_servings': '4',
    'auto_tag': 'true'
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend Not Running
**Error**: "Backend is not running"
**Solution**: Start the backend with `python run.py`

#### 2. Missing Dependencies
**Error**: "Missing dependency: watchdog"
**Solution**: Run `pip install -r requirements.txt`

#### 3. Permission Issues
**Error**: "Permission denied" when creating folders
**Solution**: Run as administrator or check folder permissions

#### 4. Upload Failures
**Error**: "Upload failed with status 500"
**Solution**: Check backend logs and ensure database is accessible

### Debug Mode
Enable detailed logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Manual Upload
If automatic upload fails, you can manually upload files:
1. Use the bulk upload modal in the web interface
2. Or use the backend API directly with curl/Postman

## 📈 Performance Tips

### Large File Collections
- Process files in smaller batches (50-100 files at a time)
- Monitor system resources during large uploads
- Use SSD storage for better performance

### Network Optimization
- Ensure stable internet connection for uploads
- Consider local backend for faster processing
- Monitor upload speeds and adjust timeouts if needed

### Storage Management
- Regularly clean up the archive folder
- Monitor disk space usage
- Consider compression for large recipe collections

## 🔒 Security Considerations

### File Validation
- Only supported file types are processed
- Files are scanned for basic format validation
- Large files are rejected to prevent DoS attacks

### Access Control
- Only authenticated users can upload recipes
- User-specific recipe isolation
- Review permissions based on user roles

### Data Protection
- Files are moved to archive after processing
- No sensitive data is stored in plain text
- Logs don't contain recipe content

## 🚀 Advanced Features

### Custom File Processors
Add support for new file formats by extending the parsing functions:
```python
def parse_custom_format(file_path):
    # Add your custom parsing logic here
    pass
```

### Integration with External Sources
Connect to recipe websites or APIs:
```python
def import_from_website(url):
    # Add web scraping logic here
    pass
```

### Automated Categorization
Use AI/ML to automatically categorize recipes:
```python
def auto_categorize_recipe(recipe_data):
    # Add categorization logic here
    pass
```

## 📞 Support

For technical support or feature requests:
1. Check the log files for error details
2. Review the troubleshooting section
3. Contact the development team with specific error messages

---

*This automated upload system provides a seamless workflow for importing large recipe collections while maintaining quality control through the review process.* 