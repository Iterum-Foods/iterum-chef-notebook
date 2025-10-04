# Firebase Deployment Guide for Iterum Culinary App

## Current Status
- ✅ Firebase project configured (`iterum-culinary-app`)
- ❌ App not deployed to Firebase Hosting
- 🔧 Ready for deployment

## Prerequisites
1. **Firebase CLI**: Install Firebase CLI tools
2. **Authentication**: Login to Firebase with your Google account
3. **Project Access**: Ensure you have access to the `iterum-culinary-app` project

## Step 1: Install Firebase CLI

### Option A: Using npm (Recommended)
```bash
npm install -g firebase-tools
```

### Option B: Using Chocolatey (Windows)
```bash
choco install firebase-cli
```

### Option C: Direct Download
- Download from: https://firebase.google.com/docs/cli

## Step 2: Login to Firebase
```bash
firebase login
```

## Step 3: Initialize Firebase Hosting
```bash
# Navigate to your project directory
cd "C:\Users\chefm\my-culinary-app\Iterum App"

# Initialize Firebase Hosting
firebase init hosting
```

### Configuration Options:
- **Project**: Select `iterum-culinary-app`
- **Public Directory**: `./` (current directory)
- **Single-page App**: `Yes` (for SPA routing)
- **GitHub auto-builds**: `No` (we'll handle this manually)
- **Overwrite index.html**: `No`

## Step 4: Configure firebase.json
The `firebase.json` file should look like this:

```json
{
  "hosting": {
    "public": "./",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "**/*.@(js|css)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=31536000"
          }
        ]
      }
    ]
  }
}
```

## Step 5: Deploy to Firebase
```bash
# Deploy to Firebase Hosting
firebase deploy --only hosting

# Or deploy everything
firebase deploy
```

## Step 6: Verify Deployment
After deployment, your app will be available at:
- **Primary URL**: `https://iterum-culinary-app.firebaseapp.com`
- **Custom Domain**: `https://iterum-culinary-app.web.app`

## Step 7: Configure Custom Domain (Optional)
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `iterum-culinary-app`
3. Go to **Hosting** → **Add custom domain**
4. Enter your domain (e.g., `iterum-culinary-app.com`)
5. Follow DNS configuration instructions

## Automated Deployment with GitHub Actions

### Option A: Add to Existing Workflow
Add this to your `.github/workflows/deploy.yml`:

```yaml
- name: Deploy to Firebase
  if: github.ref == 'refs/heads/main'
  run: |
    npm install -g firebase-tools
    firebase deploy --only hosting --token ${{ secrets.FIREBASE_TOKEN }}
```

### Option B: Create Firebase Token
1. Run: `firebase login:ci`
2. Copy the token
3. Add it as `FIREBASE_TOKEN` secret in GitHub

## Security Considerations

### Firebase Security Rules
If using Firestore or Storage, configure security rules:

```javascript
// Firestore Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}

// Storage Rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Environment Configuration
For different environments, you can use:

```bash
# Deploy to production
firebase use production
firebase deploy

# Deploy to staging
firebase use staging
firebase deploy
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure you're logged in: `firebase login`
   - Check project access in Firebase Console

2. **Build Errors**
   - Check for TypeScript/JavaScript errors
   - Ensure all dependencies are installed

3. **Routing Issues**
   - Configure SPA rewrites in `firebase.json`
   - Test all routes after deployment

4. **Authentication Issues**
   - Verify Firebase config in `firebase-config.js`
   - Check authorized domains in Firebase Console

### Useful Commands
```bash
# Check Firebase status
firebase projects:list

# View deployment history
firebase hosting:sites:list

# Rollback deployment
firebase hosting:rollback

# Preview locally
firebase serve
```

## Post-Deployment Checklist

- [ ] App loads correctly at Firebase URL
- [ ] Authentication works properly
- [ ] All pages/routes are accessible
- [ ] Security features are functioning
- [ ] Performance is acceptable
- [ ] Mobile responsiveness works
- [ ] SEO meta tags are present
- [ ] Analytics tracking is working

## Monitoring and Maintenance

### Firebase Console Monitoring
1. **Hosting**: Monitor traffic and performance
2. **Authentication**: Check user sign-ups and activity
3. **Analytics**: Review user engagement metrics
4. **Crashlytics**: Monitor app crashes and errors

### Regular Maintenance
- **Weekly**: Check Firebase Console for issues
- **Monthly**: Review performance metrics
- **Quarterly**: Update dependencies and security rules

## Cost Considerations

### Firebase Hosting Pricing
- **Free Tier**: 10 GB storage, 1 GB transfer/month
- **Paid Plans**: $0.026/GB for additional storage
- **Custom Domain**: Free

### Optimization Tips
- Enable compression in `firebase.json`
- Use appropriate cache headers
- Optimize images and assets
- Implement lazy loading

---

## Quick Start Commands

```bash
# 1. Install Firebase CLI
npm install -g firebase-tools

# 2. Login
firebase login

# 3. Initialize (if not done)
firebase init hosting

# 4. Deploy
firebase deploy --only hosting

# 5. Verify
# Visit: https://iterum-culinary-app.firebaseapp.com
```

**🎉 Your app will be live on Firebase after completing these steps!**
