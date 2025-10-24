# Recipe and Menu Finder

A powerful Python program that automatically scans folders for food recipes and menus, analyzes their content, categorizes them, and sorts them by various criteria.

## Features

- 🔍 **Smart File Detection**: Automatically identifies recipe and menu files using content analysis
- 📁 **Multiple File Formats**: Supports Excel (.xlsx, .xls), Word (.docx, .doc), PDF, text files, and more
- 🏷️ **Intelligent Categorization**: Distinguishes between recipes, menus, and other files
- 🌍 **Cuisine Recognition**: Automatically detects cuisine types (Italian, Mexican, Chinese, etc.)
- 📊 **Comprehensive Analysis**: Extracts cooking time, servings, difficulty level, and tags
- 📂 **Organized Output**: Sorts and organizes files into structured folders
- 📄 **Detailed Reports**: Generates JSON reports and CSV exports
- 🎯 **Confidence Scoring**: Uses AI-like analysis to determine how likely a file is to be a recipe

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_recipe_finder.txt
```

### 2. Run the Program

#### Option A: Simple Interactive Mode
```bash
python run_recipe_finder.py
```

#### Option B: Command Line Interface
```bash
python recipe_menu_finder.py "path/to/your/folder" --output "sorted_recipes" --copy --report --csv
```

### 3. View Results

The program will create a `sorted_recipes` folder with:
- Organized subfolders by category and cuisine
- Detailed JSON report
- CSV inventory file
- Log file with processing details

## How It Works

### File Detection
The program scans for files with these extensions:
- `.xlsx`, `.xls`, `.csv` (Excel/CSV files)
- `.docx`, `.doc` (Word documents)
- `.pdf` (PDF files)
- `.txt`, `.md` (Text files)
- `.json` (JSON files)
- `.html`, `.htm` (Web pages)

### Content Analysis
For each file, the program:
1. Extracts a content preview
2. Searches for recipe-related keywords
3. Identifies cuisine-specific terms
4. Detects cooking instructions and ingredients
5. Calculates a confidence score

### Categorization
Files are categorized as:
- **Recipe**: Contains ingredients and cooking instructions
- **Menu**: Contains meal planning or restaurant menus
- **Uncategorized**: Doesn't clearly fit either category

### Cuisine Detection
Automatically detects these cuisines:
- Italian, Mexican, Chinese, Indian, French
- Japanese, Mediterranean, American, Thai, Greek

## Command Line Options

```bash
python recipe_menu_finder.py [source_folder] [options]

Options:
  --output, -o FOLDER     Output folder for organized files (default: sorted_recipes)
  --sort-by, -s CRITERIA  Sort criteria: name, date_modified, date_created, size, confidence, cuisine, category
  --copy, -c              Copy files to organized folders
  --report, -r            Generate detailed JSON report
  --csv                   Export to CSV format
```

## Examples

### Basic Scan
```bash
python recipe_menu_finder.py "My Recipes"
```

### Full Analysis with Organization
```bash
python recipe_menu_finder.py "My Recipes" --output "Organized Recipes" --copy --report --csv
```

### Sort by Date Modified
```bash
python recipe_menu_finder.py "My Recipes" --sort-by date_modified
```

## Output Structure

```
sorted_recipes/
├── recipes/
│   ├── italian/
│   ├── mexican/
│   ├── chinese/
│   └── ...
├── menus/
├── uncategorized/
├── recipe_analysis_report.json
├── recipe_inventory.csv
└── recipe_finder.log
```

## File Analysis Details

### Confidence Scoring
The program uses a sophisticated scoring system:
- Recipe keywords: +0.1 each
- Menu keywords: +0.15 each
- Ingredients + Instructions: +0.3 bonus
- Cooking terms: +0.05 each
- Maximum score: 1.0

### Extracted Metadata
For each file, the program extracts:
- File information (name, size, dates)
- Category (recipe/menu/uncategorized)
- Cuisine type
- Difficulty level
- Cooking time
- Number of servings
- Relevant tags
- Confidence score

## Integration with Your Existing App

This program is designed to work with your existing culinary app structure:

- **Source Folder**: Points to your existing `Iterum App/uploads` folder
- **Compatible Formats**: Works with your existing Excel recipe files
- **Output Structure**: Creates organized folders that can be imported into your app
- **Reports**: Generates data that can be used to populate your recipe database

## Customization

### Adding New Cuisines
Edit the `cuisine_types` dictionary in `recipe_menu_finder.py`:

```python
self.cuisine_types = {
    'your_cuisine': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing cuisines
}
```

### Adjusting Confidence Scoring
Modify the `calculate_confidence` method to change how files are scored.

### Adding New File Formats
Update the `recipe_extensions` set and `extract_content_preview` method.

## Troubleshooting

### Common Issues

1. **No files found**: Check that the source folder exists and contains supported file types
2. **Permission errors**: Ensure you have read/write permissions for the folders
3. **Missing dependencies**: Install all required packages from `requirements_recipe_finder.txt`

### Log Files
Check `recipe_finder.log` for detailed processing information and error messages.

## Advanced Usage

### Programmatic Usage
```python
from recipe_menu_finder import RecipeMenuFinder

# Initialize finder
finder = RecipeMenuFinder("path/to/folder", "output/folder")

# Scan for files
files = finder.scan_folder()

# Sort by confidence
sorted_files = finder.sort_files('confidence')

# Organize files
finder.organize_files(copy_files=True)

# Generate report
finder.generate_report()
```

### Batch Processing
```python
# Process multiple folders
folders = ["folder1", "folder2", "folder3"]
for folder in folders:
    finder = RecipeMenuFinder(folder, f"output_{folder}")
    finder.scan_folder()
    finder.organize_files()
```

## Performance Tips

- For large folders, the program processes files efficiently
- Excel files are read in chunks to handle large files
- The program skips files larger than 50MB to avoid memory issues
- Processing is logged for debugging and monitoring

## Future Enhancements

Potential improvements:
- Machine learning for better recipe detection
- Image analysis for recipe photos
- Integration with recipe APIs
- Web interface for file management
- Real-time folder monitoring
- Recipe data extraction and parsing

## Support

For issues or questions:
1. Check the log file for error details
2. Verify all dependencies are installed
3. Ensure file permissions are correct
4. Test with a small folder first

---

**Happy Recipe Organizing! 🍳📁** 