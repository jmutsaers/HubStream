"""
Database module for HubStream 2.0
Handles SQLite CRUD operations for persisting content runs, topics, and generated content.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


class Database:
    def __init__(self, db_path: str = "hubstream.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # ContentRun table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    selected_topic_id INTEGER,
                    audience_context TEXT,
                    tone_of_voice TEXT,
                    hubspot_email_id TEXT,
                    hubspot_email_url TEXT,
                    status TEXT DEFAULT 'draft'
                )
            """)
            
            # User Ideas table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_ideas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    used_in_run INTEGER
                )
            """)
            
            # Web Ideas table (AI-discovered from web)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS web_ideas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    summary TEXT,
                    source_url TEXT UNIQUE,
                    source TEXT,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    used_in_run INTEGER
                )
            """)
            
            # Topics table (merged topics from ideas)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    source TEXT,
                    source_url TEXT,
                    source_type TEXT,
                    published_date TIMESTAMP,
                    discovery_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    overall_score REAL,
                    audience_relevance REAL,
                    recency REAL,
                    strategic_value REAL,
                    linkedin_potential REAL,
                    reuse_potential REAL,
                    raw_content TEXT,
                    UNIQUE(source_url)
                )
            """)
            
            # Content table (stores generated content for each run)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS generated_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_run_id INTEGER NOT NULL,
                    content_type TEXT NOT NULL,
                    title TEXT,
                    body TEXT,
                    html_body TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified TIMESTAMP,
                    version INTEGER DEFAULT 1,
                    FOREIGN KEY (content_run_id) REFERENCES content_runs(id)
                )
            """)
            
            # URLs cache table (to avoid re-scraping)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    raw_content TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Campaign Configurations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS campaign_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_name TEXT NOT NULL UNIQUE,
                    audience_context TEXT,
                    tone_of_voice TEXT,
                    email_outline TEXT,
                    newsletter_outline TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()

    def insert_topic(self, topic_data: Dict) -> int:
        """Insert a topic and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO topics (
                    title, description, source, source_url, source_type,
                    published_date, overall_score, audience_relevance,
                    recency, strategic_value, linkedin_potential, reuse_potential,
                    raw_content
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_url) DO UPDATE SET
                    published_date = excluded.published_date,
                    overall_score = excluded.overall_score
            """, (
                topic_data.get('title'),
                topic_data.get('description'),
                topic_data.get('source'),
                topic_data.get('source_url'),
                topic_data.get('source_type', 'web'),
                topic_data.get('published_date'),
                topic_data.get('overall_score', 0.0),
                topic_data.get('audience_relevance', 0.0),
                topic_data.get('recency', 0.0),
                topic_data.get('strategic_value', 0.0),
                topic_data.get('linkedin_potential', 0.0),
                topic_data.get('reuse_potential', 0.0),
                topic_data.get('raw_content')
            ))
            conn.commit()
            return cursor.lastrowid

    def insert_user_idea(self, title: str, description: Optional[str] = None) -> int:
        """Insert a user-provided idea."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_ideas (title, description)
                VALUES (?, ?)
            """, (title, description))
            conn.commit()
            return cursor.lastrowid

    def get_user_ideas(self) -> List[Dict]:
        """Get all user ideas."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_ideas ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def insert_web_idea(self, title: str, summary: str, source_url: str, 
                       source: Optional[str] = None) -> int:
        """Insert a web-discovered idea."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO web_ideas (title, summary, source_url, source)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(source_url) DO UPDATE SET
                    discovered_at = CURRENT_TIMESTAMP
            """, (title, summary, source_url, source))
            conn.commit()
            return cursor.lastrowid

    def get_web_ideas(self, days_back: int = 7) -> List[Dict]:
        """Get web ideas from the last N days."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM web_ideas 
                WHERE datetime(discovered_at) > datetime('now', ?)
                ORDER BY discovered_at DESC
            """, (f"-{days_back} days",))
            return [dict(row) for row in cursor.fetchall()]

    def get_topics_by_score(self, limit: int = 20) -> List[Dict]:
        """Get top topics sorted by overall score."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM topics
                ORDER BY overall_score DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def insert_content_run(self, audience_context: str, tone_of_voice: str, topic_id: int) -> int:
        """Insert a new content run and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO content_runs (
                    selected_topic_id, audience_context, tone_of_voice
                ) VALUES (?, ?, ?)
            """, (topic_id, audience_context, tone_of_voice))
            conn.commit()
            return cursor.lastrowid

    def insert_generated_content(self, content_run_id: int, content_type: str, 
                                body: str, html_body: Optional[str] = None, 
                                title: Optional[str] = None) -> int:
        """Insert generated content (email, newsletter, post, video script) and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO generated_content (
                    content_run_id, content_type, title, body, html_body
                ) VALUES (?, ?, ?, ?, ?)
            """, (content_run_id, content_type, title, body, html_body))
            conn.commit()
            return cursor.lastrowid

    def get_generated_content(self, content_run_id: int) -> Dict[str, Dict]:
        """Get all generated content for a run, organized by type."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM generated_content
                WHERE content_run_id = ?
                ORDER BY content_type, created_at
            """, (content_run_id,))
            
            content_by_type = {}
            for row in cursor.fetchall():
                content_type = row['content_type']
                if content_type not in content_by_type:
                    content_by_type[content_type] = []
                content_by_type[content_type].append(dict(row))
            
            return content_by_type

    def cache_scraped_url(self, url: str, content: str) -> None:
        """Cache scraped URL content."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scraped_urls (url, raw_content)
                VALUES (?, ?)
                ON CONFLICT(url) DO UPDATE SET raw_content = excluded.raw_content
            """, (url, content))
            conn.commit()

    def get_cached_content(self, url: str) -> Optional[str]:
        """Get cached content for a URL."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT raw_content FROM scraped_urls WHERE url = ?
            """, (url,))
            row = cursor.fetchone()
            return row[0] if row else None

    def update_content_run_with_email(self, content_run_id: int, 
                                     email_id: str, email_url: str) -> None:
        """Update content run with HubSpot email ID and URL."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE content_runs
                SET hubspot_email_id = ?, hubspot_email_url = ?, status = 'published'
                WHERE id = ?
            """, (email_id, email_url, content_run_id))
            conn.commit()

    def get_content_run(self, content_run_id: int) -> Optional[Dict]:
        """Get a specific content run."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM content_runs WHERE id = ?
            """, (content_run_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def save_campaign_config(self, config_name: str, audience_context: str, 
                           tone_of_voice: str, email_outline: str, 
                           newsletter_outline: str) -> int:
        """Save a campaign configuration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO campaign_configs 
                (config_name, audience_context, tone_of_voice, email_outline, newsletter_outline, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (config_name, audience_context, tone_of_voice, email_outline, newsletter_outline))
            conn.commit()
            return cursor.lastrowid

    def load_campaign_config(self, config_name: str) -> Optional[Dict]:
        """Load a saved campaign configuration."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM campaign_configs WHERE config_name = ?
            """, (config_name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_campaign_configs(self) -> List[Dict]:
        """Get list of all saved campaign configurations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, config_name, created_at, updated_at FROM campaign_configs 
                ORDER BY updated_at DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def delete_campaign_config(self, config_name: str) -> None:
        """Delete a saved campaign configuration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM campaign_configs WHERE config_name = ?
            """, (config_name,))
            conn.commit()
