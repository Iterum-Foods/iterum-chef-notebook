# 🎨 Iterum Culinary App - Master Brand Kit Guide

## 📍 Single Source of Truth

**File:** `assets/css/iterum-brand-kit.css`

This is the **ONLY** place you need to edit to change branding across the entire app!

---

## 🎯 How to Use

### ✅ To Change Any Branding Element:

1. Open `assets/css/iterum-brand-kit.css`
2. Edit the CSS variables at the top
3. Save the file
4. Deploy: `firebase deploy --only hosting`
5. **Done!** All 25+ pages update automatically

---

## 🎨 What You Can Change

### **Background Colors**
```css
--brand-bg-primary: #3D3426;        /* Main page background */
--brand-bg-secondary: #2A2420;      /* Secondary background */
--brand-bg-tertiary: #1F1D1A;       /* Darkest background */
```

**Change these to instantly update all page backgrounds!**

---

### **Card/Container Colors**
```css
--brand-card-bg: linear-gradient(145deg, #4A4136 0%, #3D3729 100%);
--brand-card-bg-elevated: linear-gradient(145deg, #5A5045 0%, #4D453A 100%);
--brand-card-bg-subtle: linear-gradient(145deg, #3D3729 0%, #35301E 100%);
```

**Change these to update all cards, panels, and containers!**

---

### **Border Colors**
```css
--brand-border-light: #6B5D47;      /* Light borders */
--brand-border-medium: #5C4D39;     /* Medium borders */
--brand-border-dark: #4A3F2F;       /* Dark borders */
```

**Change these to update all borders, dividers, and outlines!**

---

### **Text Colors**
```css
--brand-text-primary: #FFFFFF;      /* Headings */
--brand-text-secondary: #F5F2EB;    /* Body text */
--brand-text-tertiary: #E8E4D8;     /* Labels */
--brand-text-muted: #D8D4CC;        /* Secondary text */
```

**Change these to update all text colors everywhere!**

---

### **Accent Colors**
```css
--brand-accent-primary: #C9954B;    /* Golden brown - buttons, links */
--brand-accent-secondary: #A85D3A;  /* Terracotta - secondary actions */
--brand-accent-forest: #5B7A5F;     /* Forest green - nature elements */
```

**Change these to update all hover states, highlights, and focus colors!**

---

### **Button Colors**
```css
--brand-btn-primary: linear-gradient(135deg, #5B7A5F 0%, #384D3D 100%);
--brand-btn-secondary: linear-gradient(135deg, #A85D3A 0%, #8B4D2D 100%);
--brand-btn-accent: linear-gradient(135deg, #C9954B 0%, #A67C3D 100%);
```

**Change these to update all button gradients!**

---

### **Header/Navigation Colors**
```css
--brand-header-bg: linear-gradient(135deg, #0F0E0C 0%, #1A1512 100%);
--brand-header-border: rgba(201, 149, 75, 0.5);
--brand-header-text: #FFFFFF;
--brand-header-hover: rgba(201, 149, 75, 0.3);
```

**Change these to update the navigation header across all pages!**

---

### **Spacing**
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
```

**Change these to update padding/margins everywhere!**

---

### **Typography**
```css
--font-family-primary: 'Inter', sans-serif;
--font-size-base: 1rem;
--font-weight-bold: 700;
```

**Change these to update fonts, sizes, and weights everywhere!**

---

### **Shadows**
```css
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
--shadow-md: 0 8px 32px rgba(0, 0, 0, 0.5);
--shadow-lg: 0 12px 48px rgba(0, 0, 0, 0.6);
```

**Change these to update all drop shadows!**

---

### **Border Radius**
```css
--radius-sm: 6px;
--radius-md: 10px;
--radius-lg: 14px;
--radius-xl: 20px;
```

**Change these to update how rounded everything is!**

---

## 💡 Example: Change to Light Theme

Want to switch to a light theme? Just change these in `iterum-brand-kit.css`:

```css
/* Change backgrounds to light */
--brand-bg-primary: #F5F2EB;        /* Light cream */
--brand-bg-secondary: #E8E4D8;      /* Lighter cream */
--brand-bg-tertiary: #FFFFFF;       /* White */

/* Change cards to white */
--brand-card-bg: linear-gradient(145deg, #FFFFFF 0%, #F5F2EB 100%);

/* Change text to dark */
--brand-text-primary: #1F1D1A;      /* Dark for headings */
--brand-text-secondary: #2A2420;    /* Dark for body */
```

Save → Deploy → **Entire app is now light theme!**

---

## 💡 Example: Change to Blue Theme

Want a blue theme instead of brown?

```css
/* Change to blue backgrounds */
--brand-bg-primary: #2D3748;        /* Dark blue */
--brand-bg-secondary: #1A202C;      /* Darker blue */
--brand-bg-tertiary: #0F1419;       /* Almost black blue */

/* Change cards to blue */
--brand-card-bg: linear-gradient(145deg, #3D4E5C 0%, #2D3748 100%);

/* Change accents to bright blue */
--brand-accent-primary: #3B82F6;    /* Bright blue */
--brand-accent-secondary: #2563EB;  /* Deep blue */
```

Save → Deploy → **Entire app is now blue theme!**

---

## 🚀 Pages Using the Brand Kit

All 25+ application pages automatically use the brand kit:

✅ index.html (Dashboard)
✅ recipe-library.html
✅ recipe-developer.html
✅ menu-builder.html
✅ ingredients.html
✅ vendor-management.html
✅ equipment-management.html
✅ kitchen-management.html
✅ chef-dashboard.html
✅ inventory.html
✅ production-planning.html
✅ ingredient-highlights.html
✅ server-info-sheet.html
✅ audit-log.html
✅ recipe-upload.html
✅ bulk-recipe-import.html
✅ bulk-ingredient-import.html
✅ price-list-upload.html
✅ recipe-photo-studio.html
✅ project-hub.html
✅ data-backup-center.html
✅ data-management-dashboard.html
✅ user-profile.html
✅ vendor-price-comparison.html
✅ find-89-charles-project.html

---

## 🎯 Benefits of the Brand Kit

✅ **Change Once, Update Everywhere** - Edit one file, all pages update
✅ **Consistent Design** - All pages use exact same colors/spacing
✅ **Easy Theming** - Switch themes by changing a few variables
✅ **No Inline Styles** - Clean, maintainable code
✅ **Faster Development** - No need to hunt for colors/sizes
✅ **Easy Customization** - Client wants different colors? 5 minutes!

---

## 📝 Quick Reference

**To change:**
- **Page backgrounds** → Edit `--brand-bg-*`
- **Cards/containers** → Edit `--brand-card-*`
- **Text colors** → Edit `--brand-text-*`
- **Borders** → Edit `--brand-border-*`
- **Buttons** → Edit `--brand-btn-*`
- **Accents/highlights** → Edit `--brand-accent-*`
- **Header/nav** → Edit `--brand-header-*`
- **Spacing** → Edit `--space-*`
- **Fonts** → Edit `--font-*`
- **Shadows** → Edit `--shadow-*`
- **Roundness** → Edit `--radius-*`

---

## 🔥 Pro Tips

1. **Test Changes Locally First** - Use browser dev tools to test color changes before deploying
2. **Use CSS Variables** - When adding new styles, use the brand kit variables
3. **Don't Use Inline Styles** - Always use classes or the brand kit variables
4. **Document Changes** - Update this guide if you add new variables
5. **Keep Backups** - Save a copy of the brand kit before major changes

---

## 🎨 Your Brand, Your Way

The brand kit is designed to be flexible. You can:
- Create seasonal themes (winter, spring, summer, fall)
- Create client-specific themes
- A/B test different color schemes
- Quickly rebrand the entire app

**All by editing ONE file!**

---

**Last Updated:** 2025-10-19
**Version:** 1.0

