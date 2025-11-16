# Menu Import Workflow Guide

## Quick Start: Importing "Winter Menu 25 89 charles.pdf"

### Step 1: Open Menu Builder
1. Navigate to `public/menu-builder.html` in your browser
2. Ensure you're logged in (Firebase auth)
3. Select your project (default: "Master Project")

### Step 2: Import PDF Menu
1. Click **"Import Menu Files"** button in the page header
2. In the modal, click **"Choose Files"** or drag & drop your PDF
3. Select: `C:\Users\chefm\Downloads\Winter Menu 25 89 charles.pdf`
4. Ensure these options are checked:
   - ✅ Create sections from headings
   - ✅ Extract prices and currency symbols
   - ✅ Pull descriptions & chef notes (optional)
5. Click **"Import & Parse"**

### Step 3: Review Parsed Items
The system will:
- Extract text from PDF using PDF.js (client-side)
- Parse menu structure using SmartMenuParser
- Display results in a modal with:
  - **Summary**: Total items, categories, price range
  - **Preview**: List of all detected menu items
  - Each item shows: Name, Category, Price, Description (if found)

### Step 4: Apply Import Results
1. Review the parsed items in the modal
2. Edit any items if needed (click on item to edit)
3. Click **"Apply to Menu"** button
4. The system will:
   - Add all items to your current menu
   - Automatically create recipe stubs for each menu item
   - Link menu items to their recipe stubs
   - Save to localStorage and sync to Firestore

### Step 5: Verify Menu Items
1. The menu builder will refresh showing all imported items
2. Each item appears in its category section
3. Items are automatically linked to recipe stubs (marked with 🔗 icon)

### Step 6: Develop Recipes
1. Click on any menu item to view/edit
2. Click **"Develop Recipe"** to open the recipe developer
3. The recipe stub will already have:
   - Name from menu item
   - Category
   - Price information
   - Menu item link
   - Type: "menu item" or "plated dish"
4. Add ingredients, instructions, equipment, etc.

### Step 7: Generate Prep & FOH Documents
Once recipes are developed:
1. Go to **Kitchen Management** tab
2. Generate:
   - **Prep List**: Automated from linked recipes
   - **Build Sheets**: Per-recipe prep instructions
   - **FOH Briefing**: Server talking points, allergens, dietary info

## Technical Details

### PDF Processing
- **Client-side**: Uses PDF.js library (loaded from CDN)
- **Text Extraction**: Extracts text from all pages, preserving line structure
- **Parsing**: Uses `SmartMenuParser` for intelligent menu structure detection

### Menu Structure Detection
The parser looks for:
- **Categories**: Headings, section titles (e.g., "Appetizers", "Main Courses")
- **Items**: Lines with dish names
- **Prices**: Currency symbols followed by numbers ($, €, £)
- **Descriptions**: Text following item names (optional)

### Recipe Integration
- **Automatic Stub Creation**: Each menu item gets a recipe stub
- **Recipe Linking**: Menu items are linked to their recipe stubs
- **Status Tracking**: Recipe status tracked in menu workflow

### Data Persistence
- **Local Storage**: Menu data saved immediately
- **Firestore Sync**: Automatically synced to cloud
- **Project Isolation**: Data scoped to current project

## Troubleshooting

### PDF Won't Load
- Check browser console for errors
- Ensure PDF.js CDN is accessible
- Try a different PDF file to test

### Items Not Parsing Correctly
- Check the extracted text preview in console
- Manually edit items after import
- Try adjusting parser options (uncheck auto-categorize, etc.)

### Recipes Not Creating
- Check browser console for errors
- Ensure `menu-recipe-integration.js` is loaded
- Verify `universal-recipe-manager.js` is initialized

### Import Modal Not Showing
- Check that `enhanced-menu-import.js` is loaded
- Verify modal HTML exists in page
- Check browser console for JavaScript errors

## Next Steps After Import

1. **Review & Edit Menu Items**
   - Verify all items imported correctly
   - Add missing descriptions
   - Adjust prices if needed
   - Organize categories

2. **Develop Recipes**
   - Click "Develop Recipe" on each menu item
   - Add ingredients and quantities
   - Write step-by-step instructions
   - Add equipment needed
   - Set prep/cook times

3. **Link Equipment & Ingredients**
   - Add equipment to inventory if missing
   - Add ingredients to database if missing
   - Link serving ware to recipes

4. **Generate Kitchen Documents**
   - Prep lists for daily operations
   - Build sheets for each recipe
   - FOH briefing sheets for service

5. **Track Menu Workflow**
   - Check Menu Ops Checklist on dashboard
   - Monitor recipe development status
   - Track prep list completion

## File Locations

- **Menu Builder**: `public/menu-builder.html`
- **Menu Manager**: `public/assets/js/menu-manager-enhanced.js`
- **Menu Parser**: `public/assets/js/smart-menu-parser.js`
- **Import Handler**: `public/assets/js/enhanced-menu-import.js`
- **Recipe Integration**: `public/assets/js/menu-recipe-integration.js`

## Quick Test Checklist

Before importing your PDF, verify:

- [ ] Menu Builder page loads without errors
- [ ] Firebase auth is working (you're logged in)
- [ ] Project is selected (check header)
- [ ] "Import Menu Files" button is visible
- [ ] PDF.js library loads (check browser console)
- [ ] SmartMenuParser is available (check console: `window.SmartMenuParser`)
- [ ] EnhancedMenuImport is available (check console: `window.enhancedMenuImport`)

## Expected Console Output

When importing a PDF, you should see:
```
📦 PDF file read, size: [bytes] bytes
📄 PDF loaded: [N] page(s)
📄 Page 1 extracted: [N] characters
📄 Total extracted text: [N] characters
🔍 parseStructuredText called with text length: [N]
✅ Using SmartMenuParser
📋 SmartMenuParser returned [N] items
✅ Parsed [N] items from PDF
```

## Common Issues & Fixes

### Issue: PDF.js not loading
**Fix**: Check internet connection, PDF.js loads from CDN. If offline, need local copy.

### Issue: No items parsed
**Fix**: 
1. Check extracted text in console
2. Try adjusting parser options (uncheck auto-categorize)
3. Manually edit items after import

### Issue: Import modal doesn't show
**Fix**:
1. Check browser console for JavaScript errors
2. Verify `enhanced-menu-import.js` is loaded
3. Check that modal HTML exists in page

### Issue: Recipes not creating
**Fix**:
1. Check console for errors
2. Verify `menu-recipe-integration.js` is loaded
3. Verify `universal-recipe-manager.js` is initialized
4. Check that menu manager is available: `window.enhancedMenuManager`

