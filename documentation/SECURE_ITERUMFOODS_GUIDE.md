# 🔐 Securing iterumfoods.xyz with HTTPS

## Current Status Check

Your domain: `www.iterumfoods.xyz` 
CNAME file detected in `/docs/` - appears to be using GitHub Pages or similar hosting.

## 🚀 **Quick HTTPS Setup Options**

### **Option 1: GitHub Pages (If currently hosting there)**

If you're using GitHub Pages, HTTPS is automatic for custom domains:

1. **Go to your GitHub repository settings**
   ```
   Repository → Settings → Pages
   ```

2. **Custom Domain Section**
   - Domain should show: `www.iterumfoods.xyz`
   - Check "Enforce HTTPS" checkbox
   - GitHub will automatically provision SSL certificate

3. **Verify DNS Settings**
   ```bash
   # Your domain should have these DNS records:
   www.iterumfoods.xyz → CNAME → <username>.github.io
   iterumfoods.xyz → A → 185.199.108.153
   iterumfoods.xyz → A → 185.199.109.153
   iterumfoods.xyz → A → 185.199.110.153
   iterumfoods.xyz → A → 185.199.111.153
   ```

4. **Wait for SSL Provisioning**
   - Usually takes 5-15 minutes
   - GitHub uses Let's Encrypt certificates
   - Auto-renews before expiration

---

### **Option 2: CloudFlare (Free SSL + Performance)**

CloudFlare provides free SSL certificates and CDN:

1. **Sign up at CloudFlare.com**
2. **Add your domain**: `iterumfoods.xyz`
3. **Update nameservers** (CloudFlare will provide these)
4. **Configure SSL Settings**:
   - SSL/TLS → Overview → **Full (Strict)**
   - SSL/TLS → Edge Certificates → **Always Use HTTPS: ON**
5. **Create Page Rules** (optional):
   - Pattern: `http://iterumfoods.xyz/*`
   - Setting: Always Use HTTPS

**Benefits:**
- ✅ Free SSL certificate
- ✅ CDN for faster loading
- ✅ DDoS protection
- ✅ Analytics and caching

---

### **Option 3: Custom Server Deployment**

If you want to host the full Iterum app on your domain:

#### **Using DigitalOcean/Linode/AWS**

1. **Deploy your app to a server**
2. **Install Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

3. **Configure domain DNS**
   ```
   A record: iterumfoods.xyz → YOUR_SERVER_IP
   A record: www.iterumfoods.xyz → YOUR_SERVER_IP
   ```

4. **Install Certbot for Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

5. **Create Nginx configuration**
   ```nginx
   # /etc/nginx/sites-available/iterumfoods
   server {
       listen 80;
       server_name iterumfoods.xyz www.iterumfoods.xyz;
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name iterumfoods.xyz www.iterumfoods.xyz;
       
       # Frontend (your main app)
       location / {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       # Backend API
       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

6. **Enable site and get SSL**
   ```bash
   sudo ln -s /etc/nginx/sites-available/iterumfoods /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo certbot --nginx -d iterumfoods.xyz -d www.iterumfoods.xyz
   ```

7. **Setup auto-renewal**
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

---

### **Option 4: Netlify (Easy Deployment)**

1. **Connect your GitHub repository to Netlify**
2. **Set custom domain**: `www.iterumfoods.xyz`
3. **Netlify automatically provisions SSL**
4. **Update DNS**:
   ```
   www.iterumfoods.xyz → CNAME → <your-site>.netlify.app
   iterumfoods.xyz → ALIAS → <your-site>.netlify.app
   ```

---

### **Option 5: Vercel (Next.js optimized)**

1. **Deploy to Vercel**
2. **Add custom domain** in dashboard
3. **Update DNS records** as instructed
4. **SSL automatically provisioned**

---

## 🔍 **Check Current SSL Status**

Run these commands to check your current setup:

```bash
# Check if SSL is already working
curl -I https://www.iterumfoods.xyz

# Check SSL certificate details
openssl s_client -connect www.iterumfoods.xyz:443 -servername www.iterumfoods.xyz

# Online SSL checkers
# https://www.ssllabs.com/ssltest/analyze.html?d=www.iterumfoods.xyz
# https://www.ssl.com/ssl-certificate-checker/
```

---

## 🎯 **Recommended Approach**

Based on your current setup with the CNAME file:

### **If using GitHub Pages (most likely):**
1. ✅ Go to GitHub repo settings
2. ✅ Enable "Enforce HTTPS" 
3. ✅ Wait 10-15 minutes
4. ✅ Test: https://www.iterumfoods.xyz

### **If you want better performance:**
1. ✅ Set up CloudFlare (keeps GitHub Pages hosting)
2. ✅ Get free SSL + CDN + analytics
3. ✅ Better for production traffic

### **If you want to host the full app:**
1. ✅ Deploy to DigitalOcean/AWS
2. ✅ Use the Nginx + Let's Encrypt setup
3. ✅ Full control over the application

---

## 🚨 **Update Your Code for HTTPS**

Once SSL is enabled, update your API configuration:

### **Update apiConfig.js** (already done ✅)
Your `apiConfig.js` now automatically detects HTTPS and adjusts URLs.

### **Update CORS settings**
```python
# app/main.py - Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://iterumfoods.xyz", "https://www.iterumfoods.xyz"],  # Specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Force HTTPS redirects** (if self-hosting)
```python
# Add to app/main.py
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Add before CORS middleware
app.add_middleware(HTTPSRedirectMiddleware)
```

---

## ✅ **Quick Action Plan**

1. **Right now**: Check if you're using GitHub Pages
   ```bash
   # Look at your repository settings → Pages section
   ```

2. **Enable HTTPS** (if GitHub Pages):
   - Repository Settings → Pages → Check "Enforce HTTPS"

3. **Test your site**:
   - Visit: https://www.iterumfoods.xyz
   - Look for green lock icon 🔒

4. **If not working**: 
   - Try CloudFlare option (keeps current setup, adds SSL)

5. **Verify SSL Certificate**:
   - Use: https://www.ssllabs.com/ssltest/analyze.html?d=www.iterumfoods.xyz

---

## 🔧 **Troubleshooting**

### **Common Issues:**

**"Site can't be reached"**
- Check DNS propagation: https://dnschecker.org
- Verify CNAME/A records are correct

**"Not Secure" warning**
- SSL certificate not yet provisioned
- Wait 15-30 minutes after enabling
- Clear browser cache

**Mixed content errors**
- Update all HTTP links to HTTPS
- Check for hardcoded HTTP URLs in your code

**Certificate errors**
- Domain mismatch (check www vs non-www)
- Certificate not yet active
- Try incognito/private browsing mode

---

**Which hosting platform are you currently using for iterumfoods.xyz?** This will help me give you the most specific steps to enable HTTPS immediately.