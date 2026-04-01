"""
Processor module for HubStream 2.0
Handles AI-powered content generation using OpenAI GPT-4o.
"""

from openai import OpenAI
from typing import Optional, Dict
import os


class ContentProcessor:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            model: Model to use for content generation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def generate_email_content(self, topic: Dict, audience_context: str, 
                              email_outline: str, tone_of_voice: str) -> str:
        """
        Generate email content for HubSpot mailing.
        
        Args:
            topic: Selected topic with title and description
            audience_context: Target audience description
            email_outline: Email structure outline provided by user
            tone_of_voice: Brand tone of voice
        
        Returns:
            Generated email body (HTML or rich text)
        """
        prompt = f"""You are an expert B2B marketing copywriter specializing in HubSpot content.

Your task is to write a marketing email based on the following information:

TOPIC:
Title: {topic.get('title', '')}
Description: {topic.get('description', '')}

TARGET AUDIENCE:
{audience_context}

EMAIL OUTLINE/STRUCTURE:
{email_outline}

TONE OF VOICE:
{tone_of_voice}

REQUIREMENTS:
- Write in a clear, professional B2B voice
- Use short paragraphs (2-3 sentences max)
- Include a compelling subject line
- Include a clear hook/opening that captures attention
- Include exactly ONE main call-to-action (CTA)
- Format as readable plain text with clear sections
- Keep the email concise (under 300 words excluding subject line)
- Make it actionable and benefit-focused for the audience

OUTPUT FORMAT:
Start with "SUBJECT LINE: " followed by the subject line.
Then start a new line and write the email body.
Use clear section breaks with dashes (---) if needed."""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content

    def generate_newsletter_content(self, topic: Dict, audience_context: str,
                                   newsletter_outline: str, tone_of_voice: str) -> str:
        """
        Generate LinkedIn newsletter article.
        
        Args:
            topic: Selected topic with title and description
            audience_context: Target audience description
            newsletter_outline: Newsletter structure outline provided by user
            tone_of_voice: Brand tone of voice
        
        Returns:
            Generated newsletter content
        """
        prompt = f"""You are an expert B2B and SaaS content writer specializing in LinkedIn newsletters for growth marketers and HubSpot users.

Your task is to write a LinkedIn newsletter article based on:

TOPIC:
Title: {topic.get('title', '')}
Description: {topic.get('description', '')}

TARGET AUDIENCE:
{audience_context}

NEWSLETTER STRUCTURE/OUTLINE:
{newsletter_outline}

TONE OF VOICE:
{tone_of_voice}

REQUIREMENTS:
- Write a compelling introduction that hooks the reader immediately
- Include 2-3 clear main sections with helpful subheadings
- Make it practical, actionable, and insightful
- Use short paragraphs and varied sentence structure
- Include specific examples or tips when possible
- End with a clear call-to-action (link, follow, comment, etc.)
- Optimize for LinkedIn (scannable, engaging, professional)
- Length: 700-1200 words

OUTPUT:
Write the full newsletter article, formatted for LinkedIn."""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content

    def generate_linkedin_post(self, topic: Dict, audience_context: str,
                              newsletter_snippet: str, tone_of_voice: str) -> str:
        """
        Generate a standalone LinkedIn post.
        
        Args:
            topic: Selected topic with title and description
            audience_context: Target audience description
            newsletter_snippet: Key insight from the newsletter to reference
            tone_of_voice: Brand tone of voice
        
        Returns:
            Generated LinkedIn post
        """
        prompt = f"""You are a LinkedIn content expert writing for growth marketers and HubSpot professionals.

Create a LinkedIn post based on:

TOPIC:
Title: {topic.get('title', '')}
Description: {topic.get('description', '')}

TARGET AUDIENCE:
{audience_context}

KEY INSIGHT/SNIPPET:
{newsletter_snippet}

TONE OF VOICE:
{tone_of_voice}

REQUIREMENTS:
- Open with a strong hook or attention-grabbing statement (first 1-2 lines CRITICAL)
- Keep total length: 80-180 words
- Use 1-3 short paragraphs
- Optional: use 2-4 short bullet points for key insights
- Include ONE clear call-to-action (e.g., "Drop a comment below", "Click the link", "Share your thoughts", etc.)
- Use conversational, authentic language
- No emoji unless absolutely necessary for the message
- Max 3 relevant hashtags (optional)

OUTPUT:
Write the LinkedIn post exactly as it would appear."""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content

    def generate_video_script(self, topic: Dict, audience_context: str,
                             tone_of_voice: str) -> str:
        """
        Generate a video script (60-90 seconds).
        
        Args:
            topic: Selected topic with title and description
            audience_context: Target audience description
            tone_of_voice: Brand tone of voice
        
        Returns:
            Generated video script
        """
        prompt = f"""You are a video scriptwriter for B2B SaaS content targeting growth marketers and HubSpot users.

Create a 60-90 second video script based on:

TOPIC:
Title: {topic.get('title', '')}
Description: {topic.get('description', '')}

TARGET AUDIENCE:
{audience_context}

TONE OF VOICE:
{tone_of_voice}

REQUIREMENTS:
- Structure: Hook (5-10 sec) → Problem → Solution (HubSpot/feature) → Example/Proof → CTA
- Write in conversational, spoken language (as if narrating to camera)
- Avoid long sentences; use short, punchy phrasing
- Target: ~150-180 words (fits 60-90 seconds when spoken at normal pace)
- Include natural pauses marked as [PAUSE]
- Include [OPTIONAL VISUAL] notes for on-screen graphics/examples
- End with a clear call-to-action
- Sound authentic, not scripted

OUTPUT:
Format as:

[Hook]
[Spoken content]
[PAUSE]
[OPTIONAL VISUAL: description]
...and so on"""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=800,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content

    def generate_all_content(self, topic: Dict, audience_context: str,
                            email_outline: str, newsletter_outline: str,
                            tone_of_voice: str) -> Dict[str, str]:
        """
        Generate all four content types in one go.
        
        Returns:
            Dict with keys: email, newsletter, post, video_script
        """
        print("Generating email content...")
        email = self.generate_email_content(topic, audience_context, email_outline, tone_of_voice)
        
        print("Generating newsletter content...")
        newsletter = self.generate_newsletter_content(topic, audience_context, newsletter_outline, tone_of_voice)
        
        print("Generating LinkedIn post...")
        post = self.generate_linkedin_post(topic, audience_context, newsletter[:200], tone_of_voice)
        
        print("Generating video script...")
        video_script = self.generate_video_script(topic, audience_context, tone_of_voice)
        
        return {
            'email': email,
            'newsletter': newsletter,
            'post': post,
            'video_script': video_script
        }
