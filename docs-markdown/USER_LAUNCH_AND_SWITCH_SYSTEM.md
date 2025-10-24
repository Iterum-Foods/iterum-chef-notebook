# User Launch and Switch System - Iterum App

## Overview

The Iterum App implements a dual-mode user authentication system:
1. **Launch Mode**: Popup modal for initial user selection (cannot be closed by clicking outside)
2. **Switch Mode**: Header dropdown for switching users after the app is running

## System Architecture

### 1. Launch Authentication Flow

When the app launches, the following sequence occurs:

1. **App Initialization** (`main.js`)
   - Calls `checkAuthentication()`
   - If no user is authenticated, calls `forceUserSelection()`

2. **Forced User Selection** (`unified_auth_system.js`)
   - Clears any existing session
   - Loads saved users from storage
   - Shows user selection popup modal

3. **User Selection Modal** (`showUserSelection()`)
   - Creates a full-screen popup modal
   - **Cannot be closed by clicking outside** - user must make a selection
   - Displays existing users with "Select" buttons
   - Provides options to create new profile, sign in, or continue offline

### 2. User Switch Flow

After the app is running, users can switch profiles using:

1. **Header User Section**
   - Click on the user avatar/name in the header
   - Shows dropdown menu with "Switch User" option

2. **Switch User Dropdown** (`showUserSwitchDropdown()`)
   - Creates a compact dropdown positioned below the header
   - Lists all available users with "Switch To" buttons
   - Current user is marked as "Current"
   - Provides quick access to profile management

## Key Components

### UnifiedAuthSystem Class

```javascript
class UnifiedAuthSystem {
    constructor() {
        this.currentUser = null;
        this.isOnline = false;
        this.savedUsers = JSON.parse(localStorage.getItem('saved_users')) || [];
        this.setupSessionHandlers();
        this.init();
    }
    
    async init() {
        // Always force user selection at startup
        await this.forceUserSelection();
    }
}
```

### Launch Modal Methods

- **`showUserSelection()`**: Creates launch popup modal
- **`showLoginOptions()`**: Shows options when no users exist
- **`createOfflineProfile()`**: Creates offline user profile

### Switch Dropdown Methods

- **`showUserSwitchDropdown()`**: Creates header-aligned dropdown
- **`removeUserSwitchDropdown()`**: Removes dropdown
- **`handleClickOutsideDropdown()`**: Closes dropdown on outside click

## User Data Management

### Loading Users

```javascript
async loadSavedUsers() {
    if (this.isOnline) {
        // Try backend first
        try {
            const response = await fetch('http://localhost:8000/api/users');
            this.savedUsers = response.json().users || [];
        } catch (error) {
            // Fallback to local storage
            this.loadSavedUsersFromLocal();
        }
    } else {
        // Offline mode - local storage only
        this.loadSavedUsersFromLocal();
    }
}
```

### Saving Users

Users are automatically saved to:
- `localStorage['saved_users']` - Array of all user profiles
- `localStorage['current_user']` - Currently active user
- `localStorage['session_active']` - Session status

## Security Features

### Launch Security

- **Modal cannot be closed by clicking outside**
- **User must select a profile to continue**
- **No automatic session restoration**
- **Fresh authentication required on each launch**

### Session Management

- **Session persists across page refreshes**
- **Session expires on explicit logout**
- **Cross-tab synchronization via localStorage events**

## UI Components

### Launch Modal Styling

```css
.auth-modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}
```

### Switch Dropdown Styling

```css
.user-switch-dropdown {
    position: fixed;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    animation: dropdownSlideIn 0.2s ease-out;
}
```

## Event Flow

### Launch Events

1. `DOMContentLoaded` → `main.js.init()`
2. `checkAuthentication()` → `forceUserSelection()`
3. `showUserSelection()` → Popup modal displayed
4. User selects profile → `selectUser()`
5. `updateAuthUI()` → App content revealed

### Switch Events

1. Header user click → `toggleUserDropdown()`
2. "Switch User" click → `window.switchUser()`
3. `showUserSwitchDropdown()` → Dropdown displayed
4. User selects profile → `selectUser()`
5. `updateAuthUI()` → Header updated

## Testing

### Test Page

Use `test/test_user_loading.html` to verify:
- User loading functionality
- Saved users storage
- Local storage integration
- Authentication system status

### Test Commands

```javascript
// Test user loading
await window.unifiedAuth.loadSavedUsers();

// Test saved users
console.log(window.unifiedAuth.savedUsers);

// Test auth system
console.log(window.unifiedAuth.getSessionInfo());
```

## Troubleshooting

### Common Issues

1. **Users not loading on launch**
   - Check `localStorage['saved_users']`
   - Verify `loadSavedUsers()` method execution
   - Check console for error messages

2. **Switch dropdown not positioning correctly**
   - Verify `.header-user-section` element exists
   - Check dropdown positioning calculations
   - Ensure proper z-index values

3. **Launch modal can be closed**
   - Verify click outside event handler
   - Check modal z-index and positioning
   - Ensure modal is properly attached to body

### Debug Information

```javascript
// Get auth system status
const auth = window.unifiedAuth;
console.log('Auth Status:', {
    initialized: !!auth,
    currentUser: auth.currentUser?.name,
    savedUsers: auth.savedUsers?.length,
    sessionActive: auth.isSessionActive(),
    isOnline: auth.isOnline
});
```

## Benefits

1. **Secure Launch**: Users cannot bypass authentication
2. **Intuitive Switching**: Easy user switching after launch
3. **Persistent Sessions**: User state maintained across pages
4. **Offline Support**: Works without backend connection
5. **Cross-tab Sync**: User changes sync across browser tabs

## Future Enhancements

1. **Biometric Authentication**: Fingerprint/face recognition
2. **Multi-factor Authentication**: SMS/email verification
3. **Role-based Access Control**: Different permissions per user
4. **Session Timeout**: Automatic logout after inactivity
5. **Audit Logging**: Track user actions and changes
