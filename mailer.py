"""
Mailer module for HubStream 2.0
Handles sending notification emails to the user.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os


class NotificationMailer:
    """Sends notification emails for content runs."""
    
    def __init__(self, sender_email: Optional[str] = None, 
                 smtp_host: str = "smtp.gmail.com",
                 smtp_port: int = 587):
        """
        Initialize mailer (uses SMTP).
        
        Args:
            sender_email: Sender email address (uses NOTIFICATION_EMAIL_FROM env var if not provided)
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
        """
        self.sender_email = sender_email or os.getenv("NOTIFICATION_EMAIL_FROM", "no-reply@hubstream.local")
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        # Note: For production, use environment variables for credentials
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")

    def send_email_draft_notification(self, recipient_email: str,
                                     hubspot_email_id: str,
                                     hubspot_email_url: str,
                                     topic_title: str) -> bool:
        """
        Send notification that HubSpot email draft is ready.
        
        Args:
            recipient_email: Recipient email address
            hubspot_email_id: ID of the created HubSpot email
            hubspot_email_url: URL to view the email in HubSpot
            topic_title: Title of the topic/content
        
        Returns:
            True if sent successfully
        """
        subject = f"HubStream: Email Draft Ready - {topic_title[:40]}"
        
        body = f"""Hi there,

Your HubStream content run is ready for review!

📧 EMAIL DRAFT
Topic: {topic_title}
Email ID: {hubspot_email_id}

Review and schedule your email here:
{hubspot_email_url}

The email is currently in DRAFT status in HubSpot. Review the content, make any final edits, and schedule the send.

Happy sending!
HubStream Team
"""
        
        return self._send_smtp_email(recipient_email, subject, body)

    def send_social_content_notification(self, recipient_email: str,
                                        linkedin_post: str,
                                        video_script: str,
                                        topic_title: str,
                                        newsletter: Optional[str] = None) -> bool:
        """
        Send notification with LinkedIn post and video script.
        
        Args:
            recipient_email: Recipient email address
            linkedin_post: Generated LinkedIn post content
            video_script: Generated video script content
            topic_title: Title of the topic/content
            newsletter: Optional newsletter content
        
        Returns:
            True if sent successfully
        """
        subject = f"HubStream: Social Content Ready - {topic_title[:40]}"
        
        # Build email body with proper formatting
        body = f"""Hi there,

Your social content for "{topic_title}" is ready!

📱 LINKEDIN POST
{'-' * 50}
{linkedin_post}
{'-' * 50}

You can copy this directly to LinkedIn or use the HubStream app to copy to clipboard.


🎬 VIDEO SCRIPT (60-90 seconds)
{'-' * 50}
{video_script}
{'-' * 50}

Use this script for your video recording or adaptation.
"""
        
        if newsletter:
            body += f"""

📰 LINKEDIN NEWSLETTER (Full Article)
{'-' * 50}
{newsletter[:1000]}... [see full on HubStream app]
{'-' * 50}
"""
        
        body += """

All content is ready to publish. Review in the HubStream app and adapt as needed.

Happy creating!
HubStream Team
"""
        
        return self._send_smtp_email(recipient_email, subject, body)

    def _send_smtp_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Send email via SMTP.
        
        Args:
            recipient_email: Recipient email address
            subject: Email subject
            body: Email body (plain text)
        
        Returns:
            True if sent successfully
        """
        try:
            # If using Gmail or SMTP with authentication
            if self.smtp_user and self.smtp_password:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
            else:
                # Fallback: local SMTP without auth (for testing)
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Attach plain text part
            text_part = MIMEText(body, "plain")
            message.attach(text_part)
            
            # Send
            server.sendmail(self.sender_email, recipient_email, message.as_string())
            server.quit()
            
            print(f"Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def mock_send_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Mock email send for development/testing (prints to console instead).
        
        Args:
            recipient_email: Recipient email address
            subject: Email subject
            body: Email body
        
        Returns:
            True (always succeeds)
        """
        print(f"\n{'='*60}")
        print(f"[MOCK EMAIL SENT]")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print(f"{'='*60}\n")
        return True
