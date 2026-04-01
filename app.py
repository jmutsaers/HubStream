"""
HubStream 2.0 - Main Streamlit Application
AI-powered automation for HubSpot content generation across multiple channels.
"""

import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import modules
from database import Database
from scraper import Scraper
from discovery import DiscoveryEngine
from topic_selector import TopicSelector
from processor import ContentProcessor
from hubspot_client import HubSpotClient
from mailer import NotificationMailer

# Load environment variables
load_dotenv()

# Initialize session state
if "content_run_id" not in st.session_state:
    st.session_state.content_run_id = None
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None
if "generated_content" not in st.session_state:
    st.session_state.generated_content = None
if "user_ideas_input" not in st.session_state:
    st.session_state.user_ideas_input = [""]
if "web_ideas" not in st.session_state:
    st.session_state.web_ideas = []
if "user_ideas" not in st.session_state:
    st.session_state.user_ideas = []
if "candidate_topics" not in st.session_state:
    st.session_state.candidate_topics = []
if "ideas_confirmed" not in st.session_state:
    st.session_state.ideas_confirmed = False

# Page config
app_icon_path = "assets/HubSpot Logo.svg"
page_icon = app_icon_path if os.path.exists(app_icon_path) else ":sparkles:"

st.set_page_config(
    page_title="HubStream",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

col_logo, col_title = st.columns([0.8, 3], vertical_alignment="center", gap="small")

with col_logo:
    if os.path.exists(app_icon_path):
        st.image(app_icon_path, width=150)
    else:
        st.markdown("**HubStream**")

with col_title:
    st.markdown(
        "<h1 style='margin-bottom:0px;margin-top:0px;'>HubStream</h1>"
        "<p style='margin-top:0px;color:#555;font-size:14px;'>AI-powered content generation for HubSpot, LinkedIn, and more</p>",
        unsafe_allow_html=True,
    )

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key status
    api_keys_configured = all([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("HUBSPOT_ACCESS_TOKEN"),
        os.getenv("SERP_API_KEY")
    ])
    
    if api_keys_configured:
        st.success("✅ API Keys configured")
    else:
        st.warning("⚠️ Missing API Keys")
        st.info("Please set up .env file with required keys")
    
    database_path = os.getenv("DATABASE_PATH", "./hubstream.db")
    st.text(f"Database: {database_path}")
    
    st.divider()
    
    # Workflow Progress Tracker - Single central bar (sticky in sidebar)
    st.markdown("### 📈 Overall Progress")
    workflow_progress_placeholder = st.empty()
    
    # Function to calculate and update progress
    def update_sidebar_progress(step_completion_dict):
        """Update the sidebar progress bar based on current workflow state"""
        # Calculate overall progress (0-1)
        overall_progress = sum(step_completion_dict.values()) / len(step_completion_dict)
        
        # Current step
        current_step = None
        for step, completion in step_completion_dict.items():
            if completion > 0 and completion < 1:
                current_step = step
                break
        if not current_step and overall_progress == 0:
            current_step = "Campaign Setup"
        elif not current_step and overall_progress == 1:
            current_step = "Complete!"
        else:
            current_step = current_step or "Next Step"
        
        with workflow_progress_placeholder.container():
            st.progress(overall_progress)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.metric("Progress", f"{int(overall_progress*100)}%")
            with col2:
                st.markdown(f"**{current_step}**")
            with col3:
                st.markdown(f"Step {list(step_completion_dict.keys()).index(current_step) + 1}/6" if current_step != "Complete!" else "✅ Done")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📤 Discover & Generate", "📝 Edit Content", "📊 History", "ℹ️ About"])

# TAB 1: DISCOVERY & GENERATION
with tab1:
    st.header("Campaign Setup & Content Generation")
    
    # STEP 1: Campaign Configuration
    st.subheader("Step 1: Campaign Configuration")
    
    # Load saved configurations
    db = Database()
    saved_configs = db.list_campaign_configs()
    config_names = [cfg["config_name"] for cfg in saved_configs]
    
    col_load, col_new = st.columns([2, 1])
    with col_load:
        if config_names:
            selected_config = st.selectbox(
                "📂 Load Saved Configuration",
                options=["--- Create New ---"] + config_names,
                key="selected_config"
            )
        else:
            selected_config = "--- Create New ---"
            st.info("No saved configurations yet. Fill in the form below to create a new one.")
    
    # Load configuration if selected
    if selected_config != "--- Create New ---":
        loaded_config = db.load_campaign_config(selected_config)
        if loaded_config:
            st.success(f"✅ Loaded configuration: {selected_config}")
    else:
        loaded_config = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        audience_context = st.text_area(
            "Target Audience Description",
            value=loaded_config.get("audience_context", "") if loaded_config else "",
            placeholder="E.g., B2B SaaS marketing managers, HubSpot users, growth-focused professionals",
            height=100,
            help="Describe your target audience: industry, pain points, goals, etc."
        )
    
    with col2:
        tone_of_voice = st.text_area(
            "Tone of Voice",
            value=loaded_config.get("tone_of_voice", "") if loaded_config else "",
            placeholder="E.g., Professional yet approachable, data-driven, inspiring, conversational",
            height=100,
            help="How should the content sound? What's your brand voice?"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        email_outline = st.text_area(
            "Email Outline / Structure",
            value=loaded_config.get("email_outline", "") if loaded_config else "",
            placeholder="E.g., Hook - Problem - Solution - CTA",
            height=100,
            help="Provide the structure or key sections for the email"
        )
    
    with col2:
        newsletter_outline = st.text_area(
            "LinkedIn Newsletter Outline",
            value=loaded_config.get("newsletter_outline", "") if loaded_config else "",
            placeholder="E.g., Introduction - Main Points - Expert Insights - CTA",
            height=100,
            help="Provide the structure for the newsletter article"
        )
    
    # Save Configuration Button
    col_save, col_delete = st.columns([2, 1])
    with col_save:
        config_name = st.text_input(
            "💾 Save This Configuration As",
            value=selected_config if selected_config != "--- Create New ---" else "",
            placeholder="E.g., 'Marketing Managers 2025', 'Enterprise SaaS'"
        )
        if st.button("Save Configuration", use_container_width=True):
            if config_name and config_name.strip():
                db.save_campaign_config(
                    config_name.strip(),
                    audience_context,
                    tone_of_voice,
                    email_outline,
                    newsletter_outline
                )
                st.success(f"✅ Configuration '{config_name}' saved successfully!")
                st.rerun()
            else:
                st.error("Please enter a configuration name")
    
    with col_delete:
        if selected_config != "--- Create New ---":
            if st.button("🗑️ Delete", use_container_width=True):
                db.delete_campaign_config(selected_config)
                st.success(f"Deleted configuration: {selected_config}")
                st.rerun()
    
    # Calculate Step 1 completion
    step1_fields = [audience_context, tone_of_voice, email_outline, newsletter_outline]
    step1_completion = len([f for f in step1_fields if f and f.strip()]) / 4
    
    st.divider()
    
    # STEP 2: Your Ideas Input
    st.subheader("Step 2: Your Ideas (Manual Input)")
    st.markdown("💡 Enter your own content ideas below. These will be combined with AI-discovered topics.")
    
    num_ideas = st.number_input("How many ideas would you like to add?", min_value=0, max_value=5, value=1)
    
    user_ideas_list = []
    for i in range(num_ideas):
        col1, col2 = st.columns([2, 1])
        with col1:
            title = st.text_input(f"Idea {i+1} - Title", placeholder="E.g., 'AI-powered email personalization'")
        with col2:
            desc = st.text_input(f"Idea {i+1} - Description (optional)", placeholder="Brief description")
        
        if title:
            user_ideas_list.append({"title": title, "description": desc or None})
    
    # Step 2 progress tracker
    step2_completion = len(user_ideas_list) / max(num_ideas, 1) if num_ideas > 0 else 0
    
    st.divider()
    
    # STEP 3: Discover Web Ideas
    st.subheader("Step 3: AI-Discovered Ideas (Last 7 Days)")
    st.markdown("🔍 Click below to search for recent HubSpot updates and automatically generate ideas.")
    
    if st.button("🔍 Discover Web Ideas from HubSpot Updates", use_container_width=True, type="secondary"):
        if not audience_context or not email_outline or not newsletter_outline:
            st.error("Please fill in Campaign Configuration first")
        else:
            with st.spinner("🔍 Searching for HubSpot updates..."):
                try:
                    discovery = DiscoveryEngine()
                    db = Database(database_path)
                    
                    # Discover web ideas
                    search_queries = [
                        "HubSpot new features 2025",
                        "HubSpot product updates",
                        "HubSpot tips and best practices"
                    ]
                    
                    web_ideas_list = discovery.discover_web_ideas(search_queries, audience_context)
                    
                    if web_ideas_list:
                        # Save to database
                        for idea in web_ideas_list:
                            db.insert_web_idea(
                                title=idea['title'],
                                summary=idea['summary'],
                                source_url=idea['source_url'],
                                source=idea['source']
                            )
                        
                        st.session_state.web_ideas = web_ideas_list
                        st.success(f"✅ Found {len(web_ideas_list)} relevant topics from the web!")
                    else:
                        st.warning("No topics found. Check your API key or try again.")
                
                except Exception as e:
                    st.error(f"Error discovering topics: {e}")
    
    st.divider()
    
    # STEP 4: Ideas Overview & Selection
    if st.session_state.web_ideas or user_ideas_list:
        st.subheader("Step 4: Ideas Overview - Select Ideas for Topic Generation")
        st.markdown("📋 Choose which ideas should be considered for topic selection. Uncheck ideas you want to exclude.")
        
        selected_ideas = []
        
        # User Ideas Section
        if user_ideas_list:
            st.markdown("#### 👤 Your Ideas")
            for i, idea in enumerate(user_ideas_list):
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    include = st.checkbox("", value=True, key=f"user_idea_{i}")
                with col2:
                    st.write(f"**{idea['title']}**")
                    if idea.get('description'):
                        st.caption(idea['description'])
                
                if include:
                    selected_ideas.append({
                        "type": "user",
                        "title": idea['title'],
                        "description": idea.get('description', ''),
                        "source": "User Input"
                    })
        
        # Web Ideas Section
        if st.session_state.web_ideas:
            st.markdown("#### 🌐 AI-Found Ideas (Last 7 Days)")
            for i, idea in enumerate(st.session_state.web_ideas):
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    include = st.checkbox("", value=True, key=f"web_idea_{i}")
                with col2:
                    st.write(f"**{idea['title']}**")
                    st.caption(idea.get('summary', '')[:150] + "..." if len(idea.get('summary', '')) > 150 else idea.get('summary', ''))
                    
                    # Display source with clickable link
                    source_url = idea.get('source_url')
                    source_name = idea['source']
                    discovered_date = idea.get('discovered_at', '')[:10]
                    
                    if source_url:
                        st.markdown(f"🔗 [{source_name}]({source_url}) | {discovered_date}")
                    else:
                        st.caption(f"🔗 {source_name} | {discovered_date}")
                
                if include:
                    selected_ideas.append({
                        "type": "web",
                        "title": idea['title'],
                        "summary": idea.get('summary', ''),
                        "source_url": idea.get('source_url'),
                        "source": idea['source'],
                        "source_type": "web"
                    })
        
        # Confirmation Button
        if st.button("✅ Continue with Selected Ideas", use_container_width=True, type="primary"):
            if not selected_ideas:
                st.error("Please select at least one idea")
            else:
                st.session_state.candidate_topics = selected_ideas
                st.session_state.ideas_confirmed = True
                st.success(f"✅ Selected {len(selected_ideas)} ideas for topic ranking")
                st.rerun()
    
    st.divider()
    
    # STEP 5: Topic Selection (from candidate ideas)
    if st.session_state.ideas_confirmed and st.session_state.candidate_topics:
        st.subheader("Step 5: Topic Selection - AI Ranking")
        st.markdown("🎯 HubStream AI has ranked your ideas by relevance. Choose one to proceed with content generation.")
        
        with st.spinner("Ranking topics by relevance..."):
            try:
                selector = TopicSelector()
                db = Database(database_path)
                
                # Convert candidate topics to topic format for scoring
                topics_to_score = []
                for candidate in st.session_state.candidate_topics:
                    topic = {
                        "title": candidate['title'],
                        "description": candidate.get('summary', candidate.get('description', '')),
                        "source": candidate.get('source', 'User'),
                        "source_url": candidate.get('source_url'),
                        "source_type": candidate.get('source_type', 'user'),
                        "published_date": datetime.now().isoformat()
                    }
                    topics_to_score.append(topic)
                
                # Score and rank
                ranked_topics = selector.rank_topics(topics_to_score, audience_context)
                
                # Display best topic
                if ranked_topics:
                    best_topic = ranked_topics[0]
                    st.success(f"🏆 Most Relevant Topic Selected")
                    
                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        st.markdown(f"### {best_topic['title']}")
                        st.write(best_topic.get('description', ''))
                    with col2:
                        score = best_topic.get('overall_score', 0)
                        st.metric("Relevance Score", f"{score:.2%}")
                    
                    # Option to select different topic
                    if len(ranked_topics) > 1:
                        st.markdown("---")
                        st.markdown("**Or choose a different topic:**")
                        
                        topic_options = {
                            f"{t['title'][:50]}... ({t.get('overall_score', 0):.0%} match)": t
                            for t in ranked_topics
                        }
                        
                        selected_topic_name = st.selectbox(
                            "Select topic for content generation",
                            options=list(topic_options.keys()),
                            index=0,
                            label_visibility="collapsed"
                        )
                        
                        st.session_state.selected_topic = topic_options[selected_topic_name]
                    else:
                        st.session_state.selected_topic = best_topic
                    
                    # Content generation button
                    st.divider()
                    if st.button("✨ Generate Content from Selected Topic", use_container_width=True, type="primary"):
                        with st.spinner("✨ Generating content (this may take 1-2 minutes)..."):
                            try:
                                processor = ContentProcessor()
                                
                                content = processor.generate_all_content(
                                    topic=st.session_state.selected_topic,
                                    audience_context=audience_context,
                                    email_outline=email_outline,
                                    newsletter_outline=newsletter_outline,
                                    tone_of_voice=tone_of_voice
                                )
                                
                                st.session_state.generated_content = content
                                st.success("✅ Content generated successfully!")
                                st.rerun()
                            
                            except Exception as e:
                                st.error(f"Error generating content: {e}")
            
            except Exception as e:
                st.error(f"Error ranking topics: {e}")
    
    st.divider()
    
    # STEP 6: Display Generated Content
    if st.session_state.generated_content:
        st.subheader("Step 6: Generated Content Preview")
        st.markdown(f"📄 Content generated for: **{st.session_state.selected_topic.get('title')}**")
        
        content = st.session_state.generated_content
        
        tab_email, tab_newsletter, tab_post, tab_video = st.tabs([
            "📧 Email",
            "📰 Newsletter",
            "📱 LinkedIn Post",
            "🎬 Video Script"
        ])
        
        with tab_email:
            st.write(content['email'])
            st.button("Copy Email to Clipboard", key="copy_email")
        
        with tab_newsletter:
            st.write(content['newsletter'])
            st.button("Copy Newsletter to Clipboard", key="copy_newsletter")
        
        with tab_post:
            st.write(content['post'])
            st.button("Copy Post to Clipboard", key="copy_post")
        
        with tab_video:
            st.write(content['video_script'])
            st.button("Copy Script to Clipboard", key="copy_video")
        
        # Push to HubSpot
        st.divider()
        if st.button("🚀 Push to HubSpot + Send Notifications", use_container_width=True, type="primary"):
            with st.spinner("Pushing content..."):
                try:
                    hubspot = HubSpotClient()
                    mailer = NotificationMailer()
                    db = Database(database_path)
                    
                    # Create content run
                    content_run_id = db.insert_content_run(
                        audience_context=audience_context,
                        tone_of_voice=tone_of_voice,
                        topic_id=0
                    )
                    
                    # Save generated content to database
                    db.insert_generated_content(content_run_id, "email", content['email'])
                    db.insert_generated_content(content_run_id, "newsletter", content['newsletter'])
                    db.insert_generated_content(content_run_id, "post", content['post'])
                    db.insert_generated_content(content_run_id, "video_script", content['video_script'])
                    
                    # Create HubSpot email draft
                    template_id = os.getenv("HUBSPOT_EMAIL_TEMPLATE_ID")
                    if template_id:
                        email_result = hubspot.clone_email_template(
                            template_id=template_id,
                            name=f"HubStream - {st.session_state.selected_topic['title'][:40]}",
                            html_content=content['email']
                        )
                        
                        if email_result:
                            db.update_content_run_with_email(
                                content_run_id,
                                email_result['email_id'],
                                email_result['email_url']
                            )
                            
                            # Send email notification
                            recipient = os.getenv("NOTIFICATION_EMAIL_TO")
                            if recipient:
                                mailer.mock_send_email(
                                    recipient,
                                    f"HubStream: Email Draft Ready - {st.session_state.selected_topic['title'][:40]}",
                                    f"Email draft is ready:\n{email_result['email_url']}"
                                )
                    
                    # Send social content notification
                    recipient = os.getenv("NOTIFICATION_EMAIL_TO")
                    if recipient:
                        mailer.mock_send_email(
                            recipient,
                            f"HubStream: Social Content Ready - {st.session_state.selected_topic['title'][:40]}",
                            f"LinkedIn Post:\n{content['post']}\n\nVideo Script:\n{content['video_script']}"
                        )
                    
                    st.success("✅ Content pushed to HubSpot and notifications sent!")
                    st.balloons()
                
                except Exception as e:
                    st.error(f"Error: {e}")

    # Update sidebar progress at the end of tab1
    try:
        # Calculate step completion
        step1_complete = 1.0 if step1_completion >= 0.75 else step1_completion
        step2_complete = 1.0 if len(user_ideas_list) >= max(num_ideas, 1) else (len(user_ideas_list) / max(num_ideas, 1) if num_ideas > 0 else 0)
        step3_complete = 1.0 if st.session_state.web_ideas else 0.0
        step4_complete = 1.0 if st.session_state.ideas_confirmed else 0.5 if (st.session_state.web_ideas or user_ideas_list) else 0.0
        step5_complete = 1.0 if st.session_state.selected_topic else 0.5 if st.session_state.candidate_topics else 0.0
        step6_complete = 1.0 if st.session_state.generated_content else 0.0
        
        # Update progress bar
        progress_dict = {
            "Campaign Setup": step1_complete,
            "Your Ideas": step2_complete,
            "Web Discovery": step3_complete,
            "Review Ideas": step4_complete,
            "Select Topic": step5_complete,
            "Generate": step6_complete
        }
        update_sidebar_progress(progress_dict)
    except:
        pass

# TAB 2: EDIT CONTENT
with tab2:
    st.header("Edit & Refine Content")
    st.info("Features for editing generated content coming soon")

# TAB 3: HISTORY
with tab3:
    st.header("Content History")
    
    try:
        db = Database(database_path)
        # Would display history from database
        st.info("View your past content runs and topics here")
    except Exception as e:
        st.error(f"Error loading history: {e}")

# TAB 4: ABOUT
with tab4:
    st.header("About HubStream 2.0")
    st.markdown("""
    **HubStream 2.0** is an intelligent content generation automation tool designed to:
    
    - 🔍 **Discover** relevant HubSpot topics and trends
    - 🎯 **Score** topics based on audience relevance, recency, and engagement potential
    - ✨ **Generate** high-quality content across 4 channels simultaneously:
      - Marketing Email (HubSpot)
      - LinkedIn Newsletter
      - LinkedIn Post
      - Video Script
    - 🚀 **Distribute** drafts and notifications with one click
    
    ### Key Features
    - AI-powered content generation using OpenAI GPT-4o
    - Multi-channel content strategy in minutes
    - HubSpot integration for email drafts
    - Topic scoring and ranking algorithm
    - Content history and versioning
    - Notification system for team coordination
    
    ### Architecture
    - **Frontend:** Streamlit (Python web app)
    - **AI:** OpenAI GPT-4o
    - **Search:** SerpApi for topic discovery
    - **CRM:** HubSpot Marketing Hub API
    - **Database:** SQLite for content versioning
    
    ### Contact & Support
    For issues or feature requests, contact the HubStream team.
    """)
