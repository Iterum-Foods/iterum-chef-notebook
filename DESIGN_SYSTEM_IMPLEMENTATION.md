# Design System Implementation Guide

## Overview
This guide provides step-by-step instructions for implementing the Iterum Design System across your application to ensure consistency and maintainability.

## Phase 1: Foundation Setup ✅

### 1.1 Tailwind Configuration ✅
- [x] Created `tailwind.config.js` with design system colors
- [x] Added Iterum brand colors and semantic colors
- [x] Configured custom spacing and animations

### 1.2 CSS Design System ✅
- [x] Created `assets/css/iterum-design-system.css`
- [x] Implemented CSS custom properties (design tokens)
- [x] Built component library (buttons, forms, cards, etc.)

### 1.3 Landing Page Updates ✅
- [x] Replaced conflicting CSS variables with design system
- [x] Updated button styles to use design system classes
- [x] Standardized color usage

## Phase 2: Button Standardization (Current)

### 2.1 Button Class Mapping
Replace all custom button styles with design system classes:

```html
<!-- BEFORE: Custom button styling -->
<button class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg">

<!-- AFTER: Design system button -->
<button class="iterum-button iterum-button-primary">
```

### 2.2 Button Variants by Function
- **Primary Actions**: `iterum-button iterum-button-primary`
- **Secondary Actions**: `iterum-button iterum-button-secondary`
- **Danger Actions**: `iterum-button iterum-button-danger`
- **Outline Actions**: `iterum-button iterum-button-outline`
- **Ghost Actions**: `iterum-button iterum-button-ghost`

### 2.3 Button Sizes
- **Small**: `iterum-button-sm` (12px text, compact padding)
- **Medium**: Default size (14px text, standard padding)
- **Large**: `iterum-button-lg` (16px text, generous padding)
- **Extra Large**: `iterum-button-xl` (18px text, maximum padding)

## Phase 3: Form Element Standardization

### 3.1 Input Fields
```html
<!-- BEFORE: Custom input styling -->
<input class="w-full px-3 py-2 border border-gray-300 rounded">

<!-- AFTER: Design system input -->
<input class="iterum-input">
```

### 3.2 Textareas
```html
<!-- BEFORE: Custom textarea styling -->
<textarea class="w-full px-3 py-2 border border-gray-300 rounded">

<!-- AFTER: Design system textarea -->
<textarea class="iterum-textarea">
```

### 3.3 Select Dropdowns
```html
<!-- BEFORE: Custom select styling -->
<select class="w-full px-3 py-2 border border-gray-300 rounded">

<!-- AFTER: Design system select -->
<select class="iterum-select">
```

### 3.4 Form Groups
```html
<!-- BEFORE: Custom form layout -->
<div class="mb-4">
  <label class="block text-sm font-medium mb-2">Label</label>
  <input class="w-full px-3 py-2 border rounded">
</div>

<!-- AFTER: Design system form group -->
<div class="iterum-form-group">
  <label>Label</label>
  <input class="iterum-input">
</div>
```

## Phase 4: Card System Implementation

### 4.1 Standard Cards
```html
<!-- BEFORE: Custom card styling -->
<div class="bg-white rounded-lg shadow p-6 border">

<!-- AFTER: Design system card -->
<div class="iterum-card">
  <div class="iterum-card-body">
    <!-- Card content -->
  </div>
</div>
```

### 4.2 Card Variants
- **Standard**: `iterum-card`
- **Elevated**: `iterum-card iterum-card-elevated`
- **Interactive**: `iterum-card iterum-card-interactive`

### 4.3 Card Structure
```html
<div class="iterum-card">
  <div class="iterum-card-header">
    <h3 class="heading-3">Card Title</h3>
  </div>
  <div class="iterum-card-body">
    <p class="body-medium">Card content goes here...</p>
  </div>
  <div class="iterum-card-footer">
    <button class="iterum-button iterum-button-primary">Action</button>
  </div>
</div>
```

## Phase 5: Typography System

### 5.1 Heading Classes
```html
<!-- BEFORE: Custom heading styles -->
<h1 class="text-4xl font-bold text-gray-900">

<!-- AFTER: Design system headings -->
<h1 class="heading-1">Main Title</h1>
<h2 class="heading-2">Section Title</h2>
<h3 class="heading-3">Subsection Title</h3>
<h4 class="heading-4">Card Title</h4>
```

### 5.2 Body Text Classes
```html
<!-- BEFORE: Custom text styles -->
<p class="text-base text-gray-700 leading-relaxed">

<!-- AFTER: Design system body text -->
<p class="body-medium">Regular paragraph text</p>
<p class="body-large">Larger emphasis text</p>
<p class="body-small">Smaller supporting text</p>
```

## Phase 6: Navigation System

### 6.1 Navigation Links
```html
<!-- BEFORE: Custom nav styling -->
<a class="text-gray-600 hover:text-blue-500 px-3 py-2 rounded">

<!-- AFTER: Design system navigation -->
<a class="iterum-nav-link">Navigation Item</a>
<a class="iterum-nav-link iterum-nav-link-active">Active Item</a>
```

### 6.2 Navigation Container
```html
<!-- BEFORE: Custom nav container -->
<nav class="bg-white border-b border-gray-200 shadow">

<!-- AFTER: Design system navigation -->
<nav class="iterum-nav-container">
```

## Phase 7: Loading States

### 7.1 Loading Spinners
```html
<!-- BEFORE: Custom loading -->
<div class="animate-spin w-4 h-4 border-2 border-blue-500 rounded-full">

<!-- AFTER: Design system loading -->
<div class="iterum-loading"></div>
```

### 7.2 Skeleton Loading
```html
<!-- BEFORE: Custom skeleton -->
<div class="bg-gray-200 animate-pulse rounded h-4">

<!-- AFTER: Design system skeleton -->
<div class="iterum-skeleton h-4"></div>
```

### 7.3 Loading States
```html
<!-- BEFORE: Custom loading state -->
<div class="opacity-50 pointer-events-none">

<!-- AFTER: Design system loading state -->
<div class="iterum-loading-state">
```

## Implementation Checklist

### ✅ **Completed**
- [x] Design system CSS file
- [x] Tailwind configuration
- [x] Landing page foundation
- [x] Basic button updates

### 🔄 **In Progress**
- [ ] Button standardization across all pages
- [ ] Form element updates
- [ ] Card system implementation

### 📋 **Pending**
- [ ] Typography system rollout
- [ ] Navigation standardization
- [ ] Loading state updates
- [ ] Responsive design fixes
- [ ] Accessibility improvements

## Quick Reference Commands

### Find All Custom Buttons
```bash
grep -r 'class=".*bg-.*text-.*px-.*py-.*rounded' *.html
```

### Find All Custom Inputs
```bash
grep -r 'class=".*px-.*py-.*border.*rounded' *.html
```

### Find All Custom Cards
```bash
grep -r 'class=".*bg-white.*rounded.*shadow.*p-' *.html
```

## Testing Checklist

### Visual Consistency
- [ ] All buttons use consistent styling
- [ ] Form elements have uniform appearance
- [ ] Cards follow consistent layout patterns
- [ ] Typography hierarchy is maintained

### Functionality
- [ ] Hover states work correctly
- [ ] Focus states are visible
- [ ] Transitions are smooth
- [ ] Responsive behavior is consistent

### Accessibility
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators are clear
- [ ] Screen reader compatibility
- [ ] Keyboard navigation works

## Troubleshooting

### Common Issues
1. **CSS Conflicts**: Ensure design system CSS loads after Tailwind
2. **Missing Classes**: Check that all design system classes are defined
3. **Responsive Issues**: Verify breakpoint usage is consistent
4. **Performance**: Monitor CSS bundle size and optimize if needed

### Debug Commands
```javascript
// Check if design system is loaded
console.log('Design System CSS:', document.querySelector('link[href*="iterum-design-system.css"]'));

// Check CSS custom properties
console.log('CSS Variables:', getComputedStyle(document.documentElement).getPropertyValue('--iterum-primary'));
```

## Next Steps

1. **Complete Button Standardization**: Update all remaining buttons
2. **Implement Form System**: Standardize all input elements
3. **Roll Out Card System**: Update layout components
4. **Add Typography Classes**: Implement consistent text styling
5. **Test and Validate**: Ensure all changes work correctly

---

*This guide should be updated as implementation progresses and new patterns are discovered.*
