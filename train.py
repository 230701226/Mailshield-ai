
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from app.feature_extractors import TextLengthExtractor, LinkCountExtractor


# Load dataset
print("📥 Loading dataset...")
df = pd.read_csv("emails.csv")  # Update if your dataset file is named differently

df.columns = df.columns.str.lower()
print("🧾 Available Columns:", df.columns)

df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")
df = df.dropna(subset=["label"])

def combine_text_features(X):
    return X["subject"] + " " + X["body"]

text_features = ["subject", "body"]

text_transformer = Pipeline(steps=[
    ("combine", FunctionTransformer(combine_text_features, validate=False)),
    ("tfidf", TfidfVectorizer(stop_words="english"))
])

preprocessor = ColumnTransformer(transformers=[
    ("text", text_transformer, text_features)
])

X = df[text_features]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

print("🔠 Vectorizing text...")
print("🧠 Training Random Forest model...")
model_pipeline.fit(X_train, y_train)

os.makedirs("models", exist_ok=True)
joblib.dump(model_pipeline, "models/isolation_forest_model.pkl")
print("✅ Model saved to models/isolation_forest_model.pkl")
