# survey_app_email_csv.py
import streamlit as st
import pandas as pd
import os
import json
import time
import hashlib
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ------------------------------
# 1. COLUMN DEFINITIONS
# ------------------------------
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

# ------------------------------
# 2. DATA PERSISTENCE CLASS
# ------------------------------
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

        # Save to master CSV
        try:
            df_master = pd.read_csv(self.master_file) if os.path.exists(self.master_file) else pd.DataFrame(columns=columns)
            df_master = pd.concat([df_master, pd.DataFrame([data])], ignore_index=True)
            df_master.to_csv(self.master_file, index=False)
            master_success = True
        except Exception as e:
            master_success = False
            st.error(f"Save error: {str(e)[:100]}")

        # Daily backup CSV
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
        json_file = f"backups/survey_{timestamp.replace(':', '-')}.json"
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

# ------------------------------
# 3. STREAMLIT APP CONFIG
# ------------------------------
st.set_page_config(
    page_title="Report Writing MVP Survey",
    layout="wide"
)

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

persistence = DataPersistence()

# ------------------------------
# 4. SURVEY FORM
# ------------------------------
st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. Responses are saved locally and emailed to the admin.")

with st.form("survey_form", clear_on_submit=True):
    st.header("Your Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name (optional)")
    with col2:
        email = st.text_input("Email (optional)")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")

    st.header("Methods You've Used")
    methods = st.multiselect(
        "Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
         "Previous year's comments", "Dropdown tool", "Other"]
    )

    st.header("Time Efficiency")
    col1, col2, col3, col4 = st.columns(4)
    with col1: time_scratch = st.selectbox("From scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    with col2: time_ai = st.selectbox("AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    with col3: time_school_bank = st.selectbox("School banks:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    with col4: time_dropdown = st.selectbox("Dropdown tool:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])

    st.header("Mental Effort")
    col1, col2, col3 = st.columns(3)
    with col1: cognitive_scratch = st.selectbox("From scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
    with col2: cognitive_ai = st.selectbox("AI prompts:", ["Exhausting","High","Moderate","Low","Didn't use"])
    with col3: cognitive_dropdown = st.selectbox("Dropdown tool:", ["Very low","Low","Moderate","High","Didn't use"])

    st.header("Output Quality")
    col1, col2, col3 = st.columns(3)
    with col1: quality_scratch = st.selectbox("From scratch:", ["High quality", "Moderate", "Low", "Didn't use"])
    with col2: quality_ai = st.selectbox("AI prompts:", ["High quality", "Moderate", "Low", "Didn't use"])
    with col3: quality_dropdown = st.selectbox("Dropdown tool:", ["High quality", "Moderate", "Low", "Didn't use"])

    st.header("Open Feedback")
    open_feedback_ai = st.text_area("One thing AI does WRONG:", height=80)
    open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:", height=80)
    suggestions = st.text_area("Suggestions for improvement:", height=80)

    submitted = st.form_submit_button("Submit Survey")

# ------------------------------
# 5. HANDLE SUBMISSION
# ------------------------------
if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Select at least one method.")
        st.stop()

    form_data = {
        "name": name or "Anonymous",
        "email": email or "",
        "allow_contact": allow_contact,
        "methods": ", ".join(methods),
        "time_scratch": time_scratch,
        "time_ai": time_ai,
        "time_school_bank": time_school_bank,
        "time_dropdown": time_dropdown,
        "cognitive_scratch": cognitive_scratch,
        "cognitive_ai": cognitive_ai,
        "cognitive_dropdown": cognitive_dropdown,
        "quality_scratch": quality_scratch,
        "quality_ai": quality_ai,
        "quality_dropdown": quality_dropdown,
        "open_feedback_ai": open_feedback_ai,
        "open_feedback_tool": open_feedback_tool,
        "suggestions": suggestions
    }

    with st.spinner("Saving your feedback..."):
        success = persistence.save_submission(form_data)

    if success:
        st.success("Thank you! Your submission was saved.")

        # ------------------------------
        # 6. EMAIL WITH CSV ATTACHMENT
        # ------------------------------
        try:
            EMAIL = st.secrets["EMAIL"]
            EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
            EMAIL_RECEIVER = st.secrets.get("EMAIL_RECEIVER", EMAIL)

            msg = MIMEMultipart()
            msg['From'] = EMAIL
            msg['To'] = EMAIL_RECEIVER
            msg['Subject'] = f"New Survey Submission {st.session_state.last_submission['id']}"
            body = f"New survey submitted by {name or 'Anonymous'} ({email})."
            msg.attach(MIMEText(body, 'plain'))

            # Attach the CSV
            with open(persistence.master_file, "rb") as f:
                part = MIMEApplication(f.read(), Name="survey_data_master.csv")
            part['Content-Disposition'] = 'attachment; filename="survey_data_master.csv"'
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            st.success("Email sent with CSV attached!")
        except Exception as e:
            st.error(f"Email failed: {str(e)}")

        st.session_state.submitted = True
        time.sleep(1)
        st.experimental_rerun()
