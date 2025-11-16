/**
 * Enhanced Menu Import Handler
 * Adds recipe linking and FOH notes creation to imported menu items
 */

class EnhancedMenuImport {
    constructor() {
        this.importedItems = [];
        this.menuInfo = null;
    }

    /**
     * Show import results with recipe linking options
     */
    showImportResults(items, menuInfo = null) {
        this.importedItems = items;
        this.menuInfo = menuInfo;
        
        const modal = document.getElementById('import-results-modal');
        if (!modal) return;

        // Show menu info if available
        this.displayMenuInfo(menuInfo);
        
        // Show summary
        this.displaySummary(items);
        
        // Show items with recipe linking
        this.displayItems(items);
        
        // Show modal
        modal.style.display = 'block';
    }

    /**
     * Display menu information
     */
    displayMenuInfo(menuInfo) {
        const container = document.getElementById('import-menu-info');
        const display = document.getElementById('menu-info-display');
        
        if (!menuInfo || !display || !container) return;

        display.innerHTML = `
            <div class="form-group">
                <strong>Menu:</strong> ${menuInfo.name || 'Untitled'}
            </div>
            ${menuInfo.description ? `
                <div class="form-group">
                    <strong>Description:</strong> ${menuInfo.description}
                </div>
            ` : ''}
            ${menuInfo.type ? `
                <div class="form-group">
                    <strong>Type:</strong> ${menuInfo.type}
                </div>
            ` : ''}
        `;
        
        container.style.display = 'block';
    }

    /**
     * Display import summary
     */
    displaySummary(items) {
        const container = document.getElementById('import-summary');
        if (!container) return;

        const categories = [...new Set(items.map(i => i.category))];
        const totalItems = items.length;
        const avgPrice = items.reduce((sum, i) => sum + (Number(i.price) || 0), 0) / totalItems || 0;

        container.innerHTML = `
            <div class="file-preview-body">
                <div class="preview-stat">
                    <div class="preview-stat-label">Total Items</div>
                    <div class="preview-stat-value">${totalItems}</div>
                </div>
                <div class="preview-stat">
                    <div class="preview-stat-label">Categories</div>
                    <div class="preview-stat-value">${categories.length}</div>
                </div>
                <div class="preview-stat">
                    <div class="preview-stat-label">Avg Price</div>
                    <div class="preview-stat-value">$${avgPrice.toFixed(2)}</div>
                </div>
            </div>
        `;
    }

    /**
     * Display items with recipe linking options
     */
    displayItems(items) {
        const container = document.getElementById('import-items-list');
        if (!container) return;

        container.innerHTML = items.map((item, index) => `
            <div class="parse-item" data-item-index="${index}">
                <div class="parse-item-header">
                    <div>
                        <div class="parse-item-name">${this.escapeHtml(item.name)}</div>
                        ${item.price ? `
                            <div class="parse-item-price">$${Number(item.price).toFixed(2)}</div>
                        ` : ''}
                    </div>
                    <div class="parse-item-category">${this.escapeHtml(item.category)}</div>
                </div>
                ${item.description ? `
                    <div class="parse-item-description">${this.escapeHtml(item.description)}</div>
                ` : ''}
                
                <!-- FOH Notes Badge -->
                <div class="parse-item-foh-notes">
                    FOH Note Created
                </div>
                
                <!-- Recipe Link Section -->
                <div class="parse-item-recipe-section">
                    <div class="parse-item-recipe-label">Recipe</div>
                    <div class="parse-item-recipe-actions">
                        <button class="btn-link-recipe" onclick="enhancedMenuImport.linkRecipe(${index})">
                            🔗 Link Existing
                        </button>
                        <button class="btn-create-recipe" onclick="enhancedMenuImport.createRecipe(${index})">
                            ➕ Create New
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Link to existing recipe
     */
    linkRecipe(index) {
        const item = this.importedItems[index];
        if (!item) return;

        // TODO: Show recipe selector modal
        console.log('Linking recipe for:', item.name);
        
        // For now, just mark as linked
        const itemElement = document.querySelector(`[data-item-index="${index}"]`);
        if (itemElement) {
            const actionsDiv = itemElement.querySelector('.parse-item-recipe-actions');
            if (actionsDiv) {
                actionsDiv.innerHTML = '<div class="recipe-linked-badge">✓ Recipe Linked</div>';
            }
        }
        
        // Store the link intent
        item.recipeLink = 'existing';
    }

    /**
     * Create new recipe for this item
     */
    createRecipe(index) {
        const item = this.importedItems[index];
        if (!item) return;

        // TODO: Create recipe with item details
        console.log('Creating recipe for:', item.name);
        
        // Mark as creating
        const itemElement = document.querySelector(`[data-item-index="${index}"]`);
        if (itemElement) {
            const actionsDiv = itemElement.querySelector('.parse-item-recipe-actions');
            if (actionsDiv) {
                actionsDiv.innerHTML = '<div class="recipe-linked-badge">✓ Creating Recipe...</div>';
            }
        }
        
        // Store the creation intent
        item.recipeLink = 'new';
        item.needsRecipe = true;
    }

    /**
     * Apply import results to menu
     */
    async applyResults() {
        if (!this.importedItems || this.importedItems.length === 0) {
            alert('No items to apply.');
            return;
        }

        console.log('📥 Applying imported items:', this.importedItems);

        // Add menu info if available
        if (this.menuInfo) {
            const nameEl = document.getElementById('menu-name');
            const descEl = document.getElementById('menu-description');
            const typeEl = document.getElementById('menu-type');
            
            if (nameEl && this.menuInfo.name) nameEl.value = this.menuInfo.name;
            if (descEl && this.menuInfo.description) descEl.value = this.menuInfo.description;
            if (typeEl && this.menuInfo.type) typeEl.value = this.menuInfo.type;
        }

        if (window.enhancedMenuManager) {
            try {
                let targetMenuId = window.enhancedMenuManager.currentMenu?.id;

                if (!targetMenuId) {
                    const newMenu = await window.enhancedMenuManager.createMenuFromImport({
                        name: this.menuInfo?.name || 'Imported Menu',
                        description: this.menuInfo?.description || 'Imported via Menu Builder',
                        type: this.menuInfo?.type || 'Imported',
                        items: this.importedItems
                    });
                    targetMenuId = newMenu?.id;
                } else {
                    for (const item of this.importedItems) {
                        await window.enhancedMenuManager.addMenuItem({
                            name: item.name,
                            description: item.description || '',
                            category: item.category || 'Main Courses',
                            price: item.price || 0,
                            allergens: item.allergens || [],
                            dietaryInfo: item.dietaryInfo || []
                        }, true, targetMenuId);
                    }
                }

                await this.createFOHNotes(targetMenuId);
                await this.createRecipes(targetMenuId);

                this.closeModal();

                if (window.enhancedMenuManager.showToast) {
                    window.enhancedMenuManager.showToast(
                        `✅ Imported ${this.importedItems.length} items${targetMenuId ? '' : ' into a new menu'}!`,
                        'success'
                    );
                } else {
                    alert(`✅ Imported ${this.importedItems.length} items!`);
                }

                window.enhancedMenuManager.renderMenuItems();

            } catch (error) {
                console.error('❌ Error importing items:', error);
                alert('Error importing items. Check console for details.');
                return;
            }
        } else {
            console.error('❌ Enhanced menu manager not available');
            alert('Menu manager not ready. Please refresh the page and try again.');
            return;
        }
    }

    /**
     * Create FOH notes for all imported items
     */
    async createFOHNotes(menuId = null) {
        // Get existing notes or create new list
        const notesKey = `iterum_foh_notes_${this.getCurrentUserId()}_${this.getCurrentProjectId()}`;
        let notes = [];
        
        try {
            const stored = localStorage.getItem(notesKey);
            if (stored) {
                notes = JSON.parse(stored);
            }
        } catch (e) {
            console.error('Error loading FOH notes:', e);
        }

        // Create notes for each menu item
        for (const item of this.importedItems) {
            const note = {
                id: Date.now() + Math.random(),
                menuItem: item.name,
                category: item.category,
                price: item.price,
                description: item.description || '',
                allergens: item.allergens || [],
                dietaryInfo: item.dietaryInfo || [],
                ingredients: [],
                prepTime: '',
                cookingTime: '',
                notes: '',
                warnings: '',
                menuId: menuId || null,
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };
            
            notes.push(note);
        }

        // Save notes
        try {
            localStorage.setItem(notesKey, JSON.stringify(notes));
            console.log(`Created ${this.importedItems.length} FOH notes`);
        } catch (e) {
            console.error('Error saving FOH notes:', e);
        }
    }

    /**
     * Create recipes for items that need them
     */
    async createRecipes(menuId = null) {
        const itemsNeedingRecipes = this.importedItems.filter(i => i.needsRecipe);
        
        if (itemsNeedingRecipes.length === 0) return;

        // Load existing recipes
        const recipesKey = `iterum_recipes_${this.getCurrentUserId()}_${this.getCurrentProjectId()}`;
        let recipes = [];
        
        try {
            const stored = localStorage.getItem(recipesKey);
            if (stored) {
                recipes = JSON.parse(stored);
            }
        } catch (e) {
            console.error('Error loading recipes:', e);
        }

        // Create recipes
        for (const item of itemsNeedingRecipes) {
            const recipe = {
                id: Date.now() + Math.random(),
                name: item.name,
                description: item.description || '',
                category: 'Menu Recipe',
                servings: 1,
                prepTime: '',
                cookTime: '',
                ingredients: [],
                instructions: [],
                allergens: item.allergens || [],
                dietaryInfo: item.dietaryInfo || [],
                menuLinked: true,
                menuItemName: item.name,
                menuId: menuId || null,
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };
            
            recipes.push(recipe);
        }

        // Save recipes
        try {
            localStorage.setItem(recipesKey, JSON.stringify(recipes));
            console.log(`Created ${itemsNeedingRecipes.length} recipes`);
        } catch (e) {
            console.error('Error saving recipes:', e);
        }
    }

    /**
     * Close modal
     */
    closeModal() {
        const modal = document.getElementById('import-results-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    /**
     * Show success message
     */
    showSuccess() {
        // TODO: Use toast notification system
        alert(`✓ Successfully imported ${this.importedItems.length} menu items!`);
    }

    /**
     * Get current user ID
     */
    getCurrentUserId() {
        try {
            const user = (window.userSystem && window.userSystem.getCurrentUser && window.userSystem.getCurrentUser()) || null;
            return user?.id || user?.userId || 'guest';
        } catch {
            return 'guest';
        }
    }

    /**
     * Get current project ID
     */
    getCurrentProjectId() {
        try {
            const stored = localStorage.getItem('iterum_current_project');
            if (stored) {
                const p = JSON.parse(stored);
                return p?.id || p?.projectId || 'master';
            }
            return 'master';
        } catch {
            return 'master';
        }
    }

    /**
     * Escape HTML
     */
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Create global instance
const enhancedMenuImport = new EnhancedMenuImport();
window.enhancedMenuImport = enhancedMenuImport;

