/**
 * Authentication Guard
 * Protects pages and ensures user is logged in
 * Lightweight and non-blocking
 */

(function() {
    'use strict';
    
    console.log('🔐 Auth Guard checking credentials...');
    
    // List of pages that don't require authentication
    const publicPages = [
        'launch.html',
        'index_simple.html',
        'index_minimal.html',
        'emergency_fix_index.html'
    ];
    
    // Get current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    // Check if this is a public page
    const isPublicPage = publicPages.some(page => currentPage.includes(page));
    
    if (isPublicPage) {
        console.log('✅ Public page - no auth required:', currentPage);
        return;
    }
    
    // Check authentication
    const sessionActive = localStorage.getItem('session_active');
    const currentUser = localStorage.getItem('current_user');
    
    console.log('🔍 Checking credentials...');
    console.log('  Current page:', currentPage);
    console.log('  session_active:', sessionActive);
    console.log('  current_user exists:', !!currentUser);
    
    // If not authenticated, redirect to login
    if (sessionActive !== 'true' || !currentUser) {
        console.warn('🚫 NO CREDENTIALS - Redirecting to login page');
        console.log('  Attempted to access:', currentPage);
        
        // Store the page they were trying to access
        sessionStorage.setItem('redirect_after_login', window.location.href);
        
        // Show message and redirect
        alert('Please sign in to access this page');
        
        // Redirect to launch page
        window.location.href = 'launch.html';
        
        // Prevent page from loading
        throw new Error('Authentication required');
    }
    
    // User is authenticated
    try {
        const user = JSON.parse(currentUser);
        console.log('✅ Credentials verified');
        console.log('👤 User:', user.name || user.email);
        
        // Check if trial has expired
        if (user.type === 'trial' && user.trialEndDate) {
            const trialEnd = new Date(user.trialEndDate);
            const now = new Date();
            const daysRemaining = Math.ceil((trialEnd - now) / (1000 * 60 * 60 * 24));
            
            if (daysRemaining <= 0) {
                console.warn('⚠️ Trial has expired');
                alert('Your 14-day trial has expired. Please subscribe to continue using the app.');
                // Still allow access but show warning
            } else if (daysRemaining <= 3) {
                console.warn(`⚠️ Trial expiring in ${daysRemaining} days`);
                // Show subtle warning
                setTimeout(() => {
                    showTrialWarning(daysRemaining);
                }, 1000);
            }
        }
        
        // Make user data globally available
        window.currentUser = user;
        
    } catch (error) {
        console.error('❌ Error parsing user data:', error);
        console.log('Clearing invalid session...');
        localStorage.removeItem('current_user');
        localStorage.removeItem('session_active');
        window.location.href = 'launch.html';
        throw new Error('Invalid user data');
    }
    
    // Function to show trial warning
    function showTrialWarning(daysRemaining) {
        const warning = document.createElement('div');
        warning.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #fef3c7;
            border: 2px solid #f59e0b;
            padding: 16px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            max-width: 350px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        warning.innerHTML = `
            <div style="color: #92400e; font-weight: 600; margin-bottom: 8px;">
                ⚠️ Trial Ending Soon
            </div>
            <div style="color: #92400e; font-size: 14px; line-height: 1.5; margin-bottom: 12px;">
                Only ${daysRemaining} day${daysRemaining === 1 ? '' : 's'} remaining in your trial
            </div>
            <button onclick="this.parentElement.remove()" 
                    style="padding: 6px 12px; background: #f59e0b; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 13px;">
                Got it
            </button>
        `;
        document.body.appendChild(warning);
        
        // Auto-dismiss after 10 seconds
        setTimeout(() => {
            if (warning.parentElement) warning.remove();
        }, 10000);
    }
    
    console.log('✅ Auth Guard complete - access granted');
})();

