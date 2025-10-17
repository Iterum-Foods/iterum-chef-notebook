/**
 * Inventory Management System
 * Track stock levels, usage, reorder points, and waste
 */

class InventoryManager {
  constructor() {
    this.inventoryKey = 'inventory_items';
    this.transactionsKey = 'inventory_transactions';
    this.parLevelsKey = 'inventory_par_levels';
    this.init();
  }

  init() {
    console.log('📦 Inventory Manager initialized');
    this.checkLowStock();
  }

  /**
   * Get all inventory items
   */
  getInventory() {
    return JSON.parse(localStorage.getItem(this.inventoryKey) || '[]');
  }

  /**
   * Save inventory
   */
  saveInventory(inventory) {
    localStorage.setItem(this.inventoryKey, JSON.stringify(inventory));
  }

  /**
   * Add or update inventory item
   */
  upsertInventoryItem(ingredientId, ingredientName, quantity, unit, location = 'Main Kitchen') {
    const inventory = this.getInventory();
    const existing = inventory.find(item => item.ingredientId === ingredientId && item.location === location);

    if (existing) {
      existing.quantity = quantity;
      existing.unit = unit;
      existing.lastUpdated = new Date().toISOString();
    } else {
      inventory.push({
        id: `inv_${Date.now()}`,
        ingredientId: ingredientId,
        ingredientName: ingredientName,
        quantity: quantity,
        unit: unit,
        location: location,
        parLevel: 0,
        reorderPoint: 0,
        cost: 0,
        lastUpdated: new Date().toISOString(),
        createdAt: new Date().toISOString()
      });
    }

    this.saveInventory(inventory);
    return existing || inventory[inventory.length - 1];
  }

  /**
   * Adjust stock (add or remove)
   */
  adjustStock(ingredientId, quantity, unit, reason = 'Manual Adjustment', location = 'Main Kitchen') {
    const inventory = this.getInventory();
    const item = inventory.find(i => i.ingredientId === ingredientId && i.location === location);

    if (!item) {
      throw new Error('Inventory item not found');
    }

    const oldQuantity = item.quantity;
    item.quantity += quantity;
    item.lastUpdated = new Date().toISOString();

    this.saveInventory(inventory);

    // Record transaction
    this.recordTransaction({
      ingredientId: ingredientId,
      ingredientName: item.ingredientName,
      quantityChange: quantity,
      unit: unit,
      oldQuantity: oldQuantity,
      newQuantity: item.quantity,
      reason: reason,
      location: location,
      timestamp: new Date().toISOString()
    });

    // Check if now low stock
    if (item.quantity <= item.reorderPoint && item.reorderPoint > 0) {
      this.triggerReorderAlert(item);
    }

    return item;
  }

  /**
   * Deduct ingredients for a recipe
   */
  deductForRecipe(recipeId, recipeName, ingredients, servings = 1) {
    const transactions = [];
    
    for (const ing of ingredients) {
      try {
        const item = this.adjustStock(
          ing.ingredientId || ing.id,
          -ing.quantity * servings,
          ing.unit,
          `Recipe: ${recipeName}`,
          ing.location || 'Main Kitchen'
        );
        transactions.push(item);
      } catch (error) {
        console.warn(`Could not deduct ${ing.name}:`, error.message);
      }
    }

    return transactions;
  }

  /**
   * Record transaction
   */
  recordTransaction(transaction) {
    const transactions = JSON.parse(localStorage.getItem(this.transactionsKey) || '[]');
    transaction.id = `txn_${Date.now()}`;
    transactions.push(transaction);
    
    // Keep last 1000 transactions
    if (transactions.length > 1000) {
      transactions.shift();
    }
    
    localStorage.setItem(this.transactionsKey, JSON.stringify(transactions));
  }

  /**
   * Get transactions
   */
  getTransactions(ingredientId = null, limit = 100) {
    const transactions = JSON.parse(localStorage.getItem(this.transactionsKey) || '[]');
    
    let filtered = transactions;
    if (ingredientId) {
      filtered = transactions.filter(t => t.ingredientId === ingredientId);
    }
    
    return filtered.slice(-limit).reverse();
  }

  /**
   * Set par levels and reorder points
   */
  setParLevel(ingredientId, parLevel, reorderPoint, location = 'Main Kitchen') {
    const inventory = this.getInventory();
    const item = inventory.find(i => i.ingredientId === ingredientId && i.location === location);

    if (item) {
      item.parLevel = parLevel;
      item.reorderPoint = reorderPoint;
      this.saveInventory(inventory);
    }
  }

  /**
   * Check for low stock items
   */
  getLowStockItems() {
    const inventory = this.getInventory();
    return inventory.filter(item => 
      item.reorderPoint > 0 && item.quantity <= item.reorderPoint
    );
  }

  /**
   * Check low stock and send alerts
   */
  checkLowStock() {
    const lowStock = this.getLowStockItems();
    
    if (lowStock.length > 0) {
      console.log(`⚠️ ${lowStock.length} items low in stock`);
      
      // Store in localStorage for display
      localStorage.setItem('low_stock_count', lowStock.length);
      
      // Dispatch event
      window.dispatchEvent(new CustomEvent('lowStockAlert', { 
        detail: { items: lowStock } 
      }));
    }
  }

  /**
   * Trigger reorder alert
   */
  triggerReorderAlert(item) {
    console.log(`🔔 Reorder alert: ${item.ingredientName}`);
    
    // Create notification
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('Low Stock Alert', {
        body: `${item.ingredientName} is low (${item.quantity} ${item.unit})`,
        icon: '/assets/icons/iterum.ico'
      });
    }
  }

  /**
   * Generate shopping list from low stock
   */
  generateShoppingList() {
    const lowStock = this.getLowStockItems();
    
    return lowStock.map(item => ({
      ingredientId: item.ingredientId,
      ingredientName: item.ingredientName,
      currentQuantity: item.quantity,
      parLevel: item.parLevel,
      orderQuantity: Math.max(item.parLevel - item.quantity, 0),
      unit: item.unit,
      location: item.location,
      priority: item.quantity <= 0 ? 'urgent' : 'normal'
    }));
  }

  /**
   * Calculate total inventory value
   */
  calculateInventoryValue() {
    const inventory = this.getInventory();
    return inventory.reduce((total, item) => total + (item.cost * item.quantity), 0);
  }

  /**
   * Get inventory statistics
   */
  getStats() {
    const inventory = this.getInventory();
    const lowStock = this.getLowStockItems();
    const outOfStock = inventory.filter(item => item.quantity <= 0);
    
    return {
      totalItems: inventory.length,
      lowStockCount: lowStock.length,
      outOfStockCount: outOfStock.length,
      totalValue: this.calculateInventoryValue(),
      locations: [...new Set(inventory.map(i => i.location))],
      lastUpdated: inventory.length > 0 ? 
        Math.max(...inventory.map(i => new Date(i.lastUpdated).getTime())) : null
    };
  }

  /**
   * Export inventory to CSV
   */
  exportToCSV() {
    const inventory = this.getInventory();
    
    const headers = ['Ingredient', 'Quantity', 'Unit', 'Location', 'Par Level', 'Reorder Point', 'Value', 'Last Updated'];
    const rows = inventory.map(item => [
      item.ingredientName,
      item.quantity,
      item.unit,
      item.location,
      item.parLevel,
      item.reorderPoint,
      (item.cost * item.quantity).toFixed(2),
      new Date(item.lastUpdated).toLocaleDateString()
    ]);

    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `inventory-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  /**
   * Import inventory from CSV
   */
  async importFromCSV(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        try {
          const text = e.target.result;
          const lines = text.split('\n').filter(line => line.trim());
          const headers = lines[0].split(',');
          
          let imported = 0;
          for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',');
            const ingredientName = values[0]?.trim();
            const quantity = parseFloat(values[1]) || 0;
            const unit = values[2]?.trim() || 'unit';
            const location = values[3]?.trim() || 'Main Kitchen';
            
            if (ingredientName) {
              this.upsertInventoryItem(
                `ing_import_${Date.now()}_${i}`,
                ingredientName,
                quantity,
                unit,
                location
              );
              imported++;
            }
          }
          
          resolve({ success: true, imported: imported });
        } catch (error) {
          reject(error);
        }
      };
      
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }

  /**
   * Perform physical inventory count
   */
  startPhysicalCount() {
    const countData = {
      id: `count_${Date.now()}`,
      startedAt: new Date().toISOString(),
      completedAt: null,
      items: this.getInventory().map(item => ({
        ...item,
        countedQuantity: null,
        variance: null,
        counted: false
      }))
    };
    
    localStorage.setItem('current_physical_count', JSON.stringify(countData));
    return countData;
  }

  /**
   * Complete physical count
   */
  completePhysicalCount(countData) {
    for (const item of countData.items) {
      if (item.counted && item.countedQuantity !== null) {
        const variance = item.countedQuantity - item.quantity;
        
        if (variance !== 0) {
          this.adjustStock(
            item.ingredientId,
            variance,
            item.unit,
            'Physical Count Adjustment',
            item.location
          );
        }
      }
    }
    
    countData.completedAt = new Date().toISOString();
    localStorage.removeItem('current_physical_count');
    
    // Save count history
    const history = JSON.parse(localStorage.getItem('physical_count_history') || '[]');
    history.push(countData);
    localStorage.setItem('physical_count_history', JSON.stringify(history));
    
    return countData;
  }
}

// Initialize global instance
window.inventoryManager = new InventoryManager();

console.log('📦 Inventory Manager loaded');

