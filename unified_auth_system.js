/**
 * Unified Authentication System for Iterum R&D Chef Notebook
 * Combines the best features of both authManager.js and profileManager.js
 * into one cohesive authentication flow
 */

class UnifiedAuthSystem {
    constructor() {
        this.currentUser = null;
        this.isOnline = false;
        this.savedUsers = JSON.parse(localStorage.getItem('saved_users')) || [];
        this.init();
    }

    /**
     * Initialize the authentication system
     */
    async init() {
        console.log('🔐 Initializing Unified Authentication System...');
        
        // Check backend connection
        await this.checkBackendConnection();
        
        // Load current user
        this.loadCurrentUser();
        
        if (this.currentUser) {
            // User is already logged in
            this.hideLoadingScreen();
            this.updateAuthUI(this.currentUser);
        } else {
            // Show authentication flow
            await this.showAuthFlow();
        }
    }

    /**
     * Check if backend is available
     */
    async checkBackendConnection() {
        try {
            const response = await fetch('http://localhost:8000/health', {
                method: 'GET',
                timeout: 3000
            });
            this.isOnline = response.ok;
            console.log(`🌐 Backend connection: ${this.isOnline ? 'Online' : 'Offline'}`);
        } catch (error) {
            this.isOnline = false;
            console.warn('⚠️ Backend not available, using offline mode');
        }
    }

    /**
     * Load current user from localStorage
     */
    loadCurrentUser() {
        const user = localStorage.getItem('current_user');
        this.currentUser = user ? JSON.parse(user) : null;
    }

    /**
     * Show the main authentication flow
     */
    async showAuthFlow() {
        // Load saved users if online
        if (this.isOnline) {
            await this.loadSavedUsers();
        }

        // Show the appropriate auth interface
        if (this.savedUsers.length > 0) {
            this.showUserSelection();
        } else {
            this.showLoginOptions();
        }
    }

    /**
     * Load saved users from backend
     */
    async loadSavedUsers() {
        try {
            const response = await fetch('http://localhost:8000/api/profiles/');
            if (response.ok) {
                this.savedUsers = await response.json();
            }
        } catch (error) {
            console.warn('Could not load saved users:', error);
            this.savedUsers = [];
        }
    }

    /**
     * Show user selection interface
     */
    showUserSelection() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (!loadingOverlay) return;

        loadingOverlay.innerHTML = `
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                <!-- Header -->
                <div class="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white text-center">
                    <div class="text-3xl mb-2">👨‍🍳</div>
                    <h2 class="text-2xl font-bold">Welcome Back</h2>
                    <p class="text-blue-100">Choose your profile to continue</p>
                </div>
                
                <!-- User Selection -->
                <div class="p-6">
                    <div id="saved-users-list" class="space-y-3 mb-6">
                        ${this.savedUsers.map(user => `
                            <div class="flex items-center justify-between bg-gray-50 rounded-lg p-3 border hover:bg-gray-100 transition-colors">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
                                        ${user.name.charAt(0).toUpperCase()}
                                    </div>
                                    <div>
                                        <div class="font-semibold text-gray-800">${user.name}</div>
                                        <div class="text-sm text-gray-600">${user.email || 'No email'}</div>
                                        ${user.role ? `<div class="text-xs text-gray-500">${user.role}</div>` : ''}
                                    </div>
                                </div>
                                <button onclick="unifiedAuth.selectUser('${user.id}')" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm">
                                    Select
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="space-y-3">
                        <button onclick="unifiedAuth.showLoginModal()" class="w-full bg-gray-100 text-gray-700 py-3 px-4 rounded-lg font-semibold hover:bg-gray-200 transition-all">
                            🔐 Sign In with Different Account
                        </button>
                        <button onclick="unifiedAuth.showCreateProfile()" class="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-600 transition-all">
                            ➕ Create New Profile
                        </button>
                        <button onclick="unifiedAuth.createOfflineProfile()" class="w-full bg-orange-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-orange-600 transition-all">
                            🚀 Continue Offline
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Show login options when no saved users
     */
    showLoginOptions() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (!loadingOverlay) return;

        loadingOverlay.innerHTML = `
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                <!-- Header -->
                <div class="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white text-center">
                    <div class="text-3xl mb-2">👨‍🍳</div>
                    <h2 class="text-2xl font-bold">Welcome to Iterum</h2>
                    <p class="text-blue-100">Your Culinary Research & Development Notebook</p>
                </div>
                
                <!-- Login Options -->
                <div class="p-6 space-y-4">
                    <button onclick="unifiedAuth.showLoginModal()" class="w-full bg-blue-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-600 transition-all">
                        🔐 Sign In
                    </button>
                    <button onclick="unifiedAuth.showCreateProfile()" class="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-600 transition-all">
                        ➕ Create Account
                    </button>
                    <button onclick="unifiedAuth.createOfflineProfile()" class="w-full bg-orange-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-orange-600 transition-all">
                        🚀 Continue Offline
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Show traditional login modal
     */
    showLoginModal() {
        const modal = document.getElementById('login-modal');
        if (modal) {
            modal.classList.remove('hidden');
            this.hideLoadingScreen();
        }
    }

    /**
     * Hide loading screen
     */
    hideLoadingScreen() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.opacity = '0';
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
            }, 500);
        }
    }

    /**
     * Select a saved user
     */
    async selectUser(userId) {
        try {
            let user;
            
            if (this.isOnline) {
                const response = await fetch(`http://localhost:8000/api/profiles/${userId}`);
                if (!response.ok) throw new Error('Failed to fetch user data');
                user = await response.json();
            } else {
                // Find user in saved users list
                user = this.savedUsers.find(u => u.id === userId);
                if (!user) throw new Error('User not found');
            }

            this.currentUser = user;
            localStorage.setItem('current_user', JSON.stringify(user));
            
            this.hideLoadingScreen();
            this.updateAuthUI(user);
            
            // Refresh user data manager
            if (window.userDataManager) {
                window.userDataManager.refreshUserData();
            }
            
        } catch (error) {
            console.error('Error selecting user:', error);
            alert('Failed to select user. Please try again.');
        }
    }

    /**
     * Create offline profile
     */
    async createOfflineProfile() {
        try {
            let user;
            
            if (this.isOnline) {
                const response = await fetch('http://localhost:8000/api/profiles/offline', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                if (!response.ok) throw new Error('Failed to create offline profile');
                const data = await response.json();
                user = data.user;
            } else {
                // Create local offline user
                user = {
                    id: 'offline_' + Date.now(),
                    name: 'Local User',
                    email: 'local@offline.com',
                    role: 'Chef',
                    restaurant: 'My Kitchen',
                    avatar: null,
                    isGoogleUser: false,
                    recipes: [],
                    ingredients: [],
                    equipment: [],
                    lastUpdated: new Date().toISOString()
                };
            }

            this.currentUser = user;
            localStorage.setItem('current_user', JSON.stringify(user));
            
            this.hideLoadingScreen();
            this.updateAuthUI(user);
            
            // Refresh user data manager
            if (window.userDataManager) {
                window.userDataManager.refreshUserData();
            }
            
        } catch (error) {
            console.error('Error creating offline profile:', error);
            alert('Failed to create offline profile. Please try again.');
        }
    }

    /**
     * Show create profile interface
     */
    showCreateProfile() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (!loadingOverlay) return;

        loadingOverlay.innerHTML = `
            <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                <!-- Header -->
                <div class="bg-gradient-to-r from-green-600 to-blue-600 p-6 text-white text-center">
                    <div class="text-3xl mb-2">➕</div>
                    <h2 class="text-2xl font-bold">Create Profile</h2>
                    <p class="text-green-100">Set up your culinary profile</p>
                </div>
                
                <!-- Create Profile Form -->
                <div class="p-6">
                    <form id="create-profile-form" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                            <input type="text" id="profile-name" name="name" required class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all" placeholder="Enter your full name">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                            <input type="email" id="profile-email" name="email" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all" placeholder="Enter your email (optional)">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Role</label>
                            <select id="profile-role" name="role" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all">
                                <option value="Chef">Chef</option>
                                <option value="Sous Chef">Sous Chef</option>
                                <option value="Line Cook">Line Cook</option>
                                <option value="Pastry Chef">Pastry Chef</option>
                                <option value="Kitchen Manager">Kitchen Manager</option>
                                <option value="Home Cook">Home Cook</option>
                                <option value="Food Enthusiast">Food Enthusiast</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Restaurant/Kitchen</label>
                            <input type="text" id="profile-restaurant" name="restaurant" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all" placeholder="Enter restaurant or kitchen name">
                        </div>
                        <div id="profile-error" class="hidden bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"></div>
                        <button type="submit" class="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-600 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all">
                            Create Profile
                        </button>
                    </form>
                    
                    <div class="mt-4 text-center">
                        <button onclick="unifiedAuth.showAuthFlow()" class="text-gray-600 hover:text-gray-800">
                            ← Back to options
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Add form submission handler
        const form = document.getElementById('create-profile-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleCreateProfile(e));
        }
    }

    /**
     * Handle create profile form submission
     */
    async handleCreateProfile(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const profileData = {
            name: formData.get('name'),
            email: formData.get('email') || '',
            role: formData.get('role'),
            restaurant: formData.get('restaurant') || 'My Kitchen'
        };

        try {
            let user;
            
            if (this.isOnline) {
                const response = await fetch('http://localhost:8000/api/profiles/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(profileData)
                });
                if (!response.ok) throw new Error('Failed to create profile');
                const data = await response.json();
                user = data.user;
            } else {
                // Create local profile
                user = {
                    id: 'local_' + Date.now(),
                    name: profileData.name,
                    email: profileData.email,
                    role: profileData.role,
                    restaurant: profileData.restaurant,
                    avatar: null,
                    isGoogleUser: false,
                    recipes: [],
                    ingredients: [],
                    equipment: [],
                    lastUpdated: new Date().toISOString()
                };
            }

            this.currentUser = user;
            localStorage.setItem('current_user', JSON.stringify(user));
            
            this.hideLoadingScreen();
            this.updateAuthUI(user);
            
            // Refresh user data manager
            if (window.userDataManager) {
                window.userDataManager.refreshUserData();
            }
            
        } catch (error) {
            console.error('Error creating profile:', error);
            const errorDiv = document.getElementById('profile-error');
            if (errorDiv) {
                errorDiv.textContent = 'Failed to create profile. Please try again.';
                errorDiv.classList.remove('hidden');
            }
        }
    }

    /**
     * Update authentication UI
     */
    updateAuthUI(user) {
        console.log('🔄 Updating auth UI for user:', user ? user.name : 'Guest');
        
        // Update user info display
        const userInfo = document.getElementById('user-info');
        const currentUserSpan = document.getElementById('current-user');
        const loginBtn = document.getElementById('login-btn');
        const logoutBtn = document.getElementById('logout-btn');
        
        // Update user display elements
        if (userInfo) userInfo.textContent = user && user.name ? user.name : 'Guest';
        if (currentUserSpan) currentUserSpan.textContent = user && user.name ? user.name : '';
        
        // Update button visibility
        if (loginBtn) loginBtn.style.display = user ? 'none' : 'inline-block';
        if (logoutBtn) logoutBtn.style.display = user ? 'inline-block' : 'none';
        
        // Update profile display in header
        const profileDisplay = document.getElementById('user-profile-display');
        if (profileDisplay) {
            profileDisplay.classList.remove('hidden');
        }
        
        // Update profile information
        const userName = document.getElementById('user-name');
        const userEmail = document.getElementById('user-email');
        const userRole = document.getElementById('user-role');
        const userRestaurant = document.getElementById('user-restaurant');
        const userAvatar = document.getElementById('user-avatar');
        
        if (userName) userName.textContent = user.name;
        if (userEmail) userEmail.textContent = user.email || '';
        if (userRole) userRole.textContent = user.role || '';
        if (userRestaurant) userRestaurant.textContent = user.restaurant || '';
        
        // Set avatar (use first letter of name)
        if (userAvatar) {
            userAvatar.src = user.photoURL || `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="%234285F4"/><text x="50" y="65" font-family="Arial" font-size="40" fill="white" text-anchor="middle">${user.name.charAt(0).toUpperCase()}</text></svg>`;
        }
    }

    /**
     * Handle user login
     */
    async handleLogin(loginData) {
        console.log('🔐 Handling login for:', loginData.email);
        
        try {
            let user;
            
            if (this.isOnline) {
                // Try backend authentication
                const response = await fetch('http://localhost:8000/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(loginData)
                });
                
                if (response.ok) {
                    const data = await response.json();
                    user = data.user;
                    
                    // Store auth token if provided
                    if (data.token) {
                        localStorage.setItem('iterum_auth_token', data.token);
                    }
                } else {
                    throw new Error('Invalid email or password');
                }
            } else {
                // Offline mode: check saved users
                const savedUser = this.savedUsers.find(u => 
                    u.email === loginData.email && u.password === loginData.password
                );
                
                if (!savedUser) {
                    throw new Error('User not found in offline mode');
                }
                
                user = savedUser;
            }
            
            // Set current user
            this.currentUser = user;
            localStorage.setItem('current_user', JSON.stringify(user));
            
            // Hide modal and update UI
            const loginModal = document.getElementById('login-modal');
            if (loginModal) loginModal.classList.add('hidden');
            
            this.hideLoadingScreen();
            this.updateAuthUI(user);
            
            // Refresh user data manager
            if (window.userDataManager) {
                window.userDataManager.refreshUserData();
            }
            
            console.log('✅ Login successful for:', user.name);
            
        } catch (error) {
            console.error('❌ Login error:', error);
            throw error; // Re-throw to be handled by the form
        }
    }

    /**
     * Handle user signup
     */
    async handleSignup(signupData) {
        console.log('🔐 Handling signup for:', signupData.email);
        
        try {
            let user;
            
            if (this.isOnline) {
                // Try backend user creation
                const response = await fetch('http://localhost:8000/api/auth/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(signupData)
                });
                
                if (response.ok) {
                    const data = await response.json();
                    user = data.user;
                    
                    // Store auth token if provided
                    if (data.token) {
                        localStorage.setItem('iterum_auth_token', data.token);
                    }
                } else if (response.status === 409) {
                    throw new Error('An account with this email already exists');
                } else {
                    throw new Error('Failed to create account. Please try again.');
                }
            } else {
                // Offline mode: create user locally
                user = {
                    id: 'user_' + Date.now(),
                    name: signupData.name,
                    email: signupData.email,
                    role: signupData.role,
                    restaurant: signupData.restaurant || 'My Kitchen',
                    password: signupData.password, // Store for offline auth
                    avatar: null,
                    isGoogleUser: false,
                    recipes: [],
                    ingredients: [],
                    equipment: [],
                    createdAt: new Date().toISOString(),
                    lastUpdated: new Date().toISOString()
                };
                
                // Add to saved users
                this.savedUsers.push(user);
                localStorage.setItem('saved_users', JSON.stringify(this.savedUsers));
            }
            
            // Set current user
            this.currentUser = user;
            localStorage.setItem('current_user', JSON.stringify(user));
            
            // Hide modal and update UI
            const loginModal = document.getElementById('login-modal');
            if (loginModal) loginModal.classList.add('hidden');
            
            this.hideLoadingScreen();
            this.updateAuthUI(user);
            
            // Refresh user data manager
            if (window.userDataManager) {
                window.userDataManager.refreshUserData();
            }
            
            console.log('✅ Signup successful for:', user.name);
            
        } catch (error) {
            console.error('❌ Signup error:', error);
            throw error; // Re-throw to be handled by the form
        }
    }

    /**
     * Handle logout
     */
    handleLogout() {
        console.log('🔐 Handling logout...');
        
        // Clear current user
        this.currentUser = null;
        
        // Clear all authentication data
        localStorage.removeItem('current_user');
        localStorage.removeItem('currentLocalProfile');
        localStorage.removeItem('iterum_auth_token');
        localStorage.removeItem('access_token');
        
        // Clear any profile-specific data
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
          if (key.startsWith('equipment_') || key.startsWith('profile_') || key.includes('user')) {
            localStorage.removeItem(key);
          }
        });
        
        // Sign out from Firebase if available
        if (window.firebaseAuth && window.firebaseAuth.currentUser) {
            window.firebaseAuth.signOut().catch(console.warn);
        }
        
        // Show loading overlay and auth flow
        this.showLoadingOverlay();
        
        // Show auth flow again
        setTimeout(() => {
            this.showAuthFlow();
        }, 100);
    }

    /**
     * Show loading overlay for auth
     */
    showLoadingOverlay() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
            loadingOverlay.style.opacity = '1';
        }
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * Check if user is logged in
     */
    isLoggedIn() {
        return !!this.currentUser;
    }
}

// Initialize unified auth system
const unifiedAuth = new UnifiedAuthSystem();

// Make it globally available
window.unifiedAuth = unifiedAuth;

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UnifiedAuthSystem;
} 