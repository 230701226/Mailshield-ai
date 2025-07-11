import streamlit as st
import joblib
import os
import re
import numpy as np
import pandas as pd

# === Custom Feature Utilities === #
def check_urgency(text):
    urgent_keywords = ['urgent', 'immediately', 'asap', 'action required', 'important', 'response needed']
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in urgent_keywords)

def extract_email_headers(email_text):
    headers = {}
    for line in email_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

# === Load Model === #
MODEL_PATH = "models/isolation_forest_model.pkl"
model = joblib.load(MODEL_PATH)

# === Streamlit UI === #
st.set_page_config(page_title="MailShield-AI", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #008080;'>📧 MailShield-AI: Phishing Email Detection</h1>
    """, unsafe_allow_html=True
)

st.markdown("---")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 Enter Email Content Below")
    subject = st.text_input("✉️ Subject")
    body = st.text_area("📝 Email Body", height=250)

    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing..."):
        # ... earlier logic
            features = vectorizer.transform([input_text])
            prediction = model.predict(features)

            if prediction[0] == 1:
                st.markdown("### 🛑 **Prediction: Phishing** ❌", unsafe_allow_html=True)
            else:
                st.markdown("### ✅ **Prediction: Legitimate** ✅", unsafe_allow_html=True)
        # Urgency
        urgent = check_urgency(full_text)
        urgency_note = "⚠️ Urgent Language Detected" if urgent else "✅ No Urgency Detected"
        urgency_color = "orange" if urgent else "gray"
        st.markdown(f"<h4 style='color: {urgency_color};'>{urgency_note}</h4>", unsafe_allow_html=True)

with col2:
    st.subheader("📌 Email Header Insights (Optional)")
    raw_headers = st.text_area("Paste full raw headers here", height=250)
    if raw_headers:
        headers = extract_email_headers(raw_headers)
        if headers:
            st.write("Parsed Headers:")
            st.json(headers)
        else:
            st.warning("⚠️ Could not parse headers properly.")

st.markdown("---")
st.markdown(
    "<small>🚀 Powered by Isolation Forest, TF-IDF, and Custom Feature Extractors | Streamlit App</small>",
    unsafe_allow_html=True
)
