# Recipe Library System

A library-style system for organizing recipes using metadata and tags instead of folder structures.

## 🎯 What This System Does

Instead of organizing recipes into folders, this system:
- **Stores all recipes in one location** with hash-based naming
- **Uses a database** to store metadata and relationships
- **Organizes by tags and metadata** (cuisine, difficulty, category, etc.)
- **Provides powerful search and filtering** capabilities
- **Maintains file integrity** with hash-based file management

## 📁 System Structure

```
recipe_library/
├── recipe_library.db          # SQLite database with metadata
├── metadata.json              # Library metadata
├── index.json                 # Search index
├── [hash1].xlsx               # Recipe files (hash-based naming)
├── [hash2].docx
├── [hash3].pdf
└── ...
```

## 🚀 Quick Start

### Option 1: Interactive Interface (Recommended)
```bash
# Windows
double-click recipe_library.bat

# Or command line
python run_library.py
```

### Option 2: Command Line
```bash
# Scan and import recipes
python recipe_library_system.py --scan

# Search recipes
python recipe_library_system.py --search "chicken"

# Filter by cuisine
python recipe_library_system.py --cuisine italian

# Show statistics
python recipe_library_system.py --stats

# Export library
python recipe_library_system.py --export
```

## 🔍 Key Features

### 📚 Library-Style Organization
- **Single Location**: All recipes stored in one folder
- **Hash-Based Naming**: Files named by content hash to prevent duplicates
- **Database Metadata**: All organization info stored in SQLite database
- **No Folder Structure**: Clean, flat file organization

### 🏷️ Smart Metadata
- **Automatic Detection**: Cuisine, difficulty, cooking time, servings
- **Tag System**: Flexible tagging for ingredients, meal types, dietary restrictions
- **Content Analysis**: Extracts metadata from file content and filenames
- **Confidence Scoring**: Rates how likely a file is to be a recipe

### 🔍 Powerful Search
- **Text Search**: Search by title and content
- **Filter by Cuisine**: Italian, Mexican, Chinese, etc.
- **Filter by Category**: Recipe, menu, uncategorized
- **Filter by Difficulty**: Easy, medium, hard
- **Tag Filtering**: Find recipes with specific tags
- **Combined Filters**: Mix multiple search criteria

### 📊 Comprehensive Statistics
- **Library Overview**: Total recipes, categories, cuisines
- **Popular Tags**: Most common tags in your library
- **Upload Status**: Track which recipes have been uploaded
- **Trends**: See patterns in your recipe collection

## 🎛️ How It Works

### 1. File Import Process
1. **Scan Source**: Scans your uploads folder for recipe files
2. **Content Analysis**: Analyzes file content for recipe indicators
3. **Metadata Extraction**: Extracts cuisine, difficulty, tags, etc.
4. **Hash Generation**: Creates unique hash for file identification
5. **Copy to Library**: Copies file to library with hash-based name
6. **Database Storage**: Stores all metadata in SQLite database

### 2. Search and Organization
1. **Query Database**: Searches metadata stored in database
2. **Filter Results**: Applies multiple filter criteria
3. **Rank Results**: Orders by confidence score and relevance
4. **Return Metadata**: Returns recipe information and file locations

### 3. File Management
- **No Duplicates**: Hash-based naming prevents duplicate files
- **File Integrity**: Original files remain untouched
- **Easy Backup**: Single folder to backup entire library
- **Version Control**: Can track changes through database

## 📋 Supported File Formats

- **Excel**: `.xlsx`, `.xls`, `.csv`
- **Word**: `.docx`, `.doc`
- **PDF**: `.pdf`
- **Text**: `.txt`, `.md`
- **Web**: `.html`, `.htm`
- **Data**: `.json`

## 🏷️ Metadata Categories

### Cuisine Types
- Italian, Mexican, Chinese, Indian, French
- Japanese, Mediterranean, American, Thai, Greek

### Categories
- **Recipe**: Contains ingredients and cooking instructions
- **Menu**: Meal planning or restaurant menus
- **Uncategorized**: Doesn't clearly fit either category

### Difficulty Levels
- **Easy**: Simple, quick, basic recipes
- **Medium**: Moderate complexity
- **Hard**: Advanced, complex recipes

### Tags
- **Meal Types**: Breakfast, lunch, dinner, dessert, snack
- **Dietary**: Vegetarian, vegan, gluten-free, dairy-free
- **Flavors**: Spicy, sweet, savory
- **Ingredients**: Based on detected ingredients

## 🔍 Search Examples

### Basic Search
```bash
# Search for chicken recipes
python recipe_library_system.py --search "chicken"

# Search for Italian recipes
python recipe_library_system.py --cuisine italian

# Search for easy recipes
python recipe_library_system.py --difficulty easy
```

### Advanced Search
```python
# Search with multiple criteria
recipes = library.search_recipes(
    cuisine="italian",
    difficulty="easy",
    tags=["vegetarian", "dinner"],
    search_text="pasta"
)
```

### Interactive Search
```bash
python run_library.py
# Choose option 2 (Search recipes)
# Enter search terms
```

## 📊 Library Statistics

### View Statistics
```bash
python recipe_library_system.py --stats
```

### Sample Output
```
📊 Library Statistics:
Total recipes: 45

By category:
  Recipe: 38
  Menu: 5
  Uncategorized: 2

By cuisine:
  Italian: 12
  Mediterranean: 8
  Mexican: 6
  American: 5
  Chinese: 4

By difficulty:
  Easy: 15
  Medium: 20
  Hard: 10

Popular tags:
  dinner: 25
  vegetarian: 8
  spicy: 6
  dessert: 5
```

## 📄 Export and Backup

### Export Library
```bash
python recipe_library_system.py --export
```

### Export Format
```json
{
  "export_date": "2025-07-12T15:30:00",
  "total_recipes": 45,
  "library_path": "recipe_library",
  "recipes": [
    {
      "id": "abc123...",
      "title": "Chicken Pasta",
      "cuisine_type": "italian",
      "difficulty": "medium",
      "tags": ["dinner", "pasta", "chicken"],
      "file_path": "recipe_library/abc123.xlsx"
    }
  ]
}
```

## 🛠️ Customization

### Adding New Cuisines
Edit `recipe_library_system.py`:
```python
self.cuisine_types = {
    'your_cuisine': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing cuisines
}
```

### Adding New Tags
Modify the `extract_tags` method to detect new tag types.

### Adjusting Confidence Scoring
Modify the `calculate_confidence` method to change detection sensitivity.

## 🔒 File Management

### File Storage
- **Original Files**: Remain in source location unchanged
- **Library Files**: Copied to library with hash-based names
- **Database**: Stores relationships between original and library files

### Backup Strategy
- **Library Folder**: Single folder to backup all recipes
- **Database**: Backup `recipe_library.db` for metadata
- **Export**: Regular JSON exports for portability

## 📈 Performance

- **Fast Search**: SQLite database for quick queries
- **Efficient Storage**: Hash-based deduplication
- **Scalable**: Handles thousands of recipes efficiently
- **Memory Efficient**: Processes files in chunks

## 🔍 Troubleshooting

### Common Issues

1. **No Recipes Found**
   ```
   Solution: Check source folder path and file formats
   ```

2. **Database Errors**
   ```
   Solution: Delete recipe_library.db to recreate
   ```

3. **Missing Dependencies**
   ```
   Solution: pip install pandas sqlite3
   ```

### Log Files
- `recipe_library.log` - Detailed operation logs
- Check for error details and processing information

## 🚀 Future Enhancements

Potential improvements:
- **Web Interface**: Browser-based library management
- **Recipe Parsing**: Extract ingredients and instructions
- **Image Support**: Recipe photo management
- **Cloud Sync**: Sync library across devices
- **Recipe Sharing**: Export/import recipe collections
- **Nutrition Data**: Automatic nutrition calculation

## 📝 Usage Examples

### Basic Workflow
```bash
# 1. Start the library system
python run_library.py

# 2. Scan and import recipes
# Choose option 1

# 3. Browse your recipes
# Choose options 3-5 for different views

# 4. Search for specific recipes
# Choose option 2
```

### Advanced Usage
```python
from recipe_library_system import RecipeLibrary

# Initialize library
library = RecipeLibrary()

# Import recipes
recipes = library.scan_and_import()

# Search with filters
italian_recipes = library.search_recipes(
    cuisine="italian",
    difficulty="easy",
    tags=["dinner"]
)

# Get statistics
stats = library.get_library_stats()
print(f"Total recipes: {stats['total_recipes']}")

# Export library
export_path = library.export_library()
```

---

## 🎉 Ready to Use!

Your recipe library system is ready to organize recipes without folder structures. The system provides:

- **Clean organization** without complex folder hierarchies
- **Powerful search** and filtering capabilities
- **Flexible metadata** and tagging system
- **Easy backup** and export options
- **Scalable architecture** for growing collections

**Start with `recipe_library.bat` or `python run_library.py` to get started!**

---

**Happy Recipe Organizing! 📚🍳** 