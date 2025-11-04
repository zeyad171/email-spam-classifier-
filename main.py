"""
Gmail Spam Classifier - Main Application
"""

import os
import sys
import time
import logging
import argparse
import schedule

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.gmail_handler import GmailHandler
from models.classifier import SpamClassifier
from config.gmail_config import FETCH_LIMIT, EMAIL_QUERY, ENABLE_MOVE_TO_SPAM

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/spam_classifier.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def classify_and_process_emails():
    """Fetch, classify, and process emails"""
    try:
        logger.info("Starting email classification...")
        
        gmail = GmailHandler()
        classifier = SpamClassifier()
        
        if classifier.model is None:
            logger.error("Model not loaded. Train first: python models/trainer.py")
            return
        
        logger.info(f"Fetching unread emails (limit: {FETCH_LIMIT})...")
        emails = gmail.fetch_unread_emails(query=EMAIL_QUERY, max_results=FETCH_LIMIT)
        
        if not emails:
            logger.info("No emails to process.")
            return
        
        logger.info(f"Processing {len(emails)} email(s)...")
        
        spam_count = 0
        not_spam_count = 0
        
        for email in emails:
            msg_id = email['id']
            
            subject = gmail.get_message_subject(email)
            sender = gmail.get_message_from(email)
            body = gmail.get_message_body(email)
            snippet = gmail.get_message_snippet(email)
            
            email_text = f"{subject} {body}".strip()
            if not email_text:
                email_text = snippet
            
            result = classifier.predict(email_text)
            prediction = result['prediction']
            confidence = result['confidence']
            spam_prob = result['spam_probability']
            
            logger.info(f"Email: {subject[:50]}...")
            logger.info(f"  From: {sender}")
            logger.info(f"  Prediction: {prediction} (Probability: {spam_prob:.2%})")
            
            if prediction == 'spam':
                spam_count += 1
                
                if ENABLE_MOVE_TO_SPAM:
                    success = gmail.move_to_spam(msg_id)
                    if success:
                        logger.info(f"  Moved to spam folder")
                    else:
                        logger.warning(f"  Failed to move to spam")
                else:
                    logger.info(f"  (Move to spam disabled)")
            else:
                not_spam_count += 1
                gmail.mark_as_read(msg_id)
                logger.info(f"  Marked as read")
        
        logger.info("Classification Summary:")
        logger.info(f"  Total: {len(emails)}, Spam: {spam_count}, Not spam: {not_spam_count}")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


def run_scheduler():
    """Run scheduler to process emails every 6 hours"""
    logger.info("Starting Gmail Spam Classifier")
    logger.info("Runs every 6 hours. Press Ctrl+C to stop")
    
    schedule.every(6).hours.do(classify_and_process_emails)
    
    logger.info("Running initial classification...")
    classify_and_process_emails()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Gmail Spam Classifier')
    parser.add_argument('--test', action='store_true', 
                       help='Run once and exit (test mode)')
    
    args = parser.parse_args()
    
    if args.test:
        logger.info("Running in TEST mode")
        classify_and_process_emails()
        logger.info("Test completed.")
    else:
        run_scheduler()


if __name__ == "__main__":
    main()
