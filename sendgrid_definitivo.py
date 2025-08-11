#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DEFINITIVE EMAIL SENDING SYSTEM - TWILIO SENDGRID
================================================

Optimized system with the definitive Twilio SendGrid account:
- API Key: YOUR_SENDGRID_API_KEY
- Sender: heliopsis@outlook.be
- Professional headers to avoid spam
- Complete campaign management system
"""

import requests
import json
import time
import logging
from typing import List, Dict
from tqdm import tqdm
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sendgrid_definitive.log'),
        logging.StreamHandler()
    ]
)

class SendGridDefinitive:
    """Definitive email sending system using Twilio SendGrid"""
    
    def __init__(self, api_key=None):
        # Definitive Twilio SendGrid API Key
        self.api_key = api_key or "YOUR_SENDGRID_API_KEY"
        self.base_url = "https://api.sendgrid.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.sent_count = 0
        self.failed_count = 0
        
        # Definitive professional headers to avoid spam
        self.default_headers = {
            'X-Mailer': 'Twilio-SendGrid-Professional',
            'X-Priority': '3',
            'X-MSMail-Priority': 'Normal',
            'Importance': 'Normal',
            'X-Campaign': 'EmailCampaign',
            'X-Company': 'Heliopsis',
            'X-Contact-Info': 'heliopsis@outlook.be'
        }
        
        # Optimized sending configuration
        self.emails_per_minute = 10
        self.delay_between_emails = 6
        
        # Large list handling
        self.max_batch_size = 100
        self.batch_delay = 60  # seconds between batches
        
    def test_connection(self):
        """Test connection with Twilio SendGrid"""
        try:
            response = requests.get(f"{self.base_url}/user/profile", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                logging.info(f"SUCCESSFUL connection to Twilio SendGrid for {user_data.get('email', 'user')}")
                return True
            else:
                logging.error(f"CONNECTION ERROR to Twilio SendGrid: {response.status_code}")
                if response.text:
                    logging.error(f"Error details: {response.text}")
                return False
        except Exception as e:
            logging.error(f"CONNECTION ERROR to Twilio SendGrid: {str(e)}")
            return False
    
    def create_professional_headers(self, custom_headers=None):
        """Create definitive professional headers to avoid spam"""
        headers = self.default_headers.copy()
        
        # Add timestamp
        headers['X-Sent-Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Add custom headers if provided
        if custom_headers:
            headers.update(custom_headers)
            
        return headers
    
    def create_simple_template(self, title: str, message: str, button_text: str = None, button_url: str = None) -> str:
        """Create a simple HTML template without requiring HTML knowledge"""
        
        # Simple template structure
        template = f"""
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; font-family: Arial, sans-serif;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; margin: 0;">{title}</h1>
            </div>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; line-height: 1.6;">
                {message.replace(chr(10), '<br>')}
            </div>
        """
        
        # Add button if provided
        if button_text and button_url:
            template += f"""
            <div style="text-align: center; margin: 30px 0;">
                <a href="{button_url}" style="background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">{button_text}</a>
            </div>
            """
        
        # Footer
        template += """
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="text-align: center; color: #666; font-size: 12px;">
                Sent from Heliopsis Email System
            </p>
        </div>
        """
        
        return template
    
    def optimize_email_content(self, content: str, contact_data: Dict) -> str:
        """Optimize email content to avoid spam"""
        
        # Personalize content
        optimized_content = content
        
        # Replace placeholders
        for key, value in contact_data.items():
            placeholder = f"{{{{{key}}}}}"
            optimized_content = optimized_content.replace(placeholder, str(value))
        
        # If content is already HTML, return as is
        if content.strip().startswith('<!DOCTYPE html>') or content.strip().startswith('<html'):
            return optimized_content
        else:
            # Convert plain text to simple HTML
            return self.create_simple_template("Email", optimized_content)
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   sender_name: str = None, from_email: str = None, 
                   custom_headers: Dict = None) -> bool:
        """Send an email using Twilio SendGrid with optimized headers"""
        try:
            # Create professional headers
            email_headers = self.create_professional_headers(custom_headers)
            
            data = {
                "personalizations": [
                    {
                        "to": [{"email": to_email}],
                        "headers": email_headers
                    }
                ],
                "from": {
                    "email": from_email or "heliopsis@outlook.be",  # Verified email
                    "name": sender_name or "Heliopsis"
                },
                "subject": subject,
                "content": [
                    {
                        "type": "text/html",
                        "value": body
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/mail/send",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 202:
                self.sent_count += 1
                logging.info(f"EMAIL sent successfully to {to_email}")
                return True
            else:
                self.failed_count += 1
                logging.error(f"ERROR sending email to {to_email}: {response.status_code}")
                if response.text:
                    logging.error(f"Error details: {response.text}")
                return False
                
        except Exception as e:
            self.failed_count += 1
            logging.error(f"ERROR sending email to {to_email}: {str(e)}")
            return False
    
    def send_bulk_emails(self, emails: List[Dict], subject: str, 
                         template: str, sender_name: str = None, 
                         from_email: str = None, custom_headers: Dict = None) -> Dict:
        """Send emails in bulk with definitive optimizations and large list handling"""
        results = {'total': len(emails), 'sent': 0, 'failed': 0, 'errors': [], 'batches': 0}
        
        if not self.test_connection():
            logging.error("COULD NOT establish connection to Twilio SendGrid")
            return results
        
        logging.info(f"STARTING bulk send of {len(emails)} emails with definitive account")
        
        # Handle large lists in batches
        if len(emails) > self.max_batch_size:
            logging.info(f"Large list detected ({len(emails)} emails). Processing in batches of {self.max_batch_size}")
            
            # Split into batches
            batches = [emails[i:i + self.max_batch_size] for i in range(0, len(emails), self.max_batch_size)]
            
            for batch_num, batch in enumerate(batches, 1):
                logging.info(f"Processing batch {batch_num}/{len(batches)} ({len(batch)} emails)")
                results['batches'] += 1
                
                # Process batch
                batch_results = self._process_batch(batch, subject, template, sender_name, from_email, custom_headers)
                
                # Update results
                results['sent'] += batch_results['sent']
                results['failed'] += batch_results['failed']
                results['errors'].extend(batch_results['errors'])
                
                # Delay between batches (except for the last one)
                if batch_num < len(batches):
                    logging.info(f"Waiting {self.batch_delay} seconds before next batch...")
                    time.sleep(self.batch_delay)
        else:
            # Small list, process normally
            batch_results = self._process_batch(emails, subject, template, sender_name, from_email, custom_headers)
            results['sent'] = batch_results['sent']
            results['failed'] = batch_results['failed']
            results['errors'] = batch_results['errors']
        
        logging.info(f"BULK SEND completed: {results['sent']} sent, {results['failed']} failed")
        return results
    
    def _process_batch(self, emails: List[Dict], subject: str, template: str, 
                       sender_name: str, from_email: str, custom_headers: Dict) -> Dict:
        """Process a batch of emails"""
        batch_results = {'sent': 0, 'failed': 0, 'errors': []}
        
        with tqdm(total=len(emails), desc=f"Sending batch") as pbar:
            for email_data in emails:
                try:
                    # Optimize content
                    personalized_body = self.optimize_email_content(template, email_data)
                    
                    # Send email with optimized headers
                    if self.send_email(
                        email_data['email'], 
                        subject, 
                        personalized_body, 
                        sender_name, 
                        from_email,
                        custom_headers
                    ):
                        batch_results['sent'] += 1
                    else:
                        batch_results['failed'] += 1
                        batch_results['errors'].append(f"Error sending to {email_data['email']}")
                    
                    # Optimized delay between emails (6 seconds)
                    time.sleep(self.delay_between_emails)
                    pbar.update(1)
                    
                except Exception as e:
                    batch_results['failed'] += 1
                    batch_results['errors'].append(f"Error with {email_data['email']}: {str(e)}")
                    pbar.update(1)
        
        return batch_results
    
    def get_sending_stats(self) -> Dict:
        """Get sending statistics"""
        return {
            'sent': self.sent_count,
            'failed': self.failed_count,
            'total': self.sent_count + self.failed_count,
            'account': 'Twilio SendGrid - Definitive Account',
            'sender': 'heliopsis@outlook.be',
            'max_batch_size': self.max_batch_size,
            'batch_delay': self.batch_delay
        }
    
    def get_account_info(self) -> Dict:
        """Get Twilio SendGrid account information"""
        try:
            response = requests.get(f"{self.base_url}/user/profile", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                return {
                    'email': user_data.get('email', 'Not available'),
                    'first_name': user_data.get('first_name', 'Not available'),
                    'last_name': user_data.get('last_name', 'Not available'),
                    'website': user_data.get('website', 'Not available'),
                    'company': user_data.get('company', 'Not available'),
                    'address': user_data.get('address', 'Not available'),
                    'city': user_data.get('city', 'Not available'),
                    'country': user_data.get('country', 'Not available')
                }
            else:
                return {'error': f'Error getting information: {response.status_code}'}
        except Exception as e:
            return {'error': f'Connection error: {str(e)}'}

def main():
    """Main function to test the definitive system"""
    print("🚀 DEFINITIVE SYSTEM - TWILIO SENDGRID")
    print("=" * 50)
    print(f"📧 Sender: heliopsis@outlook.be")
    print(f"🔑 API Key: YOUR_SENDGRID_API_KEY")
    print(f"🏢 Company: Twilio SendGrid")
    print()
    
    sender = SendGridDefinitive()
    
    # Test connection
    print("1️⃣ Testing connection with definitive account...")
    if sender.test_connection():
        print("✅ Successful connection to Twilio SendGrid!")
        
        # Get account information
        print("\n2️⃣ Account information:")
        account_info = sender.get_account_info()
        if 'error' not in account_info:
            print(f"   📧 Email: {account_info['email']}")
            print(f"   👤 Name: {account_info['first_name']} {account_info['last_name']}")
            print(f"   🏢 Company: {account_info['company']}")
            print(f"   🌍 Country: {account_info['country']}")
        else:
            print(f"   ❌ Error: {account_info['error']}")
        
        # Custom headers to avoid spam
        print("\n3️⃣ Configuring professional headers...")
        custom_headers = {
            'X-Campaign-Type': 'Newsletter',
            'X-Company': 'Heliopsis',
            'X-Contact-Info': 'heliopsis@outlook.be',
            'X-Sender-ID': 'Heliopsis-System'
        }
        
        # Test email
        print("\n4️⃣ Preparing test email...")
        test_emails = [
            {'email': 'guillermoromerog@gmail.com', 'name': 'Heliopsis', 'company': 'Definitive Company'}
        ]
        
        # Simple template creation (no HTML knowledge required)
        test_template = sender.create_simple_template(
            title="Definitive System Working!",
            message="This is a test email from the definitive Twilio SendGrid system.\n\n✅ Definitive account configured\n✅ Professional headers for spam prevention\n✅ System optimized 100%\n✅ Sender: heliopsis@outlook.be",
            button_text="Learn More",
            button_url="#"
        )
        
        # Send test email
        print("\n5️⃣ Sending test email...")
        results = sender.send_bulk_emails(
            test_emails,
            "Definitive System - Twilio SendGrid Working",
            test_template,
            "Heliopsis",
            "heliopsis@outlook.be",  # Verified email
            custom_headers
        )
        
        print(f"\n📊 Sending results:")
        print(f"   • Total: {results['total']}")
        print(f"   • Sent: {results['sent']}")
        print(f"   • Failed: {results['failed']}")
        
        if results['sent'] > 0:
            print(f"\n🎉 Definitive system working perfectly!")
            print(f"✅ Twilio SendGrid account active")
            print(f"✅ Professional headers configured")
            print(f"✅ Sender: heliopsis@outlook.be")
            print(f"✅ System ready for production")
            print(f"✅ Large list handling: {sender.max_batch_size}+ emails")
        else:
            print(f"\n❌ Sending error")
            
        # Show final statistics
        print(f"\n📈 System statistics:")
        stats = sender.get_sending_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
            
    else:
        print("❌ Could not establish connection to Twilio SendGrid")
        print("Verify that the API Key is correct and the account is active")

if __name__ == "__main__":
    main()
