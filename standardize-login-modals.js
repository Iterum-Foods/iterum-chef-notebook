/**
 * Standardize Login Modals Across Platform
 * This script automatically replaces any existing login modal with the standardized version
 */

function standardizeLoginModal() {
    // Remove existing login modal if it exists
    const existingModal = document.getElementById('login-modal');
    if (existingModal) {
        existingModal.remove();
        console.log('📝 Removed existing login modal for standardization');
    }

    // Check if standardized modal is already loaded
    const standardModal = document.querySelector('#login-modal[data-standardized="true"]');
    if (standardModal) {
        console.log('✅ Standardized login modal already loaded');
        return;
    }

    // Load standardized modal from template
    fetch('shared-login-modal.html')
        .then(response => {
            if (!response.ok) {
                console.warn('⚠️ Standardized login modal template not found, creating fallback');
                createFallbackModal();
                return null;
            }
            return response.text();
        })
        .then(html => {
            if (html) {
                insertStandardizedModal(html);
            }
        })
        .catch(error => {
            console.warn('⚠️ Error loading standardized login modal:', error);
            createFallbackModal();
        });
}

function insertStandardizedModal(html) {
    try {
        // Create a temporary div to parse the HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        
        // Extract the modal elements
        const loadingOverlay = tempDiv.querySelector('#loading-overlay');
        const loginModal = tempDiv.querySelector('#login-modal');
        
        // Insert loading overlay if it doesn't exist
        if (!document.getElementById('loading-overlay') && loadingOverlay) {
            document.body.appendChild(loadingOverlay);
        }
        
        // Insert login modal
        if (loginModal) {
            // Mark as standardized
            loginModal.setAttribute('data-standardized', 'true');
            document.body.appendChild(loginModal);
            console.log('✅ Standardized login modal loaded successfully');
            
            // Execute any scripts from the template
            const scripts = tempDiv.querySelectorAll('script');
            scripts.forEach(script => {
                try {
                    const newScript = document.createElement('script');
                    newScript.textContent = script.textContent;
                    document.head.appendChild(newScript);
                } catch (e) {
                    console.warn('Script execution error:', e);
                }
            });
            
            // Execute any styles from the template
            const styles = tempDiv.querySelectorAll('style');
            styles.forEach(style => {
                document.head.appendChild(style.cloneNode(true));
            });
        }
    } catch (error) {
        console.error('❌ Error inserting standardized modal:', error);
        createFallbackModal();
    }
}

function createFallbackModal() {
    // Create a basic fallback modal if the standardized one fails to load
    const fallbackModal = document.createElement('div');
    fallbackModal.id = 'login-modal';
    fallbackModal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 hidden';
    fallbackModal.setAttribute('data-standardized', 'fallback');
    
    fallbackModal.innerHTML = `
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-gray-800">Welcome to Iterum</h2>
                <button onclick="document.getElementById('login-modal').classList.add('hidden')" 
                        class="text-gray-500 hover:text-red-500 text-2xl font-bold">×</button>
            </div>
            
            <div class="space-y-4">
                <p class="text-gray-600">Choose how you'd like to continue:</p>
                
                <button onclick="createBasicOfflineProfile()" 
                        class="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold transition-all">
                    🚀 Continue Offline
                </button>
                
                <button onclick="showBasicLoginForm()" 
                        class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 px-4 rounded-lg font-semibold transition-all">
                    📧 Sign In with Email
                </button>
            </div>
            
            <!-- Basic Login Form (initially hidden) -->
            <div id="basic-login-form" class="hidden mt-6 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Name or Email</label>
                    <input type="text" id="fallback-login-input" 
                           class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" 
                           placeholder="Enter your name or email">
                </div>
                <button onclick="handleFallbackLogin()" 
                        class="w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg font-semibold">
                    Sign In
                </button>
                <button onclick="document.getElementById('basic-login-form').classList.add('hidden')" 
                        class="w-full text-gray-500 hover:text-gray-700 text-sm">
                    ← Back to options
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(fallbackModal);
    console.log('⚠️ Fallback login modal created');
    
    // Add fallback functions to window
    window.createBasicOfflineProfile = function() {
        const user = {
            id: 'offline_' + Date.now(),
            name: 'Local User',
            email: 'local@offline.com',
            role: 'Chef',
            restaurant: 'My Kitchen',
            isOffline: true
        };
        localStorage.setItem('current_user', JSON.stringify(user));
        fallbackModal.classList.add('hidden');
        
        // Update UI if possible
        if (window.unifiedAuth && window.unifiedAuth.updateAuthUI) {
            window.unifiedAuth.updateAuthUI(user);
        }
        
        console.log('✅ Offline profile created');
    };
    
    window.showBasicLoginForm = function() {
        document.getElementById('basic-login-form').classList.remove('hidden');
    };
    
    window.handleFallbackLogin = function() {
        const input = document.getElementById('fallback-login-input');
        const nameOrEmail = input.value.trim();
        
        if (!nameOrEmail) {
            alert('Please enter your name or email');
            return;
        }
        
        const user = {
            id: 'user_' + Date.now(),
            name: nameOrEmail.includes('@') ? nameOrEmail.split('@')[0] : nameOrEmail,
            email: nameOrEmail.includes('@') ? nameOrEmail : nameOrEmail + '@local.com',
            role: 'Chef',
            restaurant: 'My Kitchen'
        };
        
        localStorage.setItem('current_user', JSON.stringify(user));
        fallbackModal.classList.add('hidden');
        
        // Update UI if possible
        if (window.unifiedAuth && window.unifiedAuth.updateAuthUI) {
            window.unifiedAuth.updateAuthUI(user);
        }
        
        console.log('✅ User logged in:', user.name);
    };
}

// Global function to show login modal
window.showLoginModal = function() {
    const modal = document.getElementById('login-modal');
    if (modal) {
        modal.classList.remove('hidden');
    } else {
        console.warn('Login modal not found, triggering standardization...');
        standardizeLoginModal();
        // Try again after a short delay
        setTimeout(() => {
            const newModal = document.getElementById('login-modal');
            if (newModal) {
                newModal.classList.remove('hidden');
            }
        }, 100);
    }
};

// Auto-standardize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to let other scripts load first
    setTimeout(standardizeLoginModal, 100);
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { standardizeLoginModal, showLoginModal };
} 