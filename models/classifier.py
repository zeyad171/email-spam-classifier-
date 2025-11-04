"""
Spam Classifier Model
"""

import os
import pickle
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocessor import TextPreprocessor
from config.model_config import MODEL_FILE, VECTORIZER_FILE, CONFIDENCE_THRESHOLD


class SpamClassifier:
    """Spam classification using trained ML model"""
    
    def __init__(self, model_path=None, vectorizer_path=None):
        self.model_path = model_path or MODEL_FILE
        self.vectorizer_path = vectorizer_path or VECTORIZER_FILE
        self.preprocessor = TextPreprocessor()
        self.model = None
        self.vectorizer = None
        self.confidence_threshold = CONFIDENCE_THRESHOLD
        self._load_model()
    
    def _load_model(self):
        """Load trained model and vectorizer"""
        if not os.path.exists(self.model_path):
            print(f"Warning: Model file not found at {self.model_path}")
            print("Train the model first: python models/trainer.py")
            return
        
        if not os.path.exists(self.vectorizer_path):
            print(f"Warning: Vectorizer file not found at {self.vectorizer_path}")
            print("Train the model first: python models/trainer.py")
            return
        
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            print(f"Model loaded from {self.model_path}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def predict(self, text):
        """Predict if text is spam or not"""
        if self.model is None or self.vectorizer is None:
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'spam_probability': 0.0
            }
        
        # Preprocess text
        preprocessed_text = self.preprocessor.preprocess(text)
        
        # Transform to features
        text_vectorized = self.vectorizer.transform([preprocessed_text])
        
        # Make prediction (0=spam, 1=ham)
        prediction = self.model.predict(text_vectorized)[0]
        probabilities = self.model.predict_proba(text_vectorized)[0]
        
        spam_prob = probabilities[0]  # class 0 is spam
        is_spam = spam_prob >= self.confidence_threshold
        
        return {
            'prediction': 'spam' if is_spam else 'not_spam',
            'confidence': max(spam_prob, 1 - spam_prob),
            'spam_probability': spam_prob
        }
    


