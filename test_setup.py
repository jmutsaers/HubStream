"""
HubStream 2.0 - Setup Test Script
Validates all modules and configuration without running the full app.
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("HubStream 2.0 - Setup Test")
print("=" * 60)

# Test 1: Python Version
print("\n✅ Test 1: Python Version")
print(f"   Python {sys.version}")

# Test 2: Project Structure
print("\n✅ Test 2: Project Structure")
required_files = [
    "app.py",
    "database.py",
    "discovery.py",
    "scraper.py",
    "topic_selector.py",
    "processor.py",
    "hubspot_client.py",
    "mailer.py",
    "requirements.txt",
    ".env.template",
    "README.md"
]

missing_files = []
for file in required_files:
    if Path(file).exists():
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} (MISSING)")
        missing_files.append(file)

if missing_files:
    print(f"\n❌ Missing files: {missing_files}")
    sys.exit(1)

# Test 3: Dependencies
print("\n✅ Test 3: Python Dependencies")
dependencies = {
    "streamlit": "Streamlit UI framework",
    "openai": "OpenAI GPT-4o API",
    "requests": "HTTP requests library",
    "bs4": "BeautifulSoup web scraping",
    "dotenv": "Environment variables",
    "serpapi": "SerpApi search",
    "sqlalchemy": "Database ORM",
    "markdown2": "Markdown processing"
}

missing_deps = []
for module, description in dependencies.items():
    try:
        __import__(module)
        print(f"   ✓ {module:<15} ({description})")
    except ImportError as e:
        print(f"   ✗ {module:<15} ({description}) - NOT INSTALLED")
        missing_deps.append(module)

if missing_deps:
    print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
    sys.exit(1)

# Test 4: Module Imports
print("\n✅ Test 4: Module Imports")
modules = [
    ("database", "Database"),
    ("scraper", "Scraper"),
    ("discovery", "DiscoveryEngine"),
    ("topic_selector", "TopicSelector"),
    ("processor", "ContentProcessor"),
    ("hubspot_client", "HubSpotClient"),
    ("mailer", "NotificationMailer")
]

for module_name, class_name in modules:
    try:
        module = __import__(module_name)
        cls = getattr(module, class_name)
        print(f"   ✓ {module_name:<20} - {class_name}")
    except Exception as e:
        print(f"   ✗ {module_name:<20} - Error: {e}")
        sys.exit(1)

# Test 5: Environment Configuration
print("\n✅ Test 5: Environment Configuration")
env_file = Path(".env")
env_template = Path(".env.template")

if env_file.exists():
    print("   ✓ .env file exists")
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = [
        "SERP_API_KEY",
        "OPENAI_API_KEY",
        "HUBSPOT_ACCESS_TOKEN",
        "HUBSPOT_EMAIL_TEMPLATE_ID",
        "NOTIFICATION_EMAIL_TO"
    ]
    
    configured = []
    missing = []
    for key in required_keys:
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}_here":
            configured.append(key)
            print(f"   ✓ {key:<30} configured")
        else:
            missing.append(key)
            print(f"   ⚠ {key:<30} NOT configured")
    
    if missing:
        print(f"\n   ⚠️  Missing API Keys: {', '.join(missing)}")
        print("   ℹ️  Copy .env.template → .env and fill in your API keys")
else:
    if env_template.exists():
        print("   ✓ .env.template exists")
        print("   ⚠ .env file not found")
        print("   ℹ️  Run: cp .env.template .env")
    else:
        print("   ✗ Neither .env nor .env.template found")
        sys.exit(1)

# Test 6: Database
print("\n✅ Test 6: Database Module")
try:
    from database import Database
    db = Database(":memory:")  # Use in-memory DB for testing
    
    # Test schema creation
    assert hasattr(db, 'insert_topic')
    assert hasattr(db, 'get_topics_by_score')
    assert hasattr(db, 'insert_content_run')
    print("   ✓ Database schema initialized")
    print("   ✓ All CRUD methods available")
except Exception as e:
    print(f"   ✗ Database error: {e}")
    sys.exit(1)

# Test 7: Content Processor
print("\n✅ Test 7: Content Processor")
try:
    from processor import ContentProcessor
    processor = ContentProcessor(api_key="test_key")
    
    # Check all methods exist
    assert hasattr(processor, 'generate_email_content')
    assert hasattr(processor, 'generate_newsletter_content')
    assert hasattr(processor, 'generate_linkedin_post')
    assert hasattr(processor, 'generate_video_script')
    assert hasattr(processor, 'generate_all_content')
    print("   ✓ Processor initialized")
    print("   ✓ All content generation methods available")
except Exception as e:
    print(f"   ✗ Processor error: {e}")
    sys.exit(1)

# Test 8: TopicSelector
print("\n✅ Test 8: Topic Selector")
try:
    from topic_selector import TopicSelector
    selector = TopicSelector()
    
    # Test with sample topic
    sample_topic = {
        "title": "HubSpot New Feature",
        "description": "A new feature for HubSpot users",
        "source": "HubSpot Blog",
        "published_date": "2024-01-15"
    }
    
    score = selector.calculate_overall_score(sample_topic, "marketing managers")
    assert 0 <= score <= 1, f"Score {score} out of range"
    print(f"   ✓ Selector initialized")
    print(f"   ✓ Sample topic scored: {score:.2f}")
except Exception as e:
    print(f"   ✗ TopicSelector error: {e}")
    sys.exit(1)

# Test 9: Scraper
print("\n✅ Test 9: Web Scraper")
try:
    from scraper import Scraper
    scraper = Scraper()
    
    assert hasattr(scraper, 'fetch_url')
    assert hasattr(scraper, 'extract_text_content')
    assert hasattr(scraper, 'scrape_url')
    print("   ✓ Scraper initialized")
    print("   ✓ All scraping methods available")
except Exception as e:
    print(f"   ✗ Scraper error: {e}")
    sys.exit(1)

# Test 10: HubSpot Client
print("\n✅ Test 10: HubSpot Client")
try:
    from hubspot_client import HubSpotClient
    hubspot = HubSpotClient(access_token="test_token")
    
    assert hasattr(hubspot, 'clone_email_template')
    assert hasattr(hubspot, 'update_email_content')
    assert hasattr(hubspot, 'test_connection')
    print("   ✓ HubSpot client initialized")
    print("   ✓ All API methods available")
except Exception as e:
    print(f"   ✗ HubSpot client error: {e}")
    sys.exit(1)

# Test 11: Mailer
print("\n✅ Test 11: Notification Mailer")
try:
    from mailer import NotificationMailer
    mailer = NotificationMailer()
    
    assert hasattr(mailer, 'send_email_draft_notification')
    assert hasattr(mailer, 'send_social_content_notification')
    assert hasattr(mailer, 'mock_send_email')
    print("   ✓ Mailer initialized")
    print("   ✓ All notification methods available")
except Exception as e:
    print(f"   ✗ Mailer error: {e}")
    sys.exit(1)

# Final Report
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n🚀 Next Steps:")
print("   1. Configure API keys in .env file")
print("   2. Run: streamlit run app.py")
print("   3. Access app at: http://localhost:8501")
print("\n📚 Documentation: See README.md for detailed instructions")
print("=" * 60)
