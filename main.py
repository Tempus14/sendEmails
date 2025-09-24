import os
import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from newPage import newPage

def load_recipients(csv_file="exampleRecipient.csv"):
    """Load recipients from CSV file and return pandas DataFrame"""
    try:
        # Read CSV file with proper handling of spaces in column names
        df = pd.read_csv(csv_file)
        # Clean column names (remove quotes and extra spaces)
        df.columns = df.columns.str.strip().str.replace('"', '')
        
        # Clean all string data (remove quotes and extra spaces)
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                df[col] = df[col].astype(str).str.strip().str.replace('"', '')
        
        print(f"Loaded {len(df)} recipients from {csv_file}")
        print("Columns:", df.columns.tolist())
        return df
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        return None
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def process_personalized_email(recipient_row, test_mode=False, sender_email=None, password=None, sender_server=None, port=None):
    """Process a personalized email for a single recipient - either send or preview based on test_mode"""
    try:
        # Extract recipient information
        name = recipient_row['Name']
        email = recipient_row['Mail']
        
        print(f"Processing email for {name} ({email})")
        
        # Create personalized email content with all recipient data
        email_page = newPage(recipient_name=name, recipient_data=dict(recipient_row))
        
        # Process all conditional content automatically
        applied_conditions = email_page.processConditionalContent()
        if applied_conditions:
            print(f"  - Applied conditions: {', '.join(applied_conditions)}")
        else:
            print(f"  - No conditions applied")
        
        # Generate email content
        plain_text, html_text = email_page.returnPage()
        
        if test_mode:
            # Test mode - just display the email content
            print(f"\n--- Email Preview for {name} ---")
            print(plain_text)
            print("-" * 50)
            return True, None
        else:
            # Send mode - actually send the email
            # Create email message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Personal message for {name}"
            message["From"] = sender_email
            message["To"] = email
            
            # Attach plain text and HTML parts
            part1 = MIMEText(plain_text, "plain", "utf-8")
            part2 = MIMEText(html_text, "html", "utf-8")
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(sender_server, int(port), context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, email, message.as_string())
            
            print(f"  [SUCCESS] Email sent successfully to {name} ({email})")
            return True, None
        
    except Exception as e:
        error_msg = f"Failed to process email for {name}: {e}"
        print(f"  [FAILED] {error_msg}")
        return False, error_msg

def confirm_send():
    """Ask for user confirmation before sending emails"""
    print("\n" + "="*60)
    print("WARNING: You are about to send REAL emails!")
    print("="*60)
    print("This will send actual emails to the recipients in your CSV file.")
    print("Make sure you have:")
    print(" - Reviewed the email content in test mode")
    print(" - Verified all recipient email addresses")
    print(" - Checked your email credentials")
    print(" - Confirmed you want to send these emails")
    print()
    
    while True:
        response = input("Are you absolutely sure you want to send emails? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            print("\nEmail sending cancelled. Run in test mode to preview emails:")
            print("  python main.py")
            return False
        else:
            print("Please enter 'yes' or 'no'")

def main():
    """Main function to orchestrate the email sending process"""
    import sys
    
    # Default is test mode - send mode requires explicit --send flag
    send_mode = len(sys.argv) > 1 and sys.argv[1].lower() in ['send', '--send', '-s']
    test_mode = not send_mode
    
    # Load recipients
    recipients_df = load_recipients()
    if recipients_df is None:
        return
    
    if test_mode:
        print("[TEST MODE] Generating sample emails without sending...")
        print("=" * 60)
        print("TIP: To actually send emails, run: python main.py --send")
        print("=" * 60)
    else:
        # Send mode - require confirmation
        if not confirm_send():
            return
            
        # Load environment variables for sending
        load_dotenv("credentials.env")
        
        sender_email = os.getenv("SenderMail")
        password = os.getenv("SenderPassword")
        sender_server = os.getenv("SenderServer")
        port = os.getenv("SenderPort")
        
        # Validate required environment variables
        if not all([sender_email, password, sender_server, port]):
            print("[ERROR] Missing required environment variables in credentials.env")
            print("Required: SenderMail, SenderPassword, SenderServer, SenderPort")
            print("Create a credentials.env file based on credentials.env_template")
            return
        
        print(f"\n[SEND MODE] Starting to send {len(recipients_df)} personalized emails...")
        print("=" * 50)
    
    # Process emails for each recipient
    successful_sends = 0
    failed_sends = 0
    failed_recipients = []
    
    for index, recipient in recipients_df.iterrows():
        if test_mode:
            success, error_msg = process_personalized_email(recipient, test_mode=True)
        else:
            success, error_msg = process_personalized_email(
                recipient, test_mode=False, 
                sender_email=sender_email, password=password, 
                sender_server=sender_server, port=port
            )
        
        if success:
            successful_sends += 1
        else:
            failed_sends += 1
            failed_recipients.append((recipient['Name'], error_msg))
        
        print()  # Empty line for readability
    
    # Summary
    print("=" * 50)
    if test_mode:
        print(f"[TEST SUMMARY] Email preview complete!")
        print(f"[PROCESSED] Total previewed: {len(recipients_df)}")
        print()
        print("Ready to send? Run: python main.py --send")
        print("Want to modify? Edit email_config.py or your CSV file")
    else:
        print(f"[SUMMARY] Email sending complete!")
        print(f"[SUCCESS] Successful: {successful_sends}")
        print(f"[FAILED] Failed: {failed_sends}")
        if failed_recipients:
            print(f"[FAILED RECIPIENTS]:")
            for name, error in failed_recipients:
                print(f"  - {name}: {error}")
        print(f"[TOTAL] Total: {len(recipients_df)}")
        print()
        print("All done! Your personalized emails have been sent.")

if __name__ == "__main__":
    main()