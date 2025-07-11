# ✅ app.py error-proof version with all potential fixes
import streamlit as st
import joblib
import os
import sys
import re

# 📦 Add app/ to path for dynamic imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

# 🔒 Safe imports with fallbacks
try:
    from urgency_keywords import check_urgency
except ImportError:
    def check_urgency(text):
        return "(Urgency check unavailable)"

try:
    from header_parser import inspect_headers
except ImportError:
    def inspect_headers(text):
        return "(Header inspection not available)"

try:
    from link_checker import analyze_links
except ImportError:
    def analyze_links(text):
        return "(Link analysis unavailable)"

try:
    from ai_style_checker import detect_ai_signature
except ImportError:
    def detect_ai_signature(text):
        return "(AI style detection unavailable)"

# 📂 Load model and vectorizer paths
MODEL_PATH = "models/isolation_forest_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

# 🔐 Load model with error handling
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"❌ Model loading failed: {e}")
    model = None

# 🎨 Streamlit App UI
st.set_page_config(page_title="📧 MailShield-AI", layout="centered")
st.title("📧 MailShield-AI: Email Phishing Detection")
st.markdown("""
Enter an email content below and we will analyze whether it's **phishing** or **legitimate**, along with helpful breakdowns.
""")

email_text = st.text_area("✉️ Paste Email Content Here:", height=200)

if st.button("🔍 Analyze Email"):
    if not email_text.strip():
        st.warning("⚠️ Please enter email content first.")
    elif model is None:
        st.error("❌ Model not available. Please check deployment.")
    else:
        # 📊 Prediction
        prediction = model.predict([email_text])[0]
        result = "🛑 Phishing Detected" if prediction == -1 else "✅ Legitimate Email"
        st.subheader("🔎 Result:")
        st.success(result) if prediction != -1 else st.error(result)

        # 🧠 Feature Breakdowns
        with st.expander("🧠 Breakdown & Insights"):
            st.write("🔗 Link Analysis:", analyze_links(email_text))
            st.write("🚨 Urgency Check:", check_urgency(email_text))
            st.write("🔍 Header Inspection:", inspect_headers(email_text))
            st.write("🤖 AI-Writing Style:", detect_ai_signature(email_text))

        # 🔢 Debug score (optional)
        with st.expander("📈 Raw Feature Score (Debug)"):
            try:
                scores = model.decision_function([email_text])
                st.code(f"Anomaly Score: {scores[0]:.4f}")
            except Exception as e:
                st.warning(f"(Score unavailable: {e})")

