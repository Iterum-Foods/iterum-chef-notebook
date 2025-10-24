# 🚂 Deploy to Railway - Step by Step

## ✅ Your code is on GitHub! Now let's deploy it to Railway.

**GitHub Repository:** https://github.com/chefmatt2024/usta-backend

---

## 📝 Steps (20 minutes)

### **Step 1: Create Railway Account**

Click this link: **https://railway.app/**

1. Click **"Login"** or **"Start a New Project"**
2. Choose **"Sign in with GitHub"**
3. Authorize Railway to access your GitHub account
4. ✅ **Account created!**

---

### **Step 2: Create New Project**

1. You'll land on the Railway dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. You'll see a list of your repositories
5. Find and click **"chefmatt2024/usta-backend"**
6. ✅ **Railway starts building!**

Railway will automatically:
- Detect your Dockerfile
- Build the container
- Deploy it
- Give you a URL

**Wait 2-3 minutes for the first build to complete.**

---

### **Step 3: Add PostgreSQL Database**

1. In your Railway project page, click **"+ New"** button
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Railway creates the database
5. ✅ **Database is automatically linked to your backend!**

Railway automatically sets the `DATABASE_URL` environment variable!

---

### **Step 4: Set Environment Variables**

1. Click on your **backend service** (not the PostgreSQL database)
2. Go to **"Variables"** tab
3. Click **"New Variable"** button

**Add these variables ONE BY ONE:**

**Variable 1:**
```
Name: FLASK_APP
Value: backend/app_usta.py
```

**Variable 2:**
```
Name: FLASK_ENV
Value: production
```

**Variable 3:** (Generate a random key first!)
```
Name: SECRET_KEY
Value: [PASTE GENERATED KEY HERE]
```

**Variable 4:** (Generate another random key!)
```
Name: JWT_SECRET_KEY
Value: [PASTE GENERATED KEY HERE]
```

**Variable 5:**
```
Name: FRONTEND_URL
Value: https://usta-app-a86db.web.app
```

**Variable 6:**
```
Name: MAX_CONTENT_LENGTH
Value: 524288000
```

**Variable 7:**
```
Name: UPLOAD_FOLDER
Value: uploads
```

**Variable 8:**
```
Name: FIREBASE_STORAGE_BUCKET
Value: usta-app-a86db.appspot.com
```

**To generate SECRET_KEY and JWT_SECRET_KEY:**

Open a new PowerShell window and run this TWICE:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output each time for the two secret keys.

After adding all variables, Railway will automatically redeploy (takes 1-2 minutes).

---

### **Step 5: Generate Domain**

1. Click on your backend service
2. Go to **"Settings"** tab
3. Scroll down to **"Networking"** section
4. Click **"Generate Domain"**

You'll get a URL like:
```
https://usta-backend-production-1a2b.up.railway.app
```

**📋 COPY THIS URL!** You'll need to send it to me!

---

### **Step 6: Initialize Database**

Railway needs to set up the database tables.

1. In Railway, click your backend service
2. Click the **"..."** menu (three dots)
3. Select **"Open Terminal"** or find the terminal/shell icon
4. Wait for the terminal to open

In the terminal, run:
```bash
python init_database.py
```

You should see:
```
Creating database tables...
✅ Database initialized successfully!
```

Then run:
```bash
python backend/seed_data.py
```

You should see:
```
✅ Demo data created successfully!
```

✅ **Database is ready!**

---

### **Step 7: Test Backend**

Visit your Railway URL in a browser:
```
https://your-railway-url.up.railway.app/api/health
```

**If it works, you'll see:**
```json
{
  "status": "ok",
  "message": "Usta API is running"
}
```

✅ **Backend is LIVE!**

---

## 🎉 Success! What's Next?

**Your Railway URL is:**
```
https://usta-backend-production-XXXX.up.railway.app
```

**Send me this URL and I'll:**
1. Update the frontend to connect to your backend
2. Guide you through enabling Firebase Storage
3. Deploy the frontend
4. Test everything end-to-end
5. **GO LIVE!** 🚀

---

## 📊 Monitor Your Backend

### **View Logs**
1. Railway → Backend Service → "Deployments" tab
2. Click latest deployment → "View Logs"
3. See all API requests and errors in real-time

### **Check Metrics**
1. Backend Service → "Metrics" tab
2. See CPU, memory, network usage

### **Database Stats**
1. Click PostgreSQL service
2. See connections, queries, storage

---

## 🐛 Troubleshooting

### **Build Failed**
- Check logs for errors
- Verify Dockerfile is correct
- Make sure all files pushed to GitHub

### **Service Won't Start**
- Check environment variables are all set
- Verify DATABASE_URL exists (auto-set by Railway)
- Check logs for Python errors

### **Can't Access Domain**
- Make sure domain was generated
- Wait 1-2 minutes for DNS to propagate
- Try the railway.app domain, not custom domain

### **Database Connection Error**
- Verify PostgreSQL service is running
- Check DATABASE_URL in variables (should be auto-set)
- Run init_database.py again in terminal

---

## 💡 Quick Tips

**Automatic Deploys:**
- Push code to GitHub → Railway auto-deploys!
- No manual steps needed after initial setup

**Free Tier Limits:**
- 500 hours/month (always-on = ~16 days)
- $5 credit/month
- More than enough for beta testing!

**View Usage:**
- Railway dashboard shows remaining hours
- Set up billing before running out (if needed)

**Environment Variables:**
- Never commit secrets to GitHub!
- Always use environment variables
- Change them in Railway dashboard anytime

---

## ✅ Checklist

- [ ] Created Railway account
- [ ] Created new project from GitHub
- [ ] PostgreSQL database added
- [ ] All 8 environment variables set
- [ ] Domain generated
- [ ] Database initialized (ran init_database.py)
- [ ] Demo data seeded (ran seed_data.py)
- [ ] Health check works
- [ ] **COPIED RAILWAY URL TO SEND**

---

## 🚀 Ready to Deploy?

**Click here to start:** https://railway.app/

**Follow the steps above, then send me your Railway URL!**

Let's get this live! 🎉

