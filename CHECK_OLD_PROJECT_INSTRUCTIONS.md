# 🔍 How to Check Old Firebase Project Data

## Quick Manual Check (Easiest)

### **Step 1: Check Firestore Database**

1. **Open this link in your browser:**
   ```
   https://console.firebase.google.com/project/iterum-chef-notebook-26949/firestore
   ```

2. **What to look for:**
   - Do you see any collections listed on the left?
   - Do any collections have documents (numbers next to them)?
   - If you see "Get started" or empty screen → **Database is EMPTY** ✅

3. **If you see data:**
   - Click on each collection
   - See what data is there
   - Decide if it's important

**Screenshot what you see and let me know!**

---

### **Step 2: Check Authentication Users**

1. **Open this link:**
   ```
   https://console.firebase.google.com/project/iterum-chef-notebook-26949/authentication/users
   ```

2. **What to look for:**
   - How many users are listed?
   - If **0 users** → **No users to migrate** ✅
   - If users exist → Note their count

**Tell me the user count!**

---

### **Step 3: Check Storage Files**

1. **Open this link:**
   ```
   https://console.firebase.google.com/project/iterum-chef-notebook-26949/storage
   ```

2. **What to look for:**
   - Do you see any folders or files?
   - If **empty** or "Get started" → **No files** ✅
   - If files exist → Browse and download important ones

**Any files there?**

---

## Quick Decision Tree

### **If ALL are empty:**
```
Firestore: EMPTY ✅
Auth Users: 0 ✅
Storage: EMPTY ✅

→ ✅ SAFE TO ARCHIVE/DELETE
→ No data to lose!
```

### **If ANY have data:**
```
Firestore: HAS DATA ⚠️
OR
Auth Users: > 0 ⚠️
OR
Storage: HAS FILES ⚠️

→ ⚠️ EXPORT FIRST
→ Then decide if you need it
```

---

## Alternative: Use Automated Checker

I created a tool to help check automatically, but it requires the old project's Firebase config.

### **To use the automated checker:**

1. **Get Firebase Config:**
   - Go to: `https://console.firebase.google.com/project/iterum-chef-notebook-26949/settings/general`
   - Scroll to "Your apps" section
   - If no web app exists:
     - Click "Add app" (</> icon)
     - Register app nickname: "Checker"
     - Copy the `firebaseConfig` code
   - If web app exists:
     - Click the app name
     - Copy the `firebaseConfig` code

2. **Open the checker:**
   - Open `check_old_firebase.html` in your browser
   - Replace the Firebase config in the file with the one you copied
   - Click "Check All Data"

---

## What I Need From You

**Please check these 3 things manually (5 minutes):**

1. ✅ Open Firestore link → Any collections/data? (YES/NO)
2. ✅ Open Authentication link → How many users? (NUMBER)
3. ✅ Open Storage link → Any files? (YES/NO)

**Reply with:**
```
Firestore: [EMPTY or HAS DATA]
Users: [0 or NUMBER]
Storage: [EMPTY or HAS FILES]
```

Then I can tell you exactly what to do! 🎯

---

## Quick Links

- **Firestore:** `https://console.firebase.google.com/project/iterum-chef-notebook-26949/firestore`
- **Authentication:** `https://console.firebase.google.com/project/iterum-chef-notebook-26949/authentication/users`
- **Storage:** `https://console.firebase.google.com/project/iterum-chef-notebook-26949/storage`
- **Project Settings:** `https://console.firebase.google.com/project/iterum-chef-notebook-26949/settings/general`

---

## If You Find Data to Export

### **Export Firestore:**
1. In Firestore console, click "Import/Export" at top
2. Click "Export"
3. Select collections
4. Export to Cloud Storage
5. Download backup

### **Export Users:**
1. In Authentication console, click "Export Users"
2. Download CSV file

### **Download Storage Files:**
1. Browse Storage console
2. Click download icon on each file
3. Or use `gsutil` command:
   ```bash
   gsutil -m cp -r gs://iterum-chef-notebook-26949.appspot.com/* ./backup/
   ```

---

**After checking, let me know what you found!** 🔍

