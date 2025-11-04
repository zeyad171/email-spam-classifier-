"""
Gmail API Configuration Settings
"""

# Gmail API scopes needed for the application
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

# Credentials file path
CREDENTIALS_FILE = 'config/credentials.json'

# Token file path (created after first authentication)
TOKEN_FILE = 'config/token.json'

# Number of emails to fetch per run
FETCH_LIMIT = 50

# Whether to actually move emails to spam folder
ENABLE_MOVE_TO_SPAM = True

# Query to fetch emails (is:unread means unread emails only)
EMAIL_QUERY = 'is:unread'

