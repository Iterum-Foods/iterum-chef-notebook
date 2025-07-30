// Debug script for authentication buttons
// This helps diagnose why logout and switch user buttons may not be working

function debugAuthButtons() {
    console.log('🐛 === AUTH BUTTONS DEBUG ===');
    
    // Check if buttons exist
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const switchUserBtn = document.querySelector('button[onclick="window.switchUser()"]');
    
    console.log('Login button element:', loginBtn);
    console.log('Logout button element:', logoutBtn);
    console.log('Switch user button element:', switchUserBtn);
    
    // Check if unified auth is available
    console.log('window.unifiedAuth available:', !!window.unifiedAuth);
    if (window.unifiedAuth) {
        console.log('window.unifiedAuth.handleLogout available:', typeof window.unifiedAuth.handleLogout);
    }
    
    // Check if window.switchUser function exists
    console.log('window.switchUser function:', typeof window.switchUser);
    
    // Check button visibility
    if (loginBtn) console.log('Login button display:', getComputedStyle(loginBtn).display);
    if (logoutBtn) console.log('Logout button display:', getComputedStyle(logoutBtn).display);
    if (switchUserBtn) console.log('Switch user button display:', getComputedStyle(switchUserBtn).display);
    
    // Check event listeners
    console.log('Checking for event listeners...');
    if (logoutBtn) {
        console.log('Logout button onclick:', logoutBtn.onclick);
        console.log('Logout button event listeners:', getEventListeners ? getEventListeners(logoutBtn) : 'getEventListeners not available');
    }
    
    if (switchUserBtn) {
        console.log('Switch user button onclick:', switchUserBtn.onclick);
        console.log('Switch user button event listeners:', getEventListeners ? getEventListeners(switchUserBtn) : 'getEventListeners not available');
    }
    
    // Test button clicks programmatically
    console.log('🧪 Testing button functionality...');
    
    if (logoutBtn && logoutBtn.style.display !== 'none') {
        console.log('Attempting to click logout button programmatically...');
        try {
            logoutBtn.click();
        } catch (error) {
            console.error('Error clicking logout button:', error);
        }
    }
    
    console.log('🐛 === END DEBUG ===');
}

// Add to window for manual testing
window.debugAuthButtons = debugAuthButtons;

// Test button clicking manually
window.testLogoutButton = function() {
    console.log('🧪 Manual logout button test...');
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        console.log('Logout button found, attempting click...');
        logoutBtn.click();
    } else {
        console.log('❌ Logout button not found');
    }
};

window.testSwitchUserButton = function() {
    console.log('🧪 Manual switch user button test...');
    const switchUserBtn = document.querySelector('button[onclick="window.switchUser()"]');
    if (switchUserBtn) {
        console.log('Switch user button found, attempting click...');
        switchUserBtn.click();
    } else {
        console.log('❌ Switch user button not found');
    }
};

// Auto-run debug after page loads
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        console.log('🔍 Auto-running auth button debug...');
        debugAuthButtons();
    }, 2000);
}); 