# How to Disable GitHub Pages

## Issue
GitHub Pages is trying to build and deploy your site, but it's failing because:
1. The build structure doesn't match your project (files are in `public/`, not root)
2. You're using **Firebase Hosting** instead of GitHub Pages
3. The automatic build is conflicting with your Firebase deployment

## Solution: Disable GitHub Pages in Repository Settings

### Steps:

1. **Go to your GitHub repository**
   - Navigate to: https://github.com/Iterum-Foods/iterum-chef-notebook

2. **Open Settings**
   - Click on the "Settings" tab (top navigation)

3. **Go to Pages section**
   - Scroll down to "Pages" in the left sidebar
   - Or go directly to: `https://github.com/Iterum-Foods/iterum-chef-notebook/settings/pages`

4. **Disable GitHub Pages**
   - Under "Source", select "None" from the dropdown
   - Click "Save"

5. **Verify**
   - The "Pages build and deployment" workflow should stop running
   - You'll see a message: "Your site is live at [URL]" will disappear

## Alternative: Keep Pages Disabled via Workflow

I've already updated the workflows to prevent GitHub Pages deployment:
- ✅ `.github/workflows/deploy.yml` - GitHub Pages step disabled
- ✅ `.github/workflows/disable-pages.yml` - New workflow to prevent auto-builds

But you still need to disable it in repository settings to stop the automatic builds.

## Why This Happens

GitHub automatically enables Pages builds when:
- You have a `gh-pages` branch
- You have a `docs/` folder with `index.html`
- Pages is enabled in repository settings
- A workflow triggers Pages deployment

## Your Current Setup

- **Hosting**: Firebase Hosting ✅
- **URL**: https://iterum-culinary-app.web.app ✅
- **Deployment**: `firebase deploy --only hosting` ✅
- **GitHub Pages**: Should be disabled ❌

## After Disabling

Once disabled, you should:
- ✅ Stop seeing "pages build and deployment" errors
- ✅ Continue using Firebase Hosting normally
- ✅ Deploy with: `firebase deploy --only hosting`

## If You Need GitHub Pages Later

If you ever want to use GitHub Pages:
1. Enable it in Settings → Pages
2. Set source to `public/` directory
3. Update the workflow to build from `public/`
4. But you can't use both Firebase Hosting and GitHub Pages for the same site

