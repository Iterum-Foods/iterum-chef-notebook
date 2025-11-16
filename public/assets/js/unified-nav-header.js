/**
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

        // Setup dropdown hover delay
        this.setupDropdownHover();

        console.log('✅ Navigation header injected');
    }

    setupDropdownHover() {
        // Add delay for dropdown hover to stay open when moving to it
        const dropdowns = document.querySelectorAll('.nav-dropdown');
        
        dropdowns.forEach(dropdown => {
            let hoverTimeout;
            
            dropdown.addEventListener('mouseenter', () => {
                clearTimeout(hoverTimeout);
                const content = dropdown.querySelector('.nav-dropdown-content');
                if (content) {
                    content.classList.add('show');
                }
            });
            
            dropdown.addEventListener('mouseleave', () => {
                hoverTimeout = setTimeout(() => {
                    const content = dropdown.querySelector('.nav-dropdown-content');
                    if (content) {
                        content.classList.remove('show');
                    }
                }, 300); // 300ms delay before closing
            });
        });
    }

    getHeaderHTML() {
        return `
            <div class="nav-container">
                <a href="index.html" class="nav-logo">
                    <span class="nav-logo-icon">🍳</span>
                    <span class="nav-logo-text">Iterum Culinary</span>
                </a>

                <div class="nav-links">
                    <a href="index.html" class="nav-link nav-link-emphasis ${this.currentPage === 'dashboard' ? 'active' : ''}">
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
                    <div class="nav-dropdown">
                        <button class="nav-link nav-dropdown-btn">
                            <span>☰</span> More
                        </button>
                        <div class="nav-dropdown-content">
                            <div class="nav-dropdown-category">Kitchen Tools</div>
                            <a href="kitchen-management.html">🔪 Kitchen Management</a>
                            <a href="kitchen-management.html?tab=pdf">📕 Recipe Book PDF</a>
                            <a href="kitchen-management.html?tab=preplist">📝 Prep Lists</a>
                            <a href="ingredient-highlights.html">✨ Ingredient Stories</a>
                            <a href="server-info-sheet.html">🗣️ Server Info</a>
                            <hr>
                            <div class="nav-dropdown-category">Inventory</div>
                            <a href="inventory.html">📦 Inventory</a>
                            <a href="vendor-management.html">🏪 Vendors</a>
                            <a href="vendor-price-comparison.html">💰 Price Compare</a>
                            <a href="equipment-management.html">🔧 Equipment</a>
                            <a href="production-planning.html">📋 Production</a>
                            <hr>
                            <div class="nav-dropdown-category">Import</div>
                            <a href="bulk-recipe-import.html">🚀 Recipe Import</a>
                            <a href="bulk-ingredient-import.html">📥 Ingredient Import</a>
                            <a href="recipe-photo-studio.html">📸 Photo Studio</a>
                            <hr>
                            <div class="nav-dropdown-category">System</div>
                            <a href="project-hub.html">📂 Project Hub</a>
                            <a href="data-backup-center.html">💾 Backup Center</a>
                            <a href="data-management-dashboard.html">🧠 Data Management</a>
                            <a href="audit-log.html">📜 Audit Log</a>
                        </div>
                    </div>
                </div>

                <div class="nav-meta">
                    <div class="nav-project-chip" id="nav-project-chip">Project: Master Project</div>
                    <div class="nav-dropdown">
                        <button class="nav-link nav-user-btn">
                            <span class="nav-avatar" id="nav-user-avatar">👤</span>
                            <span class="nav-label" id="nav-user-name">User</span>
                        </button>
                        <div class="nav-dropdown-content nav-user-menu">
                            <a href="user-profile.html">👤 Profile & Settings</a>
                            <a href="project-hub.html">📂 Project Hub</a>
                            <hr>
                            <a href="#" onclick="event.preventDefault(); signOut?.();">🚪 Sign Out</a>
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
                background: var(--brand-header-bg);
                color: var(--brand-header-text);
                padding: 0;
                position: sticky;
                top: 0;
                z-index: 1000;
                border-bottom: 1px solid var(--brand-header-border);
                box-shadow: 0 24px 48px rgba(15, 23, 42, 0.35);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
            }

            .nav-container {
                max-width: 1240px;
                margin: 0 auto;
                padding: 0 32px;
                display: flex;
                align-items: center;
                gap: 24px;
                height: 74px;
            }

            .nav-logo {
                display: inline-flex;
                align-items: center;
                gap: 12px;
                text-decoration: none;
                color: #ffffff;
                font-weight: 800;
                font-size: 1.28rem;
                letter-spacing: -0.02em;
                white-space: nowrap;
            }

            .nav-logo-icon {
                font-size: 1.7rem;
                filter: drop-shadow(0 8px 18px rgba(37, 99, 235, 0.42));
            }

            .nav-links {
                display: flex;
                align-items: center;
                gap: 6px;
                flex: 1;
            }

            .nav-link {
                color: var(--brand-header-text);
                text-decoration: none;
                padding: 10px 18px;
                border-radius: 999px;
                transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-weight: 500;
                background: transparent;
                border: 1px solid transparent;
                cursor: pointer;
                font-size: 0.98rem;
                white-space: nowrap;
            }

            .nav-link span:first-child {
                font-size: 1.1rem;
            }

            .nav-link:hover,
            .nav-link:focus {
                background: rgba(148, 163, 184, 0.16);
                border-color: rgba(148, 163, 184, 0.22);
                transform: translateY(-1px);
                color: #ffffff;
            }

            .nav-link.active {
                color: #ffffff;
                background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
                border-color: transparent;
                box-shadow: 0 18px 36px rgba(37, 99, 235, 0.38);
                font-weight: 600;
            }

            .nav-link-emphasis {
                background: rgba(59, 130, 246, 0.16);
                border-color: rgba(59, 130, 246, 0.35);
                color: rgba(226, 232, 240, 0.95);
            }

            .nav-link-emphasis:hover,
            .nav-link-emphasis:focus {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.62) 0%, rgba(37, 99, 235, 0.82) 100%);
                color: #ffffff;
                border-color: transparent;
                box-shadow: 0 18px 36px rgba(37, 99, 235, 0.45);
            }

            .nav-right {
                display: flex;
                align-items: center;
                gap: 14px;
            }

            .nav-dropdown {
                position: relative;
            }

            .nav-dropdown-btn,
            .nav-user-btn {
                display: inline-flex;
                align-items: center;
                gap: 10px;
            }

            .nav-dropdown-content {
                display: none;
                position: absolute;
                top: calc(100% + 14px);
                right: 0;
                background: rgba(15, 23, 42, 0.94);
                border-radius: 18px;
                box-shadow: 0 30px 60px rgba(15, 23, 42, 0.4);
                min-width: 260px;
                padding: 14px;
                z-index: 1001;
                border: 1px solid rgba(96, 165, 250, 0.22);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
            }

            .nav-dropdown-content.show {
                display: block !important;
            }

            .nav-dropdown-content a {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 11px 12px;
                color: rgba(226, 232, 240, 0.9);
                text-decoration: none;
                border-radius: 12px;
                transition: background 0.2s ease, color 0.2s ease;
                font-weight: 500;
                font-size: 0.94rem;
            }

            .nav-dropdown-content a:hover {
                background: rgba(59, 130, 246, 0.18);
                color: #ffffff;
            }

            .nav-dropdown-content hr {
                border: none;
                border-top: 1px solid rgba(148, 163, 184, 0.22);
                margin: 10px 0;
            }

            .nav-dropdown-content .nav-dropdown-category {
                padding: 6px 12px 4px;
                font-size: 0.72rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: rgba(148, 163, 184, 0.78);
            }

            .nav-user-menu {
                min-width: 240px;
            }

            #nav-user-avatar {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.45), rgba(37, 99, 235, 0.75));
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
                color: #ffffff;
                box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
            }

            .nav-label {
                letter-spacing: 0.01em;
            }

            /* Mobile Responsive */
            @media (max-width: 900px) {
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

                /* Aggressively hide any legacy headers/navs to prevent double headers */
                header:not(.unified-nav-header) { display: none !important; }
                nav:not(.unified-nav-header) { display: none !important; }
                .page-header,
                .legacy-header,
                .site-header,
                .app-header,
                .old-header,
                .top-nav { display: none !important; }
        `;
        document.head.appendChild(style);
    }

    updateProjectChip(projectName = 'Master Project') {
        const chip = document.getElementById('nav-project-chip');
        if (chip) {
            chip.textContent = `Project: ${projectName}`;
        }
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

document.addEventListener('projectChanged', (event) => {
    const detail = event.detail || {};
    const projectName = detail.project?.name || detail.projectName || detail.projectId || 'Master Project';
    window.unifiedNavHeader?.updateProjectChip(projectName);
});

document.addEventListener('iterumAppReady', () => {
    const storedProject = (() => {
        try {
            const value = localStorage.getItem('iterum_current_project');
            return value ? JSON.parse(value) : null;
        } catch {
            return null;
        }
    })();
    const projectName = window.projectManager?.currentProject?.name || storedProject?.name || storedProject?.projectName || 'Master Project';
    window.unifiedNavHeader?.updateProjectChip(projectName);
});

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

