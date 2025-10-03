# 🌐 URL Ingredient Import System

## Overview

The URL Ingredient Import System allows you to easily expand your ingredient database by importing ingredient data from web sources like Wikipedia, nutrition databases, and food websites. Simply paste a URL, preview the extracted data, and import it with one click.

## 🚀 Quick Start

### Access URL Import
1. Navigate to the **Ingredients** page (`ingredients.html`)
2. Look for the **🌐 Import from URL** button in the debug controls section
3. Click to open the URL import modal

### Import Process
1. **Paste URL**: Enter the URL of an ingredient page
2. **Preview Data**: Click "🔍 Preview Data" to see what will be imported
3. **Import**: Click "✅ Import Ingredient" to add to your database

## 📚 Supported Sources

### Wikipedia
- **Format**: `https://en.wikipedia.org/wiki/[Ingredient_Name]`
- **Best For**: Comprehensive ingredient information with descriptions
- **Data Extracted**: Name, description, category, nutritional info, allergens

**Example URLs:**
- `https://en.wikipedia.org/wiki/Tomato`
- `https://en.wikipedia.org/wiki/Basil`
- `https://en.wikipedia.org/wiki/Avocado`

### USDA Nutrition Databases
- **Format**: Various USDA and nutrition database URLs
- **Best For**: Detailed nutritional information
- **Data Extracted**: Nutritional facts, serving sizes, calorie content

### General Food Websites
- **Format**: Any food-related website with ingredient information
- **Best For**: General ingredient data
- **Data Extracted**: Basic information extracted from page content

## 🔧 How It Works

### Backend Processing
1. **URL Validation**: Ensures the URL is properly formatted
2. **Content Fetching**: Retrieves the webpage content
3. **Intelligent Extraction**: Uses domain-specific parsing for optimal results
4. **Data Structuring**: Organizes extracted data into ingredient format

### Content Extraction Strategy

#### Wikipedia Pages
- Extracts title as ingredient name
- Gets first paragraph for description
- Identifies category from page categories
- Parses nutrition infoboxes
- Removes citation brackets and cleans text

#### Nutrition Databases
- Focuses on nutritional data tables
- Extracts serving information
- Identifies calorie and macro information

#### Generic Sources
- Fallback extraction from title tags
- Meta description parsing
- Basic paragraph content extraction

## 📊 Data Structure

### Extracted Information
```json
{
  "name": "Ingredient Name",
  "description": "Detailed description from source",
  "category": "Auto-detected or 'Imported'",
  "default_unit": "gram/piece/ml based on type",
  "nutritional_info": {
    "calories": "per 100g",
    "protein": "grams",
    "carbs": "grams",
    "fat": "grams"
  },
  "allergens": ["detected allergens"]
}
```

### Categories
- **Wikipedia Sources**: Attempts to detect from page categories
- **Nutrition Sources**: Categorized as "Nutrition Database"
- **Generic Sources**: Categorized as "Web Import"
- **Fallback**: "Imported" category for unclassified items

## 🎯 Features

### Preview Before Import
- See exactly what data will be imported
- Review ingredient name, category, and description
- Check nutritional information if available
- Verify allergen detection

### Duplicate Prevention
- Automatic check for existing ingredients
- Warning message if ingredient already exists
- Option to view existing ingredient details

### Error Handling
- Network error recovery
- Invalid URL detection
- Missing data graceful handling
- User-friendly error messages

### Status Feedback
- Real-time import progress
- Success/error notifications
- Color-coded status messages
- Detailed error descriptions

## 🛠️ Technical Implementation

### Backend API Endpoints

#### Preview Endpoint
```
POST /api/ingredients/preview-url
Body: url=<ingredient_url>
```
- Returns extracted data without saving
- Useful for validation before import

#### Import Endpoint
```
POST /api/ingredients/import-from-url
Body: url=<ingredient_url>
```
- Extracts and saves ingredient to database
- Returns created ingredient data

### Frontend Integration
- Modal-based interface
- Real-time status updates
- Example URL suggestions
- Responsive design

### Web Scraping
- User-agent spoofing for compatibility
- Timeout handling (10 seconds)
- BeautifulSoup HTML parsing
- Intelligent content extraction

## 📝 Usage Examples

### Example 1: Wikipedia Tomato
```
URL: https://en.wikipedia.org/wiki/Tomato
Extracted:
- Name: "Tomato"
- Description: "The tomato is the edible berry of the plant Solanum lycopersicum..."
- Category: "Fruit" (detected from categories)
- Nutrition: Vitamin C, lycopene content
```

### Example 2: USDA Database
```
URL: [USDA nutrition URL]
Extracted:
- Name: From page title
- Nutrition: Detailed macro and micronutrients
- Category: "Nutrition Database"
```

## ⚠️ Best Practices

### URL Selection
- Use well-formatted Wikipedia pages for best results
- Prefer English Wikipedia for consistent extraction
- USDA databases provide excellent nutritional data
- Avoid heavily dynamic or JavaScript-dependent pages

### Data Verification
- Always preview before importing
- Verify ingredient name spelling
- Check category assignment
- Review nutritional information accuracy

### Quality Control
- Import from reputable sources
- Double-check exotic or specialized ingredients
- Verify allergen information manually
- Update descriptions if needed after import

## 🔍 Troubleshooting

### Common Issues

#### "Invalid URL format"
- Ensure URL includes http:// or https://
- Check for typos in URL
- Verify URL is accessible

#### "Could not extract ingredient name"
- Page may not contain clear ingredient information
- Try a different source for the same ingredient
- Some pages may not be suitable for extraction

#### "Network error"
- Check internet connection
- Some sites may block automated requests
- Try again after a short wait

#### "Ingredient already exists"
- Check existing ingredient database
- Consider if this is a different variety
- Use manual entry for variations

### Optimization Tips
- Wikipedia articles are most reliable
- Look for pages with nutrition infoboxes
- Avoid disambiguation pages
- Use specific ingredient names

## 🚀 Future Enhancements

### Planned Features
- Bulk URL import from lists
- Image extraction from sources
- Multiple language Wikipedia support
- Enhanced nutrition database integration
- Recipe URL import (extract ingredients from recipe pages)

### Custom Source Configuration
- Add custom parsing rules for specific sites
- Configure extraction patterns
- User-defined source priorities

---

**💡 The URL Import System dramatically speeds up ingredient database expansion, allowing you to quickly build a comprehensive ingredient library from authoritative web sources!**