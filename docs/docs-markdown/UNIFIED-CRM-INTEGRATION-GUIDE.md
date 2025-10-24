# 🎯 Unified CRM Integration Guide

## Overview

Your **Iterum Foods Unified CRM** (`iterum-crm-unified.html`) is now centralized in your main folder and ready to integrate with all 4 platforms:

1. 🍽️ **Culinary R&D Platform** (Recipe organizer, menu builder)
2. 📊 **Restaurant Business Planner** (Financial planning, market analysis)
3. 💰 **Payroll System** (Time tracking, employee management)
4. 🎯 **Skills Portfolio** (Professional networking)

---

## 📍 CRM Location

**File:** `C:\Users\chefm\Iterum Innovation\iterum-crm-unified.html`

**Quick Access:** Double-click `OPEN-CRM.bat` (see below to create)

---

## 🚀 How to Use

### **Opening the Unified CRM**

1. Navigate to: `C:\Users\chefm\Iterum Innovation\`
2. Open: `iterum-crm-unified.html` in your browser
3. The CRM shows all contacts from all 4 platforms

### **Features**

✅ **Platform Launchers** - Quick access buttons to open each platform  
✅ **Unified Contact List** - All contacts from all platforms in one view  
✅ **Platform Tracking** - See which platform each contact came from  
✅ **Contact Conversion** - Convert waitlist/leads → active users  
✅ **Export to CSV** - Download all contacts for analysis  
✅ **Cloud Sync** - Firebase/Firestore integration  
✅ **Search & Filter** - Find contacts by name, email, platform  

---

## 🔗 Integration with Each Platform

### 1️⃣ Culinary R&D Platform Integration

**Location:** `index.html`

**How to Integrate:**

Add this code to your main app's user signup/registration:

```javascript
// When a user signs up in the Culinary R&D app
function onUserSignup(userData) {
    // Save to CRM
    const contactData = {
        name: userData.name,
        email: userData.email,
        contactType: 'app-user',
        platform: 'culinary-rd',
        source: 'culinary_app_signup',
        company: userData.company || '',
        role: userData.role || 'Chef',
        status: 'active',
        createdAt: new Date().toISOString(),
        trialEndDate: userData.trialEndDate || null
    };
    
    // Save to localStorage (for CRM to access)
    let crmContacts = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
    crmContacts.push(contactData);
    localStorage.setItem('crm_all_contacts', JSON.stringify(crmContacts));
    
    // Also save to Firestore if available
    if (window.firestoreSync) {
        window.firestoreSync.saveUser(contactData);
    }
}
```

**Add CRM Link:**

```html
<!-- Add to navigation menu -->
<a href="iterum-crm-unified.html" target="_blank">
    📊 View CRM Dashboard
</a>
```

---

### 2️⃣ Business Planner Integration

**Location:** `App-starting a business/restaurant-business-planner.html`

**How to Integrate:**

Add this code to capture business planner users:

```javascript
// When someone starts using the business planner
function onBusinessPlannerStart(userData) {
    const contactData = {
        name: userData.name,
        email: userData.email,
        contactType: 'lead',
        platform: 'business-planner',
        source: 'business_planner_signup',
        company: userData.restaurantName || '',
        role: 'Restaurant Entrepreneur',
        status: 'active',
        createdAt: new Date().toISOString(),
        planType: userData.planType || 'standard',
        businessStage: userData.stage || 'planning'
    };
    
    // Save to CRM
    let crmContacts = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
    crmContacts.push(contactData);
    localStorage.setItem('crm_all_contacts', JSON.stringify(crmContacts));
    
    console.log('✅ Contact saved to CRM from Business Planner');
}
```

**Add CRM Access:**

```html
<!-- Add to business planner dashboard -->
<button onclick="window.open('../../iterum-crm-unified.html', '_blank')"
        style="padding: 12px 24px; background: #10b981; color: white; border: none; border-radius: 8px; cursor: pointer;">
    📊 Open CRM
</button>
```

---

### 3️⃣ Payroll System Integration

**Location:** `payroll app/` (Python/Desktop App)

**How to Integrate:**

**Option A: Export CSV from Payroll → Import to CRM**

1. In your payroll app, add an export function:

```python
# In your payroll_app.py or enhanced_payroll_app.py
def export_employees_for_crm():
    """Export employee data in CRM-compatible format"""
    import csv
    import datetime
    
    # Get all employees
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees WHERE status = "active"').fetchall()
    
    # Create CSV
    filename = f'payroll_employees_{datetime.date.today()}.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'email', 'contactType', 'platform', 'role', 'status', 'company'])
        
        for emp in employees:
            writer.writerow([
                emp['name'],
                emp['email'] if emp['email'] else f"{emp['name'].replace(' ', '').lower()}@temp.com",
                'app-user',
                'payroll',
                emp['position'] or 'Employee',
                'active',
                'Your Restaurant'  # Replace with actual restaurant name
            ])
    
    print(f"✅ Exported {len(employees)} employees to {filename}")
    return filename
```

**Option B: Direct Integration (if using web interface)**

```html
<!-- Add to payroll web interface if you create one -->
<script>
function saveEmployeeToCRM(employeeData) {
    const contactData = {
        name: employeeData.name,
        email: employeeData.email,
        contactType: 'app-user',
        platform: 'payroll',
        source: 'payroll_system',
        company: employeeData.restaurant,
        role: employeeData.position,
        status: employeeData.status,
        createdAt: new Date().toISOString(),
        employeeId: employeeData.id
    };
    
    let crmContacts = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
    crmContacts.push(contactData);
    localStorage.setItem('crm_all_contacts', JSON.stringify(crmContacts));
}
</script>
```

**Add CRM Link to Payroll:**

Add a menu option in your payroll GUI to open the CRM in a browser:

```python
# In your payroll GUI
def open_crm():
    import webbrowser
    import os
    
    crm_path = os.path.abspath('../../iterum-crm-unified.html')
    webbrowser.open(f'file:///{crm_path}')
    print("✅ Opened CRM in browser")
```

---

### 4️⃣ Skills Portfolio Integration

**Location:** `Skills App/mobile-web/index.html`

**How to Integrate:**

Add this code to the Skills Portfolio app:

```javascript
// When a professional signs up for Skills Portfolio
function onProfessionalSignup(userData) {
    const contactData = {
        name: userData.name,
        email: userData.email,
        contactType: 'app-user',
        platform: 'skills-portfolio',
        source: 'skills_app_signup',
        company: userData.currentEmployer || '',
        role: userData.title || 'Culinary Professional',
        status: 'active',
        createdAt: new Date().toISOString(),
        skills: userData.skills || [],
        experienceYears: userData.years || 0
    };
    
    // Save to CRM
    let crmContacts = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
    crmContacts.push(contactData);
    localStorage.setItem('crm_all_contacts', JSON.stringify(crmContacts));
    
    // Sync to Firestore
    if (window.firestoreSync) {
        window.firestoreSync.saveUser(contactData);
    }
    
    console.log('✅ Professional saved to CRM');
}
```

**Add CRM Access:**

```html
<!-- Add to Skills App navigation -->
<div class="nav-item" onclick="window.open('../../iterum-crm-unified.html', '_blank')">
    <i class="fas fa-chart-bar"></i>
    <span>CRM Dashboard</span>
</div>
```

---

## 📊 Data Structure

All platforms should save contacts in this format:

```javascript
{
    name: "John Doe",                    // Required
    email: "john@example.com",           // Required
    contactType: "app-user",             // app-user, waitlist, trial, lead
    platform: "culinary-rd",             // culinary-rd, business-planner, payroll, skills-portfolio
    source: "culinary_app_signup",       // Specific source within platform
    company: "Doe's Restaurant",         // Optional
    role: "Executive Chef",              // Optional
    status: "active",                    // active, pending, expired, inactive
    createdAt: "2025-10-21T12:00:00Z",  // ISO 8601 timestamp
    // Platform-specific fields (optional)
    trialEndDate: "2025-11-05T...",     // For trial users
    planType: "professional",            // For business planner users
    employeeId: "EMP001",                // For payroll users
    skills: ["Pastry", "French"],       // For skills portfolio users
}
```

---

## 💾 Storage Architecture

The CRM uses multiple storage methods:

### 1. **localStorage** (Browser-based)
- Key: `crm_all_contacts`
- Format: JSON array
- Scope: Per-browser, instant access
- Use: Primary storage for quick access

### 2. **Firestore** (Cloud-based)
- Collection: `users`
- Document ID: user.email or user.id
- Scope: Cross-device, persistent
- Use: Backup and sync across devices

### 3. **CSV Export** (File-based)
- Format: Standard CSV
- Columns: name, email, contactType, platform, role, company, status, createdAt
- Use: Excel analysis, email marketing, backups

---

## 🔄 Data Flow

```
Platform (Signup/Action)
         ↓
  Save to localStorage
     (crm_all_contacts)
         ↓
  Optional: Save to Firestore
         ↓
  CRM reads from both sources
         ↓
  Display in unified dashboard
         ↓
  Export to CSV when needed
```

---

## 🛠️ Quick Setup Script

Add this universal script to **all platforms**:

```html
<!-- Add to every platform's HTML (at the bottom, before </body>) -->
<script>
// Universal CRM Integration Script
(function() {
    // Function to save contact to CRM
    window.saveToCRM = function(contactData) {
        try {
            // Ensure required fields
            if (!contactData.name || !contactData.email) {
                console.error('❌ CRM: name and email are required');
                return false;
            }
            
            // Set defaults
            contactData.contactType = contactData.contactType || 'lead';
            contactData.status = contactData.status || 'active';
            contactData.createdAt = contactData.createdAt || new Date().toISOString();
            contactData.id = contactData.id || `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            // Get existing contacts
            let allContacts = JSON.parse(localStorage.getItem('crm_all_contacts') || '[]');
            
            // Check for duplicate (by email)
            const existingIndex = allContacts.findIndex(c => c.email === contactData.email);
            if (existingIndex >= 0) {
                // Update existing
                allContacts[existingIndex] = { ...allContacts[existingIndex], ...contactData };
                console.log('✅ CRM: Updated existing contact');
            } else {
                // Add new
                allContacts.push(contactData);
                console.log('✅ CRM: Added new contact');
            }
            
            // Save back to localStorage
            localStorage.setItem('crm_all_contacts', JSON.stringify(allContacts));
            
            // Try to sync to Firestore (if available)
            if (window.firestoreSync) {
                window.firestoreSync.saveUser(contactData)
                    .then(() => console.log('☁️ CRM: Synced to cloud'))
                    .catch(err => console.warn('⚠️ CRM: Cloud sync failed', err));
            }
            
            return true;
        } catch (error) {
            console.error('❌ CRM save error:', error);
            return false;
        }
    };
    
    console.log('✅ CRM Integration Script Loaded');
})();
</script>
```

Then in your platform-specific code, just call:

```javascript
// Example: In any platform
window.saveToCRM({
    name: "Jane Smith",
    email: "jane@example.com",
    platform: "culinary-rd",  // or "business-planner", "payroll", "skills-portfolio"
    source: "recipe_developer_signup",
    company: "Smith's Bistro",
    role: "Sous Chef"
});
```

---

## 📋 Integration Checklist

### For Each Platform:

- [ ] Add universal CRM integration script
- [ ] Call `window.saveToCRM()` on user signup
- [ ] Call `window.saveToCRM()` on important actions (trial start, subscription, etc.)
- [ ] Add "Open CRM" link/button to admin sections
- [ ] Test data flow: signup → CRM → verify in dashboard
- [ ] Document platform-specific contact fields
- [ ] Set up proper platform identifier

### Global Setup:

- [ ] Test CRM opens from all platforms
- [ ] Verify Firebase/Firestore connection
- [ ] Test CSV export functionality
- [ ] Set up regular backups
- [ ] Document admin access procedures
- [ ] Train team on CRM usage

---

## 🎯 Usage Examples

### **Example 1: Capturing Recipe Developer Signup**

```javascript
// In index.html (Culinary R&D Platform)
async function handleSignUp(event) {
    event.preventDefault();
    
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    
    // ... your existing signup code ...
    
    // Save to CRM
    window.saveToCRM({
        name: name,
        email: email,
        platform: 'culinary-rd',
        source: 'recipe_developer_signup',
        contactType: 'trial',
        role: 'Recipe Developer',
        trialEndDate: new Date(Date.now() + 14*24*60*60*1000).toISOString()
    });
}
```

### **Example 2: Capturing Business Plan Creation**

```javascript
// In restaurant-business-planner.html
function onBusinessPlanCreated(planData) {
    window.saveToCRM({
        name: planData.ownerName,
        email: planData.email,
        platform: 'business-planner',
        source: 'business_plan_created',
        contactType: 'lead',
        company: planData.restaurantName,
        role: 'Restaurant Owner',
        businessStage: 'planning',
        planType: planData.cuisineType
    });
}
```

### **Example 3: Capturing Employee Addition (Payroll)**

```python
# In your payroll app
def add_employee(name, email, position, restaurant):
    # ... your existing employee add code ...
    
    # Export to JSON for CRM pickup
    import json
    crm_data = {
        'name': name,
        'email': email or f"{name.replace(' ', '').lower()}@{restaurant}.com",
        'platform': 'payroll',
        'source': 'employee_added',
        'contactType': 'app-user',
        'company': restaurant,
        'role': position,
        'status': 'active',
        'createdAt': datetime.datetime.now().isoformat()
    }
    
    # Save to a JSON file that CRM can read
    with open('crm_sync/payroll_contacts.json', 'a') as f:
        f.write(json.dumps(crm_data) + '\n')
```

---

## 📁 File Structure

```
Iterum Innovation/
├── iterum-crm-unified.html              ⭐ Main CRM
├── UNIFIED-CRM-INTEGRATION-GUIDE.md     📚 This guide
├── OPEN-CRM.bat                         🚀 Quick launcher
│
├── index.html                           (Culinary R&D Platform)
├── App-starting a business/
│   └── restaurant-business-planner.html (Business Planner)
├── payroll app/
│   └── dist/
│       └── PayrollApp.exe               (Payroll System)
└── Skills App/
    └── mobile-web/
        └── index.html                   (Skills Portfolio)
```

---

## 🚀 Quick Actions

### **Create Quick Launcher**

Save this as `OPEN-CRM.bat`:

```batch
@echo off
echo Opening Iterum Foods Unified CRM...
start iterum-crm-unified.html
echo CRM opened in your default browser!
pause
```

### **Create Desktop Shortcut**

1. Right-click on `iterum-crm-unified.html`
2. Send to → Desktop (create shortcut)
3. Rename to "Iterum CRM"
4. Change icon (optional)

---

## 📊 Monitoring & Analytics

### **Key Metrics to Track:**

1. **Total Contacts** - Overall growth across all platforms
2. **Platform Distribution** - Which platform brings most users
3. **Conversion Rates** - Waitlist → Active users
4. **Trial Status** - Active trials, expired trials
5. **Weekly Growth** - New contacts per week
6. **Platform Engagement** - Active users per platform

### **Regular Tasks:**

- **Daily:** Check new contacts from each platform
- **Weekly:** Export CSV for analysis
- **Monthly:** Review conversion rates
- **Quarterly:** Clean up inactive/duplicate contacts

---

## 🐛 Troubleshooting

### **Issue: Contacts not showing in CRM**

**Solution:**
1. Check localStorage: Open DevTools → Application → Local Storage → `crm_all_contacts`
2. Verify `window.saveToCRM()` is being called
3. Check browser console for errors
4. Try manual entry to test CRM functionality

### **Issue: Platform launcher not working**

**Solution:**
1. Check file paths are correct (relative to CRM location)
2. Verify files exist at specified paths
3. Use browser's developer tools to see navigation errors
4. Try absolute paths if relative paths fail

### **Issue: Firestore sync not working**

**Solution:**
1. Check Firebase config in `assets/js/firebase-config.js`
2. Verify Firestore is enabled in Firebase Console
3. Check browser console for Firestore errors
4. Fallback to localStorage-only mode if needed

---

## 💡 Best Practices

1. **Consistent Data Format** - Use the same field names across all platforms
2. **Unique Identifiers** - Use email as primary unique identifier
3. **Platform Tags** - Always include platform source
4. **Regular Backups** - Export CSV weekly
5. **Data Quality** - Validate email addresses before saving
6. **Privacy** - Don't store sensitive data in CRM (passwords, payment info)
7. **Sync Strategy** - Save to localStorage first, then Firestore
8. **Error Handling** - Gracefully handle storage failures

---

## 🎉 Next Steps

1. ✅ Add universal CRM script to each platform
2. ✅ Test contact capture from each platform
3. ✅ Verify CRM displays contacts correctly
4. ✅ Set up regular backup routine
5. ✅ Train team on CRM usage
6. ✅ Monitor metrics weekly

---

**Your Unified CRM is ready to serve all 4 platforms!** 🚀

For questions or issues, refer to this guide or check the browser console for debugging information.

**Last Updated:** October 21, 2025  
**Version:** 1.0.0

