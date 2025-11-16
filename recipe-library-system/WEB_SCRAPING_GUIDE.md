# 🌐 Web Recipe Scraping Guide

## New Feature: Scrape Recipes from Websites!

Your recipe management system can now extract recipes directly from recipe websites and automatically import them into your library.

---

## 🚀 Quick Start

### Option 1: Web Interface (Easiest)

1. **Start the enhanced web app:**
   ```powershell
   start_enhanced_app.bat
   ```

2. **Navigate to "Scrape from Web"** in the Quick Actions section

3. **Enter a recipe URL** and click "Scrape Recipe"

4. **Done!** The recipe is automatically imported to your library

### Option 2: Command Line

**Single recipe:**
```powershell
python web_recipe_scraper.py "https://example.com/recipe/pasta-carbonara"
```

**Multiple recipes from file:**
```powershell
# Create a file with URLs (one per line)
python web_recipe_scraper.py --file urls.txt
```

**Interactive mode:**
```powershell
python web_recipe_scraper.py
# Then enter URLs one by one
```

### Option 3: Batch File

```powershell
scrape_web_recipe.bat "https://example.com/recipe"
```

---

## 📋 What Gets Extracted

The scraper extracts:
- ✅ Recipe title
- ✅ Ingredients list
- ✅ Instructions/method
- ✅ Prep time
- ✅ Cook time
- ✅ Servings/yield
- ✅ Cuisine type (if available)
- ✅ Recipe description
- ✅ Source URL (saved for reference)

---

## 🎯 Supported Formats

The scraper supports multiple recipe formats:

### 1. Schema.org JSON-LD (Most Reliable)
Most modern recipe sites use this format. It's the most accurate extraction method.

**Example sites:**
- AllRecipes.com
- FoodNetwork.com
- BBC Good Food
- Most recipe blogs

### 2. Schema.org Microdata
Alternative structured data format used by some sites.

### 3. Common HTML Patterns
Fallback method that looks for common recipe HTML patterns:
- `.ingredients` or `.ingredient-list`
- `.instructions` or `.directions`
- Recipe title in `<h1>` tags

---

## 💡 Usage Examples

### Example 1: Single Recipe

```powershell
python web_recipe_scraper.py "https://www.allrecipes.com/recipe/213742/cheesy-ham-and-hash-brown-casserole/"
```

**Output:**
```
📥 Scraping recipe from: https://www.allrecipes.com/recipe/...
✅ Successfully scraped and imported: Cheesy Ham and Hash Brown Casserole
   ID: abc123def456
   Library path: recipe_library/abc123def456.md
```

### Example 2: Multiple Recipes

Create a file `recipe_urls.txt`:
```
https://example.com/recipe1
https://example.com/recipe2
https://example.com/recipe3
```

Then run:
```powershell
python web_recipe_scraper.py --file recipe_urls.txt
```

### Example 3: Web Interface

1. Open `http://localhost:5000` in your browser
2. Click "Scrape from Web"
3. Paste recipe URL
4. Click "Scrape Recipe"
5. View the imported recipe!

---

## 🔧 Installation

If you haven't installed the required packages yet:

```powershell
pip install -r requirements_recipe_finder.txt
```

This installs:
- `requests` - For fetching web pages
- `beautifulsoup4` - For parsing HTML
- `lxml` - For faster HTML parsing

---

## 📊 Workflow Integration

### Complete Workflow

1. **Scrape recipes from web**
   ```powershell
   python web_recipe_scraper.py "https://example.com/recipe"
   ```

2. **Convert to Iterum format**
   ```powershell
   standardize_recipes.bat
   ```

3. **Fill in costing data**
   - Open files in `converted_iterum/`
   - Add ingredient costs

4. **Upload to Iterum**
   - Batch upload to Chef's Notebook

---

## ⚠️ Important Notes

### What Works Well
- ✅ Sites with Schema.org Recipe markup
- ✅ Most modern recipe blogs
- ✅ AllRecipes, Food Network, BBC Good Food
- ✅ Sites with structured recipe data

### Limitations
- ❌ Sites that require JavaScript (scraper doesn't execute JS)
- ❌ Sites behind paywalls or login
- ❌ Some sites with complex layouts
- ❌ Very old recipe sites without structured data

### Tips for Best Results
1. **Use direct recipe page URLs** (not category or search pages)
2. **Check scraped recipes** for accuracy
3. **Some sites may need manual review** after scraping
4. **Convert to Iterum format** after scraping to standardize

---

## 🐛 Troubleshooting

### Issue: "Could not extract recipe data"

**Solutions:**
- Make sure you're using a direct recipe page URL
- Some sites may not have structured data
- Try a different recipe from the same site
- Check if the site requires JavaScript (not supported)

### Issue: "Error fetching URL"

**Solutions:**
- Check your internet connection
- Verify the URL is correct
- Some sites may block automated requests
- Try again later (site may be temporarily down)

### Issue: Missing ingredients or instructions

**Solutions:**
- The site may not use standard recipe markup
- Check the scraped file manually
- You can edit the recipe after import
- Try a different recipe from the same site

---

## 📝 Example URLs to Try

Here are some example recipe URLs you can test with:

```
https://www.allrecipes.com/recipe/213742/cheesy-ham-and-hash-brown-casserole/
https://www.foodnetwork.com/recipes/alton-brown/baked-macaroni-and-cheese-recipe-1939524
https://www.bbcgoodfood.com/recipes/classic-spaghetti-carbonara-recipe
```

**Note:** Always respect website terms of service and copyright when scraping recipes.

---

## 🎯 Next Steps

After scraping recipes:

1. **Review scraped recipes** in your library
2. **Convert to Iterum format** using `standardize_recipes.bat`
3. **Fill in costing data** in the Excel files
4. **Track sources** using `track_sources.bat` (URLs are saved automatically)
5. **Upload to Iterum** Chef's Notebook

---

## 📚 Related Documentation

- **MASTER_GUIDE.md** - Complete system overview
- **COMPLETE_SYSTEM_OVERVIEW.md** - All features
- **WEB_UI_GUIDE.md** - Web interface guide
- **CONVERT_TO_ITERUM.md** - Conversion guide

---

## 🎉 Summary

You now have a powerful web scraping tool that:
- ✅ Extracts recipes from websites automatically
- ✅ Supports multiple recipe formats
- ✅ Integrates seamlessly with your library
- ✅ Works via web interface or command line
- ✅ Saves source URLs for reference

**Start scraping recipes now!**

```powershell
# Quick start
start_enhanced_app.bat
# Then click "Scrape from Web"
```

---

*Last Updated: October 2025*  
*Feature: Web Recipe Scraping*

