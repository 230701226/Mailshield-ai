 Internship Info
 Project: MailShield-AI: Phishing Email Detection
 Company: Codtech IT Solutions Pvt. Ltd.
 Name: POOJA AK
 Duration: 4 weeks
 Mentor: Neela santhosh

 Goal: Build a working ML-based email classifier with clear output via Streamlit.


📧 MailShield-AI: Phishing Email Detection System
MailShield-AI is a practical phishing email detection tool built during an internship at Codtech IT Solutions Pvt. Ltd.. This system classifies emails as phishing or legitimate based on their subject and body content, with an optional field for email headers.

Note: This project is deployed and works  via Streamlit.io

 Features Implemented
📝 Email Subject and Body analysis

🟡 Urgent Language Detection

✅ Phishing / Legitimate classification using Random Forest

🌐 Hosted  via Streamlit.io

📦 Simple ML pipeline built and trained manually using Python



🧪 Example Input – Tested on Streamlit.io
Subject	Body	Prediction
to ensure security of the encrypted information	Dear Customer, your account will be suspended...	✅ Legitimate (but urgent language detected)
⚠️ Update required immediately	Please click the secure link below to verify.	❌ Phishing
Welcome to our service	This is your monthly newsletter.	✅ Legitimate

✅ This interface and results were tested and captured directly on the deployed Streamlit.io app.

🖥️ Streamlit Deployment Instructions ( Method Used)
You’ve successfully deployed this using Streamlit.io Cloud.
Here’s how it was done:

🛠 How You Deployed It:
Created a GitHub repo with:

app.py (Streamlit frontend)

models/phishing_model.pkl (trained ML model)

requirements.txt

Visited https://share.streamlit.io

Chose the GitHub repo and selected app.py as entry point

Clicked Deploy

Accessed the working app on a public Streamlit.io link

output link

https://mailshield-ai-2tzwagavzkhkkzynuben8f.streamlit.app/

📸 Screenshot of working app on Streamlit:
<img width="1733" height="927" alt="Screenshot 2025-07-11 231220" src="https://github.com/user-attachments/assets/cb1df6aa-c68d-4517-87f4-c8a84d54260e" />

<img width="1738" height="847" alt="Screenshot 2025-07-11 231840" src="https://github.com/user-attachments/assets/592aa4c7-8642-410e-b0b5-23ce42ca78a9" />




📂 Folder Overview
bash
Copy
Edit
MailShield-AI/
├── app.py                  # Streamlit frontend (used for deployment)
├── models/
│   └── phishing_model.pkl  # Trained model (Random Forest)
├── train.py                # Custom model training script
├── Updated_MailShield_Email_Dataset.csv
├── requirements.txt
└── README.md               # This file



This entire project, including training and deployment, was built without any external AI APIs or advanced libraries.
The only working deployment is through Streamlit.io, and all functionality was implemented manually.
