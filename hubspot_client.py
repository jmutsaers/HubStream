"""
HubSpot Client module for HubStream 2.0
Handles HubSpot API v3 integration for email marketing.
"""

import requests
from typing import Optional, Dict
import os


class HubSpotClient:
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize HubSpot API client.
        
        Args:
            access_token: HubSpot private app access token
        """
        self.access_token = access_token or os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def clone_email_template(self, template_id: str, name: str, 
                            html_content: str) -> Optional[Dict]:
        """
        Clone an existing email template and update its content.
        
        Args:
            template_id: Source template ID to clone from
            name: Name for the new email
            html_content: HTML content for the email body
        
        Returns:
            Dict with email_id and email_url, or None if failed
        """
        # Step 1: Fetch the source template
        template_url = f"{self.base_url}/marketing/v3/emails/{template_id}"
        response = requests.get(template_url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"Error fetching template: {response.status_code}")
            return None
        
        template_data = response.json()
        
        # Step 2: Create new email based on template
        # Clone the template by creating a new email with the necessary fields
        new_email_data = {
            "name": name,
            "subject": template_data.get("subject", "HubStream Generated Email"),
            "from_name": template_data.get("from_name", "HubStream"),
            "preview_text": template_data.get("preview_text", ""),
            "html": html_content,
            "status": "DRAFT"
        }
        
        create_url = f"{self.base_url}/marketing/v3/emails"
        response = requests.post(create_url, headers=self.headers, json=new_email_data)
        
        if response.status_code not in [200, 201]:
            print(f"Error creating email: {response.status_code} - {response.text}")
            return None
        
        email = response.json()
        email_id = email.get("id")
        
        # Construct public URL for the email
        email_url = f"https://app.hubspot.com/crm/email/{email_id}/"
        
        return {
            "email_id": email_id,
            "email_url": email_url,
            "name": email.get("name"),
            "status": email.get("status")
        }

    def update_email_content(self, email_id: str, html_content: str) -> bool:
        """
        Update an existing email's HTML content.
        
        Args:
            email_id: Email ID to update
            html_content: New HTML content
        
        Returns:
            True if successful, False otherwise
        """
        update_url = f"{self.base_url}/marketing/v3/emails/{email_id}"
        update_data = {"html": html_content}
        
        response = requests.patch(update_url, headers=self.headers, json=update_data)
        
        if response.status_code not in [200, 204]:
            print(f"Error updating email: {response.status_code}")
            return False
        
        return True

    def get_email(self, email_id: str) -> Optional[Dict]:
        """Get email details."""
        url = f"{self.base_url}/marketing/v3/emails/{email_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"Error fetching email: {response.status_code}")
            return None
        
        return response.json()

    def upload_file(self, file_path: str, file_name: str) -> Optional[str]:
        """
        Upload a file to HubSpot File Manager.
        
        Args:
            file_path: Local file path to upload
            file_name: Name for the file in HubSpot
        
        Returns:
            File URL if successful, None otherwise
        """
        upload_url = f"{self.base_url}/filemanager/api/v3/files/upload"
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            response = requests.post(upload_url, headers=self.headers, files=files)
        
        if response.status_code not in [200, 201]:
            print(f"Error uploading file: {response.status_code}")
            return None
        
        file_data = response.json()
        return file_data.get("url")

    def test_connection(self) -> bool:
        """Test HubSpot API connection."""
        url = f"{self.base_url}/marketing/v3/emails"
        response = requests.get(url, headers=self.headers, params={"limit": 1})
        
        if response.status_code == 200:
            return True
        else:
            print(f"Connection test failed: {response.status_code}")
            return False
