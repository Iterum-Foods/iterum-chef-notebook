/**
 * AuthManager - Centralized Authentication System
 * Handles all authentication logic, state management, and persistence
 * Eliminates timing issues and provides bulletproof auth flow
 */

class AuthManager {
    constructor() {
        this.initialized = false;
        this.currentUser = null;
        this.isAuthenticated = false;
        this.listeners = [];
        this.debugMode = true; // Set to false in production
        this.backendUser = null; // Backend user data
        this.firebaseToken = null; // Firebase ID token
        
        // Backend API URL
        this.API_BASE_URL = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://your-backend-url.com'; // Update with your production URL
        
        // State keys
        this.STORAGE_KEYS = {
            CURRENT_USER: 'current_user',
            SESSION_ACTIVE: 'session_active',
            LAST_LOGIN: 'last_login',
            SAVED_USERS: 'saved_users',
            AUTH_STATE: 'auth_state',
            BACKEND_USER: 'backend_user_id',
            FIREBASE_TOKEN: 'firebase_token'
        };
        
        // Initialize immediately
        this.init();
    }
    
    /**
     * Initialize the auth system
     */
    async init() {
        this.log('🔐 AuthManager initializing...');
        
        try {
            // Load current session
            await this.loadSession();
            
            // Set up storage event listener for cross-tab sync
            window.addEventListener('storage', (e) => this.handleStorageChange(e));
            
            // Set up beforeunload to ensure data is saved
            window.addEventListener('beforeunload', () => this.saveState());
            
            this.initialized = true;
            this.log('✅ AuthManager initialized');
            this.notifyListeners('initialized');
            
        } catch (error) {
            this.error('❌ AuthManager initialization failed:', error);
        }
    }
    
    /**
     * Load session from localStorage
     */
    async loadSession() {
        this.log('📂 Loading session from localStorage...');
        
        try {
            const sessionActive = localStorage.getItem(this.STORAGE_KEYS.SESSION_ACTIVE);
            const userJson = localStorage.getItem(this.STORAGE_KEYS.CURRENT_USER);
            
            if (sessionActive === 'true' && userJson) {
                const user = JSON.parse(userJson);
                this.currentUser = user;
                this.isAuthenticated = true;
                window.currentUser = user; // Global access
                
                this.log('✅ Session loaded:', user.email);
                this.notifyListeners('session_loaded', user);
                return true;
            } else {
                this.log('ℹ️ No active session found');
                this.isAuthenticated = false;
                return false;
            }
        } catch (error) {
            this.error('❌ Error loading session:', error);
            this.clearSession();
            return false;
        }
    }
    
    /**
     * Sign in with email and password
     */
    async signInWithEmail(email, password) {
        this.log('🔐 Signing in with email:', email);
        
        try {
            // Wait for Firebase Auth to be ready
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            // Sign in with Firebase
            const firebaseUser = await firebaseAuth.signInWithEmail(email, password);
            
            if (!firebaseUser) {
                throw new Error('Firebase authentication failed');
            }
            
            this.log('✅ Firebase authentication successful');
            
            // Get Firebase ID token
            const idToken = await firebaseUser.getIdToken();
            this.firebaseToken = idToken;
            localStorage.setItem(this.STORAGE_KEYS.FIREBASE_TOKEN, idToken);
            
            // Create user profile
            const user = {
                id: firebaseUser.uid,
                userId: firebaseUser.uid,
                name: firebaseUser.displayName || email.split('@')[0],
                email: firebaseUser.email || email,
                type: 'email',
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            };
            
            // Sync with backend
            await this.syncWithBackend(user, idToken);
            
            // Save session
            await this.saveSession(user);
            
            this.log('✅ Sign-in complete');
            return user;
            
        } catch (error) {
            this.error('❌ Sign-in failed:', error);
            throw error;
        }
    }
    
    /**
     * Sign up with email and password
     */
    async signUpWithEmail(name, email, password) {
        this.log('📝 Signing up with email:', email);
        
        try {
            // Wait for Firebase Auth to be ready
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            // Create account with Firebase
            const firebaseUser = await firebaseAuth.createUserWithEmail(email, password, name);
            
            if (!firebaseUser) {
                throw new Error('Firebase account creation failed');
            }
            
            this.log('✅ Firebase account created successfully');
            
            // Send email verification
            try {
                await firebaseUser.sendEmailVerification();
                this.log('✅ Verification email sent to:', email);
            } catch (verifyError) {
                this.log('⚠️ Could not send verification email:', verifyError.message);
                // Don't fail signup if verification email fails
            }
            
            // Get Firebase ID token
            const idToken = await firebaseUser.getIdToken();
            this.firebaseToken = idToken;
            localStorage.setItem(this.STORAGE_KEYS.FIREBASE_TOKEN, idToken);
            
            // Create user profile
            const user = {
                id: firebaseUser.uid,
                userId: firebaseUser.uid,
                name: name,
                email: firebaseUser.email,
                type: 'email',
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            };
            
            // Sync with backend
            await this.syncWithBackend(user, idToken);
            
            // Save session
            await this.saveSession(user);
            
            this.log('✅ Sign-up complete');
            return user;
            
        } catch (error) {
            this.error('❌ Sign-up failed:', error);
            throw error;
        }
    }
    
    /**
     * Sign in with Google
     */
    async signInWithGoogle() {
        this.log('🔵 Signing in with Google...');
        
        try {
            // Wait for Firebase Auth to be ready
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            // Sign in with Google
            const result = await firebaseAuth.signInWithGoogle();
            
            if (!result || !result.user) {
                throw new Error('Google sign-in failed');
            }
            
            this.log('✅ Google authentication successful');
            
            // Get Firebase ID token
            const idToken = await result.user.getIdToken();
            this.firebaseToken = idToken;
            localStorage.setItem(this.STORAGE_KEYS.FIREBASE_TOKEN, idToken);
            
            // Create user profile
            const user = {
                id: result.user.uid,
                userId: result.user.uid,
                name: result.user.displayName || result.user.email.split('@')[0],
                email: result.user.email,
                photoURL: result.user.photoURL,
                type: 'google',
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            };
            
            // Sync with backend
            await this.syncWithBackend(user, idToken);
            
            // Save session
            await this.saveSession(user);
            
            this.log('✅ Google sign-in complete');
            return user;
            
        } catch (error) {
            this.error('❌ Google sign-in failed:', error);
            throw error;
        }
    }
    
    /**
     * Send email verification
     */
    async sendEmailVerification() {
        this.log('📧 Sending email verification...');
        
        try {
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            if (!firebaseAuth.currentUser) {
                throw new Error('No user logged in');
            }
            
            await firebaseAuth.currentUser.sendEmailVerification();
            this.log('✅ Email verification sent');
            return true;
            
        } catch (error) {
            this.error('❌ Failed to send verification email:', error);
            throw error;
        }
    }
    
    /**
     * Send password reset email
     */
    async sendPasswordResetEmail(email) {
        this.log('🔑 Sending password reset email to:', email);
        
        try {
            const firebaseAuth = await this.waitForFirebaseAuth();
            await firebaseAuth.sendPasswordResetEmail(email);
            this.log('✅ Password reset email sent');
            return true;
            
        } catch (error) {
            this.error('❌ Failed to send password reset email:', error);
            throw error;
        }
    }
    
    /**
     * Update user profile
     */
    async updateProfile(updates) {
        this.log('📝 Updating user profile...');
        
        try {
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            if (!firebaseAuth.currentUser) {
                throw new Error('No user logged in');
            }
            
            // Update Firebase profile
            if (updates.displayName || updates.photoURL) {
                await firebaseAuth.currentUser.updateProfile({
                    displayName: updates.displayName,
                    photoURL: updates.photoURL
                });
                this.log('✅ Firebase profile updated');
            }
            
            // Update local user data
            if (this.currentUser) {
                if (updates.displayName) {
                    this.currentUser.name = updates.displayName;
                }
                if (updates.photoURL) {
                    this.currentUser.photoURL = updates.photoURL;
                }
                
                // Save updated session
                await this.saveSession(this.currentUser);
            }
            
            // Sync to backend
            const idToken = await firebaseAuth.currentUser.getIdToken();
            await this.syncWithBackend(this.currentUser, idToken);
            
            this.log('✅ Profile updated successfully');
            this.notifyListeners('profile_updated', this.currentUser);
            
            return this.currentUser;
            
        } catch (error) {
            this.error('❌ Profile update failed:', error);
            throw error;
        }
    }
    
    /**
     * Update email address
     */
    async updateEmail(newEmail, password) {
        this.log('📧 Updating email to:', newEmail);
        
        try {
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            if (!firebaseAuth.currentUser) {
                throw new Error('No user logged in');
            }
            
            // Re-authenticate first (required by Firebase)
            const currentEmail = firebaseAuth.currentUser.email;
            await firebaseAuth.signInWithEmail(currentEmail, password);
            
            // Update email
            await firebaseAuth.currentUser.updateEmail(newEmail);
            
            // Send verification to new email
            await firebaseAuth.currentUser.sendEmailVerification();
            
            // Update local data
            if (this.currentUser) {
                this.currentUser.email = newEmail;
                await this.saveSession(this.currentUser);
            }
            
            // Sync to backend
            const idToken = await firebaseAuth.currentUser.getIdToken();
            await this.syncWithBackend(this.currentUser, idToken);
            
            this.log('✅ Email updated successfully');
            this.notifyListeners('email_updated', newEmail);
            
            return true;
            
        } catch (error) {
            this.error('❌ Email update failed:', error);
            throw error;
        }
    }
    
    /**
     * Update password
     */
    async updatePassword(currentPassword, newPassword) {
        this.log('🔑 Updating password...');
        
        try {
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            if (!firebaseAuth.currentUser) {
                throw new Error('No user logged in');
            }
            
            // Re-authenticate first (required by Firebase)
            const email = firebaseAuth.currentUser.email;
            await firebaseAuth.signInWithEmail(email, currentPassword);
            
            // Update password
            await firebaseAuth.currentUser.updatePassword(newPassword);
            
            this.log('✅ Password updated successfully');
            this.notifyListeners('password_updated');
            
            return true;
            
        } catch (error) {
            this.error('❌ Password update failed:', error);
            throw error;
        }
    }
    
    /**
     * Delete account
     */
    async deleteAccount(password) {
        this.log('🗑️ Deleting account...');
        
        try {
            const firebaseAuth = await this.waitForFirebaseAuth();
            
            if (!firebaseAuth.currentUser) {
                throw new Error('No user logged in');
            }
            
            // Re-authenticate first (required by Firebase)
            const email = firebaseAuth.currentUser.email;
            await firebaseAuth.signInWithEmail(email, password);
            
            // Delete from Firebase
            await firebaseAuth.currentUser.delete();
            
            // Clear local session
            this.clearSession();
            
            this.log('✅ Account deleted successfully');
            this.notifyListeners('account_deleted');
            
            return true;
            
        } catch (error) {
            this.error('❌ Account deletion failed:', error);
            throw error;
        }
    }
    
    /**
     * Create trial account
     */
    async createTrialAccount(userData) {
        this.log('🎁 Creating trial account:', userData.email);
        
        try {
            // Calculate trial end date
            const trialEndDate = new Date();
            trialEndDate.setDate(trialEndDate.getDate() + 14);
            
            // Create trial user profile
            const user = {
                id: 'trial_' + Date.now(),
                userId: 'trial_' + Date.now(),
                name: userData.name,
                email: userData.email,
                company: userData.company || null,
                role: userData.role || null,
                source: userData.source || null,
                type: 'trial',
                trialStartDate: new Date().toISOString(),
                trialEndDate: trialEndDate.toISOString(),
                trialDaysRemaining: 14,
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString()
            };
            
            // Save session
            await this.saveSession(user);
            
            // Track trial users
            this.trackTrialUser(userData);
            
            this.log('✅ Trial account created');
            return user;
            
        } catch (error) {
            this.error('❌ Trial account creation failed:', error);
            throw error;
        }
    }
    
    /**
     * Sync user with backend database
     */
    async syncWithBackend(user, idToken) {
        this.log('🔄 Syncing user with backend...');
        
        try {
            const response = await fetch(`${this.API_BASE_URL}/api/firebase/sync-user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    firebase_uid: user.id,
                    email: user.email,
                    name: user.name,
                    photo_url: user.photoURL || null,
                    provider: user.type,
                    id_token: idToken
                })
            });
            
            if (!response.ok) {
                throw new Error(`Backend sync failed: ${response.statusText}`);
            }
            
            const backendUser = await response.json();
            this.backendUser = backendUser;
            localStorage.setItem(this.STORAGE_KEYS.BACKEND_USER, JSON.stringify(backendUser));
            
            this.log('✅ User synced with backend:', backendUser.message);
            this.log('   Backend user ID:', backendUser.id);
            
            return backendUser;
            
        } catch (error) {
            // Log error but don't fail - user can still use app without backend sync
            this.log('⚠️ Backend sync failed (non-critical):', error.message);
            this.log('   User can still use app with local data');
            return null;
        }
    }
    
    /**
     * Save session to localStorage with verification
     */
    async saveSession(user) {
        this.log('💾 Saving session for:', user.email);
        
        try {
            // Update instance state
            this.currentUser = user;
            this.isAuthenticated = true;
            window.currentUser = user;
            
            // Save to localStorage
            localStorage.setItem(this.STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
            localStorage.setItem(this.STORAGE_KEYS.SESSION_ACTIVE, 'true');
            localStorage.setItem(this.STORAGE_KEYS.LAST_LOGIN, new Date().toISOString());
            
            // Force a small delay to ensure write completes
            await this.sleep(50);
            
            // Verify the save
            const verified = await this.verifySessionSaved();
            
            if (!verified) {
                throw new Error('Session save verification failed');
            }
            
            // Save to user profiles
            await this.saveToProfiles(user);
            
            // Save to Firestore (cloud backup - don't wait)
            this.saveToFirestore(user).catch(e => this.log('⚠️ Firestore save failed (non-critical):', e));
            
            // Notify listeners
            this.notifyListeners('session_saved', user);
            
            this.log('✅ Session saved and verified');
            return true;
            
        } catch (error) {
            this.error('❌ Session save failed:', error);
            throw error;
        }
    }
    
    /**
     * Verify that session was saved correctly
     */
    async verifySessionSaved() {
        this.log('🔍 Verifying session save...');
        
        const sessionActive = localStorage.getItem(this.STORAGE_KEYS.SESSION_ACTIVE);
        const userJson = localStorage.getItem(this.STORAGE_KEYS.CURRENT_USER);
        
        if (sessionActive !== 'true') {
            this.error('❌ Verification failed: session_active not set');
            return false;
        }
        
        if (!userJson) {
            this.error('❌ Verification failed: current_user not set');
            return false;
        }
        
        try {
            const user = JSON.parse(userJson);
            if (!user.email || !user.id) {
                this.error('❌ Verification failed: invalid user data');
                return false;
            }
            
            this.log('✅ Session verified:', user.email);
            return true;
            
        } catch (e) {
            this.error('❌ Verification failed: invalid JSON');
            return false;
        }
    }
    
    /**
     * Clear session
     */
    clearSession() {
        this.log('🗑️ Clearing session...');
        
        this.currentUser = null;
        this.isAuthenticated = false;
        window.currentUser = null;
        
        localStorage.removeItem(this.STORAGE_KEYS.CURRENT_USER);
        localStorage.removeItem(this.STORAGE_KEYS.SESSION_ACTIVE);
        
        this.notifyListeners('session_cleared');
        this.log('✅ Session cleared');
    }
    
    /**
     * Sign out
     */
    async signOut() {
        this.log('👋 Signing out...');
        
        try {
            // Sign out from Firebase if available
            if (window.firebaseAuth && window.firebaseAuth.isInitialized) {
                await window.firebaseAuth.signOut();
            }
            
            // Clear local session
            this.clearSession();
            
            this.notifyListeners('signed_out');
            this.log('✅ Signed out successfully');
            
            return true;
            
        } catch (error) {
            this.error('❌ Sign out error:', error);
            // Clear session anyway
            this.clearSession();
            throw error;
        }
    }
    
    /**
     * Check if user is authenticated
     */
    async checkAuth() {
        this.log('🔍 Checking authentication...');
        
        // If we already have state, return it
        if (this.isAuthenticated && this.currentUser) {
            this.log('✅ Already authenticated:', this.currentUser.email);
            return { authenticated: true, user: this.currentUser };
        }
        
        // Try to load session
        const loaded = await this.loadSession();
        
        if (loaded) {
            this.log('✅ Authentication check passed');
            return { authenticated: true, user: this.currentUser };
        } else {
            this.log('❌ Not authenticated');
            return { authenticated: false, user: null };
        }
    }
    
    /**
     * Require authentication (for protected pages)
     */
    async requireAuth() {
        this.log('🔒 Authentication required for this page');
        
        const { authenticated, user } = await this.checkAuth();
        
        if (!authenticated) {
            this.log('❌ Not authenticated - showing sign-in modal');
            return false;
        }
        
        this.log('✅ Authentication verified:', user.email);
        return true;
    }
    
    /**
     * Save user to profiles
     */
    async saveToProfiles(user) {
        try {
            let savedUsers = [];
            const existing = localStorage.getItem(this.STORAGE_KEYS.SAVED_USERS);
            if (existing) {
                savedUsers = JSON.parse(existing);
            }
            
            const existingIndex = savedUsers.findIndex(u => u.email === user.email);
            if (existingIndex >= 0) {
                savedUsers[existingIndex] = user;
            } else {
                savedUsers.push(user);
            }
            
            localStorage.setItem(this.STORAGE_KEYS.SAVED_USERS, JSON.stringify(savedUsers));
            this.log('✅ User saved to profiles');
            
        } catch (error) {
            this.log('⚠️ Failed to save to profiles:', error);
        }
    }
    
    /**
     * Save to Firestore (cloud backup)
     */
    async saveToFirestore(user) {
        try {
            if (window.firestoreSync && window.firestoreSync.initialized) {
                await window.firestoreSync.saveUser(user);
                this.log('✅ User backed up to Firestore');
            } else {
                this.log('ℹ️ Firestore not available');
            }
        } catch (error) {
            this.log('⚠️ Firestore save failed:', error);
        }
    }
    
    /**
     * Track trial user
     */
    trackTrialUser(userData) {
        try {
            let trialUsers = [];
            const existing = localStorage.getItem('trial_users');
            if (existing) {
                trialUsers = JSON.parse(existing);
            }
            
            trialUsers.push({
                ...userData,
                signedUpAt: new Date().toISOString()
            });
            
            localStorage.setItem('trial_users', JSON.stringify(trialUsers));
            this.log('✅ Trial user tracked');
            
        } catch (error) {
            this.log('⚠️ Trial tracking failed:', error);
        }
    }
    
    /**
     * Wait for Firebase Auth to be ready
     */
    async waitForFirebaseAuth(maxAttempts = 30) {
        this.log('⏳ Waiting for Firebase Auth...');
        
        for (let i = 0; i < maxAttempts; i++) {
            if (window.firebaseAuth && window.firebaseAuth.isInitialized) {
                this.log('✅ Firebase Auth ready');
                return window.firebaseAuth;
            }
            await this.sleep(100);
        }
        
        throw new Error('Firebase Auth not available after ' + (maxAttempts * 100) + 'ms');
    }
    
    /**
     * Handle storage changes (cross-tab sync)
     */
    handleStorageChange(event) {
        if (event.key === this.STORAGE_KEYS.SESSION_ACTIVE || 
            event.key === this.STORAGE_KEYS.CURRENT_USER) {
            this.log('🔄 Storage changed, reloading session...');
            this.loadSession();
        }
    }
    
    /**
     * Save current state
     */
    saveState() {
        if (this.isAuthenticated && this.currentUser) {
            localStorage.setItem(this.STORAGE_KEYS.AUTH_STATE, JSON.stringify({
                authenticated: this.isAuthenticated,
                user: this.currentUser,
                timestamp: new Date().toISOString()
            }));
        }
    }
    
    /**
     * Add event listener
     */
    on(event, callback) {
        this.listeners.push({ event, callback });
    }
    
    /**
     * Remove event listener
     */
    off(event, callback) {
        this.listeners = this.listeners.filter(
            listener => !(listener.event === event && listener.callback === callback)
        );
    }
    
    /**
     * Notify listeners
     */
    notifyListeners(event, data) {
        this.listeners
            .filter(listener => listener.event === event)
            .forEach(listener => {
                try {
                    listener.callback(data);
                } catch (error) {
                    this.error('❌ Listener error:', error);
                }
            });
    }
    
    /**
     * Utility: Sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * Logging utilities
     */
    log(...args) {
        if (this.debugMode) {
            console.log('[AuthManager]', ...args);
        }
    }
    
    error(...args) {
        console.error('[AuthManager]', ...args);
    }
    
    /**
     * Get auth headers for API calls
     */
    getAuthHeaders() {
        const token = this.firebaseToken || localStorage.getItem(this.STORAGE_KEYS.FIREBASE_TOKEN);
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        return headers;
    }
    
    /**
     * Get backend user ID
     */
    getBackendUserId() {
        if (this.backendUser) {
            return this.backendUser.id;
        }
        
        try {
            const stored = localStorage.getItem(this.STORAGE_KEYS.BACKEND_USER);
            if (stored) {
                const user = JSON.parse(stored);
                return user.id;
            }
        } catch (e) {
            this.log('⚠️ Error getting backend user ID:', e);
        }
        
        return null;
    }
    
    /**
     * Get diagnostic info
     */
    getDiagnostics() {
        return {
            initialized: this.initialized,
            isAuthenticated: this.isAuthenticated,
            currentUser: this.currentUser,
            backendUser: this.backendUser,
            hasFirebaseToken: !!this.firebaseToken,
            localStorage: {
                session_active: localStorage.getItem(this.STORAGE_KEYS.SESSION_ACTIVE),
                current_user_exists: !!localStorage.getItem(this.STORAGE_KEYS.CURRENT_USER),
                last_login: localStorage.getItem(this.STORAGE_KEYS.LAST_LOGIN),
                backend_user_exists: !!localStorage.getItem(this.STORAGE_KEYS.BACKEND_USER),
                firebase_token_exists: !!localStorage.getItem(this.STORAGE_KEYS.FIREBASE_TOKEN)
            },
            firebaseAuth: {
                available: !!window.firebaseAuth,
                initialized: window.firebaseAuth?.isInitialized
            },
            timestamp: new Date().toISOString()
        };
    }
}

// Create global instance
window.authManager = new AuthManager();

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthManager;
}

console.log('✅ AuthManager loaded and initialized');

