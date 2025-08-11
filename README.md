# 🚀 Heliopsis Email System - Complete Solution

Advanced email campaign management system with Twilio SendGrid integration, designed for users with no HTML knowledge.

## ✨ Features

### 🎯 **Core Capabilities**
- **Large List Handling**: Support for 100+ emails with automatic batching
- **Professional Templates**: No HTML knowledge required
- **Advanced Contact Management**: Categorization, import/export, search
- **Spam Prevention**: Professional headers and optimization
- **Campaign Tracking**: Detailed statistics and monitoring

### 🔧 **Technical Features**
- **Twilio SendGrid Integration**: Professional email delivery
- **SQLite Database**: Local contact storage
- **CSV Import/Export**: Easy data management
- **Template System**: Visual builder with variables
- **Batch Processing**: Efficient large-scale sending

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone the repository
git clone https://github.com/chichermo/heliopsisemails.git
cd heliopsisemails

# Install dependencies
pip install requests tqdm
```

### 2. **Configuration**
1. Copy the example configuration file:
   ```bash
   cp config_example.env config.env
   ```

2. Edit `config.env` with your actual credentials:
   - **API Key**: Get from [SendGrid Dashboard](https://app.sendgrid.com/settings/api_keys)
   - **Sender Email**: Must be verified in SendGrid
   - **Sender Name**: Your company or personal name

3. Verify your sender identity in SendGrid dashboard

### 3. **Run the System**
```bash
# Start the complete system
python complete_system.py

# Or run individual components
python sendgrid_definitivo.py      # Email sending
python email_list_manager.py       # Contact management
python template_manager.py         # Template system
```

## 📁 System Components

### 📧 **SendGrid Definitive** (`sendgrid_definitivo.py`)
- Professional email sending with Twilio SendGrid
- Large list handling (100+ emails)
- Professional headers for spam prevention
- Connection testing and account information

### 📋 **Email List Manager** (`email_list_manager.py`)
- Advanced contact database management
- Bulk import/export (CSV)
- Contact categorization and search
- Statistics and reporting

### 📄 **Template Manager** (`template_manager.py`)
- Simple template creation (no HTML required)
- Professional pre-built templates
- Variable placeholders
- Visual template builder

### 🎯 **Complete System** (`complete_system.py`)
- Integrated interface for all components
- Interactive menus
- Demo campaigns
- System testing and monitoring

## 💡 Usage Examples

### **Creating a Simple Template**
```python
from template_manager import TemplateManager

tm = TemplateManager()
template = tm.create_simple_text_template(
    title="Welcome!",
    message="Hello {{name}}, welcome to our service!",
    button_text="Get Started",
    button_url="#"
)
```

### **Managing Contacts**
```python
from email_list_manager import EmailListManager

em = EmailListManager()
# Add single contact
em.add_contact("user@example.com", "John Doe", "Company Inc")

# Bulk import from CSV
results = em.import_from_csv("contacts.csv")
```

### **Sending Campaigns**
```python
from sendgrid_definitivo import SendGridDefinitive

sender = SendGridDefinitive()
results = sender.send_bulk_emails(
    contacts,
    "Campaign Subject",
    template_content,
    "Sender Name",
    "heliopsis@outlook.be"
)
```

## 📊 Large List Handling

### **Automatic Batching**
- **Batch Size**: 100 emails per batch
- **Batch Delay**: 60 seconds between batches
- **Email Delay**: 6 seconds between individual emails
- **Rate Limit**: 10 emails per minute

### **Benefits**
- ✅ Prevents SendGrid rate limiting
- ✅ Maintains deliverability
- ✅ Professional sending patterns
- ✅ Automatic progress tracking

## 🎨 Template System

### **No HTML Knowledge Required**
- Visual template builder
- Professional pre-built designs
- Simple text-based creation
- Variable placeholders

### **Template Categories**
- **Newsletter**: Professional newsletters
- **Business**: Corporate communications
- **Promotional**: Marketing campaigns
- **Simple**: Basic messages

### **Variables Support**
- `{{name}}` - Contact name
- `{{company}}` - Company name
- `{{email}}` - Email address
- Custom variables supported

## 📈 Contact Management

### **Categories**
- Personal
- Business
- Corporate
- Educational
- Government
- Newsletter
- Marketing
- VIP

### **Import Options**
- CSV files (with/without headers)
- Plain text (one email per line)
- Automatic column detection
- Bulk validation

### **Export Options**
- CSV format
- Filtered by category
- Filtered by status
- Complete data export

## 🔒 Professional Headers

### **Anti-Spam Features**
- Professional email headers
- Company identification
- Campaign tracking
- Sender verification
- Content optimization

### **Headers Included**
- `X-Mailer`: Professional identification
- `X-Company`: Company branding
- `X-Campaign`: Campaign tracking
- `X-Sender-ID`: Sender identification

## 📊 System Requirements

### **Python**
- Python 3.7+
- pip package manager

### **Dependencies**
```
requests>=2.25.0
tqdm>=4.60.0
```

### **SendGrid Account**
- Verified sender identity
- API key access
- Sufficient sending limits

## 🚀 Getting Started

### **1. System Test**
```bash
python complete_system.py
# Select option 1: Test System Components
```

### **2. Create Demo Data**
```bash
# Select option 2: Create Demo Data
# This adds sample contacts and templates
```

### **3. Run Demo Campaign**
```bash
# Select option 3: Run Demo Campaign
# Tests the complete system
```

### **4. Manage Your Data**
```bash
# Select option 5: Manage Contacts
# Select option 6: Manage Templates
```

## 📋 File Structure

```
heliopsisemails/
├── README.md                    # This file
├── complete_system.py           # Main integrated system
├── sendgrid_definitivo.py      # SendGrid email sending
├── email_list_manager.py       # Contact management
├── template_manager.py          # Template system
├── config_definitiva.py        # Configuration
├── email_contacts.db           # SQLite database
├── email_templates.json        # Template storage
└── sendgrid_definitive.log     # System logs
```

## 🔧 Configuration

### **SendGrid Settings**
- **API Key**: Automatically configured
- **Sender**: `heliopsis@outlook.be`
- **Rate Limits**: Optimized for professional sending

### **Database Settings**
- **Type**: SQLite (local)
- **Location**: `email_contacts.db`
- **Backup**: Export to CSV recommended

### **Template Settings**
- **Storage**: JSON files
- **Location**: `email_templates.json`
- **Backup**: Export/import functionality

## 📊 Performance

### **Sending Capacity**
- **Small Lists**: <100 emails (direct sending)
- **Large Lists**: 100+ emails (batched sending)
- **Maximum**: Limited by SendGrid account limits

### **Processing Speed**
- **Email Rate**: 10 emails per minute
- **Batch Processing**: 100 emails per batch
- **Total Time**: Depends on list size

## 🛠️ Troubleshooting

### **Common Issues**

#### **SendGrid Connection Error**
- Verify API key is correct
- Check internet connection
- Verify sender identity is verified

#### **Template Rendering Issues**
- Check variable placeholders
- Verify template format
- Use simple text templates

#### **Contact Import Errors**
- Check CSV format
- Verify email validation
- Check file encoding

### **Support**
- Check system logs: `sendgrid_definitive.log`
- Run system test: `python complete_system.py` (option 1)
- Verify SendGrid dashboard

## 🔄 Updates and Maintenance

### **Regular Tasks**
- Monitor SendGrid sending limits
- Backup contact database
- Update templates as needed
- Check system logs

### **Backup Recommendations**
- Export contacts to CSV weekly
- Backup template files
- Monitor SendGrid account status

## 📄 License

This project is proprietary software developed for Heliopsis.

## 🤝 Support

For technical support or questions:
- Check the troubleshooting section
- Review system logs
- Verify SendGrid account status

---

**🎉 Welcome to Heliopsis Email System - Professional email campaigns made simple!** 