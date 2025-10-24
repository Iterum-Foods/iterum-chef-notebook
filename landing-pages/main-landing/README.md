# 🚀 Iterum Foods - Main Landing Pages

## Complete Unified System with Waitlist & CRM Integration

This folder contains the **production-ready landing pages** for iterumfoods.xyz with unified branding, multi-platform waitlists, and full CRM integration.

---

## 📁 Files in This Folder

### **Landing Pages:**
1. **`index.html`** ⭐ Main homepage
   - Showcases all 4 platforms
   - Hero section with CTAs
   - Stats section
   - Platform cards
   - Footer

2. **`culinary-rd.html`** 🍽️ Culinary R&D Platform
   - Recipe development features
   - Menu planning tools
   - Cost analysis capabilities
   - Green branding

3. **`business-planner.html`** 📊 Business Planner
   - Business planning features
   - Financial projections
   - Market analysis
   - Blue branding

4. **`payroll.html`** 💰 Payroll System
   - Time tracking features
   - Tip management
   - Schedule tools
   - Orange branding

5. **`skills-portfolio.html`** 🎯 Skills Portfolio
   - Professional networking
   - Video portfolio
   - Skill validation
   - Purple branding

### **Shared Resources:**
6. **`shared-styles.css`** 🎨 Unified branding stylesheet
7. **`shared-scripts.js`** ⚡ Waitlist & CRM integration

---

## 🎨 Unified Branding

All pages share:
- ✅ Same navigation structure
- ✅ Same fonts (Inter)
- ✅ Same button styles
- ✅ Same form designs
- ✅ Same modal popups
- ✅ Same animations
- ✅ Platform-specific colors

**Color System:**
- Main Brand: Green (#10b981)
- Culinary: Green (#10b981)
- Business: Blue (#3b82f6)
- Payroll: Orange (#f59e0b)
- Skills: Purple (#8b5cf6)

---

## 📋 Waitlist Integration

### **How It Works:**

Every page has "Join Waitlist" buttons that:
1. Open modal popup
2. Collect contact information
3. Save to 3 places:
   - Main waitlist
   - Platform-specific waitlist
   - CRM contacts
4. Track with Google Analytics
5. Show success message with position number

### **Waitlist Data Saved To:**

**localStorage Keys:**
- `iterum_main_waitlist` - Main waitlist
- `iterum_waitlist_culinary` - Culinary signups
- `iterum_waitlist_business` - Business signups
- `iterum_waitlist_payroll` - Payroll signups
- `iterum_waitlist_skills` - Skills signups
- `crm_all_contacts` - CRM integration

### **Form Fields:**
- Name (required)
- Email (required)
- Phone (optional)
- Company (optional)
- Role (dropdown)
- Source (dropdown - how they heard about you)

---

## 🎯 Platform Configurations

Each page has a `PLATFORM_CONFIG` that identifies it:

```javascript
// culinary-rd.html
const PLATFORM_CONFIG = {
    name: 'Culinary R&D',
    code: 'culinary',
    icon: '🍽️'
};

// business-planner.html
const PLATFORM_CONFIG = {
    name: 'Business Planner',
    code: 'business',
    icon: '📊'
};

// payroll.html
const PLATFORM_CONFIG = {
    name: 'Payroll System',
    code: 'payroll',
    icon: '💰'
};

// skills-portfolio.html
const PLATFORM_CONFIG = {
    name: 'Skills Portfolio',
    code: 'skills',
    icon: '🎯'
};
```

This tells the waitlist script which platform the signup is for.

---

## 🚀 Deployment

### **Option 1: Deploy All Pages**

Upload entire folder to web server:
```
iterumfoods.xyz/
├── index.html              (from main-landing/index.html)
├── culinary/
│   └── index.html         (from culinary-rd.html)
├── business/
│   └── index.html         (from business-planner.html)
├── payroll/
│   └── index.html         (from payroll.html)
├── skills/
│   └── index.html         (from skills-portfolio.html)
├── shared-styles.css      (from shared-styles.css)
└── shared-scripts.js      (from shared-scripts.js)
```

### **Option 2: Firebase Hosting**

```bash
cd landing-pages/main-landing
firebase init hosting
firebase deploy
```

### **Option 3: Netlify**

```bash
cd landing-pages/main-landing
netlify deploy --prod
```

---

## 🔧 Customization

### **Update Contact Info:**

Edit all HTML files, find and replace:
- `hello@iterumfoods.xyz` → Your email
- `(555) 123-4567` → Your phone

### **Update Colors:**

Edit `shared-styles.css`:
```css
:root {
    --primary: #10b981;        /* Your primary color */
    --primary-dark: #059669;   /* Darker shade */
}
```

### **Update Google Analytics:**

Edit each HTML file, find:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-MC8Q3SZ47K"></script>
```
Replace `G-MC8Q3SZ47K` with your GA ID.

---

## 📊 Viewing Waitlist Data

### **Admin Tools:**

**Master Waitlist Manager:**
- File: `../../iterum-master-waitlist.html`
- Shows: All waitlists combined
- Actions: View, email, convert, export

**Ultimate CRM:**
- File: `../../iterum-crm-ultimate.html`
- Shows: All contacts including waitlist
- Actions: Full contact management

### **Console Commands:**

Open browser DevTools (F12) and type:
```javascript
// View all waitlist data
viewWaitlistData()

// Export to CSV
exportWaitlistCSV()
```

---

## 🧪 Testing

### **Test Waitlist Signup:**

1. Open `index.html` in browser
2. Click "Join Waitlist" button
3. Fill out form with test data
4. Submit
5. Check success message
6. Open Master Waitlist Manager
7. Verify test signup appears

### **Test Platform-Specific:**

1. Open `culinary-rd.html`
2. Click "Join Waitlist"
3. Submit form
4. Open Master Waitlist Manager
5. Filter to "Culinary" tab
6. Verify signup appears

---

## 📱 Mobile Optimization

All pages are fully responsive:
- ✅ Mobile navigation (hamburger menu on small screens)
- ✅ Touch-friendly buttons (min 44px)
- ✅ Readable text sizes
- ✅ Proper viewport settings
- ✅ Fast loading on mobile

Test on:
- iPhone (Safari)
- Android (Chrome)
- iPad/Tablet

---

## 🔐 Security Notes

**Public Pages:**
- All landing pages are public
- Waitlist forms are open to all
- No sensitive data collected

**Admin Pages:**
- Master Waitlist Manager should be protected
- CRM should be admin-only
- Recommendation: Add authentication

**Data Storage:**
- localStorage (browser-based, per-device)
- Firestore (optional cloud backup)
- CSV export (for backups)

---

## 📈 Success Metrics

Track these KPIs:
- Total waitlist signups
- Signups per platform
- Conversion rate (goal: 20%)
- Average time to convert (goal: < 14 days)
- Source attribution
- Geographic distribution

---

## 💡 Best Practices

1. **Daily:** Check Master Waitlist for new signups
2. **Daily:** Respond to high-priority contacts within 24 hours
3. **Weekly:** Export waitlist to CSV for backup
4. **Weekly:** Convert ready contacts to active users
5. **Monthly:** Analyze conversion rates and optimize

---

## 🎉 Summary

This folder contains a **complete, production-ready** landing page system with:

- ✅ 5 pages with unified branding
- ✅ 5 separate waitlists
- ✅ Automatic CRM integration
- ✅ Google Analytics tracking
- ✅ Mobile responsive design
- ✅ Export tools
- ✅ Admin management tools

**Ready to deploy to iterumfoods.xyz!** 🚀

---

**Questions?** Check the main documentation: `../../🎯 UNIFIED-SYSTEM-COMPLETE.md`

**Created:** October 21, 2025  
**Version:** 1.0.0

