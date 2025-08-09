/**
 * Profile Manager - User profile and settings management
 * Handles user profile data, preferences, and settings
 */

class ProfileManager {
    constructor() {
        this.currentProfile = null;
        this.profiles = [];
        this.apiBase = 'http://localhost:8000/api';
        this.init();
    }

    /**
     * Initialize profile manager
     */
    init() {
        this.loadProfiles();
        this.setupEventListeners();
        console.log('📋 Profile Manager initialized');
    }

    /**
     * Load user profiles
     */
    async loadProfiles() {
        try {
            const response = await fetch(`${this.apiBase}/profiles/`, {
                headers: this.getAuthHeaders()
            });

            if (response.ok) {
                this.profiles = await response.json();
                console.log(`📋 Loaded ${this.profiles.length} profiles`);
            } else {
                console.warn('⚠️ Failed to load profiles from API, using local storage');
                this.loadProfilesFromStorage();
            }
        } catch (error) {
            console.warn('⚠️ Profile API unavailable, using local storage');
            this.loadProfilesFromStorage();
        }

        this.displayProfiles();
    }

    /**
     * Load profiles from local storage
     */
    loadProfilesFromStorage() {
        const stored = localStorage.getItem('user_profiles');
        this.profiles = stored ? JSON.parse(stored) : [];
    }

    /**
     * Save profiles to local storage
     */
    saveProfilesToStorage() {
        localStorage.setItem('user_profiles', JSON.stringify(this.profiles));
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Profile creation button
        const createProfileBtn = document.getElementById('create-profile-btn');
        if (createProfileBtn) {
            createProfileBtn.addEventListener('click', () => this.showCreateProfileModal());
        }

        // Profile management buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="edit-profile"]')) {
                const profileId = e.target.dataset.profileId;
                this.editProfile(profileId);
            }
            if (e.target.matches('[data-action="delete-profile"]')) {
                const profileId = e.target.dataset.profileId;
                this.confirmDeleteProfile(profileId);
            }
            if (e.target.matches('[data-action="switch-profile"]')) {
                const profileId = e.target.dataset.profileId;
                this.switchProfile(profileId);
            }
        });
    }

    /**
     * Display profiles in UI
     */
    displayProfiles() {
        const profileContainer = document.getElementById('profile-list');
        if (!profileContainer) return;

        if (this.profiles.length === 0) {
            profileContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">👤</div>
                    <h3>No Profiles Yet</h3>
                    <p>Create your first user profile to get started</p>
                    <button class="btn btn-primary" onclick="window.profileManager.showCreateProfileModal()">
                        Create Profile
                    </button>
                </div>
            `;
            return;
        }

        profileContainer.innerHTML = this.profiles.map(profile => `
            <div class="profile-card" data-profile-id="${profile.id}">
                <div class="profile-header">
                    <div class="profile-info">
                        <h3 class="profile-name">${profile.name}</h3>
                        <div class="profile-meta">
                            <span class="profile-role">${profile.role || 'Chef'}</span>
                            <span class="profile-status ${profile.is_active ? 'active' : 'inactive'}">
                                ${profile.is_active ? 'Active' : 'Inactive'}
                            </span>
                        </div>
                    </div>
                    <div class="profile-actions">
                        <button class="btn-icon" data-action="edit-profile" data-profile-id="${profile.id}" title="Edit">
                            ✏️
                        </button>
                        <button class="btn-icon" data-action="switch-profile" data-profile-id="${profile.id}" title="Switch">
                            🔄
                        </button>
                        <button class="btn-icon btn-danger" data-action="delete-profile" data-profile-id="${profile.id}" title="Delete">
                            🗑️
                        </button>
                    </div>
                </div>
                <div class="profile-content">
                    <p class="profile-description">${profile.description || 'No description'}</p>
                    <div class="profile-stats">
                        <span>${profile.experience_years || 0} years experience</span>
                        <span>${profile.specialties?.length || 0} specialties</span>
                        <span>Updated ${this.formatDate(profile.updated_at)}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Show create profile modal
     */
    showCreateProfileModal() {
        const modal = this.createProfileModal();
        document.body.appendChild(modal);
        
        setTimeout(() => {
            const nameInput = modal.querySelector('#profile-name');
            if (nameInput) nameInput.focus();
        }, 100);
    }

    /**
     * Create profile modal HTML
     */
    createProfileModal(profile = null) {
        const isEdit = !!profile;
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = isEdit ? 'edit-profile-modal' : 'create-profile-modal';

        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${isEdit ? 'Edit Profile' : 'Create New Profile'}</h2>
                    <button class="modal-close" onclick="this.closest('.modal-overlay').remove()">×</button>
                </div>
                
                <div class="modal-body">
                    <form id="profile-form">
                        <div class="form-group">
                            <label for="profile-name">Profile Name *</label>
                            <input type="text" id="profile-name" name="name" required 
                                   value="${profile?.name || ''}" placeholder="Chef John, Sous Chef Sarah, etc.">
                        </div>
                        
                        <div class="form-group">
                            <label for="profile-role">Role</label>
                            <select id="profile-role" name="role">
                                <option value="Chef" ${profile?.role === 'Chef' ? 'selected' : ''}>Chef</option>
                                <option value="Sous Chef" ${profile?.role === 'Sous Chef' ? 'selected' : ''}>Sous Chef</option>
                                <option value="Line Cook" ${profile?.role === 'Line Cook' ? 'selected' : ''}>Line Cook</option>
                                <option value="Pastry Chef" ${profile?.role === 'Pastry Chef' ? 'selected' : ''}>Pastry Chef</option>
                                <option value="Kitchen Manager" ${profile?.role === 'Kitchen Manager' ? 'selected' : ''}>Kitchen Manager</option>
                                <option value="Culinary Student" ${profile?.role === 'Culinary Student' ? 'selected' : ''}>Culinary Student</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="profile-description">Description</label>
                            <textarea id="profile-description" name="description" rows="3" 
                                      placeholder="Brief description of this profile...">${profile?.description || ''}</textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="profile-experience">Years of Experience</label>
                            <input type="number" id="profile-experience" name="experience_years" 
                                   value="${profile?.experience_years || 0}" min="0" max="50">
                        </div>
                        
                        <div class="form-group">
                            <label for="profile-specialties">Specialties (comma-separated)</label>
                            <input type="text" id="profile-specialties" name="specialties" 
                                   value="${profile?.specialties?.join(', ') || ''}" 
                                   placeholder="Italian, French, Pastry, etc.">
                        </div>
                        
                        <div class="form-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="profile-active" name="is_active" 
                                       ${profile?.is_active !== false ? 'checked' : ''}>
                                <span class="checkmark"></span>
                                Active profile
                            </label>
                        </div>
                    </form>
                </div>
                
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">
                        Cancel
                    </button>
                    <button type="button" class="btn btn-primary" 
                            onclick="window.profileManager.${isEdit ? 'saveProfileEdit' : 'saveNewProfile'}('${profile?.id || ''}')">
                        ${isEdit ? 'Save Changes' : 'Create Profile'}
                    </button>
                </div>
            </div>
        `;

        return modal;
    }

    /**
     * Create new profile
     */
    async createProfile(profileData) {
        const profile = {
            id: Date.now().toString(),
            name: profileData.name,
            role: profileData.role || 'Chef',
            description: profileData.description || '',
            experience_years: profileData.experience_years || 0,
            specialties: profileData.specialties ? profileData.specialties.split(',').map(s => s.trim()).filter(s => s) : [],
            is_active: profileData.is_active !== false,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        };

        try {
            const response = await fetch(`${this.apiBase}/profiles/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeaders()
                },
                body: JSON.stringify(profile)
            });

            if (response.ok) {
                const savedProfile = await response.json();
                this.profiles.push(savedProfile);
                this.displayProfiles();
                return savedProfile;
            } else {
                throw new Error('Failed to save profile to server');
            }
        } catch (error) {
            console.warn('⚠️ Saving profile locally due to API error:', error);
            this.profiles.push(profile);
            this.saveProfilesToStorage();
            this.displayProfiles();
            return profile;
        }
    }

    /**
     * Save new profile
     */
    async saveNewProfile() {
        const form = document.getElementById('profile-form');
        if (!form) return;

        const formData = new FormData(form);
        const profileData = {
            name: formData.get('name').trim(),
            role: formData.get('role'),
            description: formData.get('description').trim(),
            experience_years: parseInt(formData.get('experience_years')) || 0,
            specialties: formData.get('specialties'),
            is_active: formData.has('is_active')
        };

        if (!profileData.name) {
            alert('Please enter a profile name');
            return;
        }

        try {
            await this.createProfile(profileData);
            document.getElementById('create-profile-modal')?.remove();
            this.showNotification(`Profile "${profileData.name}" created successfully!`, 'success');
        } catch (error) {
            console.error('Error creating profile:', error);
            alert(`Failed to create profile: ${error.message}`);
        }
    }

    /**
     * Edit profile
     */
    editProfile(profileId) {
        const profile = this.profiles.find(p => p.id === profileId);
        if (!profile) return;

        const modal = this.createProfileModal(profile);
        document.body.appendChild(modal);
    }

    /**
     * Save profile edits
     */
    async saveProfileEdit(profileId) {
        const form = document.getElementById('profile-form');
        if (!form) return;

        const formData = new FormData(form);
        const updates = {
            name: formData.get('name').trim(),
            role: formData.get('role'),
            description: formData.get('description').trim(),
            experience_years: parseInt(formData.get('experience_years')) || 0,
            specialties: formData.get('specialties'),
            is_active: formData.has('is_active')
        };

        if (!updates.name) {
            alert('Please enter a profile name');
            return;
        }

        try {
            await this.updateProfile(profileId, updates);
            document.getElementById('edit-profile-modal')?.remove();
            this.showNotification(`Profile "${updates.name}" updated successfully!`, 'success');
        } catch (error) {
            console.error('Error updating profile:', error);
            alert(`Failed to update profile: ${error.message}`);
        }
    }

    /**
     * Update profile
     */
    async updateProfile(profileId, updates) {
        const profileIndex = this.profiles.findIndex(p => p.id === profileId);
        if (profileIndex === -1) {
            throw new Error('Profile not found');
        }

        const updatedProfile = {
            ...this.profiles[profileIndex],
            ...updates,
            specialties: updates.specialties ? updates.specialties.split(',').map(s => s.trim()).filter(s => s) : [],
            updated_at: new Date().toISOString()
        };

        try {
            const response = await fetch(`${this.apiBase}/profiles/${profileId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeaders()
                },
                body: JSON.stringify(updatedProfile)
            });

            if (response.ok) {
                const savedProfile = await response.json();
                this.profiles[profileIndex] = savedProfile;
                this.displayProfiles();
                return savedProfile;
            } else {
                throw new Error('Failed to update profile on server');
            }
        } catch (error) {
            console.warn('⚠️ Updating profile locally due to API error:', error);
            this.profiles[profileIndex] = updatedProfile;
            this.saveProfilesToStorage();
            this.displayProfiles();
            return updatedProfile;
        }
    }

    /**
     * Switch to profile
     */
    async switchProfile(profileId) {
        const profile = this.profiles.find(p => p.id === profileId);
        if (!profile) return;

        try {
            // Update current profile
            this.currentProfile = profile;
            
            // Update UI to show current profile
            this.updateCurrentProfileDisplay();
            
            // Save to localStorage
            localStorage.setItem('current_profile', JSON.stringify(profile));
            
            this.showNotification(`Switched to profile: ${profile.name}`, 'success');
            
            // Trigger profile change event
            document.dispatchEvent(new CustomEvent('profileChanged', {
                detail: { profile }
            }));
            
        } catch (error) {
            console.error('Error switching profile:', error);
            this.showNotification(`Failed to switch profile: ${error.message}`, 'error');
        }
    }

    /**
     * Update current profile display
     */
    updateCurrentProfileDisplay() {
        if (!this.currentProfile) return;

        // Update user info in header
        const userInitial = document.getElementById('user-avatar-initial');
        const currentUser = document.getElementById('current-user');
        
        if (userInitial) {
            userInitial.textContent = this.currentProfile.name.charAt(0).toUpperCase();
        }
        
        if (currentUser) {
            currentUser.textContent = this.currentProfile.name;
        }
    }

    /**
     * Confirm delete profile
     */
    confirmDeleteProfile(profileId) {
        const profile = this.profiles.find(p => p.id === profileId);
        if (!profile) return;

        if (confirm(`Are you sure you want to delete the profile "${profile.name}"? This action cannot be undone.`)) {
            this.deleteProfile(profileId);
        }
    }

    /**
     * Delete profile
     */
    async deleteProfile(profileId) {
        const profileIndex = this.profiles.findIndex(p => p.id === profileId);
        if (profileIndex === -1) {
            throw new Error('Profile not found');
        }

        try {
            const response = await fetch(`${this.apiBase}/profiles/${profileId}`, {
                method: 'DELETE',
                headers: this.getAuthHeaders()
            });

            if (response.ok) {
                this.profiles.splice(profileIndex, 1);
                this.displayProfiles();
                return true;
            } else {
                throw new Error('Failed to delete profile from server');
            }
        } catch (error) {
            console.warn('⚠️ Deleting profile locally due to API error:', error);
            this.profiles.splice(profileIndex, 1);
            this.saveProfilesToStorage();
            this.displayProfiles();
            return true;
        }
    }

    /**
     * Get current profile
     */
    getCurrentProfile() {
        return this.currentProfile;
    }

    /**
     * Helper: Format date
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 1) return 'today';
        if (diffDays <= 7) return `${diffDays} days ago`;
        return date.toLocaleDateString();
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
        if (window.showNotification) {
            window.showNotification(message, type);
            return;
        }

        console.log(`${type.toUpperCase()}: ${message}`);
    }
}

// Initialize profile manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.profileManager = new ProfileManager();
    });
} else {
    window.profileManager = new ProfileManager();
} 