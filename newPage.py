from bs4 import BeautifulSoup  
from email_config import (
    CONDITIONAL_CONTENT, 
    DEFAULT_EMAIL_BODY_TEMPLATE, 
    FALLBACK_EMAIL_BODY_TEMPLATE,
    DEFAULT_CLOSING,
    SHOW_MISSING_COLUMN_WARNINGS
)

# Class for creating a new email page in html format built from different parts
# the final page can then be returned as html and plain text
class newPage:
    def __init__(self, recipient_name="", recipient_data=None):
        self.recipient_name = recipient_name
        self.recipient_data = recipient_data or {}
        self.text = self.defaultText()
        self.conditional_content = ""
        self.greetings = self.defaultGreetings()
        self.personal_note = ""
    
    def defaultText(self):
        # Default text for the new email using configuration with full recipient data access
        if self.recipient_name:
            return self.format_template(DEFAULT_EMAIL_BODY_TEMPLATE, self.recipient_data)
        else:
            return self.format_template(FALLBACK_EMAIL_BODY_TEMPLATE, self.recipient_data)
    
    def defaultGreetings(self):
        # Default greetings using configuration with full recipient data access
        return self.format_template(DEFAULT_CLOSING, self.recipient_data)
    
    def format_template(self, template, recipient_data):
        """
        Format a template with recipient data, supporting fallback syntax.
        Supports {ColumnName|fallback_text} syntax for graceful fallbacks.
        """
        result = template
        max_iterations = 5  # Prevent infinite loops
        
        for iteration in range(max_iterations):
            # Find all simple placeholders first: {ColumnName}
            import re
            
            def replace_simple_placeholder(match):
                column_name = match.group(1).strip()
                if column_name in recipient_data:
                    value = str(recipient_data[column_name]).strip()
                    if value and value.lower() not in ['nan', 'none', 'false', '']:
                        return value
                return ""
            
            # First pass: replace all simple placeholders
            prev_result = result
            result = re.sub(r'\{([^|{}]+)\}', replace_simple_placeholder, result)
            
            # Second pass: handle fallback placeholders
            def replace_fallback_placeholder(match):
                content = match.group(1)
                if '|' in content:
                    parts = content.split('|', 1)
                    column_name = parts[0].strip()
                    fallback = parts[1].strip()
                    
                    # Check if the column exists and has a non-empty value
                    if column_name in recipient_data:
                        value = str(recipient_data[column_name]).strip()
                        if value and value.lower() not in ['nan', 'none', 'false', '']:
                            return value
                    
                    # Use fallback
                    return fallback
                
                return match.group(0)  # Return unchanged if no fallback
            
            result = re.sub(r'\{([^{}]+\|[^{}]+)\}', replace_fallback_placeholder, result)
            
            # If no changes were made, we're done
            if result == prev_result:
                break
        
        return result
    
    def processConditionalContent(self):
        """
        Process all conditional content based on recipient data and configuration.
        This automatically handles all conditions defined in email_config.py
        """
        applied_conditions = []
        
        for condition in CONDITIONAL_CONTENT:
            condition_name = condition['name']
            column_name = condition['column']
            trigger_values = [str(v).upper() for v in condition['trigger_values']]
            content = condition['content']
            is_template = condition.get('is_template', False)
            template_key = condition.get('template_key', '')
            
            # Check if the required column exists in recipient data
            if column_name not in self.recipient_data:
                if SHOW_MISSING_COLUMN_WARNINGS:
                    print(f"  [WARNING] Column '{column_name}' not found for condition '{condition_name}'")
                continue
            
            # Get the value and check if it matches any trigger values
            recipient_value = str(self.recipient_data[column_name]).strip()
            recipient_value_upper = recipient_value.upper()
            
            # Handle special '*' trigger that matches any non-empty value
            should_apply = False
            if '*' in trigger_values:
                should_apply = recipient_value and recipient_value != 'nan' and recipient_value.strip()
            else:
                should_apply = recipient_value_upper in trigger_values
            
            if should_apply:
                # Handle template conditions with full recipient data access
                if is_template:
                    final_content = self.format_template(content, self.recipient_data)
                else:
                    final_content = content
                
                self.conditional_content += final_content
                applied_conditions.append(condition_name)
                print(f"  [APPLIED] Condition '{condition_name}' activated")
        
        return applied_conditions
    



    def returnPage(self):
        # Return the final page as plain text and html for sending the email compatible with different email clients and preferences
        htmlText = f"""\
        <html>
          <head>
            <meta charset="UTF-8">
          </head>
          <body>
            {self.text}
            {self.conditional_content}
            {self.personal_note}
            {self.greetings}
          </body>
        </html>
        """
        # Parse HTML with explicit UTF-8 encoding and better text extraction
        soup = BeautifulSoup(htmlText, 'html.parser')
        plainText = soup.get_text(separator='\n', strip=True)
        return plainText, htmlText
    
    def saveHTML(self, filename="email.html"):
        # Save the html text to a file
        _, htmlText = self.returnPage()
        with open(filename, "w", encoding="utf-8") as file:
            file.write(htmlText)
    

if __name__ == "__main__":
    # Example usage
    sample_data = {'Name': 'John Doe', 'Mail': 'john@example.com', 'PersonalNote': 'Great to meet you!'}
    email_page = newPage(recipient_name='John Doe', recipient_data=sample_data)
    email_page.processConditionalContent()
    plain, html = email_page.returnPage()
    email_page.saveHTML()