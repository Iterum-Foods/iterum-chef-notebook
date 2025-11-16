# 🕷️ Website Recipe Crawler Guide

## New Feature: Crawl Entire Websites for Recipes!

Your recipe management system can now crawl entire websites to automatically discover and extract all recipes, then export them to JSON or PDF format.

---

## 🚀 Quick Start

### Option 1: Web Interface (Easiest)

1. **Start the enhanced web app:**
   ```powershell
   start_enhanced_app.bat
   ```

2. **Navigate to "Crawl Website"** in the Quick Actions section

3. **Enter the website URL** (e.g., `https://example.com`)

4. **Choose export format** (JSON or PDF)

5. **Click "Start Crawling"**

6. **Wait for completion** - This may take several minutes

7. **Download your exported file!**

### Option 2: Command Line

**Basic usage:**
```powershell
python website_recipe_crawler.py "https://example.com"
```

**Export to PDF:**
```powershell
python website_recipe_crawler.py "https://example.com" --format pdf
```

**Limit pages and set delay:**
```powershell
python website_recipe_crawler.py "https://example.com" --max-pages 50 --delay 2.0
```

**Crawl only (don't scrape):**
```powershell
python website_recipe_crawler.py "https://example.com" --crawl-only
```

### Option 3: Batch File

```powershell
crawl_website.bat "https://example.com"
```

---

## 📋 What It Does

### 1. **Crawls the Website**
- Starts from the base URL you provide
- Follows links to discover pages
- Identifies pages that contain recipes
- Respects robots.txt files

### 2. **Identifies Recipe Pages**
The crawler uses multiple methods to identify recipe pages:
- **Schema.org Recipe markup** (JSON-LD or microdata)
- **URL patterns** (e.g., `/recipe`, `/recipes`)
- **Content analysis** (looks for recipe indicators)
- **HTML patterns** (common recipe page structures)

### 3. **Extracts Recipe Data**
For each recipe page found:
- Extracts title, ingredients, instructions
- Gets prep/cook times, servings
- Captures cuisine type and description
- Saves source URL

### 4. **Exports to Format**
- **JSON**: Structured data, easy to process
- **PDF**: Printable recipe book format

---

## 🎯 Usage Examples

### Example 1: Basic Crawl (JSON)

```powershell
python website_recipe_crawler.py "https://www.example-recipes.com"
```

**Output:**
```
🌐 Website Recipe Crawler
============================================================
URL: https://www.example-recipes.com
Max pages: 100
Delay: 1.0s
Format: json
============================================================

Starting crawl of https://www.example-recipes.com
Crawling: https://www.example-recipes.com (1/100)
  ✓ Found recipe: https://www.example-recipes.com/recipe/pasta
Crawling: https://www.example-recipes.com/recipe/pasta (2/100)
...

Crawl complete!
  Visited: 45 pages
  Found: 12 recipe pages
  Failed: 0 pages

Scraping 12 recipes...
Scraping 1/12: https://www.example-recipes.com/recipe/pasta
  ✓ Success: Pasta Carbonara
...

✅ Success!
   Recipes found: 12
   Recipes scraped: 12
   Output file: recipes_example_recipes_com_20251020_143022.json
```

### Example 2: Export to PDF

```powershell
python website_recipe_crawler.py "https://www.example-recipes.com" --format pdf
```

Creates a PDF file with all recipes formatted as a recipe book.

### Example 3: Limited Crawl

```powershell
python website_recipe_crawler.py "https://www.example-recipes.com" --max-pages 20 --delay 2.0
```

Crawls only 20 pages with 2-second delays between requests.

### Example 4: Just Find Recipe URLs

```powershell
python website_recipe_crawler.py "https://www.example-recipes.com" --crawl-only
```

Only crawls and lists recipe URLs without scraping them.

---

## 📊 Export Formats

### JSON Format

The JSON export includes:
```json
{
  "export_info": {
    "base_url": "https://example.com",
    "export_date": "2025-10-20T14:30:22",
    "total_recipes": 12,
    "crawler_version": "1.0"
  },
  "recipes": [
    {
      "title": "Pasta Carbonara",
      "description": "Classic Italian pasta dish",
      "ingredients": ["pasta", "eggs", "bacon", ...],
      "instructions": ["Cook pasta", "Fry bacon", ...],
      "prep_time": "15 min",
      "cook_time": "20 min",
      "servings": "4",
      "cuisine": "Italian",
      "source_url": "https://example.com/recipe/pasta",
      "scraped_date": "2025-10-20T14:30:22"
    },
    ...
  ]
}
```

### PDF Format

The PDF export creates a formatted recipe book with:
- Title page with website info
- Each recipe on separate pages
- Formatted ingredients and instructions
- Source URLs for reference
- Professional layout

---

## ⚙️ Configuration Options

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Export format (`json` or `pdf`) | `json` |
| `--output` | Output file path | Auto-generated |
| `--max-pages` | Maximum pages to crawl | `100` |
| `--delay` | Delay between requests (seconds) | `1.0` |
| `--crawl-only` | Only crawl, don't scrape | `False` |

### Web Interface Options

- **Website URL**: Base URL to start crawling
- **Export Format**: JSON or PDF
- **Max Pages**: Limit number of pages (1-1000)
- **Delay**: Seconds between requests (0-10)
- **Crawl Only**: Just find recipe URLs without scraping

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
- `reportlab` - For PDF export (optional)

---

## ⚠️ Important Notes

### Best Practices

1. **Respect robots.txt**: The crawler automatically checks and respects robots.txt files
2. **Use delays**: Set appropriate delays (1-2 seconds) to avoid overwhelming servers
3. **Start small**: Test with `--max-pages 10` first
4. **Be patient**: Crawling can take a long time for large websites
5. **Check terms**: Always respect website terms of service

### Limitations

- **JavaScript sites**: Sites that require JavaScript won't work (crawler doesn't execute JS)
- **Login required**: Sites behind authentication won't be accessible
- **Rate limiting**: Some sites may block automated crawlers
- **Large sites**: Very large sites may take hours to crawl

### Legal Considerations

- ✅ Always respect website terms of service
- ✅ Check robots.txt before crawling
- ✅ Use reasonable delays between requests
- ✅ Don't crawl sites that explicitly prohibit it
- ✅ Respect copyright on recipe content

---

## 🐛 Troubleshooting

### Issue: "No recipes found"

**Solutions:**
- The website may not use standard recipe markup
- Try a different starting URL (e.g., `/recipes` page)
- Check if the site requires JavaScript
- Verify the URL is correct

### Issue: "Crawling is very slow"

**Solutions:**
- Reduce `--max-pages` to crawl fewer pages
- Increase `--delay` to be more respectful
- Some sites are just slow - be patient
- Check your internet connection

### Issue: "Many failed pages"

**Solutions:**
- Some pages may require login
- Some pages may be broken links
- Increase `--delay` to avoid rate limiting
- Check if the site blocks crawlers

### Issue: "PDF export not working"

**Solutions:**
- Install reportlab: `pip install reportlab`
- Use JSON format instead
- Check if you have write permissions

---

## 📝 Example Workflows

### Workflow 1: Extract All Recipes from a Blog

```powershell
# 1. Crawl the blog
python website_recipe_crawler.py "https://myrecipeblog.com" --format json

# 2. Review the JSON file
# 3. Import specific recipes to your library
python web_recipe_scraper.py --file recipe_urls.txt
```

### Workflow 2: Create Recipe Book PDF

```powershell
# 1. Crawl website
python website_recipe_crawler.py "https://example.com" --format pdf --max-pages 50

# 2. Open the PDF file
# 3. Print or share the recipe book
```

### Workflow 3: Find Recipe URLs First

```powershell
# 1. Just crawl to find URLs
python website_recipe_crawler.py "https://example.com" --crawl-only

# 2. Review the recipe URLs
# 3. Scrape specific ones you want
python web_recipe_scraper.py "https://example.com/recipe/1"
```

---

## 🎯 Tips for Best Results

1. **Start with recipe index pages**: If a site has a `/recipes` page, start there
2. **Use appropriate delays**: 1-2 seconds is usually respectful
3. **Test first**: Use `--max-pages 10` to test before full crawl
4. **JSON is faster**: JSON export is faster than PDF
5. **Check output location**: Files are saved in the current directory
6. **Review results**: Always check the exported file for accuracy

---

## 📚 Related Documentation

- **WEB_SCRAPING_GUIDE.md** - Single recipe scraping
- **MASTER_GUIDE.md** - Complete system overview
- **COMPLETE_SYSTEM_OVERVIEW.md** - All features

---

## 🎉 Summary

You now have a powerful website crawler that:
- ✅ Automatically discovers recipe pages on websites
- ✅ Extracts recipe data from each page
- ✅ Exports to JSON or PDF format
- ✅ Respects robots.txt and rate limits
- ✅ Works via web interface or command line

**Start crawling websites now!**

```powershell
# Quick start
start_enhanced_app.bat
# Then click "Crawl Website"
```

---

*Last Updated: October 2025*  
*Feature: Website Recipe Crawler*

