# 📊 Convert Recipes to Iterum Format for Costing

## What This Does

The Recipe Standardizer converts ALL your recipes into the **uniform Iterum Chef's Notebook format** - the professional standard for recipe costing and menu planning.

### Why This Matters

✅ **Uniform Format** - All recipes follow the same structure  
✅ **Professional Costing** - Track AP/EP costs, yields, portions  
✅ **Ready for Upload** - Direct compatibility with Iterum Chef's Notebook  
✅ **Menu Planning** - Calculate recipe costs and food cost percentages  
✅ **Inventory Management** - Track ingredient usage and quantities  

---

## 🎯 Iterum Format Features

### Recipe Header
```
Recipe name: Caramelized Onions
Concept: [Your concept]
Submitted by: Chef
Number of Portions: 1
Cuisine: unknown
Category: recipe
Date: 2025-10-20
Cost per Portion: [Calculated]
Cost per Recipe: [Calculated]
Projected FC%: [Food Cost %]
```

### Ingredients Table
```
┌─────────────────┬─────────┬────────┬────────┬───────────┬──────┬─────────┬───────────┬──────┐
│ Ingredients     │ Quantity│ Weight │ Volume │ AP$ / Unit│ Unit │ Yield % │ EP$ / Unit│ Cost │
├─────────────────┼─────────┼────────┼────────┼───────────┼──────┼─────────┼───────────┼──────┤
│ Onions, yellow  │         │ 10#    │        │           │      │         │           │      │
│ Oil, canola     │         │ 4oz    │        │           │      │         │           │      │
│ Salt            │         │        │        │           │      │         │           │      │
│ Sherry          │         │ 6oz    │        │           │      │         │           │      │
└─────────────────┴─────────┴────────┴────────┴───────────┴──────┴─────────┴───────────┴──────┘
```

### Method Section
```
Method:
1. Thinly slice onions and add to a pot with oil
2. Cook low and slow for 3hrs, or until onions are a deep caramel color
3. Season with salt to bring more moisture out of onions
4. Add sherry, and reduce
```

---

## 🚀 How to Use

### Method 1: Quick Standardization (One Command)

```powershell
# Convert all recipes at once
py standardize_recipes.py --auto
```

### Method 2: Interactive Mode

```powershell
# Double-click this file:
standardize_recipes.bat

# Or run:
py standardize_recipes.py
```

### Method 3: Complete Workflow (Organize + Convert)

```powershell
# Double-click this file for complete workflow:
FULL_WORKFLOW.bat

# This does everything:
#   1. Organizes recipes into library
#   2. Converts to Iterum format
#   3. Prepares for upload
```

---

## 📁 Output Structure

After conversion:

```
converted_iterum/
├── Banana Brown Butter Scone.xlsx
├── Brown Butter Pancakes.xlsx
├── Butternut Hummus.xlsx
├── Caramelized Onions.xlsx
├── Chicken Salad.xlsx
├── Chocolate Chip Cookies New.xlsx
├── Cooked Farro.xlsx
├── Cooked Wild Rice.xlsx
├── Crinkle Cookies.xlsx
├── Dessert Cookie Cups.xlsx
└── Dirty Chai Cookies.xlsx
```

Each file is ready for costing and upload to Iterum Chef's Notebook!

---

## 💰 Recipe Costing Workflow

### Step 1: Convert Recipes
```powershell
py standardize_recipes.py --auto
```

### Step 2: Open Converted Files
Navigate to `converted_iterum/` folder and open any recipe.

### Step 3: Fill in Costing Data

For each ingredient, add:

1. **AP$ / Unit** (As Purchased cost per unit)
   - Example: $2.50 for 1 pound of onions

2. **Unit** (Purchase unit)
   - Examples: lb, oz, each, gallon, bunch

3. **Yield %** (Edible portion percentage)
   - Example: 90% for onions (10% waste from peels)
   - Use built-in yield tools: Produce Yields, Fruit Yields, etc.

4. **EP$ / Unit** (Edible Portion cost)
   - Formula: `= (AP$ / Unit) / (Yield % / 100)`
   - Example: $2.50 / 0.90 = $2.78

5. **Total Cost** (Cost for this recipe quantity)
   - Formula: `= (Weight in lbs) × (EP$ / Unit per lb)`

### Step 4: Calculate Recipe Totals

- **Cost per Recipe** = Sum of all ingredient costs
- **Cost per Portion** = Cost per Recipe ÷ Number of Portions
- **Projected FC%** = (Cost per Portion / Menu Price) × 100

### Example: Costing Caramelized Onions

```excel
Ingredients      | Weight | AP$/Unit | Unit | Yield% | EP$/Unit | Total Cost
-----------------|--------|----------|------|--------|----------|-----------
Onions, yellow   | 10 lb  | $1.50    | lb   | 90%    | $1.67    | $16.70
Oil, canola      | 0.25lb | $3.00    | lb   | 100%   | $3.00    | $0.75
Salt             | 0.02lb | $0.50    | lb   | 100%   | $0.50    | $0.01
Sherry           | 0.38lb | $12.00   | lb   | 100%   | $12.00   | $4.56
--------------------------------------------------------------------------------
                                              Cost per Recipe:     $22.02
                                              Number of Portions:  24
                                              Cost per Portion:    $0.92
```

---

## 🎓 Professional Features

### 1. Yield Management
Track waste and calculate true costs:
- **Produce**: Peeling, trimming (usually 80-95%)
- **Fruits**: Seeds, cores, peels (usually 75-90%)
- **Fish**: Filleting, bones (usually 40-60%)
- **Meat**: Trimming, bones (usually 70-85%)

### 2. Portion Control
```
Number of Portions: 24
Serving Size Per Person: 2 oz
Total Recipe Yield: 48 oz = 3 lbs
```

### 3. Recipe Scaling
Change "Number of Portions" and all costs recalculate automatically!

### 4. Menu Pricing
```
Cost per Portion: $0.92
Target FC%: 30%
Menu Price = $0.92 / 0.30 = $3.07
```

---

## 📤 Upload to Iterum Chef's Notebook

### Option 1: Direct Upload
1. Open Iterum Chef's Notebook
2. Go to "Import Recipes"
3. Select your converted Excel files
4. Review and confirm import

### Option 2: Batch Upload
1. Select all files in `converted_iterum/` folder
2. Use Iterum's batch import feature
3. Map columns if prompted
4. Import all recipes at once

### Option 3: Manual Entry
1. Open Iterum Chef's Notebook
2. Create new recipe
3. Copy/paste from converted Excel files
4. Save and cost

---

## 🔄 Complete Workflow Example

### Scenario: Restaurant Menu Development

**Step 1: Collect recipes from multiple sources**
```powershell
# Recipes from different projects
C:\Projects\Italian Menu\
C:\Projects\Summer Specials\
C:\Projects\Desserts\
```

**Step 2: Organize into library**
```powershell
py organize_recipes.py "C:\Projects\Italian Menu"
py organize_recipes.py "C:\Projects\Summer Specials"
py organize_recipes.py "C:\Projects\Desserts"
```

**Step 3: Convert to Iterum format**
```powershell
py standardize_recipes.py --auto
```

**Step 4: Cost all recipes**
- Open each file in `converted_iterum/`
- Fill in ingredient costs
- Calculate totals

**Step 5: Menu planning**
- Cost per Portion ÷ Target FC% = Menu Price
- Example: $3.50 cost ÷ 30% FC = $11.67 menu price

**Step 6: Upload to Iterum**
- Batch upload all costed recipes
- Use for menu planning and inventory

---

## 📊 Real-World Example

### Before Conversion:
12 recipes in different formats:
- Various Excel layouts
- Different column names
- Inconsistent data
- Hard to compare costs

### After Conversion:
12 recipes in uniform format:
- Same layout
- Same columns
- Consistent data
- Easy to compare costs
- Ready for professional use

---

## 🎯 Key Benefits

### For Chefs:
✅ Professional recipe documentation  
✅ Accurate portion costing  
✅ Recipe scaling made easy  
✅ Menu planning with real costs  

### For Restaurant Owners:
✅ Control food costs  
✅ Optimize menu pricing  
✅ Track ingredient usage  
✅ Reduce waste  

### For Culinary Students:
✅ Learn professional costing  
✅ Build recipe portfolio  
✅ Practice menu development  
✅ Industry-standard format  

---

## 💡 Tips & Best Practices

### 1. Keep Vendor Invoices
- Update AP$ costs from actual invoices
- Track price changes over time
- Use average prices for stability

### 2. Use Yield Tables
- USDA yield tables for produce
- Standard yield percentages for proteins
- Document your own yields for accuracy

### 3. Review Regularly
- Update costs quarterly
- Adjust for seasonal ingredients
- Recalculate menu prices as needed

### 4. Document Everything
- Note source of costs
- Record date of last update
- Add special notes (seasonal, limited, etc.)

### 5. Scale Smart
- Test scaled recipes before production
- Verify yields don't change with scale
- Adjust cooking times accordingly

---

## 🛠️ Customization

### Add Your Own Fields
The converter can be modified to add:
- Allergen information
- Nutritional data
- Prep time / Cook time
- Equipment needed
- Skill level required

### Modify Template
Edit `standardize_recipes.py` to customize:
- Header fields
- Ingredient table columns
- Calculation formulas
- Styling and formatting

---

## ❓ Troubleshooting

### Issue: Missing Ingredients
**Solution**: Manually add ingredients in the Excel file after conversion

### Issue: Incorrect Extraction
**Solution**: The converter tries its best to extract data, but may need manual verification

### Issue: Costs Not Calculating
**Solution**: Check formulas in Excel, ensure all cells have proper values

### Issue: Upload Errors
**Solution**: Verify file format matches Iterum's requirements exactly

---

## 📈 Next Steps

After converting your recipes:

1. ✅ **Cost all recipes** with current ingredient prices
2. ✅ **Upload to Iterum** Chef's Notebook
3. ✅ **Calculate menu pricing** based on target FC%
4. ✅ **Track recipe sources** using `track_recipe_sources.py`
5. ✅ **Update regularly** as prices change

---

## 🎉 You're Ready!

Your recipes are now in professional Iterum format:
- ✓ Uniform structure
- ✓ Ready for costing
- ✓ Professional presentation
- ✓ Upload-ready for Iterum Chef's Notebook

**Start converting:** `py standardize_recipes.py --auto`

---

## 📚 Additional Resources

- **Iterum Documentation**: [Your Iterum manual/guide]
- **USDA Yield Tables**: For produce and protein yields
- **Recipe Costing Guide**: Professional costing methods
- **Menu Engineering**: Pricing strategies and optimization

---

**Happy Costing! 📊💰**

