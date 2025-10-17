# 🍽️ Menu Builder Enhancement Plan

## Overview
Transform the menu builder from a basic import tool into a comprehensive menu management system fully integrated with the recipe development workflow.

---

## 🎯 Core Objectives

### 1. **Seamless Recipe Integration**
- Automatically create recipe stubs for new menu items
- Link menu items to existing recipes
- Track recipe completion status
- Quick navigation between menu items and recipes

### 2. **Intelligent Pricing & Costing**
- Auto-calculate costs based on recipe ingredients
- Suggest pricing based on target food cost %
- Display profit margins
- Highlight unprofitable items

### 3. **Enhanced Menu Creation**
- Modern drag-and-drop interface
- Menu templates (breakfast, lunch, dinner, etc.)
- Seasonal menu variants
- Menu versioning and history

### 4. **Professional Output**
- Generate printable menus (PDF)
- Export for online ordering systems
- QR code generation for digital menus
- Multiple format exports (JSON, CSV, PDF)

---

## 🚀 Key Features to Implement

### Phase 1: Recipe Integration (PRIORITY)

#### A. Auto-Create Recipe Stubs
```
When adding new menu item:
1. Create draft recipe in recipe library
2. Link menu item to recipe
3. Set recipe status: "Menu Item - Draft"
4. Pre-fill:
   - Recipe name = Menu item name
   - Description = Menu description
   - Category = Menu category
   - Target cost = Based on price / desired food cost %
```

#### B. Recipe Status Tracking
```
Menu Item Status:
- 🔴 No Recipe - Needs development
- 🟡 Draft Recipe - In progress
- 🟢 Complete Recipe - Ready to cook
- 🔵 Costed Recipe - Full costing done
```

#### C. Quick Navigation
```
From Menu Builder:
- "Edit Recipe" button → Opens recipe developer
- "View Costing" button → Shows ingredient costs
- "Recipe Status" badge → Visual indicator
```

---

### Phase 2: Smart Pricing & Costing

#### A. Automatic Cost Calculation
```
For items with complete recipes:
1. Sum ingredient costs from inventory
2. Add prep time labor cost
3. Calculate total COGS
4. Show actual food cost %
5. Highlight items over target %
```

#### B. Pricing Recommendations
```
Smart pricing engine:
- Target food cost: 28-32%
- Labor cost consideration
- Market rate comparison
- Competitor analysis placeholder
- Profitability alerts
```

#### C. Menu Analytics Dashboard
```
Display:
- Total menu items
- Items with recipes: X/Y
- Average food cost %
- Most/least profitable items
- Items needing attention
```

---

### Phase 3: Modern Menu Builder UI

#### A. Visual Menu Designer
```
Drag-and-drop interface:
- Reorder menu items
- Organize into sections
- Visual category grouping
- Real-time preview
```

#### B. Menu Templates
```
Pre-built templates:
- Fine Dining Tasting Menu
- Casual Restaurant Menu
- Café Menu (Breakfast/Lunch)
- Bar & Appetizer Menu
- Dessert Menu
- Kids Menu
- Seasonal Specials
```

#### C. Menu Versions
```
Version management:
- Spring 2025 Menu
- Summer 2025 Menu
- Holiday Menu
- Private Event Menu
- Save/restore previous versions
```

---

### Phase 4: Professional Output

#### A. PDF Generation
```
Export formats:
- Single-page menu
- Tri-fold menu
- Table tent
- Digital display
- Print-ready with bleeds
```

#### B. Digital Menu Features
```
Generate:
- QR codes for tables
- Online menu widget
- JSON for POS systems
- CSV for inventory systems
```

---

## 📋 Implementation Checklist

### Immediate (Today):
- [x] Enhanced header UI matching other pages
- [ ] Auto-create recipe stubs for new menu items
- [ ] Recipe status badges on menu items
- [ ] Quick "Edit Recipe" buttons
- [ ] Recipe completion tracker

### Short-term (This Week):
- [ ] Smart cost calculation from recipes
- [ ] Food cost % display
- [ ] Pricing recommendations
- [ ] Menu analytics dashboard
- [ ] Template system

### Medium-term (Next Week):
- [ ] Drag-and-drop menu designer
- [ ] Menu versioning
- [ ] PDF export
- [ ] Digital menu QR codes
- [ ] Advanced filtering

### Long-term (Future):
- [ ] Multi-location menu management
- [ ] A/B testing menus
- [ ] Sales data integration
- [ ] Seasonal auto-switching
- [ ] AI menu optimization

---

## 🔗 Integration Points

### With Recipe System:
```javascript
// When adding menu item
async function addMenuItemWithRecipe(itemData) {
  // 1. Create recipe stub
  const recipe = await createRecipeStub({
    title: itemData.name,
    description: itemData.description,
    category: itemData.category,
    status: 'draft',
    type: 'dish',
    tags: ['menu-item', itemData.category],
    source: 'Menu Builder'
  });
  
  // 2. Link to menu item
  itemData.recipeId = recipe.id;
  itemData.recipeStatus = 'draft';
  
  // 3. Save menu item
  await saveMenuItem(itemData);
  
  // 4. Show success
  showToast('Menu item added! Recipe draft created.');
}
```

### With Ingredient System:
```javascript
// Calculate costs from ingredients
async function calculateMenuItemCost(menuItem) {
  const recipe = await getRecipe(menuItem.recipeId);
  let totalCost = 0;
  
  for (const ingredient of recipe.ingredients) {
    const cost = await getIngredientCost(ingredient.name);
    totalCost += cost * ingredient.quantity;
  }
  
  return {
    cost: totalCost,
    price: menuItem.price,
    foodCostPercent: (totalCost / menuItem.price) * 100,
    profit: menuItem.price - totalCost
  };
}
```

### With Project System:
```javascript
// Menus are project-specific
const currentProject = window.projectManager.getCurrentProject();
const menuKey = `menu_${currentProject.id}`;
```

---

## 💾 Data Structure

### Menu Item Schema:
```json
{
  "id": "menu_item_123",
  "name": "Grilled Salmon",
  "description": "Wild-caught salmon with lemon butter",
  "category": "Main Courses",
  "price": 28.00,
  "recipeId": "recipe_456",
  "recipeStatus": "draft", // draft, complete, costed
  "hasRecipe": true,
  "costData": {
    "ingredientCost": 8.40,
    "laborCost": 2.50,
    "totalCost": 10.90,
    "foodCostPercent": 38.9,
    "targetPercent": 30.0,
    "profit": 17.10
  },
  "metadata": {
    "tags": ["signature", "gluten-free"],
    "allergens": ["fish"],
    "prepTime": 15,
    "dietary": ["pescatarian"],
    "spiceLevel": "mild"
  },
  "availability": {
    "seasonal": false,
    "daysAvailable": ["all"],
    "mealPeriods": ["dinner"]
  },
  "createdAt": "2025-01-01T12:00:00Z",
  "updatedAt": "2025-01-01T12:00:00Z"
}
```

---

## 🎨 UI Improvements

### Menu Item Card Design:
```
┌─────────────────────────────────────┐
│ 🍽️ Grilled Salmon         $28.00  │
├─────────────────────────────────────┤
│ Wild-caught salmon with...          │
│                                     │
│ Status: 🟡 Draft Recipe             │
│ Food Cost: 38.9% ⚠️ (Target: 30%)  │
│                                     │
│ [Edit Recipe] [View Cost] [Remove] │
└─────────────────────────────────────┘
```

### Analytics Dashboard:
```
┌─────────────────────────────────────┐
│ 📊 Menu Performance                 │
├─────────────────────────────────────┤
│ Total Items: 42                     │
│ With Recipes: 38/42 (90%)          │
│ Avg Food Cost: 31.5%               │
│ Items Over Target: 8               │
│                                     │
│ [View Problem Items]                │
└─────────────────────────────────────┘
```

---

## 🧪 Testing Plan

### Test Scenarios:
1. ✅ Create menu item → Recipe stub created
2. ✅ Edit recipe → Menu item updates
3. ✅ Complete recipe → Status changes to green
4. ✅ Add ingredients → Cost auto-calculates
5. ✅ Set price → Food cost % updates
6. ✅ Export menu → PDF generates
7. ✅ Switch project → Correct menu loads

---

## 📈 Success Metrics

### User Experience:
- Time to create menu item: < 30 seconds
- Recipe completion rate: > 80%
- Cost accuracy: > 95%
- User satisfaction: 9/10

### System Performance:
- Page load: < 2 seconds
- Cost calculation: < 1 second
- PDF generation: < 5 seconds
- Data sync: Real-time

---

## 🚧 Technical Considerations

### Performance:
- Lazy load recipe data
- Cache cost calculations
- Debounce search/filter
- Paginate large menus

### Data Integrity:
- Validate price > 0
- Ensure recipe links exist
- Handle deleted recipes
- Sync across sessions

### Error Handling:
- Graceful API failures
- Offline support
- Auto-save drafts
- Conflict resolution

---

## 📝 Documentation Needs

### User Guides:
- How to create a menu from scratch
- How to import existing menu
- How to cost menu items
- How to export menus

### Developer Docs:
- API endpoints
- Data schemas
- Integration points
- Extension guide

---

## ✨ Future Enhancements

### AI-Powered Features:
- Menu item name suggestions
- Description generation
- Price optimization
- Seasonal recommendations

### Advanced Analytics:
- Sales integration
- Popularity tracking
- Profitability trends
- Customer feedback

### Multi-Channel:
- POS integration
- Online ordering sync
- Third-party delivery
- Reservation systems

---

**Status:** Ready for Implementation  
**Priority:** HIGH  
**Timeline:** Phase 1 (Today), Phase 2-3 (This Week), Phase 4 (Next Week)

