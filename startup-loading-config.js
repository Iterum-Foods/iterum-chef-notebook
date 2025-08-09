/**
 * Startup Loading Configuration
 * Controls the loading screen duration at startup
 */

class StartupLoadingManager {
    constructor() {
        this.loadingDuration = 3000; // 3 seconds default
        this.fadeOutDuration = 500; // Fade out animation duration
        this.loadingStartTime = Date.now();
        this.hasStarted = false;
        
        this.init();
    }

    /**
     * Initialize the loading manager
     */
    init() {
        console.log('🕒 Startup loading configured for 3 seconds');
        
        // Override existing loading screen hide functions
        this.overrideExistingFunctions();
        
        // Set up automatic hiding after 3 seconds
        this.setupAutoHide();
        
        // Track loading completion
        this.trackLoadingCompletion();
    }

    /**
     * Override existing hideLoadingScreen functions to use our timing
     */
    overrideExistingFunctions() {
        // Store original functions
        const originalUnifiedAuthHide = window.unifiedAuth?.hideLoadingScreen;
        const originalMainAuthUI = window.updateAuthUI;

        // Override unified auth hideLoadingScreen
        if (window.unifiedAuth) {
            window.unifiedAuth.hideLoadingScreen = () => {
                this.hideLoadingScreenWithDelay();
            };
        }

        // Override main.js updateAuthUI
        window.updateAuthUI = (user) => {
            // Call original function but with our timing
            this.hideLoadingScreenWithDelay();
            
            // Update sign-in button if needed
            const signInBtn = document.querySelector('button[onclick="window.signInWithGoogle()"]');
            if (signInBtn && user) {
                signInBtn.textContent = `Signed in as ${user.displayName}`;
                signInBtn.onclick = () => {
                    if (window.firebaseAuth) {
                        window.firebaseAuth.signOut().then(() => {
                            window.location.reload();
                        });
                    }
                };
            }
        };

        console.log('✅ Loading screen timing functions overridden');
    }

    /**
     * Set up automatic hiding after 3 seconds
     */
    setupAutoHide() {
        // Always hide after 3 seconds regardless of other events
        setTimeout(() => {
            this.forceHideLoadingScreen();
            console.log('⏰ 3-second loading screen completed');
        }, this.loadingDuration);
    }

    /**
     * Hide loading screen with minimum duration check
     */
    hideLoadingScreenWithDelay() {
        const elapsed = Date.now() - this.loadingStartTime;
        const remainingTime = Math.max(0, this.loadingDuration - elapsed);

        if (remainingTime > 0) {
            console.log(`⏳ Loading screen will continue for ${remainingTime}ms more`);
            setTimeout(() => {
                this.forceHideLoadingScreen();
            }, remainingTime);
        } else {
            this.forceHideLoadingScreen();
        }
    }

    /**
     * Force hide the loading screen with animation
     */
    forceHideLoadingScreen() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay && loadingOverlay.style.display !== 'none') {
            console.log('🎭 Hiding loading screen with fade out animation');
            
            // Start fade out
            loadingOverlay.style.opacity = '0';
            loadingOverlay.style.transition = `opacity ${this.fadeOutDuration}ms ease-out`;
            
            // Remove after fade out
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
                console.log('✅ Loading screen hidden completely');
                
                // Ensure page is fully visible
                this.ensurePageVisibility();
            }, this.fadeOutDuration);
        }
    }

    /**
     * Ensure page content is visible
     */
    ensurePageVisibility() {
        if (document.body) {
            document.body.style.display = 'block';
            document.body.style.visibility = 'visible';
            document.body.style.opacity = '1';
        }

        // Show main content elements
        const mainElements = document.querySelectorAll('.container, main, .main-content, #main-content, header, .header');
        mainElements.forEach(el => {
            el.style.display = 'block';
            el.style.visibility = 'visible';
            el.style.opacity = '1';
        });

        console.log('✅ Page visibility ensured');
    }

    /**
     * Track when loading operations complete
     */
    trackLoadingCompletion() {
        // Track script loading completion
        if (typeof Promise !== 'undefined') {
            // Monitor script loading promises
            const originalPromiseAll = Promise.all;
            Promise.all = function(promises) {
                return originalPromiseAll.call(this, promises).then(results => {
                    console.log('📦 Scripts finished loading, but maintaining 3-second minimum display');
                    return results;
                });
            };
        }

        // Track DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                console.log('📄 DOM ready, but maintaining 3-second loading screen');
            });
        }

        // Track window load
        window.addEventListener('load', () => {
            console.log('🌐 Window loaded, but maintaining 3-second loading screen');
        });
    }

    /**
     * Allow manual override of loading duration
     */
    setLoadingDuration(milliseconds) {
        if (typeof milliseconds === 'number' && milliseconds > 0) {
            this.loadingDuration = milliseconds;
            console.log(`⏱️ Loading duration set to ${milliseconds}ms`);
        }
    }

    /**
     * Get remaining loading time
     */
    getRemainingTime() {
        const elapsed = Date.now() - this.loadingStartTime;
        return Math.max(0, this.loadingDuration - elapsed);
    }

    /**
     * Manual hide (for debugging)
     */
    manualHide() {
        console.log('🔧 Manual loading screen hide triggered');
        this.forceHideLoadingScreen();
    }
}

// Initialize the startup loading manager immediately
window.startupLoadingManager = new StartupLoadingManager();

// Global functions for easy access
window.setLoadingDuration = function(ms) {
    if (window.startupLoadingManager) {
        window.startupLoadingManager.setLoadingDuration(ms);
    }
};

window.hideLoadingNow = function() {
    if (window.startupLoadingManager) {
        window.startupLoadingManager.manualHide();
    }
};

window.getLoadingTimeRemaining = function() {
    if (window.startupLoadingManager) {
        return window.startupLoadingManager.getRemainingTime();
    }
    return 0;
};

console.log('🚀 Startup Loading Manager initialized - 3 second loading screen active');
console.log('💡 Use setLoadingDuration(ms) to change duration');
console.log('💡 Use hideLoadingNow() to hide immediately');
console.log('💡 Use getLoadingTimeRemaining() to check remaining time');