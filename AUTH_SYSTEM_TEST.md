# 🔐 Authentication System Test Plan

## ✅ **Current Status**
- **Backend**: ✅ Running on port 8000
- **Frontend**: ✅ Running on port 8080  
- **Template Path**: ✅ Fixed (`templates/shared/shared-login-modal.html`)
- **Fallback Modal**: ✅ Enhanced with proper functionality

---

## 🧪 **Test Sequence**

### **1. Open Application**
Navigate to: `http://localhost:8080`

**Expected Behavior:**
- Loading screen appears
- Authentication system checks for existing session
- If no session: Show authentication options

### **2. Test Authentication Options**

#### **Option A: Continue Offline (Quick Start)**
- Click "Continue Offline" or "🚀 Continue Offline (No Setup Required)"
- Should create local user profile immediately
- Should hide loading screen and show main app

#### **Option B: Create Profile**
- Click "Create Account" or "📧 Create Profile / Sign In"
- Fill in name, email (optional), role, restaurant
- Click "Create Profile & Continue"
- Should save user data and load main app

#### **Option C: Sign In Existing**
- If there are saved users, should show user selection
- Click on existing user to continue with that profile

### **3. Test Data Persistence**

#### **Daily Notes Test**
1. Navigate to Daily Notes section
2. Fill in some data in different tabs (Operations, Staff, Financial, etc.)
3. Click "Save Daily Notes"
4. Refresh the page
5. **Expected**: User should remain logged in, data should persist

#### **Session Persistence Test**
1. Log in with any method
2. Navigate around the app
3. Refresh the page multiple times
4. **Expected**: Should remain logged in, no re-authentication required

### **4. Test User Switching**
1. Log in as one user
2. Add some daily notes or data
3. Switch to different user (if available)
4. **Expected**: Each user should have separate data

---

## 🔧 **Technical Verification**

### **Browser Console Checks**
Open browser console and verify:

```javascript
// Check if unified auth is loaded
console.log('UnifiedAuth:', window.unifiedAuth);

// Check current user
console.log('Current User:', unifiedAuth.getCurrentUser());

// Check session status
console.log('Session Info:', unifiedAuth.getSessionInfo());

// Check local storage
console.log('Stored User:', localStorage.getItem('current_user'));
console.log('Session Active:', localStorage.getItem('session_active'));
```

### **Network Checks**
In browser network tab, verify:
- ✅ `templates/shared/shared-login-modal.html` loads successfully (or fallback is used)
- ✅ Backend health check: `GET /health` returns 200
- ✅ Auth endpoints accessible: `POST /api/auth/*` available

---

## 🎯 **Success Criteria**

### **✅ Authentication Working**
- [ ] User can create account/profile
- [ ] User can sign in with existing account  
- [ ] User can continue offline without setup
- [ ] Session persists across page refreshes
- [ ] Loading screen disappears after authentication

### **✅ Data Persistence Working**
- [ ] Daily notes save and reload correctly
- [ ] User-specific data remains separate
- [ ] Data persists between sessions
- [ ] No data loss on page refresh

### **✅ UI/UX Working**
- [ ] Authentication modals display correctly
- [ ] Error messages show for invalid inputs
- [ ] Loading states work properly
- [ ] User can switch between login/signup forms

---

## 🚨 **Common Issues & Solutions**

### **Issue: "Standardized login modal template not found"**
**Solution**: Fallback modal should activate automatically
**Verification**: Check if login modal appears despite the warning

### **Issue: User data not persisting**
**Solution**: Check browser console for localStorage errors
**Verification**: Inspect localStorage in browser dev tools

### **Issue: Backend connection failed**
**Solution**: Ensure backend is running on port 8000
**Verification**: Test `http://localhost:8000/health` directly

### **Issue: Loading screen stuck**
**Solution**: Emergency timeout should activate after 5 seconds
**Verification**: Wait for automatic timeout or check console errors

---

## 🔄 **Next Steps After Testing**

1. **If authentication works**: ✅ Move to data persistence verification
2. **If issues found**: Debug specific components
3. **If all works**: ✅ Ready for production use

---

**🚀 Ready to test the complete authentication and data persistence workflow!**
