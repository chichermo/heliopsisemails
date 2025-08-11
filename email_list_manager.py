#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EMAIL LIST MANAGER - ADVANCED CONTACT MANAGEMENT
==============================================

Advanced email list management system with:
- Large list handling (100+ emails)
- Bulk import/export
- Contact categorization
- Email validation
- Simple UX for non-technical users
"""

import sqlite3
import csv
import json
import re
from typing import List, Dict, Optional
from datetime import datetime
import os

class EmailListManager:
    """Advanced email list management system"""
    
    def __init__(self, db_path: str = "email_contacts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with proper structure"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create contacts table with enhanced structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                company TEXT,
                phone TEXT,
                category TEXT DEFAULT 'General',
                status TEXT DEFAULT 'Active',
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                tags TEXT
            )
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#3498db'
            )
        ''')
        
        # Create campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT,
                template TEXT,
                status TEXT DEFAULT 'Draft',
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                sent_date TEXT,
                total_contacts INTEGER DEFAULT 0,
                sent_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0
            )
        ''')
        
        # Insert default categories
        default_categories = [
            ('Personal', 'Personal contacts and friends', '#e74c3c'),
            ('Business', 'Business and professional contacts', '#3498db'),
            ('Corporate', 'Corporate and enterprise contacts', '#2c3e50'),
            ('Educational', 'Educational institutions and students', '#9b59b6'),
            ('Government', 'Government and public sector', '#f39c12'),
            ('Newsletter', 'Newsletter subscribers', '#1abc9c'),
            ('Marketing', 'Marketing and promotional contacts', '#e67e22'),
            ('VIP', 'VIP and priority contacts', '#e91e63')
        ]
        
        for category in default_categories:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO categories (name, description, color)
                    VALUES (?, ?, ?)
                ''', category)
            except:
                pass
        
        conn.commit()
        conn.close()
    
    def add_contact(self, email: str, name: str = None, company: str = None, 
                    phone: str = None, category: str = 'General', notes: str = None) -> bool:
        """Add a single contact to the database"""
        try:
            if not self.validate_email(email):
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO contacts 
                (email, name, company, phone, category, notes, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (email, name, company, phone, category, notes))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding contact: {str(e)}")
            return False
    
    def add_contacts_bulk(self, contacts: List[Dict]) -> Dict:
        """Add multiple contacts in bulk with validation"""
        results = {
            'total': len(contacts),
            'added': 0,
            'updated': 0,
            'failed': 0,
            'errors': []
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for contact in contacts:
            try:
                email = contact.get('email', '').strip()
                if not email or not self.validate_email(email):
                    results['failed'] += 1
                    results['errors'].append(f"Invalid email: {email}")
                    continue
                
                # Check if contact exists
                cursor.execute('SELECT id FROM contacts WHERE email = ?', (email,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing contact
                    cursor.execute('''
                        UPDATE contacts 
                        SET name = COALESCE(?, name), 
                            company = COALESCE(?, company),
                            phone = COALESCE(?, phone),
                            category = COALESCE(?, category),
                            notes = COALESCE(?, notes),
                            last_updated = CURRENT_TIMESTAMP
                        WHERE email = ?
                    ''', (
                        contact.get('name'), 
                        contact.get('company'), 
                        contact.get('phone'),
                        contact.get('category', 'General'),
                        contact.get('notes'),
                        email
                    ))
                    results['updated'] += 1
                else:
                    # Add new contact
                    cursor.execute('''
                        INSERT INTO contacts 
                        (email, name, company, phone, category, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        email,
                        contact.get('name'),
                        contact.get('company'),
                        contact.get('phone'),
                        contact.get('category', 'General'),
                        contact.get('notes')
                    ))
                    results['added'] += 1
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error with {contact.get('email', 'unknown')}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return results
    
    def import_from_csv(self, csv_file_path: str, has_headers: bool = True) -> Dict:
        """Import contacts from CSV file with automatic column detection"""
        try:
            if not os.path.exists(csv_file_path):
                return {'error': 'CSV file not found'}
            
            contacts = []
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                if has_headers:
                    headers = next(reader)
                    # Auto-detect column mapping
                    column_map = {}
                    for i, header in enumerate(headers):
                        header_lower = header.lower()
                        if 'email' in header_lower:
                            column_map['email'] = i
                        elif 'name' in header_lower or 'nombre' in header_lower:
                            column_map['name'] = i
                        elif 'company' in header_lower or 'empresa' in header_lower:
                            column_map['company'] = i
                        elif 'phone' in header_lower or 'telefono' in header_lower:
                            column_map['phone'] = i
                        elif 'category' in header_lower or 'categoria' in header_lower:
                            column_map['category'] = i
                        elif 'notes' in header_lower or 'notas' in header_lower:
                            column_map['notes'] = i
                    
                    # Ensure email column is found
                    if 'email' not in column_map:
                        return {'error': 'Email column not found in CSV'}
                    
                    # Process rows
                    for row in reader:
                        if len(row) > max(column_map.values()):
                            contact = {}
                            for field, col_index in column_map.items():
                                contact[field] = row[col_index] if col_index < len(row) else ''
                            contacts.append(contact)
                else:
                    # No headers, assume first column is email
                    for row in reader:
                        if row and self.validate_email(row[0]):
                            contacts.append({'email': row[0]})
            
            # Add contacts in bulk
            return self.add_contacts_bulk(contacts)
            
        except Exception as e:
            return {'error': f'Import error: {str(e)}'}
    
    def import_from_text(self, text_content: str) -> Dict:
        """Import emails from plain text (one per line)"""
        try:
            emails = []
            lines = text_content.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if line and self.validate_email(line):
                    emails.append({'email': line})
            
            return self.add_contacts_bulk(emails)
            
        except Exception as e:
            return {'error': f'Text import error: {str(e)}'}
    
    def export_to_csv(self, file_path: str, category: str = None, status: str = None) -> bool:
        """Export contacts to CSV file with optional filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query with filters
            query = "SELECT email, name, company, phone, category, status, notes, created_date FROM contacts"
            params = []
            
            if category or status:
                query += " WHERE"
                if category:
                    query += " category = ?"
                    params.append(category)
                if status:
                    if category:
                        query += " AND"
                    query += " status = ?"
                    params.append(status)
            
            cursor.execute(query, params)
            contacts = cursor.fetchall()
            conn.close()
            
            # Write to CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Email', 'Name', 'Company', 'Phone', 'Category', 'Status', 'Notes', 'Created Date'])
                writer.writerows(contacts)
            
            return True
            
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False
    
    def get_contacts(self, category: str = None, status: str = None, limit: int = None) -> List[Dict]:
        """Get contacts with optional filtering and pagination"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM contacts"
            params = []
            
            if category or status:
                query += " WHERE"
                if category:
                    query += " category = ?"
                    params.append(category)
                if status:
                    if category:
                        query += " AND"
                    query += " status = ?"
                    params.append(status)
            
            query += " ORDER BY created_date DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            contacts = []
            for row in rows:
                contact = {
                    'id': row[0],
                    'email': row[1],
                    'name': row[2],
                    'company': row[3],
                    'phone': row[4],
                    'category': row[5],
                    'status': row[6],
                    'created_date': row[7],
                    'last_updated': row[8],
                    'notes': row[9],
                    'tags': row[10]
                }
                contacts.append(contact)
            
            return contacts
            
        except Exception as e:
            print(f"Error getting contacts: {str(e)}")
            return []
    
    def get_contact_count(self, category: str = None, status: str = None) -> int:
        """Get total count of contacts with optional filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT COUNT(*) FROM contacts"
            params = []
            
            if category or status:
                query += " WHERE"
                if category:
                    query += " category = ?"
                    params.append(category)
                if status:
                    if category:
                        query += " AND"
                    query += " status = ?"
                    params.append(status)
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
            
        except Exception as e:
            print(f"Error getting contact count: {str(e)}")
            return 0
    
    def get_categories(self) -> List[Dict]:
        """Get all available categories"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM categories ORDER BY name')
            rows = cursor.fetchall()
            conn.close()
            
            categories = []
            for row in rows:
                category = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'color': row[3]
                }
                categories.append(category)
            
            return categories
            
        except Exception as e:
            print(f"Error getting categories: {str(e)}")
            return []
    
    def update_contact(self, email: str, updates: Dict) -> bool:
        """Update contact information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build update query dynamically
            fields = []
            values = []
            for field, value in updates.items():
                if field in ['name', 'company', 'phone', 'category', 'status', 'notes', 'tags']:
                    fields.append(f"{field} = ?")
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(datetime.now().isoformat())
            values.append(email)
            
            query = f"UPDATE contacts SET {', '.join(fields)}, last_updated = ? WHERE email = ?"
            cursor.execute(query, values)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error updating contact: {str(e)}")
            return False
    
    def delete_contact(self, email: str) -> bool:
        """Delete a contact from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM contacts WHERE email = ?', (email,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error deleting contact: {str(e)}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        
        # Basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def search_contacts(self, search_term: str, limit: int = 50) -> List[Dict]:
        """Search contacts by email, name, or company"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT * FROM contacts 
                WHERE email LIKE ? OR name LIKE ? OR company LIKE ?
                ORDER BY created_date DESC
                LIMIT ?
            ''', (search_pattern, search_pattern, search_pattern, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            contacts = []
            for row in rows:
                contact = {
                    'id': row[0],
                    'email': row[1],
                    'name': row[2],
                    'company': row[3],
                    'phone': row[4],
                    'category': row[5],
                    'status': row[6],
                    'created_date': row[7],
                    'last_updated': row[8],
                    'notes': row[9],
                    'tags': row[10]
                }
                contacts.append(contact)
            
            return contacts
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about the contact database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Total contacts
            cursor.execute('SELECT COUNT(*) FROM contacts')
            stats['total_contacts'] = cursor.fetchone()[0]
            
            # Contacts by category
            cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM contacts 
                GROUP BY category 
                ORDER BY count DESC
            ''')
            stats['by_category'] = dict(cursor.fetchall())
            
            # Contacts by status
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM contacts 
                GROUP BY status 
                ORDER BY count DESC
            ''')
            stats['by_status'] = dict(cursor.fetchall())
            
            # Recent additions
            cursor.execute('''
                SELECT COUNT(*) FROM contacts 
                WHERE created_date >= date('now', '-7 days')
            ''')
            stats['recent_week'] = cursor.fetchone()[0]
            
            # Valid emails
            cursor.execute('''
                SELECT COUNT(*) FROM contacts 
                WHERE email LIKE '%@%'
            ''')
            stats['valid_emails'] = cursor.fetchone()[0]
            
            conn.close()
            return stats
            
        except Exception as e:
            print(f"Error getting statistics: {str(e)}")
            return {}

def main():
    """Main function to demonstrate the email list manager"""
    print("📧 EMAIL LIST MANAGER - ADVANCED SYSTEM")
    print("=" * 50)
    
    manager = EmailListManager()
    
    # Show statistics
    print("\n1️⃣ Current database statistics:")
    stats = manager.get_statistics()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   📊 {key}:")
            for sub_key, sub_value in value.items():
                print(f"      • {sub_key}: {sub_value}")
        else:
            print(f"   📊 {key}: {value}")
    
    # Show categories
    print("\n2️⃣ Available categories:")
    categories = manager.get_categories()
    for category in categories:
        print(f"   🏷️  {category['name']}: {category['description']}")
    
    # Show recent contacts
    print("\n3️⃣ Recent contacts:")
    contacts = manager.get_contacts(limit=5)
    if contacts:
        for contact in contacts:
            print(f"   📧 {contact['email']} - {contact['name'] or 'No name'} ({contact['category']})")
    else:
        print("   📭 No contacts found")
    
    print(f"\n✅ Email List Manager ready!")
    print(f"💡 Use the methods to manage your contact lists")
    print(f"📈 Large list handling: 100+ emails supported")
    print(f"🔄 Bulk import/export available")

if __name__ == "__main__":
    main()
