# 🔐 Header User Synchronization Integration Guide

## Overview

The Header User Sync system ensures that user information is consistently displayed in the header across all pages in your Iterum R&D app. This prevents the issue where users might see different user information when navigating between pages.

## 🚀 Quick Integration

### 1. Add the Header Sync Script

Add this line to the `<head>` section of every page:

```html
<script src="assets/js/header_user_sync.js"></script>
```

### 2. Ensure Header Elements Have Correct IDs

Your header must include these elements with the exact IDs:

```html
<!-- Main user display -->
<div class="header-user-name" id="current-user">Guest User</div>
<div class="header-user-role" id="user-role">Guest</div>

<!-- User avatar -->
<div class="header-user-avatar" id="user-avatar">G</div>

<!-- Dropdown user info -->
<div class="header-user-dropdown-title" id="dropdown-user-name">Guest User</div>
<div class="header-user-dropdown-subtitle" id="dropdown-user-role">Guest</div>
```

## 🔧 How It Works

### Automatic Synchronization

The system automatically:
- ✅ Updates user display when pages load
- ✅ Listens for authentication state changes
- ✅ Updates header across page refreshes
- ✅ Handles tab switching and visibility changes
- ✅ Updates page titles with user information

### Event-Driven Updates

The system responds to these events:
- `userLoggedIn` - When a user logs in
- `userLoggedOut` - When a user logs out  
- `userSwitched` - When switching between users

## 📱 Integration Examples

### Basic Integration

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Add the header sync script -->
    <script src="assets/js/header_user_sync.js"></script>
</head>
<body>
    <header>
        <!-- Your existing header with correct IDs -->
        <div id="current-user">Guest User</div>
        <div id="user-role">Guest</div>
        <div id="user-avatar">G</div>
    </header>
    
    <!-- Rest of your page content -->
</body>
</html>
```

### With Authentication System

```html
<!DOCTYPE html>
<html>
<head>
    <script src="assets/js/header_user_sync.js"></script>
    <script src="assets/js/unified_auth_system.js"></script>
</head>
<body>
    <!-- Your header and content -->
    
    <script>
        // The header sync will automatically work with your auth system
        // No additional code needed!
    </script>
</body>
</html>
```

## 🧪 Testing

### Test Page

Use `test_header_sync.html` to verify the system is working:

1. Open the test page
2. Click "Test Login" to simulate user login
3. Click "Test Switch User" to simulate user switching
4. Click "Test Logout" to simulate logout
5. Check that the header updates immediately

### Console Messages

Look for these messages in the browser console:
- `🔄 Initializing Header User Sync...`
- `✅ Found header elements: [list of found elements]`
- `✅ Header updated with user: [username]`
- `✅ Header updated as guest user`

## 🐛 Troubleshooting

### Common Issues

1. **Header not updating**
   - Check that all required IDs are present
   - Verify the script is loaded (check console for initialization message)
   - Ensure authentication events are being triggered

2. **Script not found**
   - Verify the path to `header_user_sync.js` is correct
   - Check that the file exists in `assets/js/`

3. **Elements not found**
   - Ensure all required header elements have the correct IDs
   - Check for typos in element IDs

### Debug Commands

In the browser console, you can run:

```javascript
// Check if header sync is active
console.log(window.headerUserSync);

// Force refresh header display
window.headerUserSync.refresh();

// Check current user state
console.log(localStorage.getItem('current_user'));
```

## 📋 Required Header Elements

| Element ID | Purpose | Required |
|------------|---------|----------|
| `current-user` | Main user name display | ✅ Yes |
| `user-role` | User role/title | ✅ Yes |
| `user-avatar` | User avatar/initials | ✅ Yes |
| `dropdown-user-name` | Dropdown user name | ✅ Yes |
| `dropdown-user-role` | Dropdown user role | ✅ Yes |

## 🎯 Benefits

- **Consistent UX**: Users see the same information across all pages
- **Real-time Updates**: Header updates immediately when user state changes
- **Automatic**: No manual coding required after integration
- **Robust**: Handles edge cases like page refreshes and tab switching
- **Debug-Friendly**: Clear console logging for troubleshooting

## 🔄 Next Steps

1. **Add the script** to all your existing pages
2. **Verify header IDs** match the requirements
3. **Test navigation** between pages
4. **Check console** for any error messages
5. **Use test page** to verify functionality

---

**Need Help?** Check the console for error messages or refer to the test page for examples.
