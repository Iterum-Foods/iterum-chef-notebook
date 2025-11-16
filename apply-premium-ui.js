/**
 * Script to add premium UI CSS to all main pages
 * Run this in Node.js: node apply-premium-ui.js
 */

const fs = require('fs');
const path = require('path');

// Main pages to update
const mainPages = [
    'recipe-library.html',
    'recipe-developer.html',
    'recipe-upload.html',
    'menu-builder.html',
    'ingredients.html',
    'equipment-management.html',
    'vendor-management.html',
    'contact_management.html',
    'user_management.html',
    'purchase-orders.html',
    'inventory.html'
];

// CSS link to add
const premiumUILink = '<link rel="stylesheet" href="assets/css/premium-ui-system.css">';

mainPages.forEach(page => {
    const filePath = path.join(__dirname, page);
    
    if (!fs.existsSync(filePath)) {
        console.log(`⚠️  ${page} not found, skipping...`);
        return;
    }
    
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Check if already has premium UI
    if (content.includes('premium-ui-system.css')) {
        console.log(`✅ ${page} already has premium UI`);
        return;
    }
    
    // Add after iterum-design-system.css
    const designSystemRegex = /<link rel="stylesheet" href="assets\/css\/iterum-design-system\.css">/;
    
    if (designSystemRegex.test(content)) {
        content = content.replace(
            designSystemRegex,
            `<link rel="stylesheet" href="assets/css/iterum-design-system.css">\n    ${premiumUILink}`
        );
        
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✅ Added premium UI to ${page}`);
    } else {
        console.log(`⚠️  Could not find design system link in ${page}`);
    }
});

console.log('\n🎉 Premium UI application complete!');

