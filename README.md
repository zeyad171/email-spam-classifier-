# Gmail Spam Classifier with NLP

An AI-powered Gmail spam classifier that automatically fetches, classifies, and moves spam emails to the spam folder every 6 hours.

## Features

- ✅ Automatic email fetching from Gmail
- ✅ NLP-based spam classification using Machine Learning
- ✅ Moves spam emails to spam folder automatically
- ✅ Runs every 6 hours automatically
- ✅ Configurable confidence threshold
- ✅ Detailed logging

## Prerequisites

1. Python 3.8 or higher
2. Google Cloud account
3. Gmail account
4. Spam dataset (CSV format)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK data:**
   ```python
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
   ```

3. **Set up Gmail API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download credentials as `credentials.json`
   - Place it in the `config/` folder

4. **Prepare your dataset:**
   - Place your `spam.csv` file in the project root or `data/` folder
   - CSV should have text and label columns (auto-detected)

## Usage

### 1. Train the Model

```bash
python models/trainer.py
```

This will:
- Load your spam dataset
- Preprocess the text
- Train the ML model
- Save the trained model

### 2. Run the Application

**Continuous mode (every 6 hours):**
```bash
python main.py
```

**Test mode (one-time run):**
```bash
python main.py --test
```

## Configuration

Edit `config/gmail_config.py`:
- `FETCH_LIMIT`: Number of emails to fetch (default: 50)
- `ENABLE_MOVE_TO_SPAM`: Toggle moving emails (default: True)

Edit `config/model_config.py`:
- `CONFIDENCE_THRESHOLD`: Minimum confidence for spam (default: 0.7)
- `MODEL_TYPE`: 'naive_bayes', 'svm', or 'logistic' (default: 'naive_bayes')

## Project Structure

```
nlp/
├── config/
│   ├── gmail_config.py      # Gmail settings
│   ├── model_config.py      # Model settings
│   └── credentials.json     # Gmail API credentials (you provide)
├── models/
│   ├── trainer.py           # Model training script
│   ├── classifier.py        # Spam classifier
│   ├── spam_classifier.pkl  # Trained model (generated)
│   └── tfidf_vectorizer.pkl # Vectorizer (generated)
├── utils/
│   ├── gmail_handler.py     # Gmail API handler
│   └── preprocessor.py      # Text preprocessing
├── data/
│   └── spam.csv             # Training dataset (you provide)
├── logs/
│   └── spam_classifier.log  # Application logs
├── main.py                  # Main application
└── requirements.txt         # Dependencies
```

## NLP Techniques Used

This project implements standard NLP practices commonly taught in NLP courses:

### Text Preprocessing
- **Tokenization**: Splits text into individual words/tokens using NLTK
- **Normalization**: Converts to lowercase, handles URLs, emails, phone numbers
- **Stop Word Removal**: Removes common words (the, a, an, etc.) that don't help classification
- **Lemmatization**: Reduces words to their root forms (running → run)
- **Feature Preservation**: Keeps important spam indicators (URLs, money mentions, etc.)

### Feature Extraction
- **TF-IDF Vectorization**: Converts text to numerical features
  - Term Frequency-Inverse Document Frequency weighting
  - Unigrams and bigrams (single words and word pairs)
  - Vocabulary size limited to 5000 most important features

### Classification Models
- **Naive Bayes**: Fast, works well with text data
- **SVM (Support Vector Machine)**: Good accuracy, robust to overfitting
- **Logistic Regression**: Interpretable, good baseline model

### Evaluation
- Train/Test split (80/20)
- Accuracy score
- Classification report (precision, recall, F1-score)

## How It Works

1. **Authentication**: Connects to Gmail using OAuth 2.0
2. **Fetching**: Retrieves unread emails from inbox
3. **Preprocessing**: Cleans and normalizes email text
4. **Classification**: Uses trained ML model to classify each email
5. **Action**: Moves spam emails to spam folder, marks others as read
6. **Scheduling**: Repeats every 6 hours automatically

## Logs

View logs:
```bash
# Windows
type logs\spam_classifier.log

# Mac/Linux
cat logs/spam_classifier.log
```

## Troubleshooting

**"Credentials not found"**
- Ensure `credentials.json` is in `config/` folder
- Download from Google Cloud Console

**"Model not found"**
- Train the model first: `python models/trainer.py`

**"High false positives"**
- Increase `CONFIDENCE_THRESHOLD` in `config/model_config.py`
- Retrain with more data

