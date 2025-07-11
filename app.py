import streamlit as st
import joblib
import os
import sys

# Safe dynamic import
try:
    from app.urgency_keywords import check_urgency
except ImportError:
    def check_urgency(text):
        return "⚠️ Urgency check unavailable."

MODEL_PATH = "models/isolation_forest_model.pkl"

st.title("📧 MailShield AI – Email Phishing Detector")
input_text = st.text_area("Paste an email message here:")

if st.button("Analyze Email"):
    if not input_text.strip():
        st.warning("Please enter some email text.")
    else:
        try:
            model = joblib.load(MODEL_PATH)
            prediction = model.predict([input_text])[0]
            label = "Phishing" if prediction == -1 else "Legitimate"
            st.success(f"🛡️ Prediction: **{label}**")
        except Exception as e:
            st.error(f"❌ Failed to load model: {e}")
        
        # Bonus check
        urgency = check_urgency(input_text)
        st.info(f"Urgency Score: {urgency}")
