# 📂 File: app.py

import streamlit as st
import requests
import json
from app.urgency_analyzer import check_urgency
from custom_features import TextLengthExtractor, LinkCountExtractor



def check_urgency(text):
    """Simple keyword-based urgency detector."""
    urgency_keywords = ['urgent', 'immediately', 'action required', 'asap', 'important', 'verify', 'now']
    score = sum(word in text.lower() for word in urgency_keywords)

    if score >= 3:
        return "🚨 High"
    elif score == 2:
        return "⚠️ Medium"
    elif score == 1:
        return "🟡 Low"
    else:
        return "🟢 None"


API_URL = "https://mailshield-backend.onrender.com/predict"  # Replace with your actual backend URL

st.set_page_config(page_title="📧 MailShield-AI", layout="wide")
st.title("📧 MailShield-AI: Email Phishing Detector")
st.markdown("""
Protect your inbox with real-time phishing detection powered by AI.
Enter the email subject and body below to check for phishing threats.
""")

# 📥 Input section with two text areas
with st.form("email_form"):
    subject = st.text_input("✉️ Subject")
    body = st.text_area("📝 Body of the Email")
    submitted = st.form_submit_button("🔍 Analyze Email")

if submitted:
    if not subject and not body:
        st.warning("⚠️ Please enter either a subject or body text.")
    else:
        with st.spinner("Analyzing email..."):
            try:
                response = requests.post(API_URL, json={"subject": subject, "body": body})
                result = response.json()

                prediction = result.get("prediction")
                urgency = check_urgency(subject + " " + body)

                # 🎯 Result display
                st.subheader("📢 Prediction Result")
                st.success(f"The email is classified as: **{prediction.upper()}**")

                st.subheader("⚡ Urgency Analysis")
                st.info(f"Urgency Level: **{urgency}**")

                # 📊 Optional: Feature Scores (if backend returns them)
                if "scores" in result:
                    st.subheader("📊 Feature Breakdown")
                    st.json(result["scores"])

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")



