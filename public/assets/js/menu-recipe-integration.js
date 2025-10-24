/**
 * Menu-Recipe Integration System
 * Automatically creates recipe stubs for menu items and manages the connection
 */

class MenuRecipeIntegration {
  constructor() {
    this.storageKey = 'menu_recipe_links';
    this.recipeStubsKey = 'recipe_stubs';
    this.init();
  }

  init() {
    console.log('🔗 Menu-Recipe Integration initialized');
  }

  /**
   * Create a recipe stub for a menu item
   */
  async createRecipeStubForMenuItem(menuItem) {
    try {
      console.log('📝 Creating recipe stub for:', menuItem.name);

      const recipeStub = {
        id: `recipe_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        title: menuItem.name,
        description: menuItem.description || `Recipe for ${menuItem.name}`,
        category: menuItem.category || 'Uncategorized',
        cuisine_type: this.guessCuisineType(menuItem),
        difficulty_level: 'Medium',
        prep_time: null,
        cook_time: null,
        servings: 4,
        tags: ['menu-item', menuItem.category?.toLowerCase() || 'uncategorized'],
        dietary_restrictions: [],
        allergens: [],
        equipment_needed: [],
        status: 'draft',
        recipe_status: 'needs-development',
        type: 'dish',
        source: 'Menu Builder',
        
        // Menu item link
        menuItemId: menuItem.id,
        menuItemName: menuItem.name,
        menuItemPrice: menuItem.price,
        
        // Target costing
        targetFoodCostPercent: 30,
        targetCost: menuItem.price ? (menuItem.price * 0.30).toFixed(2) : null,
        
        // Recipe data (empty initially)
        ingredients: [],
        instructions: [],
        
        // Metadata
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        createdBy: this.getCurrentUserId(),
        projectId: this.getCurrentProjectId()
      };

      // Save recipe stub
      await this.saveRecipeStub(recipeStub);

      // Link menu item to recipe
      await this.linkMenuItemToRecipe(menuItem.id, recipeStub.id);

      // Track analytics
      if (window.analyticsTracker) {
        window.analyticsTracker.trackCustomEvent('recipe_stub_created', {
          menu_item: menuItem.name,
          recipe_id: recipeStub.id,
          category: menuItem.category
        });
      }

      console.log('✅ Recipe stub created:', recipeStub.id);
      return recipeStub;

    } catch (error) {
      console.error('❌ Error creating recipe stub:', error);
      throw error;
    }
  }

  /**
   * Save recipe stub to localStorage and sync to backend
   */
  async saveRecipeStub(recipeStub) {
    // Save to localStorage
    const stubs = this.getRecipeStubs();
    stubs.push(recipeStub);
    localStorage.setItem(this.recipeStubsKey, JSON.stringify(stubs));

    // Also add to main recipes if recipe library exists
    const recipes = JSON.parse(localStorage.getItem('recipes') || '[]');
    recipes.push(recipeStub);
    localStorage.setItem('recipes', JSON.stringify(recipes));

    // Try to sync to backend
    try {
      if (window.authApiHelper && window.authManager?.isAuthenticated()) {
        const response = await window.authApiHelper.post('/api/recipes', {
          title: recipeStub.title,
          description: recipeStub.description,
          cuisine_type: recipeStub.cuisine_type,
          difficulty_level: recipeStub.difficulty_level,
          prep_time: recipeStub.prep_time,
          cook_time: recipeStub.cook_time,
          servings: recipeStub.servings,
          tags: recipeStub.tags,
          status: recipeStub.status,
          type: recipeStub.type,
          source: recipeStub.source
        });
        
        if (response.id) {
          recipeStub.backendId = response.id;
          console.log('✅ Recipe stub synced to backend:', response.id);
        }
      }
    } catch (error) {
      console.warn('⚠️ Could not sync recipe to backend:', error);
      // Continue anyway - we have local copy
    }

    return recipeStub;
  }

  /**
   * Get all recipe stubs
   */
  getRecipeStubs() {
    const stubs = localStorage.getItem(this.recipeStubsKey);
    return stubs ? JSON.parse(stubs) : [];
  }

  /**
   * Get recipe by ID (check stubs and main recipes)
   */
  getRecipeById(recipeId) {
    // Check stubs first
    const stubs = this.getRecipeStubs();
    let recipe = stubs.find(r => r.id === recipeId);
    
    if (!recipe) {
      // Check main recipes
      const recipes = JSON.parse(localStorage.getItem('recipes') || '[]');
      recipe = recipes.find(r => r.id === recipeId);
    }
    
    return recipe;
  }

  /**
   * Link menu item to recipe
   */
  async linkMenuItemToRecipe(menuItemId, recipeId) {
    const links = this.getMenuRecipeLinks();
    links[menuItemId] = {
      recipeId: recipeId,
      linkedAt: new Date().toISOString()
    };
    localStorage.setItem(this.storageKey, JSON.stringify(links));
    console.log('🔗 Linked menu item', menuItemId, 'to recipe', recipeId);
  }

  /**
   * Get all menu-recipe links
   */
  getMenuRecipeLinks() {
    const links = localStorage.getItem(this.storageKey);
    return links ? JSON.parse(links) : {};
  }

  /**
   * Get recipe for a menu item
   */
  getRecipeForMenuItem(menuItemId) {
    const links = this.getMenuRecipeLinks();
    const link = links[menuItemId];
    
    if (!link) {
      return null;
    }
    
    return this.getRecipeById(link.recipeId);
  }

  /**
   * Get recipe status for menu item
   */
  getRecipeStatus(menuItemId) {
    const recipe = this.getRecipeForMenuItem(menuItemId);
    
    if (!recipe) {
      return {
        status: 'no-recipe',
        label: 'No Recipe',
        icon: '🔴',
        color: '#ef4444',
        action: 'Create Recipe'
      };
    }

    // Check if recipe is complete
    const hasIngredients = recipe.ingredients && recipe.ingredients.length > 0;
    const hasInstructions = recipe.instructions && recipe.instructions.length > 0;
    const hasCosting = recipe.ingredients && recipe.ingredients.every(i => i.cost);

    if (hasCosting && hasIngredients && hasInstructions) {
      return {
        status: 'costed',
        label: 'Complete & Costed',
        icon: '🔵',
        color: '#3b82f6',
        action: 'View Recipe',
        recipeId: recipe.id
      };
    }

    if (hasIngredients && hasInstructions) {
      return {
        status: 'complete',
        label: 'Recipe Complete',
        icon: '🟢',
        color: '#22c55e',
        action: 'Add Costing',
        recipeId: recipe.id
      };
    }

    if (hasIngredients || hasInstructions) {
      return {
        status: 'draft',
        label: 'Recipe Draft',
        icon: '🟡',
        color: '#eab308',
        action: 'Complete Recipe',
        recipeId: recipe.id
      };
    }

    return {
      status: 'stub',
      label: 'Needs Development',
      icon: '🟠',
      color: '#f97316',
      action: 'Develop Recipe',
      recipeId: recipe.id
    };
  }

  /**
   * Open recipe in recipe developer
   */
  openRecipeInDeveloper(recipeId) {
    if (!recipeId) {
      console.error('No recipe ID provided');
      return;
    }

    // Store the recipe ID for the developer to load
    sessionStorage.setItem('recipe_to_edit', recipeId);
    
    // Navigate to recipe developer
    window.location.href = 'recipe-developer.html';
  }

  /**
   * Calculate menu item cost from recipe
   */
  calculateMenuItemCost(menuItemId) {
    const recipe = this.getRecipeForMenuItem(menuItemId);
    
    if (!recipe || !recipe.ingredients || recipe.ingredients.length === 0) {
      return {
        hasCost: false,
        ingredientCost: 0,
        laborCost: 0,
        totalCost: 0
      };
    }

    // Sum ingredient costs
    let ingredientCost = 0;
    for (const ingredient of recipe.ingredients) {
      if (ingredient.cost) {
        ingredientCost += parseFloat(ingredient.cost);
      }
    }

    // Estimate labor cost (simple calculation)
    const totalTime = (recipe.prep_time || 0) + (recipe.cook_time || 0);
    const laborRate = 15; // $15/hour
    const laborCost = (totalTime / 60) * laborRate;

    const totalCost = ingredientCost + laborCost;

    return {
      hasCost: true,
      ingredientCost: ingredientCost,
      laborCost: laborCost,
      totalCost: totalCost
    };
  }

  /**
   * Calculate food cost percentage
   */
  calculateFoodCostPercent(menuItem) {
    const cost = this.calculateMenuItemCost(menuItem.id);
    
    if (!cost.hasCost || !menuItem.price || menuItem.price === 0) {
      return null;
    }

    const foodCostPercent = (cost.totalCost / menuItem.price) * 100;
    
    return {
      percent: foodCostPercent.toFixed(1),
      cost: cost.totalCost.toFixed(2),
      price: menuItem.price,
      profit: (menuItem.price - cost.totalCost).toFixed(2),
      isOverTarget: foodCostPercent > 32,
      isGood: foodCostPercent <= 32 && foodCostPercent >= 28
    };
  }

  /**
   * Guess cuisine type from menu item
   */
  guessCuisineType(menuItem) {
    const name = menuItem.name.toLowerCase();
    const desc = (menuItem.description || '').toLowerCase();
    const text = name + ' ' + desc;

    const cuisineKeywords = {
      'Italian': ['pasta', 'pizza', 'risotto', 'italian', 'marinara', 'parmesan'],
      'Asian': ['sushi', 'ramen', 'stir fry', 'asian', 'teriyaki', 'tempura'],
      'Mexican': ['taco', 'burrito', 'quesadilla', 'mexican', 'salsa', 'guacamole'],
      'American': ['burger', 'bbq', 'steak', 'american', 'wings', 'fries'],
      'French': ['french', 'coq au vin', 'ratatouille', 'bouillabaisse'],
      'Mediterranean': ['mediterranean', 'greek', 'hummus', 'falafel', 'tzatziki'],
      'Indian': ['curry', 'tandoori', 'indian', 'naan', 'biryani'],
      'Seafood': ['fish', 'seafood', 'salmon', 'shrimp', 'lobster', 'scallops']
    };

    for (const [cuisine, keywords] of Object.entries(cuisineKeywords)) {
      if (keywords.some(keyword => text.includes(keyword))) {
        return cuisine;
      }
    }

    return 'American';
  }

  /**
   * Get current user ID
   */
  getCurrentUserId() {
    if (window.authManager?.currentUser) {
      return window.authManager.currentUser.userId;
    }
    return 'guest';
  }

  /**
   * Get current project ID
   */
  getCurrentProjectId() {
    if (window.projectManager?.getCurrentProject) {
      const project = window.projectManager.getCurrentProject();
      return project?.id || 'default';
    }
    return 'default';
  }

  /**
   * Update recipe from menu item changes
   */
  async updateRecipeFromMenuItem(menuItem) {
    const recipe = this.getRecipeForMenuItem(menuItem.id);
    
    if (!recipe) {
      return;
    }

    // Update recipe fields that might have changed
    recipe.title = menuItem.name;
    recipe.description = menuItem.description;
    recipe.category = menuItem.category;
    recipe.menuItemPrice = menuItem.price;
    recipe.targetCost = menuItem.price ? (menuItem.price * 0.30).toFixed(2) : null;
    recipe.updatedAt = new Date().toISOString();

    // Save updated recipe
    await this.saveRecipeStub(recipe);

    console.log('✅ Recipe updated from menu item:', recipe.id);
  }

  /**
   * Delete recipe when menu item is deleted
   */
  async deleteRecipeForMenuItem(menuItemId, keepRecipe = false) {
    const links = this.getMenuRecipeLinks();
    const link = links[menuItemId];
    
    if (!link) {
      return;
    }

    if (!keepRecipe) {
      // Remove recipe stub
      const stubs = this.getRecipeStubs();
      const filtered = stubs.filter(r => r.id !== link.recipeId);
      localStorage.setItem(this.recipeStubsKey, JSON.stringify(filtered));

      // Also remove from main recipes
      const recipes = JSON.parse(localStorage.getItem('recipes') || '[]');
      const filteredRecipes = recipes.filter(r => r.id !== link.recipeId);
      localStorage.setItem('recipes', JSON.stringify(filteredRecipes));

      console.log('🗑️ Deleted recipe stub:', link.recipeId);
    }

    // Remove link
    delete links[menuItemId];
    localStorage.setItem(this.storageKey, JSON.stringify(links));

    console.log('🔗 Unlinked menu item:', menuItemId);
  }

  /**
   * Get menu statistics
   */
  getMenuStatistics(menuItems) {
    const stats = {
      totalItems: menuItems.length,
      withRecipes: 0,
      withCompleteRecipes: 0,
      withCosting: 0,
      needsDevelopment: 0,
      averageFoodCost: 0,
      overTargetCount: 0
    };

    let totalFoodCost = 0;
    let itemsWithCost = 0;

    for (const item of menuItems) {
      const status = this.getRecipeStatus(item.id);
      
      if (status.status !== 'no-recipe') {
        stats.withRecipes++;
      }
      
      if (status.status === 'complete' || status.status === 'costed') {
        stats.withCompleteRecipes++;
      }
      
      if (status.status === 'costed') {
        stats.withCosting++;
      }
      
      if (status.status === 'no-recipe' || status.status === 'stub') {
        stats.needsDevelopment++;
      }

      // Calculate food cost
      const costData = this.calculateFoodCostPercent(item);
      if (costData) {
        totalFoodCost += parseFloat(costData.percent);
        itemsWithCost++;
        
        if (costData.isOverTarget) {
          stats.overTargetCount++;
        }
      }
    }

    stats.averageFoodCost = itemsWithCost > 0 
      ? (totalFoodCost / itemsWithCost).toFixed(1) 
      : 0;

    return stats;
  }
}

// Initialize global instance
window.menuRecipeIntegration = new MenuRecipeIntegration();

console.log('🔗 Menu-Recipe Integration loaded');

