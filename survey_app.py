# survey_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import json
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================
# 1. COLUMNS DEFINITION
# =========================
columns = [
    "submission_id", "name", "email", "allow_contact", "methods",
    "time_scratch", "time_ai", "time_school_bank", "time_dropdown",
    "cognitive_scratch", "cognitive_ai", "cognitive_dropdown",
    "quality_scratch", "quality_ai", "quality_dropdown",
    "character_accuracy_scratch", "character_accuracy_ai", "character_accuracy_dropdown",
    "curriculum_alignment_scratch", "curriculum_alignment_ai", "curriculum_alignment_dropdown",
    "stress_scratch", "stress_ai", "stress_dropdown",
    "biggest_cognitive_relief", "biggest_time_quality", "time_saved",
    "open_feedback_ai", "open_feedback_tool", "suggestions",
    "timestamp"
]

# =========================
# 2. DATA PERSISTENCE CLASS
# =========================
class DataPersistence:
    def __init__(self):
        self.submission_count = 0
        os.makedirs("data", exist_ok=True)
        os.makedirs("backups", exist_ok=True)
        os.makedirs("daily_backups", exist_ok=True)
        self.master_file = "data/survey_data_master.csv"
        if not os.path.exists(self.master_file):
            pd.DataFrame(columns=columns).to_csv(self.master_file, index=False)
        else:
            try:
                df = pd.read_csv(self.master_file)
                self.submission_count = len(df)
            except:
                self.submission_count = 0

    def save_submission(self, data):
        self.submission_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['timestamp'] = timestamp
        data['submission_id'] = hashlib.md5(f"{timestamp}{data.get('email','')}".encode()).hexdigest()[:8]

        # Save master CSV
        try:
            df_master = pd.read_csv(self.master_file) if os.path.exists(self.master_file) else pd.DataFrame(columns=columns)
            df_master = pd.concat([df_master, pd.DataFrame([data])], ignore_index=True)
            df_master.to_csv(self.master_file, index=False)
            master_success = True
        except Exception as e:
            master_success = False
            st.error(f"Save error: {str(e)[:100]}")

        # Daily backup
        date_str = datetime.now().strftime("%Y-%m-%d")
        daily_file = f"daily_backups/survey_{date_str}.csv"
        try:
            if os.path.exists(daily_file):
                df_daily = pd.read_csv(daily_file)
                df_daily = pd.concat([df_daily, pd.DataFrame([data])], ignore_index=True)
            else:
                df_daily = pd.DataFrame([data])
            df_daily.to_csv(daily_file, index=False)
        except:
            pass

        # JSON backup
        json_file = f"backups/survey_{timestamp.replace(':','-').replace(' ','_')}.json"
        try:
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except:
            pass

        st.session_state.last_submission = {
            'time': timestamp,
            'id': data['submission_id'],
            'name': data.get('name', 'Anonymous'),
            'success': master_success
        }
        return master_success

# =========================
# 3. SEND EMAIL FUNCTION
# =========================
def send_email(data):
    try:
        EMAIL = st.secrets["EMAIL"]
        PASSWORD = st.secrets["EMAIL_PASSWORD"]
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        msg['Subject'] = f"New Survey Submission: {data['submission_id']}"

        # Body with survey data
        body = "\n".join([f"{k}: {v}" for k, v in data.items()])
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email failed: {str(e)[:100]}")
        return False

# =========================
# 4. STREAMLIT APP CONFIGURATION
# =========================
st.set_page_config(
    page_title="Report Writing MVP Survey",
    layout="wide"
)

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

@st.cache_resource
def init_persistence():
    return DataPersistence()

persistence = init_persistence()

# =========================
# 5. SURVEY FORM
# =========================
st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("**Data is automatically saved with multiple backups.**")

with st.form("survey_form", clear_on_submit=True):
    name = st.text_input("Your Name (optional)")
    email = st.text_input("Email (optional)")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")
    methods = st.multiselect(
        "Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks",
         "Previous year's comments", "Dropdown tool", "Other"]
    )
    time_scratch = st.selectbox("Time from scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_ai = st.selectbox("Time AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    cognitive_scratch = st.selectbox("Cognitive effort from scratch:", ["High","Medium","Low","Didn't use"])
    cognitive_ai = st.selectbox("Cognitive effort AI:", ["High","Medium","Low","Didn't use"])
    suggestions = st.text_area("Suggestions for improvement:", height=80)

    submitted = st.form_submit_button("Submit Survey")

# =========================
# 6. HANDLE SUBMISSION
# =========================
if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Please select at least one method used")
        st.stop()
    
    form_data = {
        "name": name if name else "Anonymous",
        "email": email if email else "",
        "allow_contact": allow_contact,
        "methods": ", ".join(methods),
        "time_scratch": time_scratch,
        "time_ai": time_ai,
        "cognitive_scratch": cognitive_scratch,
        "cognitive_ai": cognitive_ai,
        "suggestions": suggestions
    }

    success = persistence.save_submission(form_data)

    # Send email
    email_success = send_email(form_data)

    if success and email_success:
        st.success("✅ Thank you! Your survey was submitted and emailed successfully.")
    elif success:
        st.warning("✅ Survey saved, but email could not be sent.")
    else:
        st.error("❌ Failed to save your survey. Please try again.")

    st.session_state.submitted = True
