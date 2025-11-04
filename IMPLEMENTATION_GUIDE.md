# Step-by-Step Implementation Guide

## 🎯 Complete Implementation Guide for Gmail Spam Classifier

Follow these steps to build your Gmail spam classifier from scratch.

---

## 📋 Prerequisites Setup

### Step 1: Verify Python Installation

Make sure you have Python 3.8 or higher installed:

```bash
# Check Python version
python --version

# Should show Python 3.8.x or higher
```

### Step 2: Google Cloud Setup (Gmail API Access)

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project**
   - Click "Select a project" → "New Project"
   - Name: "Gmail Spam Classifier"
   - Click "Create"

3. **Enable Gmail API**
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - User Type: External
     - App name: "Gmail Spam Classifier"
     - Support email: your email
     - Developer email: your email
     - Click "Save and Continue" through all steps
   - Application type: "Desktop app"
   - Name: "Gmail Spam Classifier Client"
   - Click "Create"
   - **Download the JSON credentials file** → Save as `credentials.json`
   - Place it in the `config/` folder

---

## 🏗️ Project Setup

### Step 3: Create Folder Structure

```
nlp/
├── config/
│   ├── __init__.py
│   ├── gmail_config.py
│   └── credentials.json          # Download from Google Cloud
├── models/
│   ├── __init__.py
│   ├── trainer.py
│   └── classifier.py
├── utils/
│   ├── __init__.py
│   ├── gmail_handler.py
│   └── preprocessor.py
├── data/
│   └── spam.csv                  # Training data (CSV format)
├── logs/                         # Auto-created for logs
├── main.py
├── requirements.txt
├── PROJECT_PLAN.md
└── README.md
```

---

## 💻 Installation & Setup Walkthrough

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**What each package does:**
- `google-api-python-client`: Gmail API access
- `google-auth-oauthlib`: OAuth authentication
- `google-auth-httplib2`: HTTP client for auth
- `scikit-learn`: ML models (Naive Bayes, SVM)
- `nltk`: Natural language processing
- `pandas`: Data manipulation
- `schedule`: Task scheduling
- `python-dotenv`: Environment variables

### Step 5: Download NLTK Data

Run Python and download required NLTK data:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
```

---

## 🔐 Gmail API Authentication

### Step 6: First-Time Authentication Flow

When you run the program for the first time:

1. It will open your browser
2. Sign in with your Google account
3. Grant permissions to the app
4. A `token.json` file will be saved in `config/` folder
5. Subsequent runs will use this token automatically

**Permissions needed:**
- Read email
- Modify mailbox (to move spam)

---

## 🎓 Training Your Model

### Step 7: Prepare Training Data

You need a dataset of labeled emails:
- **Spam**: Emails marked as spam
- **Not Spam**: Regular emails

**Sample training data:**
- Use publicly available spam datasets
- Or manually label your own emails
- Minimum recommended: 1000 spam + 1000 not spam

### Step 8: Train the Model

```bash
python models/trainer.py
```

**What happens:**
1. Loads training dataset
2. Preprocesses text (removes stop words, tokenizes)
3. Extracts features using TF-IDF
4. Trains Naive Bayes classifier
5. Saves model to `models/spam_classifier.pkl`

---

## 🚀 Running the Application

### Step 9: Run Main Program

```bash
python main.py
```

**What it does:**
1. Authenticates with Gmail
2. Starts scheduler (runs every 6 hours)
3. On each run:
   - Fetches unread emails
   - Classifies each email
   - Moves spam to spam folder
   - Logs results

### Step 10: Test Mode (Optional)

For testing without waiting 6 hours:

```python
# In main.py, change:
python main.py --test
```

This runs classification immediately and exits.

---

## 🔧 Configuration Options

### Adjustable Settings

**In `config/gmail_config.py`:**
- `FETCH_LIMIT`: Number of emails to fetch (default: 50)
- `ENABLE_MOVE_TO_SPAM`: Toggle moving emails (default: True)

**In `config/model_config.py`:**
- `CONFIDENCE_THRESHOLD`: Minimum confidence for spam (default: 0.7)
- `MODEL_TYPE`: 'naive_bayes' or 'svm' (default: 'naive_bayes')

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Windows
type logs\spam_classifier.log

# Mac/Linux
cat logs/spam_classifier.log
```

**Log entries include:**
- Authentication status
- Number of emails processed
- Classification results
- Errors and exceptions

---

## 🧪 Testing Your Setup

### Quick Test Checklist

✅ **Gmail API Setup**
- [ ] credentials.json downloaded
- [ ] Gmail API enabled in Google Cloud
- [ ] OAuth consent screen configured

✅ **Authentication**
- [ ] First run opens browser
- [ ] Successfully authenticates
- [ ] token.json created

✅ **Model Training**
- [ ] Training data prepared
- [ ] Model trained successfully
- [ ] spam_classifier.pkl exists

✅ **Classification**
- [ ] Can fetch emails
- [ ] Classification working
- [ ] Spam emails detected

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. "Credentials not found"**
- Check `config/credentials.json` exists
- Verify it's from Google Cloud Console

**3. "Insufficient permissions"**
- Re-authenticate: Delete `token.json` and run again
- Check OAuth consent screen in Google Cloud

**4. "Model not found"**
```bash
python models/trainer.py
```

**5. "High false positives"**
- Increase `CONFIDENCE_THRESHOLD` in config
- Retrain with more data
- Use SVM instead of Naive Bayes

---

## 🔒 Security Best Practices

1. **Never commit credentials.json to Git**
   - Add to `.gitignore`
   - Use environment variables in production

2. **Protect your token.json**
   - Keep it secure
   - Don't share with others

3. **Review permissions regularly**
   - Check in Google Cloud Console
   - Revoke if compromised

---

## 📈 Next Steps & Improvements

After basic implementation works:

1. **Better Model**
   - Try different algorithms (SVM, Random Forest)
   - Use pre-trained embeddings (Word2Vec, BERT)
   - Fine-tune hyperparameters

2. **User Interface**
   - Create a web dashboard
   - Show statistics and trends
   - Manual override controls

3. **Personalization**
   - Learn from user feedback
   - Adapt to your specific spam patterns
   - Whitelist/blacklist features

4. **Advanced Features**
   - Real-time email monitoring
   - Email categorization (not just spam/ham)
   - Summary reports

---

## 📚 Resources

- **Gmail API Documentation**: https://developers.google.com/gmail/api
- **Google Auth Guide**: https://google-auth.readthedocs.io/
- **scikit-learn Docs**: https://scikit-learn.org/
- **NLTK Tutorial**: https://www.nltk.org/book/

---

## ✅ Success Criteria

Your implementation is successful when:
- ✅ Program runs without errors
- ✅ Authenticates with Gmail successfully
- ✅ Fetches emails from inbox
- ✅ Classifies emails accurately (>85% accuracy)
- ✅ Moves spam emails to spam folder
- ✅ Runs automatically every 6 hours
- ✅ Logs all activities

---

**Ready to start coding? Follow the code implementation step by step!**

