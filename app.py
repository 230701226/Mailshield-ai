import streamlit as st
import joblib
import os
import pandas as pd

# --- Load Model ---
MODEL_PATH = "models/isolation_forest_model.pkl"
model = joblib.load(MODEL_PATH)

# --- Extra Security Modules (Bonus Enhancements) ---
from app.link_checker import analyze_links
from app.urgency_keywords import check_urgency
from app.header_parser import inspect_headers
from app.ai_style_checker import detect_ai_signature

# --- App Config ---
st.set_page_config(page_title="MailShield-AI", layout="wide")
st.title("📩 MailShield-AI: Phishing Detection System")
st.markdown("""
Protect your inbox from phishing threats using intelligent email analysis.
""")

# --- Input Form ---
st.subheader("📬 Analyze Incoming Email")
with st.form("email_form"):
    subject = st.text_input("Subject")
    body = st.text_area("Body", height=150)
    sender = st.text_input("From Email")
    receiver = st.text_input("To Email")
    headers = st.text_area("Headers (Optional)", height=100)
    submitted = st.form_submit_button("🔍 Analyze")

if submitted:
    full_text = f"{subject} {body}"
    pred = model.predict([full_text])[0]
    label = "🛑 Phishing" if pred == -1 else "✅ Legitimate"

    # --- Display Results ---
    st.markdown(f"### 🔎 Prediction Result: {label}")

    # --- Feature Analysis (Bonus Section) ---
    col1, col2 = st.columns(2)

    with col1:
        st.info("🔗 Link Analysis")
        links = analyze_links(body)
        st.write(links if links else "No links found.")

        st.warning("🚨 Urgency Check")
        urgency = check_urgency(subject + body)
        st.write("Urgent phrases detected." if urgency else "No urgency cues found.")

    with col2:
        st.info("📤 AI-Style Signature")
        ai_style = detect_ai_signature(body)
        st.write(ai_style)

        if headers:
            st.warning("📑 Suspicious Header Info")
            parsed = inspect_headers(headers)
            st.write(parsed)

# --- Footer ---
st.markdown("---")


