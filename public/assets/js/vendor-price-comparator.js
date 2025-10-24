/**
 * Vendor Price Comparator
 * Compare prices across vendors for smart purchasing decisions
 */

class VendorPriceComparator {
  constructor() {
    this.connectionsKey = 'vendor_ingredient_connections';
    this.priceHistoryKey = 'vendor_price_history';
    this.init();
  }

  init() {
    console.log('💰 Vendor Price Comparator initialized');
  }

  /**
   * Get all vendor connections for an ingredient
   */
  getVendorPricesForIngredient(ingredientId) {
    const connections = JSON.parse(localStorage.getItem(this.connectionsKey) || '[]');
    return connections.filter(conn => conn.ingredientId === ingredientId);
  }

  /**
   * Find best price for an ingredient
   */
  getBestPriceForIngredient(ingredientId) {
    const prices = this.getVendorPricesForIngredient(ingredientId);
    
    if (prices.length === 0) return null;

    // Normalize to price per lb for comparison
    const normalized = prices.map(p => ({
      ...p,
      pricePerLb: this.normalizePriceToLb(p.price, p.unit)
    }));

    // Sort by price per lb
    normalized.sort((a, b) => a.pricePerLb - b.pricePerLb);

    return normalized[0];
  }

  /**
   * Compare all vendors for an ingredient
   */
  compareVendorsForIngredient(ingredientId) {
    const prices = this.getVendorPricesForIngredient(ingredientId);
    
    if (prices.length === 0) return null;

    // Normalize prices
    const normalized = prices.map(p => ({
      ...p,
      pricePerLb: this.normalizePriceToLb(p.price, p.unit),
      displayPrice: `$${p.price.toFixed(2)}/${p.unit}`
    }));

    // Sort by price
    normalized.sort((a, b) => a.pricePerLb - b.pricePerLb);

    const bestPrice = normalized[0];
    const worstPrice = normalized[normalized.length - 1];
    const savings = worstPrice.pricePerLb - bestPrice.pricePerLb;
    const savingsPercent = ((savings / worstPrice.pricePerLb) * 100).toFixed(1);

    return {
      ingredientId: ingredientId,
      vendors: normalized,
      bestVendor: bestPrice,
      worstVendor: worstPrice,
      totalVendors: normalized.length,
      maxSavings: savings,
      savingsPercent: savingsPercent
    };
  }

  /**
   * Compare prices for multiple ingredients (shopping list)
   */
  compareShoppingList(ingredientList) {
    const results = [];
    let totalSavings = 0;

    for (const item of ingredientList) {
      const comparison = this.compareVendorsForIngredient(item.ingredientId);
      
      if (comparison) {
        const quantityInLbs = this.convertToLbs(item.quantity, item.unit);
        const bestCost = comparison.bestVendor.pricePerLb * quantityInLbs;
        const worstCost = comparison.worstVendor.pricePerLb * quantityInLbs;
        const savings = worstCost - bestCost;
        
        totalSavings += savings;

        results.push({
          ...item,
          comparison: comparison,
          quantityInLbs: quantityInLbs,
          bestCost: bestCost,
          worstCost: worstCost,
          savings: savings
        });
      }
    }

    return {
      items: results,
      totalSavings: totalSavings,
      itemCount: results.length
    };
  }

  /**
   * Get optimal vendor mix for a shopping list
   */
  getOptimalVendorMix(ingredientList) {
    const vendorOrders = {};
    let totalCost = 0;

    for (const item of ingredientList) {
      const best = this.getBestPriceForIngredient(item.ingredientId);
      
      if (best) {
        const vendorId = best.vendorId;
        const quantityInLbs = this.convertToLbs(item.quantity, item.unit);
        const cost = best.pricePerLb * quantityInLbs;

        if (!vendorOrders[vendorId]) {
          vendorOrders[vendorId] = {
            vendorId: vendorId,
            vendorName: best.vendorName,
            items: [],
            totalCost: 0
          };
        }

        vendorOrders[vendorId].items.push({
          ingredientName: item.ingredientName,
          quantity: item.quantity,
          unit: item.unit,
          price: best.price,
          priceUnit: best.unit,
          brandName: best.brandName,
          cost: cost
        });

        vendorOrders[vendorId].totalCost += cost;
        totalCost += cost;
      }
    }

    return {
      vendors: Object.values(vendorOrders),
      totalCost: totalCost,
      vendorCount: Object.keys(vendorOrders).length
    };
  }

  /**
   * Track price changes over time
   */
  recordPriceChange(ingredientId, vendorId, oldPrice, newPrice, unit) {
    const history = JSON.parse(localStorage.getItem(this.priceHistoryKey) || '[]');
    
    history.push({
      id: `price_${Date.now()}`,
      ingredientId: ingredientId,
      vendorId: vendorId,
      oldPrice: oldPrice,
      newPrice: newPrice,
      unit: unit,
      change: newPrice - oldPrice,
      changePercent: ((newPrice - oldPrice) / oldPrice * 100).toFixed(2),
      timestamp: new Date().toISOString()
    });

    // Keep last 1000 price changes
    if (history.length > 1000) {
      history.shift();
    }

    localStorage.setItem(this.priceHistoryKey, JSON.stringify(history));
  }

  /**
   * Get price history for an ingredient
   */
  getPriceHistory(ingredientId, vendorId = null) {
    const history = JSON.parse(localStorage.getItem(this.priceHistoryKey) || '[]');
    
    let filtered = history.filter(h => h.ingredientId === ingredientId);
    
    if (vendorId) {
      filtered = filtered.filter(h => h.vendorId === vendorId);
    }

    return filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  }

  /**
   * Get price trends
   */
  getPriceTrends(ingredientId) {
    const history = this.getPriceHistory(ingredientId);
    
    if (history.length === 0) return null;

    const increases = history.filter(h => h.change > 0).length;
    const decreases = history.filter(h => h.change < 0).length;
    const avgChange = history.reduce((sum, h) => sum + h.change, 0) / history.length;

    return {
      totalChanges: history.length,
      increases: increases,
      decreases: decreases,
      avgChange: avgChange,
      trend: avgChange > 0 ? 'increasing' : avgChange < 0 ? 'decreasing' : 'stable',
      lastChange: history[0]
    };
  }

  /**
   * Normalize price to per lb for comparison
   */
  normalizePriceToLb(price, unit) {
    const conversions = {
      'lb': 1,
      'oz': 16,
      'kg': 0.453592,
      'g': 453.592,
      'each': 1, // Assume 1 each = 1 lb
      'dozen': 12,
      'case': 1, // Need more context
      'box': 1,
      'cup': 2, // Rough estimate
      'tbsp': 32,
      'tsp': 96
    };

    const factor = conversions[unit.toLowerCase()] || 1;
    return price * factor;
  }

  /**
   * Convert quantity to lbs for calculation
   */
  convertToLbs(quantity, unit) {
    const conversions = {
      'lb': 1,
      'oz': 1/16,
      'kg': 2.20462,
      'g': 0.00220462,
      'each': 1,
      'dozen': 1,
      'case': 1,
      'box': 1,
      'cup': 0.5,
      'tbsp': 1/32,
      'tsp': 1/96
    };

    const factor = conversions[unit.toLowerCase()] || 1;
    return quantity * factor;
  }

  /**
   * Generate price comparison report
   */
  generateComparisonReport(ingredientIds) {
    const comparisons = ingredientIds.map(id => this.compareVendorsForIngredient(id)).filter(Boolean);
    
    const totalVendors = new Set(comparisons.flatMap(c => c.vendors.map(v => v.vendorId))).size;
    const avgSavings = comparisons.reduce((sum, c) => sum + parseFloat(c.savingsPercent), 0) / comparisons.length;

    return {
      comparisons: comparisons,
      totalIngredients: comparisons.length,
      totalVendors: totalVendors,
      avgSavingsPercent: avgSavings.toFixed(1),
      recommendations: this.generateRecommendations(comparisons)
    };
  }

  /**
   * Generate recommendations
   */
  generateRecommendations(comparisons) {
    const recommendations = [];

    for (const comp of comparisons) {
      if (comp.totalVendors > 1 && parseFloat(comp.savingsPercent) > 10) {
        recommendations.push({
          type: 'savings',
          ingredient: comp.vendors[0].ingredientName,
          message: `Switch to ${comp.bestVendor.vendorName} to save ${comp.savingsPercent}%`,
          savings: comp.maxSavings
        });
      }

      if (comp.totalVendors === 1) {
        recommendations.push({
          type: 'single_vendor',
          ingredient: comp.vendors[0].ingredientName,
          message: `Only one vendor available - consider adding more options`
        });
      }
    }

    return recommendations;
  }

  /**
   * Export comparison to CSV
   */
  exportComparisonToCSV(comparison) {
    const headers = ['Ingredient', 'Vendor', 'Brand', 'Price', 'Unit', 'Price/lb'];
    const rows = comparison.vendors.map(v => [
      v.ingredientName,
      v.vendorName,
      v.brandName || '-',
      v.price.toFixed(2),
      v.unit,
      v.pricePerLb.toFixed(2)
    ]);

    const csv = [headers, ...rows].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `price-comparison-${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

// Initialize global instance
window.vendorPriceComparator = new VendorPriceComparator();

console.log('💰 Vendor Price Comparator loaded');

