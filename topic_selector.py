"""
Topic Selector module for HubStream 2.0
Handles scoring and selection of topics based on multiple criteria.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import math


class TopicSelector:
    """Scores and selects the best topic based on multiple relevance factors."""
    
    def __init__(self, 
                 audience_weight: float = 0.3,
                 recency_weight: float = 0.2,
                 strategic_weight: float = 0.2,
                 linkedin_weight: float = 0.15,
                 reuse_weight: float = 0.15):
        """
        Initialize with weight factors for scoring.
        
        Args:
            audience_weight: Weight for audience relevance
            recency_weight: Weight for recency/timeliness
            strategic_weight: Weight for strategic value
            linkedin_weight: Weight for LinkedIn potential
            reuse_weight: Weight for reusability across channels
        """
        self.weights = {
            'audience': audience_weight,
            'recency': recency_weight,
            'strategic': strategic_weight,
            'linkedin': linkedin_weight,
            'reuse': reuse_weight
        }
        
        # Normalize weights
        total = sum(self.weights.values())
        for key in self.weights:
            self.weights[key] /= total

    def score_audience_relevance(self, topic: Dict, audience_context: str) -> float:
        """
        Score how relevant a topic is to the target audience.
        Simple keyword matching on topic title/description vs audience context.
        
        Args:
            topic: Topic dict with 'title' and 'description'
            audience_context: String describing target audience (ICP, industry, pain points)
        
        Returns:
            Score between 0 and 1
        """
        if not audience_context:
            return 0.5
        
        topic_text = f"{topic.get('title', '')} {topic.get('description', '')}".lower()
        audience_keywords = audience_context.lower().split()
        
        matches = sum(1 for keyword in audience_keywords if keyword in topic_text)
        max_matches = len(audience_keywords)
        
        return min(1.0, matches / max(max_matches, 1)) if max_matches > 0 else 0.5

    def score_recency(self, topic: Dict, days_threshold: int = 30) -> float:
        """
        Score based on how recent the content is.
        
        Args:
            topic: Topic dict with 'published_date' or 'discovery_date'
            days_threshold: Consider content older than this as less recent
        
        Returns:
            Score between 0 and 1 (1 = very recent)
        """
        date_str = topic.get('published_date') or topic.get('discovery_date')
        
        if not date_str:
            return 0.5
        
        try:
            if isinstance(date_str, str):
                # Try to parse ISO format
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date = date_str
            
            days_old = (datetime.now() - date).days
            
            # Decay function: fresh content scores high, older content scores lower
            recency_score = max(0, 1 - (days_old / days_threshold))
            return min(1.0, recency_score)
        except (ValueError, TypeError):
            return 0.5

    def score_strategic_value(self, topic: Dict) -> float:
        """
        Score strategic value based on topic source and type.
        Official HubSpot sources rank higher than general tech news.
        
        Args:
            topic: Topic dict with 'source' and 'source_type'
        
        Returns:
            Score between 0 and 1
        """
        source = (topic.get('source') or '').lower()
        source_type = (topic.get('source_type') or '').lower()
        
        score = 0.5  # baseline
        
        # Boost for official HubSpot sources
        if 'hubspot' in source or 'hubspot blog' in source:
            score = 0.9
        elif 'product update' in source or 'feature release' in source:
            score = 0.85
        elif 'community' in source:
            score = 0.75
        elif source_type == 'internal':
            score = 0.8
        else:
            score = 0.6
        
        return min(1.0, score)

    def score_linkedin_potential(self, topic: Dict) -> float:
        """
        Score potential for LinkedIn engagement.
        Topics with actionable insights, trends, or expert perspectives score higher.
        
        Args:
            topic: Topic dict
        
        Returns:
            Score between 0 and 1
        """
        title = (topic.get('title') or '').lower()
        description = (topic.get('description') or '').lower()
        combined = f"{title} {description}"
        
        score = 0.5  # baseline
        
        # Boost for engagement-driving keywords
        engagement_keywords = [
            'tip', 'trick', 'guide', 'how to', 'best practice',
            'trend', 'future', 'ai', 'automation', 'growth',
            'strategy', 'case study', 'mistake', 'lesson'
        ]
        
        matches = sum(1 for keyword in engagement_keywords if keyword in combined)
        score += (matches * 0.1)
        
        return min(1.0, score)

    def score_reuse_potential(self, topic: Dict) -> float:
        """
        Score how well a topic can be reused across multiple channels
        (email, LinkedIn newsletter, post, video).
        
        Args:
            topic: Topic dict
        
        Returns:
            Score between 0 and 1
        """
        description = (topic.get('description') or '').lower()
        
        score = 0.6  # baseline for most topics
        
        # Topics that reuse well across all channels
        multi_channel_keywords = [
            'feature', 'update', 'strategy', 'tip', 'best practice',
            'announcement', 'integration', 'case study'
        ]
        
        matches = sum(1 for keyword in multi_channel_keywords if keyword in description)
        
        # Avoid niche topics that won't work everywhere
        niche_keywords = ['beta', 'experimental', 'limited to']
        niche_matches = sum(1 for keyword in niche_keywords if keyword in description)
        
        score += (matches * 0.15) - (niche_matches * 0.1)
        
        return min(1.0, max(0.3, score))

    def calculate_overall_score(self, topic: Dict, audience_context: str = "") -> float:
        """
        Calculate overall score for a topic.
        
        Args:
            topic: Topic dict
            audience_context: Target audience description
        
        Returns:
            Overall score between 0 and 1
        """
        scores = {
            'audience': self.score_audience_relevance(topic, audience_context),
            'recency': self.score_recency(topic),
            'strategic': self.score_strategic_value(topic),
            'linkedin': self.score_linkedin_potential(topic),
            'reuse': self.score_reuse_potential(topic)
        }
        
        overall = sum(scores[key] * self.weights[key] for key in scores)
        
        # Store component scores in topic
        topic['audience_relevance'] = scores['audience']
        topic['recency'] = scores['recency']
        topic['strategic_value'] = scores['strategic']
        topic['linkedin_potential'] = scores['linkedin']
        topic['reuse_potential'] = scores['reuse']
        topic['overall_score'] = overall
        
        return overall

    def select_best_topic(self, topics: List[Dict], audience_context: str = "") -> Optional[Dict]:
        """
        Select the single best topic from a list.
        
        Args:
            topics: List of topic dicts
            audience_context: Target audience description
        
        Returns:
            The highest-scoring topic
        """
        if not topics:
            return None
        
        # Score all topics
        for topic in topics:
            self.calculate_overall_score(topic, audience_context)
        
        # Sort and return best
        sorted_topics = sorted(topics, key=lambda t: t.get('overall_score', 0), reverse=True)
        return sorted_topics[0] if sorted_topics else None

    def rank_topics(self, topics: List[Dict], audience_context: str = "") -> List[Dict]:
        """
        Rank all topics by score.
        
        Args:
            topics: List of topic dicts
            audience_context: Target audience description
        
        Returns:
            Sorted list of topics with scores
        """
        for topic in topics:
            self.calculate_overall_score(topic, audience_context)
        
        return sorted(topics, key=lambda t: t.get('overall_score', 0), reverse=True)
