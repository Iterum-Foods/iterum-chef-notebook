# 🚀 Quick Start Guide - Load Your 89 Charles Menu

**For:** chefmcpherson@gmail.com  
**Time Required:** 5 minutes

---

## Step 1: Sign In

1. Go to: https://iterum-culinary-app.web.app
2. Sign in with: `chefmcpherson@gmail.com`
3. Wait for dashboard to load

---

## Step 2: Load Ingredients (Automatic)

**Your 145 ingredients should auto-load when you:**

1. Go to **Ingredients** page
2. Click **"Import Base Ingredients"** if prompted
3. Wait for import to complete

**Result:** You should see 145 ingredients including:
- 72 base ingredients (common items)
- 73 Chef's Warehouse specialty ingredients

**If ingredients don't show:**
- Refresh the page (F5)
- Click "Import Base Ingredients" button
- Check browser console (F12) for errors

---

## Step 3: Import Recipes (Manual - One Time)

**Use the Bulk Recipe Import tool:**

1. **Go to:** https://iterum-culinary-app.web.app/bulk-recipe-import.html

2. **Select "Paste Text" method**

3. **Copy the recipe text:**
   - Open: `89-charles-recipes-for-bulk-upload.txt`
   - Select all (Ctrl+A)
   - Copy (Ctrl+C)

4. **Paste into the text area** in Bulk Recipe Import

5. **Click "Detect & Parse Recipes"**
   - System will auto-detect 10+ recipes
   - Shows preview of each recipe
   - Confirms ingredients and instructions

6. **Click "Accept All & Import"**
   - Recipes saved to library
   - Linked to 89 Charles project
   - Available immediately

**Result:** All 8-10 recipes imported and saved!

---

## Step 4: Create the 89 Charles Menu

1. **Go to:** Menu Builder
   
2. **Click "Create New Menu"**

3. **Fill in menu details:**
   ```
   Menu Name: 89 Charles Fall Food Menu
   Description: Seasonal fall menu featuring premium Chef's Warehouse ingredients
   Season: Fall
   Year: 2025
   Project: 89 Charles
   ```

4. **Add menu items:**
   - Click "Add Menu Item"
   - For each of the 15 dishes:
     ```
     Name: Hamachi Crudo
     Description: spicy citrus broth | hyssop oil | ras el hanout
     Category: Small Bites
     Price: $17.00
     Cost: $6.50
     Link Recipe: Select "Hamachi Crudo" from dropdown
     ```

5. **Save Menu**

**Result:** 89 Charles Fall Food Menu created with 15 dishes!

---

## Step 5: Verify Everything Loaded

### **Check Recipes:**
1. Go to **Recipe Library**
2. Filter by project: "89 Charles"
3. Should see: 8-10 recipes

### **Check Ingredients:**
1. Go to **Ingredients**
2. Filter by vendor: "Chef's Warehouse"
3. Should see: 73 specialty ingredients

### **Check Menu:**
1. Go to **Menu Builder**
2. Select "89 Charles Fall Food Menu"
3. Should see: 15 dishes across 6 categories

### **Check Kitchen Features:**
1. Go to **Kitchen Management**
2. Try generating a build sheet
3. Try creating a prep list
4. Generate server info sheet

---

## 🔧 **Troubleshooting**

### **Problem: No ingredients showing**

**Solution:**
1. Go to Ingredients page
2. Open browser console (F12)
3. Type: `window.baseIngredientsLoader.importIngredients()`
4. Press Enter
5. Wait for import to complete
6. Refresh page

### **Problem: Recipes not in library**

**Solution:**
1. Go to: https://iterum-culinary-app.web.app/bulk-recipe-import.html
2. Copy text from `89-charles-recipes-for-bulk-upload.txt`
3. Paste and import
4. Or manually create each recipe in Recipe Developer

### **Problem: Menu not showing**

**Solution:**
1. Check if you're logged in as chefmcpherson@gmail.com
2. Go to Menu Builder
3. Manually create menu (see Step 4 above)
4. Or import menu JSON file

### **Problem: Can't see new features**

**Solution:**
1. Hard refresh: Ctrl+Shift+R
2. Clear cache and reload
3. Make sure you're on: https://iterum-culinary-app.web.app
4. Check dashboard - should see Kitchen Mgmt, Highlights, Server Sheet cards

---

## ⚡ **Quick Import Commands**

**Open browser console (F12) and run:**

```javascript
// Force import base ingredients
window.baseIngredientsLoader.importIngredients();

// Check if 89 Charles data is loaded
const userId = window.authManager.currentUser.userId;
console.log('Menus:', localStorage.getItem(`menus_${userId}`));
console.log('Recipes:', localStorage.getItem(`recipes_${userId}`));

// Manually trigger 89 Charles loader
if (window.authManager.currentUser.email === 'chefmcpherson@gmail.com') {
  fetch('89-charles-fall-menu.json')
    .then(r => r.json())
    .then(menu => {
      const userId = window.authManager.currentUser.userId;
      const key = `menus_${userId}`;
      let menus = JSON.parse(localStorage.getItem(key) || '[]');
      if (!menus.find(m => m.id === menu.id)) {
        menus.push(menu);
        localStorage.setItem(key, JSON.stringify(menus));
        alert('✅ Menu loaded!');
      }
    });
}
```

---

## 📋 **Alternative: Manual Menu Creation**

If auto-loading doesn't work, manually create the menu:

**15 Dishes to Add:**

1. **Hamachi Crudo** - $17 (Small Bites)
2. **Olives and Almonds** - $12 (Small Bites)
3. **Blue Cheese Olives** - $7 (Appetizers)
4. **Rainbow Fingerling Potatoes** - $14 (Appetizers)
5. **Shaved Fennel Caesar** - $16 (Salads)
6. **7-rows Koginut Pumpkin and Burrata** - $16 (Salads)
7. **Spicy Flatbread** - $20 (Entrées)
8. **Wagyu Hot Dog** - $20 (Entrées)
9. **Australian Beef French Dip** - $26 (Entrées)
10. **Caviar 30g** - $100 (Caviar)
11. **Caviar 50g** - $160 (Caviar)
12. **Caviar 100g** - $240 (Caviar)
13. **Warm Chocolate Chip Cookie** - $8 (Dessert)
14. **RiceTreat** - $6 (Dessert)
15. **Charred Creme Fraiche Tart** - $14 (Dessert)

---

## ✅ **Expected Results After Setup:**

### **Dashboard:**
- ✅ See "89 Charles" in project dropdown
- ✅ See new feature cards: Kitchen Mgmt, Highlights, Server Sheet
- ✅ No welcome popup

### **Ingredients Page:**
- ✅ 145 total ingredients
- ✅ Filter by "Chef's Warehouse" shows 73 items
- ✅ All categories populated

### **Recipe Library:**
- ✅ Filter by "89 Charles" shows your recipes
- ✅ Each recipe has components listed
- ✅ Equipment linked

### **Menu Builder:**
- ✅ "89 Charles Fall Food Menu" in dropdown
- ✅ 15 dishes visible
- ✅ Categories organized

### **Kitchen Management:**
- ✅ Generate PDF recipe book
- ✅ Create build sheets
- ✅ View prep lists
- ✅ Quality checklists

### **Server Info Sheet:**
- ✅ Select menu shows all dishes
- ✅ Allergen warnings visible
- ✅ Talking points generated
- ✅ PDF export works

---

## 🎯 **Fastest Path to Full Setup:**

1. **Sign in** → chefmcpherson@gmail.com
2. **Go to Ingredients** → Auto-imports 145 ingredients
3. **Go to Bulk Recipe Import** → Paste from `89-charles-recipes-for-bulk-upload.txt`
4. **Go to Menu Builder** → Create "89 Charles Fall Food Menu"
5. **Add 15 menu items** → Link to imported recipes
6. **Done!** → All features now functional

**Time:** ~10 minutes for complete setup

---

## 📞 **Need Help?**

**Check Console Logs:**
- Press F12
- Go to Console tab
- Look for:
  - "✅ 89 Charles menu loaded"
  - "✅ Loaded X recipes"
  - "✅ Base ingredients imported"

**Common Issues:**
- **Not signed in** → Make sure you're logged in as chefmcpherson@gmail.com
- **Wrong project** → Select "89 Charles" from project dropdown
- **Cache** → Hard refresh (Ctrl+Shift+R)
- **Data not loading** → Use manual import methods above

---

Ready to set up! Follow the steps and everything should load. 🚀

