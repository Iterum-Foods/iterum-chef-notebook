# Vendor Price Import Guide

## Excel vs Website: Which is Better?

**✅ Excel Files are RECOMMENDED** for vendor price imports because:

### Advantages of Excel:
- **More Reliable** - No website changes to break the import
- **Faster** - No network delays or scraping complexity
- **Complete Data** - All products in one file
- **Offline Access** - Works without internet
- **Standardized Format** - Easy to parse consistently
- **Better Control** - You can review/edit before importing

### Website Import Limitations:
- Requires vendor-specific code for each website
- Websites change structure frequently
- Often requires login/authentication
- Slower (network requests)
- May miss products (pagination, filters)
- More complex to maintain

**Recommendation:** Use Excel files from your vendor. Most vendors provide downloadable price lists or order guides in Excel format.

---

## How to Import Vendor Prices

### Method 1: Using the Dashboard (Recommended)

1. **Open the Dashboard**
   ```powershell
   start_dashboard.bat
   ```

2. **Go to Ingredient Database Tab**
   - Click on the "🥘 Ingredient Database" tab

3. **Click "💰 Import Vendor Prices"**
   - Select your Excel file (e.g., `89 CHARLES order guide.xlsx`)
   - Enter vendor name (or use suggested name from filename)
   - Choose to preview first or import directly

4. **Review Results**
   - See how many items were matched
   - Check unmatched items
   - Costs are automatically updated for matched ingredients

### Method 2: Using Command Line

```powershell
# Preview import first
python vendor_price_importer.py "C:\Users\chefm\Downloads\89 CHARLES order guide.xlsx" --preview

# Import directly
python vendor_price_importer.py "C:\Users\chefm\Downloads\89 CHARLES order guide.xlsx" --vendor "CHARLES"
```

Or use the batch file:
```powershell
import_vendor_prices.bat "C:\Users\chefm\Downloads\89 CHARLES order guide.xlsx" --vendor "CHARLES"
```

---

## How It Works

### 1. **Automatic Column Detection**
The importer automatically detects:
- **Item/Product Name** column
- **Price/Cost** column
- **Unit** column (if available)
- **SKU/Code** column (if available)
- **Category** column (if available)

### 2. **Smart Ingredient Matching**
For each vendor item, the system:
- Tries exact name match first
- Falls back to fuzzy matching (70% similarity)
- Extracts key terms from vendor names
- Matches to ingredients in your database

### 3. **Automatic Cost Updates**
- Updates `typical_ap_cost` for matched ingredients
- Updates `cost_unit` if provided
- Preserves all other ingredient properties
- Tracks import date and vendor

---

## Excel File Format

The importer works with various Excel formats. It looks for columns with names like:

**Required:**
- Item Name / Product / Description
- Price / Cost / AP Cost / Unit Price

**Optional:**
- Unit / UOM / Unit of Measure
- SKU / Code / Item Number
- Category / Department

### Example Excel Structure:

| Item Name | Price | Unit | SKU |
|-----------|-------|------|-----|
| Onions, Yellow | 1.50 | lb | ON-001 |
| Chicken Breast | 4.50 | lb | CH-001 |
| Butter | 4.25 | lb | BT-001 |

---

## Handling Unmatched Items

If items can't be automatically matched:

1. **Review the unmatched list** after import
2. **Add missing ingredients** manually:
   - Go to Ingredient Database tab
   - Click "➕ Add New"
   - Enter ingredient details
   - The next import will match it

3. **Improve matching** by:
   - Using consistent naming in your database
   - Adding common vendor names as notes
   - Using the search terms feature

---

## Tips for Best Results

1. **Use consistent vendor files**
   - Same format each time
   - Same column names
   - Regular updates (weekly/monthly)

2. **Review before importing**
   - Always preview first
   - Check column detection
   - Verify sample items

3. **Keep ingredient database updated**
   - Add new ingredients as you discover them
   - Use standard naming conventions
   - Include common vendor names in notes

4. **Track multiple vendors**
   - Import from different vendors
   - Compare prices
   - Update costs regularly

---

## Troubleshooting

### "Could not detect required columns"
- **Solution:** Check that your Excel file has columns named something like "Item", "Product", "Price", "Cost"
- You can rename columns in Excel to match common patterns

### "No items matched"
- **Solution:** 
  - Check that ingredient names in database match vendor names
  - Try adding ingredients manually first
  - Review unmatched items and add them

### "Import failed"
- **Solution:**
  - Make sure Excel file is not open in another program
  - Check file format (.xlsx or .xls)
  - Try opening file in Excel and saving as .xlsx

---

## Example: Importing from CHARLES

```powershell
# 1. Preview first
python vendor_price_importer.py "C:\Users\chefm\Downloads\89 CHARLES order guide.xlsx" --preview

# 2. Review the preview - check detected columns and sample items

# 3. Import
python vendor_price_importer.py "C:\Users\chefm\Downloads\89 CHARLES order guide.xlsx" --vendor "CHARLES"

# 4. Check results
# - X items matched and updated
# - Y items unmatched (add manually if needed)
```

---

## Future Enhancements

- **Multi-vendor price comparison**
- **Price history tracking**
- **Automatic price change alerts**
- **Vendor-specific parsers** (if needed)
- **Website import** (for specific vendors with APIs)

---

## Questions?

**Q: Can I import from multiple vendors?**  
A: Yes! Import from as many vendors as you want. Each import updates costs for matched ingredients.

**Q: What if vendor names don't match my ingredient names?**  
A: The system uses fuzzy matching. For best results, add common vendor names to ingredient notes, or manually add unmatched items.

**Q: Does it overwrite existing costs?**  
A: Yes, it updates the `typical_ap_cost` field. You can track price history by importing regularly.

**Q: Can I import from a website instead?**  
A: Website import requires vendor-specific code. Excel is recommended for reliability and speed.

