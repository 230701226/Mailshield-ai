import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load email data
df = pd.read_csv("../data/known_emails.csv")
df['text'] = df['subject'] + " " + df['body']

# Fit TF-IDF vectorizer (or you can load the existing one)
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(df['text'])

# Train Isolation Forest model
model = IsolationForest(contamination=0.3, random_state=42)
model.fit(X)

# Create models directory if not present
os.makedirs("../models", exist_ok=True)

# Save model
joblib.dump(model, "../models/isolation_forest_model.pkl")
print("✅ Isolation Forest model saved to models/isolation_forest_model.pkl")
