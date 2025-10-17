/**
 * Vendor Management System for Iterum R&D Chef Notebook
 * Handles vendor CRUD operations, bulk import/export, and management
 */

class VendorManager {
    constructor() {
        this.vendors = [];
        this.selectedVendors = new Set();
        this.currentView = 'list';
        this.currentFilters = {
            search: '',
            company: '',
            city: '',
            state: '',
            status: 'all'
        };
        
        this.init();
    }
    
    init() {
        console.log('🏪 Initializing Vendor Manager...');
        this.setupEventListeners();
        this.loadVendors();
        this.updateVendorCount();
    }
    
    setupEventListeners() {
        // Add vendor button
        const addVendorBtn = document.getElementById('add-vendor-btn');
        if (addVendorBtn) {
            addVendorBtn.addEventListener('click', () => this.showAddVendorModal());
        }
        
        // Import vendors button
        const importVendorsBtn = document.getElementById('import-vendors-btn');
        if (importVendorsBtn) {
            importVendorsBtn.addEventListener('click', () => this.showImportModal());
        }
        
        // Export vendors button
        const exportVendorsBtn = document.getElementById('export-vendors-btn');
        if (exportVendorsBtn) {
            exportVendorsBtn.addEventListener('click', () => this.exportVendors());
        }
        
        // Bulk actions
        const bulkDeleteBtn = document.getElementById('bulk-delete-btn');
        if (bulkDeleteBtn) {
            bulkDeleteBtn.addEventListener('click', () => this.bulkDeleteVendors());
        }
        
        const bulkEditBtn = document.getElementById('bulk-edit-btn');
        if (bulkEditBtn) {
            bulkEditBtn.addEventListener('click', () => this.bulkEditVendors());
        }
        
        // Search and filters
        const searchInput = document.getElementById('vendor-search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(() => this.filterVendors(), 300));
        }
        
        const companyFilter = document.getElementById('company-filter');
        if (companyFilter) {
            companyFilter.addEventListener('change', () => this.filterVendors());
        }
        
        const cityFilter = document.getElementById('city-filter');
        if (cityFilter) {
            cityFilter.addEventListener('change', () => this.filterVendors());
        }
        
        const stateFilter = document.getElementById('state-filter');
        if (stateFilter) {
            stateFilter.addEventListener('change', () => this.filterVendors());
        }
        
        const statusFilter = document.getElementById('status-filter');
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.filterVendors());
        }
        
        // Select all checkbox
        const selectAllCheckbox = document.getElementById('select-all-vendors');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => this.toggleSelectAll(e.target.checked));
        }
    }
    
    async loadVendors() {
        try {
            console.log('🔍 Loading vendors...');
            
            // Try to load from backend API first
            const response = await fetch('/api/vendors/');
            if (response.ok) {
                const data = await response.json();
                this.vendors = data.vendors || [];
                console.log(`✅ Loaded ${this.vendors.length} vendors from API`);
            } else {
                console.log('⚠️ API not available, trying user file storage');
                // Try to load from user file storage
                if (!this.loadVendorsFromFile()) {
                    console.log('📁 No user file found, using sample data');
                    this.loadSampleVendors();
                }
            }
            
            this.updateVendorCount();
            this.displayVendors();
            this.updateFilters();
            
        } catch (error) {
            console.error('❌ Error loading vendors:', error);
            // Try to load from user file storage
            if (!this.loadVendorsFromFile()) {
                console.log('📁 No user file found, using sample data');
                this.loadSampleVendors();
            }
        }
    }
    
    loadSampleVendors() {
        // Sample vendor data for demonstration
        this.vendors = [
            {
                id: 1,
                name: 'John Smith',
                company: 'Fresh Foods Inc',
                email: 'john@freshfoods.com',
                phone: '555-1234',
                mobile: '555-5678',
                city: 'Boston',
                state: 'MA',
                zip_code: '02101',
                specialties: ['produce', 'dairy'],
                notes: 'Reliable supplier for fresh produce',
                is_active: true,
                created_at: new Date().toISOString()
            },
            {
                id: 2,
                name: 'Sarah Johnson',
                company: 'Quality Meats Co',
                email: 'sarah@qualitymeats.com',
                phone: '555-2345',
                mobile: '555-6789',
                city: 'Chicago',
                state: 'IL',
                zip_code: '60601',
                specialties: ['meat', 'poultry'],
                notes: 'Premium meat supplier',
                is_active: true,
                created_at: new Date().toISOString()
            },
            {
                id: 3,
                name: 'Mike Chen',
                company: 'Asian Spices Ltd',
                email: 'mike@asianspices.com',
                phone: '555-3456',
                mobile: '555-7890',
                city: 'Los Angeles',
                state: 'CA',
                zip_code: '90001',
                specialties: ['spices', 'asian ingredients'],
                notes: 'Specialized in Asian ingredients',
                is_active: true,
                created_at: new Date().toISOString()
            }
        ];
        
        // Save sample vendors to user file
        this.saveVendorsToFile();
    }
    
    saveVendorsToFile() {
        // Use user-specific file storage first, fallback to localStorage
        if (window.userDataManager && window.userDataManager.isUserLoggedIn()) {
            const userId = window.userDataManager.getCurrentUserId();
            const filename = `user_${userId}_vendors.json`;
            window.userDataManager.saveUserFile(filename, this.vendors);
            console.log(`💾 Saved ${this.vendors.length} vendors to user file`);
        } else {
            // Fallback to localStorage
            localStorage.setItem('iterum_vendors', JSON.stringify(this.vendors));
            console.log(`💾 Saved ${this.vendors.length} vendors to localStorage`);
        }
    }
    
    loadVendorsFromFile() {
        // Use user-specific file storage first, fallback to localStorage
        if (window.userDataManager && window.userDataManager.isUserLoggedIn()) {
            const userId = window.userDataManager.getCurrentUserId();
            const filename = `user_${userId}_vendors.json`;
            const loadedVendors = window.userDataManager.loadUserFile(filename);
            if (loadedVendors && Array.isArray(loadedVendors)) {
                this.vendors = loadedVendors;
                console.log(`📖 Loaded ${this.vendors.length} vendors from user file`);
                return true;
            }
        } else {
            // Fallback to localStorage
            const storedVendors = localStorage.getItem('iterum_vendors');
            if (storedVendors) {
                this.vendors = JSON.parse(storedVendors);
                console.log(`📖 Loaded ${this.vendors.length} vendors from localStorage`);
                return true;
            }
        }
        return false;
    }
    
    displayVendors() {
        const container = document.getElementById('vendors-container');
        if (!container) return;
        
        if (this.vendors.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🏪</div>
                    <h3 class="empty-state-title">No Vendors Found</h3>
                    <p class="empty-state-description">Get started by adding your first vendor or importing from Excel/CSV.</p>
                    <div class="empty-state-actions">
                        <button onclick="vendorManager.showAddVendorModal()" class="btn btn-primary">
                            ➕ Add First Vendor
                        </button>
                        <button onclick="vendorManager.showImportModal()" class="btn btn-secondary">
                            📥 Import Vendors
                        </button>
                    </div>
                </div>
            `;
            return;
        }
        
        const filteredVendors = this.getFilteredVendors();
        
        container.innerHTML = `
            <div class="vendors-table-container">
                <table class="vendors-table">
                    <thead>
                        <tr>
                            <th>
                                <input type="checkbox" id="select-all-vendors" class="vendor-checkbox">
                            </th>
                            <th>Vendor</th>
                            <th>Company</th>
                            <th>Contact</th>
                            <th>Location</th>
                            <th>Specialties</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filteredVendors.map(vendor => this.renderVendorRow(vendor)).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        // Re-attach event listeners
        this.attachRowEventListeners();
    }
    
    renderVendorRow(vendor) {
        const isSelected = this.selectedVendors.has(vendor.id);
        const specialties = vendor.specialties?.join(', ') || 'None';
        const statusClass = vendor.is_active ? 'status-active' : 'status-inactive';
        const statusText = vendor.is_active ? 'Active' : 'Inactive';
        
        return `
            <tr class="vendor-row ${isSelected ? 'selected' : ''}" data-vendor-id="${vendor.id}">
                <td>
                    <input type="checkbox" class="vendor-checkbox" value="${vendor.id}" ${isSelected ? 'checked' : ''}>
                </td>
                <td>
                    <div class="vendor-info">
                        <div class="vendor-name">${vendor.name}</div>
                        <div class="vendor-email">${vendor.email || 'No email'}</div>
                    </div>
                </td>
                <td>
                    <div class="company-info">
                        <div class="company-name">${vendor.company || 'No company'}</div>
                        <div class="company-website">${vendor.website ? `<a href="${vendor.website}" target="_blank">${vendor.website}</a>` : 'No website'}</div>
                    </div>
                </td>
                <td>
                    <div class="contact-info">
                        <div class="contact-phone">${vendor.phone || 'No phone'}</div>
                        <div class="contact-mobile">${vendor.mobile || 'No mobile'}</div>
                    </div>
                </td>
                <td>
                    <div class="location-info">
                        <div class="location-city">${vendor.city || 'No city'}</div>
                        <div class="location-state">${vendor.state || 'No state'}</div>
                    </div>
                </td>
                <td>
                    <div class="specialties-info">
                        <span class="specialties-tags">${specialties}</span>
                    </div>
                </td>
                <td>
                    <span class="status-badge ${statusClass}">${statusText}</span>
                </td>
                <td>
                    <div class="vendor-actions">
                        <button onclick="vendorManager.editVendor(${vendor.id})" class="btn btn-sm btn-secondary">
                            ✏️ Edit
                        </button>
                        <button onclick="vendorManager.deleteVendor(${vendor.id})" class="btn btn-sm btn-danger">
                            🗑️ Delete
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }
    
    attachRowEventListeners() {
        // Checkbox selection
        document.querySelectorAll('.vendor-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const vendorId = parseInt(e.target.value);
                if (e.target.checked) {
                    this.selectedVendors.add(vendorId);
                } else {
                    this.selectedVendors.delete(vendorId);
                }
                this.updateBulkActions();
                this.updateRowSelection(vendorId, e.target.checked);
            });
        });
        
        // Select all functionality
        const selectAllCheckbox = document.getElementById('select-all-vendors');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => {
                this.toggleSelectAll(e.target.checked);
            });
        }
    }
    
    toggleSelectAll(checked) {
        const checkboxes = document.querySelectorAll('.vendor-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = checked;
            const vendorId = parseInt(checkbox.value);
            if (checked) {
                this.selectedVendors.add(vendorId);
            } else {
                this.selectedVendors.delete(vendorId);
            }
            this.updateRowSelection(vendorId, checked);
        });
        this.updateBulkActions();
    }
    
    updateRowSelection(vendorId, selected) {
        const row = document.querySelector(`[data-vendor-id="${vendorId}"]`);
        if (row) {
            row.classList.toggle('selected', selected);
        }
    }
    
    updateBulkActions() {
        const bulkActions = document.getElementById('bulk-actions');
        if (!bulkActions) return;
        
        const hasSelection = this.selectedVendors.size > 0;
        bulkActions.style.display = hasSelection ? 'flex' : 'none';
        
        if (hasSelection) {
            const countElement = document.getElementById('selected-count');
            if (countElement) {
                countElement.textContent = this.selectedVendors.size;
            }
        }
    }
    
    getFilteredVendors() {
        let filtered = [...this.vendors];
        
        // Search filter
        if (this.currentFilters.search) {
            const searchTerm = this.currentFilters.search.toLowerCase();
            filtered = filtered.filter(vendor => 
                vendor.name.toLowerCase().includes(searchTerm) ||
                vendor.company?.toLowerCase().includes(searchTerm) ||
                vendor.email?.toLowerCase().includes(searchTerm) ||
                vendor.city?.toLowerCase().includes(searchTerm)
            );
        }
        
        // Company filter
        if (this.currentFilters.company) {
            filtered = filtered.filter(vendor => 
                vendor.company === this.currentFilters.company
            );
        }
        
        // City filter
        if (this.currentFilters.city) {
            filtered = filtered.filter(vendor => 
                vendor.city === this.currentFilters.city
            );
        }
        
        // State filter
        if (this.currentFilters.state) {
            filtered = filtered.filter(vendor => 
                vendor.state === this.currentFilters.state
            );
        }
        
        // Status filter
        if (this.currentFilters.status !== 'all') {
            const isActive = this.currentFilters.status === 'active';
            filtered = filtered.filter(vendor => vendor.is_active === isActive);
        }
        
        return filtered;
    }
    
    filterVendors() {
        // Update filters from form inputs
        const searchInput = document.getElementById('vendor-search');
        const companyFilter = document.getElementById('company-filter');
        const cityFilter = document.getElementById('city-filter');
        const stateFilter = document.getElementById('state-filter');
        const statusFilter = document.getElementById('status-filter');
        
        if (searchInput) this.currentFilters.search = searchInput.value;
        if (companyFilter) this.currentFilters.company = companyFilter.value;
        if (cityFilter) this.currentFilters.city = cityFilter.value;
        if (stateFilter) this.currentFilters.state = stateFilter.value;
        if (statusFilter) this.currentFilters.status = statusFilter.value;
        
        this.displayVendors();
    }
    
    updateFilters() {
        // Get unique values for filter dropdowns
        const companies = [...new Set(this.vendors.map(v => v.company).filter(Boolean))];
        const cities = [...new Set(this.vendors.map(v => v.city).filter(Boolean))];
        const states = [...new Set(this.vendors.map(v => v.state).filter(Boolean))];
        
        // Update company filter
        const companyFilter = document.getElementById('company-filter');
        if (companyFilter) {
            companyFilter.innerHTML = `
                <option value="">All Companies</option>
                ${companies.map(company => `<option value="${company}">${company}</option>`).join('')}
            `;
        }
        
        // Update city filter
        const cityFilter = document.getElementById('city-filter');
        if (cityFilter) {
            cityFilter.innerHTML = `
                <option value="">All Cities</option>
                ${cities.map(city => `<option value="${city}">${city}</option>`).join('')}
            `;
        }
        
        // Update state filter
        const stateFilter = document.getElementById('state-filter');
        if (stateFilter) {
            stateFilter.innerHTML = `
                <option value="">All States</option>
                ${states.map(state => `<option value="${state}">${state}</state>`).join('')}
            `;
        }
    }
    
    updateVendorCount() {
        const countElement = document.getElementById('vendor-count');
        if (countElement) {
            countElement.textContent = this.vendors.length;
        }
    }
    
    showAddVendorModal() {
        this.showVendorModal('add');
    }
    
    showVendorModal(mode = 'add', vendor = null) {
        const modal = this.createVendorModal(mode, vendor);
        if (modal) {
            document.body.appendChild(modal);
            
            // Show modal with animation
            setTimeout(() => {
                modal.style.opacity = '1';
            }, 10);
            
            console.log(`✅ Vendor ${mode} modal displayed`);
        }
    }
    
    createVendorModal(mode, vendor) {
        const isEdit = mode === 'edit';
        const title = isEdit ? 'Edit Vendor' : 'Add New Vendor';
        const buttonText = isEdit ? 'Update Vendor' : 'Add Vendor';
        
        const modal = document.createElement('div');
        modal.className = 'vendor-modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] opacity-0 transition-opacity duration-300';
        modal.setAttribute('data-modal', 'vendor');
        
        modal.innerHTML = `
            <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <div class="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
                    <h2 class="text-xl font-semibold text-gray-900">${title}</h2>
                    <p class="text-sm text-gray-600 mt-1">${isEdit ? 'Update vendor information' : 'Add a new vendor to your system'}</p>
                </div>
                
                <div class="p-6">
                    <form id="vendor-form" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label for="vendor-name" class="block text-sm font-medium text-gray-700 mb-1">
                                    Name *
                                </label>
                                <input type="text" id="vendor-name" required
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter vendor name"
                                       value="${vendor?.name || ''}">
                            </div>
                            
                            <div>
                                <label for="vendor-company" class="block text-sm font-medium text-gray-700 mb-1">
                                    Company
                                </label>
                                <input type="text" id="vendor-company"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter company name"
                                       value="${vendor?.company || ''}">
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label for="vendor-email" class="block text-sm font-medium text-gray-700 mb-1">
                                    Email
                                </label>
                                <input type="email" id="vendor-email"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter email address"
                                       value="${vendor?.email || ''}">
                            </div>
                            
                            <div>
                                <label for="vendor-phone" class="block text-sm font-medium text-gray-700 mb-1">
                                    Phone
                                </label>
                                <input type="tel" id="vendor-phone"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter phone number"
                                       value="${vendor?.phone || ''}">
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label for="vendor-mobile" class="block text-sm font-medium text-gray-700 mb-1">
                                    Mobile
                                </label>
                                <input type="tel" id="vendor-mobile"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter mobile number"
                                       value="${vendor?.mobile || ''}">
                            </div>
                            
                            <div>
                                <label for="vendor-website" class="block text-sm font-medium text-gray-700 mb-1">
                                    Website
                                </label>
                                <input type="url" id="vendor-website"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter website URL"
                                       value="${vendor?.website || ''}">
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <label for="vendor-street" class="block text-sm font-medium text-gray-700 mb-1">
                                    Street
                                </label>
                                <input type="text" id="vendor-street"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter street address"
                                       value="${vendor?.street || ''}">
                            </div>
                            
                            <div>
                                <label for="vendor-city" class="block text-sm font-medium text-gray-700 mb-1">
                                    City
                                </label>
                                <input type="text" id="vendor-city"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter city"
                                       value="${vendor?.city || ''}">
                            </div>
                            
                            <div>
                                <label for="vendor-state" class="block text-sm font-medium text-gray-700 mb-1">
                                    State
                                </label>
                                <input type="text" id="vendor-state"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter state"
                                       value="${vendor?.state || ''}">
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label for="vendor-zip" class="block text-sm font-medium text-gray-700 mb-1">
                                    ZIP Code
                                </label>
                                <input type="text" id="vendor-zip"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="Enter ZIP code"
                                       value="${vendor?.zip_code || ''}">
                            </div>
                            
                            <div>
                                <label for="vendor-specialties" class="block text-sm font-medium text-gray-700 mb-1">
                                    Specialties
                                </label>
                                <input type="text" id="vendor-specialties"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="e.g., produce, dairy, meat"
                                       value="${vendor?.specialties?.join(', ') || ''}">
                            </div>
                        </div>
                        
                        <div>
                            <label for="vendor-notes" class="block text-sm font-medium text-gray-700 mb-1">
                                Notes
                            </label>
                            <textarea id="vendor-notes" rows="3"
                                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                      placeholder="Enter any additional notes about this vendor">${vendor?.notes || ''}</textarea>
                        </div>
                        
                        <div class="flex items-center">
                            <input type="checkbox" id="vendor-active" class="mr-2"
                                   ${vendor?.is_active !== false ? 'checked' : ''}>
                            <label for="vendor-active" class="text-sm text-gray-700">
                                Vendor is active
                            </label>
                        </div>
                    </form>
                    
                    <div class="flex space-x-3 pt-6">
                        <button onclick="vendorManager.saveVendor()" 
                                class="flex-1 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors font-medium">
                            ${buttonText}
                        </button>
                        <button onclick="vendorManager.closeVendorModal()" 
                                class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 px-4 py-2 rounded-lg transition-colors">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        return modal;
    }
    
    async saveVendor() {
        const form = document.getElementById('vendor-form');
        if (!form) return;
        
        const formData = {
            name: document.getElementById('vendor-name').value.trim(),
            company: document.getElementById('vendor-company').value.trim(),
            email: document.getElementById('vendor-email').value.trim(),
            phone: document.getElementById('vendor-phone').value.trim(),
            mobile: document.getElementById('vendor-mobile').value.trim(),
            website: document.getElementById('vendor-website').value.trim(),
            street: document.getElementById('vendor-street').value.trim(),
            city: document.getElementById('vendor-city').value.trim(),
            state: document.getElementById('vendor-state').value.trim(),
            zip_code: document.getElementById('vendor-zip').value.trim(),
            specialties: document.getElementById('vendor-specialties').value.trim().split(',').map(s => s.trim()).filter(Boolean),
            notes: document.getElementById('vendor-notes').value.trim(),
            is_active: document.getElementById('vendor-active').checked
        };
        
        if (!formData.name) {
            alert('Please enter a vendor name');
            return;
        }
        
        // Check if we're editing or adding
        const modal = document.querySelector('.vendor-modal-overlay[data-modal="vendor"]');
        const isEdit = modal && modal.dataset.vendorId;
        const vendorId = isEdit ? parseInt(modal.dataset.vendorId) : null;
        
        try {
            if (isEdit) {
                // UPDATE existing vendor
                const response = await fetch(`/api/vendors/${vendorId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    const updatedVendor = await response.json();
                    const index = this.vendors.findIndex(v => v.id === vendorId);
                    if (index !== -1) {
                        this.vendors[index] = updatedVendor;
                    }
                    console.log('✅ Vendor updated in API:', updatedVendor.name);
                } else {
                    // Fallback to local storage
                    const index = this.vendors.findIndex(v => v.id === vendorId);
                    if (index !== -1) {
                        this.vendors[index] = {
                            ...this.vendors[index],
                            ...formData,
                            updated_at: new Date().toISOString()
                        };
                    }
                    console.log('✅ Vendor updated locally:', formData.name);
                }
            } else {
                // ADD new vendor
                const response = await fetch('/api/vendors/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    const savedVendor = await response.json();
                    this.vendors.push(savedVendor);
                    console.log('✅ Vendor saved to API:', savedVendor.name);
                } else {
                    // Fallback to local storage
                    const newVendor = {
                        id: Date.now(),
                        ...formData,
                        created_at: new Date().toISOString()
                    };
                    this.vendors.push(newVendor);
                    console.log('✅ Vendor saved locally:', newVendor.name);
                }
            }
            
            // Save to user file storage
            this.saveVendorsToFile();
            
            // Close modal first
            this.closeVendorModal();
            
            // Then update display with a small delay to ensure modal is closed
            setTimeout(() => {
                this.updateVendorCount();
                this.displayVendors();
                this.updateFilters();
                this.showNotification(`Vendor "${formData.name}" saved successfully!`, 'success');
            }, 100);
            
        } catch (error) {
            console.error('❌ Error saving vendor:', error);
            alert('Error saving vendor. Please try again.');
        }
    }
    
    editVendor(vendorId) {
        const vendor = this.vendors.find(v => v.id === vendorId);
        if (vendor) {
            const modal = this.showVendorModal('edit', vendor);
            // Store vendor ID for editing
            setTimeout(() => {
                const modalElement = document.querySelector('.vendor-modal-overlay[data-modal="vendor"]');
                if (modalElement) {
                    modalElement.dataset.vendorId = vendorId;
                }
            }, 50);
        }
    }
    
    async deleteVendor(vendorId) {
        if (!confirm('Are you sure you want to delete this vendor?')) {
            return;
        }
        
        try {
            // Try to delete from backend API
            const response = await fetch(`/api/vendors/${vendorId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                console.log('✅ Vendor deleted from API');
            } else {
                console.log('⚠️ API not available, deleting locally');
            }
            
            // Remove from local array
            this.vendors = this.vendors.filter(v => v.id !== vendorId);
            this.selectedVendors.delete(vendorId);
            
            // Save to user file storage
            this.saveVendorsToFile();
            
            this.updateVendorCount();
            this.displayVendors();
            this.updateFilters();
            this.updateBulkActions();
            
            this.showNotification('Vendor deleted successfully!', 'success');
            
        } catch (error) {
            console.error('❌ Error deleting vendor:', error);
            alert('Error deleting vendor. Please try again.');
        }
    }
    
    closeVendorModal() {
        const modal = document.querySelector('.vendor-modal-overlay[data-modal="vendor"]');
        if (modal) {
            modal.style.opacity = '0';
            setTimeout(() => {
                modal.remove();
                console.log('✅ Vendor modal closed');
            }, 300);
        }
    }
    
    showImportModal() {
        const modal = this.createImportModal();
        if (modal) {
            document.body.appendChild(modal);
            
            setTimeout(() => {
                modal.style.opacity = '1';
            }, 10);
            
            console.log('✅ Import modal displayed');
        }
    }
    
    createImportModal() {
        const modal = document.createElement('div');
        modal.className = 'import-modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] opacity-0 transition-opacity duration-300';
        modal.setAttribute('data-modal', 'import');
        
        modal.innerHTML = `
            <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                <div class="p-6 border-b border-gray-200 bg-gradient-to-r from-green-50 to-emerald-50">
                    <h2 class="text-xl font-semibold text-gray-900">Import Vendors</h2>
                    <p class="text-sm text-gray-600 mt-1">Import vendors from Excel or CSV file</p>
                </div>
                
                <div class="p-6 space-y-6">
                    <!-- File Upload Section -->
                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                        <div class="text-4xl mb-4">📁</div>
                        <h3 class="text-lg font-medium text-gray-900 mb-2">Upload Your File</h3>
                        <p class="text-sm text-gray-600 mb-4">Drag and drop your Excel or CSV file here, or click to browse</p>
                        
                        <input type="file" id="vendor-file-input" accept=".csv,.xlsx,.xls" 
                               class="hidden" onchange="vendorManager.handleFileSelect(event)">
                        
                        <button onclick="document.getElementById('vendor-file-input').click()" 
                                class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg transition-colors font-medium">
                            📁 Choose File
                        </button>
                        
                        <p class="text-xs text-gray-500 mt-2">Supported formats: CSV, Excel (.xlsx, .xls)</p>
                    </div>
                    
                    <!-- Template Download -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-900 mb-2">📋 Import Template</h4>
                        <p class="text-sm text-gray-600 mb-3">Download our template to ensure your data is formatted correctly</p>
                        <button onclick="vendorManager.downloadTemplate()" 
                                class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors text-sm">
                            📥 Download Template
                        </button>
                    </div>
                    
                    <!-- Import Options -->
                    <div class="space-y-4">
                        <h4 class="font-medium text-gray-900">⚙️ Import Options</h4>
                        
                        <div class="flex items-center">
                            <input type="checkbox" id="import-overwrite" class="mr-2">
                            <label for="import-overwrite" class="text-sm text-gray-700">
                                Overwrite existing vendors (by name)
                            </label>
                        </div>
                        
                        <div class="flex items-center">
                            <input type="checkbox" id="import-skip-duplicates" class="mr-2" checked>
                            <label for="import-skip-duplicates" class="text-sm text-gray-700">
                                Skip duplicate vendors
                            </label>
                        </div>
                        
                        <div class="flex items-center">
                            <input type="checkbox" id="import-validate-email" class="mr-2">
                            <label for="import-validate-email" class="text-sm text-gray-700">
                                Validate email addresses
                            </label>
                        </div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="flex space-x-3 pt-4">
                        <button onclick="vendorManager.closeImportModal()" 
                                class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 px-4 py-2 rounded-lg transition-colors">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add drag and drop functionality
        const dropZone = modal.querySelector('.border-dashed');
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-blue-400', 'bg-blue-50');
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-blue-400', 'bg-blue-50');
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-blue-400', 'bg-blue-50');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.processFile(files[0]);
            }
        });
        
        return modal;
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }
    
    async processFile(file) {
        console.log('🔍 Processing file:', file.name);
        
        try {
            let csvContent = '';
            
            if (file.name.endsWith('.csv')) {
                // Process CSV directly
                csvContent = await file.text();
            } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
                // Convert Excel to CSV
                csvContent = await this.convertExcelToCSV(file);
            } else {
                throw new Error('Unsupported file format');
            }
            
            // Process the CSV content
            await this.processCSVContent(csvContent);
            
        } catch (error) {
            console.error('❌ Error processing file:', error);
            alert('Error processing file: ' + error.message);
        }
    }
    
    async convertExcelToCSV(file) {
        // For now, we'll use a simple approach
        // In a production environment, you'd want to use a library like SheetJS
        console.log('⚠️ Excel conversion not fully implemented - please use CSV format for now');
        throw new Error('Excel conversion requires additional setup. Please convert to CSV format.');
    }
    
    async processCSVContent(csvContent) {
        try {
            // Try to import via API
            const response = await fetch('/api/vendors/import-csv', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ csv_content: csvContent })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ Import successful:', result);
                
                // Reload vendors
                await this.loadVendors();
                
                this.showNotification(`Successfully imported ${result.imported_count} vendors!`, 'success');
                this.closeImportModal();
                
            } else {
                throw new Error('API import failed');
            }
            
        } catch (error) {
            console.log('⚠️ API import failed, processing locally:', error.message);
            
            // Fallback to local processing
            const importedVendors = this.parseCSVLocally(csvContent);
            this.vendors.push(...importedVendors);
            
            this.updateVendorCount();
            this.displayVendors();
            this.updateFilters();
            
            this.showNotification(`Successfully imported ${importedVendors.length} vendors locally!`, 'success');
            this.closeImportModal();
        }
    }
    
    parseCSVLocally(csvContent) {
        const lines = csvContent.split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        const vendors = [];
        
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;
            
            const values = line.split(',').map(v => v.trim());
            const vendor = {
                id: Date.now() + i,
                name: values[0] || '',
                company: values[1] || '',
                email: values[2] || '',
                phone: values[3] || '',
                mobile: values[4] || '',
                fax: values[5] || '',
                website: values[6] || '',
                street: values[7] || '',
                city: values[8] || '',
                state: values[9] || '',
                zip_code: values[10] || '',
                specialties: values[11] ? values[11].split(';').map(s => s.trim()) : [],
                notes: values[12] || '',
                is_active: true,
                created_at: new Date().toISOString()
            };
            
            if (vendor.name) {
                vendors.push(vendor);
            }
        }
        
        return vendors;
    }
    
    downloadTemplate() {
        const template = `Name,Company,Email,Phone,Mobile,Fax,Website,Street,City,State,ZIP,Specialties,Notes
John Smith,Fresh Foods Inc,john@freshfoods.com,555-1234,555-5678,,https://freshfoods.com,123 Main St,Boston,MA,02101,"produce;dairy",Reliable supplier
Sarah Johnson,Quality Meats Co,sarah@qualitymeats.com,555-2345,555-6789,,https://qualitymeats.com,456 Oak Ave,Chicago,IL,60601,"meat;poultry",Premium meat supplier`;
        
        const blob = new Blob([template], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vendor-import-template.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('✅ Template downloaded');
    }
    
    closeImportModal() {
        const modal = document.querySelector('.import-modal-overlay[data-modal="import"]');
        if (modal) {
            modal.style.opacity = '0';
            setTimeout(() => {
                modal.remove();
                console.log('✅ Import modal closed');
            }, 300);
        }
    }
    
    exportVendors() {
        if (this.vendors.length === 0) {
            alert('No vendors to export');
            return;
        }
        
        // Convert vendors to CSV
        const headers = ['Name', 'Company', 'Email', 'Phone', 'Mobile', 'Fax', 'Website', 'Street', 'City', 'State', 'ZIP', 'Specialties', 'Notes', 'Status'];
        const csvContent = [
            headers.join(','),
            ...this.vendors.map(vendor => [
                vendor.name,
                vendor.company || '',
                vendor.email || '',
                vendor.phone || '',
                vendor.mobile || '',
                vendor.fax || '',
                vendor.website || '',
                vendor.street || '',
                vendor.city || '',
                vendor.state || '',
                vendor.zip_code || '',
                (vendor.specialties || []).join(';'),
                vendor.notes || '',
                vendor.is_active ? 'Active' : 'Inactive'
            ].join(','))
        ].join('\n');
        
        // Download file
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `vendors-export-${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('✅ Vendors exported');
        this.showNotification('Vendors exported successfully!', 'success');
    }
    
    bulkDeleteVendors() {
        if (this.selectedVendors.size === 0) {
            alert('Please select vendors to delete');
            return;
        }
        
        if (!confirm(`Are you sure you want to delete ${this.selectedVendors.size} vendors?`)) {
            return;
        }
        
        // Delete selected vendors
        this.selectedVendors.forEach(vendorId => {
            this.deleteVendor(vendorId);
        });
        
        this.selectedVendors.clear();
        this.updateBulkActions();
    }
    
    bulkEditVendors() {
        if (this.selectedVendors.size === 0) {
            alert('Please select vendors to edit');
            return;
        }
        
        // For now, show a simple bulk edit modal
        // In a more sophisticated implementation, you'd allow editing common fields
        alert(`Bulk edit for ${this.selectedVendors.size} vendors - Feature coming soon!`);
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-[10000] transform transition-all duration-300 ${
            type === 'success' ? 'bg-green-500 text-white' : 
            type === 'error' ? 'bg-red-500 text-white' : 
            'bg-blue-500 text-white'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize vendor manager when DOM is loaded
let vendorManager;
document.addEventListener('DOMContentLoaded', function() {
    vendorManager = new VendorManager();
    window.vendorManager = vendorManager;
});
