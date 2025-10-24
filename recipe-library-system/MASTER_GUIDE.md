# 🍳 Complete Recipe Management System
## From Scattered Files to Professional Iterum Format

---

## 🎯 What This System Does

This is a **complete professional recipe management system** that:

1. **📂 ORGANIZES** - Consolidates scattered recipes into one library
2. **🔍 TRACKS** - Remembers where each recipe came from (restaurant/project/date)
3. **📊 CONVERTS** - Standardizes everything to Iterum format for costing
4. **💰 ENABLES** - Professional recipe costing and menu planning

---

## 🚀 Quick Start (30 seconds)

### Want to do EVERYTHING at once?

**Double-click:** `FULL_WORKFLOW.bat`

This will:
1. Ask for your recipe folder
2. Organize all recipes into library
3. Convert to Iterum format
4. Done!

---

## 📋 Available Tools

### 1. **organize_recipes.py** - Consolidate Recipes
```powershell
py organize_recipes.py "C:\Your\Recipe\Folder"
```

**What it does:**
- Scans any folder for recipe files
- Copies or moves them to organized library
- Prevents duplicates with hash-based naming
- Stores metadata in SQLite database

**Two modes:**
- COPY mode (safe - keeps originals)
- MOVE mode (consolidates - removes originals)

📖 [Full Guide](organize_recipes.py)

---

### 2. **track_recipe_sources.py** - Track Origins
```powershell
py track_recipe_sources.py
```

**What it does:**
- Shows where each recipe came from
- Search by date (year/month)
- Search by location (restaurant/project)
- Export source reports

**Use cases:**
- "Show me all recipes from Italian Restaurant"
- "What recipes did we create in July 2025?"
- "Where did this recipe come from originally?"

📖 [Full Guide](HOW_TO_TRACK_SOURCES.md)

---

### 3. **standardize_recipes.py** - Convert to Iterum Format
```powershell
py standardize_recipes.py --auto
```

**What it does:**
- Converts ALL recipes to uniform Iterum format
- Professional costing layout
- AP/EP cost tracking
- Yield management
- Ready for Iterum Chef's Notebook upload

**Output:**
- Professional Excel files in `converted_iterum/`
- All with same format
- Ready for costing and upload

📖 [Full Guide](CONVERT_TO_ITERUM.md)

---

### 4. **scan_any_folder.py** - Import from Anywhere
```powershell
py scan_any_folder.py "C:\Any\Folder\Path"
```

**What it does:**
- Scans any folder for recipe-like files
- Smart content detection
- Imports to library
- Shows summary of what was found

---

### 5. **run_library.py** - Interactive Recipe Browser
```powershell
py run_library.py
```

**What it does:**
- Interactive menu for browsing recipes
- Search by cuisine, category, difficulty
- View library statistics
- Export library data

---

### 6. **recipe_dashboard.py** - GUI Dashboard
```powershell
py recipe_dashboard.py
```

**What it does:**
- Graphical interface
- Search recipes
- Merge recipes into folders
- Convert recipes

---

## 🎬 Complete Workflow Examples

### Example 1: New Restaurant Project

**Scenario:** You're developing a menu for a new Italian restaurant

```powershell
# Step 1: Collect test recipes into folder
C:\Projects\Mario's Italian\
├── pasta_carbonara.xlsx
├── margherita_pizza.docx
├── tiramisu.pdf
└── bruschetta.txt

# Step 2: Organize into library
py organize_recipes.py "C:\Projects\Mario's Italian"
# Result: 4 recipes imported to library

# Step 3: Convert to Iterum format
py standardize_recipes.py --auto
# Result: 4 standardized Excel files ready for costing

# Step 4: Cost the recipes
# Open files in converted_iterum/
# Fill in ingredient costs, yields

# Step 5: Upload to Iterum
# Batch upload to Chef's Notebook
# Use for menu planning
```

**Later, track the source:**
```powershell
py track_recipe_sources.py location "Mario's Italian"
# Shows all 4 recipes from that project
```

---

### Example 2: Multiple Projects Over Time

**Scenario:** You've been collecting recipes from different sources

```powershell
# Your scattered recipes:
C:\Desktop\Recipes\          (15 files)
C:\Documents\Italian Menu\   (8 files)
C:\Projects\Summer 2025\     (12 files)
D:\Backup\Old Recipes\       (25 files)

# Organize them all:
py organize_recipes.py "C:\Desktop\Recipes"
py organize_recipes.py "C:\Documents\Italian Menu"
py organize_recipes.py "C:\Projects\Summer 2025"
py organize_recipes.py "D:\Backup\Old Recipes"

# Result: 60 recipes in organized library

# Convert all to Iterum format:
py standardize_recipes.py --auto

# Result: 60 professional Excel files ready for costing
```

**Track sources later:**
```powershell
# See all sources
py track_recipe_sources.py sources

# Find specific project
py track_recipe_sources.py location "Summer 2025"

# Find by date
py track_recipe_sources.py date 2025 6
```

---

### Example 3: Daily Workflow

**Morning: Import new test recipes**
```powershell
py scan_any_folder.py "C:\TestRecipes"
```

**Afternoon: Convert for costing**
```powershell
py standardize_recipes.py --auto
```

**Evening: Cost and upload**
- Open files in `converted_iterum/`
- Fill in costs
- Upload to Iterum Chef's Notebook

---

## 📁 Directory Structure

After using the system:

```
recipe-library-system/
├── recipe_library/                    ← Organized recipes (hash-based names)
│   ├── recipe_library.db             ← SQLite database with metadata
│   ├── 2a6f1916...xlsx              ← Recipe files
│   ├── 38a10bd9...xlsx
│   └── ...
│
├── converted_iterum/                  ← Standardized Iterum format
│   ├── Caramelized Onions.xlsx      ← Ready for costing
│   ├── Chicken Salad.xlsx
│   └── ...
│
├── organize_recipes.py                ← Consolidate recipes
├── track_recipe_sources.py            ← Track origins
├── standardize_recipes.py             ← Convert to Iterum
├── scan_any_folder.py                 ← Import from anywhere
├── run_library.py                     ← Interactive browser
├── recipe_dashboard.py                ← GUI dashboard
│
├── FULL_WORKFLOW.bat                  ← Do everything at once
├── organize_recipes.bat               ← Quick organize
├── standardize_recipes.bat            ← Quick convert
├── track_sources.bat                  ← Quick track
│
└── Documentation/
    ├── MASTER_GUIDE.md               ← This file
    ├── CONVERT_TO_ITERUM.md          ← Conversion guide
    ├── HOW_TO_TRACK_SOURCES.md       ← Tracking guide
    └── RECIPE_LIBRARY_README.md      ← System overview
```

---

## 🎯 Key Features

### 1. Smart Organization
- ✅ Hash-based file naming (no duplicates)
- ✅ Flat structure (no complex folders)
- ✅ SQLite database for metadata
- ✅ Preserves original file information

### 2. Source Tracking
- ✅ Remembers original file path
- ✅ Tracks creation and modification dates
- ✅ Extracts project/restaurant names from paths
- ✅ Search by date or location

### 3. Format Standardization
- ✅ Converts to professional Iterum format
- ✅ Uniform layout for all recipes
- ✅ Ready for recipe costing
- ✅ Compatible with Iterum Chef's Notebook

### 4. Professional Costing
- ✅ AP/EP cost tracking
- ✅ Yield percentage management
- ✅ Portion costing
- ✅ Food cost percentage calculation

---

## 💡 Best Practices

### 1. Organize Before Converting
```powershell
# Always organize first
py organize_recipes.py "Your Folder"

# Then convert
py standardize_recipes.py --auto
```

This ensures all metadata is captured before conversion.

### 2. Use Meaningful Folder Names
```powershell
# ✓ Good
C:\Projects\Mario's Italian Restaurant\
C:\TestKitchen\Summer Menu 2025\

# ✗ Bad
C:\Desktop\New Folder\
C:\Temp\
```

Folder names become source tracking labels.

### 3. Use COPY Mode First
When organizing, start with COPY mode to preserve originals until you're confident.

### 4. Regular Source Reports
```powershell
# Monthly: Export source report
py track_recipe_sources.py
# Choose: 5. Export source report
```

Keep records of where recipes came from.

### 5. Update Costs Regularly
- Review ingredient costs quarterly
- Update AP$ in Iterum files
- Recalculate menu pricing

---

## 🔄 Recommended Workflow

### Initial Setup (One Time)
```powershell
1. Install dependencies
   pip install -r requirements_recipe_finder.txt

2. Test with small folder
   py organize_recipes.py "C:\TestFolder"

3. Verify results
   py run_library.py

4. Convert to Iterum
   py standardize_recipes.py --auto
```

### Daily Use
```powershell
1. Import new recipes
   py scan_any_folder.py "Today's Folder"

2. Convert to Iterum
   py standardize_recipes.py --auto

3. Cost recipes
   (Open Excel files, fill costs)

4. Upload to Iterum
   (Batch upload to Chef's Notebook)
```

### Weekly Review
```powershell
1. Check library stats
   py run_library.py
   # Choose: 6. Show library statistics

2. Review sources
   py track_recipe_sources.py sources

3. Export backup
   py run_library.py
   # Choose: 7. Export library
```

---

## 📊 System Capabilities

### Supported File Formats
- Excel: `.xlsx`, `.xls`, `.csv`
- Word: `.docx`, `.doc`
- PDF: `.pdf`
- Text: `.txt`, `.md`
- Web: `.html`, `.htm`
- Data: `.json`

### Smart Detection
- Automatically identifies recipe files
- Extracts cuisine types
- Detects difficulty levels
- Finds cooking times and servings
- Confidence scoring

### Metadata Tracking
- File name and path
- Creation and modification dates
- Cuisine type
- Category (recipe/menu)
- Difficulty level
- Tags and labels
- Confidence score

---

## 🎓 Training & Support

### Learning Path

**Level 1: Basics**
1. Organize a small folder
2. Browse with interactive menu
3. View library statistics

**Level 2: Intermediate**
1. Track recipe sources
2. Search by date and location
3. Export reports

**Level 3: Advanced**
1. Convert to Iterum format
2. Fill in costing data
3. Upload to Chef's Notebook
4. Menu planning and pricing

---

## 🆘 Troubleshooting

### Issue: No recipes found
**Solution:** Check file formats are supported

### Issue: Cuisine detection wrong
**Solution:** Edit metadata in database or Excel file

### Issue: Conversion errors
**Solution:** Check log files, manually verify problem recipes

### Issue: Upload to Iterum fails
**Solution:** Verify format matches Iterum requirements exactly

---

## 🎉 Success Metrics

After using this system, you'll have:

✅ **Organized Library**
- All recipes in one location
- No duplicates
- Easy to find anything

✅ **Source Tracking**
- Know where every recipe came from
- Track development over time
- Generate source reports

✅ **Professional Format**
- Uniform Iterum layout
- Ready for costing
- Upload-ready for Chef's Notebook

✅ **Cost Control**
- Accurate recipe costs
- Portion control
- Menu pricing optimization

---

## 📞 Quick Reference

### Most Common Commands

```powershell
# Organize folder
py organize_recipes.py "FolderPath"

# Convert to Iterum
py standardize_recipes.py --auto

# Track sources
py track_recipe_sources.py

# Browse library
py run_library.py

# Complete workflow
FULL_WORKFLOW.bat
```

---

## 🔮 Future Enhancements

Potential additions:
- Nutritional data extraction
- Image support for recipe photos
- Cloud sync capabilities
- Mobile app integration
- Recipe sharing network
- Automatic vendor pricing integration

---

## 📚 Additional Documentation

- **System Overview**: `RECIPE_LIBRARY_README.md`
- **Conversion Guide**: `CONVERT_TO_ITERUM.md`
- **Source Tracking**: `HOW_TO_TRACK_SOURCES.md`
- **Recipe Finder**: `README_Recipe_Finder.md`
- **Converter Info**: `README_CONVERTER.txt`

---

## ✨ Summary

You now have a **complete professional recipe management system** that:

1. **Organizes** scattered recipes into one library
2. **Tracks** where every recipe came from
3. **Converts** to standardized Iterum format
4. **Enables** professional recipe costing
5. **Prepares** for upload to Chef's Notebook

### Start Now:

```powershell
FULL_WORKFLOW.bat
```

**That's it! You're ready to manage recipes like a pro! 🎉**

---

*Last Updated: October 20, 2025*  
*Version: 1.0*  
*System: Recipe Management & Iterum Conversion*

