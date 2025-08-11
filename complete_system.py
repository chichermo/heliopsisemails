#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
COMPLETE EMAIL SYSTEM - INTEGRATED SOLUTION
==========================================

Complete email campaign management system with:
- SendGrid integration
- Advanced contact management
- Simple template system
- Large list handling (100+ emails)
- Professional headers
- No HTML knowledge required
"""

import time
from typing import List, Dict
from sendgrid_definitivo import SendGridDefinitive
from email_list_manager import EmailListManager
from template_manager import TemplateManager

class CompleteEmailSystem:
    """Complete integrated email system"""
    
    def __init__(self):
        self.sender = SendGridDefinitive()
        self.list_manager = EmailListManager()
        self.template_manager = TemplateManager()
        
    def test_system(self):
        """Test all system components"""
        print("🧪 TESTING COMPLETE EMAIL SYSTEM")
        print("=" * 50)
        
        # Test SendGrid connection
        print("\n1️⃣ Testing SendGrid connection...")
        if self.sender.test_connection():
            print("   ✅ SendGrid connection successful")
        else:
            print("   ❌ SendGrid connection failed")
            return False
        
        # Test database
        print("\n2️⃣ Testing database...")
        stats = self.list_manager.get_statistics()
        print(f"   ✅ Database ready - {stats.get('total_contacts', 0)} contacts")
        
        # Test templates
        print("\n3️⃣ Testing templates...")
        templates = self.template_manager.get_all_templates()
        print(f"   ✅ Templates ready - {len(templates)} available")
        
        print("\n✅ All system components working!")
        return True
    
    def create_demo_data(self):
        """Create demonstration data"""
        print("\n📊 CREATING DEMONSTRATION DATA")
        print("=" * 40)
        
        # Add demo contacts
        print("1️⃣ Adding demo contacts...")
        demo_contacts = [
            {'email': 'heliopsis@outlook.be', 'name': 'Heliopsis', 'company': 'Demo Company 1', 'phone': '123-456-7890', 'category': 'Business'},
            {'email': 'guillermoromerog@gmail.com', 'name': 'Guillermo Romero', 'company': 'Demo Company 2', 'phone': '098-765-4321', 'category': 'Personal'},
            {'email': 'v.luis.romero@tropicana.com', 'name': 'Luis Romero', 'company': 'Tropicana', 'phone': '555-123-4567', 'category': 'Corporate'}
        ]
        
        results = self.list_manager.add_contacts_bulk(demo_contacts)
        print(f"   ✅ {results['added']} contacts added, {results['updated']} updated")
        
        # Create demo template
        print("\n2️⃣ Creating demo template...")
        demo_template = self.template_manager.create_simple_text_template(
            title="Welcome to Heliopsis Email System!",
            message="Hello {{name}},\n\nWelcome to our advanced email system!\n\nCompany: {{company}}\nPhone: {{phone}}\n\nThis system supports:\n✅ Large lists (100+ emails)\n✅ Professional templates\n✅ No HTML knowledge required\n✅ Advanced contact management",
            button_text="Learn More",
            button_url="#"
        )
        
        self.template_manager.add_template(
            'demo_welcome',
            'Demo Welcome Template',
            'Demonstration template for the system',
            'General',
            ['name', 'company', 'phone'],
            demo_template
        )
        print("   ✅ Demo template created")
        
        print("\n✅ Demo data created successfully!")
    
    def run_demo_campaign(self):
        """Run a demonstration campaign"""
        print("\n🚀 RUNNING DEMONSTRATION CAMPAIGN")
        print("=" * 45)
        
        # Get contacts
        contacts = self.list_manager.get_contacts()
        if not contacts:
            print("❌ No contacts found. Create demo data first.")
            return
        
        print(f"1️⃣ Campaign setup:")
        print(f"   📧 Total contacts: {len(contacts)}")
        print(f"   📄 Template: Demo Welcome Template")
        print(f"   🎯 Subject: Welcome to Heliopsis Email System")
        
        # Get template
        template = self.template_manager.get_template('demo_welcome')
        if not template:
            print("❌ Demo template not found")
            return
        
        # Prepare campaign data
        campaign_contacts = []
        for contact in contacts:
            campaign_contacts.append({
                'email': contact['email'],
                'name': contact['name'] or 'Friend',
                'company': contact['company'] or 'Company',
                'phone': contact['phone'] or 'N/A'
            })
        
        # Send campaign
        print("\n2️⃣ Sending campaign...")
        results = self.sender.send_bulk_emails(
            campaign_contacts,
            "Welcome to Heliopsis Email System",
            template['content'],
            "Heliopsis",
            "heliopsis@outlook.be"
        )
        
        # Show results
        print(f"\n📊 Campaign results:")
        print(f"   • Total: {results['total']}")
        print(f"   • Sent: {results['sent']}")
        print(f"   • Failed: {results['failed']}")
        if results.get('batches', 0) > 0:
            print(f"   • Batches: {results['batches']}")
        
        if results['sent'] > 0:
            print(f"\n🎉 Campaign completed successfully!")
        else:
            print(f"\n❌ Campaign failed")
    
    def show_system_info(self):
        """Show comprehensive system information"""
        print("\n📋 SYSTEM INFORMATION")
        print("=" * 30)
        
        # SendGrid info
        print("\n1️⃣ SendGrid Account:")
        account_info = self.sender.get_account_info()
        if 'error' not in account_info:
            print(f"   👤 Name: {account_info['first_name']} {account_info['last_name']}")
            print(f"   🏢 Company: {account_info['company']}")
            print(f"   📧 Sender: heliopsis@outlook.be")
        else:
            print(f"   ❌ Error: {account_info['error']}")
        
        # Contact statistics
        print("\n2️⃣ Contact Database:")
        stats = self.list_manager.get_statistics()
        print(f"   📊 Total contacts: {stats.get('total_contacts', 0)}")
        print(f"   🏷️  Categories: {len(stats.get('by_category', {}))}")
        print(f"   📈 Recent additions: {stats.get('recent_week', 0)} (7 days)")
        
        # Template information
        print("\n3️⃣ Templates:")
        templates = self.template_manager.get_all_templates()
        categories = self.template_manager.get_template_categories()
        print(f"   📄 Total templates: {len(templates)}")
        print(f"   🏷️  Categories: {', '.join(categories)}")
        
        # System capabilities
        print("\n4️⃣ System Capabilities:")
        print(f"   ✅ Large list handling: 100+ emails")
        print(f"   ✅ Professional headers for spam prevention")
        print(f"   ✅ No HTML knowledge required")
        print(f"   ✅ Bulk import/export")
        print(f"   ✅ Advanced contact categorization")
        print(f"   ✅ Template management")
        print(f"   ✅ Campaign tracking")
    
    def interactive_menu(self):
        """Interactive menu for system management"""
        while True:
            print("\n" + "="*60)
            print("🎯 HELIOPSIS EMAIL SYSTEM - MAIN MENU")
            print("="*60)
            print("1️⃣ Test System Components")
            print("2️⃣ Create Demo Data")
            print("3️⃣ Run Demo Campaign")
            print("4️⃣ Show System Information")
            print("5️⃣ Manage Contacts")
            print("6️⃣ Manage Templates")
            print("7️⃣ Send Custom Campaign")
            print("8️⃣ Exit")
            print("="*60)
            
            choice = input("\nSelect an option (1-8): ").strip()
            
            if choice == '1':
                self.test_system()
            elif choice == '2':
                self.create_demo_data()
            elif choice == '3':
                self.run_demo_campaign()
            elif choice == '4':
                self.show_system_info()
            elif choice == '5':
                self.manage_contacts_menu()
            elif choice == '6':
                self.manage_templates_menu()
            elif choice == '7':
                self.custom_campaign_menu()
            elif choice == '8':
                print("\n👋 Thank you for using Heliopsis Email System!")
                break
            else:
                print("\n❌ Invalid option. Please try again.")
    
    def manage_contacts_menu(self):
        """Menu for contact management"""
        while True:
            print("\n" + "="*50)
            print("📧 CONTACT MANAGEMENT")
            print("="*50)
            print("1️⃣ View All Contacts")
            print("2️⃣ Add Single Contact")
            print("3️⃣ Import from CSV")
            print("4️⃣ Export to CSV")
            print("5️⃣ Search Contacts")
            print("6️⃣ Show Statistics")
            print("7️⃣ Back to Main Menu")
            print("="*50)
            
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == '1':
                contacts = self.list_manager.get_contacts(limit=20)
                print(f"\n📋 Recent contacts ({len(contacts)}):")
                for contact in contacts:
                    print(f"   📧 {contact['email']} - {contact['name'] or 'No name'} ({contact['category']})")
            
            elif choice == '2':
                email = input("Email: ").strip()
                name = input("Name (optional): ").strip()
                company = input("Company (optional): ").strip()
                category = input("Category (optional): ").strip()
                
                if self.list_manager.add_contact(email, name, company, category=category):
                    print("✅ Contact added successfully!")
                else:
                    print("❌ Error adding contact")
            
            elif choice == '3':
                file_path = input("CSV file path: ").strip()
                results = self.list_manager.import_from_csv(file_path)
                if 'error' not in results:
                    print(f"✅ Import completed: {results['added']} added, {results['updated']} updated")
                else:
                    print(f"❌ Import error: {results['error']}")
            
            elif choice == '4':
                file_path = input("Export file path: ").strip()
                if self.list_manager.export_to_csv(file_path):
                    print("✅ Export completed successfully!")
                else:
                    print("❌ Export failed")
            
            elif choice == '5':
                search_term = input("Search term: ").strip()
                results = self.list_manager.search_contacts(search_term)
                print(f"\n🔍 Search results ({len(results)}):")
                for contact in results:
                    print(f"   📧 {contact['email']} - {contact['name'] or 'No name'}")
            
            elif choice == '6':
                stats = self.list_manager.get_statistics()
                print(f"\n📊 Contact Statistics:")
                for key, value in stats.items():
                    if isinstance(value, dict):
                        print(f"   {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"      • {sub_key}: {sub_value}")
                    else:
                        print(f"   {key}: {value}")
            
            elif choice == '7':
                break
            
            else:
                print("\n❌ Invalid option. Please try again.")
    
    def manage_templates_menu(self):
        """Menu for template management"""
        while True:
            print("\n" + "="*50)
            print("📄 TEMPLATE MANAGEMENT")
            print("="*50)
            print("1️⃣ View All Templates")
            print("2️⃣ Create Simple Template")
            print("3️⃣ View Template Details")
            print("4️⃣ Export Template")
            print("5️⃣ Import Template")
            print("6️⃣ Back to Main Menu")
            print("="*50)
            
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == '1':
                templates = self.template_manager.get_all_templates()
                print(f"\n📋 Available templates ({len(templates)}):")
                for template in templates:
                    print(f"   📄 {template['name']} ({template['category']})")
                    print(f"      Description: {template['description']}")
                    print(f"      Variables: {', '.join(template['variables'])}")
                    print()
            
            elif choice == '2':
                title = input("Template title: ").strip()
                message = input("Message content: ").strip()
                button_text = input("Button text (optional): ").strip()
                button_url = input("Button URL (optional): ").strip()
                
                template_content = self.template_manager.create_simple_text_template(
                    title, message, button_text if button_text else None, button_url if button_url else None
                )
                
                template_id = title.lower().replace(' ', '_')
                if self.template_manager.add_template(template_id, title, f"Template: {title}", "Custom", [], template_content):
                    print("✅ Template created successfully!")
                else:
                    print("❌ Error creating template")
            
            elif choice == '3':
                template_id = input("Template ID: ").strip()
                template = self.template_manager.get_template(template_id)
                if template:
                    print(f"\n📄 Template: {template['name']}")
                    print(f"   Category: {template['category']}")
                    print(f"   Description: {template['description']}")
                    print(f"   Variables: {', '.join(template['variables'])}")
                    print(f"   Created: {template['created_date']}")
                else:
                    print("❌ Template not found")
            
            elif choice == '4':
                template_id = input("Template ID: ").strip()
                file_path = input("Export file path: ").strip()
                if self.template_manager.export_template(template_id, file_path):
                    print("✅ Template exported successfully!")
                else:
                    print("❌ Export failed")
            
            elif choice == '5':
                file_path = input("Import file path: ").strip()
                if self.template_manager.import_template(file_path):
                    print("✅ Template imported successfully!")
                else:
                    print("❌ Import failed")
            
            elif choice == '6':
                break
            
            else:
                print("\n❌ Invalid option. Please try again.")
    
    def custom_campaign_menu(self):
        """Menu for custom campaign creation"""
        print("\n" + "="*50)
        print("🚀 CUSTOM CAMPAIGN CREATION")
        print("="*50)
        
        # Get contacts
        contacts = self.list_manager.get_contacts()
        if not contacts:
            print("❌ No contacts found. Add contacts first.")
            return
        
        print(f"📧 Available contacts: {len(contacts)}")
        
        # Get template
        template_id = input("Template ID: ").strip()
        template = self.template_manager.get_template(template_id)
        if not template:
            print("❌ Template not found")
            return
        
        # Campaign details
        subject = input("Email subject: ").strip()
        if not subject:
            subject = "Campaign from Heliopsis"
        
        print(f"\n📋 Campaign Summary:")
        print(f"   📧 Contacts: {len(contacts)}")
        print(f"   📄 Template: {template['name']}")
        print(f"   🎯 Subject: {subject}")
        print(f"   📤 Sender: heliopsis@outlook.be")
        
        confirm = input("\nProceed with campaign? (y/n): ").strip().lower()
        if confirm == 'y':
            # Prepare campaign data
            campaign_contacts = []
            for contact in contacts:
                campaign_contacts.append({
                    'email': contact['email'],
                    'name': contact['name'] or 'Friend',
                    'company': contact['company'] or 'Company',
                    'phone': contact['phone'] or 'N/A'
                })
            
            # Send campaign
            print("\n🚀 Sending campaign...")
            results = self.sender.send_bulk_emails(
                campaign_contacts,
                subject,
                template['content'],
                "Heliopsis",
                "heliopsis@outlook.be"
            )
            
            # Show results
            print(f"\n📊 Campaign results:")
            print(f"   • Total: {results['total']}")
            print(f"   • Sent: {results['sent']}")
            print(f"   • Failed: {results['failed']}")
            if results.get('batches', 0) > 0:
                print(f"   • Batches: {results['batches']}")
            
            if results['sent'] > 0:
                print(f"\n🎉 Campaign completed successfully!")
            else:
                print(f"\n❌ Campaign failed")
        else:
            print("❌ Campaign cancelled")

def main():
    """Main function"""
    print("🚀 HELIOPSIS EMAIL SYSTEM - COMPLETE SOLUTION")
    print("=" * 60)
    print("Advanced email campaign management with Twilio SendGrid")
    print("✅ Large list handling (100+ emails)")
    print("✅ Professional templates (no HTML required)")
    print("✅ Advanced contact management")
    print("✅ Professional headers for spam prevention")
    print("=" * 60)
    
    system = CompleteEmailSystem()
    
    # Test system first
    if system.test_system():
        print("\n✅ System ready! Starting interactive menu...")
        time.sleep(2)
        system.interactive_menu()
    else:
        print("\n❌ System test failed. Please check configuration.")

if __name__ == "__main__":
    main()
