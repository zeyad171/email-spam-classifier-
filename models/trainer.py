"""
Model Trainer
Trains a spam classification model using labeled data
"""

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocessor import TextPreprocessor
from config.model_config import MODEL_FILE, VECTORIZER_FILE, MODEL_TYPE


# Load dataset
print("Loading dataset...")
dataset_path = None
for path in ['data/spam.csv', 'spam.csv']:
    if os.path.exists(path):
        dataset_path = path
        break

if not dataset_path:
    print("Error: Dataset not found. Please place spam.csv in data/ folder or root.")
    exit()

# Read CSV
df = pd.read_csv(dataset_path, encoding='utf-8')
print(f"Dataset loaded: {len(df)} rows")

# Use column names
df.columns = df.columns.str.lower().str.strip()

labels_raw = df['category'].astype(str).tolist()
texts = df['message'].astype(str).tolist()
print("Using columns: category, message")

# Show unique label values
unique_labels = set(str(l).lower().strip() for l in labels_raw)
print(f"Found label values: {unique_labels}")

# Convert labels to binary (ham=1, spam=0)
labels = []
for label in labels_raw:
    label_str = str(label).lower().strip()
    if label_str == 'ham':
        labels.append(1)  # ham
    elif label_str == 'spam':
        labels.append(0)  # spam
    else:
        labels.append(1)  # default to ham

# Remove empty texts
texts_clean = []
labels_clean = []
for text, label in zip(texts, labels):
    if text and text.strip() and text.lower() != 'nan':
        texts_clean.append(text)
        labels_clean.append(label)

texts = texts_clean
labels = labels_clean

print(f"Valid samples: {len(texts)}")
print(f"Ham: {sum(labels)}, Spam: {len(labels) - sum(labels)}")

# Preprocess texts
print("\nPreprocessing texts...")
preprocessor = TextPreprocessor()
preprocessed_texts = []
for text in texts:
    preprocessed = preprocessor.preprocess(text)
    preprocessed_texts.append(preprocessed)
print("Preprocessing complete!")

# Create TF-IDF vectorizer
print(f"\nTraining {MODEL_TYPE} model...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))

# Transform texts to features
X = vectorizer.fit_transform(preprocessed_texts)
y = labels

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize model
if MODEL_TYPE == 'naive_bayes':
    model = MultinomialNB()
elif MODEL_TYPE == 'svm':
    model = SVC(probability=True, kernel='linear')
elif MODEL_TYPE == 'logistic':
    model = LogisticRegression(max_iter=1000)
else:
    model = MultinomialNB()

# Train model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel trained successfully!")
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Spam', 'Ham'], labels=[0, 1], zero_division=0))

# Save model
print("\nSaving model...")
os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)

with open(MODEL_FILE, 'wb') as f:
    pickle.dump(model, f)

with open(VECTORIZER_FILE, 'wb') as f:
    pickle.dump(vectorizer, f)

print(f"Model saved to {MODEL_FILE}")
print(f"Vectorizer saved to {VECTORIZER_FILE}")
print("\nTraining complete!")

