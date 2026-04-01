# HubStream 2.0 - GitHub Upload Guide (No Git Required)

## 📤 Upload to GitHub Without Git (Web Interface)

### Step 1: Create GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon → **"New repository"**
3. Repository name: `HubStream2` (or your choice)
4. Description: `AI-powered HubSpot content generation tool`
5. Keep **Public** (for Streamlit Cloud access)
6. **DO NOT** initialize with README (we have one)
7. Click **"Create repository"**

### Step 2: Upload Files
1. On your repository page, click **"Add file"** → **"Upload files"**
2. **IMPORTANT:** Select files to upload (but exclude these):
   - ❌ `.env` (contains API keys!)
   - ❌ `hubstream.db` (local database)
   - ❌ `__pycache__/` folder
   - ❌ `.git/` folder (if exists)

3. **Files to upload:**
   - ✅ `app.py`
   - ✅ `database.py`
   - ✅ `discovery.py`
   - ✅ `processor.py`
   - ✅ `scraper.py`
   - ✅ `topic_selector.py`
   - ✅ `hubspot_client.py`
   - ✅ `mailer.py`
   - ✅ `requirements.txt`
   - ✅ `packages.txt`
   - ✅ `runtime.txt`
   - ✅ `.streamlit/config.toml`
   - ✅ `.gitignore`
   - ✅ `README.md`
   - ✅ `WEB_DEPLOYMENT.md`
   - ✅ `QUICK_START.md`
   - ✅ `SETUP_GUIDE.md`
   - ✅ `WORKFLOW_GUIDE.md`
   - ✅ `TEST_REPORT.md`
   - ✅ `Assets/` folder (HubSpot logo)
   - ✅ `.env.template` (as template)
   - ✅ All test files if you want

4. Click **"Commit changes"**

### Step 3: Verify Upload
- Check that all files are uploaded
- Make sure `.env` is NOT uploaded (security!)
- Repository should be ready for Streamlit Cloud

## 🎯 Next: Deploy to Streamlit Cloud

Once uploaded to GitHub, follow these steps:

### 1. Go to Streamlit Cloud
- Visit: [share.streamlit.io](https://share.streamlit.io)
- Sign in with your GitHub account

### 2. Create New App
- Click **"New app"**
- Select your **HubStream2** repository
- Main file path: `app.py`
- Click **"Deploy!"**

### 3. Configure Secrets
In your Streamlit Cloud app settings, add these secrets:

```
OPENAI_API_KEY = "sk-proj-your-actual-openai-key-here"
HUBSPOT_ACCESS_TOKEN = "pat-your-hubspot-token-here"
SERP_API_KEY = "your-serpapi-key-here"
DATABASE_PATH = "./hubstream.db"
NOTIFICATION_EMAIL_FROM = "your-email@domain.com"
NOTIFICATION_EMAIL_TO = "team-email@domain.com"
```

### 4. Access Your App
- Streamlit Cloud will give you a URL like: `https://your-app-name.streamlit.app`
- Share this URL with your colleagues!

## 🔧 Troubleshooting

### If deployment fails:
1. Check that `requirements.txt` has correct versions
2. Verify all Python files have no syntax errors
3. Make sure `.streamlit/config.toml` exists

### If app doesn't load:
1. Check Streamlit Cloud logs for errors
2. Verify all secrets are set correctly
3. Make sure API keys are valid and have credits

## 📞 Need Help?
If you get stuck on any step, share the error message and I'll help you fix it!