# 🔥 Enable Firebase Storage - Step by Step

## Quick 5-Minute Setup

### **Step 1: Open Firebase Console**

Click this link:
https://console.firebase.google.com/project/iterum-culinary-app/storage

**Or manually:**
1. Go to: https://console.firebase.google.com/
2. Click "iterum-culinary-app" project
3. Click "Storage" in left sidebar

---

### **Step 2: Click "Get Started"**

You'll see a button that says **"Get Started"**

Click it.

---

### **Step 3: Choose Security Rules**

You'll see two options:

**Select:** "Start in production mode"

This is safer. We'll add custom rules next.

Click **"Next"**

---

### **Step 4: Choose Location**

**Select:** "us-central1" (or your preferred region)

Click **"Done"**

✅ **Storage is now enabled!**

---

### **Step 5: Update Storage Rules**

In the Firebase Console:
1. Go to Storage tab
2. Click "Rules" tab
3. Replace everything with this:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Videos - anyone can read, authenticated users can upload
    match /videos/{videoId} {
      allow read: if true;
      allow write: if request.auth != null
                   && request.resource.size < 500 * 1024 * 1024
                   && request.resource.contentType.matches('video/.*');
    }
    
    // Thumbnails
    match /thumbnails/{thumbId} {
      allow read: if true;
      allow write: if request.auth != null
                   && request.resource.size < 5 * 1024 * 1024
                   && request.resource.contentType.matches('image/.*');
    }
  }
}
```

Click **"Publish"**

---

### **Step 6: Get Firebase Config**

1. In Firebase Console, click **⚙️ (gear icon)** → "Project settings"
2. Scroll down to **"Your apps"**
3. You should see a web app
4. If not, click **"Add app"** → Web (</>) → Register

**Copy this code block:**

```javascript
const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  projectId: "...",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "..."
};
```

**Send me these values and I'll update the file!**

---

### **Step 7: Test It Works**

After I update the config:

1. Visit: https://iterum-culinary-app.web.app/upload.html
2. Click or drag a video file
3. Select a challenge
4. Add caption
5. Click "Post Video"
6. Watch progress bar!
7. ✅ Success!

**Then check Firebase Console → Storage:**
You'll see your video file stored!

---

## ⚡ Quick Copy-Paste

**Go to:**
https://console.firebase.google.com/project/iterum-culinary-app/settings/general

**Scroll to: "Your apps" → Web app**

**Copy the firebaseConfig object and send it to me!**

It looks like:
```javascript
{
  apiKey: "AIza...",
  authDomain: "iterum-culinary-app.firebaseapp.com",
  // ... etc
}
```

---

## 🎯 After Setup You Can:

✅ Upload real cooking videos  
✅ Store them in Firebase  
✅ Share URLs automatically  
✅ Track storage usage  
✅ Manage all videos in console  

**Ready! Send me your Firebase config values!** 🔥

