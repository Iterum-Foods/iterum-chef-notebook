/**
 * HOTFIX: Authentication System Crash Fix
 * Fixes crash at sign-in screen by ensuring proper reference
 */

// Ensure unifiedAuth alias exists globally
if (typeof window.unifiedAuthSystem !== 'undefined' && typeof window.unifiedAuth === 'undefined') {
    console.log('🔧 HOTFIX: Creating unifiedAuth alias');
    window.unifiedAuth = window.unifiedAuthSystem;
}

// Add safe method wrappers
if (window.unifiedAuthSystem) {
    // Override showMandatoryAuthentication to use safe references
    const originalShowMandatoryAuth = window.unifiedAuthSystem.showMandatoryAuthentication;
    
    window.unifiedAuthSystem.showMandatoryAuthentication = function() {
        try {
            console.log('🔧 HOTFIX: Safe showMandatoryAuthentication called');
            
            // Ensure alias exists before showing modal
            window.unifiedAuth = window.unifiedAuthSystem;
            
            // Call original method
            originalShowMandatoryAuth.call(this);
            
        } catch (error) {
            console.error('❌ HOTFIX: Error in showMandatoryAuthentication:', error);
            
            // Fallback: Show basic auth prompt
            this.showBasicAuthPrompt();
        }
    };
    
    // Add basic auth prompt fallback
    window.unifiedAuthSystem.showBasicAuthPrompt = function() {
        console.log('🆘 HOTFIX: Showing basic auth prompt fallback');
        
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
        `;
        
        modal.innerHTML = `
            <div style="background: white; padding: 40px; border-radius: 20px; max-width: 500px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 20px;">🔒</div>
                <h2 style="margin-bottom: 20px; color: #1f2937;">Access Required</h2>
                <p style="margin-bottom: 30px; color: #6b7280;">Please create a profile to continue</p>
                <button id="create-profile-btn" style="background: #10b981; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; cursor: pointer; width: 100%; margin-bottom: 10px;">
                    ➕ Create Profile
                </button>
                <button id="offline-btn" style="background: #f59e0b; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; cursor: pointer; width: 100%;">
                    🚀 Continue Offline
                </button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add event listeners
        document.getElementById('create-profile-btn').onclick = () => {
            modal.remove();
            this.showCreateProfileModal();
        };
        
        document.getElementById('offline-btn').onclick = () => {
            modal.remove();
            this.createOfflineProfile();
        };
    };
}

// Add global error handler
window.addEventListener('error', function(event) {
    if (event.message && event.message.includes('unifiedAuth')) {
        console.error('❌ HOTFIX: Caught unifiedAuth error:', event.message);
        event.preventDefault();
        
        // Try to recover
        if (window.unifiedAuthSystem) {
            console.log('🔧 HOTFIX: Attempting to recover from error');
            window.unifiedAuth = window.unifiedAuthSystem;
        }
    }
});

console.log('✅ HOTFIX: Authentication crash fix loaded');

