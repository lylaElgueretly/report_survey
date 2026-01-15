# survey_app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===============================
# 1. COLUMN DEFINITIONS
# ===============================
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

# ===============================
# 2. DATA PERSISTENCE
# ===============================
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

        # Save to daily backup
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

        # Save to JSON backup
        json_file = f"backups/survey_{timestamp.replace(':','-').replace(' ','_')}.json"
        try:
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass

        st.session_state.last_submission = {
            'time': timestamp,
            'id': data['submission_id'],
            'name': data.get('name', 'Anonymous'),
            'success': master_success
        }

        return master_success

# ===============================
# 3. EMAIL FUNCTION
# ===============================
def send_email(submission):
    try:
        EMAIL = st.secrets["EMAIL"]
        PASSWORD = st.secrets["EMAIL_PASSWORD"]
        recipient = EMAIL  # send to yourself

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = recipient
        msg['Subject'] = f"New Survey Submission: {submission['submission_id']}"

        body = "\n".join([f"{k}: {v}" for k, v in submission.items()])
        msg.attach(MIMEText(body, 'plain'))

        # Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email send failed: {str(e)[:100]}")
        return False

# ===============================
# 4. STREAMLIT CONFIG
# ===============================
st.set_page_config(page_title="Report Writing MVP Survey", layout="wide")
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

persistence = DataPersistence()

# ===============================
# 5. SURVEY FORM
# ===============================
st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("**Data is automatically saved with multiple backups.**")

with st.form("survey_form", clear_on_submit=True):
    name = st.text_input("Your Name (optional)")
    email = st.text_input("Email (optional)")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")
    methods = st.multiselect("Methods used:", ["Scratch","AI","School bank","Dropdown tool","Other"])
    time_scratch = st.selectbox("Time from scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    cognitive_scratch = st.selectbox("Cognitive effort from scratch:", ["High","Medium","Low","Didn't use"])
    quality_scratch = st.selectbox("Quality from scratch:", ["High","Medium","Low","Didn't use"])
    submitted = st.form_submit_button("Submit Survey")

# ===============================
# 6. SUBMISSION HANDLING
# ===============================
if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Please select at least one method")
        st.stop()

    form_data = {
        "name": name if name else "Anonymous",
        "email": email if email else "",
        "allow_contact": allow_contact,
        "methods": ", ".join(methods),
        "time_scratch": time_scratch,
        "cognitive_scratch": cognitive_scratch,
        "quality_scratch": quality_scratch
    }

    with st.spinner("Saving your feedback..."):
        success = persistence.save_submission(form_data)

    if success:
        email_sent = send_email(form_data)
        st.success("Thank you! Your survey was submitted successfully.")
        if email_sent:
            st.info("A copy of your submission was emailed to you.")
        else:
            st.warning("Submission saved, but email could not be sent.")
        st.session_state.submitted = True
        time.sleep(1)
        st.rerun()
    else:
        st.error("Submission failed. Please try again.")

# ===============================
# 7. POST-SUBMISSION VIEW
# ===============================
if st.session_state.submitted:
    st.markdown("---")
    st.write("You may close this window or submit another response.")
    if st.button("Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.last_submission = None
        st.rerun()
