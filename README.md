# HubStream 2.0

HubStream 2.0 is an AI-powered content generation automation tool that discovers HubSpot-related topics, analyzes them, and generates high-quality content across multiple channels with minimal manual effort.

## 🎯 Overview

In **one click**, HubStream 2.0 automates the creation of:
- 📧 HubSpot Marketing Email (draft)
- 📰 LinkedIn Newsletter article
- 📱 LinkedIn Post
- 🎬 Video Script (60-90 seconds)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- API Keys for:
  - OpenAI (GPT-4o)
  - HubSpot (Marketing Hub)
  - SerpApi (Google Search API)

### Installation

1. Clone or extract the HubStream 2.0 project
2. Create a `.env` file based on `.env.template`:

```bash
cp .env.template .env
```

3. Fill in your API keys:

```
SERP_API_KEY=your_serpapi_key
OPENAI_API_KEY=your_openai_key
HUBSPOT_ACCESS_TOKEN=pat_your_token
HUBSPOT_EMAIL_TEMPLATE_ID=your_template_id
NOTIFICATION_EMAIL_FROM=no-reply@yourdomain.com
NOTIFICATION_EMAIL_TO=your_email@domain.com
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Web Deployment (Team Access)

Want your colleagues to use HubStream too? Deploy it to the web!

### Quick Deploy to Streamlit Cloud

1. **Push to GitHub** (create a new repository)
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repo**
4. **Set main file:** `app.py`
5. **Add secrets** in app settings:
   ```
   OPENAI_API_KEY = "sk-proj-your-key"
   HUBSPOT_ACCESS_TOKEN = "pat-your-token"
   SERP_API_KEY = "your-serpapi-key"
   ```
6. **Deploy!** Share the URL with your team

### Features in Web Version
- ✅ Shared database across team
- ✅ Real-time collaboration
- ✅ No local installation needed
- ✅ Automatic updates

📖 **Full deployment guide:** See `WEB_DEPLOYMENT.md`

## 📋 Workflow

### Step 1: Input Campaign Details

Provide:
- **Target Audience:** Describe your ICP, industry, pain points
- **Tone of Voice:** How should the content sound?
- **Email Outline:** Structure for the email (Hook → Problem → Solution → CTA)
- **Newsletter Outline:** Structure for the newsletter article
- **Your Ideas:** Optional internal ideas or specific themes to include

### Step 2: Discover Topics

Click **"Discover Topics & Generate Content"** to:
- Search for recent HubSpot updates using SerpApi
- Combine with your own ideas
- Score and rank topics by relevance

### Step 3: Select Topic

- Review the ranked list of topics
- Click on a topic to see details and scores
- The highest-scoring topic is selected by default (change if needed)

### Step 4: Generate Content

Click **"Generate Content"** to produce:
- Tailored email copy
- Newsletter article with hooks and CTAs
- LinkedIn post (80-180 words)
- Video script (60-90 seconds)

All generated content is shown in tabs for easy review and copying.

### Step 5: Push & Notify

Click **"Push to HubSpot + Send Notifications"** to:
- Create a **DRAFT** email in HubSpot (from a cloned template)
- Save all content to the local database
- Send notification emails with the generated content
- Get ready-to-copy LinkedIn content

## 🏗️ Project Structure

```
HubStream2/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite CRUD operations
├── discovery.py           # SerpApi topic discovery
├── hubspot_client.py      # HubSpot API v3 wrapper
├── mailer.py              # Email notification system
├── processor.py           # OpenAI content generation
├── scraper.py             # BeautifulSoup web scraping
├── topic_selector.py      # Topic scoring and ranking
├── requirements.txt       # Python dependencies
├── .env.template          # Environment variables template
└── hubstream.db           # SQLite database (auto-created)
```

## 📚 Modules

### discovery.py
Finds relevant HubSpot updates via SerpApi and combines with user ideas.

### topic_selector.py
Scores topics based on:
- Audience relevance
- Recency
- Strategic value
- LinkedIn potential
- Reusability across channels

### processor.py
Generates content using OpenAI GPT-4o with channel-specific prompts:
- **Email:** Professional B2B marketing copy
- **Newsletter:** Detailed, LinkedIn-optimized article
- **Post:** Concise, engaging 80-180 word post
- **Video:** Spoken script with visual notes

### hubspot_client.py
Integrates with HubSpot's Marketing Hub API to:
- Clone email templates
- Create email drafts
- Upload files/images

### database.py
Manages SQLite operations for:
- Topic history and scoring
- Content runs
- Generated content versions
- URL caching

### mailer.py
Sends notification emails to keep your team informed.

## ⚙️ Configuration

### HubSpot Setup

1. Create a **Private App** in HubSpot
2. Grant permissions: `emails:read` and `emails:write`
3. Create or find an email template to use as a base
4. Copy the template ID and add to `.env`

### OpenAI Setup

1. Go to https://platform.openai.com/api-keys
2. Create an API key
3. Add to `.env` as `OPENAI_API_KEY`

### SerpApi Setup

1. Sign up at https://serpapi.com
2. Get your API key from the dashboard
3. Add to `.env` as `SERP_API_KEY`

## 🧪 Testing

Run the app in **development mode**:

```bash
streamlit run app.py --logger.level=debug
```

For local testing without SMTP/email:
- The `NotificationMailer.mock_send_email()` method prints emails to console
- Check the console output for email content

## 📊 Example Usage

**Input:**
- Audience: "B2B Marketing Directors, HubSpot CRM users, 50+ employee companies"
- Tone: "Professional, data-driven, inspiring"
- Ideas: ["AI in HubSpot", "New CRM features Q1 2025"]

**Output:**
- Email ready in HubSpot (DRAFT status)
- Newsletter article (~1000 words)
- LinkedIn post ready to copy
- Video script (2-3 minutes speaking time)

**Result:** 4 pieces of high-quality content generated in 2 minutes instead of 4 hours.

## 🔄 Database Schema

### content_runs
Tracks each content generation run with references to topics and generated content.

### topics
Stores discovered topics with scores and metadata.

### generated_content
Versions of generated content (email, newsletter, post, video) per run.

### scraped_urls
Cache of previously scraped content to avoid duplicate fetches.

## 🛠️ Advanced Configuration

### Custom Topic Scoring Weights

Edit `topic_selector.py` to adjust how topics are scored:

```python
selector = TopicSelector(
    audience_weight=0.35,    # How important is audience match?
    recency_weight=0.25,     # How recent does content need to be?
    strategic_weight=0.15,   # Strategic value importance
    linkedin_weight=0.15,    # LinkedIn engagement potential
    reuse_weight=0.10        # Multi-channel reusability
)
```

### Custom Search Queries

In `app.py`, modify the search queries in the discovery section:

```python
search_queries = [
    "HubSpot CRM automation",
    "HubSpot AI features",
    "HubSpot integrations 2025"
]
```

## 🐛 Troubleshooting

### API Keys Not Working

- Verify `.env` file is in the same directory as `app.py`
- Check that keys are correct (no extra spaces)
- Ensure API keys have required permissions

### No Topics Discovered

- Check SerpApi quota and API key validity
- Try different search queries
- Add more user ideas to supplement web search

### HubSpot Integration Fails

- Verify Private App access token has `emails` permissions
- Confirm email template ID is correct and exists
- Check HubSpot account has Marketing Hub license

### Email Notifications Not Sending

- Verify `NOTIFICATION_EMAIL_TO` is set
- For Gmail: use app password (not account password)
- Check SMTP settings in `mailer.py` (defaults to Gmail)

## 📝 Future Enhancements

- [ ] Content editing UI with inline edits
- [ ] Batch content generation across multiple topics
- [ ] Scheduled content runs (daily/weekly)
- [ ] Analytics integration to track post performance
- [ ] AI-powered image generation for content
- [ ] Direct LinkedIn publishing API integration
- [ ] Multi-language content generation
- [ ] A/B testing variant generation

## 📄 License

HubStream 2.0 is proprietary software. All rights reserved.

## 💬 Support

For questions or issues:
- Check the troubleshooting section above
- Review `.env` configuration
- Enable debug logging in Streamlit
- Contact your HubStream administrator

---

**Ready to revolutionize your content creation?** 🚀

Launch HubStream 2.0 and automate your next content cycle in minutes!
