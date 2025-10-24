/**
 * Enhanced Menu Manager with Recipe Integration
 * Complete menu management system with automatic recipe creation
 */

class EnhancedMenuManager {
  constructor() {
    this.currentMenu = null;
    this.menuItems = [];
    this.storageKey = 'menu_data';
    this.init();
  }

  async init() {
    console.log('🍽️ Enhanced Menu Manager initialized');
    await this.loadMenu();
    this.setupEventListeners();
  }

  /**
   * Load menu data
   */
  async loadMenu() {
    const projectId = this.getCurrentProjectId();
    const menuKey = `${this.storageKey}_${projectId}`;
    
    const saved = localStorage.getItem(menuKey);
    if (saved) {
      try {
        const data = JSON.parse(saved);
        this.currentMenu = data.menu;
        this.menuItems = data.items || [];
        console.log('📋 Loaded menu with', this.menuItems.length, 'items');
      } catch (error) {
        console.error('Error loading menu:', error);
        this.initializeNewMenu();
      }
    } else {
      this.initializeNewMenu();
    }
    
    this.renderMenuItems();
  }

  /**
   * Initialize new menu
   */
  initializeNewMenu() {
    this.currentMenu = {
      id: `menu_${Date.now()}`,
      name: 'New Menu',
      description: '',
      version: '1.0',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    this.menuItems = [];
  }

  /**
   * Save menu data
   */
  async saveMenu() {
    const projectId = this.getCurrentProjectId();
    const menuKey = `${this.storageKey}_${projectId}`;
    
    const data = {
      menu: this.currentMenu,
      items: this.menuItems
    };
    
    localStorage.setItem(menuKey, JSON.stringify(data));
    console.log('💾 Menu saved:', this.menuItems.length, 'items');
    
    // Analytics
    if (window.analyticsTracker) {
      window.analyticsTracker.trackCustomEvent('menu_saved', {
        items_count: this.menuItems.length,
        project: projectId
      });
    }
  }

  /**
   * Add menu item (with recipe integration)
   */
  async addMenuItem(itemData, createRecipe = true) {
    try {
      // Create menu item
      const menuItem = {
        id: `item_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        name: itemData.name,
        description: itemData.description || '',
        category: itemData.category || 'Main Courses',
        price: parseFloat(itemData.price) || 0,
        allergens: itemData.allergens || [],
        dietaryInfo: itemData.dietaryInfo || [],
        spiceLevel: itemData.spiceLevel || 'mild',
        isSignature: itemData.isSignature || false,
        isNew: itemData.isNew || false,
        isSeasonal: itemData.isSeasonal || false,
        availability: itemData.availability || {
          daysAvailable: ['all'],
          mealPeriods: ['dinner']
        },
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        projectId: this.getCurrentProjectId()
      };

      // Add to menu
      this.menuItems.push(menuItem);

      // Create recipe stub if requested
      if (createRecipe && window.menuRecipeIntegration) {
        const recipe = await window.menuRecipeIntegration.createRecipeStubForMenuItem(menuItem);
        menuItem.recipeId = recipe.id;
        
        this.showToast(`✅ Menu item added! Recipe draft created.`, 'success');
      } else {
        this.showToast(`✅ Menu item "${menuItem.name}" added!`, 'success');
      }

      // Save menu
      await this.saveMenu();

      // Refresh display
      this.renderMenuItems();

      // Analytics
      if (window.analyticsTracker) {
        window.analyticsTracker.trackCustomEvent('menu_item_added', {
          item_name: menuItem.name,
          category: menuItem.category,
          has_recipe: createRecipe
        });
      }

      return menuItem;

    } catch (error) {
      console.error('Error adding menu item:', error);
      this.showToast('❌ Error adding menu item', 'error');
      throw error;
    }
  }

  /**
   * Update menu item
   */
  async updateMenuItem(itemId, updates) {
    const index = this.menuItems.findIndex(item => item.id === itemId);
    
    if (index === -1) {
      console.error('Menu item not found:', itemId);
      return;
    }

    // Update item
    this.menuItems[index] = {
      ...this.menuItems[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };

    // Update linked recipe
    if (window.menuRecipeIntegration) {
      await window.menuRecipeIntegration.updateRecipeFromMenuItem(this.menuItems[index]);
    }

    await this.saveMenu();
    this.renderMenuItems();
    
    this.showToast('✅ Menu item updated', 'success');
  }

  /**
   * Delete menu item
   */
  async deleteMenuItem(itemId, deleteRecipe = false) {
    const item = this.menuItems.find(i => i.id === itemId);
    
    if (!item) {
      return;
    }

    // Confirm deletion
    const message = deleteRecipe 
      ? `Delete "${item.name}" and its recipe?`
      : `Delete "${item.name}"? (Recipe will be kept)`;
      
    if (!confirm(message)) {
      return;
    }

    // Remove from array
    this.menuItems = this.menuItems.filter(i => i.id !== itemId);

    // Handle recipe
    if (window.menuRecipeIntegration) {
      await window.menuRecipeIntegration.deleteRecipeForMenuItem(itemId, !deleteRecipe);
    }

    await this.saveMenu();
    this.renderMenuItems();
    
    this.showToast('✅ Menu item deleted', 'success');
  }

  /**
   * Render menu items
   */
  renderMenuItems() {
    const container = document.getElementById('menu-items-grid');
    
    if (!container) {
      console.warn('Menu items container not found');
      return;
    }

    if (this.menuItems.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">🍽️</div>
          <h3>No Menu Items Yet</h3>
          <p>Add your first menu item to get started</p>
          <button class="btn btn-primary" onclick="window.enhancedMenuManager.showAddItemModal()">
            ➕ Add Menu Item
          </button>
        </div>
      `;
      return;
    }

    // Group by category
    const itemsByCategory = {};
    for (const item of this.menuItems) {
      const category = item.category || 'Uncategorized';
      if (!itemsByCategory[category]) {
        itemsByCategory[category] = [];
      }
      itemsByCategory[category].push(item);
    }

    // Render categories
    let html = '';
    for (const [category, items] of Object.entries(itemsByCategory)) {
      html += `
        <div class="menu-category">
          <div class="menu-category-header">
            <h3>${category}</h3>
            <span class="menu-category-count">${items.length} items</span>
          </div>
          <div class="menu-category-items">
            ${items.map(item => this.renderMenuItem(item)).join('')}
          </div>
        </div>
      `;
    }

    container.innerHTML = html;

    // Update statistics
    this.updateStatistics();
  }

  /**
   * Render single menu item card
   */
  renderMenuItem(item) {
    const recipeStatus = window.menuRecipeIntegration 
      ? window.menuRecipeIntegration.getRecipeStatus(item.id)
      : null;

    const costData = window.menuRecipeIntegration 
      ? window.menuRecipeIntegration.calculateFoodCostPercent(item)
      : null;

    const badges = [];
    if (item.isSignature) badges.push('<span class="menu-badge badge-signature">⭐ Signature</span>');
    if (item.isNew) badges.push('<span class="menu-badge badge-new">🆕 New</span>');
    if (item.isSeasonal) badges.push('<span class="menu-badge badge-seasonal">🍂 Seasonal</span>');

    return `
      <div class="menu-item-card" data-item-id="${item.id}">
        <div class="menu-item-header">
          <div class="menu-item-title-section">
            <h4 class="menu-item-title">${item.name}</h4>
            <div class="menu-item-price">$${item.price.toFixed(2)}</div>
          </div>
          ${badges.length > 0 ? `<div class="menu-item-badges">${badges.join('')}</div>` : ''}
        </div>

        <div class="menu-item-description">
          ${item.description || '<em>No description</em>'}
        </div>

        ${recipeStatus ? `
          <div class="menu-item-recipe-status">
            <span class="recipe-status-badge" style="color: ${recipeStatus.color}">
              ${recipeStatus.icon} ${recipeStatus.label}
            </span>
            ${costData ? `
              <span class="recipe-cost-info ${costData.isOverTarget ? 'cost-warning' : costData.isGood ? 'cost-good' : ''}">
                ${costData.percent}% food cost
                ${costData.isOverTarget ? '⚠️' : costData.isGood ? '✅' : ''}
              </span>
            ` : ''}
          </div>
        ` : ''}

        <div class="menu-item-meta">
          ${item.allergens && item.allergens.length > 0 ? `
            <span class="menu-item-allergens">⚠️ ${item.allergens.join(', ')}</span>
          ` : ''}
          ${item.dietaryInfo && item.dietaryInfo.length > 0 ? `
            <span class="menu-item-dietary">🥗 ${item.dietaryInfo.join(', ')}</span>
          ` : ''}
        </div>

        <div class="menu-item-actions">
          ${recipeStatus && recipeStatus.recipeId ? `
            <button class="btn btn-primary btn-sm" onclick="window.menuRecipeIntegration.openRecipeInDeveloper('${recipeStatus.recipeId}')">
              📝 ${recipeStatus.action}
            </button>
          ` : `
            <button class="btn btn-primary btn-sm" onclick="window.enhancedMenuManager.createRecipeForItem('${item.id}')">
              ➕ Create Recipe
            </button>
          `}
          <button class="btn btn-secondary btn-sm" onclick="window.enhancedMenuManager.showEditItemModal('${item.id}')">
            ✏️ Edit
          </button>
          <button class="btn btn-secondary btn-sm" onclick="window.enhancedMenuManager.deleteMenuItem('${item.id}')">
            🗑️
          </button>
        </div>
      </div>
    `;
  }

  /**
   * Update menu statistics
   */
  updateStatistics() {
    if (!window.menuRecipeIntegration) {
      return;
    }

    const stats = window.menuRecipeIntegration.getMenuStatistics(this.menuItems);

    const statsContainer = document.getElementById('menu-statistics');
    if (statsContainer) {
      const completionRate = stats.totalItems > 0 
        ? Math.round((stats.withRecipes / stats.totalItems) * 100) 
        : 0;

      statsContainer.innerHTML = `
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">${stats.totalItems}</div>
            <div class="stat-label">Total Items</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">${stats.withRecipes}/${stats.totalItems}</div>
            <div class="stat-label">With Recipes</div>
            <div class="stat-progress">
              <div class="stat-progress-bar" style="width: ${completionRate}%"></div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-value">${stats.averageFoodCost}%</div>
            <div class="stat-label">Avg Food Cost</div>
          </div>
          <div class="stat-card ${stats.overTargetCount > 0 ? 'stat-warning' : ''}">
            <div class="stat-value">${stats.overTargetCount}</div>
            <div class="stat-label">Over Target</div>
          </div>
        </div>
      `;
    }
  }

  /**
   * Show add item modal
   */
  showAddItemModal() {
    const modal = document.getElementById('add-menu-item-modal');
    if (modal) {
      // Reset form
      const form = document.getElementById('add-menu-item-form');
      if (form) {
        form.reset();
      }
      modal.style.display = 'flex';
    }
  }

  /**
   * Show edit item modal
   */
  showEditItemModal(itemId) {
    const item = this.menuItems.find(i => i.id === itemId);
    if (!item) {
      return;
    }

    // Store item ID for update
    window._editingItemId = itemId;

    // Populate form
    document.getElementById('edit-item-name').value = item.name;
    document.getElementById('edit-item-description').value = item.description || '';
    document.getElementById('edit-item-category').value = item.category;
    document.getElementById('edit-item-price').value = item.price;

    // Show modal
    const modal = document.getElementById('edit-menu-item-modal');
    if (modal) {
      modal.style.display = 'flex';
    }
  }

  /**
   * Create recipe for existing menu item
   */
  async createRecipeForItem(itemId) {
    const item = this.menuItems.find(i => i.id === itemId);
    if (!item) {
      return;
    }

    if (!window.menuRecipeIntegration) {
      this.showToast('❌ Recipe integration not available', 'error');
      return;
    }

    try {
      const recipe = await window.menuRecipeIntegration.createRecipeStubForMenuItem(item);
      item.recipeId = recipe.id;
      await this.saveMenu();
      this.renderMenuItems();
      
      // Ask if they want to develop it now
      if (confirm('Recipe created! Would you like to develop it now?')) {
        window.menuRecipeIntegration.openRecipeInDeveloper(recipe.id);
      }
    } catch (error) {
      console.error('Error creating recipe:', error);
      this.showToast('❌ Error creating recipe', 'error');
    }
  }

  /**
   * Apply imported items
   */
  async applyImportedItems(items) {
    for (const item of items) {
      await this.addMenuItem(item, true);
    }
    
    this.showToast(`✅ Imported ${items.length} menu items with recipes!`, 'success');
  }

  /**
   * Export menu as JSON
   */
  exportMenu() {
    const data = {
      menu: this.currentMenu,
      items: this.menuItems,
      exportedAt: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `menu-${this.currentMenu.name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    this.showToast('✅ Menu exported!', 'success');
  }

  /**
   * Download template
   */
  downloadTemplate() {
    const template = `Menu Template

# Category: Appetizers

Item Name, Description, Price
Bruschetta, Fresh tomatoes on toasted bread, 8.99
Calamari, Crispy fried squid with marinara, 12.99

# Category: Main Courses

Item Name, Description, Price
Grilled Salmon, Atlantic salmon with lemon butter, 24.99
Ribeye Steak, 12oz ribeye with garlic butter, 32.99

# Category: Desserts

Item Name, Description, Price
Tiramisu, Classic Italian dessert, 7.99
Chocolate Cake, Rich chocolate cake with ganache, 6.99
`;

    const blob = new Blob([template], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'menu-template.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    this.showToast('✅ Template downloaded!', 'success');
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Add item form
    const addForm = document.getElementById('add-menu-item-form');
    if (addForm) {
      addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addForm);
        const itemData = {
          name: formData.get('name'),
          description: formData.get('description'),
          category: formData.get('category'),
          price: parseFloat(formData.get('price')),
          allergens: formData.get('allergens')?.split(',').map(a => a.trim()).filter(Boolean) || [],
          dietaryInfo: formData.get('dietaryInfo')?.split(',').map(d => d.trim()).filter(Boolean) || []
        };

        const createRecipe = formData.get('createRecipe') !== null;

        await this.addMenuItem(itemData, createRecipe);
        
        // Close modal
        const modal = document.getElementById('add-menu-item-modal');
        if (modal) {
          modal.style.display = 'none';
        }
      });
    }

    // Edit item form
    const editForm = document.getElementById('edit-menu-item-form');
    if (editForm) {
      editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(editForm);
        const updates = {
          name: formData.get('name'),
          description: formData.get('description'),
          category: formData.get('category'),
          price: parseFloat(formData.get('price'))
        };

        await this.updateMenuItem(window._editingItemId, updates);
        
        // Close modal
        const modal = document.getElementById('edit-menu-item-modal');
        if (modal) {
          modal.style.display = 'none';
        }
      });
    }
  }

  /**
   * Utility functions
   */
  getCurrentProjectId() {
    if (window.projectManager?.getCurrentProject) {
      const project = window.projectManager.getCurrentProject();
      return project?.id || 'default';
    }
    return 'default';
  }

  showToast(message, type = 'info') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
      color: white;
      padding: 16px 24px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      font-weight: 500;
      animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
}

// Initialize global instance
window.enhancedMenuManager = new EnhancedMenuManager();

console.log('🍽️ Enhanced Menu Manager loaded');

