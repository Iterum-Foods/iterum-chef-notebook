# 🎯 LAUNCH USTA FOR TESTING - Simple Guide

## ✅ 3-Minute Launch

---

## 🚀 OPTION 1: Quick Launch (Easiest)

### **Step 1: Open PowerShell**
- Press `Windows Key`
- Type "PowerShell"
- Click it

### **Step 2: Navigate to Project**
```powershell
cd "C:\Users\chefm\Iterum Innovation\Skills App"
```

### **Step 3: Install Requirements (First Time Only)**
```powershell
pip install -r requirements-usta.txt
```

### **Step 4: Seed Database with Test Data**
```powershell
python backend/seed_data.py
```

You'll see:
```
🌱 Seeding database...
✅ Created 5 users
✅ Created 3 challenges
✅ Created 2 videos
🎉 Database seeded successfully!

Test Login:
   Email: alex@test.com
   Password: password123
```

### **Step 5: Start Backend**
```powershell
python backend/app_usta.py
```

You'll see:
```
🔨 Usta Backend Starting...
✅ Database tables created
📍 Running on http://localhost:5000
 * Debug mode: on
```

**Leave this window open!**

### **Step 6: Test It!**

**Open new browser tab:**
```
http://localhost:5000/health
```

**Should see:**
```json
{
  "status": "healthy",
  "service": "usta-api",
  "version": "1.0.0"
}
```

**✅ Backend is working!**

### **Step 7: Open Frontend**

**Open these in browser:**
- `C:\Users\chefm\Iterum Innovation\Skills App\usta-demo-app.html`
- `C:\Users\chefm\Iterum Innovation\Skills App\usta-discover-people.html`
- `C:\Users\chefm\Iterum Innovation\Skills App\usta-onboarding.html`

**Or use the live deployed version:**
- https://usta-app-a86db.web.app/demo.html
- https://usta-app-a86db.web.app/discover.html

---

## 🚀 OPTION 2: One-Click Launch

### **Just Double-Click:**
```
START-USTA-BACKEND.bat
```

Then open HTML files or visit:
https://usta-app-a86db.web.app/

---

## 🧪 What to Test

### **Test 1: Backend Health**
1. Start backend (step 5 above)
2. Visit: http://localhost:5000/health
3. Should show: `"status": "healthy"`

**✅ PASS:** Backend is running

---

### **Test 2: User Registration (API)**

**PowerShell (new window):**
```powershell
curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -Body '{"username":"testuser","email":"test@test.com","password":"test123","industry":"tech"}'
```

**Should return:**
```json
{
  "message": "User created successfully",
  "token": "eyJ0eXAi...",
  "user": {...}
}
```

**✅ PASS:** Can create users

---

### **Test 3: Login**

```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -Body '{"email":"alex@test.com","password":"password123"}'
```

**Should return token and user data**

**✅ PASS:** Authentication working

---

### **Test 4: Get Video Feed**

```powershell
curl http://localhost:5000/api/videos/feed
```

**Should return videos array**

**✅ PASS:** Video API working

---

### **Test 5: Discover Users**

```powershell
curl http://localhost:5000/api/users/discover
```

**Should return master ustas and rising stars**

**✅ PASS:** Discovery working

---

### **Test 6: Frontend Pages**

**Open each page and check:**

1. **Demo Feed** - Videos display
2. **Discover** - Shows master ustas
3. **Profile** - Shows user info
4. **Recording Interface** - Camera guides show
5. **Onboarding** - 4 steps work
6. **Landing** - All sections display

**✅ PASS:** All pages render

---

## 🌐 Live Testing (Already Deployed)

### **You can also test on the live site:**

**No backend needed, just visit:**
```
https://usta-app-a86db.web.app/demo.html
https://usta-app-a86db.web.app/discover.html
https://usta-app-a86db.web.app/record.html
https://usta-app-a86db.web.app/profile.html
https://usta-app-a86db.web.app/landing.html
```

**All pages are live and working!**

---

## 📱 Test on Phone

### **Option 1: Open on Phone Browser**
1. Open phone browser
2. Visit: https://usta-app-a86db.web.app/demo.html
3. Add to home screen
4. Use like an app!

### **Option 2: QR Code**
1. Create QR code for: https://usta-app-a86db.web.app/
2. Scan with phone
3. Opens mobile-optimized site

---

## 🐛 Troubleshooting

### **Problem: "python not found"**
**Solution:**
```powershell
# Check if Python installed
python --version

# If not, download from python.org
# Then add to PATH
```

### **Problem: "pip not found"**
**Solution:**
```powershell
python -m ensurepip
```

### **Problem: "Module not found"**
**Solution:**
```powershell
pip install -r requirements-usta.txt
```

### **Problem: "Port 5000 already in use"**
**Solution:**
- Close other apps using port 5000
- Or change port in `app_usta.py`: `app.run(port=5001)`

### **Problem: "Database locked"**
**Solution:**
- Close other Python processes
- Delete `usta.db` and re-seed
- Restart backend

---

## 🎯 Complete Testing Checklist

### **Backend Testing:**
- [ ] Backend starts successfully
- [ ] Health endpoint responds
- [ ] Database created (usta.db exists)
- [ ] Seed data loads
- [ ] Can register user
- [ ] Can login user
- [ ] Token authentication works
- [ ] Video feed returns data
- [ ] Challenges return data
- [ ] Discover users works

### **Frontend Testing:**
- [ ] All pages load without errors
- [ ] Navigation between pages works
- [ ] Mobile responsive (resize browser)
- [ ] Buttons and links work
- [ ] Forms display correctly
- [ ] Images/icons load
- [ ] Animations smooth
- [ ] No console errors

### **Integration Testing:**
- [ ] API client loads
- [ ] Can call backend from frontend
- [ ] Auth flow works end-to-end
- [ ] Data displays correctly
- [ ] Forms submit to backend
- [ ] Real-time updates work

---

## 🎉 Quick Start Summary

### **Fastest Way to Test:**

**Backend:**
```bash
cd "Skills App"
python backend/seed_data.py
python backend/app_usta.py
```

**Frontend:**
```
Visit: https://usta-app-a86db.web.app/
```

**Test:**
- Browse pages
- Check navigation
- See all features
- Show to others!

---

## 👥 Share with Testers

### **Send them this link:**
```
https://usta-app-a86db.web.app/

"Check out Usta - where craftspeople master skills together!

Try:
• Demo feed (swipe through skills)
• Discover page (find master craftspeople)
• Recording interface (see how easy it is)
• Profile examples

Give me feedback!"
```

---

## 📊 What to Test For

### **User Experience:**
- Is navigation intuitive?
- Do buttons work as expected?
- Are instructions clear?
- Is it fun to use?
- Would you come back daily?

### **Design:**
- Does it look professional?
- Is branding consistent?
- Are colors appealing?
- Is text readable?
- Does it feel modern?

### **Features:**
- Are all features useful?
- Is anything confusing?
- What's missing?
- What would you add?
- What would you remove?

### **Mobile:**
- Works well on phone?
- Touch targets big enough?
- Scrolling smooth?
- Text size good?
- Loads fast?

---

## 🎯 Next Steps After Testing

### **Collect Feedback:**
1. What do people love?
2. What's confusing?
3. What features needed?
4. What should change?

### **Then:**
- Fix critical issues
- Add requested features
- Improve based on feedback
- Iterate quickly

---

## ✅ YOU'RE READY TO TEST!

**Backend:** Run locally for API testing  
**Frontend:** Live on Firebase for UI testing  
**Both:** Can work together  

**Just start the backend and open pages!**

---

**🔨 Ready to launch for testing!**

**Quickest start:**
```bash
cd "Skills App"
python backend/app_usta.py
```

Then visit: **https://usta-app-a86db.web.app/** 🚀

