# 🔧 Firebase Storage Setup for Video Uploads

## Quick Setup (5 minutes)

### **Step 1: Enable Firebase Storage**

1. Go to Firebase Console: https://console.firebase.google.com/project/iterum-culinary-app
2. Click "Storage" in left sidebar
3. Click "Get Started"
4. Accept default rules
5. Click "Done"

✅ Storage is now enabled!

---

### **Step 2: Update Storage Rules**

In Firebase Console → Storage → Rules tab, paste this:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Allow authenticated users to upload videos
    match /videos/{videoId} {
      allow read: if true;  // Anyone can view videos
      allow write: if request.auth != null  // Only authenticated users can upload
                   && request.resource.size < 500 * 1024 * 1024  // Max 500MB
                   && request.resource.contentType.matches('video/.*');  // Videos only
    }
    
    // Allow thumbnail uploads
    match /thumbnails/{thumbId} {
      allow read: if true;
      allow write: if request.auth != null
                   && request.resource.size < 5 * 1024 * 1024  // Max 5MB
                   && request.resource.contentType.matches('image/.*');  // Images only
    }
  }
}
```

Click "Publish"

---

### **Step 3: Get Firebase Config**

1. Go to Project Settings (gear icon)
2. Scroll to "Your apps"
3. Select Web app
4. Copy the firebaseConfig object
5. Paste into `usta-public/js/firebase-config.js`

Replace these values:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "iterum-culinary-app.firebaseapp.com",
    projectId: "iterum-culinary-app",
    storageBucket: "iterum-culinary-app.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_ID",
    appId: "YOUR_APP_ID"
};
```

---

### **Step 4: Test Video Upload**

1. Visit: https://iterum-culinary-app.web.app/upload.html
2. Click to upload or drag video
3. Select challenge (optional)
4. Add caption
5. Click "Post Video"
6. Watch progress bar
7. See success message!

---

## 🎯 What Happens

### **Upload Flow:**
```
User selects video
    ↓
Shows preview
    ↓
Choose challenge (optional)
    ↓
Add caption
    ↓
Click "Post Video"
    ↓
Upload to Firebase Storage (with progress bar)
    ↓
Get video URL
    ↓
Send metadata to backend API
    ↓
Video saved to database
    ↓
Success! Redirect to feed
    ↓
Video appears in user's feed
```

### **Demo Mode (No Backend):**
If backend isn't running:
- Video still uploads to Firebase ✅
- Metadata saved to localStorage ✅
- Shows success message ✅
- Can view in demo mode ✅

---

## 📂 Files Created

1. **usta-public/upload.html** - Upload interface
2. **usta-public/js/firebase-config.js** - Firebase setup
3. **firebase.json** - Already configured for hosting

---

## 🎯 Features

✅ **Drag & Drop** - Drag video files  
✅ **Click to Upload** - Traditional file picker  
✅ **Video Preview** - See before posting  
✅ **Challenge Selection** - Link to culinary challenges  
✅ **Caption Input** - Describe your technique  
✅ **Progress Bar** - See upload progress  
✅ **File Validation** - Size limits, video types only  
✅ **Demo Mode Fallback** - Works without backend  

---

## 🧪 Test Locally

### **Without Firebase (Demo Mode):**
- Visit: /upload.html
- Upload video
- Goes to localStorage
- Still works!

### **With Firebase (Real Mode):**
1. Complete setup above
2. Update firebase-config.js
3. Deploy: `firebase deploy`
4. Upload video
5. Gets stored in Firebase Storage
6. Video URL returned
7. Sent to backend

---

## 💡 Next Steps

**After setup:**
1. Test video upload
2. Check Firebase Storage console (see uploaded files)
3. Share upload page with beta chefs
4. Monitor storage usage
5. Set up CDN for fast delivery (later)

---

## ⚠️ Important Notes

**Storage Costs:**
- First 5GB free
- After: $0.026 per GB
- First 50K downloads free
- After: $0.12 per GB

**For beta (200 users, ~500 videos):**
- Videos: ~50GB storage = $1.30/mo
- Downloads: ~500GB = $60/mo
- **Total: ~$70/mo** (very affordable!)

**Can optimize later with:**
- Video compression
- CDN (Cloudflare)
- Adaptive bitrate
- Thumbnail generation

---

**Firebase Storage ready for culinary videos! 🎥**

Setup: 5 minutes
Cost: $70/mo for beta
Ready to receive cooking technique videos! 👨‍🍳

