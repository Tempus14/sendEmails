# Email Configuration - Add your conditional content here
# Users only need to modify this file to add new conditional content

# =============================================================================
# CONDITIONAL CONTENT CONFIGURATION
# =============================================================================
# Each condition should have:
# - 'column': CSV column name to check
# - 'trigger_values': List of values that activate this content (case-insensitive)
# - 'content': HTML content to add when condition is met
# - 'description': Human-readable description of what this does

CONDITIONAL_CONTENT = [
    {
        'name': 'technic_team',
        'column': 'Technic', 
        'trigger_values': ['TRUE', 'Yes', '1'],
        'content': '''
            <p><strong>Thank you for your work in the technic department!</strong></p>
            <p>Your technical expertise is greatly appreciated.</p>
        ''',
        'description': 'Special message for technical team members'
    },
    
    {
        'name': 'workshop_participant',
        'column': 'Workshop',
        'trigger_values': ['TRUE', 'Yes', 'Attended', '1'],
        'content': '''
            <p><em>Thank you for participating in our recent workshop!</em></p>
            <p>We hope you found the content valuable and look forward to your continued engagement.</p>
        ''',
        'description': 'Thank you message for workshop participants'
    },
    
    {
        'name': 'vip_member',
        'column': 'VIP',
        'trigger_values': ['TRUE', 'Yes', 'Premium', 'Gold', '1'],
        'content': '''
            <p><strong>VIP Member Exclusive Content</strong></p>
            <p>As a valued VIP member, you have access to special benefits and priority support.</p>
        ''',
        'description': 'Special content for VIP members'
    },
    
    {
        'name': 'new_member',
        'column': 'NewMember',
        'trigger_values': ['TRUE', 'Yes', 'New', 'Recent', '1'],
        'content': '''
            <p><strong>Welcome to our community!</strong></p>
            <p>As a new member, here are some resources to help you get started...</p>
        ''',
        'description': 'Welcome message for new members'
    },
    
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
    },
    
    {
        'name': 'department_message',
        'column': 'Department',
        'trigger_values': ['Engineering', 'IT', 'Development'],
        'content': '''
            <p><strong>{Department} Team Update:</strong></p>
            <p>Hello {Nickname|{Name}}, as part of our {Department} team we wanted to share some exciting news...</p>
        ''',
        'description': 'Department-specific messaging with fallback to name',
        'is_template': True
    },
    
    {
        'name': 'personal_note',
        'column': 'PersonalNote',
        'trigger_values': ['*'],  # Special trigger: any non-empty value
        'content': '''<p><em>Personal note: {PersonalNote}</em></p>''',  # Uses full recipient data
        'description': 'Personal note for recipient (always processed last)',
        'is_template': True  # Indicates this content should be formatted with recipient data
    }

]

# =============================================================================
# EMAIL TEMPLATE CONFIGURATION
# =============================================================================
# All templates can use ANY recipient data as placeholders!
# Available placeholders: {Name}, {Mail}, {Technic}, {PersonalNote}, {Nickname}, {Birthday}, etc.
# Use {Name|fallback_text} for fallback values when data is missing

# Main email body template - can use any recipient data with fallbacks
DEFAULT_EMAIL_BODY_TEMPLATE = '''
    <p>Hi {Nickname|{Name}},<br>
       How are you doing in {Department|your role}?<br>
    </p>
'''

# Fallback when no name is provided
FALLBACK_EMAIL_BODY_TEMPLATE = '''
    <p>Hi there,<br>
       How are you?<br>
    </p>
'''

# Default closing template - can also use recipient data
DEFAULT_CLOSING = '''
    <p>Best regards,<br>Your Team</p>
'''

# Advanced template examples showing flexible data usage:
# 
# Example with nickname fallback:
# '''
#     <p>Hi {Nickname|{Name}},<br>
#        Hope you're doing well!<br>
#     </p>
# '''
#
# Example with birthday:
# '''
#     <p>Hi {Name},<br>
#        {Birthday|How are you?|Happy Birthday! Hope your special day is amazing!}<br>
#     </p>
# '''
#
# Example with multiple data points:
# '''
#     <p>Dear {Title|} {Name},<br>
#        Thank you for being part of our {Department|general} team.<br>
#     </p>
# '''

# =============================================================================
# HOW TO ADD NEW CONDITIONS - INSTRUCTIONS FOR USERS
# =============================================================================

"""
TO ADD A NEW CONDITIONAL CONTENT BLOCK:

1. Add a new dictionary to the CONDITIONAL_CONTENT list above with these fields:
   - 'name': Unique identifier (letters, numbers, underscores only)
   - 'column': Name of the CSV column to check
   - 'trigger_values': List of values that activate this content
   - 'content': HTML content to include when condition is met
   - 'description': What this condition does

2. Make sure your CSV file includes the corresponding column

EXAMPLE:
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

3. Your CSV would then include a 'Birthday' column:
   "Name", "Mail", "Birthday", "PersonalNote"
   "John", "john@email.com", "TRUE", "Have a great day!"

That's it! The system will automatically detect and apply the new condition.

TO CUSTOMIZE EMAIL TEMPLATES:

You can modify the templates above to change the basic email structure:
- DEFAULT_EMAIL_BODY_TEMPLATE: Main email body with {name} placeholder
- FALLBACK_EMAIL_BODY_TEMPLATE: Used when no name is provided
- DEFAULT_CLOSING: Email signature/closing
- PERSONAL_NOTE_TEMPLATE: Template for personal notes with {note} placeholder

EXAMPLE - Custom greeting:
DEFAULT_EMAIL_BODY_TEMPLATE = '''
    <p>Dear {name},<br>
       I hope this message finds you well!<br>
    </p>
'''

EXAMPLE - Custom closing:
DEFAULT_CLOSING = '''
    <p>Warm regards,<br>
    The Marketing Team<br>
    <em>Company Name</em></p>
'''
"""

# =============================================================================
# VALIDATION SETTINGS
# =============================================================================

# Whether to show warnings for missing columns
SHOW_MISSING_COLUMN_WARNINGS = False

# Whether to continue processing if a conditional column is missing
CONTINUE_ON_MISSING_COLUMNS = True