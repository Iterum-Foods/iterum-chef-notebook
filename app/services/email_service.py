"""
Email Service for Iterum Culinary App
Supports multiple email providers: SendGrid, Gmail SMTP, AWS SES, Mailgun
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Unified email service supporting multiple providers"""
    
    def __init__(self):
        self.provider = os.getenv('EMAIL_PROVIDER', 'smtp')  # smtp, sendgrid, ses, mailgun
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@iterumfoods.com')
        self.from_name = os.getenv('FROM_NAME', 'Iterum Foods')
        
        # SMTP Configuration (Gmail, etc.)
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        
        # SendGrid Configuration
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY', '')
        
        # AWS SES Configuration
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        # Mailgun Configuration
        self.mailgun_api_key = os.getenv('MAILGUN_API_KEY', '')
        self.mailgun_domain = os.getenv('MAILGUN_DOMAIN', '')
        
        # App URLs
        self.app_url = os.getenv('APP_URL', 'https://iterum-culinary-app.web.app')
        
        logger.info(f"📧 Email Service initialized with provider: {self.provider}")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        to_name: Optional[str] = None
    ) -> bool:
        """Send email using configured provider"""
        try:
            if self.provider == 'sendgrid':
                return self._send_via_sendgrid(to_email, to_name, subject, html_content, text_content)
            elif self.provider == 'ses':
                return self._send_via_ses(to_email, subject, html_content, text_content)
            elif self.provider == 'mailgun':
                return self._send_via_mailgun(to_email, subject, html_content, text_content)
            else:  # smtp (default)
                return self._send_via_smtp(to_email, subject, html_content, text_content)
        except Exception as e:
            logger.error(f"❌ Email sending failed: {e}")
            return False
    
    def _send_via_smtp(self, to_email: str, subject: str, html_content: str, text_content: Optional[str]) -> bool:
        """Send email via SMTP (Gmail, etc.)"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text version
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent via SMTP to {to_email}")
            return True
        except Exception as e:
            logger.error(f"❌ SMTP send failed: {e}")
            return False
    
    def _send_via_sendgrid(
        self,
        to_email: str,
        to_name: Optional[str],
        subject: str,
        html_content: str,
        text_content: Optional[str]
    ) -> bool:
        """Send email via SendGrid API"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email, to_name),
                subject=subject,
                html_content=Content("text/html", html_content)
            )
            
            if text_content:
                message.plain_text_content = Content("text/plain", text_content)
            
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            logger.info(f"✅ Email sent via SendGrid to {to_email} (status: {response.status_code})")
            return True
        except Exception as e:
            logger.error(f"❌ SendGrid send failed: {e}")
            return False
    
    def _send_via_ses(self, to_email: str, subject: str, html_content: str, text_content: Optional[str]) -> bool:
        """Send email via AWS SES"""
        try:
            import boto3
            
            client = boto3.client(
                'ses',
                region_name=self.aws_region,
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key
            )
            
            destination = {'ToAddresses': [to_email]}
            message = {
                'Subject': {'Data': subject},
                'Body': {
                    'Html': {'Data': html_content}
                }
            }
            
            if text_content:
                message['Body']['Text'] = {'Data': text_content}
            
            response = client.send_email(
                Source=f"{self.from_name} <{self.from_email}>",
                Destination=destination,
                Message=message
            )
            
            logger.info(f"✅ Email sent via AWS SES to {to_email} (MessageId: {response['MessageId']})")
            return True
        except Exception as e:
            logger.error(f"❌ AWS SES send failed: {e}")
            return False
    
    def _send_via_mailgun(self, to_email: str, subject: str, html_content: str, text_content: Optional[str]) -> bool:
        """Send email via Mailgun API"""
        try:
            import requests
            
            response = requests.post(
                f"https://api.mailgun.net/v3/{self.mailgun_domain}/messages",
                auth=("api", self.mailgun_api_key),
                data={
                    "from": f"{self.from_name} <{self.from_email}>",
                    "to": to_email,
                    "subject": subject,
                    "text": text_content or "",
                    "html": html_content
                }
            )
            
            response.raise_for_status()
            logger.info(f"✅ Email sent via Mailgun to {to_email}")
            return True
        except Exception as e:
            logger.error(f"❌ Mailgun send failed: {e}")
            return False
    
    # ===== TRIAL USER EMAILS =====
    
    def send_trial_welcome(self, user_name: str, user_email: str) -> bool:
        """Send welcome email to new trial user"""
        trial_end_date = (datetime.now() + timedelta(days=14)).strftime('%B %d, %Y')
        
        subject = f"🎁 Welcome to Your 14-Day Trial, {user_name}!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f9fafb;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background: #f9fafb; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 40px 30px; text-align: center;">
                                    <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 900;">
                                        🎉 Welcome to Iterum!
                                    </h1>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="color: #1f2937; font-size: 24px; font-weight: 800; margin: 0 0 16px 0;">
                                        Hi {user_name},
                                    </h2>
                                    
                                    <p style="color: #6b7280; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0;">
                                        Your <strong>14-day free trial</strong> is now active! You have full access to all premium features.
                                    </p>
                                    
                                    <!-- Trial Benefits Box -->
                                    <div style="background: #f0f9ff; border: 2px solid #0ea5e9; border-radius: 12px; padding: 24px; margin: 0 0 32px 0;">
                                        <h3 style="color: #0369a1; font-size: 18px; font-weight: 700; margin: 0 0 16px 0;">
                                            ✨ What's Included in Your Trial:
                                        </h3>
                                        <ul style="color: #0369a1; margin: 0; padding-left: 20px; line-height: 1.8;">
                                            <li><strong>Unlimited Recipe Development</strong> - Create and test as many recipes as you need</li>
                                            <li><strong>Unlimited Menu Creation</strong> - Build professional menus in minutes</li>
                                            <li><strong>Full Analytics & Insights</strong> - Track costs, nutrition, and performance</li>
                                            <li><strong>All Premium Features</strong> - Import, export, scale, and optimize</li>
                                        </ul>
                                    </div>
                                    
                                    <!-- Trial Expiration -->
                                    <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px 20px; margin: 0 0 32px 0;">
                                        <p style="color: #92400e; margin: 0; font-size: 15px;">
                                            <strong>📅 Trial Expires:</strong> {trial_end_date}
                                        </p>
                                    </div>
                                    
                                    <!-- CTA Button -->
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td align="center" style="padding: 0 0 32px 0;">
                                                <a href="{self.app_url}" 
                                                   style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                                                    🚀 Start Using Iterum
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Getting Started -->
                                    <h3 style="color: #1f2937; font-size: 20px; font-weight: 700; margin: 0 0 16px 0;">
                                        🎯 Quick Start Guide:
                                    </h3>
                                    <ol style="color: #6b7280; line-height: 1.8; margin: 0 0 32px 0; padding-left: 20px;">
                                        <li>Create your first recipe or import existing ones</li>
                                        <li>Build a professional menu in minutes</li>
                                        <li>Explore the ingredient database and smart search</li>
                                        <li>Try recipe scaling and cost optimization</li>
                                    </ol>
                                    
                                    <!-- Support -->
                                    <div style="background: #f9fafb; border-radius: 10px; padding: 20px; margin: 0 0 32px 0;">
                                        <p style="color: #6b7280; margin: 0; font-size: 15px; line-height: 1.6;">
                                            <strong style="color: #1f2937;">Need help?</strong> Just reply to this email - we read every message and respond quickly!
                                        </p>
                                    </div>
                                    
                                    <p style="color: #6b7280; font-size: 16px; line-height: 1.6; margin: 0;">
                                        Let's cook up something amazing together!
                                    </p>
                                    
                                    <p style="color: #1f2937; font-size: 16px; font-weight: 600; margin: 24px 0 0 0;">
                                        The Iterum Team<br>
                                        <span style="color: #9ca3af; font-size: 14px; font-weight: 400;">Building the future of professional kitchens</span>
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background: #f9fafb; padding: 30px 40px; text-align: center; border-top: 1px solid #e5e7eb;">
                                    <p style="color: #9ca3af; font-size: 13px; line-height: 1.6; margin: 0;">
                                        You're receiving this email because you started a free trial at {self.app_url}<br>
                                        © 2025 Iterum Foods. All rights reserved.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Iterum, {user_name}!
        
        Your 14-day free trial is now active!
        
        What's Included:
        - Unlimited Recipe Development
        - Unlimited Menu Creation
        - Full Analytics & Insights
        - All Premium Features
        
        Trial Expires: {trial_end_date}
        
        Get started: {self.app_url}
        
        Need help? Just reply to this email!
        
        The Iterum Team
        """
        
        return self.send_email(to_email, subject, html_content, text_content, user_name)
    
    def send_trial_reminder_day7(self, user_name: str, user_email: str) -> bool:
        """Send mid-trial check-in (7 days remaining)"""
        subject = f"⏰ {user_name}, you're halfway through your trial!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f9fafb;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background: #f9fafb; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <tr>
                                <td>
                                    <h2 style="color: #1f2937; font-size: 28px; font-weight: 800; margin: 0 0 20px 0;">
                                        Hi {user_name}, 👋
                                    </h2>
                                    
                                    <p style="color: #6b7280; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0;">
                                        You're <strong>halfway through your 14-day trial</strong>! How's it going?
                                    </p>
                                    
                                    <div style="background: #fff3e0; border-left: 4px solid #f59e0b; padding: 16px 20px; margin: 0 0 24px 0;">
                                        <p style="color: #92400e; margin: 0; font-size: 15px;">
                                            <strong>⏰ 7 days remaining</strong> in your trial
                                        </p>
                                    </div>
                                    
                                    <h3 style="color: #1f2937; font-size: 20px; font-weight: 700; margin: 0 0 16px 0;">
                                        Have you tried these features?
                                    </h3>
                                    
                                    <ul style="color: #6b7280; line-height: 1.8; margin: 0 0 32px 0;">
                                        <li><strong>Recipe Import</strong> - Upload PDFs, Word docs, or paste text</li>
                                        <li><strong>Menu Builder</strong> - Create professional menus in minutes</li>
                                        <li><strong>Cost Analysis</strong> - Real-time ingredient pricing</li>
                                        <li><strong>Recipe Scaling</strong> - Perfect portions every time</li>
                                    </ul>
                                    
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td align="center" style="padding: 0 0 24px 0;">
                                                <a href="{self.app_url}" 
                                                   style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 14px 32px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 15px;">
                                                    Continue Exploring →
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; margin: 0 0 24px 0;">
                                        <p style="color: #0369a1; margin: 0; font-size: 15px; line-height: 1.6;">
                                            <strong>💡 Need help?</strong> Reply to this email or book a quick call with our team!
                                        </p>
                                    </div>
                                    
                                    <p style="color: #6b7280; font-size: 15px; line-height: 1.6; margin: 0;">
                                        Keep innovating!<br><br>
                                        <strong style="color: #1f2937;">The Iterum Team</strong>
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content, None, user_name)
    
    def send_trial_expiring_soon(self, user_name: str, user_email: str, days_left: int) -> bool:
        """Send trial expiration warning (4 or 2 days left)"""
        subject = f"⚡ {days_left} days left in your trial - Special offer inside"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f9fafb;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background: #f9fafb; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <tr>
                                <td>
                                    <div style="text-align: center; margin: 0 0 24px 0;">
                                        <span style="font-size: 64px;">⚡</span>
                                    </div>
                                    
                                    <h2 style="color: #1f2937; font-size: 28px; font-weight: 800; margin: 0 0 16px 0; text-align: center;">
                                        Your Trial Ends in {days_left} Days
                                    </h2>
                                    
                                    <p style="color: #6b7280; font-size: 16px; line-height: 1.6; margin: 0 0 32px 0; text-align: center;">
                                        Don't lose access to your recipes, menus, and data!
                                    </p>
                                    
                                    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 12px; padding: 32px; margin: 0 0 32px 0; text-align: center;">
                                        <h3 style="color: white; font-size: 24px; font-weight: 800; margin: 0 0 12px 0;">
                                            🎁 Limited Time Offer
                                        </h3>
                                        <p style="color: white; font-size: 40px; font-weight: 900; margin: 0 0 12px 0;">
                                            20% OFF
                                        </p>
                                        <p style="color: rgba(255,255,255,0.9); font-size: 16px; margin: 0;">
                                            Subscribe before your trial ends
                                        </p>
                                    </div>
                                    
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td align="center" style="padding: 0 0 32px 0;">
                                                <a href="{self.app_url}" 
                                                   style="display: inline-block; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 18px 48px; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 18px; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);">
                                                    Claim 20% Discount →
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <h3 style="color: #1f2937; font-size: 18px; font-weight: 700; margin: 0 0 16px 0;">
                                        What you'll keep:
                                    </h3>
                                    <ul style="color: #6b7280; line-height: 1.8; margin: 0 0 24px 0;">
                                        <li>All your recipes and menus</li>
                                        <li>Cost analysis and insights</li>
                                        <li>Unlimited recipe scaling</li>
                                        <li>Priority support</li>
                                    </ul>
                                    
                                    <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 16px 20px; margin: 0 0 24px 0;">
                                        <p style="color: #991b1b; margin: 0; font-size: 15px;">
                                            <strong>⚠️ After {days_left} days:</strong> Your account will be downgraded and you'll lose access to premium features
                                        </p>
                                    </div>
                                    
                                    <p style="color: #6b7280; font-size: 15px; line-height: 1.6; margin: 0; text-align: center;">
                                        Questions? Reply to this email or contact us anytime.<br><br>
                                        <strong style="color: #1f2937;">The Iterum Team</strong>
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content, None, user_name)
    
    def send_trial_expired(self, user_name: str, user_email: str) -> bool:
        """Send trial expired notification"""
        subject = f"Your trial has ended - Keep your data with Iterum"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #f9fafb;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background: #f9fafb; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <tr>
                                <td>
                                    <h2 style="color: #1f2937; font-size: 28px; font-weight: 800; margin: 0 0 20px 0;">
                                        Hi {user_name},
                                    </h2>
                                    
                                    <p style="color: #6b7280; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0;">
                                        Your 14-day trial has ended. We hope you enjoyed exploring everything Iterum has to offer!
                                    </p>
                                    
                                    <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; margin: 0 0 32px 0;">
                                        <p style="color: #92400e; margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">
                                            📦 Your data is safe!
                                        </p>
                                        <p style="color: #92400e; margin: 0; font-size: 15px; line-height: 1.6;">
                                            All your recipes and menus are securely saved. Subscribe anytime to restore full access.
                                        </p>
                                    </div>
                                    
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td align="center" style="padding: 0 0 32px 0;">
                                                <a href="{self.app_url}" 
                                                   style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 18px 48px; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 18px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                                                    Subscribe Now →
                                                </a>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="color: #6b7280; font-size: 15px; line-height: 1.6; margin: 0 0 24px 0;">
                                        <strong style="color: #1f2937;">Not ready yet?</strong> No problem! Your data will be kept for 30 days. Come back anytime.
                                    </p>
                                    
                                    <div style="background: #f9fafb; border-radius: 10px; padding: 20px;">
                                        <p style="color: #6b7280; margin: 0; font-size: 14px; line-height: 1.6;">
                                            Have questions or feedback? We'd love to hear from you - just reply to this email!
                                        </p>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content, None, user_name)


# Global instance
email_service = EmailService()

