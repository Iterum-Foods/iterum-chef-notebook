import { initializeApp } from 'firebase/app';
import { 
  getAuth, 
  signInAnonymously, 
  signInWithCustomToken, 
  onAuthStateChanged 
} from 'firebase/auth';
import { 
  getFirestore, 
  doc, 
  setDoc, 
  getDoc, 
  onSnapshot,
  collection,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  orderBy,
  getDocs
} from 'firebase/firestore';

// Firebase configuration
const firebaseConfig = typeof window !== 'undefined' && window.__firebase_config 
  ? JSON.parse(window.__firebase_config) 
  : {
      // Default configuration for development
      apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
      authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
      projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
      storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
      messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
      appId: process.env.REACT_APP_FIREBASE_APP_ID
    };

// Initialize Firebase
let app, auth, db;
let isFirebaseEnabled = false;

try {
  // Check if we have valid Firebase config
  if (firebaseConfig.apiKey && firebaseConfig.projectId && 
      firebaseConfig.apiKey !== 'undefined' && firebaseConfig.projectId !== 'undefined') {
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    db = getFirestore(app);
    isFirebaseEnabled = true;
    console.log('✅ Firebase initialized successfully');
  } else {
    console.log('🔄 Running in offline mode (no Firebase config)');
  }
} catch (error) {
  console.error('❌ Firebase initialization failed, running in offline mode:', error);
  isFirebaseEnabled = false;
}

// Authentication service
export const authService = {
  // Sign in anonymously
  signInAnonymously: () => {
    if (isFirebaseEnabled && auth) {
      return signInAnonymously(auth);
    }
    // Offline mode - simulate successful sign in
    return Promise.resolve({ user: { uid: 'offline-user', isAnonymous: true } });
  },
  
  // Sign in with custom token
  signInWithCustomToken: (token) => {
    if (isFirebaseEnabled && auth) {
      return signInWithCustomToken(auth, token);
    }
    return Promise.resolve({ user: { uid: 'offline-user' } });
  },
  
  // Listen to auth state changes
  onAuthStateChanged: (callback) => {
    if (isFirebaseEnabled && auth) {
      return onAuthStateChanged(auth, callback);
    }
    // Offline mode - simulate authenticated user
    setTimeout(() => callback({ uid: 'offline-user', isAnonymous: true }), 100);
    return () => {}; // Return unsubscribe function
  },
  
  // Get current user
  getCurrentUser: () => {
    if (isFirebaseEnabled && auth?.currentUser) {
      return auth.currentUser;
    }
    return { uid: 'offline-user', isAnonymous: true };
  },
  
  // Get user ID
  getUserId: () => {
    if (isFirebaseEnabled && auth?.currentUser) {
      return auth.currentUser.uid;
    }
    return 'offline-user';
  }
};

// Offline storage helpers
const offlineStorage = {
  save: (key, data) => {
    try {
      localStorage.setItem(key, JSON.stringify({ ...data, updatedAt: new Date().toISOString() }));
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  },
  
  get: (key) => {
    try {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return null;
    }
  },
  
  remove: (key) => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing from localStorage:', error);
    }
  }
};

// Database service
export const dbService = {
  // Business plan operations
  saveBusinessPlan: async (userId, appId, data) => {
    if (isFirebaseEnabled && db && userId) {
      const docRef = doc(db, `artifacts/${appId}/users/${userId}/business_plan`, 'business_plan_data');
      await setDoc(docRef, { ...data, updatedAt: new Date() });
    } else {
      // Offline mode - save to localStorage
      const key = `businessPlan_${appId}_${userId}`;
      offlineStorage.save(key, data);
    }
  },
  
  getBusinessPlan: async (userId, appId) => {
    if (isFirebaseEnabled && db && userId) {
      const docRef = doc(db, `artifacts/${appId}/users/${userId}/business_plan`, 'business_plan_data');
      const docSnap = await getDoc(docRef);
      return docSnap.exists() ? docSnap.data() : null;
    } else {
      // Offline mode - get from localStorage
      const key = `businessPlan_${appId}_${userId}`;
      return offlineStorage.get(key);
    }
  },
  
  subscribeToBusinessPlan: (userId, appId, callback) => {
    if (isFirebaseEnabled && db && userId) {
      const docRef = doc(db, `artifacts/${appId}/users/${userId}/business_plan`, 'business_plan_data');
      return onSnapshot(docRef, callback);
    } else {
      // Offline mode - simulate subscription with periodic checks
      const key = `businessPlan_${appId}_${userId}`;
      let lastData = offlineStorage.get(key);
      
      const interval = setInterval(() => {
        const currentData = offlineStorage.get(key);
        if (JSON.stringify(currentData) !== JSON.stringify(lastData)) {
          lastData = currentData;
          callback({ data: () => currentData, exists: () => !!currentData });
        }
      }, 1000);
      
      // Initial callback
      setTimeout(() => callback({ data: () => lastData, exists: () => !!lastData }), 100);
      
      return () => clearInterval(interval);
    }
  },
  
  // Progress tracking operations
  saveProgressData: async (userId, appId, data) => {
    if (isFirebaseEnabled && db && userId) {
      const docRef = doc(db, `artifacts/${appId}/users/${userId}/progress`, 'progress_data');
      await setDoc(docRef, { ...data, updatedAt: new Date() });
    } else {
      // Offline mode
      const key = `progressData_${appId}_${userId}`;
      offlineStorage.save(key, data);
    }
  },
  
  getProgressData: async (userId, appId) => {
    if (isFirebaseEnabled && db && userId) {
      const docRef = doc(db, `artifacts/${appId}/users/${userId}/progress`, 'progress_data');
      const docSnap = await getDoc(docRef);
      return docSnap.exists() ? docSnap.data() : null;
    } else {
      // Offline mode
      const key = `progressData_${appId}_${userId}`;
      return offlineStorage.get(key);
    }
  },
  
  subscribeToProgressData: (userId, appId, callback) => {
    if (isFirebaseEnabled && db && userId) {
      const docRef = doc(db, `artifacts/${appId}/users/${userId}/progress`, 'progress_data');
      return onSnapshot(docRef, callback);
    } else {
      // Offline mode
      const key = `progressData_${appId}_${userId}`;
      let lastData = offlineStorage.get(key);
      
      const interval = setInterval(() => {
        const currentData = offlineStorage.get(key);
        if (JSON.stringify(currentData) !== JSON.stringify(lastData)) {
          lastData = currentData;
          callback({ data: () => currentData, exists: () => !!currentData });
        }
      }, 1000);
      
      setTimeout(() => callback({ data: () => lastData, exists: () => !!lastData }), 100);
      return () => clearInterval(interval);
    }
  },
  
  // Vendor operations
  addVendor: async (userId, appId, vendorData) => {
    if (isFirebaseEnabled && db && userId) {
      const vendorsRef = collection(db, `artifacts/${appId}/users/${userId}/vendors`);
      return await addDoc(vendorsRef, { ...vendorData, createdAt: new Date() });
    } else {
      // Offline mode
      const key = `vendors_${appId}_${userId}`;
      const vendors = offlineStorage.get(key) || [];
      const newVendor = { 
        ...vendorData, 
        id: Date.now().toString(), 
        createdAt: new Date().toISOString() 
      };
      vendors.unshift(newVendor);
      offlineStorage.save(key, vendors);
      return { id: newVendor.id };
    }
  },
  
  updateVendor: async (userId, appId, vendorId, vendorData) => {
    if (isFirebaseEnabled && db && userId) {
      const vendorRef = doc(db, `artifacts/${appId}/users/${userId}/vendors`, vendorId);
      await updateDoc(vendorRef, { ...vendorData, updatedAt: new Date() });
    } else {
      // Offline mode
      const key = `vendors_${appId}_${userId}`;
      const vendors = offlineStorage.get(key) || [];
      const index = vendors.findIndex(v => v.id === vendorId);
      if (index !== -1) {
        vendors[index] = { ...vendors[index], ...vendorData, updatedAt: new Date().toISOString() };
        offlineStorage.save(key, vendors);
      }
    }
  },
  
  deleteVendor: async (userId, appId, vendorId) => {
    if (isFirebaseEnabled && db && userId) {
      const vendorRef = doc(db, `artifacts/${appId}/users/${userId}/vendors`, vendorId);
      await deleteDoc(vendorRef);
    } else {
      // Offline mode
      const key = `vendors_${appId}_${userId}`;
      const vendors = offlineStorage.get(key) || [];
      const filtered = vendors.filter(v => v.id !== vendorId);
      offlineStorage.save(key, filtered);
    }
  },
  
  subscribeToVendors: (userId, appId, callback) => {
    if (isFirebaseEnabled && db && userId) {
      const vendorsRef = collection(db, `artifacts/${appId}/users/${userId}/vendors`);
      const q = query(vendorsRef, orderBy('createdAt', 'desc'));
      return onSnapshot(q, callback);
    } else {
      // Offline mode
      const key = `vendors_${appId}_${userId}`;
      let lastData = offlineStorage.get(key) || [];
      
      const interval = setInterval(() => {
        const currentData = offlineStorage.get(key) || [];
        if (JSON.stringify(currentData) !== JSON.stringify(lastData)) {
          lastData = currentData;
          callback({ docs: currentData.map(doc => ({ id: doc.id, data: () => doc })) });
        }
      }, 1000);
      
      setTimeout(() => callback({ docs: lastData.map(doc => ({ id: doc.id, data: () => doc })) }), 100);
      return () => clearInterval(interval);
    }
  },

  // Draft operations
  saveDraft: async (userId, appId, draftData) => {
    if (isFirebaseEnabled && db && userId) {
      const draftRef = doc(db, `artifacts/${appId}/users/${userId}/drafts`, draftData.id);
      await setDoc(draftRef, { ...draftData, updatedAt: new Date() });
    } else {
      // Offline mode
      const key = `drafts_${appId}_${userId}`;
      const drafts = offlineStorage.get(key) || [];
      const index = drafts.findIndex(d => d.id === draftData.id);
      const updatedDraft = { ...draftData, updatedAt: new Date().toISOString() };
      
      if (index !== -1) {
        drafts[index] = updatedDraft;
      } else {
        drafts.push(updatedDraft);
      }
      
      // Sort by updatedAt desc
      drafts.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
      offlineStorage.save(key, drafts);
    }
  },

  getDraft: async (userId, appId, draftId) => {
    if (isFirebaseEnabled && db && userId) {
      const draftRef = doc(db, `artifacts/${appId}/users/${userId}/drafts`, draftId);
      const docSnap = await getDoc(draftRef);
      return docSnap.exists() ? docSnap.data() : null;
    } else {
      // Offline mode
      const key = `drafts_${appId}_${userId}`;
      const drafts = offlineStorage.get(key) || [];
      return drafts.find(d => d.id === draftId) || null;
    }
  },

  getDrafts: async (userId, appId) => {
    if (isFirebaseEnabled && db && userId) {
      try {
        const draftsRef = collection(db, `artifacts/${appId}/users/${userId}/drafts`);
        const q = query(draftsRef, orderBy('updatedAt', 'desc'));
        const querySnapshot = await getDocs(q);
        
        const drafts = [];
        querySnapshot.forEach((doc) => {
          drafts.push(doc.data());
        });
        
        return drafts;
      } catch (error) {
        console.error('Error getting drafts:', error);
        return [];
      }
    } else {
      // Offline mode
      const key = `drafts_${appId}_${userId}`;
      return offlineStorage.get(key) || [];
    }
  },

  deleteDraft: async (userId, appId, draftId) => {
    if (isFirebaseEnabled && db && userId) {
      const draftRef = doc(db, `artifacts/${appId}/users/${userId}/drafts`, draftId);
      await deleteDoc(draftRef);
    } else {
      // Offline mode
      const key = `drafts_${appId}_${userId}`;
      const drafts = offlineStorage.get(key) || [];
      const filtered = drafts.filter(d => d.id !== draftId);
      offlineStorage.save(key, filtered);
    }
  },

  saveDraftsMetadata: async (userId, appId, draftsArray) => {
    if (isFirebaseEnabled && db && userId) {
      const metadataRef = doc(db, `artifacts/${appId}/users/${userId}`, 'drafts_metadata');
      await setDoc(metadataRef, { 
        drafts: draftsArray.map(draft => ({
          id: draft.id,
          name: draft.name,
          createdAt: draft.createdAt,
          updatedAt: draft.updatedAt
        })),
        lastUpdated: new Date()
      });
    } else {
      // Offline mode - metadata is handled automatically with draft operations
      console.log('Drafts metadata saved in offline mode');
    }
  },

  subscribeToDrafts: (userId, appId, callback) => {
    if (isFirebaseEnabled && db && userId) {
      const draftsRef = collection(db, `artifacts/${appId}/users/${userId}/drafts`);
      const q = query(draftsRef, orderBy('updatedAt', 'desc'));
      return onSnapshot(q, callback);
    } else {
      // Offline mode
      const key = `drafts_${appId}_${userId}`;
      let lastData = offlineStorage.get(key) || [];
      
      const interval = setInterval(() => {
        const currentData = offlineStorage.get(key) || [];
        if (JSON.stringify(currentData) !== JSON.stringify(lastData)) {
          lastData = currentData;
          callback({ docs: currentData.map(doc => ({ id: doc.id, data: () => doc })) });
        }
      }, 1000);
      
      setTimeout(() => callback({ docs: lastData.map(doc => ({ id: doc.id, data: () => doc })) }), 100);
      return () => clearInterval(interval);
    }
  }
};

// App configuration
export const getAppId = () => {
  return typeof window !== 'undefined' && window.__app_id 
    ? window.__app_id 
    : process.env.REACT_APP_ID || 'default-app-id';
};

export const getInitialAuthToken = () => {
  return typeof window !== 'undefined' && window.__initial_auth_token 
    ? window.__initial_auth_token 
    : null;
};

export { auth, db }; 