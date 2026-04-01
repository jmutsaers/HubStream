"""
Scraper module for HubStream 2.0
Handles web scraping using BeautifulSoup and URL fetching.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
from urllib.parse import urljoin


class Scraper:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch raw HTML from a URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_text_content(self, html: str) -> str:
        """Extract clean text content from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up excessive whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)

    def extract_images(self, html: str, base_url: str) -> list:
        """Extract image URLs from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # Handle relative URLs
                absolute_url = urljoin(base_url, src)
                images.append({
                    'url': absolute_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        
        return images

    def extract_headings_and_paragraphs(self, html: str) -> Dict[str, list]:
        """Extract main headings and paragraphs from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = h.get_text(strip=True)
            if text:
                headings.append({
                    'level': h.name,
                    'text': text
                })
        
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Filter out very short paragraphs
                paragraphs.append(text)
        
        return {
            'headings': headings,
            'paragraphs': paragraphs
        }

    def scrape_url(self, url: str) -> Optional[Dict]:
        """
        Scrape a URL and extract structured content.
        
        Returns:
            Dict with keys: raw_html, text_content, headings, paragraphs, images
        """
        html = self.fetch_url(url)
        if not html:
            return None
        
        text_content = self.extract_text_content(html)
        structured = self.extract_headings_and_paragraphs(html)
        images = self.extract_images(html, url)
        
        return {
            'url': url,
            'raw_html': html,
            'text_content': text_content,
            'headings': structured['headings'],
            'paragraphs': structured['paragraphs'],
            'images': images
        }
