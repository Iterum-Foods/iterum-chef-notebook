# 📧 Email System Setup Guide

## Quick Start (Choose One Method)

### Option 1: Gmail SMTP (Fastest - 10 minutes)
**Best for:** Testing, small volume (<100 emails/day)

### Option 2: SendGrid (Recommended - 30 minutes)
**Best for:** Production, professional delivery, scaling

### Option 3: AWS SES (Advanced - 1 hour)
**Best for:** High volume, lowest cost at scale

---

## ⚡ Option 1: Gmail SMTP Setup

### Step 1: Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow setup wizard

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select app: "Mail"
3. Select device: "Other" → "Iterum App"
4. Click "Generate"
5. **COPY THE 16-CHARACTER PASSWORD** (you won't see it again!)

### Step 3: Create `.env` File
Create ``.env`` in your project root:

```bash
# Email Configuration - Gmail SMTP
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Iterum Foods

# App Configuration
APP_URL=https://iterum-culinary-app.web.app
```

### Step 4: Test It
```bash
# Start backend
cd app
python -m uvicorn main:app --reload

# In another terminal, test email
curl -X POST "http://localhost:8000/api/trial/test-email/your-test-email@gmail.com"
```

### Step 5: Check Your Inbox!
You should receive a welcome email within 30 seconds.

---

## 🚀 Option 2: SendGrid Setup (RECOMMENDED)

### Step 1: Create SendGrid Account
1. Go to https://signup.sendgrid.com/
2. Sign up (free tier: 100 emails/day forever)
3. Verify your email address

### Step 2: Verify Sender Identity
1. Go to Settings → Sender Authentication
2. Click "Verify a Single Sender"
3. Fill in your details:
   - From Name: `Iterum Foods`
   - From Email: `noreply@iterumfoods.com` (or your domain)
   - Reply To: `support@iterumfoods.com`
4. Check your email and click verification link

### Step 3: Create API Key
1. Go to Settings → API Keys
2. Click "Create API Key"
3. Name: "Iterum Production"
4. Permissions: "Full Access" (or "Mail Send" only)
5. Click "Create & View"
6. **COPY THE API KEY** (you won't see it again!)

### Step 4: Install SendGrid
```bash
pip install sendgrid
```

### Step 5: Create `.env` File
```bash
# Email Configuration - SendGrid
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@iterumfoods.com
FROM_NAME=Iterum Foods

# App Configuration
APP_URL=https://iterum-culinary-app.web.app
```

### Step 6: Test It
```bash
# Start backend
python -m uvicorn app.main:app --reload

# Test email
curl -X POST "http://localhost:8000/api/trial/test-email/your-email@gmail.com"
```

---

## ☁️ Option 3: AWS SES Setup

### Step 1: Create AWS Account
1. Go to https://aws.amazon.com/
2. Create account (requires credit card but has free tier)

### Step 2: Verify Email Address
1. Go to AWS Console → SES
2. Click "Email Addresses" → "Verify a New Email Address"
3. Enter your from email
4. Check inbox and click verification link

### Step 3: Request Production Access
1. In SES Console, click "Sending Statistics"
2. Click "Request Production Access"
3. Fill out form (usually approved in 24 hours)
4. **NOTE:** Until approved, you can only send to verified emails

### Step 4: Create IAM User
1. Go to IAM Console → Users → Add User
2. Username: `iterum-ses-sender`
3. Access type: Programmatic access
4. Permissions: Attach policy "AmazonSESFullAccess"
5. **SAVE ACCESS KEY AND SECRET KEY**

### Step 5: Install boto3
```bash
pip install boto3
```

### Step 6: Create `.env` File
```bash
# Email Configuration - AWS SES
EMAIL_PROVIDER=ses
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
FROM_EMAIL=noreply@iterumfoods.com
FROM_NAME=Iterum Foods

# App Configuration
APP_URL=https://iterum-culinary-app.web.app
```

---

## 🧪 Testing Your Setup

### Test 1: Backend API Test
```bash
# Start your backend
python -m uvicorn app.main:app --reload

# Send test email
curl -X POST "http://localhost:8000/api/trial/test-email/YOUR_EMAIL@gmail.com"
```

### Test 2: Full Trial Signup Flow
1. Open https://iterum-culinary-app.web.app/launch.html
2. Click "Start Free 14-Day Trial"
3. Fill in the form with YOUR email
4. Submit
5. Check your inbox for welcome email!

### Test 3: Check Backend Logs
```bash
# You should see:
✅ Trial user saved: your-email@gmail.com
✅ Welcome email sent to your-email@gmail.com
```

---

## 📊 Monitoring Email Delivery

### Gmail SMTP
- Check "Sent" folder in your Gmail account
- Look for bounce messages in inbox

### SendGrid
1. Go to SendGrid Dashboard
2. Click "Activity" → see all sent emails
3. View opens, clicks, bounces, spam reports

### AWS SES
1. Go to SES Console → "Sending Statistics"
2. See delivery rate, bounce rate, complaint rate
3. Set up SNS notifications for bounces

---

## 🔧 Troubleshooting

### "Authentication failed" (Gmail)
- ✅ Verify 2-Step Verification is enabled
- ✅ Use App Password, not regular password
- ✅ Check SMTP_USER matches the Gmail account
- ✅ Try regenerating App Password

### "Invalid API Key" (SendGrid)
- ✅ Check API key was copied correctly (no spaces)
- ✅ Verify API key has "Mail Send" permission
- ✅ Key should start with `SG.`

### "Email not verified" (AWS SES)
- ✅ Verify your FROM_EMAIL in SES Console
- ✅ Check verification link in email
- ✅ Request production access if sending to non-verified emails

### "Connection refused" (Backend)
- ✅ Verify backend is running: `http://localhost:8000/health`
- ✅ Check firewall isn't blocking port 8000
- ✅ Update `launch.html` backend URL if deployed

### Emails not being received
1. ✅ Check spam/junk folder
2. ✅ Verify email address is correct
3. ✅ Check backend logs for errors
4. ✅ Test with different email provider (Gmail, Outlook, Yahoo)

---

## 📈 Email Analytics Setup

### Track Opens & Clicks
Add to your email HTML:

```html
<!-- Track email opens -->
<img src="https://your-backend.com/api/track/open/{{user_id}}" width="1" height="1" />

<!-- Track link clicks -->
<a href="https://your-backend.com/api/track/click/{{user_id}}/{{link_id}}?redirect={{actual_url}}">
    Click here
</a>
```

### Integrate with Analytics
```python
# In your backend
from mixpanel import Mixpanel
mp = Mixpanel("YOUR_MIXPANEL_TOKEN")

# Track email sent
mp.track(user_email, 'Email Sent', {
    'email_type': 'trial_welcome',
    'trial_days': 14
})

# Track email opened
mp.track(user_email, 'Email Opened', {
    'email_type': 'trial_welcome'
})
```

---

## 🎯 Email Best Practices

### Subject Lines
- ✅ Keep under 50 characters
- ✅ Use emojis sparingly (🎁 works great)
- ✅ Personalize with name
- ✅ Create urgency when appropriate
- ❌ Avoid ALL CAPS or excessive punctuation!!!

### Email Content
- ✅ Mobile-responsive design
- ✅ Clear call-to-action button
- ✅ Unsubscribe link (legal requirement)
- ✅ Plain text alternative
- ❌ Don't use too many images

### Sending Schedule
- ✅ Send during business hours (9am-5pm recipient timezone)
- ✅ Avoid weekends for business emails
- ✅ Test different send times
- ❌ Don't send more than 1 email per day

### Deliverability
- ✅ Verify your domain (SPF, DKIM, DMARC)
- ✅ Warm up new sending domain gradually
- ✅ Monitor bounce and complaint rates
- ✅ Clean your email list regularly

---

## 🔐 Security Best Practices

### Protect API Keys
```bash
# NEVER commit .env file to git
echo ".env" >> .gitignore

# Use environment variables in production
export SENDGRID_API_KEY="your-key"

# Rotate keys regularly (every 90 days)
```

### Validate Email Addresses
```python
from email_validator import validate_email

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except:
        return False
```

### Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=lambda: "global")

@app.post("/api/trial/signup")
@limiter.limit("5/minute")  # Max 5 signups per minute
async def trial_signup(...):
    ...
```

---

## 📅 Automated Email Schedule

Once setup is complete, these emails will send automatically:

| Day | Email | Purpose |
|-----|-------|---------|
| 0 | Welcome | Onboarding, set expectations |
| 1 | Getting Started | Drive first action |
| 3 | Feature Highlight | Increase adoption |
| 7 | Mid-Trial Check-In | Re-engage, offer help |
| 10 | "4 Days Left" | Create urgency |
| 12 | "2 Days Left" + Offer | Strong conversion push |
| 14 | Trial Ended | Convert or retain |
| 16 | Last Chance | Win back |

---

## ✅ Setup Checklist

### Initial Setup
- [ ] Choose email provider (Gmail/SendGrid/AWS SES)
- [ ] Create account and verify sender
- [ ] Get API credentials
- [ ] Create `.env` file with credentials
- [ ] Install required packages (`sendgrid` or `boto3`)
- [ ] Test with `/api/trial/test-email` endpoint

### Integration
- [ ] Verify backend includes trial router
- [ ] Test trial signup from launch.html
- [ ] Check email arrives in inbox (not spam)
- [ ] Verify email formatting looks good
- [ ] Test on mobile device

### Production
- [ ] Set up custom domain email
- [ ] Configure SPF/DKIM/DMARC records
- [ ] Set up email analytics
- [ ] Create unsubscribe handling
- [ ] Set up bounce handling
- [ ] Monitor delivery rates

---

## 🆘 Need Help?

### Check Logs
```bash
# Backend logs
tail -f logs/iterum_app.log

# Email service logs
grep "Email" logs/iterum_app.log
```

### Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Test email
curl -X POST http://localhost:8000/api/trial/test-email/test@example.com

# Get trial users
curl http://localhost:8000/api/trial/users

# Get stats
curl http://localhost:8000/api/trial/stats
```

---

## 🎉 You're Ready!

Once you complete any of the setup options above, your app will:

1. ✅ Automatically send welcome emails to new trial users
2. ✅ Track all trial signups in the database
3. ✅ Allow manual sending of reminder emails
4. ✅ Provide analytics on trial user behavior

**Your trial users will now receive professional, branded emails!** 🚀

