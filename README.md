# Sending personalized mails in batch

This system sends **infinitely customizable** personalized emails based on CSV data with a **one-file configuration** approach.

## Key Features

- ✅ **One-File Configuration**: Add unlimited conditions by editing only `email_config.py`
- ✅ **CSV-based recipient management**: Load recipient data from CSV files  
- ✅ **Unlimited conditional content**: Workshop participants, VIP members, new users, etc.
- ✅ **Multiple conditions per recipient**: Recipients can match several conditions simultaneously
- ✅ **Personalized content**: Names, personal notes, dynamic greetings
- ✅ **HTML & Plain text**: Dual-format emails for maximum compatibility
- ✅ **UTF-8 support**: International character support
- ✅ **Test mode**: Preview emails without sending
- ✅ **Auto-detection**: System automatically finds and applies all matching conditions
- ✅ **Error handling**: Graceful handling of missing columns and data issues

## 📁 File Structure

```
sendEmails/
├── main.py                        # Main script for sending emails
├── newPage.py                     # Email content generation class  
├── email_config.py                # 🎯 CONFIGURATION FILE - Edit this to add conditions
├── exampleRecipient.csv           # Sample data with multiple conditions
├── credentials.env_template       # Template for email credentials
├── credentials.env                # Your email server credentials (not in repo)
└── README.md                      # This file
```

## Quick Start - Adding New Conditions

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

## Setup

1. **Install required packages** (assuming you are using conda):
   ```bash
   conda run pip install pandas beautifulsoup4 python-dotenv
   ```

2. **Create credentials.env file** (you can copy the provided template):
   ```env
   SenderMail=your-email@example.com
   SenderPassword=your-password
   SenderServer=smtp.gmail.com
   SenderPort=465
   ```
**Never commit `credentials.env` to version control or upload the file together with other files in some shared cloud!!!**

3. **Prepare CSV file** with columns:
   - `Name`: Recipient's name (required)
   - `Mail`: Email address (required)
   - Any additional columns for conditions (e.g., `Technic`, `Workshop`, `VIP`, `PersonalNote`)

## Usage

### Preview Mode (Default - Safe!)
```bash
python main.py
# Shows email previews without sending anything
```

### Send Mode (Requires confirmation)
```bash
python main.py --send
# Asks for confirmation before actually sending emails
```

**The system runs in safe preview mode by default!** You must explicitly use `--send` to actually send emails.

## CSV Format

```csv
"Name", "Mail", "Nickname", "Department", "Birthday", "Age", "Technic", "VIP", "PersonalNote"
"John Doe", "john@example.com", "Johnny", "Engineering", "TRUE", "25", "TRUE", "TRUE", "Great work!"
"Jane Smith", "jane@example.com", "", "Marketing", "FALSE", "30", "FALSE", "TRUE", "Excellent campaign!"
```

**Templates can use ANY CSV column with fallbacks:** `{Nickname|{Name}}` uses nickname or falls back to name!

## Email Personalization

The system automatically:
- **Personalizes greetings** with recipient names from email templates
- **Applies all matching conditions** based on CSV data and configuration
- **Handles personal notes** as conditional content (processed and added to the mails text last)
- **Supports unlimited conditions** through the configuration file
- **Generates both HTML and plain text** versions (readable by basically all mail clients and configurations)
- **Templates are fully configurable** in `email_config.py`


## Sample Output

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

## Error Handling

The system handles:
- Missing CSV files
- Invalid email credentials
- Network connection issues
- Malformed recipient data
- Encoding problems
