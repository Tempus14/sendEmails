# Sending personalized mails in batch

This system sends **infinitely customizable** personalized emails based on CSV data with a **one-file configuration** approach.

## Key Features

- ✅ **CSV-based recipient management**: Load recipient data from CSV files  
- ✅ **Test mode**: Preview emails without sending
- ✅ **Personalized content**: Names, personal notes, dynamic greetings
- ✅ **HTML & Plain text**: Dual-format emails for maximum compatibility
- ✅ **One-File Configuration**: Add unlimited conditions by editing only `email_config.py`
- ✅ **Unlimited conditional content**: Workshop participants, VIP members, new users, etc.
- ✅ **Multiple conditions per recipient**: Recipients can match several conditions simultaneously
- ✅ **UTF-8 support**: International character support
- ✅ **Auto-detection**: System automatically finds and applies all matching conditions
- ✅ **Error handling**: Graceful handling of missing columns and data issues

## Quick Setup & First Run

### 1. Install Dependencies
```bash
conda run pip install pandas beautifulsoup4 python-dotenv
```

### 2. Configure Email Credentials
Copy `credentials.env_template` to `credentials.env` and fill in your email settings:
```env
SenderMail=your-email@example.com
SenderPassword=your-password
SenderServer=smtp.gmail.com
SenderPort=465
```
**⚠️ SECURITY WARNING: Never commit `credentials.env` to version control or upload it to shared cloud storage! This file contains your unencrypted email password.**

### 3. Prepare Your CSV File
Your CSV file needs at minimum these columns:
- `Name`: Recipient's name (required)
- `Mail`: Email address (required)  
- Any additional columns for conditions (e.g., `Technic`, `Workshop`, `VIP`, `PersonalNote`)

**Minimum example:**
```csv
"Name", "Mail"
"John Doe", "john@example.com"
"Jane Smith", "jane@example.com"
```

### 4. Try It Out (Safe Preview Mode)
```bash
python main.py
```
This shows you what emails would be sent **without actually sending them**. Perfect for testing!

### 5. Send Real Emails (When Ready)
```bash
python main.py --send
```
This will ask for confirmation before sending.

## 📁 File Structure

```
sendEmails/
├── main.py                        # Main script for sending emails
├── newPage.py                     # Email content generation class  
├── email_config.py                # CONFIGURATION FILE - Edit this to add conditions
├── exampleRecipient.csv           # Sample data with multiple conditions
├── credentials.env_template       # Template for email credentials
├── credentials.env                # Your email server credentials (not in repo)
└── README.md                      # This file
```

**IMPORTANT SECURITY NOTE:** 
- `credentials.env` contains your unencrypted email password
- **NEVER** commit it to version control (git)
- **NEVER** upload it to shared cloud storage (Dropbox, Google Drive, etc.)
- **NEVER** share it in chat/email/messaging apps
- Keep it local to your machine only!

## How It Works - Basic Example

The system uses CSV files to manage recipients and applies conditions based on their data.

**Sample CSV (`exampleRecipient.csv`):**
```csv
"Name", "Mail", "Technic", "Workshop", "VIP", "PersonalNote"
"Frodo", "frodo@shire.hobbit", "FALSE", "TRUE", "TRUE", "Welcome to the adventure!"
"Legolas", "legolas@mirkwood.elf", "TRUE", "FALSE", "TRUE", "Great archery skills!"
```

**What happens:**
- Frodo gets: Base email + Workshop content + VIP content + Personal note
- Legolas gets: Base email + Technical content + VIP content + Personal note

The system automatically detects all matching conditions and builds personalized emails!

## What You'll See When Running

### Preview Mode (Default - Safe!)
```bash
python main.py
```
- Shows you exactly what each email will look like
- Lists all recipients and their conditions
- **No emails are sent** - perfect for testing!

### Send Mode (When You're Ready)
```bash
python main.py --send
```
- Shows the same preview
- Asks for confirmation before sending
- Only then sends the actual emails

## Advanced Customization

### Quick Example - Adding New Conditions

**Want to add a birthday greeting with flexible data? Just edit `email_config.py`:**

```python
{
    'name': 'birthday_greeting',
    'column': 'Birthday',
    'trigger_values': ['TRUE', 'Today', 'This Month'], 
    'content': '''
        <p><strong>Happy Birthday, {Nickname|{Name}}!</strong></p>
        <p>Wishing you a wonderful {Age|new} year ahead!</p>
    ''',
    'description': 'Birthday greeting with nickname fallback and age',
    'is_template': True
}
```

**Templates can use ANY recipient data with fallbacks: `{Nickname|{Name}}` uses nickname if available, otherwise name!**

## Adding New Conditions - Step by Step

### Step 1: Add to `email_config.py`
```python
CONDITIONAL_CONTENT = [
    # ... existing conditions ...
    
    {
        'name': 'birthday_greeting',
        'column': 'Birthday', 
        'trigger_values': ['TRUE', 'Today', 'This Month'],
        'content': '''
            <p><strong>Happy Birthday!</strong></p>
            <p>Wishing you a wonderful year ahead!</p>
        ''',
        'description': 'Birthday greeting for recipients'
    }
]
```

### Step 2: Update Your CSV
```csv
"Name", "Mail", "Technic", "Workshop", "Birthday", "PersonalNote"
"John", "john@email.com", "FALSE", "TRUE", "TRUE", "Have a great day!"
```

### Step 3: That's It! 
The system automatically detects and applies the new condition.

## Flexible Template System

**All templates can use ANY recipient data from your CSV!**

### Template Syntax:
- **Simple**: `{ColumnName}` → inserts the value from that CSV column
- **Fallback**: `{Nickname|{Name}}` → uses Nickname if available, otherwise Name
- **Empty fallback**: `{Manager|}` → uses Manager if available, otherwise empty string

### Real Examples:

```python
# Greeting with nickname fallback
DEFAULT_EMAIL_BODY_TEMPLATE = '''
    <p>Hi {Nickname|{Name}},<br>
       How are you doing in {Department|your role}?<br>
    </p>
'''

# Birthday with age and nickname
{
    'content': '''
        <p><strong>Happy Birthday, {Nickname|{Name}}!</strong></p>
        <p>Wishing you a wonderful {Age|new} year ahead!</p>
    '''
}

# Department message with manager info
{
    'content': '''
        <p>Hello {Nickname|{Name}},</p>
        <p>As part of the {Department} team{Manager|, your manager {Manager}} wanted to share...</p>
    '''
}
```

### Use Cases:
- **Nicknames**: `Hi {Nickname|{Name}}` → "Hi Johnny" or "Hi John Doe"
- **Optional data**: `{Birthday|How are you?|Happy Birthday!}` 
- **Departments**: `Welcome to {Department|our team}`
- **Ages**: `Celebrating {Age} years!`
- **Managers**: `Your manager {Manager} says...`

## Real Example Results

**Input CSV:**
```csv
"Name", "Mail", "Technic", "Workshop", "VIP", "NewMember", "PersonalNote"
"Frodo", "frodo@shire.hobbit", "FALSE", "TRUE", "TRUE", "TRUE", "Welcome!"
```

**Generated Email for Frodo:**
```
Hi Frodo,
How are you?

Thank you for participating in our recent workshop!
We hope you found the content valuable and look forward to your continued engagement.

VIP Member Exclusive Content
As a valued VIP member, you have access to special benefits and priority support.

Welcome to our community!
As a new member, here are some resources to help you get started...

Personal note: Welcome!

Best regards,
Your Team
```

## Sample Email Output

**For Frodo (Workshop + VIP + New Member + Nickname):**
```
Hi Mr. Underhill,
How are you doing in Marketing?

Thank you for participating in our recent workshop!
We hope you found the content valuable and look forward to your continued engagement.

VIP Member Exclusive Content
As a valued VIP member, you have access to special benefits and priority support.

Welcome to our community!
As a new member, here are some resources to help you get started...

Personal note: Welcome to Middle Earth adventures!

Best regards,
Your Team
```

**For Legolas (IT Team + VIP + Birthday + Template Fallback):**
```
Hi Legolas,
How are you doing in IT?

VIP Member Exclusive Content
As a valued VIP member, you have access to special benefits and priority support.

Happy Birthday, Legolas!
Wishing you a wonderful 2931 year ahead!

IT Team Update:
Hello Legolas, as part of our IT team we wanted to share some exciting news...

Best regards,
Your Team
```

## Email Features

The system automatically:
- **Personalizes greetings** with recipient names from email templates
- **Applies all matching conditions** based on CSV data and configuration
- **Handles personal notes** as conditional content (processed and added to the mails text last)
- **Supports unlimited conditions** through the configuration file
- **Generates both HTML and plain text** versions (readable by basically all mail clients and configurations)
- **Templates are fully configurable** in `email_config.py`

## Error Handling

The system gracefully handles:
- Missing CSV files
- Invalid email credentials
- Network connection issues
- Malformed recipient data
- Encoding problems
