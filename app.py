import streamlit as st
import joblib
import os
from app.link_checker import count_links
# Optional: import urgency analyzer if implemented
try:
    from app.urgency_analyzer import check_urgency
    URGENCY_AVAILABLE = True
except ImportError:
    URGENCY_AVAILABLE = False

# Load model and vectorizer paths
MODEL_PATH = "models/isolation_forest_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

# Load model
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error("🚨 Model file not found!")
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

# UI
st.set_page_config(page_title="📧 MailShield-AI", layout="centered")
st.title("📧 MailShield-AI: Email Phishing Detection")
st.markdown("Protect yourself from email-based phishing attacks using AI.")

# Input
subject = st.text_input("Subject", "")
body = st.text_area("Email Body", "", height=200)

if st.button("🚀 Analyze Email"):
    if model is None:
        st.error("❌ Model could not be loaded.")
    elif not subject and not body:
        st.warning("Please enter either a subject or body.")
    else:
        text = subject + " " + body
        prediction = model.predict([text])[0]
        result = "🔐 Legitimate" if prediction == 1 else "⚠️ Phishing"

        st.subheader("📊 Prediction Result:")
        st.success(f"Result: **{result}**")

        # Show optional features
        st.subheader("📌 Feature Breakdown:")
        st.markdown(f"- **Text Length**: {len(text)} characters")
        st.markdown(f"- **Link Count**: {count_links(text)}")

        # Bonus: Show urgency if analyzer available
        if URGENCY_AVAILABLE:
            urgency = check_urgency(text)
            st.markdown(f"- **Urgency Level**: {urgency}")

# Footer
st.markdown("---")



