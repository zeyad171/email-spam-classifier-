"""
Model Configuration Settings
"""

# Model type: 'naive_bayes', 'svm', or 'logistic'
MODEL_TYPE = 'naive_bayes'

# Confidence threshold for spam classification (0.0 to 1.0)
CONFIDENCE_THRESHOLD = 0.7

# Path to trained model file
MODEL_FILE = 'models/spam_classifier.pkl'

# Path to TF-IDF vectorizer
VECTORIZER_FILE = 'models/tfidf_vectorizer.pkl'


