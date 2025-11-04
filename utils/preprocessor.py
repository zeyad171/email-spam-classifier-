"""
Text Preprocessing Utilities
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)


class TextPreprocessor:
    """Preprocesses text for spam classification"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Add email-specific stop words
        self.stop_words.update([
            'subject', 're', 'fw', 'fwd', 'cc', 'bcc',
            'to', 'from', 'date', 'sent', 'message',
            'http', 'https', 'www', 'com', 'org', 'net'
        ])
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'http[s]?://\S+|www\.\S+', 'url', text)
        text = re.sub(r'\S+@\S+', 'emailaddr', text)
        text = re.sub(r'[$]\d+\.?\d*|\d+\.?\d*\s*dollars?', 'money', text)
        text = re.sub(r'\d{3}-\d{3}-\d{4}|\(\d{3}\)\s*\d{3}-\d{4}', 'phonenumber', text)
        text = re.sub(r'\d+', 'number', text)
        text = re.sub(r'[^\w\s!]', ' ', text)
        text = re.sub(r'!{2,}', ' !!', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """Remove stop words"""
        return [word for word in tokens if word not in self.stop_words]
    
    def lemmatize(self, tokens):
        """Lemmatize tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text):
        """Complete preprocessing pipeline"""
        # Clean text
        cleaned = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        
        # Remove stop words
        tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        tokens = self.lemmatize(tokens)
        
        # Filter short tokens (keep important features)
        tokens = [t for t in tokens if len(t) > 1 or t in ['url', 'money', 'number', 'emailaddr', 'phonenumber']]
        
        # Join tokens back
        return ' '.join(tokens)



