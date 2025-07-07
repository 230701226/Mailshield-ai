import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

# Load email data (make sure subject and body columns exist)
df = pd.read_csv("../data/known_emails.csv")  # relative path from training/

# Combine subject and body
df['text'] = df['subject'] + " " + df['body']

# Initialize and fit TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(df['text'])

# Create models directory if not present
os.makedirs("../models", exist_ok=True)

# Save vectorizer
joblib.dump(vectorizer, "../models/tfidf_vectorizer.pkl")
print("✅ TF-IDF vectorizer saved to models/tfidf_vectorizer.pkl")
