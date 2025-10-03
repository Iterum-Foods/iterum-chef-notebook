# GitHub Security Setup Guide

This guide will walk you through configuring the security features and secrets needed for the Iterum Culinary App's CI/CD pipeline.

## 🔐 Step 1: Configure GitHub Secrets

### 1.1 Access Repository Settings
1. Go to your GitHub repository: `https://github.com/Iterum-Foods/iterum-chef-notebook`
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**

### 1.2 Add Required Secrets

#### SNYK_TOKEN (Required for security scanning)
1. **Get Snyk Token**:
   - Go to [Snyk.io](https://snyk.io) and sign up/login
   - Navigate to Account Settings → API Token
   - Copy your API token

2. **Add to GitHub**:
   - Click **New repository secret**
   - Name: `SNYK_TOKEN`
   - Value: `your-snyk-api-token-here`
   - Click **Add secret**

#### SLACK_WEBHOOK_URL (Optional for notifications)
1. **Create Slack Webhook**:
   - Go to your Slack workspace
   - Navigate to Apps → Incoming Webhooks
   - Create a new webhook for your channel (e.g., #security-alerts)
   - Copy the webhook URL

2. **Add to GitHub**:
   - Click **New repository secret**
   - Name: `SLACK_WEBHOOK_URL`
   - Value: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`
   - Click **Add secret**

### 1.3 Verify Secrets
After adding secrets, you should see:
- ✅ `SNYK_TOKEN` (if added)
- ✅ `SLACK_WEBHOOK_URL` (if added)

## 👥 Step 2: Set Up Security Team

### 2.1 Create Security Team
1. Go to your GitHub organization: `https://github.com/Iterum-Foods`
2. Click **Teams** tab
3. Click **New team**
4. Team name: `security-team`
5. Description: `Security team responsible for reviewing security-related changes`
6. Visibility: **Private** (recommended)
7. Click **Create team**

### 2.2 Add Team Members
1. In the security team page, click **Add a member**
2. Add team members who should review security changes
3. Set permissions: **Write** (minimum for reviewing PRs)

### 2.3 Create Additional Teams (Optional)
- `maintainers`: Core maintainers of the project
- `backend-team`: Backend developers
- `frontend-team`: Frontend developers
- `devops-team`: DevOps and infrastructure

## 🛡️ Step 3: Enable GitHub Security Features

### 3.1 Enable Dependabot Alerts
1. Go to repository **Settings**
2. Click **Security** in left sidebar
3. Under **Code security**, click **Dependabot alerts**
4. Click **Enable Dependabot alerts**
5. Configure alert settings:
   - **Alert frequency**: Daily
   - **Email notifications**: Enabled
   - **Security updates**: Auto-merge enabled (optional)

### 3.2 Enable CodeQL Analysis
1. Go to repository **Settings**
2. Click **Security** in left sidebar
3. Under **Code security**, click **Code scanning**
4. Click **Set up code scanning**
5. Choose **Set up this workflow**
6. The workflow is already configured in `.github/workflows/test.yml`

### 3.3 Enable Security Advisories
1. Go to repository **Settings**
2. Click **Security** in left sidebar
3. Under **Reporting**, click **Security advisories**
4. Click **Enable security advisories**
5. Configure settings:
   - **Allow private reporting**: Enabled
   - **Email notifications**: Enabled

### 3.4 Configure Branch Protection
1. Go to repository **Settings**
2. Click **Branches** in left sidebar
3. Click **Add rule** for `main` branch
4. Configure protection rules:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Require conversation resolution before merging**
   - ✅ **Require signed commits** (optional)
   - ✅ **Require linear history** (optional)
   - ✅ **Include administrators** (recommended)

5. **Required status checks**:
   - `test` (from test.yml)
   - `lint` (from test.yml)
   - `security` (from test.yml)

6. **Restrict pushes**:
   - ✅ **Restrict pushes that create files**
   - ✅ **Restrict pushes that delete files**

## 🔧 Step 4: Configure Additional Settings

### 4.1 Repository Settings
1. **General Settings**:
   - **Features**: Enable Issues, Projects, Wiki (as needed)
   - **Pull Requests**: Enable merge commits, squash merging, rebase merging
   - **Pages**: Enable GitHub Pages for documentation

2. **Security Settings**:
   - **Dependency graph**: Enabled
   - **Dependabot alerts**: Enabled
   - **Code scanning**: Enabled
   - **Secret scanning**: Enabled (if available)

### 4.2 Organization Settings (If Applicable)
1. Go to organization settings: `https://github.com/Iterum-Foods`
2. **Security** tab:
   - Enable **Two-factor authentication requirement**
   - Configure **SAML single sign-on** (if applicable)
   - Enable **IP allow list** (if applicable)

## 📋 Step 5: Verify Setup

### 5.1 Test Security Scanning
1. Create a test branch: `git checkout -b test-security-setup`
2. Make a small change and push: `git push origin test-security-setup`
3. Create a pull request
4. Verify that security scans run in the Actions tab
5. Check that security team is notified for review

### 5.2 Test Dependency Updates
1. Wait for Dependabot to create a PR (usually within 24 hours)
2. Verify that the PR includes security team review
3. Test the dependency update workflow

### 5.3 Test Security Alerts
1. Check the **Security** tab for any existing alerts
2. Verify that alerts are properly categorized
3. Test the security advisory process

## 🚨 Step 6: Security Monitoring

### 6.1 Set Up Monitoring
1. **GitHub Notifications**:
   - Enable email notifications for security alerts
   - Configure notification preferences

2. **Slack Integration** (if configured):
   - Verify webhook is working
   - Test notification delivery
   - Configure channel permissions

### 6.2 Regular Maintenance
1. **Weekly Tasks**:
   - Review security scan results
   - Check for new security alerts
   - Review dependency updates

2. **Monthly Tasks**:
   - Update security team members
   - Review security policies
   - Update security documentation

## 🔍 Troubleshooting

### Common Issues

#### Security Scans Not Running
- Check that secrets are properly configured
- Verify workflow files are in the correct location
- Check GitHub Actions permissions

#### Dependabot Not Creating PRs
- Verify Dependabot is enabled
- Check `.github/dependabot.yml` configuration
- Ensure repository has proper permissions

#### Security Team Not Receiving Notifications
- Verify team members are added correctly
- Check notification settings
- Ensure team has proper permissions

### Getting Help
- **GitHub Documentation**: [GitHub Security](https://docs.github.com/en/code-security)
- **Snyk Documentation**: [Snyk GitHub Integration](https://docs.snyk.io/integrations/ci-cd-integrations/github-integration)
- **Repository Issues**: Create an issue in the repository for support

## ✅ Completion Checklist

- [ ] SNYK_TOKEN secret added
- [ ] SLACK_WEBHOOK_URL secret added (optional)
- [ ] Security team created
- [ ] Dependabot alerts enabled
- [ ] CodeQL analysis enabled
- [ ] Security advisories enabled
- [ ] Branch protection rules configured
- [ ] Security scanning tested
- [ ] Dependency updates tested
- [ ] Security monitoring configured

---

**🎉 Congratulations!** Your Iterum Culinary App now has enterprise-grade security infrastructure configured and ready to protect your application.

For questions or support, create an issue in the repository or contact the security team.
