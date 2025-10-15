# 🔍 Debug Index.html Crash

## Steps to Identify the Crashing Script:

### 1. Open Browser Console (F12)
Press F12 and go to the Console tab before loading index.html

### 2. Look for These Errors:
- ❌ `Uncaught Error`
- ❌ `TypeError: Cannot read property`
- ❌ `ReferenceError: X is not defined`
- ❌ `Maximum call stack size exceeded` (infinite loop/recursion)
- ❌ Page becomes unresponsive

### 3. Check Network Tab:
- See which scripts loaded successfully
- Check for failed script loads (red)
- See which was the LAST script to load before crash

### 4. Scripts Loading Order (index.html):
```
1. auth_guard.js ← Runs FIRST, could block
2. firebase-config.js
3. firebase-auth.js (module)
4. firebase-auth-ui.js (module)
5. auth_lite.js
6. header_user_sync.js
7. header_sync_loader.js
8. main.js
9. ai-integration.js
10. project-management-system.js
11. userControlledStorage.js
12. data-tagging-system.js
13. ingredientLibrary.js ← Loads 100+ items
14. userDataManager.js ← NEW, auto-initializes
15. Inline initialization script
```

### 5. Most Likely Culprits:

#### **A. userDataManager.js** (NEW)
```javascript
// Line 406 - Automatically creates instance
window.userDataManager = new UserDataManager();

// Constructor calls init()
constructor() {
    this.currentUser = null;
    this.init(); // ← Might be blocking
}

// Init calls initialization
init() {
    this.loadCurrentUser();
    this.initializeUserData(); // ← Creates 100+ default items
}
```

**Problem:** If user is signed in, it loads:
- 20 default ingredients
- 10 default equipment items
- Empty arrays for recipes, inventory, HACCP, calendar, drafts
- All synchronously on page load!

#### **B. ingredientLibrary.js**
- Loads default database (100+ items)
- Could be heavy on initial load

#### **C. auth_guard.js**
- If not authenticated, shows modal
- Could be blocking page render

### 6. Quick Fix to Test:

**Option 1: Comment out userDataManager temporarily**

In `index.html`, comment out:
```html
<!-- User Data Manager -->
<!-- <script src="assets/js/userDataManager.js"></script> -->
```

Test if page loads. If yes, userDataManager is the issue.

**Option 2: Make userDataManager non-blocking**

Change line 406 in `userDataManager.js`:
```javascript
// OLD:
window.userDataManager = new UserDataManager();

// NEW:
setTimeout(() => {
    window.userDataManager = new UserDataManager();
    console.log('✅ UserDataManager initialized (delayed)');
}, 500);
```

### 7. Check Console Logs:

**Should see in order:**
```
🔐 Auth Guard checking credentials...
✅ Credentials verified
👤 User: [Your Name]
✅ Auth Guard complete - access granted
🔥 Firebase config set on window: iterum-culinary-app
✅ Firebase Auth initialized
✅ AuthLite loaded
🔄 Initializing Header User Sync...
✅ Header updated with user: [Your Name]
🔍 Initializing authentication system...
✅ AuthLite system loaded successfully
```

**If it stops at any point, that's where it crashed.**

### 8. Test in Incognito:

Always test in incognito (Ctrl+Shift+N) to avoid cache issues.

### 9. Report Back:

Please provide:
1. ✅ Last console log before crash
2. ✅ Any error messages (red)
3. ✅ Does it say "Page Unresponsive"?
4. ✅ Which browser? (Chrome, Firefox, Edge?)
5. ✅ Does it happen immediately or after delay?

---

## Quick Test Commands (Console):

```javascript
// Check what's loaded
console.log('authLite:', !!window.authLite);
console.log('userDataManager:', !!window.userDataManager);
console.log('ingredientLibrary:', !!window.ingredientLibrary);
console.log('currentUser:', localStorage.getItem('current_user'));

// Force refresh header
if (window.headerUserSync) {
    window.headerUserSync.refresh();
}
```

---

## Temporary Workaround:

If you need the app to work NOW while we debug:

1. Visit: `https://iterum-culinary-app.web.app/recipe-library.html`
2. Sign in via popup modal
3. Use other pages that might not have the issue

---

**Copy the console logs and error messages and send them to me!** 🔍

