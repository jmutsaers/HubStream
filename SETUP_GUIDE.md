# HubStream 2.0 - Local Setup Guide

## ⚠️ Prerequisites

Before running HubStream 2.0, you need:

1. **Python 3.9+** (installed and in PATH)
2. **API Keys** for OpenAI, HubSpot, and SerpApi
3. **A HubSpot Email Template ID**

## 📥 Step 1: Install Python

### Windows

#### Option A: Python.org (Recommended)
1. Go to https://www.python.org/downloads/
2. Download **Python 3.11** or **3.12** (Windows installer)
3. **IMPORTANT:** During installation, check ✅ **"Add Python to PATH"**
4. Click "Install Now"
5. Verify installation:

```powershell
python --version
# Should output: Python 3.11.x or Python 3.12.x
```

#### Option B: Microsoft Store
1. Open Windows PowerShell as Administrator
2. Run: `winget install Python.Python.3.12`
3. Verify: `python --version`

#### Option C: Chocolatey
```powershell
choco install python
python --version
```

### macOS
```bash
brew install python@3.12
python3 --version
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3-pip
python3 --version
```

---

## 📦 Step 2: Install Dependencies

Once Python is installed and accessible:

```powershell
cd C:\HubStream2  # or wherever the project is

# Install dependencies
pip install -r requirements.txt
```

To verify installation:
```powershell
python -c "import streamlit; print('✅ Streamlit installed')"
python -c "import openai; print('✅ OpenAI installed')"
python -c "import requests; print('✅ Requests installed')"
```

---

## 🔐 Step 3: Configure API Keys

1. **Copy the template file:**
```powershell
cp .env.template .env
```

2. **Edit `.env` and fill in your API keys:**

```
SERP_API_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_key_here
HUBSPOT_ACCESS_TOKEN=pat_your_token_here
HUBSPOT_EMAIL_TEMPLATE_ID=your_email_template_id_here
NOTIFICATION_EMAIL_FROM=no-reply@yourdomain.com
NOTIFICATION_EMAIL_TO=your_email@domain.com
DATABASE_PATH=./hubstream.db
DEBUG=false
```

### Getting API Keys

#### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy and paste into `.env`

#### HubSpot
1. Go to HubSpot app → Settings → Integrations → Private Apps
2. Create new app with name "HubStream 2.0"
3. Grant permissions needed:
   - `crm.objects.marketing_emails.read`
   - `crm.objects.marketing_emails.write`
4. Click "Create app"
5. Copy the **access token** (starts with `pat_`)
6. Copy **email template ID** (find in Marketing → Email templates)

#### SerpApi
1. Go to https://serpapi.com/users/sign_up
2. Create free account (includes 100 free searches)
3. Go to Dashboard → API Key
4. Copy the API key

---

## 🚀 Step 4: Run the Application

```powershell
cd C:\HubStream2
streamlit run app.py
```

The app will automatically open in your browser at:
```
http://localhost:8501
```

---

## ✅ Step 5: Test the Setup

1. In the Streamlit app, check the sidebar:
   - ✅ Should show "API Keys configured"
   - ✅ Should show database path

2. Fill in sample campaign details:
   - Audience: "B2B SaaS marketers using HubSpot"
   - Tone: "Professional and helpful"
   - Email outline: "Hook → Problem → Solution → CTA"

3. Click **"Discover Topics & Generate Content"**
   - Should discover topics from SerpApi
   - Should rank them by relevance

4. Click **"Generate Content"**
   - Should create email, newsletter, post, and video script
   - Takes 30-60 seconds (depends on API response time)

---

## 🐛 Troubleshooting

### "Python is not found"
- **Solution:** Python is not installed or not in PATH
- Install from https://www.python.org/downloads/ (check "Add to PATH")
- Restart PowerShell after installing
- Verify: `python --version`

### "ModuleNotFoundError: streamlit"
- **Solution:** Dependencies not installed
- Run: `pip install -r requirements.txt`
- Verify: `python -c "import streamlit; print('OK')"`

### "API key invalid" error
- **Check:** .env file exists in HubStream2 folder
- **Check:** API keys are correct (no extra spaces)
- **Check:** API keys have correct permissions in their dashboards

### "No topics discovered"
- **Check:** SerpApi key is valid and has quota
- **Check:** Internet connection is working
- **Try:** Add your own ideas instead of relying on web search

### "Email not created in HubSpot"
- **Check:** HubSpot token is valid
- **Check:** Email template ID exists
- **Check:** HubSpot account has Marketing Hub license

### Port 8501 already in use
```powershell
# Run on different port
streamlit run app.py --server.port 8502
```

---

## 📁 Project Structure After Setup

```
HubStream2/
├── .env                      # Your configured API keys (DO NOT COMMIT)
├── hubstream.db              # Database (auto-created on first run)
├── app.py                    # Main application
├── database.py               # Database module
├── discovery.py              # Topic discovery
├── hubspot_client.py         # HubSpot integration
├── mailer.py                 # Email notifications
├── processor.py              # AI content generation
├── scraper.py                # Web scraping
├── topic_selector.py         # Topic ranking
├── requirements.txt          # Python dependencies
├── .env.template             # Configuration template
├── README.md                 # Main documentation
├── SETUP_GUIDE.md            # This file
└── .github/
    └── copilot-instructions.md
```

---

## 🎯 Quick Start (After Setup)

```powershell
# 1. Open HubStream2 folder
cd C:\HubStream2

# 2. Run the app
streamlit run app.py

# 3. Fill in campaign details
# 4. Click "Discover Topics & Generate Content"
# 5. Click "Generate Content"
# 6. Review and click "Push to HubSpot + Send Notifications"
```

---

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify .env file configuration
3. Ensure all API keys are valid
4. Check internet connection
5. Review Streamlit logs (check terminal output)

---

## ✨ Ready!

Once Python is installed and dependencies are installed, your HubStream 2.0 setup is complete.

Start creating amazing content with AI! 🚀
