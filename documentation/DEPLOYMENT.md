# 🚀 Deployment Guide

This guide covers various deployment options for Iterum R&D Chef Notebook, from local development to production environments.

## 📋 Quick Start Options

### Option 1: Local Development (Recommended for Testing)
```bash
# Clone and setup
git clone https://github.com/yourusername/iterum-chef-notebook.git
cd iterum-chef-notebook
pip install -r requirements.txt

# Launch (all-in-one)
python launch_marketing.py

# Or manual launch
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
python serve_frontend.py
```

### Option 2: GitHub Pages (Marketing Site Only)
1. Fork the repository
2. Go to Settings > Pages
3. Source: Deploy from branch `main`
4. Your site will be available at: `https://username.github.io/iterum-chef-notebook/`

### Option 3: One-Click Heroku Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/iterum-chef-notebook)

## 🖥️ Production Deployment

### Prerequisites
- Python 3.8+
- Domain name (optional)
- SSL certificate (recommended)
- Database backup strategy

### Environment Setup
```bash
# Create production environment file
cp .env.example .env.production

# Edit with production values
nano .env.production
```

### Required Environment Variables
```env
# Application
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=sqlite:///./production.db
# Or PostgreSQL: postgresql://user:password@localhost/dbname

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Analytics (optional)
GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID

# Security
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## ☁️ Cloud Platform Deployment

### 1. Heroku

#### Automatic Deployment
1. Click the "Deploy to Heroku" button above
2. Configure environment variables
3. Deploy and open app

#### Manual Deployment
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main

# Open app
heroku open
```

#### Heroku Files Needed
Create `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: python create_preloaded_ingredients.py
```

Create `runtime.txt`:
```
python-3.11.7
```

### 2. DigitalOcean App Platform

#### Create `app.yaml`:
```yaml
name: iterum-chef-notebook
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/iterum-chef-notebook
    branch: main
  run_command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: ENVIRONMENT
    value: production
  - key: SECRET_KEY
    value: your-secret-key
    type: SECRET
```

Deploy:
```bash
doctl apps create --spec app.yaml
```

### 3. Google Cloud Platform

#### App Engine Deployment
Create `app.yaml`:
```yaml
runtime: python311

env_variables:
  ENVIRONMENT: production
  SECRET_KEY: your-secret-key

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto
```

Deploy:
```bash
gcloud app deploy
```

#### Cloud Run Deployment
```bash
# Build and deploy
gcloud run deploy iterum-chef-notebook \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

### 4. AWS

#### Elastic Beanstalk
Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app.main:app
  aws:elasticbeanstalk:application:environment:
    ENVIRONMENT: production
    SECRET_KEY: your-secret-key
```

Deploy:
```bash
eb init -p python-3.11 iterum-chef-notebook
eb create production
eb deploy
```

#### ECS/Fargate
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and push:
```bash
docker build -t iterum-chef-notebook .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
docker tag iterum-chef-notebook:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/iterum-chef-notebook:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/iterum-chef-notebook:latest
```

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - SECRET_KEY=your-secret-key
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./static:/var/www/static:ro
    depends_on:
      - web
    restart: unless-stopped
```

### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Scale application
docker-compose up -d --scale web=3
```

## 🌐 Traditional Server Deployment

### Ubuntu/Debian Setup

#### 1. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx supervisor -y

# Install Node.js (for frontend tools)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. Setup Application
```bash
# Create app directory
sudo mkdir -p /var/www/iterum-chef-notebook
cd /var/www/iterum-chef-notebook

# Clone repository
sudo git clone https://github.com/yourusername/iterum-chef-notebook.git .

# Create virtual environment
sudo python3 -m venv venv
sudo ./venv/bin/pip install -r requirements.txt

# Set permissions
sudo chown -R www-data:www-data /var/www/iterum-chef-notebook
```

#### 3. Configure Supervisor
Create `/etc/supervisor/conf.d/iterum-chef-notebook.conf`:
```ini
[program:iterum-chef-notebook]
command=/var/www/iterum-chef-notebook/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
directory=/var/www/iterum-chef-notebook
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/iterum-chef-notebook.log
environment=ENVIRONMENT="production",SECRET_KEY="your-secret-key"
```

Start service:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start iterum-chef-notebook
```

#### 4. Configure Nginx
Create `/etc/nginx/sites-available/iterum-chef-notebook`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/iterum-chef-notebook/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/iterum-chef-notebook /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 5. SSL with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### CentOS/RHEL Setup
Similar process but use `yum`/`dnf` instead of `apt`:
```bash
sudo dnf update -y
sudo dnf install python3 python3-pip nginx supervisor -y
```

## 📊 Monitoring & Maintenance

### Health Checks
The application includes health check endpoints:
- `/health` - Basic health check
- `/api/health` - API health check

### Logging
Configure structured logging:
```python
# In production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/iterum-chef-notebook.log',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Database Backups
```bash
# SQLite backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/www/iterum-chef-notebook/iterum_rnd.db /backups/iterum_rnd_${DATE}.db
cp /var/www/iterum-chef-notebook/culinary_data.db /backups/culinary_data_${DATE}.db
cp /var/www/iterum-chef-notebook/waitlist.db /backups/waitlist_${DATE}.db

# Keep only last 30 days
find /backups -name "*.db" -mtime +30 -delete
```

### Monitoring with Prometheus
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'iterum-chef-notebook'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill process
sudo kill -9 <PID>
```

#### Permission Denied
```bash
# Fix file permissions
sudo chown -R www-data:www-data /var/www/iterum-chef-notebook
sudo chmod -R 755 /var/www/iterum-chef-notebook
```

#### Database Locked
```bash
# Check for hanging processes
ps aux | grep python
# Restart application
sudo supervisorctl restart iterum-chef-notebook
```

### Performance Optimization

#### Enable Gzip Compression
```nginx
# In nginx.conf
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript;
```

#### Use CDN for Static Files
```python
# In settings
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

#### Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_recipes_user_id ON recipes(user_id);
CREATE INDEX idx_ingredients_category ON ingredients(category);
```

## 📞 Support

### Getting Help
- **Documentation**: Check this guide and README.md
- **Issues**: GitHub Issues for bugs and features
- **Email**: hello@iterum-chef.com for deployment support
- **Community**: GitHub Discussions for questions

### Professional Deployment Support
For enterprise deployments:
- Custom deployment configurations
- Load balancing and scaling
- High availability setups
- Performance optimization
- Security hardening

Contact us at enterprise@iterum-chef.com

---

**🍅 Happy Deploying! Your professional kitchen management platform is ready to serve the world! 🍅**