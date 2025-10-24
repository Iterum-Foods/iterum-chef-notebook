# 🔄 Professional Recipe Workflow System

## 📋 Workflow Overview

```
📤 UPLOAD → 🔍 VERIFICATION → ✅ APPROVAL → 📚 MASTER LIST → 📁 PROJECT ASSIGNMENT
```

### **Stage 1: Recipe Upload**
- Recipes uploaded via various methods (Word docs, PDFs, manual entry)
- Auto-parsing extracts basic information
- Status: `pending_review`

### **Stage 2: Verification & Enhancement**
- **Review Screen** shows uploaded recipes needing verification
- **Missing Information Highlighted** in red/orange
- **Chef/Manager adds missing details**:
  - Complete ingredient measurements
  - Detailed cooking instructions
  - Allergen information
  - Cost data
  - Nutritional information
  - Cooking techniques

### **Stage 3: Approval & Master List**
- Verified recipes added to **Recipe Master List**
- Status: `approved` 
- Available for use across all projects

### **Stage 4: Project Assignment**
- During verification, select which **project(s)** recipe belongs to
- Recipe automatically added to selected project(s)
- Can be assigned to multiple projects simultaneously

---

## 🎯 Implementation Plan

### **Database Schema Enhancement**
```sql
-- Recipe Status Tracking
ALTER TABLE recipes ADD COLUMN workflow_status VARCHAR(20) DEFAULT 'pending_review';
ALTER TABLE recipes ADD COLUMN reviewed_by INTEGER REFERENCES users(id);
ALTER TABLE recipes ADD COLUMN reviewed_at TIMESTAMP;
ALTER TABLE recipes ADD COLUMN missing_fields JSON; -- Track what needs completion

-- Project-Recipe Assignment
CREATE TABLE recipe_project_assignments (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id),
    project_id INTEGER REFERENCES projects(id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    assigned_by INTEGER REFERENCES users(id)
);
```

### **Verification Interface Components**
```javascript
// Recipe Review Card with missing fields highlighted
class RecipeReviewCard {
    constructor(recipe) {
        this.recipe = recipe;
        this.missingFields = this.identifyMissingFields();
    }
    
    identifyMissingFields() {
        const required = ['ingredients', 'instructions', 'prep_time', 'cook_time', 'servings'];
        const missing = [];
        
        required.forEach(field => {
            if (!this.recipe[field] || this.isEmpty(this.recipe[field])) {
                missing.push(field);
            }
        });
        
        return missing;
    }
    
    render() {
        return `
            <div class="recipe-review-card">
                <h3>${this.recipe.title}</h3>
                <div class="completion-status">
                    ${this.renderCompletionBar()}
                </div>
                <div class="missing-fields">
                    ${this.renderMissingFields()}
                </div>
                <div class="recipe-content">
                    ${this.renderEditableFields()}
                </div>
                <div class="project-assignment">
                    ${this.renderProjectSelector()}
                </div>
                <div class="actions">
                    <button onclick="saveAndApprove(${this.recipe.id})">Approve & Add to Master</button>
                    <button onclick="saveProgress(${this.recipe.id})">Save Progress</button>
                    <button onclick="rejectRecipe(${this.recipe.id})">Reject</button>
                </div>
            </div>
        `;
    }
}
```

---

## 🎨 User Interface Design

### **Recipe Review Dashboard**
```html
<!-- Review Queue -->
<div class="review-dashboard">
    <div class="review-stats">
        <div class="stat-card">
            <h3>12</h3>
            <p>Pending Review</p>
        </div>
        <div class="stat-card">
            <h3>5</h3>
            <p>In Progress</p>
        </div>
        <div class="stat-card">
            <h3>23</h3>
            <p>Approved Today</p>
        </div>
    </div>
    
    <!-- Recipe Cards -->
    <div class="recipe-review-grid">
        <!-- Individual recipe review cards -->
    </div>
</div>
```

### **Recipe Enhancement Form**
```html
<div class="recipe-enhancement-form">
    <!-- Missing fields highlighted -->
    <div class="field-section" data-required="true" data-missing="true">
        <label class="missing-field">Prep Time (Required)</label>
        <input type="text" placeholder="e.g., 15 minutes" class="highlight-missing">
    </div>
    
    <div class="field-section" data-complete="true">
        <label class="complete-field">Ingredients ✓</label>
        <textarea class="complete">2 cups flour...</textarea>
    </div>
    
    <!-- Project Assignment -->
    <div class="project-assignment-section">
        <label>Assign to Projects:</label>
        <div class="project-checkboxes">
            <label><input type="checkbox" value="89-charles"> 89 Charles Cocktail Bar</label>
            <label><input type="checkbox" value="summer-menu"> Summer Menu 2025</label>
            <label><input type="checkbox" value="catering"> Catering Division</label>
        </div>
    </div>
</div>
```

---

## 🔧 Backend API Endpoints

### **Review Management**
```python
# Get recipes pending review
@router.get("/recipes/pending-review")
async def get_pending_recipes(db: Session = Depends(get_db)):
    """Get all recipes waiting for verification"""
    
# Update recipe during review
@router.put("/recipes/{recipe_id}/review")
async def update_recipe_review(recipe_id: int, updates: dict):
    """Update recipe with missing information"""
    
# Approve recipe and add to master list
@router.post("/recipes/{recipe_id}/approve")
async def approve_recipe(recipe_id: int, project_assignments: List[int]):
    """Approve recipe and assign to projects"""
    
# Assign recipe to projects
@router.post("/recipes/{recipe_id}/assign-projects")
async def assign_to_projects(recipe_id: int, project_ids: List[int]):
    """Assign approved recipe to multiple projects"""
```

### **Missing Field Detection**
```python
class RecipeCompletionAnalyzer:
    def analyze_completeness(self, recipe: Recipe) -> Dict[str, Any]:
        """Analyze recipe completeness and identify missing fields"""
        
        missing_fields = []
        completion_score = 0
        
        # Required fields
        required_checks = {
            'title': self.check_title(recipe),
            'ingredients': self.check_ingredients(recipe),
            'instructions': self.check_instructions(recipe),
            'prep_time': self.check_prep_time(recipe),
            'cook_time': self.check_cook_time(recipe),
            'servings': self.check_servings(recipe)
        }
        
        # Optional but recommended fields
        recommended_checks = {
            'allergens': self.check_allergens(recipe),
            'nutrition': self.check_nutrition(recipe),
            'cost_info': self.check_cost_info(recipe),
            'difficulty': self.check_difficulty(recipe),
            'cuisine_type': self.check_cuisine_type(recipe)
        }
        
        # Calculate completion score
        total_fields = len(required_checks) + len(recommended_checks)
        completed_fields = sum(required_checks.values()) + sum(recommended_checks.values())
        completion_score = (completed_fields / total_fields) * 100
        
        # Identify missing required fields
        missing_required = [field for field, complete in required_checks.items() if not complete]
        missing_recommended = [field for field, complete in recommended_checks.items() if not complete]
        
        return {
            'completion_score': completion_score,
            'missing_required': missing_required,
            'missing_recommended': missing_recommended,
            'is_ready_for_approval': len(missing_required) == 0,
            'priority_level': self.calculate_priority(missing_required, missing_recommended)
        }
```

---

## 📱 Frontend Components

### **Review Interface**
```javascript
class RecipeReviewInterface {
    constructor() {
        this.currentRecipe = null;
        this.selectedProjects = [];
    }
    
    async loadPendingRecipes() {
        const recipes = await fetch('/api/recipes/pending-review').then(r => r.json());
        this.renderReviewQueue(recipes);
    }
    
    async saveRecipeChanges(recipeId, updates) {
        const response = await fetch(`/api/recipes/${recipeId}/review`, {
            method: 'PUT',
            body: JSON.stringify(updates),
            headers: {'Content-Type': 'application/json'}
        });
        return response.json();
    }
    
    async approveRecipe(recipeId) {
        const response = await fetch(`/api/recipes/${recipeId}/approve`, {
            method: 'POST',
            body: JSON.stringify({
                project_assignments: this.selectedProjects
            }),
            headers: {'Content-Type': 'application/json'}
        });
        
        if (response.ok) {
            this.showSuccess('Recipe approved and added to master list!');
            this.loadPendingRecipes(); // Refresh the queue
        }
    }
    
    highlightMissingFields(recipe) {
        const analyzer = new RecipeCompletionAnalyzer();
        const analysis = analyzer.analyze(recipe);
        
        analysis.missing_required.forEach(field => {
            document.querySelector(`[data-field="${field}"]`)
                   .classList.add('missing-required');
        });
        
        analysis.missing_recommended.forEach(field => {
            document.querySelector(`[data-field="${field}"]`)
                   .classList.add('missing-recommended');
        });
    }
}
```

### **Visual Status Indicators**
```css
/* Missing field highlighting */
.missing-required {
    border: 2px solid #e74c3c;
    background-color: #fdf2f2;
}

.missing-recommended {
    border: 2px solid #f39c12;
    background-color: #fef9e7;
}

.field-complete {
    border: 2px solid #27ae60;
    background-color: #eafaf1;
}

/* Completion progress bar */
.completion-bar {
    width: 100%;
    height: 8px;
    background-color: #ecf0f1;
    border-radius: 4px;
    overflow: hidden;
}

.completion-progress {
    height: 100%;
    background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #27ae60 100%);
    transition: width 0.3s ease;
}
```

---

## 🎯 Workflow Implementation Steps

### **Phase 1: Review Interface** (Week 1)
1. Create recipe review dashboard
2. Implement missing field detection
3. Add highlighting for incomplete fields
4. Build basic save/approve functionality

### **Phase 2: Project Assignment** (Week 2)
1. Create project selection interface
2. Implement multi-project assignment
3. Add recipe-project relationship tracking
4. Build project-specific recipe views

### **Phase 3: Master List Integration** (Week 3)
1. Create comprehensive recipe master list
2. Add filtering and search capabilities
3. Implement recipe status tracking
4. Add bulk operations for recipe management

### **Phase 4: Advanced Features** (Week 4)
1. Add recipe version control
2. Implement approval workflows
3. Add notification system for pending reviews
4. Create reporting and analytics

---

## 💡 Key Benefits

### **Quality Control**
- ✅ Ensures all recipes meet professional standards
- ✅ Prevents incomplete recipes from reaching production
- ✅ Maintains consistency across all projects

### **Efficiency**
- ✅ Clear visual indicators of missing information
- ✅ Streamlined approval process
- ✅ Bulk project assignment capabilities

### **Organization**
- ✅ Central master list of all approved recipes
- ✅ Project-specific recipe collections
- ✅ Full audit trail of recipe changes

### **Professional Standards**
- ✅ Chef/manager oversight of all recipes
- ✅ Complete nutritional and allergen information
- ✅ Standardized format and presentation

---

## 🚀 Ready to Implement

This workflow system transforms your recipe management from basic upload-and-store to a **professional kitchen-grade quality control system**. 

**Next steps:**
1. Implement the review interface
2. Add missing field detection
3. Create project assignment functionality
4. Test with your "89 Charles" project workflow

**This ensures every recipe in your system is complete, accurate, and ready for professional use! 👨‍🍳🎯**
