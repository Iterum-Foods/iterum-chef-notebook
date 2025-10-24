// Iterum Foods - Unified Waitlist & CRM Integration
// This script handles waitlist signups and CRM integration for all landing pages

// Get platform config from page (set by individual pages)
const getPlatformConfig = () => {
    return window.PLATFORM_CONFIG || { name: 'Main', code: 'main', icon: '🎯' };
};

// Open waitlist modal
function openWaitlistModal() {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.id = 'waitlist-modal-dynamic';
    
    const platform = getPlatformConfig();
    
    modal.innerHTML = `
        <div class="modal-content">
            <button class="close-modal" onclick="closeWaitlistModal()">×</button>
            <div style="margin-bottom: 32px; text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 16px;">${platform.icon}</div>
                <h2 style="font-size: 2rem; font-weight: 900; margin-bottom: 8px;">Join ${platform.name} Waitlist</h2>
                <p style="color: #6b7280; font-size: 1.125rem;">Get early access and exclusive updates</p>
            </div>
            
            <div class="success-message" id="success-message-modal">
                ✅ Success! You're on the waitlist. We'll be in touch soon!
            </div>
            
            <form id="waitlist-form-modal" onsubmit="submitWaitlist(event)">
                <div class="form-group">
                    <label class="form-label">Full Name *</label>
                    <input type="text" class="form-input" id="waitlist-name" required placeholder="John Doe">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Email Address *</label>
                    <input type="email" class="form-input" id="waitlist-email" required placeholder="john@restaurant.com">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Phone Number</label>
                    <input type="tel" class="form-input" id="waitlist-phone" placeholder="+1 (555) 123-4567">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Company / Restaurant Name</label>
                    <input type="text" class="form-input" id="waitlist-company" placeholder="Your Restaurant">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Role</label>
                    <select class="form-select" id="waitlist-role">
                        <option value="">Select your role...</option>
                        <option value="Owner">Restaurant Owner</option>
                        <option value="Executive Chef">Executive Chef</option>
                        <option value="Sous Chef">Sous Chef</option>
                        <option value="Manager">Restaurant Manager</option>
                        <option value="Entrepreneur">Aspiring Entrepreneur</option>
                        <option value="Professional">Culinary Professional</option>
                        <option value="Student">Culinary Student</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label class="form-label">How did you hear about us?</label>
                    <select class="form-select" id="waitlist-source">
                        <option value="">Select source...</option>
                        <option value="google">Google Search</option>
                        <option value="social">Social Media</option>
                        <option value="referral">Friend/Colleague Referral</option>
                        <option value="blog">Blog/Article</option>
                        <option value="ad">Advertisement</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 8px;">
                    <i class="fas fa-rocket"></i> Join Waitlist
                </button>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeWaitlistModal();
        }
    });
    
    // Close on escape
    const escHandler = (e) => {
        if (e.key === 'Escape') {
            closeWaitlistModal();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
}

// Close waitlist modal
function closeWaitlistModal() {
    const modal = document.getElementById('waitlist-modal-dynamic');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.remove();
            document.body.style.overflow = '';
        }, 300);
    }
}

// Submit waitlist form
function submitWaitlist(event) {
    event.preventDefault();
    
    const platform = getPlatformConfig();
    
    const data = {
        id: `waitlist_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        name: document.getElementById('waitlist-name').value,
        email: document.getElementById('waitlist-email').value,
        phone: document.getElementById('waitlist-phone').value,
        company: document.getElementById('waitlist-company').value,
        role: document.getElementById('waitlist-role').value,
        hearAbout: document.getElementById('waitlist-source').value,
        platform: platform.code,
        platformName: platform.name,
        timestamp: new Date().toISOString(),
        source: 'landing_page_waitlist',
        status: 'new',
        priority: 'medium',
        position: getNextWaitlistPosition()
    };
    
    // Save to main waitlist
    saveToMainWaitlist(data);
    
    // Save to platform-specific waitlist
    saveToPlatformWaitlist(data);
    
    // Save to CRM
    saveToCRM(data);
    
    // Track with Google Analytics
    trackWaitlistSignup(data);
    
    // Show success message
    document.getElementById('success-message-modal').classList.add('show');
    document.getElementById('waitlist-form-modal').style.display = 'none';
    
    // Notify user of position
    const position = data.position;
    setTimeout(() => {
        alert(`🎉 Success! You're #${position} on the ${platform.name} waitlist!\n\nWe'll email you at ${data.email} when it's your turn.`);
    }, 500);
    
    // Close modal after 3 seconds
    setTimeout(() => {
        closeWaitlistModal();
    }, 3000);
    
    console.log('✅ Waitlist signup complete:', data);
}

// Save to main waitlist
function saveToMainWaitlist(data) {
    let mainWaitlist = JSON.parse(localStorage.getItem('iterum_main_waitlist') || '[]');
    mainWaitlist.push(data);
    localStorage.setItem('iterum_main_waitlist', JSON.stringify(mainWaitlist));
    console.log('✅ Saved to main waitlist');
}

// Save to platform-specific waitlist
function saveToPlatformWaitlist(data) {
    const key = `iterum_waitlist_${data.platform}`;
    let platformWaitlist = JSON.parse(localStorage.getItem(key) || '[]');
    platformWaitlist.push(data);
    localStorage.setItem(key, JSON.stringify(platformWaitlist));
    console.log(`✅ Saved to ${data.platform} waitlist`);
}

// Save to CRM
function saveToCRM(data) {
    let crmContacts = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
    
    // Check for duplicate
    const existingIndex = crmContacts.findIndex(c => c.email === data.email);
    
    const crmContact = {
        id: data.id,
        name: data.name,
        email: data.email,
        phone: data.phone,
        company: data.company,
        role: data.role,
        type: 'waitlist',
        contactType: 'waitlist',
        platform: data.platformName,
        status: 'pending',
        added: data.timestamp,
        source: data.source,
        waitlistPosition: data.position,
        priority: data.priority,
        hearAbout: data.hearAbout
    };
    
    if (existingIndex >= 0) {
        crmContacts[existingIndex] = crmContact;
        console.log('✅ Updated existing CRM contact');
    } else {
        crmContacts.push(crmContact);
        console.log('✅ Added new CRM contact');
    }
    
    localStorage.setItem('crm_all_contacts', JSON.stringify(crmContacts));
}

// Get next waitlist position
function getNextWaitlistPosition() {
    const mainWaitlist = JSON.parse(localStorage.getItem('iterum_main_waitlist') || '[]');
    return mainWaitlist.length + 1;
}

// Track with Google Analytics
function trackWaitlistSignup(data) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'waitlist_signup', {
            event_category: 'Waitlist',
            event_label: data.platform,
            platform: data.platformName,
            value: 1
        });
        console.log('📊 Tracked with Google Analytics');
    }
}

// Try to sync to Firestore (if available)
async function syncToFirestore(data) {
    try {
        if (window.firestoreSync && window.firestoreSync.initialized) {
            await window.firestoreSync.saveUser(data);
            console.log('☁️ Synced to Firestore');
        }
    } catch (error) {
        console.warn('⚠️ Firestore sync failed (non-critical):', error);
    }
}

// View all waitlist data (for admin/testing)
window.viewWaitlistData = function() {
    const main = JSON.parse(localStorage.getItem('iterum_main_waitlist') || '[]');
    const culinary = JSON.parse(localStorage.getItem('iterum_waitlist_culinary') || '[]');
    const business = JSON.parse(localStorage.getItem('iterum_waitlist_business') || '[]');
    const payroll = JSON.parse(localStorage.getItem('iterum_waitlist_payroll') || '[]');
    const skills = JSON.parse(localStorage.getItem('iterum_waitlist_skills') || '[]');
    const crm = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
    
    console.log('📊 WAITLIST DATA:');
    console.log('Main Waitlist:', main.length, 'contacts');
    console.log('Culinary Waitlist:', culinary.length, 'contacts');
    console.log('Business Waitlist:', business.length, 'contacts');
    console.log('Payroll Waitlist:', payroll.length, 'contacts');
    console.log('Skills Waitlist:', skills.length, 'contacts');
    console.log('CRM Total:', crm.length, 'contacts');
    
    return {
        main,
        culinary,
        business,
        payroll,
        skills,
        crm
    };
};

// Export waitlist to CSV
window.exportWaitlistCSV = function() {
    const main = JSON.parse(localStorage.getItem('iterum_main_waitlist') || '[]');
    
    if (main.length === 0) {
        alert('No waitlist data to export');
        return;
    }
    
    const headers = ['Position', 'Name', 'Email', 'Phone', 'Company', 'Role', 'Platform', 'Source', 'Date Added'];
    const rows = main.map(contact => [
        contact.position,
        contact.name,
        contact.email,
        contact.phone || '',
        contact.company || '',
        contact.role || '',
        contact.platformName,
        contact.hearAbout || 'Not specified',
        contact.timestamp
    ]);
    
    let csvContent = headers.join(',') + '\n';
    rows.forEach(row => {
        csvContent += row.map(field => `"${field}"`).join(',') + '\n';
    });
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `iterum-waitlist-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    
    console.log('✅ Exported waitlist to CSV');
};

console.log('✅ Iterum Foods Waitlist & CRM Integration Loaded');

