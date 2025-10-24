/**
 * Kitchen Management System
 * Features available to all users, but data is user-specific
 * - Recipe Book PDF Generator
 * - Build Sheets
 * - Pre-Service Quality Checklists
 * - Next Day Prep Lists
 * - Recipe Version Tracking
 */

class KitchenManagementSystem {
  constructor() {
    this.userId = null;
    this.userEmail = null;
    this.currentRecipes = [];
    this.currentMenu = null;
    this.pdfGenerator = new RecipeBookPDFGenerator();
    this.versionTracker = new RecipeVersionTracker();
  }

  /**
   * Initialize for current user
   */
  async init(userId, userEmail) {
    this.userId = userId;
    this.userEmail = userEmail;
    
    console.log(`🔧 Kitchen Management System initialized for ${userEmail}`);
    
    // Load user's recipes and menu
    await this.loadUserData();
  }

  /**
   * Load user-specific data
   */
  async loadUserData() {
    try {
      // Load recipes from universal recipe manager (user-specific)
      if (window.universalRecipeManager) {
        this.currentRecipes = window.universalRecipeManager.getAllRecipes();
      } else {
        // Fallback to localStorage (filtered by user)
        const allRecipes = JSON.parse(localStorage.getItem('recipes') || '[]');
        this.currentRecipes = allRecipes.filter(r => r.userId === this.userId);
      }

      // Load user's menu
      const menuKey = `menu_${this.userId}`;
      this.currentMenu = JSON.parse(localStorage.getItem(menuKey) || 'null');

      console.log(`📊 Loaded ${this.currentRecipes.length} recipes for user`);
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  }

  /**
   * Generate Recipe Book PDF
   */
  async generateRecipeBookPDF(options = {}) {
    const {
      includeComponents = true,
      includePhotos = false,
      includeNutrition = true,
      includeCosts = false,
      format = 'standard' // 'standard', 'compact', 'full'
    } = options;

    console.log('📕 Generating Recipe Book PDF...');

    return await this.pdfGenerator.generate({
      recipes: this.currentRecipes,
      menu: this.currentMenu,
      userId: this.userId,
      userEmail: this.userEmail,
      includeComponents,
      includePhotos,
      includeNutrition,
      includeCosts,
      format
    });
  }

  /**
   * Generate Build Sheet for specific recipe
   */
  generateBuildSheet(recipeId) {
    const recipe = this.currentRecipes.find(r => r.id === recipeId);
    
    if (!recipe) {
      console.error('Recipe not found:', recipeId);
      return null;
    }

    const buildSheet = {
      recipeName: recipe.title || recipe.name,
      recipeId: recipe.id,
      version: recipe.version || '1.0',
      generatedDate: new Date().toISOString(),
      generatedBy: this.userEmail,
      
      // Recipe Overview
      category: recipe.category,
      servings: recipe.servings || 1,
      prepTime: recipe.prepTime,
      cookTime: recipe.cookTime,
      totalTime: (recipe.prepTime || 0) + (recipe.cookTime || 0),
      difficulty: recipe.difficulty,
      
      // Components with par levels
      components: (recipe.components || []).map(comp => ({
        name: comp.name,
        dailyPar: comp.dailyPar || 'N/A',
        yield: comp.yield || 'N/A',
        portionSize: comp.portionSize || 'N/A',
        shelfLife: comp.shelfLife || 'Unknown',
        ingredients: comp.ingredients || [],
        instructions: comp.instructions || []
      })),
      
      // Ingredients
      ingredients: recipe.ingredients || [],
      
      // Instructions
      instructions: recipe.instructions || [],
      
      // Plating
      plating: recipe.plating || [],
      
      // Quality Standards
      qualityChecks: [
        'Check ingredient freshness',
        'Verify proper storage temperatures',
        'Confirm proper mise en place',
        'Taste and season appropriately',
        'Verify plating consistency',
        'Check portion sizes'
      ],
      
      // Equipment Needed
      equipment: recipe.equipmentNeeded || recipe.equipment || [],
      
      // Allergens & Dietary
      allergens: recipe.allergens || [],
      dietary: recipe.dietary || []
    };

    return buildSheet;
  }

  /**
   * Generate Pre-Service Quality Checklist
   */
  generatePreServiceChecklist(date = new Date()) {
    const checklist = {
      date: date.toISOString().split('T')[0],
      generatedBy: this.userEmail,
      restaurant: this.currentMenu?.projectName || 'Restaurant',
      
      sections: [
        {
          name: 'Equipment Check',
          items: [
            { task: 'All cooking equipment functioning properly', checked: false },
            { task: 'Refrigeration temperatures correct (33-40°F)', checked: false },
            { task: 'Freezer temperatures correct (0°F or below)', checked: false },
            { task: 'Ovens calibrated and preheated', checked: false },
            { task: 'All small equipment clean and ready', checked: false },
            { task: 'Fire suppression system checked', checked: false }
          ]
        },
        {
          name: 'Ingredient Quality',
          items: [
            { task: 'All ingredients within shelf life', checked: false },
            { task: 'Proper FIFO (First In, First Out) rotation', checked: false },
            { task: 'All proteins at proper temperature', checked: false },
            { task: 'Fresh herbs and vegetables trimmed', checked: false },
            { task: 'All sauces and components prepared', checked: false },
            { task: 'Inventory levels adequate for service', checked: false }
          ]
        },
        {
          name: 'Prep Station Readiness',
          items: [
            { task: 'All stations fully stocked', checked: false },
            { task: 'Mise en place complete for each station', checked: false },
            { task: 'Backup ingredients accessible', checked: false },
            { task: 'Garnishes prepped and ready', checked: false },
            { task: 'Plates and serving vessels clean', checked: false },
            { task: 'Station cleanliness verified', checked: false }
          ]
        },
        {
          name: 'Recipe Components',
          items: this.currentRecipes.flatMap(recipe => 
            (recipe.components || []).map(comp => ({
              task: `${comp.name} - Par: ${comp.dailyPar || 'N/A'}`,
              checked: false,
              shelfLife: comp.shelfLife
            }))
          ).slice(0, 10) // Limit to top 10 for checklist
        },
        {
          name: 'Safety & Sanitation',
          items: [
            { task: 'All surfaces sanitized', checked: false },
            { task: 'Hand washing stations stocked', checked: false },
            { task: 'Proper hair restraints available', checked: false },
            { task: 'Clean aprons and towels ready', checked: false },
            { task: 'First aid kit accessible and stocked', checked: false },
            { task: 'Emergency exits clear', checked: false }
          ]
        },
        {
          name: 'Service Setup',
          items: [
            { task: 'All recipes reviewed by team', checked: false },
            { task: 'Daily specials communicated', checked: false },
            { task: '86\'d items noted', checked: false },
            { task: 'Timing and plating reviewed', checked: false },
            { task: 'Team briefing completed', checked: false },
            { task: 'Communication systems tested', checked: false }
          ]
        }
      ]
    };

    return checklist;
  }

  /**
   * Generate Next Day Prep List
   */
  generateNextDayPrepList(targetDate = null) {
    if (!targetDate) {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      targetDate = tomorrow;
    }

    const prepList = {
      prepDate: targetDate.toISOString().split('T')[0],
      generatedDate: new Date().toISOString(),
      generatedBy: this.userEmail,
      restaurant: this.currentMenu?.projectName || 'Restaurant',
      
      components: [],
      shopping: [],
      notes: []
    };

    // Gather all components from recipes
    this.currentRecipes.forEach(recipe => {
      if (recipe.components && Array.isArray(recipe.components)) {
        recipe.components.forEach(comp => {
          prepList.components.push({
            recipeName: recipe.title || recipe.name,
            componentName: comp.name,
            dailyPar: comp.dailyPar || 'N/A',
            yield: comp.yield || 'N/A',
            shelfLife: comp.shelfLife || 'Unknown',
            ingredients: comp.ingredients || [],
            instructions: comp.instructions || [],
            priority: this.calculatePriority(comp.shelfLife)
          });
        });
      }
    });

    // Sort by priority (shorter shelf life = higher priority)
    prepList.components.sort((a, b) => b.priority - a.priority);

    // Generate shopping list from ingredients
    const ingredientMap = new Map();
    
    prepList.components.forEach(comp => {
      comp.ingredients.forEach(ing => {
        const key = ing.name || ing.ingredientName;
        if (ingredientMap.has(key)) {
          const existing = ingredientMap.get(key);
          existing.quantity += ing.quantity || 0;
        } else {
          ingredientMap.set(key, {
            name: key,
            quantity: ing.quantity || 0,
            unit: ing.unit || '',
            category: ing.category || 'Misc'
          });
        }
      });
    });

    prepList.shopping = Array.from(ingredientMap.values())
      .sort((a, b) => a.category.localeCompare(b.category));

    // Add prep notes
    prepList.notes = [
      'Check inventory before starting prep',
      'Verify all equipment is functioning',
      'Prepare long shelf-life items first',
      'Label all containers with date and time',
      'Follow FIFO rotation',
      'Taste and adjust seasoning',
      'Store at proper temperatures'
    ];

    return prepList;
  }

  /**
   * Calculate priority based on shelf life
   */
  calculatePriority(shelfLife) {
    if (!shelfLife || typeof shelfLife !== 'string') return 1;
    
    const lower = shelfLife.toLowerCase();
    
    if (lower.includes('1 day') || lower.includes('same day')) return 5;
    if (lower.includes('2 day') || lower.includes('3 day')) return 4;
    if (lower.includes('week') || lower.includes('5 day')) return 3;
    if (lower.includes('month')) return 2;
    return 1;
  }

  /**
   * Get recipe version history
   */
  getVersionHistory(recipeId) {
    return this.versionTracker.getHistory(recipeId);
  }

  /**
   * Save new recipe version
   */
  saveRecipeVersion(recipe, changes) {
    return this.versionTracker.saveVersion(recipe, changes, this.userEmail);
  }

  /**
   * Export all kitchen documents as ZIP
   */
  async exportKitchenDocuments() {
    console.log('📦 Exporting all kitchen documents...');
    
    const documents = {
      recipeBook: await this.generateRecipeBookPDF(),
      buildSheets: this.currentRecipes.map(r => this.generateBuildSheet(r.id)),
      preServiceChecklist: this.generatePreServiceChecklist(),
      prepList: this.generateNextDayPrepList()
    };

    return documents;
  }
}

/**
 * Recipe Book PDF Generator
 */
class RecipeBookPDFGenerator {
  async generate(options) {
    const {
      recipes,
      menu,
      userId,
      userEmail,
      includeComponents,
      includePhotos,
      includeNutrition,
      includeCosts,
      format
    } = options;

    console.log(`📕 Generating ${format} recipe book for ${userEmail}...`);

    // Create PDF structure
    const pdfData = {
      metadata: {
        title: `${menu?.name || 'Recipe Book'}`,
        author: userEmail,
        subject: 'Professional Recipe Collection',
        keywords: 'recipes, cooking, kitchen, chef',
        creator: 'Iterum Culinary App',
        producer: 'Iterum Kitchen Management System',
        creationDate: new Date()
      },
      
      coverPage: {
        title: menu?.name || 'Recipe Book',
        subtitle: menu?.description || 'Professional Recipe Collection',
        author: userEmail,
        date: new Date().toLocaleDateString(),
        logo: '🍃 Iterum'
      },
      
      tableOfContents: recipes.map((recipe, index) => ({
        title: recipe.title || recipe.name,
        category: recipe.category,
        pageNumber: index + 1
      })),
      
      recipes: recipes.map(recipe => this.formatRecipeForPDF(recipe, {
        includeComponents,
        includePhotos,
        includeNutrition,
        includeCosts,
        format
      })),
      
      appendix: {
        ingredientsIndex: this.generateIngredientsIndex(recipes),
        equipmentList: this.generateEquipmentList(recipes),
        allergenMatrix: this.generateAllergenMatrix(recipes)
      }
    };

    return pdfData;
  }

  formatRecipeForPDF(recipe, options) {
    return {
      title: recipe.title || recipe.name,
      category: recipe.category,
      description: recipe.description,
      servings: recipe.servings,
      prepTime: recipe.prepTime,
      cookTime: recipe.cookTime,
      totalTime: (recipe.prepTime || 0) + (recipe.cookTime || 0),
      difficulty: recipe.difficulty,
      
      components: options.includeComponents ? recipe.components : undefined,
      ingredients: recipe.ingredients,
      instructions: recipe.instructions,
      plating: recipe.plating,
      
      nutrition: options.includeNutrition ? recipe.nutrition : undefined,
      costs: options.includeCosts ? recipe.costs : undefined,
      photo: options.includePhotos ? recipe.photo : undefined,
      
      allergens: recipe.allergens,
      dietary: recipe.dietary,
      equipment: recipe.equipment,
      
      notes: recipe.notes,
      version: recipe.version,
      lastUpdated: recipe.updatedAt
    };
  }

  generateIngredientsIndex(recipes) {
    const ingredientMap = new Map();
    
    recipes.forEach(recipe => {
      (recipe.ingredients || []).forEach(ing => {
        const name = ing.name || ing.ingredientName;
        if (!ingredientMap.has(name)) {
          ingredientMap.set(name, []);
        }
        ingredientMap.get(name).push(recipe.title || recipe.name);
      });
    });

    return Array.from(ingredientMap.entries())
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([ingredient, recipesUsedIn]) => ({
        ingredient,
        recipesUsedIn: [...new Set(recipesUsedIn)]
      }));
  }

  generateEquipmentList(recipes) {
    const equipmentSet = new Set();
    
    recipes.forEach(recipe => {
      (recipe.equipment || []).forEach(equip => {
        equipmentSet.add(equip.name || equip);
      });
    });

    return Array.from(equipmentSet).sort();
  }

  generateAllergenMatrix(recipes) {
    const matrix = {};
    
    recipes.forEach(recipe => {
      matrix[recipe.title || recipe.name] = recipe.allergens || [];
    });

    return matrix;
  }
}

/**
 * Recipe Version Tracker
 */
class RecipeVersionTracker {
  constructor() {
    this.storageKey = 'recipe_versions';
  }

  saveVersion(recipe, changes, userEmail) {
    const versions = this.loadAllVersions();
    const recipeId = recipe.id;

    if (!versions[recipeId]) {
      versions[recipeId] = [];
    }

    const version = {
      versionNumber: versions[recipeId].length + 1,
      timestamp: new Date().toISOString(),
      modifiedBy: userEmail,
      changes: changes || 'Recipe updated',
      snapshot: JSON.parse(JSON.stringify(recipe)) // Deep copy
    };

    versions[recipeId].push(version);
    
    // Keep only last 20 versions per recipe
    if (versions[recipeId].length > 20) {
      versions[recipeId] = versions[recipeId].slice(-20);
    }

    localStorage.setItem(this.storageKey, JSON.stringify(versions));
    
    console.log(`📝 Saved version ${version.versionNumber} of recipe ${recipe.title || recipe.name}`);
    
    return version;
  }

  getHistory(recipeId) {
    const versions = this.loadAllVersions();
    return versions[recipeId] || [];
  }

  loadAllVersions() {
    try {
      return JSON.parse(localStorage.getItem(this.storageKey) || '{}');
    } catch (error) {
      console.error('Error loading versions:', error);
      return {};
    }
  }

  compareVersions(recipeId, version1, version2) {
    const history = this.getHistory(recipeId);
    const v1 = history.find(v => v.versionNumber === version1);
    const v2 = history.find(v => v.versionNumber === version2);

    if (!v1 || !v2) {
      return null;
    }

    return {
      version1: v1,
      version2: v2,
      differences: this.findDifferences(v1.snapshot, v2.snapshot)
    };
  }

  findDifferences(obj1, obj2) {
    const diffs = [];
    
    Object.keys(obj1).forEach(key => {
      if (JSON.stringify(obj1[key]) !== JSON.stringify(obj2[key])) {
        diffs.push({
          field: key,
          oldValue: obj1[key],
          newValue: obj2[key]
        });
      }
    });

    return diffs;
  }
}

// Initialize global instance
window.kitchenManagementSystem = new KitchenManagementSystem();

// Auto-initialize when user authenticates
window.addEventListener('userAuthenticated', (event) => {
  if (event.detail && event.detail.userId) {
    window.kitchenManagementSystem.init(
      event.detail.userId,
      event.detail.email || event.detail.userEmail
    );
  }
});

console.log('🔧 Kitchen Management System loaded');

