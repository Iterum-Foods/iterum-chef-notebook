# 🔐 HTTPS Deployment Guide for Iterum R&D Chef Notebook

This guide covers implementing HTTPS security for both development and production environments.

## 🏠 **Local Development HTTPS**

### Quick Setup (Recommended)

1. **Install and Setup Local Certificates**
   ```bash
   python setup_https_local.py
   ```

2. **Start with HTTPS**
   ```bash
   python start_https_app.py
   ```

3. **Access Your App**
   - 🔐 Frontend: https://localhost:8080
   - 📚 API Docs: https://localhost:8000/docs
   - 💚 Health: https://localhost:8000/health

### Manual Certificate Setup

If the automated setup doesn't work:

#### Using mkcert (Recommended)

**Windows:**
```powershell
# Install mkcert
choco install mkcert
# OR
scoop bucket add extras && scoop install mkcert

# Generate certificates
mkcert -install
mkdir certs
mkcert -cert-file certs/localhost.pem -key-file certs/localhost-key.pem localhost 127.0.0.1 ::1
```

**macOS:**
```bash
# Install mkcert
brew install mkcert

# Generate certificates
mkcert -install
mkdir certs
mkcert -cert-file certs/localhost.pem -key-file certs/localhost-key.pem localhost 127.0.0.1 ::1
```

**Linux:**
```bash
# Download and install mkcert
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert

# Generate certificates
mkcert -install
mkdir certs
mkcert -cert-file certs/localhost.pem -key-file certs/localhost-key.pem localhost 127.0.0.1 ::1
```

#### Using OpenSSL (Alternative)

```bash
# Create directory for certificates
mkdir certs

# Generate private key
openssl genrsa -out certs/localhost-key.pem 2048

# Generate certificate signing request
openssl req -new -key certs/localhost-key.pem -out certs/localhost.csr -subj "/CN=localhost"

# Generate self-signed certificate
openssl x509 -req -in certs/localhost.csr -signkey certs/localhost-key.pem -out certs/localhost.pem -days 365

# Clean up
rm certs/localhost.csr
```

**Note:** OpenSSL certificates will show "Not Secure" warnings in browsers. Use mkcert for trusted certificates.

---

## 🌐 **Production HTTPS Deployment**

### Option 1: Using Let's Encrypt (Free SSL)

#### Prerequisites
- Domain name pointing to your server
- Port 80 and 443 accessible
- Nginx or Apache web server

#### Setup with Nginx

1. **Install Certbot**
   ```bash
   # Ubuntu/Debian
   sudo apt install certbot python3-certbot-nginx
   
   # CentOS/RHEL
   sudo yum install certbot python3-certbot-nginx
   ```

2. **Create Nginx Configuration**
   ```nginx
   # /etc/nginx/sites-available/iterum
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name your-domain.com;
       
       # SSL Configuration (certbot will add these)
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
       
       # Frontend
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
       
       # API docs
       location /docs {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable Site and Get Certificate**
   ```bash
   sudo ln -s /etc/nginx/sites-available/iterum /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo certbot --nginx -d your-domain.com
   ```

4. **Setup Auto-Renewal**
   ```bash
   sudo crontab -e
   # Add this line:
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

### Option 2: Cloud Platform SSL

#### Heroku
```bash
# Enable automatic certificate management
heroku certs:auto:enable -a your-app-name
```

#### Vercel
```bash
# Vercel automatically provides SSL
vercel --prod
```

#### AWS (with ALB)
- Use AWS Certificate Manager (ACM)
- Configure Application Load Balancer with SSL termination

#### DigitalOcean App Platform
- SSL certificates are automatically provisioned

### Option 3: CloudFlare (Free SSL + CDN)

1. **Sign up for CloudFlare**
2. **Add your domain**
3. **Update nameservers**
4. **Enable SSL/TLS**
   - SSL/TLS → Overview → Full (strict)
5. **Configure Page Rules** (optional)
   - Always Use HTTPS

---

## ⚙️ **Environment Configuration**

### Update Environment Variables

Add to your `.env` file:

```env
# HTTPS Configuration
HTTPS_ENABLED=true
SSL_CERT_PATH=./certs/localhost.pem
SSL_KEY_PATH=./certs/localhost-key.pem

# For production
# SSL_CERT_PATH=/etc/letsencrypt/live/your-domain.com/fullchain.pem
# SSL_KEY_PATH=/etc/letsencrypt/live/your-domain.com/privkey.pem
```

### Update Settings

```python
# app/core/settings.py additions
class Settings(BaseSettings):
    # ... existing settings ...
    
    # HTTPS settings
    https_enabled: bool = Field(default=False, env="HTTPS_ENABLED")
    ssl_cert_path: str = Field(default="./certs/localhost.pem", env="SSL_CERT_PATH")
    ssl_key_path: str = Field(default="./certs/localhost-key.pem", env="SSL_KEY_PATH")
```

---

## 🔧 **Testing Your HTTPS Setup**

### Local Testing
```bash
# Test backend API
curl -k https://localhost:8000/health

# Test frontend
curl -k https://localhost:8080

# Check certificate (with mkcert, -k flag not needed)
curl https://localhost:8000/health
```

### Production Testing
```bash
# Check SSL certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Test with curl
curl https://your-domain.com/health

# SSL Labs test (online)
# Visit: https://www.ssllabs.com/ssltest/
```

### Browser Testing
- ✅ Green lock icon in address bar
- ✅ "Connection is secure" when clicking lock
- ✅ Certificate details show correct domain
- ❌ No mixed content warnings

---

## 🚨 **Troubleshooting**

### Common Issues

#### "NET::ERR_CERT_AUTHORITY_INVALID"
- **Cause**: Self-signed certificate or mkcert not installed properly
- **Solution**: Ensure mkcert is installed: `mkcert -install`

#### "Mixed Content" Errors
- **Cause**: HTTPS page loading HTTP resources
- **Solution**: Update all URLs to use HTTPS

#### Certificate Expired
- **Local**: Regenerate with mkcert
- **Production**: Check auto-renewal setup

#### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # or :8080

# Kill process
kill -9 <PID>
```

### Debugging Commands

```bash
# Check certificate validity
openssl x509 -in certs/localhost.pem -text -noout

# Test SSL connection
openssl s_client -connect localhost:8000

# Check nginx configuration
sudo nginx -t

# View nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## 📋 **Security Best Practices**

### SSL/TLS Configuration
- Use TLS 1.2 or higher
- Strong cipher suites only
- Enable HSTS headers
- Implement OCSP stapling

### Nginx Security Headers
```nginx
# Add to your server block
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
```

### Application Security
- Never log or display SSL private keys
- Keep certificates updated
- Monitor certificate expiration
- Use environment variables for sensitive data

---

## 📈 **Performance Considerations**

### HTTPS Optimizations
- Enable HTTP/2
- Use SSL session resumption
- Implement OCSP stapling
- Consider CDN with SSL termination

### Monitoring
- Set up certificate expiration alerts
- Monitor SSL handshake performance
- Track HTTPS adoption metrics

---

## 🎯 **Quick Start Commands**

```bash
# Local HTTPS development (complete setup)
python setup_https_local.py && python start_https_app.py

# Production deployment (nginx + Let's Encrypt)
sudo certbot --nginx -d your-domain.com

# Test everything is working
curl https://your-domain.com/health
```

---

**Next Steps:**
1. Choose your deployment method (local/production)
2. Run the setup commands
3. Test your HTTPS implementation
4. Monitor certificate expiration
5. Enjoy secure connections! 🔐