import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Paths
MODEL_PATH = "models/isolation_forest_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
DATA_PATH = "data/Updated_MailShield_Email_Dataset.csv"

# Load dataset
print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Debug print to check actual column names
print("🧾 Available Columns:", df.columns)

# Try auto-detect subject/body/label column names (case-insensitive)
subject_col = next((col for col in df.columns if col.lower() == "subject"), None)
body_col = next((col for col in df.columns if col.lower() == "body"), None)
label_col = next((col for col in df.columns if col.lower() == "label"), None)

if not all([subject_col, body_col, label_col]):
    raise ValueError("❌ Required columns ('Subject', 'Body', 'label') not found. Found: " + ", ".join(df.columns))

# Remove rows where label is NaN
df = df.dropna(subset=[label_col])

# Clean missing values in text
df[subject_col] = df[subject_col].fillna("")
df[body_col] = df[body_col].fillna("")

# Combine text
df["text"] = df[subject_col] + " " + df[body_col]

# Encode labels
df["label"] = df[label_col].str.lower().map({"legitimate": 0, "phishing": 1})

# Remove rows with invalid labels (still NaN after mapping)
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

# Vectorize text
print("🔠 Vectorizing text...")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Train model
print("🧠 Training Random Forest model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and vectorizer
print("💾 Saving model and vectorizer...")
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("✅ Training complete. Model saved.")
