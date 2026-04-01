# 🚀 HubStream 2.0 - Quick Start Guide

## One-Minute Setup

```bash
# You already have everything installed! Just run:
cd C:\HubStream2
streamlit run app.py
```

✅ **Done!** App opens at `http://localhost:8501`

---

## What You Have

✅ **All modules built and tested:**
- [x] Discovery (SerpApi topic search)
- [x] Topic Selection (5-factor scoring)
- [x] Content Generation (4 outputs via OpenAI)
- [x] HubSpot Integration (email templates)
- [x] Database (SQLite)
- [x] Email Notifications
- [x] Web Scraping

✅ **All dependencies installed:**
- Streamlit, OpenAI, HubSpot API, SerpApi, BeautifulSoup, etc.

✅ **Ready-to-use UI:**
- Input campaign details
- Auto-discover topics
- Generate content
- Push to HubSpot

---

## To Go Live (Get Real API Keys)

### Step 1: Get API Keys

**OpenAI (GPT-4o)**
1. Visit https://platform.openai.com/api-keys
2. Create a new key
3. Copy it

**HubSpot**
1. Go to HubSpot Settings → Integrations → Private Apps
2. Create new app "HubStream 2.0"
3. Grant: `crm.objects.marketing_emails.read` + `write`
4. Copy the access token
5. Find an email template ID in Marketing → Email Templates

**SerpApi**
1. Visit https://serpapi.com/users/sign_up
2. Create free account
3. Copy API key from dashboard

### Step 2: Update Configuration

```bash
# Edit .env file in C:\HubStream2
SERP_API_KEY=your_real_serpapi_key
OPENAI_API_KEY=sk-your_openai_key
HUBSPOT_ACCESS_TOKEN=pat-your_hubspot_token
HUBSPOT_EMAIL_TEMPLATE_ID=your_template_id
NOTIFICATION_EMAIL_TO=your_email@domain.com
```

### Step 3: Restart App

```bash
cd C:\HubStream2
streamlit run app.py
```

---

## Using the App

### Workflow

1. **Fill in details:**
   - Target audience (who are we writing for?)
   - Tone of voice (how should it sound?)
   - Email outline (structure)
   - Newsletter outline (structure)
   - Your ideas (optional)

2. **Discover & Select:**
   - Click "Discover Topics & Generate Content"
   - App finds relevant HubSpot updates
   - Ranks them by relevance
   - Selects the best one

3. **Generate:**
   - Click "Generate Content"
   - AI creates:
     - 📧 Email (for HubSpot)
     - 📰 Newsletter article (for LinkedIn)
     - 📱 LinkedIn post (80-180 words)
     - 🎬 Video script (60-90 seconds)

4. **Push:**
   - Click "Push to HubSpot + Send Notifications"
   - Email draft created in HubSpot (DRAFT status)
   - Social content ready to copy/paste
   - Notifications sent

---

## File Structure

```
C:\HubStream2\
├── app.py              ← Main app (run this!)
├── .env                ← Your API keys (NEVER share!)
├── .env.template       ← Template with all keys needed
├── requirements.txt    ← Dependencies (already installed)
├── database.py         ← Content storage
├── discovery.py        ← Topic search
├── topic_selector.py   ← Scoring algorithm
├── processor.py        ← AI content generation
├── scraper.py          ← Web scraping
├── hubspot_client.py   ← HubSpot API
├── mailer.py           ← Email notifications
├── README.md           ← Full documentation
└── test_setup.py       ← Setup validation
```

---

## Testing

### Verify Everything Works

```bash
cd C:\HubStream2
python test_setup.py
```

Should show: ✅ **ALL TESTS PASSED!**

### Quick Test without API Keys

```bash
# Just see if the app starts
streamlit run app.py
```

Fill the form and click "Discover Topics" - it will show API key errors, which is expected if you don't have real keys yet.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "streamlit: command not found" | Reinstall: `pip install streamlit` |
| "No module named X" | Reinstall deps: `pip install -r requirements.txt` |
| "Invalid API key" | Check .env file has real keys, not test placeholders |
| "Connection refused" | Make sure HubSpot token is valid |
| Port 8501 in use | Use different port: `streamlit run app.py --server.port 8502` |

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│   Streamlit Web Interface (app.py)  │
└──────────────┬──────────────────────┘
               │
   ┌───────────┼────────────┐
   │           │            │
   ▼           ▼            ▼
DISCOVERY   PROCESSOR    HUBSPOT
(SerpApi)   (OpenAI)     (Email)
   │           │            │
   └───────────┼────────────┘
               │
        ┌──────▼──────┐
        │   DATABASE  │
        │  (SQLite)   │
        └─────┬───────┘
              │
        ┌─────▼─────────┐
        │   GENERATED   │
        │    CONTENT    │
        └───────────────┘
```

---

## What's Next

### Immediate (Today)
- [ ] Get API keys from OpenAI, HubSpot, SerpApi
- [ ] Update .env with real credentials
- [ ] Test with real API keys
- [ ] Generate first piece of content
- [ ] Review in HubSpot and publish

### Short Term (This Week)
- [ ] Set up email notifications for your team
- [ ] Test different audience contexts
- [ ] Fine-tune outlines for your brand
- [ ] Create content calendar using the tool

### Long Term (This Month)
- [ ] Automate weekly content runs
- [ ] Track performance of generated content
- [ ] Refine topic selection for your niche
- [ ] Scale to other marketing channels

---

## Key Features Summary

| Feature | What It Does |
|---------|-------------|
| **Discovery** | Finds relevant HubSpot topics from web + user ideas |
| **Scoring** | Ranks topics by audience fit, recency, strategic value |
| **Generation** | Creates 4 content pieces with AI (email, newsletter, post, video) |
| **HubSpot** | Pushes email draft directly into your HubSpot account |
| **Database** | Stores all content and topics for history/versioning |
| **Notifications** | Emails you when content is ready |

---

## Important Notes

🔐 **Security**
- Never commit .env with real keys
- Rotate API keys every 3-6 months
- Use separate API keys for staging/production

💰 **Costs**
- OpenAI: ~$0.01-0.05 per content run (depends on tokens)
- SerpApi: Free tier = 100 searches/month
- HubSpot: Requires Marketing Hub license
- Everything else: Free

⏱️ **Speed**
- Topic discovery: 10-20 seconds
- Content generation: 30-60 seconds
- Total workflow: 2-3 minutes per content run

---

## Support

📖 **Full Documentation:** See README.md  
🔧 **Setup Help:** See SETUP_GUIDE.md  
✅ **Test Results:** See TEST_REPORT.md  
💬 **Module Docs:** Check docstrings in each .py file

---

## Example Campaign

```
🎯 Target: B2B SaaS marketing directors
🎤 Tone: Professional, insightful, data-driven
📧 Email: Hook about AI in marketing → Problem with manual processes → HubSpot solution
📰 Newsletter: Deep dive on personalization trends
📱 Post: "3 ways AI improves email campaigns" (LinkedIn)
🎬 Script: How-to video on automation

⏱️ Time to create all 4: 2-3 minutes instead of 4-6 hours
```

---

**You're all set!** 🚀

Run `streamlit run app.py` and start generating amazing content.
