# HubStream 2.0 - Web Deployment Guide
# Deploy HubStream to Streamlit Cloud for team access

## 🚀 Quick Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository
1. **Push to GitHub** (required for Streamlit Cloud)
   - Create a new GitHub repository
   - Upload all HubStream files
   - Make sure `.env` is NOT included (use `.env.template` as template)

2. **Required Files** (already created):
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `packages.txt` - System dependencies
   - ✅ `.streamlit/config.toml` - Streamlit configuration

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your HubStream repository
5. Set main file path: `app.py`
6. Click "Deploy!"

### Step 3: Configure Secrets (Environment Variables)
In Streamlit Cloud, go to your app settings and add these secrets:

```
OPENAI_API_KEY = "sk-proj-your-actual-openai-key-here"
HUBSPOT_ACCESS_TOKEN = "pat-your-hubspot-token-here"
SERP_API_KEY = "your-serpapi-key-here"
DATABASE_PATH = "./hubstream.db"
NOTIFICATION_EMAIL_FROM = "your-email@domain.com"
NOTIFICATION_EMAIL_TO = "team-email@domain.com"
```

### Step 4: Share with Team
- Share the Streamlit Cloud URL with your colleagues
- Everyone can access the same app simultaneously
- Data is shared across all users

## 🔧 Alternative Deployment Options

### Option 2: Heroku
```bash
# Install Heroku CLI
# Create app
heroku create your-hubstream-app
# Set environment variables
heroku config:set OPENAI_API_KEY="your-key"
# Deploy
git push heroku main
```

### Option 3: Docker + Cloud
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
```

## 📊 Features Available in Web Version
- ✅ All HubStream functionality
- ✅ Shared database across team
- ✅ Real-time collaboration
- ✅ No local installation needed
- ✅ Automatic updates when you push code

## ⚠️ Important Notes
- **Database**: SQLite works in cloud but data resets on redeploy
- **File Storage**: Use cloud storage (AWS S3, etc.) for persistent files
- **API Limits**: Monitor OpenAI usage costs
- **Security**: Keep API keys secure as secrets

## 🎯 Next Steps
1. Push code to GitHub
2. Deploy to Streamlit Cloud
3. Configure secrets
4. Test with team members
5. Monitor usage and costs

Need help with any step? Just ask!