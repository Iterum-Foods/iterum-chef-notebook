# Iterum Design System

## 🎨 **Brand Foundation**

### **Brand Values**
- **Innovation**: Pushing culinary boundaries
- **Precision**: Exact measurements and techniques
- **Sustainability**: Eco-conscious food practices
- **Community**: Connecting food professionals

### **Brand Personality**
- **Professional**: Expert-level culinary tools
- **Approachable**: Easy to use for all skill levels
- **Reliable**: Consistent, dependable performance
- **Inspiring**: Encourages culinary creativity

## 🎨 **Visual Identity**

### **Primary Logo**
```
🍃 Iterum R&D
```
- **Usage**: Primary brand identifier
- **Clear Space**: Minimum 1x logo height on all sides
- **Minimum Size**: 24px height for digital, 0.5" for print

### **Logo Variations**
- **Full Logo**: 🍃 Iterum R&D Chef Notebook
- **Icon Only**: 🍃 (for small spaces)
- **Text Only**: Iterum R&D (when icon doesn't work)

### **Logo Guidelines**
- ✅ Use on light backgrounds
- ✅ Maintain aspect ratio
- ✅ Ensure minimum size requirements
- ❌ Don't stretch or distort
- ❌ Don't add effects or shadows
- ❌ Don't change colors

## 🌈 **Color Palette**

### **Primary Colors**
```css
--iterum-primary: #10b981    /* Main brand green */
--iterum-secondary: #059669   /* Darker green for emphasis */
--iterum-accent: #7c3aed     /* Purple for highlights */
--iterum-dark: #064e3b       /* Deep green for text */
--iterum-light: #ecfdf5      /* Light green for backgrounds */
--iterum-warm: #fef3c7       /* Warm yellow for accents */
--iterum-orange: #f97316     /* Orange for calls-to-action */
```

### **Semantic Colors**
```css
--success-50: #f0fdf4        /* Light success */
--success-500: #22c55e       /* Success */
--success-700: #15803d       /* Dark success */

--error-50: #fef2f2          /* Light error */
--error-500: #ef4444         /* Error */
--error-700: #b91c1c         /* Dark error */

--warning-50: #fffbeb         /* Light warning */
--warning-500: #f59e0b       /* Warning */
--warning-700: #b45309       /* Dark warning */

--info-50: #eff6ff           /* Light info */
--info-500: #3b82f6          /* Info */
--info-700: #1d4ed8          /* Dark info */
```

### **Neutral Colors**
```css
--gray-50: #f9fafb           /* Lightest gray */
--gray-100: #f3f4f6          /* Very light gray */
--gray-200: #e5e7eb          /* Light gray */
--gray-300: #d1d5db          /* Medium light gray */
--gray-400: #9ca3af          /* Medium gray */
--gray-500: #6b7280          /* True gray */
--gray-600: #4b5563          /* Medium dark gray */
--gray-700: #374151          /* Dark gray */
--gray-800: #1f2937          /* Very dark gray */
--gray-900: #111827          /* Darkest gray */
```

### **Color Usage Guidelines**
- **Primary**: Main actions, links, brand elements
- **Secondary**: Supporting elements, borders
- **Accent**: Highlights, special features
- **Success**: Positive actions, confirmations
- **Error**: Destructive actions, warnings
- **Warning**: Caution, attention needed
- **Info**: Information, help text

## 🔤 **Typography**

### **Font Family**
```css
--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### **Font Weights**
```css
--font-weight-light: 300      /* Light text */
--font-weight-normal: 400     /* Body text */
--font-weight-medium: 500     /* Medium emphasis */
--font-weight-semibold: 600   /* Semi-bold headings */
--font-weight-bold: 700       /* Bold headings */
--font-weight-extrabold: 800  /* Extra bold */
```

### **Type Scale**
```css
--font-size-xs: 0.75rem      /* 12px - Captions */
--font-size-sm: 0.875rem     /* 14px - Small text */
--font-size-base: 1rem       /* 16px - Body text */
--font-size-lg: 1.125rem     /* 18px - Large body */
--font-size-xl: 1.25rem      /* 20px - Small headings */
--font-size-2xl: 1.5rem      /* 24px - Subheadings */
--font-size-3xl: 1.875rem    /* 30px - Headings */
--font-size-4xl: 2.25rem     /* 36px - Large headings */
--font-size-5xl: 3rem        /* 48px - Hero text */
```

### **Typography Guidelines**
- **Headings**: Use Inter font, weight 600-700
- **Body Text**: Use Inter font, weight 400-500
- **Captions**: Use Inter font, weight 300-400
- **Line Height**: 1.5 for body text, 1.2 for headings
- **Letter Spacing**: -0.025em for headings, normal for body

## 📏 **Spacing System**

### **4px Grid System**
```css
--space-1: 0.25rem           /* 4px */
--space-2: 0.5rem            /* 8px */
--space-3: 0.75rem           /* 12px */
--space-4: 1rem              /* 16px */
--space-5: 1.25rem           /* 20px */
--space-6: 1.5rem            /* 24px */
--space-8: 2rem              /* 32px */
--space-10: 2.5rem           /* 40px */
--space-12: 3rem             /* 48px */
--space-16: 4rem             /* 64px */
--space-20: 5rem             /* 80px */
--space-24: 6rem             /* 96px */
```

### **Spacing Guidelines**
- **Component Padding**: Use space-4, space-6, space-8
- **Section Margins**: Use space-8, space-12, space-16
- **Element Gaps**: Use space-2, space-3, space-4
- **Page Margins**: Use space-6, space-8 on mobile, space-12, space-16 on desktop

## 🎭 **Component Library**

### **Buttons**
```css
/* Base Button */
.iterum-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
  cursor: pointer;
  border: none;
  outline: none;
}

/* Button Variants */
.iterum-button-primary {
  background-color: var(--iterum-primary);
  color: white;
}

.iterum-button-secondary {
  background-color: var(--gray-100);
  color: var(--gray-700);
}

.iterum-button-outline {
  background-color: transparent;
  border: 2px solid var(--iterum-primary);
  color: var(--iterum-primary);
}

.iterum-button-ghost {
  background-color: transparent;
  color: var(--gray-600);
}

.iterum-button-danger {
  background-color: var(--error-500);
  color: white;
}

/* Button Sizes */
.iterum-button-sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-sm);
}

.iterum-button-md {
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-base);
}

.iterum-button-lg {
  padding: var(--space-4) var(--space-6);
  font-size: var(--font-size-lg);
}
```

### **Form Elements**
```css
/* Input Fields */
.iterum-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  transition: border-color var(--transition-fast);
}

.iterum-input:focus {
  outline: none;
  border-color: var(--iterum-primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

/* Textareas */
.iterum-textarea {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
}

/* Select Dropdowns */
.iterum-select {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  background-color: white;
  cursor: pointer;
}
```

### **Cards**
```css
/* Base Card */
.iterum-card {
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--gray-200);
  overflow: hidden;
}

/* Card Variants */
.iterum-card-elevated {
  box-shadow: var(--shadow-lg);
}

.iterum-card-bordered {
  border: 2px solid var(--gray-200);
}

.iterum-card-interactive {
  transition: all var(--transition-normal);
  cursor: pointer;
}

.iterum-card-interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}
```

### **Navigation**
```css
/* Navigation Links */
.iterum-nav-link {
  color: var(--gray-600);
  text-decoration: none;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.iterum-nav-link:hover {
  color: var(--iterum-primary);
  background-color: var(--iterum-light);
}

.iterum-nav-link.active {
  color: var(--iterum-primary);
  background-color: var(--iterum-light);
  font-weight: var(--font-weight-medium);
}

/* Navigation Container */
.iterum-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}
```

### **Loading States**
```css
/* Spinner */
.iterum-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--gray-200);
  border-top: 3px solid var(--iterum-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Skeleton Loading */
.iterum-skeleton {
  background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Loading States */
.iterum-loading {
  opacity: 0.6;
  pointer-events: none;
}

.iterum-loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid var(--gray-300);
  border-top: 2px solid var(--iterum-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

## 🎬 **Animation & Transitions**

### **Transition Speeds**
```css
--transition-fast: 150ms      /* Quick interactions */
--transition-normal: 300ms    /* Standard transitions */
--transition-slow: 500ms      /* Slow, deliberate movements */
```

### **Easing Functions**
```css
--transition-ease: cubic-bezier(0.4, 0, 0.2, 1)      /* Standard ease */
--transition-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55)  /* Bouncy */
--transition-sharp: cubic-bezier(0.4, 0, 0.6, 1)      /* Sharp, precise */
```

### **Keyframe Animations**
```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.iterum-fade-in {
  animation: fadeIn var(--transition-normal) var(--transition-ease);
}

/* Slide Up */
@keyframes slideUp {
  from { 
    transform: translateY(20px);
    opacity: 0;
  }
  to { 
    transform: translateY(0);
    opacity: 1;
  }
}

.iterum-slide-up {
  animation: slideUp var(--transition-normal) var(--transition-ease);
}

/* Bounce Gentle */
@keyframes bounceGentle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.iterum-bounce-gentle {
  animation: bounceGentle 0.6s var(--transition-bounce);
}
```

## 🎯 **Interactive States**

### **Hover States**
- **Buttons**: Slight scale (1.02) and shadow increase
- **Cards**: Lift effect with shadow increase
- **Links**: Color change and underline
- **Form Elements**: Border color change and focus ring

### **Focus States**
- **Focus Ring**: 3px ring with primary color at 10% opacity
- **Focus Visible**: Always show focus indicators
- **Keyboard Navigation**: Clear visual feedback

### **Active States**
- **Buttons**: Scale down (0.98) and shadow decrease
- **Form Elements**: Border color darkening
- **Interactive Elements**: Immediate visual feedback

### **Disabled States**
- **Opacity**: 0.5 for disabled elements
- **Cursor**: Not-allowed for disabled buttons
- **Color**: Muted gray tones
- **Interaction**: No hover or focus effects

## 📱 **Responsive Design**

### **Breakpoints**
```css
/* Mobile First Approach */
--breakpoint-sm: 640px       /* Small devices */
--breakpoint-md: 768px       /* Medium devices */
--breakpoint-lg: 1024px      /* Large devices */
--breakpoint-xl: 1280px      /* Extra large devices */
--breakpoint-2xl: 1536px     /* 2X large devices */
```

### **Responsive Guidelines**
- **Mobile First**: Design for mobile, enhance for larger screens
- **Touch Friendly**: Minimum 44px touch targets
- **Content Priority**: Most important content first
- **Performance**: Optimize for slower connections

### **Grid System**
```css
/* Responsive Grid */
.iterum-grid {
  display: grid;
  gap: var(--space-6);
}

.iterum-grid-1 { grid-template-columns: 1fr; }
.iterum-grid-2 { grid-template-columns: repeat(2, 1fr); }
.iterum-grid-3 { grid-template-columns: repeat(3, 1fr); }
.iterum-grid-4 { grid-template-columns: repeat(4, 1fr); }

/* Responsive Breakpoints */
@media (min-width: 768px) {
  .iterum-grid-2-md { grid-template-columns: repeat(2, 1fr); }
  .iterum-grid-3-md { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
  .iterum-grid-4-lg { grid-template-columns: repeat(4, 1fr); }
}
```

## ♿ **Accessibility**

### **Color Contrast**
- **Normal Text**: Minimum 4.5:1 contrast ratio
- **Large Text**: Minimum 3:1 contrast ratio
- **UI Elements**: Minimum 3:1 contrast ratio

### **Focus Management**
- **Visible Focus**: Always show focus indicators
- **Logical Tab Order**: Natural keyboard navigation
- **Skip Links**: Quick access to main content

### **Screen Reader Support**
- **Semantic HTML**: Proper heading structure
- **Alt Text**: Descriptive image alternatives
- **ARIA Labels**: Enhanced screen reader support
- **Live Regions**: Dynamic content announcements

### **Keyboard Navigation**
- **Tab Order**: Logical element sequence
- **Enter/Space**: Activate interactive elements
- **Arrow Keys**: Navigate within components
- **Escape**: Close modals and menus

## 🔧 **Implementation Guidelines**

### **CSS Custom Properties**
```css
/* Use CSS variables for all design tokens */
.button {
  background-color: var(--iterum-primary);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
}
```

### **Component Classes**
```css
/* Use consistent class naming */
.iterum-button.iterum-button-primary.iterum-button-lg
.iterum-card.iterum-card-elevated
.iterum-input.iterum-input-error
```

### **Utility Classes**
```css
/* Common utility classes */
.iterum-text-center { text-align: center; }
.iterum-mt-4 { margin-top: var(--space-4); }
.iterum-p-6 { padding: var(--space-6); }
.iterum-rounded-lg { border-radius: var(--radius-lg); }
```

### **State Modifiers**
```css
/* State-based styling */
.iterum-button:disabled { opacity: 0.5; }
.iterum-input:focus { border-color: var(--iterum-primary); }
.iterum-card:hover { transform: translateY(-2px); }
```

## 📚 **Documentation & Maintenance**

### **Component Documentation**
- **Usage Examples**: Code snippets for each component
- **Props/Props**: Available options and variations
- **Accessibility Notes**: Screen reader and keyboard support
- **Browser Support**: Compatible browsers and versions

### **Design Tokens**
- **Centralized Values**: Single source of truth for all design values
- **Version Control**: Track changes to design tokens
- **Migration Guides**: Help teams update to new versions
- **Breaking Changes**: Clear communication of updates

### **Quality Assurance**
- **Visual Testing**: Automated visual regression testing
- **Accessibility Testing**: Automated accessibility checks
- **Performance Testing**: Monitor impact on performance
- **Cross-browser Testing**: Ensure consistent experience

## 🚀 **Getting Started**

### **1. Install Design System**
```html
<link rel="stylesheet" href="assets/css/iterum-design-system.css">
```

### **2. Use Component Classes**
```html
<button class="iterum-button iterum-button-primary iterum-button-lg">
  Create Recipe
</button>
```

### **3. Apply Design Tokens**
```css
.my-component {
  color: var(--iterum-primary);
  padding: var(--space-6);
  border-radius: var(--radius-lg);
}
```

### **4. Follow Guidelines**
- Use established component classes
- Maintain consistent spacing
- Follow accessibility standards
- Test across devices and browsers

---

*This design system ensures consistency, accessibility, and maintainability across your entire Iterum application ecosystem.*
