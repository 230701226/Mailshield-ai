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

# Step 1: Load dataset
print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Step 2: Combine subject + body into a single text column
df["Subject"] = df["Subject"].fillna("")
df["Body"] = df["Body"].fillna("")
df["text"] = df["Subject"] + " " + df["Body"]

# Step 3: Encode labels (legitimate=0, phishing=1)
df["label"] = df["label"].map({"legitimate": 0, "phishing": 1})

# Step 4: TF-IDF vectorization
print("🔠 Vectorizing text...")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Step 5: Split and train the model
print("🧠 Training Random Forest model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Save model and vectorizer
print("💾 Saving model and vectorizer...")
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("✅ Training complete. Model saved to:")
print("   →", MODEL_PATH)
print("   →", VECTORIZER_PATH)
