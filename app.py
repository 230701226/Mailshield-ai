import streamlit as st
import joblib
import os
from app.link_checker import analyze_links
from app.header_parser import inspect_headers
from app.ai_style_checker import detect_ai_signature
from app.urgency_keywords import check_urgency

# Paths
MODEL_PATH = "models/isolation_forest_model.pkl"

# Load model
model = joblib.load(MODEL_PATH)

def predict_phishing(email_text):
    prediction = model.predict([email_text])[0]
    return "Phishing" if prediction == -1 else "Legitimate"

# Streamlit UI
st.set_page_config(page_title="MailShield-AI", layout="centered")
st.title("📧 MailShield-AI: Email Phishing Detection")
st.markdown("""
This app uses an Isolation Forest ML model to detect whether an email is **phishing** or **legitimate**.
""")

email_subject = st.text_input("Subject:")
email_body = st.text_area("Body:")

tabs = st.tabs(["📬 Prediction", "🧠 Features"])

if email_subject or email_body:
    email_text = email_subject + " " + email_body

    with tabs[0]:
        st.subheader("🔍 Prediction Result")
        result = predict_phishing(email_text)
        st.success(f"This email is likely: **{result}**")

        st.subheader("⚠️ Urgency Analysis")
        if check_urgency(email_text):
            st.warning("This email contains urgent-sounding phrases! Be cautious.")

    with tabs[1]:
        st.subheader("🔗 Link Analysis")
        analyze_links(email_text)

        st.subheader("🧠 AI Style Signature")
        detect_ai_signature(email_text)

        st.subheader("📥 Header Parser (Simulated)")
        inspect_headers("From: someone@example.com\nTo: you@example.com\nSubject: Hello")
else:
    st.info("Enter email subject and body to begin analysis.")



