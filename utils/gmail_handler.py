"""
Gmail API Handler
"""

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.gmail_config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE


class GmailHandler:
    """Handles Gmail API operations"""
    
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Credentials file not found: {CREDENTIALS_FILE}\n"
                        "Download from Google Cloud Console and place in config/ folder."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            
            print("Authentication successful!")
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("Gmail API connected!")
    
    def get_message(self, msg_id):
        """Get message by ID"""
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id).execute()
            return message
        except HttpError as error:
            print(f"Error: {error}")
            return None
    
    def get_message_body(self, message):
        """Extract body text from message"""
        body_text = ""
        
        if 'payload' in message:
            payload = message['payload']
            
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] in ['text/plain', 'text/html']:
                        data = part['body']['data']
                        body_text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            elif 'body' in payload:
                data = payload['body'].get('data', '')
                if data:
                    body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        return body_text
    
    def get_message_subject(self, message):
        """Extract subject from message"""
        headers = message['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == 'subject':
                return header['value']
        return "No Subject"
    
    def get_message_from(self, message):
        """Extract sender from message"""
        headers = message['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == 'from':
                return header['value']
        return "Unknown"
    
    def get_message_snippet(self, message):
        """Get message snippet"""
        return message.get('snippet', '')
    
    def fetch_unread_emails(self, query='is:unread', max_results=50):
        """Fetch unread emails"""
        try:
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                print("No unread emails found.")
                return []
            
            print(f"Found {len(messages)} unread email(s).")
            
            full_messages = []
            for msg in messages:
                message = self.get_message(msg['id'])
                if message:
                    full_messages.append(message)
            
            return full_messages
            
        except HttpError as error:
            print(f"Error fetching emails: {error}")
            return []
    
    def move_to_spam(self, msg_id):
        """Move email to spam folder"""
        if not msg_id:
            return False
        
        try:
            labels_result = self.service.users().labels().list(userId='me').execute()
            labels = labels_result.get('labels', [])
            
            spam_label_id = None
            for label in labels:
                if label['name'].lower() == 'spam':
                    spam_label_id = label['id']
                    break
            
            if not spam_label_id:
                print("SPAM label not found!")
                return False
            
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={
                    'addLabelIds': [spam_label_id],
                    'removeLabelIds': ['INBOX']
                }
            ).execute()
            
            return True
            
        except HttpError as error:
            print(f"Error moving to spam: {error}")
            return False
    
    def mark_as_read(self, msg_id):
        """Mark email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            print(f"Error marking as read: {error}")
            return False