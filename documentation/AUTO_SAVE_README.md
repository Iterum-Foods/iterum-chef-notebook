# 🔄 Auto-Save System for Iterum R&D Chef Notebook

The Auto-Save System automatically preserves user work when navigating between screens, preventing data loss and improving user experience across your culinary R&D platform.

## ✨ Features

### 🎯 Smart Saving
- **Automatic Detection**: Monitors all form inputs, textareas, and select elements
- **Debounced Saving**: Waits for user to stop typing before saving (configurable delay)
- **Critical Field Priority**: Important fields like recipe names save immediately
- **Navigation Triggers**: Saves automatically when clicking links or using browser navigation

### 💾 Multiple Storage Methods
- **Local Storage**: Client-side backup for offline use
- **Server Sync**: Syncs to backend when online
- **Offline Support**: Continues saving locally when offline, syncs when connection restored

### 🎨 Visual Feedback
- **Save Indicators**: Shows "💾 Saved" animation on fields
- **Status Display**: Real-time status in header
- **Restore Prompts**: Offers to restore previous work on page load
- **Critical Field Highlighting**: Green border for important fields

### 📱 Cross-Platform
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Browser Compatibility**: Modern browsers with localStorage support
- **Performance Optimized**: Minimal impact on page performance

## 🚀 Quick Start

### 1. Include Scripts
Add these scripts to your HTML pages in order:

```html
<script src="auto_save_system.js"></script>
<script src="auto_save_config.js"></script>
```

### 2. Automatic Initialization
The system initializes automatically when the DOM loads. No additional setup required!

### 3. Page-Specific Configuration
The system automatically detects the current page and applies appropriate settings:

- **Menu Builder**: High-frequency saving (15s interval)
- **Recipe Developer**: Very high-frequency saving (10s interval)  
- **Recipe Upload**: Moderate saving (30s interval)
- **Recipe Library**: Lower frequency (45s interval)
- **Other Pages**: Default configuration (30s interval)

## 🛠️ Configuration

### Page-Specific Settings
Each page type has optimized settings in `auto_save_config.js`:

```javascript
'menu-builder': {
    saveInterval: 15000,    // Save every 15 seconds
    debounceDelay: 1500,    // Wait 1.5s after user stops typing
    showNotifications: true, // Show save confirmations
    priority: 'high'        // Critical page
}
```

### Critical Fields
These fields trigger immediate saving:
- `recipe-name`, `recipe-title`
- `menu-title`, `project-name`
- `restaurant-name`
- `ingredients-list`, `instructions`
- `description`, `main-content`

### Immediate Save Fields
These fields force a full page save when changed:
- `recipe-type`, `cuisine-type`
- `difficulty-level`, `serving-size`
- `prep-time`, `cook-time`

## 📋 API Endpoints

### Save Data
```
POST /api/autosave/save
```
Saves form data with metadata including timestamp, page ID, and user context.

### Load Data
```
GET /api/autosave/load/{page_id}
```
Retrieves the most recent auto-saved data for a specific page.

### Clear Data
```
DELETE /api/autosave/clear/{page_id}
```
Clears all auto-saved data for a specific page.

### Health Check
```
GET /api/autosave/health
```
Returns auto-save system status and statistics.

## 🎮 Manual Controls

### Force Save
```javascript
window.autoSaveConfig.manualSave();
```

### Check Status
```javascript
const status = window.autoSaveConfig.getStatus();
console.log(status);
```

### Clear Data
```javascript
window.autoSaveConfig.clearData();
```

## 🔧 Advanced Usage

### Custom Field Handlers
Monitor specific fields with custom logic:

```javascript
// In your page-specific code
document.addEventListener('input', (e) => {
    if (e.target.matches('#special-field')) {
        // Custom handling for special fields
        window.autoSave.forceSave();
    }
});
```

### Page-Specific Features
Add custom auto-save behavior for specific pages:

```javascript
// Example: Save when menu sections are added
document.addEventListener('click', (e) => {
    if (e.target.matches('.add-menu-section')) {
        setTimeout(() => {
            window.autoSave.forceSave();
        }, 500);
    }
});
```

## 🛡️ Data Privacy & Security

### Local Storage
- Uses namespaced keys: `iterum_autosave_[page]_[field]`
- Excludes sensitive fields (passwords, etc.)
- Automatic cleanup of old data (>24 hours)

### Server Storage
- Temporary storage for session continuity
- No permanent user data retention
- Automatic cleanup of old saves

### Security Features
- Excludes password fields automatically
- Configurable field exclusion list
- No file upload content saved (metadata only)

## 🐛 Troubleshooting

### Auto-Save Not Working
1. Check browser console for errors
2. Verify scripts are loaded in correct order
3. Ensure localStorage is enabled
4. Check network connectivity for server sync

### Restore Prompt Not Showing
1. Data must be newer than 24 hours
2. Page ID must match exactly
3. Must have substantial form data
4. Check localStorage for saved data

### Performance Issues
1. Increase debounce delay for slower devices
2. Reduce save interval frequency
3. Exclude non-essential fields
4. Check for memory leaks in long sessions

## 📊 Monitoring

### Status Indicators
- **🟢 Green**: Auto-save active and online
- **🟡 Yellow**: Auto-save active but offline
- **🔴 Red**: Auto-save disabled or error

### Debug Information
```javascript
// Get detailed status
const status = window.autoSave.getAutoSaveStatus();
console.log('Auto-save status:', status);

// List all configurations
console.log('Page configs:', window.autoSaveConfig.configs);
```

## 🎯 Demo Page

Visit `auto_save_demo.html` to see the system in action:
- Interactive forms with real-time saving
- Visual indicators and status display
- Test navigation and restore functionality
- Debug tools and status monitoring

## 🚀 Best Practices

### For Users
1. **Trust the System**: You don't need to manually save constantly
2. **Watch for Indicators**: Green borders = critical fields that save immediately
3. **Use Manual Save**: Click "💾 Manual Save" before important navigation
4. **Check Restore Prompts**: Always review what's being restored

### For Developers
1. **Test Navigation**: Ensure saves trigger on all navigation methods
2. **Monitor Performance**: Watch for excessive save frequency
3. **Handle Offline**: Test offline scenarios and sync recovery
4. **User Feedback**: Provide clear visual feedback for save status

## 🔄 Future Enhancements

- **Conflict Resolution**: Handle concurrent editing scenarios
- **Version History**: Track multiple save versions
- **Real-time Collaboration**: Multi-user auto-save coordination
- **Advanced Analytics**: Detailed save/restore statistics
- **Mobile Optimization**: Enhanced mobile-specific features

---

*Auto-Save System v1.0 - Part of Iterum R&D Chef Notebook Professional Recipe Development Platform*