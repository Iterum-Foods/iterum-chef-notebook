# Firebase Setup Guide for Iterum R&D Chef Notebook

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: `iterum-chef-notebook` (or your preferred name)
4. Enable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Authentication

1. In Firebase Console, go to "Authentication" → "Sign-in method"
2. Enable "Google" provider
3. Add your domain to authorized domains (localhost for development)
4. Save

## Step 3: Enable Firestore Database

1. Go to "Firestore Database" → "Create database"
2. Choose "Start in test mode" (for development)
3. Select a location (choose closest to your users)
4. Click "Done"

## Step 4: Get Firebase Configuration

1. Go to Project Settings (gear icon)
2. Scroll down to "Your apps"
3. Click "Add app" → "Web" (</>)
4. Register app with name: "Iterum Chef Notebook"
5. Copy the configuration object

## Step 5: Update Your App

Replace the Firebase config in `index-local.html`:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

## Step 6: Test the Integration

1. Start your app: `python start_full_app.py`
2. Open: http://localhost:8080/index-local.html
3. Click "Sign in with Google"
4. Check Firebase Console → Authentication → Users
5. Check Firestore → Data → users collection

## Features Now Available

✅ **Google Sign-in** - Users can sign in with their Google account
✅ **User Profiles** - Stored in Firestore with subscription tracking
✅ **Cross-device Sync** - Users can access their data from any device
✅ **User Analytics** - Track user engagement and usage
✅ **Subscription Ready** - Foundation for monetization

## Next Steps for Monetization

1. **Add Stripe Integration** for payments
2. **Create subscription tiers** (Free, Basic, Premium)
3. **Implement usage limits** based on subscription
4. **Add team features** for Pro users
5. **Set up analytics** to track feature usage

## Security Rules (Firestore)

For production, update Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /users/{userId}/recipes/{recipeId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## Troubleshooting

- **"Firebase not initialized"** - Check your config object
- **"Permission denied"** - Check Firestore security rules
- **"Popup blocked"** - Allow popups for localhost
- **"Network error"** - Check internet connection

Your app now has professional user management with Firebase! 🚀 