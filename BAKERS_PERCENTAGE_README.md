# 🍞 Baker's Percentage Recipe Scaling System

A professional recipe scaling system that uses baker's percentage method for accurate scaling of larger batches - the industry standard for professional baking and cooking.

## ✨ Why Baker's Percentage is Better

**Traditional Scaling Problems:**
- Simple multiplication can lead to rounding errors
- Ingredient ratios can become unbalanced in large batches
- Difficult to adjust individual ingredients while maintaining balance

**Baker's Percentage Advantages:**
- ✅ **More Accurate**: Maintains precise ratios regardless of batch size
- ✅ **Professional Standard**: Used by commercial bakeries worldwide
- ✅ **Flexible**: Easy to adjust individual ingredients while keeping proportions
- ✅ **Scalable**: Perfect for scaling from home batches to commercial production
- ✅ **Standardized**: Consistent results across different batch sizes

## 🚀 Features

### 📊 Professional Scaling Methods
- **Percentage Scaling**: Scale by percentage (e.g., 150% for 1.5x batch)
- **Factor Scaling**: Scale by multiplication factor (e.g., 2.5x)
- **Target Amount**: Scale to specific weight of base ingredient
- **Batch Count**: Scale by number of batches needed

### 🎯 Recipe Validation
- **Hydration Analysis**: Automatic calculation for bread recipes
- **Salt Percentage**: Validation of salt content (1.5-3% recommended)
- **Yeast Percentage**: Check yeast levels for proper fermentation
- **Professional Warnings**: Industry-standard recommendations

### 📐 Unit Conversion System
**Weight Units:**
- Grams (g) - Base unit for precision
- Kilograms (kg)
- Ounces (oz)
- Pounds (lb)

**Volume Units (with ingredient-specific conversions):**
- Cups (flour, sugar, butter, liquid)
- Tablespoons (tbsp)
- Teaspoons (tsp)

### 🍞 Quick Start Templates
- **Basic Bread**: Flour, water, yeast, salt
- **Pizza Dough**: Italian-style with 00 flour
- **Pastry Dough**: Butter, flour, water for laminated doughs

## 📋 How It Works

### 1. Set Base Ingredient (100%)
The base ingredient (typically flour) is set to 100%. All other ingredients are calculated as percentages of this base.

**Example:**
```
Flour: 1000g (100%)
Water: 650g (65%)
Salt: 20g (2%)
Yeast: 7g (0.7%)
```

### 2. Scale the Recipe
Choose your scaling method and value. The system maintains all percentages while scaling absolute amounts.

**Scaling to 300%:**
```
Flour: 3000g (100%)
Water: 1950g (65%)
Salt: 60g (2%)
Yeast: 21g (0.7%)
```

### 3. Validation & Feedback
Get professional feedback on your recipe:
- Hydration levels for bread doughs
- Salt and yeast percentages
- Recommendations for improvements

## 🔧 Technical Implementation

### Frontend (`recipe-scaling-tool.html`)
- Interactive web interface
- Real-time calculations
- Visual feedback and validation
- Export functionality (CSV, JSON, text)

### JavaScript Engine (`bakers_percentage_calculator.js`)
- Professional calculation engine
- Unit conversion system
- Recipe validation logic
- Export/import functionality

### Backend API (`app/routers/recipe_scaling.py`)
- RESTful API endpoints
- Recipe storage and retrieval
- Scaling history tracking
- Professional validation algorithms

## 🚀 Getting Started

### 1. Access the Tool
Visit: `http://localhost:8080/recipe-scaling-tool.html`

### 2. Quick Start
1. **Load a Template**: Click on Bread, Pizza, or Pastry template
2. **Review Ingredients**: See the baker's percentages calculated
3. **Scale Recipe**: Choose percentage, factor, or target amount
4. **Get Results**: View scaled recipe with validation

### 3. Create Custom Recipe
1. **Set Base Ingredient**: Enter flour amount and unit
2. **Add Ingredients**: Add water, salt, yeast, etc. with amounts
3. **Review Percentages**: See calculated baker's percentages
4. **Scale as Needed**: Use any scaling method
5. **Export Recipe**: Save as CSV, JSON, or text

## 📊 Example: Scaling Bread Recipe

### Original Recipe (1000g flour base):
```
Bread Flour: 1000g (100.0%)
Water: 650g (65.0%)
Salt: 20g (2.0%)
Active Dry Yeast: 7g (0.7%)
Total: 1677g
```

### Scaled to 300% (3000g flour):
```
Bread Flour: 3000g (100.0%)
Water: 1950g (65.0%)
Salt: 60g (2.0%)
Active Dry Yeast: 21g (0.7%)
Total: 5031g
```

### Validation Results:
- ✅ **Hydration**: 65% (Good for artisan bread)
- ✅ **Salt**: 2% (Perfect for flavor and fermentation)
- ✅ **Yeast**: 0.7% (Good for long fermentation)

## 🔌 API Endpoints

### Core Scaling
- `POST /api/recipe-scaling/calculate-percentage` - Calculate baker's percentages
- `POST /api/recipe-scaling/scale-recipe` - Scale a recipe
- `POST /api/recipe-scaling/validate-recipe` - Validate recipe proportions

### Recipe Management
- `POST /api/recipe-scaling/save-recipe` - Save recipe to database
- `GET /api/recipe-scaling/recipes` - List all saved recipes
- `GET /api/recipe-scaling/recipes/{id}` - Get specific recipe

### Utilities
- `GET /api/recipe-scaling/conversion-factors` - Get unit conversions
- `GET /api/recipe-scaling/scaling-history` - View scaling history
- `GET /api/recipe-scaling/health` - System health check

## 💡 Pro Tips

### For Home Bakers
- **Start Small**: Test new recipes at 50% scale first
- **Use Weights**: Grams are more accurate than volume measurements
- **Save Templates**: Create templates for your favorite base recipes

### For Commercial Use
- **Scale Gradually**: Test at 200%, then 500% before full commercial scale
- **Document Everything**: Use export features to keep records
- **Monitor Ratios**: Check validation warnings for large batches

### Best Practices
- **Flour First**: Always use flour as your base ingredient (100%)
- **Weigh Ingredients**: Use a digital scale for accuracy
- **Check Hydration**: Important for dough texture and handling
- **Validate Salt**: 1.5-3% is optimal for most bread recipes

## 🛠️ Integration

### With Auto-Save System
The baker's percentage tool integrates with the auto-save system to preserve your work when navigating between screens.

### With Recipe Library
Save scaled recipes directly to your recipe library for future use.

### With Menu Builder
Use scaled recipes in menu planning and cost calculation.

## 📈 Benefits for Large Batches

### Traditional Method Issues:
- 10x recipe: 1 cup flour → 10 cups (but what about the 1.5 tsp salt?)
- Rounding errors accumulate
- Ingredient balance can be lost

### Baker's Percentage Solution:
- 10x recipe: All percentages stay exact
- No rounding errors in ratios
- Perfect balance maintained at any scale

**Example - 10x Scaling:**
```
Original: 500g flour, 325g water, 10g salt
Traditional 10x: 5000g flour, 3250g water, 100g salt
Baker's % 10x: 5000g flour, 3250g water, 100g salt ✓

But what about 7.3x scaling?
Traditional: Complex calculations, rounding errors
Baker's %: 3650g flour, 2372.5g water, 73g salt ✓
```

## 🎯 Future Enhancements

- **Recipe Cost Calculation**: Integration with ingredient pricing
- **Nutritional Analysis**: Automatic nutritional facts for scaled recipes
- **Production Planning**: Timeline and equipment requirements
- **Quality Control**: Track batch consistency and results
- **Mobile App**: Dedicated mobile interface for kitchen use

---

*Baker's Percentage Scaling System - Part of Iterum R&D Chef Notebook Professional Recipe Development Platform*