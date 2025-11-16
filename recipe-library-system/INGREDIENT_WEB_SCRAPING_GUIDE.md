# Ingredient Web Scraping Guide

## Overview

You can now add a URL link to any ingredient and automatically scrape information from product/vendor websites. This extracts details like name, price, description, storage notes, and usage suggestions.

## How to Use

### Method 1: Add New Ingredient with URL

1. **Open Dashboard**
   ```powershell
   start_dashboard.bat
   ```

2. **Go to Ingredient Database Tab**
   - Click on "🥘 Ingredient Database"

3. **Click "➕ Add New"**

4. **Enter URL and Scrape**
   - In the "Source URL" field, paste the product URL
   - Example: `https://zigantetartufi.com/products/fresh-black-truffle-tuber-unicatum`
   - Click the "🌐 Scrape" button next to the URL field

5. **Review Scraped Data**
   - The form will auto-populate with:
     - Name
     - Price
     - Unit
     - Storage notes
     - Description/Notes
   - Review and adjust as needed

6. **Fill Remaining Fields**
   - Category
   - Subcategory (optional)
   - Typical Yield % (if different from default)
   - Shelf Life (if available)

7. **Save Ingredient**

### Method 2: Edit Existing Ingredient

1. **Select an ingredient** from the list
2. **Click "✏️ Edit"**
3. **Add or update URL** in the "Source URL" field
4. **Click "🌐 Scrape"** to update information
5. **Save changes**

### Method 3: Command Line

```powershell
# Scrape ingredient info from URL
python ingredient_web_scraper.py "https://zigantetartufi.com/products/fresh-black-truffle-tuber-unicatum"

# Output as JSON
python ingredient_web_scraper.py "URL" --json
```

---

## What Gets Scraped

The scraper automatically extracts:

### ✅ Always Extracted:
- **Product Name** - From page title or product name
- **Price** - Current price (if available)
- **Unit/Size** - Weight or unit (g, kg, oz, lb)
- **Description** - Product description and details

### ✅ When Available:
- **Storage Notes** - Preservation/storage instructions
- **Usage Suggestions** - Serving recommendations
- **Origin/Season** - Where it's from, seasonality
- **Additional Notes** - Other relevant information

---

## Supported Websites

### ✅ Fully Supported:
- **Zigante Tartufi** - Specialized extraction for truffle products
- **Shopify Stores** - Generic Shopify product pages
- **WooCommerce Stores** - Generic WooCommerce product pages

### ✅ Generic Support:
- Most e-commerce sites with standard product page structure
- Sites with Schema.org product markup
- Sites with common HTML patterns

---

## Example: Black Truffles

**URL:** `https://zigantetartufi.com/products/fresh-black-truffle-tuber-unicatum`

**Scraped Information:**
- Name: "Fresh Black Truffle-Tuber Uncinatum"
- Price: €48.30 (for 50g)
- Unit: 50g
- Storage: "Wrap each truffle in paper... Store in fridge (+2°C/+4°C)..."
- Usage: "Best served grated or finely sliced over warm dishes... Ideal with pasta, rice, eggs..."
- Origin: "Istria, Season: September to January"
- Notes: Full product description

---

## Tips for Best Results

1. **Use Product Pages**
   - Use direct product URLs, not category pages
   - Product pages have the most detailed information

2. **Review Scraped Data**
   - Always review auto-populated fields
   - Adjust category, subcategory, and yield % as needed
   - Add missing information manually

3. **Update Prices Regularly**
   - Prices change frequently
   - Re-scrape periodically to update costs
   - Or use vendor price import for bulk updates

4. **Combine with Vendor Import**
   - Use URL scraping for detailed product info
   - Use Excel import for bulk price updates
   - Best of both worlds!

---

## Troubleshooting

### "Scraping Failed" Error

**Possible Causes:**
- Website requires login/authentication
- Website blocks automated access
- URL is not a product page
- Website structure changed

**Solutions:**
- Try a different product page
- Check if URL is correct
- Some sites may require manual entry

### Missing Information

**If some fields aren't populated:**
- Website may not have that information
- Fill manually based on your knowledge
- Check if information is in a different format

### Price Not Detected

**If price isn't scraped:**
- Price may be in a non-standard format
- Enter manually
- Use vendor price import for accurate pricing

---

## Advanced Usage

### Custom Scraping

The scraper uses multiple extraction methods:
1. **Site-specific** - Optimized for known sites (Zigante, Shopify, etc.)
2. **Generic** - Works with most standard product pages
3. **Fallback** - Basic extraction from any HTML

### Extending Support

To add support for a specific vendor:
1. Edit `ingredient_web_scraper.py`
2. Add a new extraction method (e.g., `_extract_vendorname`)
3. Add domain check in `scrape_ingredient_info`

---

## Benefits

✅ **Save Time** - Auto-populate ingredient details  
✅ **Accurate Information** - Direct from vendor/product pages  
✅ **Price Tracking** - Keep costs up to date  
✅ **Complete Details** - Storage, usage, origin information  
✅ **Source Reference** - Always know where info came from  

---

## Example Workflow

1. **Find a new ingredient** on a vendor website
2. **Copy the product URL**
3. **Add new ingredient** in dashboard
4. **Paste URL and click Scrape**
5. **Review and adjust** scraped information
6. **Save** - Done!

The ingredient is now in your database with all the details from the website.

---

## Questions?

**Q: Can I scrape from any website?**  
A: Most product pages work, but some sites may block scraping or require login.

**Q: Does it update prices automatically?**  
A: No, you need to re-scrape or use vendor price import to update prices.

**Q: Can I scrape multiple ingredients at once?**  
A: Currently, scrape one at a time. Use vendor price import for bulk updates.

**Q: What if the website changes?**  
A: The scraper has fallback methods, but you may need to update the extraction code for major site changes.

