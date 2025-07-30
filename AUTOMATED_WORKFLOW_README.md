# 🤖 Automated Recipe Workflow System

## Overview

The Automated Recipe Workflow System is a powerful addition to your Iterum R&D Chef Notebook that automatically finds, organizes, and uploads recipe files to your backend. This system eliminates manual file processing and provides intelligent categorization and organization.

## 🚀 Quick Start

### Option 1: Use the Startup Script (Recommended)
```bash
python start_automated_workflow.py
```

### Option 2: Manual Start
1. Start your backend server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Open the workflow interface:
   ```
   http://localhost:8000/automated-workflow.html
   ```

## 🎯 What It Does

### 1. **Smart Recipe Detection** 🔍
- Automatically scans folders for recipe files
- Analyzes file content to determine if it's a recipe, menu, or other
- Detects cuisine types (Italian, Mexican, Chinese, etc.)
- Calculates confidence scores for recipe detection
- Supports multiple file formats: Excel, Word, PDF, text files

### 2. **Intelligent Organization** 📁
- Sorts files by category (recipes, menus, uncategorized)
- Organizes recipes by cuisine type
- Creates structured folder hierarchy
- Prevents duplicate files
- Generates detailed analysis reports

### 3. **Seamless Upload** 📤
- Uploads organized recipes to your Iterum app backend
- Handles authentication and error recovery
- Provides real-time progress tracking
- Supports batch operations
- Archives successfully uploaded files

### 4. **Complete Workflow** 🔄
- End-to-end automation from file detection to backend upload
- Progress tracking and status monitoring
- Comprehensive reporting and analytics
- Error handling and recovery
- Cleanup and archiving

## 📋 Prerequisites

### Required Python Packages
```bash
pip install fastapi uvicorn sqlalchemy requests pandas
```

### Optional Packages (for enhanced file support)
```bash
pip install openpyxl python-docx PyPDF2
```

### Folder Structure
Ensure you have these folders in your project:
```
Iterum App/
├── uploads/              # Source folder for recipe files
├── app/
│   ├── routers/         # API endpoints
│   └── services/        # Workflow services
├── sorted_recipes/      # Organized files (created automatically)
└── uploaded_recipes/    # Archived files (created automatically)
```

## 🎛️ How to Use

### 1. **Prepare Your Files**
Place your recipe files in the `uploads/` folder:
```
uploads/
├── recipe1.xlsx
├── recipe2.docx
├── menu.pdf
└── ...
```

### 2. **Access the Workflow Interface**
- Navigate to `http://localhost:8000/automated-workflow.html`
- Or click "🤖 Automated Workflow" in your main navigation

### 3. **Configure Settings**
- **Source Folder**: Where to scan for recipe files (default: `uploads`)
- **Output Folder**: Where to organize files (default: `sorted_recipes`)
- **Backend URL**: Your Iterum app backend (default: `http://localhost:8000`)
- **Authentication**: Optional username/password for secure uploads
- **Archive After Upload**: Whether to move files to archive after upload

### 4. **Run the Workflow**

#### Option A: Complete Workflow
1. Click "🚀 Start Complete Workflow"
2. Monitor progress in real-time
3. View results and reports

#### Option B: Step by Step
1. Click "🔍 Validate Prerequisites" to check everything
2. Click "⚙️ Run Step by Step" for manual control
3. Execute each step individually

### 5. **Monitor Progress**
- Real-time progress bar
- Current step indicator
- Activity log with timestamps
- Status updates and error messages

## 📊 Understanding the Results

### File Analysis
- **Total Files Processed**: Number of files found and analyzed
- **Recipes Found**: Files identified as recipes
- **Menus Found**: Files identified as menus
- **Cuisine Breakdown**: Distribution by cuisine type
- **Confidence Scores**: How certain the system is about categorization

### Upload Results
- **Successfully Uploaded**: Files successfully added to backend
- **Failed Uploads**: Files that couldn't be uploaded
- **Success Rate**: Percentage of successful uploads
- **Performance Metrics**: Processing speed and efficiency

### Reports Generated
- **Organization Report**: Detailed analysis of file categorization
- **Upload Report**: Upload success/failure details
- **Workflow Summary**: Complete workflow statistics
- **Performance Metrics**: Timing and efficiency data

## 🔧 API Endpoints

The workflow system adds these new API endpoints:

### Workflow Management
- `POST /api/workflow/start` - Start complete workflow
- `GET /api/workflow/{id}/status` - Get workflow status
- `GET /api/workflow/list` - List all workflows
- `DELETE /api/workflow/{id}` - Clean up workflow

### Individual Steps
- `POST /api/workflow/find-recipes` - Find and analyze recipe files
- `POST /api/workflow/organize-recipes` - Organize files by category/cuisine
- `POST /api/workflow/upload-recipes` - Upload organized files to backend

### Validation
- `GET /api/workflow/validate` - Validate workflow prerequisites
- `GET /api/workflow/statistics` - Get workflow statistics

## 🎨 Supported File Formats

### Recipe Files
- **Excel**: `.xlsx`, `.xls`, `.csv`
- **Word**: `.docx`, `.doc`
- **PDF**: `.pdf`
- **Text**: `.txt`, `.md`

### Content Analysis
The system analyzes file content to:
- Detect recipe indicators (ingredients, instructions, measurements)
- Identify cuisine types through keyword matching
- Calculate confidence scores for categorization
- Extract metadata (cooking time, servings, difficulty)

## 🏷️ Cuisine Detection

The system automatically detects these cuisine types:
- **Italian**: pasta, pizza, risotto, basil, oregano
- **Mexican**: taco, enchilada, guacamole, cilantro, lime
- **Chinese**: stir-fry, dim sum, soy sauce, ginger
- **Indian**: curry, naan, tandoori, masala, cumin
- **French**: sauce, beurre, roux, herbes, shallot
- **Japanese**: sushi, miso, tempura, wasabi, nori
- **Mediterranean**: olive oil, feta, hummus, oregano
- **American**: burger, barbecue, apple pie, cornbread
- **Thai**: pad thai, tom yum, fish sauce, lemongrass
- **Greek**: moussaka, spanakopita, feta, olive

## 🔍 Recipe Detection Logic

### Recipe Indicators
- **Ingredients**: Lists of ingredients with measurements
- **Instructions**: Step-by-step cooking directions
- **Measurements**: Cups, tablespoons, ounces, etc.
- **Cooking Terms**: Bake, fry, grill, simmer, etc.
- **Preparation**: Chop, dice, mince, slice, etc.

### Confidence Scoring
- **High (0.7+)**: Clear recipe with ingredients and instructions
- **Medium (0.4-0.7)**: Some recipe indicators present
- **Low (<0.4)**: Few recipe indicators, likely not a recipe

## 🛠️ Customization

### Adding New Cuisines
Edit `app/services/recipe_finder.py`:
```python
self.cuisine_types = {
    'your_cuisine': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing cuisines
}
```

### Adjusting Detection Sensitivity
Modify the `calculate_confidence` method in the RecipeFinder class to change how files are scored.

### Adding New File Formats
Update the `recipe_extensions` set and `extract_content_preview` method to support new file types.

## 📈 Performance

### Typical Performance
- **File Processing**: 50-100 files per minute
- **Upload Speed**: 10-20 files per minute (depending on file size)
- **Memory Usage**: Efficient processing with chunked file handling
- **Error Recovery**: Continues processing on individual file failures

### Optimization Tips
- Use SSD storage for faster file access
- Ensure adequate RAM for large file processing
- Close other applications during large workflows
- Use wired network connection for uploads

## 🐛 Troubleshooting

### Common Issues

#### "Backend is not accessible"
- Ensure your FastAPI server is running
- Check that port 8000 is not blocked
- Verify the backend URL in the configuration

#### "No recipe files found"
- Check that files are in the source folder
- Verify file extensions are supported
- Ensure files are not corrupted or password-protected

#### "Upload failed"
- Check authentication credentials
- Verify backend API endpoints are working
- Check file size limits
- Review error logs for specific issues

#### "Permission denied"
- Ensure write permissions for output folders
- Check that the app can create directories
- Run as administrator if needed (Windows)

### Debug Mode
Enable detailed logging by setting the log level:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Error Logs
Check these log files for detailed error information:
- `recipe_finder.log` - Recipe detection errors
- `recipe_uploader.log` - Upload errors
- `workflow.log` - General workflow errors

## 🔒 Security

### Authentication
- Optional username/password authentication
- Secure token-based authentication
- Session management for workflow tracking

### File Safety
- Original files are never modified
- Files are copied, not moved (until archiving)
- Hash-based duplicate detection
- Safe file handling with error recovery

### Data Privacy
- No external data transmission
- All processing happens locally
- Secure API communication with backend
- Optional data encryption for sensitive files

## 📚 Integration

### With Existing Iterum App
- Seamlessly integrates with your current recipe system
- Uses existing API endpoints for uploads
- Maintains user authentication and permissions
- Preserves existing data structure

### With Other Systems
- Export reports in JSON/CSV format
- RESTful API for external integration
- Webhook support for notifications
- Standard file formats for compatibility

## 🚀 Future Enhancements

### Planned Features
- **Machine Learning**: Improved recipe detection with ML models
- **Image Analysis**: Extract recipes from photos
- **Cloud Integration**: Upload to cloud storage services
- **Batch Scheduling**: Automated workflow scheduling
- **Advanced Analytics**: Detailed usage and performance analytics

### Extensibility
The system is designed to be easily extensible:
- Modular service architecture
- Plugin system for custom processors
- Configurable detection rules
- Custom report generators

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. Review error logs for specific issues
3. Validate prerequisites before running workflows
4. Test with a small number of files first

### Reporting Issues
When reporting issues, please include:
- Error messages and logs
- File types and sizes
- System configuration
- Steps to reproduce the issue

### Contributing
The automated workflow system is designed to be extensible. Contributions are welcome for:
- New file format support
- Additional cuisine detection
- Performance improvements
- Bug fixes and enhancements

---

## 🎉 Ready to Get Started?

Your automated recipe workflow system is now ready to use! Start by running the startup script and exploring the workflow interface. The system will help you process hundreds of recipe files automatically, saving you hours of manual work.

**Happy cooking! 🍳** 