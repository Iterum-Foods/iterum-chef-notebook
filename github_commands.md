# 📋 Manual GitHub Setup Commands

If you prefer to set up GitHub manually or the batch file doesn't work, here are the step-by-step commands:

## 🔧 Prerequisites

1. **Install Git**: Download from https://git-scm.com/download/windows
2. **Create GitHub Account**: Sign up at https://github.com
3. **Configure Git** (replace with your details):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## 📚 Step-by-Step Setup

### 1. Initialize Git Repository
```bash
# Navigate to your project directory
cd "C:\Users\chefm\my-culinary-app\Iterum App"

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Iterum R&D Chef Notebook v2.0"
```

### 2. Create GitHub Repository
1. Go to https://github.com/new
2. **Repository name**: `iterum-chef-notebook`
3. **Description**: `Revolutionary culinary management platform for professional kitchens`
4. **Visibility**: Public (recommended for open source) or Private
5. **DO NOT** check "Add a README file" (we already have one)
6. **DO NOT** check "Add .gitignore" (we already have one)
7. **License**: Choose "MIT License" or leave blank
8. Click **"Create repository"**

### 3. Connect Local Repository to GitHub
```bash
# Add GitHub repository as remote origin
# Replace 'yourusername' with your actual GitHub username
git remote add origin https://github.com/yourusername/iterum-chef-notebook.git

# Rename main branch (modern Git standard)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 4. Authentication Options

#### Option A: Personal Access Token (Recommended)
1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Note**: "Iterum R&D Chef Notebook"
4. **Expiration**: Choose your preference (90 days recommended)
5. **Scopes**: Check `repo` and `workflow`
6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)
8. When Git asks for password, **use the token instead**

#### Option B: GitHub CLI
```bash
# Install GitHub CLI from https://cli.github.com/
# Then authenticate
gh auth login
# Follow the prompts to authenticate via web browser
```

### 5. Verify Setup
```bash
# Check remote connection
git remote -v

# Check repository status
git status

# View your repository
# Replace 'yourusername' with your GitHub username
start https://github.com/yourusername/iterum-chef-notebook
```

## 🌐 Setting Up GitHub Pages (Optional)

To host your marketing website for free on GitHub Pages:

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section
4. **Source**: Deploy from a branch
5. **Branch**: main
6. **Folder**: / (root)
7. Click **Save**

Your marketing site will be available at:
`https://yourusername.github.io/iterum-chef-notebook/landing_page.html`

## 📝 Repository Configuration

### Add Repository Description and Topics
1. Go to your repository main page
2. Click the ⚙️ gear icon next to "About"
3. **Description**: "Revolutionary culinary management platform for professional kitchens with AI-powered recipe intelligence and smart ingredient tracking"
4. **Website**: Your deployed URL (if available)
5. **Topics**: Add these tags:
   - `chef`
   - `cooking`
   - `recipe-management`
   - `fastapi`
   - `python`
   - `restaurant`
   - `culinary`
   - `food-tech`
   - `ai`
   - `kitchen-management`

### Enable Features
- ✅ **Issues** (for bug reports and feature requests)
- ✅ **Discussions** (for community conversations)
- ✅ **Projects** (for project management)
- ✅ **Wiki** (for additional documentation)

## 🔒 Security Settings

### Branch Protection Rules
1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. **Branch name pattern**: `main`
4. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

### Security Features
1. Go to **Settings** → **Security & analysis**
2. Enable:
   - ✅ **Dependency graph**
   - ✅ **Dependabot alerts**
   - ✅ **Dependabot security updates**
   - ✅ **Secret scanning**

## 📊 Adding Collaborators

### Adding Team Members
1. Go to **Settings** → **Collaborators and teams**
2. Click **Add people**
3. Enter GitHub username or email
4. Choose permission level:
   - **Read**: Can view and clone
   - **Triage**: Can manage issues and pull requests
   - **Write**: Can push to repository
   - **Maintain**: Can manage repository settings
   - **Admin**: Full access

### Creating Teams (for Organizations)
1. Create GitHub Organization
2. Create teams (Frontend, Backend, Marketing, etc.)
3. Add team members
4. Grant team permissions to repository

## 🚀 Continuous Integration (Future)

### GitHub Actions Workflow
Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python -m pytest
        
    - name: Run linting
      run: |
        flake8 app/
```

## 🔧 Troubleshooting

### Common Issues

#### Error: "repository not found"
- Check repository name spelling
- Verify you have access to the repository
- Ensure you're authenticated properly

#### Error: "failed to push"
- Check if branch protection rules are blocking
- Verify you have write permissions
- Try authenticating with personal access token

#### Error: "remote origin already exists"
```bash
# Remove existing remote and add new one
git remote remove origin
git remote add origin https://github.com/yourusername/iterum-chef-notebook.git
```

#### Large files error
```bash
# Remove large files from tracking
git rm --cached large-file.db
echo "*.db" >> .gitignore
git add .gitignore
git commit -m "Remove database files from tracking"
```

### Getting Help
- **GitHub Docs**: https://docs.github.com/
- **Git Documentation**: https://git-scm.com/doc
- **GitHub Community**: https://github.community/

## 📞 Next Steps

After your repository is set up:

1. **⭐ Star your own repository** (shows activity)
2. **📝 Create your first issue** (roadmap or bug)
3. **🔀 Make your first pull request** (small improvement)
4. **📢 Share with the community** (social media, forums)
5. **🚀 Set up automated deployment** (Heroku, Netlify, etc.)

## 🎉 Success!

Your Iterum R&D Chef Notebook is now on GitHub! 

**Repository URL**: `https://github.com/yourusername/iterum-chef-notebook`

Welcome to the open-source culinary technology community! 🍅👨‍🍳