givewqhst/**
 * Unified Navigation Header
 * Provides consistent navigation across all pages
 */

class UnifiedNavHeader {
    constructor() {
        this.currentPage = this.detectCurrentPage();
        this.init();
    }

    detectCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('chef-dashboard')) return 'chef';
        if (path.includes('index')) return 'dashboard';
        if (path.includes('recipe-library')) return 'recipes';
        if (path.includes('recipe-developer')) return 'developer';
        if (path.includes('menu-builder')) return 'menu';
        if (path.includes('kitchen-management')) return 'kitchen';
        if (path.includes('ingredients')) return 'ingredients';
        if (path.includes('vendor')) return 'vendors';
        if (path.includes('equipment')) return 'equipment';
        if (path.includes('user-profile')) return 'profile';
        if (path.includes('ingredient-highlights')) return 'highlights';
        if (path.includes('server-info')) return 'server';
        if (path.includes('audit-log')) return 'audit';
        return 'other';
    }

    init() {
        // Check if header already exists
        if (document.querySelector('.unified-nav-header')) {
            console.log('Navigation header already exists');
            return;
        }

        this.injectHeader();
    }

    injectHeader() {
        const header = document.createElement('nav');
        header.className = 'unified-nav-header';
        header.innerHTML = this.getHeaderHTML();

        // Insert at top of body
        document.body.insertBefore(header, document.body.firstChild);

        // Add styles
        this.injectStyles();

        console.log('✅ Navigation header injected');
    }

    getHeaderHTML() {
        return `
            <div class="nav-container">
                <!-- Logo -->
                <a href="index.html" class="nav-logo">
                    <span class="nav-logo-icon">🍳</span>
                    <span class="nav-logo-text">Iterum Culinary</span>
                </a>

                <!-- Main Navigation -->
                <div class="nav-links">
                    <a href="chef-dashboard.html" class="nav-link ${this.currentPage === 'chef' ? 'active' : ''}" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 8px 16px; border-radius: 8px; font-weight: 700; margin-right: 10px; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);">
                        <span>👨‍🍳</span> Chef
                    </a>
                    <a href="index.html" class="nav-link ${this.currentPage === 'dashboard' ? 'active' : ''}">
                        <span>🏠</span> Dashboard
                    </a>
                    <a href="recipe-library.html" class="nav-link ${this.currentPage === 'recipes' ? 'active' : ''}">
                        <span>📚</span> Recipes
                    </a>
                    <a href="menu-builder.html" class="nav-link ${this.currentPage === 'menu' ? 'active' : ''}">
                        <span>🍽️</span> Menus
                    </a>
                    <a href="kitchen-management.html" class="nav-link ${this.currentPage === 'kitchen' ? 'active' : ''}">
                        <span>🔪</span> Kitchen
                    </a>
                    <a href="ingredients.html" class="nav-link ${this.currentPage === 'ingredients' ? 'active' : ''}">
                        <span>🥬</span> Ingredients
                    </a>
                    
                    <!-- More Menu -->
                    <div class="nav-dropdown">
                        <button class="nav-link nav-dropdown-btn">
                            <span>☰</span> More Features
                        </button>
                        <div class="nav-dropdown-content" style="min-width: 280px; max-height: 500px; overflow-y: auto;">
                            <div style="padding: 10px 12px; font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">Kitchen Tools</div>
                            <a href="kitchen-management.html">🔪 Kitchen Management</a>
                            <a href="kitchen-management.html?tab=pdf">📕 Recipe Book PDF</a>
                            <a href="kitchen-management.html?tab=preplist">📝 Prep Lists</a>
                            <a href="ingredient-highlights.html">✨ Ingredient Stories</a>
                            <a href="server-info-sheet.html">🗣️ Server Info Sheets</a>
                            
                            <hr style="margin: 8px 0; border: none; border-top: 1px solid #e5e7eb;">
                            <div style="padding: 10px 12px; font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">Inventory</div>
                            <a href="inventory.html">📦 Inventory Tracking</a>
                            <a href="vendor-management.html">🏪 Vendor Management</a>
                            <a href="vendor-price-comparison.html">💰 Price Comparison</a>
                            <a href="equipment-management.html">🔧 Equipment</a>
                            <a href="production-planning.html">📋 Production Planning</a>
                            
                            <hr style="margin: 8px 0; border: none; border-top: 1px solid #e5e7eb;">
                            <div style="padding: 10px 12px; font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">Import Tools</div>
                            <a href="bulk-recipe-import.html">🚀 Bulk Recipe Import</a>
                            <a href="bulk-ingredient-import.html">📥 Bulk Ingredient Import</a>
                            <a href="recipe-photo-studio.html">📸 Photo Studio</a>
                            
                            <hr style="margin: 8px 0; border: none; border-top: 1px solid #e5e7eb;">
                            <div style="padding: 10px 12px; font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px;">System</div>
                            <a href="project-hub.html">📂 Project Hub</a>
                            <a href="data-backup-center.html">💾 Backup Center</a>
                            <a href="data-management-dashboard.html">💾 Data Management</a>
                            <a href="audit-log.html">📜 Audit Log</a>
                        </div>
                    </div>
                </div>

                <!-- Right Side -->
                <div class="nav-right">
                    <!-- Project Selector Placeholder -->
                    <div id="nav-project-selector-placeholder"></div>
                    
                    <!-- User Menu -->
                    <div class="nav-dropdown">
                        <button class="nav-link nav-user-btn">
                            <span id="nav-user-avatar">👤</span>
                            <span id="nav-user-name">User</span>
                        </button>
                        <div class="nav-dropdown-content nav-user-menu">
                            <a href="user-profile.html">👤 Profile & Settings</a>
                            <a href="project-hub.html">📂 Project Hub</a>
                            <hr style="margin: 5px 0; border: none; border-top: 1px solid #e5e7eb;">
                            <a href="#" onclick="event.preventDefault(); signOut();">🚪 Sign Out</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .unified-nav-header {
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                color: white;
                padding: 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                position: sticky;
                top: 0;
                z-index: 1000;
                border-bottom: 2px solid rgba(59, 130, 246, 0.3);
            }

            .nav-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                gap: 20px;
                height: 70px;
            }

            .nav-logo {
                display: flex;
                align-items: center;
                gap: 12px;
                text-decoration: none;
                color: white;
                font-weight: 800;
                font-size: 1.3rem;
                white-space: nowrap;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }

            .nav-logo-icon {
                font-size: 1.8rem;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
            }

            .nav-links {
                display: flex;
                align-items: center;
                gap: 5px;
                flex: 1;
            }

            .nav-link {
                color: white;
                text-decoration: none;
                padding: 10px 18px;
                border-radius: 8px;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                font-weight: 600;
                background: transparent;
                border: none;
                cursor: pointer;
                font-size: 1rem;
                white-space: nowrap;
                text-shadow: 0 1px 2px rgba(0,0,0,0.3);
            }

            .nav-link:hover {
                background: rgba(59, 130, 246, 0.3);
                transform: translateY(-1px);
            }

            .nav-link.active {
                background: rgba(59, 130, 246, 0.5);
                font-weight: 700;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
            }

            .nav-link span:first-child {
                font-size: 1.1rem;
            }

            .nav-right {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .nav-dropdown {
                position: relative;
            }

            .nav-dropdown-btn, .nav-user-btn {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .nav-dropdown-content {
                display: none;
                position: absolute;
                top: calc(100% + 10px);
                right: 0;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                min-width: 200px;
                padding: 8px;
                z-index: 1001;
            }

            .nav-dropdown:hover .nav-dropdown-content,
            .nav-dropdown-content:hover {
                display: block;
            }

            .nav-dropdown-content a {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 10px 12px;
                color: #1f2937;
                text-decoration: none;
                border-radius: 8px;
                transition: background 0.2s;
            }

            .nav-dropdown-content a:hover {
                background: #f3f4f6;
            }

            .nav-user-menu {
                min-width: 220px;
            }

            #nav-user-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background: rgba(255,255,255,0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
            }

            /* Mobile Responsive */
            @media (max-width: 768px) {
                .nav-links {
                    display: none;
                }
                
                .nav-container {
                    justify-content: space-between;
                }

                .nav-logo-text {
                    display: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    updateUserInfo(user) {
        const nameEl = document.getElementById('nav-user-name');
        const avatarEl = document.getElementById('nav-user-avatar');
        
        if (nameEl && user) {
            const displayName = user.displayName || user.name || user.email?.split('@')[0] || 'User';
            nameEl.textContent = displayName;
        }

        if (avatarEl && user) {
            if (user.photoURL || user.avatarUrl) {
                avatarEl.innerHTML = `<img src="${user.photoURL || user.avatarUrl}" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
            } else {
                const initial = (user.name || user.email || 'U')[0].toUpperCase();
                avatarEl.textContent = initial;
            }
        }
    }
}

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.unifiedNavHeader = new UnifiedNavHeader();
        
        // Update user info when available
        if (window.authManager?.currentUser) {
            window.unifiedNavHeader.updateUserInfo(window.authManager.currentUser);
        }
        
        window.addEventListener('userLoggedIn', (e) => {
            if (e.detail?.user) {
                window.unifiedNavHeader.updateUserInfo(e.detail.user);
            }
        });
    });
} else {
    window.unifiedNavHeader = new UnifiedNavHeader();
    
    if (window.authManager?.currentUser) {
        window.unifiedNavHeader.updateUserInfo(window.authManager.currentUser);
    }
}

// Global sign out function
window.signOut = function() {
    if (confirm('Are you sure you want to sign out?')) {
        if (window.authManager) {
            window.authManager.signOut();
        }
        localStorage.clear();
        window.location.href = 'index.html';
    }
};

console.log('✅ Unified Nav Header script loaded');

