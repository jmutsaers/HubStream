"""
Discovery module for HubStream 2.0
Handles topic discovery from SerpApi and enhanced idea generation with AI summaries.
"""

from serpapi import GoogleSearch
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta


class DiscoveryEngine:
    """Discovers HubSpot-related ideas from web search and generates summaries."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize discovery engine with SerpApi.
        
        Args:
            api_key: SerpApi API key (uses SERP_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("SERP_API_KEY")

    def search_hubspot_updates(self, query: str = "HubSpot updates features", 
                               num_results: int = 10) -> List[Dict]:
        """
        Search for recent HubSpot updates and features.
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of raw search results with title, snippet, link
        """
        try:
            # Use SerpApi GoogleSearch to search
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            search_results = []
            organic_results = results.get("organic_results", [])
            
            # Process organic results
            for result in organic_results[:num_results]:
                search_result = {
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "url": result.get("link", ""),
                    "source": result.get("source", "")
                }
                search_results.append(search_result)
            
            return search_results
        
        except Exception as e:
            print(f"Error in SerpApi search: {e}")
            return []

    def create_web_ideas(self, search_results: List[Dict], 
                        audience_context: str = "") -> List[Dict]:
        """
        Convert search results into structured ideas with AI summaries.
        Uses the snippet as a quick summary (no AI call needed here).
        
        Args:
            search_results: List of search results from SerpApi
            audience_context: Optional audience context for relevance
        
        Returns:
            List of idea dicts with title, summary, source_url, source_type
        """
        ideas = []
        
        for result in search_results:
            if not result.get("title") or not result.get("url"):
                continue
            
            idea = {
                "title": result.get("title", ""),
                "summary": result.get("snippet", "")[:200],  # Truncate to 200 chars
                "source_url": result.get("url", ""),
                "source": result.get("source", "Web"),
                "source_type": "web",
                "discovered_at": datetime.now().isoformat(),
                "id": None  # Will be set when inserted into DB
            }
            ideas.append(idea)
        
        return ideas

    def discover_web_ideas(self, search_queries: Optional[List[str]] = None,
                          audience_context: str = "") -> List[Dict]:
        """
        Discover web ideas from multiple search queries.
        
        Args:
            search_queries: Custom search queries (default: HubSpot updates)
            audience_context: Optional audience context
        
        Returns:
            Combined list of discovered web ideas
        """
        # Default search queries if not provided
        if not search_queries:
            search_queries = [
                "HubSpot new features 2025",
                "HubSpot product updates",
                "HubSpot best practices"
            ]
        
        all_ideas = []
        
        for query in search_queries:
            print(f"Searching: {query}")
            try:
                search_results = self.search_hubspot_updates(query, num_results=5)
                ideas = self.create_web_ideas(search_results, audience_context)
                all_ideas.extend(ideas)
            except Exception as e:
                print(f"Error processing query '{query}': {e}")
        
        # Remove duplicates by URL
        seen_urls = {}
        unique_ideas = []
        for idea in all_ideas:
            url = idea.get("source_url", "")
            if url and url not in seen_urls:
                seen_urls[url] = True
                unique_ideas.append(idea)
        
        print(f"Discovered {len(unique_ideas)} unique web ideas")
        return unique_ideas
