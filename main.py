from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import joblib
import pandas as pd
from app.link_checker import analyze_links
import os

app = FastAPI(
    title="MailShield AI",
    description="An API to detect phishing emails using Isolation Forest and link heuristics",
    version="1.0.0"
)

# Load model and vectorizer
MODEL_PATH = os.path.join("models", "isolation_forest_model.pkl")
VECTORIZER_PATH = os.path.join("models", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


class EmailInput(BaseModel):
    subject: str
    body: str


@app.get("/")
def welcome():
    return {"message": "Welcome to MailShield AI - Phishing Email Detection API"}


@app.post("/predict")
def predict_phishing(email: EmailInput):
    try:
        # Step 1: Extract and analyze links from body
        link_features = analyze_links(email.body)  # Dict of heuristic link features

        # Step 2: Vectorize text
        email_text = email.subject + " " + email.body
        text_vector = vectorizer.transform([email_text])

        # Step 3: Combine features
        input_df = pd.DataFrame(text_vector.toarray())
        for key, value in link_features.items():
            input_df[key] = value

        # Step 4: Make prediction
        prediction = model.predict(input_df)[0]
        result = "Phishing" if prediction == -1 else "Safe"

        return {
            "prediction": result,
            "link_analysis": link_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
