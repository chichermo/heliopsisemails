#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TEMPLATE MANAGER - SIMPLE EMAIL TEMPLATE SYSTEM
==============================================

Simple email template management system with:
- No HTML knowledge required
- Visual template builder
- Variable placeholders
- Professional designs
- Easy customization
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime

class TemplateManager:
    """Simple email template management system"""
    
    def __init__(self, templates_file: str = "email_templates.json"):
        self.templates_file = templates_file
        self.templates = self.load_templates()
        self.init_default_templates()
    
    def load_templates(self) -> Dict:
        """Load templates from JSON file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error loading templates: {str(e)}")
            return {}
    
    def save_templates(self):
        """Save templates to JSON file"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving templates: {str(e)}")
            return False
    
    def init_default_templates(self):
        """Initialize with professional default templates"""
        if not self.templates:
            self.templates = {
                'newsletter': {
                    'name': 'Newsletter Template',
                    'description': 'Professional newsletter template with header, content, and footer',
                    'category': 'Newsletter',
                    'variables': ['company_name', 'newsletter_title', 'main_content', 'call_to_action', 'unsubscribe_link'],
                    'content': self.create_newsletter_template(),
                    'created_date': datetime.now().isoformat(),
                    'last_modified': datetime.now().isoformat()
                },
                'business': {
                    'name': 'Business Communication',
                    'description': 'Professional business email template',
                    'category': 'Business',
                    'variables': ['recipient_name', 'company_name', 'message_content', 'contact_info'],
                    'content': self.create_business_template(),
                    'created_date': datetime.now().isoformat(),
                    'last_modified': datetime.now().isoformat()
                },
                'promotional': {
                    'name': 'Promotional Email',
                    'description': 'Marketing and promotional email template',
                    'category': 'Marketing',
                    'variables': ['recipient_name', 'offer_title', 'offer_description', 'cta_button', 'expiry_date'],
                    'content': self.create_promotional_template(),
                    'created_date': datetime.now().isoformat(),
                    'last_modified': datetime.now().isoformat()
                },
                'simple': {
                    'name': 'Simple Message',
                    'description': 'Clean and simple email template',
                    'category': 'General',
                    'variables': ['recipient_name', 'message_content'],
                    'content': self.create_simple_template(),
                    'created_date': datetime.now().isoformat(),
                    'last_modified': datetime.now().isoformat()
                }
            }
            self.save_templates()
    
    def create_newsletter_template(self) -> str:
        """Create a professional newsletter template"""
        return {
            'title': 'Newsletter Title',
            'header_color': '#2c3e50',
            'content_background': '#ffffff',
            'accent_color': '#3498db',
            'sections': [
                {
                    'type': 'header',
                    'content': 'Welcome to our Newsletter!',
                    'style': 'large_title'
                },
                {
                    'type': 'text',
                    'content': 'This is the main content of your newsletter. You can write multiple paragraphs here.',
                    'style': 'body_text'
                },
                {
                    'type': 'button',
                    'content': 'Read More',
                    'url': '#',
                    'style': 'primary_button'
                },
                {
                    'type': 'divider',
                    'style': 'thin_line'
                },
                {
                    'type': 'footer',
                    'content': '© 2025 Company Name. All rights reserved.',
                    'style': 'small_text'
                }
            ]
        }
    
    def create_business_template(self) -> str:
        """Create a professional business template"""
        return {
            'title': 'Business Communication',
            'header_color': '#34495e',
            'content_background': '#f8f9fa',
            'accent_color': '#2c3e50',
            'sections': [
                {
                    'type': 'header',
                    'content': 'Business Communication',
                    'style': 'business_title'
                },
                {
                    'type': 'text',
                    'content': 'Dear {{recipient_name}},\n\nThis is a professional business communication.',
                    'style': 'formal_text'
                },
                {
                    'type': 'text',
                    'content': 'Best regards,\n{{company_name}}',
                    'style': 'signature'
                }
            ]
        }
    
    def create_promotional_template(self) -> str:
        """Create a promotional template"""
        return {
            'title': 'Special Offer',
            'header_color': '#e74c3c',
            'content_background': '#fff5f5',
            'accent_color': '#c0392b',
            'sections': [
                {
                    'type': 'header',
                    'content': '🎉 Special Offer Just for You!',
                    'style': 'promotional_title'
                },
                {
                    'type': 'text',
                    'content': 'Hi {{recipient_name}},\n\nWe have an amazing offer that you won\'t want to miss!',
                    'style': 'excited_text'
                },
                {
                    'type': 'button',
                    'content': 'Claim Offer Now',
                    'url': '#',
                    'style': 'urgent_button'
                },
                {
                    'type': 'text',
                    'content': 'Offer expires: {{expiry_date}}',
                    'style': 'urgent_text'
                }
            ]
        }
    
    def create_simple_template(self) -> str:
        """Create a simple template"""
        return {
            'title': 'Simple Message',
            'header_color': '#7f8c8d',
            'content_background': '#ffffff',
            'accent_color': '#95a5a6',
            'sections': [
                {
                    'type': 'header',
                    'content': 'Simple Message',
                    'style': 'simple_title'
                },
                {
                    'type': 'text',
                    'content': 'Hello {{recipient_name}},\n\n{{message_content}}',
                    'style': 'simple_text'
                }
            ]
        }
    
    def create_template_from_builder(self, template_data: Dict) -> str:
        """Create HTML template from builder data"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{template_data.get('title', 'Email Template')}</title>
            <style>
                body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: {template_data.get('content_background', '#ffffff')}; }}
                .header {{ background-color: {template_data.get('header_color', '#2c3e50')}; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: {template_data.get('accent_color', '#3498db')}; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                .divider {{ border-top: 1px solid #eee; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
        """
        
        for section in template_data.get('sections', []):
            section_type = section.get('type', 'text')
            content = section.get('content', '')
            style = section.get('style', '')
            
            if section_type == 'header':
                html += f'<div class="header"><h1>{content}</h1></div>'
            elif section_type == 'text':
                html += f'<div class="content"><p>{content.replace(chr(10), "<br>")}</p></div>'
            elif section_type == 'button':
                url = section.get('url', '#')
                html += f'<div class="content" style="text-align: center;"><a href="{url}" class="button">{content}</a></div>'
            elif section_type == 'divider':
                html += '<div class="divider"></div>'
            elif section_type == 'footer':
                html += f'<div class="footer">{content}</div>'
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
    
    def create_simple_text_template(self, title: str, message: str, button_text: str = None, button_url: str = None) -> str:
        """Create a simple text-based template (no HTML knowledge required)"""
        template_data = {
            'title': title,
            'header_color': '#2c3e50',
            'content_background': '#ffffff',
            'accent_color': '#3498db',
            'sections': [
                {
                    'type': 'header',
                    'content': title,
                    'style': 'large_title'
                },
                {
                    'type': 'text',
                    'content': message,
                    'style': 'body_text'
                }
            ]
        }
        
        if button_text and button_url:
            template_data['sections'].append({
                'type': 'button',
                'content': button_text,
                'url': button_url,
                'style': 'primary_button'
            })
        
        template_data['sections'].append({
            'type': 'footer',
            'content': 'Sent from Heliopsis Email System',
            'style': 'small_text'
        })
        
        return self.create_template_from_builder(template_data)
    
    def add_template(self, template_id: str, name: str, description: str, category: str, 
                    variables: List[str], content: str) -> bool:
        """Add a new template"""
        try:
            self.templates[template_id] = {
                'name': name,
                'description': description,
                'category': category,
                'variables': variables,
                'content': content,
                'created_date': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat()
            }
            return self.save_templates()
        except Exception as e:
            print(f"Error adding template: {str(e)}")
            return False
    
    def update_template(self, template_id: str, updates: Dict) -> bool:
        """Update an existing template"""
        try:
            if template_id in self.templates:
                for key, value in updates.items():
                    if key in ['name', 'description', 'category', 'variables', 'content']:
                        self.templates[template_id][key] = value
                
                self.templates[template_id]['last_modified'] = datetime.now().isoformat()
                return self.save_templates()
            return False
        except Exception as e:
            print(f"Error updating template: {str(e)}")
            return False
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template"""
        try:
            if template_id in self.templates:
                del self.templates[template_id]
                return self.save_templates()
            return False
        except Exception as e:
            print(f"Error deleting template: {str(e)}")
            return False
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get a specific template"""
        return self.templates.get(template_id)
    
    def get_templates_by_category(self, category: str) -> List[Dict]:
        """Get all templates in a specific category"""
        return [template for template in self.templates.values() if template.get('category') == category]
    
    def get_all_templates(self) -> List[Dict]:
        """Get all templates"""
        return list(self.templates.values())
    
    def get_template_categories(self) -> List[str]:
        """Get all available template categories"""
        categories = set()
        for template in self.templates.values():
            if 'category' in template:
                categories.add(template['category'])
        return sorted(list(categories))
    
    def render_template(self, template_id: str, variables: Dict) -> str:
        """Render a template with variables"""
        template = self.get_template(template_id)
        if not template:
            return "Template not found"
        
        content = template.get('content', '')
        
        # Replace variables in content
        if isinstance(content, str):
            for var_name, var_value in variables.items():
                placeholder = f"{{{{{var_name}}}}}"
                content = content.replace(placeholder, str(var_value))
        
        return content
    
    def export_template(self, template_id: str, file_path: str) -> bool:
        """Export a template to a file"""
        try:
            template = self.get_template(template_id)
            if not template:
                return False
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting template: {str(e)}")
            return False
    
    def import_template(self, file_path: str) -> bool:
        """Import a template from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            template_id = template_data.get('name', '').lower().replace(' ', '_')
            if template_id:
                return self.add_template(
                    template_id,
                    template_data.get('name', 'Imported Template'),
                    template_data.get('description', ''),
                    template_data.get('category', 'General'),
                    template_data.get('variables', []),
                    template_data.get('content', '')
                )
            return False
        except Exception as e:
            print(f"Error importing template: {str(e)}")
            return False

def main():
    """Main function to demonstrate the template manager"""
    print("📧 TEMPLATE MANAGER - SIMPLE SYSTEM")
    print("=" * 50)
    
    manager = TemplateManager()
    
    # Show available templates
    print("\n1️⃣ Available templates:")
    templates = manager.get_all_templates()
    for template_id, template in manager.templates.items():
        print(f"   📄 {template['name']} ({template['category']})")
        print(f"      Description: {template['description']}")
        print(f"      Variables: {', '.join(template['variables'])}")
        print()
    
    # Show categories
    print("\n2️⃣ Template categories:")
    categories = manager.get_template_categories()
    for category in categories:
        print(f"   🏷️  {category}")
    
    # Create a simple template
    print("\n3️⃣ Creating a simple template...")
    simple_template = manager.create_simple_text_template(
        title="Welcome to Our Service!",
        message="Hello {{recipient_name}},\n\nThank you for joining our service. We're excited to have you on board!\n\nBest regards,\n{{company_name}}",
        button_text="Get Started",
        button_url="#"
    )
    
    # Add the template
    manager.add_template(
        'welcome',
        'Welcome Template',
        'Simple welcome email template',
        'General',
        ['recipient_name', 'company_name'],
        simple_template
    )
    
    print("   ✅ Simple template created and added!")
    
    # Show final template count
    print(f"\n📊 Total templates: {len(manager.templates)}")
    print(f"✅ Template Manager ready!")
    print(f"💡 No HTML knowledge required!")
    print(f"🎨 Professional designs included")

if __name__ == "__main__":
    main()
