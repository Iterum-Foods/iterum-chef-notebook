# 🚀 Deployment Guide for iterumfoods.xyz

This guide will help you deploy your landing pages to iterumfoods.xyz and create a comprehensive company showcase website.

## 📋 Quick Start

### Option 1: Simple Deployment (Recommended)
Deploy the unified landing page as your homepage:

1. **Upload to iterumfoods.xyz root:**
   - Copy `2-company-showcase/iterumfoods-unified-landing.html`
   - Rename to `index.html`
   - Upload to your web server root directory

2. **That's it!** Your site is live at https://iterumfoods.xyz

### Option 2: Full Platform Deployment
Set up multiple pages for a complete web presence:

```
iterumfoods.xyz/
├── index.html                    # Main landing (unified-landing.html)
├── app.html                      # Main app entry (main-app-index.html)
├── business-planner/
│   └── index.html               # Restaurant Business Planner
├── payroll/
│   └── index.html               # Payroll App
├── skills-portfolio/
│   └── index.html               # Skills Portfolio App
└── assets/                      # CSS, JS, images
```

## 🎯 Recommended Structure

### Homepage (iterumfoods.xyz)
**Use:** `2-company-showcase/iterumfoods-unified-landing.html`

**Why:**
- Shows all 4 platforms
- Professional design
- Google Analytics already configured
- Multiple CTAs for each product
- Mobile responsive

**Changes Needed:**
1. Update any placeholder URLs to actual product URLs
2. Add real screenshots/images of your apps
3. Update contact information
4. Add your actual domain links

### App Portal (app.iterumfoods.xyz or iterumfoods.xyz/app)
**Use:** `1-main-platform/main-app-index.html`

**Why:**
- Full authentication system
- Firebase integration
- User dashboard access
- Recipe development platform

**Changes Needed:**
1. Configure Firebase production credentials
2. Update redirect URLs
3. Test authentication flows
4. Set up proper domain routing

### Individual Product Pages

#### /business-planner
**Use:** `3-individual-apps/restaurant-business-planner.html`
- Direct signups for business planning tool
- Focused marketing for entrepreneurs

#### /payroll
**Use:** `3-individual-apps/payroll-app.html`
- Direct signups for payroll system
- Focused on restaurant managers

#### /skills-portfolio
**Use:** `3-individual-apps/skills-portfolio-app.html`
- Professional networking features
- Targeted at culinary professionals

## 🔧 Pre-Deployment Checklist

### [ ] 1. Content Updates

#### Update Contact Information
```html
<!-- Find and update in all files: -->
- Email: your-email@iterumfoods.xyz
- Phone: Your actual phone number
- Address: Your business address (if applicable)
```

#### Update URLs
```html
<!-- Replace placeholder URLs with actual domains: -->
- Main site: https://iterumfoods.xyz
- App portal: https://app.iterumfoods.xyz
- Blog/resources: https://blog.iterumfoods.xyz (if applicable)
```

#### Update CTAs (Call-to-Actions)
```html
<!-- Ensure all buttons link to correct pages: -->
<a href="https://app.iterumfoods.xyz/signup">Get Started</a>
<a href="/business-planner">Learn More</a>
<a href="mailto:hello@iterumfoods.xyz">Contact Us</a>
```

### [ ] 2. Firebase Configuration

If using `main-app-index.html`, update Firebase config:

```javascript
// File: assets/js/firebase-config.js
const firebaseConfig = {
    apiKey: "YOUR_PRODUCTION_API_KEY",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef123456"
};
```

**Steps:**
1. Create production Firebase project
2. Enable Authentication (Email, Google)
3. Set up Firestore database
4. Update security rules
5. Add authorized domains (iterumfoods.xyz)

### [ ] 3. Google Analytics

Already configured with ID: `G-MC8Q3SZ47K`

**To update:**
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'YOUR-GA-ID');
</script>
```

### [ ] 4. SEO Optimization

Update meta tags in all landing pages:

```html
<head>
    <title>Your Optimized Title - Iterum Foods</title>
    <meta name="description" content="Your SEO-optimized description">
    <meta property="og:title" content="Iterum Foods">
    <meta property="og:description" content="Description for social media">
    <meta property="og:image" content="https://iterumfoods.xyz/og-image.jpg">
    <meta property="og:url" content="https://iterumfoods.xyz">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Iterum Foods">
    <meta name="twitter:description" content="Description">
    <meta name="twitter:image" content="https://iterumfoods.xyz/twitter-card.jpg">
</head>
```

### [ ] 5. Images & Assets

**Create/Upload:**
- Company logo (transparent PNG)
- App screenshots (high-quality)
- Team photos (if showing team)
- Open Graph image (1200x630px)
- Twitter Card image (1200x600px)
- Favicon (multiple sizes)

**Optimize:**
- Compress all images
- Use WebP format for modern browsers
- Add lazy loading for images
- Create responsive image sets

### [ ] 6. Performance Optimization

**CDN Usage:**
- Use CDN for fonts (already configured)
- Use CDN for Font Awesome (already configured)
- Consider CDN for images (Cloudflare, etc.)

**Minimize Assets:**
- Minify CSS
- Minify JavaScript
- Compress HTML (optional)

**Caching:**
```html
<!-- Add to .htaccess or server config -->
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

### [ ] 7. Security

**HTTPS:**
- Ensure SSL certificate is installed
- Force HTTPS redirects

**Security Headers:**
```
Content-Security-Policy: default-src 'self'
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

### [ ] 8. Mobile Testing

Test on:
- iPhone (Safari)
- Android (Chrome)
- iPad/Tablet
- Different screen sizes

Check:
- Touch targets are large enough
- Text is readable
- Forms work properly
- Navigation is accessible

## 📁 Hosting Options

### Option 1: Firebase Hosting (Recommended if using Firebase)
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting

# Deploy
firebase deploy --only hosting
```

**Benefits:**
- Free SSL
- Global CDN
- Easy rollback
- Custom domain support
- Integrates with Firebase Auth

### Option 2: Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
```

**Benefits:**
- Easy deployment
- Free SSL
- Form handling
- Continuous deployment from Git

### Option 3: Traditional Web Hosting
Upload via FTP/SFTP to providers like:
- Bluehost
- HostGator
- SiteGround
- DigitalOcean

### Option 4: Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**Benefits:**
- Zero config
- Free SSL
- Global CDN
- Git integration

## 🌐 Domain Configuration

### DNS Settings

Point your domain to your hosting:

**For Firebase Hosting:**
```
Type: A
Name: @
Value: (Firebase will provide IPs)

Type: TXT
Name: @
Value: (Firebase verification code)
```

**For Subdomains:**
```
app.iterumfoods.xyz -> Your app hosting
blog.iterumfoods.xyz -> Your blog hosting
```

### SSL Certificate
- Most modern hosts provide free Let's Encrypt SSL
- Ensure auto-renewal is enabled
- Verify HTTPS is working after setup

## 📊 Post-Deployment

### [ ] 1. Test Everything

**Functionality:**
- [ ] All links work
- [ ] Forms submit correctly
- [ ] Authentication flows work
- [ ] Images load properly
- [ ] No console errors

**Performance:**
- [ ] Run Google PageSpeed Insights
- [ ] Check GTmetrix score
- [ ] Test loading speed
- [ ] Verify mobile performance

**SEO:**
- [ ] Submit sitemap to Google Search Console
- [ ] Verify structured data
- [ ] Check meta tags
- [ ] Test social media previews

### [ ] 2. Set Up Monitoring

**Analytics:**
- Google Analytics (already configured)
- Set up goals and conversions
- Track user journeys
- Monitor bounce rate

**Uptime Monitoring:**
- UptimeRobot (free)
- Pingdom
- StatusCake

**Error Tracking:**
- Sentry
- Rollbar
- LogRocket

### [ ] 3. Marketing Setup

**Email Marketing:**
- Set up email capture forms
- Connect to Mailchimp/ConvertKit
- Create welcome email sequence

**Social Media:**
- Share launch announcement
- Update all social profiles
- Add website links

**SEO:**
- Submit to Google Search Console
- Submit to Bing Webmaster Tools
- Create and submit sitemap.xml
- Create robots.txt

## 🎨 Customization Ideas

### Add More Sections

**Pricing Page:**
```html
<section id="pricing">
    <!-- Add pricing tiers for each platform -->
</section>
```

**About Page:**
```html
<section id="about">
    <!-- Team, mission, vision -->
</section>
```

**Blog/Resources:**
- Recipe tips
- Restaurant management advice
- Platform tutorials
- Case studies

**Customer Testimonials:**
```html
<section id="testimonials">
    <!-- Real customer reviews -->
    <!-- Video testimonials -->
    <!-- Case studies -->
</section>
```

### Interactive Elements

**Product Demos:**
- Embed demo videos
- Interactive screenshots
- Live platform tours

**Lead Capture:**
- Exit-intent popups
- Email newsletter signup
- Free resource downloads

**Live Chat:**
- Intercom
- Drift
- Tawk.to (free)

## 🔄 Ongoing Maintenance

### Regular Updates
- [ ] Update content quarterly
- [ ] Add new testimonials
- [ ] Refresh screenshots
- [ ] Update pricing (if changed)
- [ ] Add new features

### Performance
- [ ] Monitor site speed monthly
- [ ] Optimize images as needed
- [ ] Update dependencies
- [ ] Check broken links

### Security
- [ ] Update SSL certificates (auto-renew)
- [ ] Keep CMS/plugins updated
- [ ] Regular security scans
- [ ] Backup regularly

## 📞 Need Help?

### Resources
- [Firebase Hosting Docs](https://firebase.google.com/docs/hosting)
- [Netlify Docs](https://docs.netlify.com/)
- [Google Analytics Setup](https://analytics.google.com/)
- [SEO Best Practices](https://developers.google.com/search/docs)

### Support Checklist
Before asking for help:
1. Check browser console for errors
2. Verify all URLs are correct
3. Test in incognito mode
4. Clear cache and cookies
5. Try different browser

---

## 🎉 Quick Deploy Commands

### Deploy to Firebase
```bash
cd landing-pages
firebase init
firebase deploy
```

### Deploy to Netlify
```bash
cd landing-pages
netlify deploy --prod
```

### Deploy to Vercel
```bash
cd landing-pages
vercel --prod
```

---

**Good luck with your deployment!** 🚀

Your landing pages are well-organized and ready to showcase Iterum Foods to the world. Don't forget to celebrate when you go live! 🎉

