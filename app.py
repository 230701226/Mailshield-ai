import streamlit as st
import joblib
import json

from app.link_checker import analyze_links
from app.urgency_analyzer import check_urgency
from app.ai_detector import detect_ai_signature
from app.header_inspector import inspect_headers

# Load model and vectorizer
model = joblib.load("models/isolation_forest_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

st.set_page_config(page_title="📧 MailShield AI - Phishing Detection", layout="centered")
st.title("📨 MailShield AI")
st.markdown("##### Intelligent Email Threat Detection & Analysis")

email_input = st.text_area("✉️ Paste the email content here:", height=250)

if st.button("🔍 Analyze Email"):
    if not email_input.strip():
        st.warning("Please enter some email content.")
    else:
        features = vectorizer.transform([email_input])
        score = model.decision_function(features)[0]

        # Individual Modules
        link_result = analyze_links(email_input)
        urgency_result = check_urgency(email_input)
        ai_result = detect_ai_signature(email_input)
        header_result = inspect_headers(email_input)

        # Threat Score Logic
        flags = 0
        if link_result['suspicious_links']: flags += 1
        if urgency_result['urgency_score'] > 1: flags += 1
        if ai_result['ai_signature_score'] > 0.6: flags += 1
        if header_result['impersonation_detected']: flags += 1

        threat_score = min(100, round(abs(score) * 50 + flags * 12))
        st.markdown(f"### ☣️ Threat Score: `{threat_score} / 100`")
        st.progress(threat_score / 100)

        st.subheader("🔗 Link Analysis")
        st.write(link_result)

        st.subheader("⚠️ Urgency Indicator")
        st.write(urgency_result)

        st.subheader("🤖 AI-Generated Content Detector")
        st.write(ai_result)

        st.subheader("🕵️ Email Header Analysis")
        st.write(header_result)
