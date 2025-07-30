import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-analytics.js";
import { getAuth, GoogleAuthProvider, signInWithRedirect, getRedirectResult } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAMl-TWSa93_bJIiIGzr6n3VC1QVPZ4bh4",
  authDomain: "iterum-chef-notebook-26949.firebaseapp.com",
  projectId: "iterum-chef-notebook-26949",
  storageBucket: "iterum-chef-notebook-26949.firebasestorage.app",
  messagingSenderId: "34478776055",
  appId: "1:34478776055:web:c5522926c47a1aa7ec7df2",
  measurementId: "G-784WCBH1D9"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

const provider = new GoogleAuthProvider();

// Handle redirect result when page loads
getRedirectResult(auth)
  .then((result) => {
    if (result) {
      const user = result.user;
      console.log("Signed in as:", user.displayName);
      
      // Call the profile manager's function to handle the Google sign-in
      if (window.handleGoogleSignInResult) {
        window.handleGoogleSignInResult(user);
      } else {
        // Fallback to old behavior
        updateAuthUI(user);
      }
    }
  })
  .catch((error) => {
    console.error("Redirect sign-in error:", error);
    // Handle specific error cases
    if (error.code === 'auth/account-exists-with-different-credential') {
      alert('An account already exists with the same email address but different sign-in credentials.');
    } else if (error.code === 'auth/redirect-cancelled-by-user') {
      console.log('Sign-in redirect was cancelled by user');
    } else {
      console.error('Authentication error:', error.message);
    }
  });

// Expose sign-in function globally for use in HTML
window.signInWithGoogle = function() {
  signInWithRedirect(auth, provider)
    .then(() => {
      // Redirect will happen automatically
      console.log("Redirecting to Google sign-in...");
    })
    .catch((error) => {
      console.error("Sign-in error:", error);
      alert("Sign-in failed. Please try again.");
    });
};

// Function to update UI based on auth state (legacy support)
function updateAuthUI(user) {
  const loadingOverlay = document.getElementById('loading-overlay');
  if (loadingOverlay) {
    loadingOverlay.style.opacity = '0';
    setTimeout(() => loadingOverlay.style.display = 'none', 500);
  }
  
  // Update sign-in button text if user is signed in
  const signInBtn = document.querySelector('button[onclick="window.signInWithGoogle()"]');
  if (signInBtn && user) {
    signInBtn.textContent = `Signed in as ${user.displayName}`;
    signInBtn.onclick = () => {
      auth.signOut().then(() => {
        window.location.reload();
      });
    };
  }
}

// Listen for auth state changes
auth.onAuthStateChanged((user) => {
  if (user) {
    console.log("User is signed in:", user.displayName);
    // Don't automatically update UI here - let the profile manager handle it
  } else {
    console.log("User is signed out");
    // Don't automatically show loading overlay - let the profile manager handle it
  }
});

// Expose auth for use in other scripts if needed
window.firebaseAuth = auth;

// UPDATE: User switching to use unified auth system
window.switchUser = function() {
    console.log('Switch user clicked');
    console.log('window.unifiedAuth available:', !!window.unifiedAuth);
    
    // Try unified auth first
    if (window.unifiedAuth && typeof window.unifiedAuth.handleLogout === 'function') {
        console.log('Using unified auth for user switch');
        window.unifiedAuth.handleLogout();
        return;
    }
    
    // If unified auth not available, wait a bit and try again
    let retryCount = 0;
    const maxRetries = 10;
    
    function tryUnifiedAuth() {
        if (window.unifiedAuth && typeof window.unifiedAuth.handleLogout === 'function') {
            console.log('Using unified auth for user switch (after wait)');
            window.unifiedAuth.handleLogout();
        } else if (retryCount < maxRetries) {
            retryCount++;
            setTimeout(tryUnifiedAuth, 100);
        } else {
            console.log('Using fallback for user switch - unified auth not available');
            // Fallback: clear user and reload
            localStorage.removeItem('current_user');
            localStorage.removeItem('currentLocalProfile');
            localStorage.removeItem('iterum_auth_token');
            localStorage.removeItem('access_token');
            
            // Clear any profile data
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
              if (key.startsWith('equipment_') || key.startsWith('profile_') || key.includes('user')) {
                localStorage.removeItem(key);
              }
            });
            
            alert('Switching user - page will reload');
            setTimeout(() => window.location.reload(), 500);
        }
    }
    
    tryUnifiedAuth();
};

// Daily Notes and HACCP Integration
document.addEventListener('DOMContentLoaded', function() {
    // Initialize daily notes functionality
    initializeDailyNotes();
    
    // Initialize HACCP integration
    initializeHACCPIntegration();
    updateUserInfo(); // Call updateUserInfo on page load
});

function updateUserInfo() {
  const userInfo = document.getElementById('user-info');
  if (!userInfo) return;
  const username = localStorage.getItem('username');
  userInfo.textContent = username ? username : 'Guest';
}

function initializeDailyNotes() {
    const notesForm = document.getElementById('daily-notes-form');
    const notesDate = document.getElementById('notes-date');
    
    if (notesForm) {
        // Set today's date as default
        const today = new Date().toISOString().split('T')[0];
        notesDate.value = today;
        
        // Load existing notes for today
        loadDailyNotes(today);
        
        // Handle date changes
        notesDate.addEventListener('change', function() {
            loadDailyNotes(this.value);
        });
        
        // Handle form submission
        notesForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveDailyNotes();
        });
    }
}

function initializeHACCPIntegration() {
    const addDailyTempBtn = document.getElementById('add-daily-temp');
    const dailyFridgeSelect = document.getElementById('daily-fridge-select');
    
    if (addDailyTempBtn) {
        addDailyTempBtn.addEventListener('click', function() {
            addTemperatureFromDailyNotes();
        });
    }
    
    // Update refrigerator select when HACCP manager is ready
    setTimeout(() => {
        if (window.haccpManager && dailyFridgeSelect) {
            updateDailyFridgeSelect();
        }
    }, 1000);
}

function updateDailyFridgeSelect() {
    const dailyFridgeSelect = document.getElementById('daily-fridge-select');
    if (!dailyFridgeSelect || !window.haccpManager) return;
    
    // Clear existing options except the first one
    dailyFridgeSelect.innerHTML = '<option value="">Select Refrigerator</option>';
    
    // Add refrigerators from HACCP manager
    window.haccpManager.refrigerators.forEach(fridge => {
        const option = document.createElement('option');
        option.value = fridge.id;
        option.textContent = fridge.name;
        dailyFridgeSelect.appendChild(option);
    });
}

function addTemperatureFromDailyNotes() {
    const fridgeSelect = document.getElementById('daily-fridge-select');
    const tempInput = document.getElementById('daily-temp');
    const haccpNotes = document.getElementById('haccp-notes');
    
    const fridgeId = fridgeSelect.value;
    const temperature = parseFloat(tempInput.value);
    
    if (!fridgeId || isNaN(temperature)) {
        showNotification('Please select a refrigerator and enter a valid temperature', 'error');
        return;
    }
    
    if (!window.haccpManager) {
        showNotification('HACCP system not ready. Please try again.', 'error');
        return;
    }
    
    const fridge = window.haccpManager.refrigerators.find(f => f.id == fridgeId);
    if (!fridge) {
        showNotification('Selected refrigerator not found', 'error');
        return;
    }
    
    // Add to HACCP system
    const reading = {
        id: Date.now(),
        refrigerator_id: fridgeId,
        refrigerator_name: fridge.name,
        temperature: temperature,
        time_slot: getCurrentTimeSlot(),
        timestamp: new Date().toISOString(),
        notes: haccpNotes.value.trim(),
        status: window.haccpManager.getTemperatureStatus(temperature, fridge.category || 'refrigerator')
    };
    
    window.haccpManager.temperatureReadings.push(reading);
    window.haccpManager.saveToLocalStorage();
    window.haccpManager.updateDisplay();
    window.haccpManager.checkForAlerts();
    
    // Clear the temperature input
    tempInput.value = '';
    
    // Add to notes textarea
    const currentNotes = haccpNotes.value;
    const newEntry = `${fridge.name}: ${temperature}°F (${new Date().toLocaleTimeString()})`;
    haccpNotes.value = currentNotes ? `${currentNotes}\n${newEntry}` : newEntry;
    
    showNotification(`Temperature logged: ${fridge.name} - ${temperature}°F`, 'success');
}

function getCurrentTimeSlot() {
    const hour = new Date().getHours();
    if (hour >= 6 && hour < 10) return 'morning';
    if (hour >= 14 && hour < 18) return 'afternoon';
    if (hour >= 18 && hour < 22) return 'evening';
    return 'night';
}

function loadDailyNotes(date) {
    const notes = JSON.parse(localStorage.getItem(`daily_notes_${date}`) || '{}');
    
    document.getElementById('general-notes').value = notes.generalNotes || notes.general || '';
    document.getElementById('haccp-notes').value = notes.haccpNotes || notes.haccp || '';
    document.getElementById('maintenance-notes').value = notes.maintenanceNotes || notes.maintenance || '';
    document.getElementById('recipe-changes-notes').value = notes.recipeChangesNotes || notes.recipe_changes || '';
}

function saveDailyNotes() {
    const date = document.getElementById('notes-date').value;
    const notes = {
        date: date,
        generalNotes: document.getElementById('general-notes').value,
        haccpNotes: document.getElementById('haccp-notes').value,
        maintenanceNotes: document.getElementById('maintenance-notes').value,
        recipeChangesNotes: document.getElementById('recipe-changes-notes').value,
        timestamp: new Date().toISOString()
    };
    
    // Save to localStorage with date key
    localStorage.setItem(`daily_notes_${date}`, JSON.stringify(notes));
    
    // Also save to calendar manager if available
    if (window.calendarManager) {
        window.calendarManager.addJournalEntry(notes);
    }
    
    showNotification('Daily notes saved successfully', 'success');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
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