import streamlit as st

st.set_page_config(page_title="Survey Test")

if st.button("Test Email Secret"):
    try:
        st.write("EMAIL found:", st.secrets["EMAIL"])
        st.success("Secrets loaded correctly!")
    except KeyError:
        st.error("EMAIL not found! Check your secrets.toml on Streamlit Cloud.")

# survey_app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import hashlib

# ============================
# 0. STREAMLIT PAGE CONFIG
# ============================

st.set_page_config(
    page_title="Report Writing MVP Survey",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# 1. ACCESS SECRETS
# ============================

EMAIL = st.secrets["EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

# ============================
# 2. COLUMNS DEFINITION
# ============================

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

# ============================
# 3. DATA PERSISTENCE CLASS
# ============================

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
        except:
            master_success = False

        # Daily backup
        date_str = datetime.now().strftime("%Y-%m-%d")
        daily_file = f"daily_backups/survey_{date_str}.csv"
        try:
            df_daily = pd.read_csv(daily_file) if os.path.exists(daily_file) else pd.DataFrame(columns=columns)
            df_daily = pd.concat([df_daily, pd.DataFrame([data])], ignore_index=True)
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

# ============================
# 4. INIT SESSION STATE
# ============================

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

persistence = DataPersistence()

# ============================
# 5. EMAIL FUNCTION
# ============================

def send_email_notification(form_data):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = EMAIL
        msg['Subject'] = "New Survey Submission"

        body = "New survey submission received:\n\n"
        for key, val in form_data.items():
            body += f"{key}: {val}\n"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email failed: {str(e)}")
        return False

# ============================
# 6. SURVEY FORM
# ============================

st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("**Data is automatically saved with multiple backups.**")

with st.form("survey_form", clear_on_submit=True):
    # Basic info
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name (optional)")
    with col2:
        email = st.text_input("Email (optional)")

    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")

    # Methods used
    methods = st.multiselect(
        "Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
         "Previous year's comments", "Dropdown tool", "Other"]
    )

    # Time
    col1, col2, col3, col4 = st.columns(4)
    time_scratch = col1.selectbox("From scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_ai = col2.selectbox("AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_school_bank = col3.selectbox("School banks:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_dropdown = col4.selectbox("Dropdown tool:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])

    # Cognitive effort
    col1, col2, col3 = st.columns(3)
    cognitive_scratch = col1.selectbox("Mental effort from scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
    cognitive_ai = col2.selectbox("Mental effort AI:", ["Exhausting","High","Moderate","Low","Didn't use"])
    cognitive_dropdown = col3.selectbox("Mental effort dropdown:", ["Very low","Low","Moderate","High","Didn't use"])

    # Quality
    col1, col2, col3 = st.columns(3)
    quality_scratch = col1.selectbox("Quality scratch:", ["High","Medium","Low","Didn't use"])
    quality_ai = col2.selectbox("Quality AI:", ["High","Medium","Low","Didn't use"])
    quality_dropdown = col3.selectbox("Quality dropdown:", ["High","Medium","Low","Didn't use"])

    # Open feedback
    open_feedback_ai = st.text_area("One thing AI does WRONG:", height=80)
    open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:", height=80)
    suggestions = st.text_area("Suggestions for improvement:", height=80)

    submitted = st.form_submit_button("Submit Survey")

# ============================
# 7. HANDLE SUBMISSION
# ============================

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

    # Save to CSV + backups
    persistence.save_submission(form_data)

    # Send email notification
    email_success = send_email_notification(form_data)

    if email_success:
        st.success("Thank you! Your response has been saved and emailed successfully.")
    else:
        st.warning("Saved locally, but email failed. Check secrets and internet.")

    st.session_state.submitted = True
    time.sleep(1)
    st.experimental_rerun()

# ============================
# 8. POST-SUBMISSION VIEW
# ============================

if st.session_state.submitted:
    st.markdown("### Submission Complete! You may close this tab or submit another response.")
    if st.button("Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.last_submission = None
        st.experimental_rerun()
