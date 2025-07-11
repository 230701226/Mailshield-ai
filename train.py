# train.py

import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import re

# ==== Paths ====
DATA_PATH = "data/Updated_MailShield_Email_Dataset.csv"
MODEL_PATH = "models/isolation_forest_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

# ==== Custom Feature: Email Text Length ====
class TextLengthExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([[len(text)] for text in X])

class LinkCountExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([[len(re.findall(r'http[s]?://', text))] for text in X])# ==== Main training function ====
def main():
    print("📥 Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Validate required columns
    if 'subject' not in df.columns or 'body' not in df.columns or 'label' not in df.columns:
        raise ValueError("❗ Columns 'subject', 'body', or 'label' not found in dataset")

    # Combine subject and body into one text field
    df['text'] = df['subject'].fillna('') + ' ' + df['body'].fillna('')
    X = df['text']

    print("🔧 Building feature pipeline...")
    features = FeatureUnion([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('length', TextLengthExtractor()),
        ('links', LinkCountExtractor())
    ])

    print("🎯 Training model...")
    pipeline = Pipeline([
        ('features', features),
        ('clf', IsolationForest(n_estimators=100, contamination=0.1, random_state=42))
    ])

    pipeline.fit(X)

    # Save the pipeline (model + features)
    print(f"💾 Saving model to {MODEL_PATH}")
    joblib.dump(pipeline, MODEL_PATH)

    # Optionally, also save just the TF-IDF vectorizer
    tfidf = pipeline.named_steps['features'].transformer_list[0][1]
    print(f"💾 Saving TF-IDF vectorizer to {VECTORIZER_PATH}")
    joblib.dump(tfidf, VECTORIZER_PATH)

    print("✅ Training complete.")

# ==== Run ====
if __name__ == "__main__":
    main()
