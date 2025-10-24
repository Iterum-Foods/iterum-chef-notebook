# 🎯 Create GitHub Repository - Step by Step

## ✅ Your code is ready! Just need to create the GitHub repo.

---

## 📝 Steps (5 minutes)

### **Step 1: Go to GitHub**

Click this link: **https://github.com/new**

(You'll need to sign in if you're not already)

---

### **Step 2: Fill in Repository Details**

On the "Create a new repository" page:

```
Repository name: usta-backend

Description: Backend API for Usta - Community platform for craftspeople

☑️ Private (check this box - recommended for now)

DO NOT CHECK:
☐ Add a README file (we already have one)
☐ Add .gitignore (we already have one)
☐ Choose a license (we already have one)
```

---

### **Step 3: Click "Create repository"**

Big green button at the bottom.

---

### **Step 4: GitHub shows you setup commands**

You'll see a page that says "Quick setup" with commands.

**IGNORE** the first section about creating files.

**GO TO** the section that says:
**"…or push an existing repository from the command line"**

It will show you something like:

```bash
git remote add origin https://github.com/YOUR_USERNAME/usta-backend.git
git branch -M main
git push -u origin main
```

**COPY THESE 3 COMMANDS** (they'll have YOUR username, not "YOUR_USERNAME")

---

### **Step 5: Run the Commands**

In PowerShell (still in Skills App directory), paste and run the 3 commands:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/usta-backend.git
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username!

---

### **Step 6: Enter Credentials**

When prompted:
- Username: Your GitHub username
- Password: Your GitHub password (or Personal Access Token if you have 2FA)

**If you have 2-Factor Authentication:**
You need a Personal Access Token instead of password.
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Give it a name: "Usta Backend Deploy"
- Select scopes: ✅ repo (full control)
- Click "Generate token"
- Copy the token
- Use this as your password when pushing

---

### **Step 7: Verify Upload**

After the push completes:

1. Go to: https://github.com/YOUR_USERNAME/usta-backend
2. You should see all your files!
3. ✅ **SUCCESS!**

---

## 🎉 Done! What's Next?

**Tell me:** ✅ "Code is on GitHub!"

**Then we'll:**
1. Deploy backend to Railway (20 min)
2. Enable Firebase Storage (5 min)
3. Connect frontend to backend (5 min)
4. **LAUNCH!** 🚀

---

## 🐛 Troubleshooting

### "Authentication failed"

**If you have 2FA enabled:**
You need a Personal Access Token (see Step 6 above)

**If you don't have 2FA:**
Just use your regular GitHub password

### "Repository already exists"

That's ok! You already created it. Just run:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/usta-backend.git
git push -u origin main
```

### "Remote origin already exists"

Run this first:
```powershell
git remote remove origin
```

Then try again with the commands from Step 5.

---

## 💡 Quick Checklist

- [ ] Went to https://github.com/new
- [ ] Created repository named "usta-backend"
- [ ] Set to Private
- [ ] Did NOT add README/gitignore/license
- [ ] Copied the 3 command lines
- [ ] Ran them in PowerShell
- [ ] Entered credentials
- [ ] Push completed successfully!
- [ ] Verified files on GitHub

---

## 🚀 Ready?

**Go to:** https://github.com/new

**Create the repo and run the commands!**

**Then come back and tell me:** ✅ "It's on GitHub!"

Let's get this deployed! 🎉

