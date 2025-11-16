# Quick Menu Import Guide

## Import "Winter Menu 25 89 charles.pdf" in 5 Steps

### 1. Open Menu Builder
- Navigate to: `http://localhost:8090/public/menu-builder.html` (or your server URL)
- Ensure you're logged in (check header for user email)

### 2. Click "Import Menu Files"
- Button is in the page header (top right area)
- Modal will open

### 3. Select Your PDF
- Click "Choose Files" or drag & drop
- Navigate to: `C:\Users\chefm\Downloads\Winter Menu 25 89 charles.pdf`
- Select the file

### 4. Review Parsed Items
- System extracts text from PDF (may take a few seconds)
- Review the items in the modal:
  - Check names are correct
  - Verify prices extracted
  - Confirm categories assigned
- Edit any items if needed

### 5. Apply to Menu
- Click "✓ Apply to Menu" button
- System will:
  - Add all items to your menu
  - Create recipe stubs automatically
  - Link menu items to recipes
  - Save to localStorage & Firestore

## What Happens Next?

### Automatic Actions:
1. ✅ Menu items added to current menu
2. ✅ Recipe stubs created for each item
3. ✅ Menu items linked to recipe stubs
4. ✅ Data saved locally and synced to cloud

### Manual Steps:
1. **Develop Recipes**: Click on menu items → "Develop Recipe"
2. **Add Ingredients**: Fill in recipe details
3. **Link Equipment**: Select from inventory
4. **Generate Prep Lists**: Go to Kitchen Management tab
5. **Create FOH Briefings**: Generate server talking points

## Verification

After import, check:
- [ ] Menu items appear in Menu Builder
- [ ] Items show recipe link icon (🔗)
- [ ] Recipe stubs exist in Recipe Library
- [ ] Menu Ops Checklist updates on dashboard

## Troubleshooting

**PDF won't load?**
- Check browser console (F12)
- Verify PDF.js loaded: Look for `pdfjsLib` in console
- Try refreshing the page

**No items parsed?**
- Check console for extracted text
- Try unchecking "Auto-categorize" option
- Manually edit items after import

**Recipes not created?**
- Check console for errors
- Verify: `window.enhancedMenuManager` exists
- Verify: `window.menuRecipeIntegration` exists

## Next Steps

1. Review imported menu items
2. Develop recipes (add ingredients, instructions)
3. Generate prep lists and FOH briefings
4. Track workflow on dashboard

---

**Full workflow guide**: See `MENU_IMPORT_WORKFLOW.md` for detailed documentation.

