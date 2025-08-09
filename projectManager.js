/**
 * Project Manager - Handle project selection and context
 * Manages multi-project organization for recipes, menus, and equipment
 */

class ProjectManager {
    constructor() {
        this.currentProject = null;
        this.projects = [];
        // Use the global API config for consistent URL handling
        this.apiConfig = window.apiConfig || {
            getURL: (endpoint) => `http://localhost:8000/api/${endpoint}`,
            getAuthHeaders: () => ({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`
            })
        };
        this.init();
    }

    /**
     * Initialize project manager
     */
    async init() {
        await this.loadUserProjects();
        this.createProjectSelector();
        this.setupEventListeners();
        await this.setDefaultProject();
    }

    /**
     * Load user's projects from API
     */
    async loadUserProjects() {
        try {
            // Use apiConfig if available for better error handling
            if (this.apiConfig.get) {
                const response = await this.apiConfig.get('projects/');
                this.projects = await response.json();
            } else {
                const response = await fetch(this.apiConfig.getURL('projects/'), {
                    headers: this.apiConfig.getAuthHeaders()
                });

                if (response.ok) {
                    this.projects = await response.json();
                } else {
                    throw new Error(`API error: ${response.status}`);
                }
            }
            console.log('✅ Loaded projects:', this.projects.length);
        } catch (error) {
            console.warn('⚠️ Projects API unavailable, using offline mode:', error.message);
            this.projects = this.getOfflineProjects();
        }
    }

    /**
     * Get offline projects from localStorage
     */
    getOfflineProjects() {
        const currentUser = this.getCurrentUser();
        if (!currentUser) return [];

        const stored = localStorage.getItem(`projects_${currentUser.id}`);
        if (stored) {
            return JSON.parse(stored);
        }

        // Create default Full Library project
        const defaultProject = {
            id: 'offline_default',
            name: 'Full Library',
            description: 'Complete recipe and menu library',
            is_default: true,
            is_active: true,
            color_theme: '#3B82F6',
            owner_id: currentUser.id,
            recipe_count: 0,
            menu_count: 0,
            equipment_count: 0
        };

        localStorage.setItem(`projects_${currentUser.id}`, JSON.stringify([defaultProject]));
        return [defaultProject];
    }

    /**
     * Create project selector UI
     */
    createProjectSelector() {
        // Remove existing selector
        const existing = document.getElementById('project-selector-container');
        if (existing) existing.remove();

        // Create container
        const container = document.createElement('div');
        container.id = 'project-selector-container';
        container.className = 'project-selector-container';

        container.innerHTML = `
            <div class="project-selector">
                <div class="project-current" id="current-project-display">
                    <div class="project-color-indicator" id="project-color"></div>
                    <div class="project-info">
                        <span class="project-name" id="current-project-name">Full Library</span>
                        <span class="project-stats" id="current-project-stats">Loading...</span>
                    </div>
                    <div class="project-dropdown-arrow">▼</div>
                </div>
                
                <div class="project-dropdown" id="project-dropdown" style="display: none;">
                    <div class="project-search">
                        <input type="text" id="project-search" placeholder="Search projects..." />
                    </div>
                    
                    <div class="project-list" id="project-list">
                        <!-- Projects will be populated here -->
                    </div>
                    
                    <div class="project-actions">
                        <button class="btn-new-project" id="btn-new-project">
                            <span class="icon">+</span>
                            <span>New Project</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Insert into the header project selector area if it exists
        const headerProjectArea = document.getElementById('header-project-selector');
        if (headerProjectArea) {
            // Clear the hidden class and make it visible
            headerProjectArea.classList.remove('hidden');
            headerProjectArea.appendChild(container);
            console.log('✅ Project selector inserted into header');
        } else {
            console.warn('⚠️ Header project selector not found, using fallback');
            // Fallback: Insert after header/navigation
            const header = document.querySelector('header, nav, .header, .navigation');
            if (header) {
                header.insertAdjacentElement('afterend', container);
            } else {
                document.body.insertBefore(container, document.body.firstChild);
            }
        }

        this.populateProjectList();
        this.injectProjectStyles();
    }

    /**
     * Populate project list dropdown
     */
    populateProjectList() {
        const projectList = document.getElementById('project-list');
        if (!projectList) return;

        projectList.innerHTML = '';

        this.projects.forEach(project => {
            const projectItem = document.createElement('div');
            projectItem.className = `project-item ${project.is_default ? 'default-project' : ''}`;
            projectItem.dataset.projectId = project.id;

            const stats = `${project.recipe_count || 0} recipes, ${project.menu_count || 0} menus`;
            
            projectItem.innerHTML = `
                <div class="project-color-indicator" style="background-color: ${project.color_theme}"></div>
                <div class="project-details">
                    <div class="project-name">${project.name}</div>
                    <div class="project-meta">
                        ${project.restaurant_name ? `<span class="restaurant">${project.restaurant_name}</span>` : ''}
                        <span class="stats">${stats}</span>
                    </div>
                </div>
                <div class="project-actions">
                    ${!project.is_default ? '<button class="btn-edit-project" title="Edit">⚙️</button>' : ''}
                </div>
            `;

            projectItem.addEventListener('click', () => this.selectProject(project));
            projectList.appendChild(projectItem);
        });
    }

    /**
     * Set default project (Full Library)
     */
    async setDefaultProject() {
        const defaultProject = this.projects.find(p => p.is_default) || this.projects[0];
        if (defaultProject) {
            await this.selectProject(defaultProject);
        }
    }

    /**
     * Select a project
     */
    async selectProject(project) {
        this.currentProject = project;
        
        // Update UI
        this.updateCurrentProjectDisplay();
        this.hideDropdown();
        
        // Store selection
        const currentUser = this.getCurrentUser();
        if (currentUser) {
            localStorage.setItem(`current_project_${currentUser.id}`, JSON.stringify(project));
        }
        
        // Trigger project change event
        this.triggerProjectChange(project);
        
        console.log(`📁 Selected project: ${project.name}`);
    }

    /**
     * Update current project display
     */
    updateCurrentProjectDisplay() {
        if (!this.currentProject) return;

        const nameEl = document.getElementById('current-project-name');
        const colorEl = document.getElementById('project-color');
        const statsEl = document.getElementById('current-project-stats');

        if (nameEl) nameEl.textContent = this.currentProject.name;
        if (colorEl) colorEl.style.backgroundColor = this.currentProject.color_theme;
        
        if (statsEl) {
            const stats = `${this.currentProject.recipe_count || 0} recipes, ${this.currentProject.menu_count || 0} menus`;
            statsEl.textContent = stats;
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Project selector toggle
        document.addEventListener('click', (e) => {
            if (e.target.closest('#current-project-display')) {
                this.toggleDropdown();
            } else if (!e.target.closest('.project-dropdown')) {
                this.hideDropdown();
            }
        });

        // New project button
        document.addEventListener('click', (e) => {
            if (e.target.closest('#btn-new-project')) {
                this.showNewProjectModal();
            }
        });

        // Project search
        document.addEventListener('input', (e) => {
            if (e.target.id === 'project-search') {
                this.filterProjects(e.target.value);
            }
        });
    }

    /**
     * Toggle project dropdown
     */
    toggleDropdown() {
        const dropdown = document.getElementById('project-dropdown');
        if (dropdown) {
            const isVisible = dropdown.style.display !== 'none';
            dropdown.style.display = isVisible ? 'none' : 'block';
            
            if (!isVisible) {
                // Reset search when opening
                const searchInput = document.getElementById('project-search');
                if (searchInput) {
                    searchInput.value = '';
                    this.filterProjects('');
                }
            }
        }
    }

    /**
     * Hide dropdown
     */
    hideDropdown() {
        const dropdown = document.getElementById('project-dropdown');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    }

    /**
     * Filter projects by search term
     */
    filterProjects(searchTerm) {
        const projectItems = document.querySelectorAll('.project-item');
        const term = searchTerm.toLowerCase();

        projectItems.forEach(item => {
            const name = item.querySelector('.project-name').textContent.toLowerCase();
            const restaurant = item.querySelector('.restaurant')?.textContent?.toLowerCase() || '';
            
            const matches = name.includes(term) || restaurant.includes(term);
            item.style.display = matches ? 'flex' : 'none';
        });
    }

    /**
     * Show new project modal
     */
    showNewProjectModal() {
        const modal = this.createNewProjectModal();
        document.body.appendChild(modal);
        
        // Focus name input
        setTimeout(() => {
            const nameInput = modal.querySelector('#new-project-name');
            if (nameInput) nameInput.focus();
        }, 100);
    }

    /**
     * Create new project modal
     */
    createNewProjectModal() {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'new-project-modal';

        modal.innerHTML = `
            <div class="modal-content new-project-modal">
                <div class="modal-header">
                    <h2>Create New Project</h2>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
                </div>
                
                <div class="modal-body">
                    <form id="new-project-form">
                        <div class="form-group">
                            <label for="new-project-name">Project Name *</label>
                            <input type="text" id="new-project-name" name="name" required 
                                   placeholder="My Restaurant, Special Menu, etc." maxlength="200">
                        </div>
                        
                        <div class="form-group">
                            <label for="new-project-restaurant">Restaurant/Venue Name</label>
                            <input type="text" id="new-project-restaurant" name="restaurant_name" 
                                   placeholder="Optional - name of restaurant or venue" maxlength="200">
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label for="new-project-cuisine">Cuisine Type</label>
                                <select id="new-project-cuisine" name="cuisine_type">
                                    <option value="">Select cuisine type</option>
                                    <option value="American">American</option>
                                    <option value="Italian">Italian</option>
                                    <option value="French">French</option>
                                    <option value="Mexican">Mexican</option>
                                    <option value="Asian">Asian</option>
                                    <option value="Mediterranean">Mediterranean</option>
                                    <option value="Fusion">Fusion</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="new-project-color">Color Theme</label>
                                <div class="color-picker">
                                    <input type="color" id="new-project-color" name="color_theme" value="#3B82F6">
                                    <div class="color-presets">
                                        <div class="color-preset" data-color="#3B82F6" style="background: #3B82F6" title="Blue"></div>
                                        <div class="color-preset" data-color="#10B981" style="background: #10B981" title="Green"></div>
                                        <div class="color-preset" data-color="#F59E0B" style="background: #F59E0B" title="Orange"></div>
                                        <div class="color-preset" data-color="#EF4444" style="background: #EF4444" title="Red"></div>
                                        <div class="color-preset" data-color="#8B5CF6" style="background: #8B5CF6" title="Purple"></div>
                                        <div class="color-preset" data-color="#6B7280" style="background: #6B7280" title="Gray"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="new-project-description">Description</label>
                            <textarea id="new-project-description" name="description" rows="3" 
                                      placeholder="Brief description of this project..." maxlength="500"></textarea>
                        </div>
                    </form>
                </div>
                
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">
                        Cancel
                    </button>
                    <button type="button" class="btn btn-primary" onclick="window.projectManager.createProject()">
                        Create Project
                    </button>
                </div>
            </div>
        `;

        // Color preset selection
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('color-preset')) {
                const color = e.target.dataset.color;
                modal.querySelector('#new-project-color').value = color;
                
                // Update preset selection
                modal.querySelectorAll('.color-preset').forEach(p => p.classList.remove('selected'));
                e.target.classList.add('selected');
            }
        });

        return modal;
    }

    /**
     * Create new project
     */
    async createProject() {
        const form = document.getElementById('new-project-form');
        if (!form) return;

        const formData = new FormData(form);
        const projectData = {
            name: formData.get('name').trim(),
            restaurant_name: formData.get('restaurant_name').trim() || null,
            cuisine_type: formData.get('cuisine_type') || null,
            color_theme: formData.get('color_theme') || '#3B82F6',
            description: formData.get('description').trim() || null
        };

        // Validation
        if (!projectData.name) {
            alert('Please enter a project name');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/projects/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeaders()
                },
                body: JSON.stringify(projectData)
            });

            if (response.ok) {
                const newProject = await response.json();
                
                // Add to projects list
                this.projects.push(newProject);
                
                // Update UI
                this.populateProjectList();
                
                // Select new project
                await this.selectProject(newProject);
                
                // Close modal
                document.getElementById('new-project-modal')?.remove();
                
                // Show success message
                this.showNotification(`Project "${newProject.name}" created successfully!`, 'success');
                
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to create project');
            }
            
        } catch (error) {
            console.error('Error creating project:', error);
            alert(`Failed to create project: ${error.message}`);
        }
    }

    /**
     * Trigger project change event for other components
     */
    triggerProjectChange(project) {
        const event = new CustomEvent('projectChanged', {
            detail: { project }
        });
        
        document.dispatchEvent(event);
        
        // Also trigger on window for legacy support
        if (window.onProjectChange) {
            window.onProjectChange(project);
        }
    }

    /**
     * Get current project
     */
    getCurrentProject() {
        return this.currentProject;
    }

    /**
     * Get project-scoped storage key
     */
    getProjectStorageKey(key) {
        const projectId = this.currentProject?.id || 'default';
        const currentUser = this.getCurrentUser();
        const userId = currentUser?.id || 'anonymous';
        
        return `${key}_project_${projectId}_user_${userId}`;
    }

    /**
     * Helper: Get current user
     */
    getCurrentUser() {
        try {
            return JSON.parse(localStorage.getItem('current_user'));
        } catch {
            return null;
        }
    }

    /**
     * Helper: Get auth headers
     */
    getAuthHeaders() {
        const token = localStorage.getItem('auth_token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        // Use existing notification system if available
        if (window.showNotification) {
            window.showNotification(message, type);
            return;
        }

        // Simple fallback notification
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            padding: 12px 20px; border-radius: 8px; color: white;
            background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#3B82F6'};
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    /**
     * Inject project selector styles
     */
    injectProjectStyles() {
        if (document.getElementById('project-manager-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'project-manager-styles';
        styles.textContent = `
            /* Project Selector - Header Integrated Version */
            .project-selector-container {
                position: relative;
                z-index: 1000;
                width: 100%;
            }
            
            .project-selector {
                position: relative;
                width: 100%;
            }
            
            .project-current {
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: pointer;
                padding: 8px 16px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background: white;
                transition: all 0.2s;
                width: 100%;
                min-height: 44px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            
            .project-current:hover {
                border-color: #10b981;
                box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1), 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            
            .project-color-indicator {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #10b981;
                flex-shrink: 0;
                border: 2px solid white;
                box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1);
            }
            
            .project-info {
                flex: 1;
                min-width: 0;
            }
            
            .project-name {
                font-weight: 600;
                color: #111827;
                display: block;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 14px;
            }
            
            .project-stats {
                font-size: 11px;
                color: #6b7280;
                display: block;
                line-height: 1.2;
            }
            
            .project-dropdown-arrow {
                color: #6b7280;
                font-size: 12px;
                transition: transform 0.2s;
            }
            
            .project-current:hover .project-dropdown-arrow {
                transform: rotate(180deg);
            }
            
            .project-dropdown {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                max-width: 480px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                z-index: 1001;
                margin-top: 8px;
            }
            
            .project-search {
                padding: 12px;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .project-search input {
                width: 100%;
                padding: 8px 12px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 14px;
            }
            
            .project-list {
                max-height: 300px;
                overflow-y: auto;
            }
            
            .project-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                cursor: pointer;
                transition: background 0.2s;
                border-bottom: 1px solid #f3f4f6;
            }
            
            .project-item:hover {
                background: #f8fafc;
            }
            
            .project-item.default-project {
                background: #fef3c7;
            }
            
            .project-item.default-project:hover {
                background: #fde68a;
            }
            
            .project-details {
                flex: 1;
                min-width: 0;
            }
            
            .project-details .project-name {
                font-weight: 500;
                color: #111827;
                margin-bottom: 2px;
            }
            
            .project-meta {
                font-size: 12px;
                color: #6b7280;
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            
            .project-meta .restaurant {
                font-weight: 500;
            }
            
            .project-actions {
                display: flex;
                gap: 4px;
            }
            
            .btn-edit-project {
                background: none;
                border: none;
                padding: 4px;
                cursor: pointer;
                border-radius: 4px;
                opacity: 0.6;
                transition: opacity 0.2s;
            }
            
            .btn-edit-project:hover {
                opacity: 1;
                background: #f3f4f6;
            }
            
            .project-actions {
                padding: 12px;
                border-top: 1px solid #e5e7eb;
                background: #f9fafb;
            }
            
            .btn-new-project {
                display: flex;
                align-items: center;
                gap: 8px;
                width: 100%;
                padding: 10px 16px;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s;
            }
            
            .btn-new-project:hover {
                background: #2563eb;
            }
            
            .btn-new-project .icon {
                font-size: 16px;
                font-weight: bold;
            }
            
            /* New Project Modal */
            .new-project-modal {
                width: 600px;
                max-width: 90vw;
            }
            
            .form-row {
                display: flex;
                gap: 16px;
            }
            
            .form-row .form-group {
                flex: 1;
            }
            
            .color-picker {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .color-picker input[type="color"] {
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }
            
            .color-presets {
                display: flex;
                gap: 6px;
            }
            
            .color-preset {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                cursor: pointer;
                border: 2px solid transparent;
                transition: border-color 0.2s;
            }
            
            .color-preset:hover,
            .color-preset.selected {
                border-color: #374151;
            }
            
            /* Responsive */
            @media (max-width: 1024px) {
                .project-selector-container {
                    display: none; /* Hide in header on smaller screens */
                }
            }
            
            @media (max-width: 768px) {
                .form-row {
                    flex-direction: column;
                }
            }
        `;
        
        document.head.appendChild(styles);
    }
}

// Initialize project manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.projectManager = new ProjectManager();
    });
} else {
    window.projectManager = new ProjectManager();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProjectManager;
}