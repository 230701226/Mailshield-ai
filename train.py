# train.py

import os
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from custom_features import TextLengthExtractor, LinkCountExtractor


DATA_PATH = 'data/Updated_MailShield_Email_Dataset.csv'
MODEL_PATH = 'models/isolation_forest_model.pkl'
VECTORIZER_PATH = 'models/vectorizer.pkl'

os.makedirs('models', exist_ok=True)

# Custom transformer to extract features from raw email text
class TextStatsExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Example numeric features extracted from text
        df = pd.DataFrame()
        df['text_length'] = X['email_text'].apply(len)
        df['num_links'] = X['email_text'].str.count(r'http')
        return df

def main():
    print("📥 Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    if 'email_text' not in df.columns:
        raise ValueError("⚠️ Column 'email_text' not found in dataset")

    print("🔢 Extracting features...")
    # TF-IDF for email_text
    tfidf = TfidfVectorizer(max_features=500)

    # Additional custom features
    stats_extractor = TextStatsExtractor()

    # Combine both into a single pipeline
    combined = ColumnTransformer(
        transformers=[
            ('tfidf', tfidf, 'email_text'),
            ('stats', stats_extractor, ['email_text'])
        ]
    )

    pipeline = Pipeline([
        ('features', combined),
        ('model', IsolationForest(contamination=0.1, random_state=42))
    ])

    print("⚙️ Training model...")
    pipeline.fit(df)

    print("💾 Saving entire pipeline...")
    joblib.dump(pipeline, MODEL_PATH)
    print(f"✅ Full model pipeline saved to {MODEL_PATH}")

    print("💾 Saving vectorizer separately (optional)...")
    joblib.dump(tfidf, VECTORIZER_PATH)
    print(f"✅ TF-IDF Vectorizer saved to {VECTORIZER_PATH}")

if __name__ == "__main__":
    main()
