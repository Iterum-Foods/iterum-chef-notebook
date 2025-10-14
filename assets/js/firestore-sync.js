/**
 * Firestore Sync Service
 * Syncs user data between localStorage and Firebase Firestore
 */

import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { 
    getFirestore, 
    doc, 
    setDoc, 
    getDoc, 
    collection, 
    query, 
    where, 
    getDocs,
    updateDoc,
    deleteDoc,
    serverTimestamp 
} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

class FirestoreSync {
    constructor() {
        this.db = null;
        this.initialized = false;
        this.init();
    }
    
    async init() {
        try {
            console.log('🔥 Initializing Firestore...');
            
            // Get Firebase config
            const config = window.firebaseConfig;
            if (!config) {
                throw new Error('Firebase config not found');
            }
            
            // Initialize Firebase app (if not already initialized)
            let app;
            try {
                app = initializeApp(config);
            } catch (e) {
                // App might already be initialized
                const { getApp } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js');
                app = getApp();
            }
            
            // Initialize Firestore
            this.db = getFirestore(app);
            this.initialized = true;
            
            console.log('✅ Firestore initialized successfully');
            console.log('📊 Database:', config.projectId);
            
            // Make globally available
            window.firestoreDB = this.db;
            window.firestoreSync = this;
            
        } catch (error) {
            console.error('❌ Firestore initialization failed:', error);
            this.initialized = false;
        }
    }
    
    /**
     * Save user to Firestore
     */
    async saveUser(userData) {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized, skipping cloud save');
            return false;
        }
        
        try {
            console.log('💾 Saving user to Firestore:', userData.email);
            
            const userId = userData.id || userData.userId || userData.email.replace(/[^a-zA-Z0-9]/g, '_');
            const userRef = doc(this.db, 'users', userId);
            
            const firestoreData = {
                // Profile
                name: userData.name || '',
                email: userData.email || '',
                userId: userId,
                
                // Account info
                type: userData.type || 'email',
                createdAt: userData.createdAt || new Date().toISOString(),
                lastLogin: new Date().toISOString(),
                
                // Optional fields
                company: userData.company || null,
                role: userData.role || null,
                source: userData.source || null,
                photoURL: userData.photoURL || null,
                
                // Trial info (if applicable)
                ...(userData.type === 'trial' && {
                    trial: {
                        startDate: userData.trialStartDate || new Date().toISOString(),
                        endDate: userData.trialEndDate || new Date(Date.now() + 14*24*60*60*1000).toISOString(),
                        daysRemaining: userData.trialDaysRemaining || 14,
                        isActive: true
                    }
                }),
                
                // Metadata
                updatedAt: serverTimestamp()
            };
            
            await setDoc(userRef, firestoreData, { merge: true });
            
            console.log('✅ User saved to Firestore successfully');
            return true;
            
        } catch (error) {
            console.error('❌ Error saving to Firestore:', error);
            return false;
        }
    }
    
    /**
     * Get user from Firestore
     */
    async getUser(userId) {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized');
            return null;
        }
        
        try {
            const userRef = doc(this.db, 'users', userId);
            const userSnap = await getDoc(userRef);
            
            if (userSnap.exists()) {
                console.log('✅ User found in Firestore');
                return userSnap.data();
            } else {
                console.log('⚠️ User not found in Firestore');
                return null;
            }
        } catch (error) {
            console.error('❌ Error getting user from Firestore:', error);
            return null;
        }
    }
    
    /**
     * Get all users from Firestore
     */
    async getAllUsers() {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized');
            return [];
        }
        
        try {
            console.log('📊 Fetching all users from Firestore...');
            
            const usersRef = collection(this.db, 'users');
            const querySnapshot = await getDocs(usersRef);
            
            const users = [];
            querySnapshot.forEach((doc) => {
                users.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            console.log('✅ Fetched', users.length, 'users from Firestore');
            return users;
            
        } catch (error) {
            console.error('❌ Error fetching users from Firestore:', error);
            return [];
        }
    }
    
    /**
     * Get trial users from Firestore
     */
    async getTrialUsers() {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized');
            return [];
        }
        
        try {
            const usersRef = collection(this.db, 'users');
            const q = query(usersRef, where('type', '==', 'trial'));
            const querySnapshot = await getDocs(q);
            
            const users = [];
            querySnapshot.forEach((doc) => {
                users.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            console.log('✅ Fetched', users.length, 'trial users from Firestore');
            return users;
            
        } catch (error) {
            console.error('❌ Error fetching trial users:', error);
            return [];
        }
    }
    
    /**
     * Update user in Firestore
     */
    async updateUser(userId, updates) {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized');
            return false;
        }
        
        try {
            const userRef = doc(this.db, 'users', userId);
            await updateDoc(userRef, {
                ...updates,
                updatedAt: serverTimestamp()
            });
            
            console.log('✅ User updated in Firestore');
            return true;
            
        } catch (error) {
            console.error('❌ Error updating user:', error);
            return false;
        }
    }
    
    /**
     * Delete user from Firestore
     */
    async deleteUser(userId) {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized');
            return false;
        }
        
        try {
            const userRef = doc(this.db, 'users', userId);
            await deleteDoc(userRef);
            
            console.log('✅ User deleted from Firestore');
            return true;
            
        } catch (error) {
            console.error('❌ Error deleting user:', error);
            return false;
        }
    }
    
    /**
     * Sync localStorage to Firestore
     * Migrates existing users from localStorage to cloud
     */
    async syncLocalStorageToFirestore() {
        if (!this.initialized) {
            console.warn('⚠️ Firestore not initialized, cannot sync');
            return { success: false, synced: 0 };
        }
        
        try {
            console.log('🔄 Syncing localStorage to Firestore...');
            
            let syncedCount = 0;
            
            // Sync saved_users
            const savedUsersStr = localStorage.getItem('saved_users');
            if (savedUsersStr) {
                const savedUsers = JSON.parse(savedUsersStr);
                console.log('  Found', savedUsers.length, 'saved users to sync');
                
                for (const user of savedUsers) {
                    const success = await this.saveUser(user);
                    if (success) syncedCount++;
                }
            }
            
            // Sync trial_users
            const trialUsersStr = localStorage.getItem('trial_users');
            if (trialUsersStr) {
                const trialUsers = JSON.parse(trialUsersStr);
                console.log('  Found', trialUsers.length, 'trial users to sync');
                
                for (const user of trialUsers) {
                    // Check if not already synced
                    const userId = user.email.replace(/[^a-zA-Z0-9]/g, '_');
                    const exists = await this.getUser(userId);
                    if (!exists) {
                        const success = await this.saveUser(user);
                        if (success) syncedCount++;
                    }
                }
            }
            
            console.log('✅ Sync complete:', syncedCount, 'users synced to Firestore');
            return { success: true, synced: syncedCount };
            
        } catch (error) {
            console.error('❌ Error syncing to Firestore:', error);
            return { success: false, synced: 0, error: error.message };
        }
    }
    
    /**
     * Load user from Firestore to localStorage
     */
    async loadUserToLocalStorage(userId) {
        const userData = await this.getUser(userId);
        if (userData) {
            localStorage.setItem('current_user', JSON.stringify(userData));
            localStorage.setItem('session_active', 'true');
            console.log('✅ User loaded from Firestore to localStorage');
            return true;
        }
        return false;
    }
}

// Initialize Firestore Sync
console.log('🔥 Loading Firestore Sync Service...');
const firestoreSync = new FirestoreSync();

// Make globally available
window.firestoreSync = firestoreSync;
console.log('✅ Firestore Sync set on window.firestoreSync');

// Export
export default firestoreSync;
export { FirestoreSync };

