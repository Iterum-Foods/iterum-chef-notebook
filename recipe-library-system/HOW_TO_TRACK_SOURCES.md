# 🔍 Track Recipe Sources by Date and Location

## What This Does

The Recipe Source Tracker lets you find recipes based on:
- **📅 Date** - When they were created or modified
- **📍 Location** - Where they came from (folder path)
- **🏢 Project/Restaurant** - Automatically extracts project names from folder paths

This is perfect for tracking:
- Recipes from specific restaurants
- Recipes from different projects or clients
- Recipes from specific time periods
- Original file locations before they were organized

---

## 🎯 Quick Start

### Option 1: Interactive Menu (Easiest!)
```powershell
# Double-click this file:
track_sources.bat

# Or run:
py track_recipe_sources.py
```

### Option 2: Command Line
```powershell
# View all source locations
py track_recipe_sources.py sources

# Search by date (year and month)
py track_recipe_sources.py date 2025 7

# Search by location
py track_recipe_sources.py location "Italian Restaurant"
```

---

## 📊 What Data is Tracked

For every recipe, the system stores:

```
✓ Original File Path    C:\Projects\Italian Restaurant\pasta.xlsx
✓ Created Date          2025-03-15
✓ Modified Date         2025-07-12
✓ Original Filename     pasta.xlsx
✓ Source Folder         Italian Restaurant
```

---

## 🔍 Use Cases

### Use Case 1: Find All Recipes from a Restaurant

**Example:** You tested recipes at "Mario's Italian" in June 2025

```powershell
# Interactive way:
py track_recipe_sources.py
# Choose: 2. View recipes from specific location
# Enter: Mario's Italian

# Command line way:
py track_recipe_sources.py location "Mario's Italian"
```

**Result:**
```
RECIPES FROM: MARIO'S ITALIAN
=================================
Source Folder: Mario's Italian
Total Recipes: 15

1. Spaghetti Carbonara
   Cuisine: italian
   Modified: 2025-06-15
   Path: C:\Projects\Mario's Italian\carbonara.xlsx

2. Margherita Pizza
   Cuisine: italian
   Modified: 2025-06-16
   Path: C:\Projects\Mario's Italian\pizza.xlsx
...
```

---

### Use Case 2: Find All Recipes from a Specific Month

**Example:** All recipes modified in July 2025

```powershell
py track_recipe_sources.py date 2025 7
```

**Result:**
```
RECIPES FROM 7/2025
===================
Found 12 recipes:

1. Cooked Wild Rice (Modified: 2025-07-07)
2. Dessert Cookie Cups (Modified: 2025-07-07)
...
```

---

### Use Case 3: Find All Source Locations

**Example:** See all restaurants/projects you have recipes from

```powershell
py track_recipe_sources.py sources
```

**Result:**
```
ALL RECIPE SOURCES
==================
Found 5 different sources:

[Mario's Italian]
   15 recipes
   Sample: Spaghetti Carbonara
           Margherita Pizza

[Taco Bell Test Kitchen]
   8 recipes
   Sample: Crunchy Taco
           Bean Burrito

[Home Recipes]
   25 recipes
   Sample: Chocolate Chip Cookies
           Banana Bread
...
```

---

### Use Case 4: Search by Path Keyword

**Example:** Find all recipes with "project" in the path

```powershell
# Interactive:
py track_recipe_sources.py
# Choose: 4. Search by location keyword
# Enter: project
```

This searches the FULL file path, so you can find recipes from:
- Specific folders: `Desktop`, `Documents`, `Projects`
- Specific projects: `Italian Project`, `Summer Menu`
- Specific clients: `Restaurant ABC`, `Catering Co`

---

## 📤 Export Report

Generate a complete JSON report of all sources:

```powershell
# Interactive:
py track_recipe_sources.py
# Choose: 5. Export source report
```

Creates `recipe_sources_report.json`:
```json
{
  "generated": "2025-10-20T17:30:00",
  "total_sources": 5,
  "total_recipes": 48,
  "sources": {
    "Mario's Italian": {
      "count": 15,
      "recipes": [
        {
          "title": "Spaghetti Carbonara",
          "path": "C:\\Projects\\Mario's Italian\\carbonara.xlsx",
          "modified": "2025-06-15",
          "cuisine": "italian"
        }
      ]
    }
  }
}
```

---

## 💡 Real-World Scenarios

### Scenario 1: Restaurant Menu Development
You're developing menus for 3 different restaurants. Keep recipes organized:

```
C:\Projects\
├── Mario's Italian\       ← 15 recipes
├── Taco Palace\          ← 8 recipes
└── Sushi Bar\            ← 12 recipes
```

**Organize them:**
```powershell
py organize_recipes.py "C:\Projects\Mario's Italian"
py organize_recipes.py "C:\Projects\Taco Palace"
py organize_recipes.py "C:\Projects\Sushi Bar"
```

**Later, find all recipes from Mario's:**
```powershell
py track_recipe_sources.py location "Mario's Italian"
```

---

### Scenario 2: Time-Based Recipe Development

Track recipe development over time:

```powershell
# What did we create in Q1 2025?
py track_recipe_sources.py date 2025 1
py track_recipe_sources.py date 2025 2
py track_recipe_sources.py date 2025 3

# What did we create in 2024?
py track_recipe_sources.py date 2024
```

---

### Scenario 3: Client Work Tracking

You work with multiple clients:

```
C:\ClientWork\
├── Restaurant A\
├── Catering Company B\
└── Food Truck C\
```

**After organizing:**
```powershell
# See all clients
py track_recipe_sources.py sources

# Find specific client's recipes
py track_recipe_sources.py location "Restaurant A"
```

---

## 🔑 Key Features

### ✅ Preserves Original Location
Even after organizing recipes into the library, you can always see where they originally came from.

### ✅ Date Tracking
Search by creation date or modification date to track when recipes were developed.

### ✅ Smart Folder Detection
Automatically extracts meaningful folder names from paths (skips generic folders like "Documents", "Downloads").

### ✅ Multiple Search Methods
- By exact date (year + month)
- By date range (whole year)
- By location name
- By path keyword
- View all sources

### ✅ Export Capabilities
Generate JSON reports for further analysis or record-keeping.

---

## 📝 Interactive Menu Options

```
RECIPE SOURCE TRACKER
=====================

1. View all source locations (restaurants/projects)
2. View recipes from specific location
3. Search by date (year/month)
4. Search by location keyword
5. Export source report
6. Exit
```

---

## 🎓 Tips

1. **Organize with meaningful folder names**
   - ✓ Good: `C:\Projects\Italian Restaurant 2025\`
   - ✗ Bad: `C:\Desktop\New folder\`

2. **Keep folder structure before organizing**
   - Use COPY mode first to preserve originals
   - Original paths are stored in database

3. **Use date ranges for time tracking**
   - Monthly: `date 2025 7`
   - Yearly: `date 2025`

4. **Export reports regularly**
   - Keep JSON backups of source tracking
   - Useful for auditing and reporting

---

## 🔗 Integration with Other Tools

This tool works with:
- **organize_recipes.py** - Consolidate recipes while preserving source info
- **scan_any_folder.py** - Import from any folder, tracks original location
- **run_library.py** - Search and browse organized recipes
- **recipe_dashboard.py** - GUI for recipe management

---

## 📊 Example Workflow

**Step 1:** Organize recipes from multiple sources
```powershell
py organize_recipes.py "C:\RestaurantA"
py organize_recipes.py "C:\RestaurantB"
py organize_recipes.py "C:\HomeRecipes"
```

**Step 2:** Browse all sources
```powershell
py track_recipe_sources.py sources
```

**Step 3:** Find specific restaurant's recipes
```powershell
py track_recipe_sources.py location "RestaurantA"
```

**Step 4:** Export report
```powershell
py track_recipe_sources.py
# Choose: 5. Export source report
```

---

## 🎉 You're Ready!

Now you can:
- ✓ Track which restaurant/project recipes came from
- ✓ Search by date to see recipe development over time  
- ✓ Find original file locations
- ✓ Group recipes by their source
- ✓ Export detailed source reports

**Start tracking:** `py track_recipe_sources.py`

