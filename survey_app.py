# survey_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
import json
from datetime import datetime
import hashlib
import smtplib
from email.message import EmailMessage

# ============================
# 1. STREAMLIT SECRETS
# ============================
EMAIL = st.secrets["EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
EMAIL_RECEIVER = EMAIL  # send to yourself for notifications

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
# 3. DATA PERSISTENCE
# ============================
class DataPersistence:
    """Simple data persistence with multiple backups"""
    
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
        daily_file = f"daily_backups/survey_{datetime.now().strftime('%Y-%m-%d')}.csv"
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
        
        # Store last submission
        st.session_state.last_submission = {
            'time': timestamp,
            'id': data['submission_id'],
            'name': data.get('name', 'Anonymous'),
            'success': master_success
        }
        
        return master_success

persistence = DataPersistence()

# ============================
# 4. STREAMLIT CONFIG
# ============================
st.set_page_config(
    page_title="Report Writing MVP Validation Survey",
    layout="wide"
)

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

# ============================
# 5. SIDEBAR DASHBOARD
# ============================
with st.sidebar:
    st.title("Survey Dashboard")
    st.subheader("System Status")
    col1, col2 = st.columns(2)
    col1.metric("Total Submissions", persistence.submission_count)
    col2.metric("Data Size (KB)", f"{os.path.getsize(persistence.master_file)/1024:.1f}" if os.path.exists(persistence.master_file) else "0")
    
    st.subheader("Quick Actions")
    if st.button("View All Data"):
        if os.path.exists(persistence.master_file):
            df = pd.read_csv(persistence.master_file)
            st.dataframe(df)
        else:
            st.info("No data yet")
    
    if st.button("Download Data"):
        if os.path.exists(persistence.master_file):
            with open(persistence.master_file, "rb") as f:
                st.download_button(
                    label="Download CSV",
                    data=f,
                    file_name=f"survey_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    if st.session_state.last_submission:
        st.divider()
        st.subheader("Last Submission")
        ls = st.session_state.last_submission
        st.write(f"Time: {ls['time']}")
        st.write(f"ID: {ls['id']}")
        st.write(f"Name: {ls['name']}")
        st.write(f"Status: {'Saved' if ls['success'] else 'Failed'}")

# ============================
# 6. MAIN SURVEY FORM
# ============================
st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("**Data is automatically saved with multiple backups.**")

with st.form("survey_form", clear_on_submit=True):
    st.header("Your Information")
    col1, col2 = st.columns(2)
    name = col1.text_input("Your Name (optional)")
    email = col2.text_input("Email (optional)")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")
    
    st.header("Methods Used")
    methods = st.multiselect("Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", "Previous year's comments", "Dropdown tool", "Other"])
    
    st.header("Time Efficiency")
    col1, col2, col3, col4 = st.columns(4)
    time_scratch = col1.selectbox("From scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_ai = col2.selectbox("AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_school_bank = col3.selectbox("School banks:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_dropdown = col4.selectbox("Dropdown tool:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])
    
    st.header("Mental Effort")
    col1, col2, col3 = st.columns(3)
    cognitive_scratch = col1.selectbox("From scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
    cognitive_ai = col2.selectbox("AI prompts:", ["Exhausting","High","Moderate","Low","Didn't use"])
    cognitive_dropdown = col3.selectbox("Dropdown tool:", ["Very low","Low","Moderate","High","Didn't use"])
    
    st.header("Output Quality")
    col1, col2, col3 = st.columns(3)
    quality_scratch = col1.selectbox("From scratch:", ["High quality and consistent", "High quality but inconsistent", "Generally good", "Variable", "Often rushed/generic", "Didn't use"])
    quality_ai = col2.selectbox("AI prompts:", ["High after edits", "Good with minor tweaks", "Acceptable", "Too generic/not suitable", "Haven't used AI", "Didn't use"])
    quality_dropdown = col3.selectbox("Dropdown tool:", ["High & curriculum-aligned", "Good, ready to use", "Acceptable with minor tweaks", "Too generic", "Didn't use"])
    
    st.header("Specific Metrics")
    col1, col2, col3 = st.columns(3)
    character_accuracy_scratch = col1.radio("Character Accuracy (Scratch):", ["Within range","Exceeds range","Didn't use"])
    character_accuracy_ai = col2.radio("Character Accuracy (AI):", ["Within range","Exceeds range","Didn't use"])
    character_accuracy_dropdown = col3.radio("Character Accuracy (Dropdown):", ["Within range","Exceeds range","Didn't use"])
    
    col1, col2, col3 = st.columns(3)
    curriculum_alignment_scratch = col1.selectbox("Curriculum Alignment (Scratch):", ["Always","Usually","Sometimes","Rarely","Didn't use"])
    curriculum_alignment_ai = col2.selectbox("Curriculum Alignment (AI):", ["Always","Usually","Sometimes","Rarely","Didn't use"])
    curriculum_alignment_dropdown = col3.selectbox("Curriculum Alignment (Dropdown):", ["Always","Usually","Sometimes","Rarely","Didn't use"])
    
    col1, col2, col3 = st.columns(3)
    stress_scratch = col1.selectbox("Stress Level (Scratch):", ["Very high","High","Moderate","Low","Didn't use"])
    stress_ai = col2.selectbox("Stress Level (AI):", ["Very high","High","Moderate","Low","Didn't use"])
    stress_dropdown = col3.selectbox("Stress Level (Dropdown):", ["Very high","High","Moderate","Low","Didn't use"])
    
    st.header("Dropdown Tool Benefits")
    col1, col2, col3 = st.columns(3)
    biggest_cognitive_relief = col1.selectbox("Cognitive relief:", [
        "No need to decide what to include/exclude",
        "Character count automatically perfect",
        "No rephrasing/editing needed",
        "Curriculum-aligned language pre-written",
        "Clear structure removes blank page stress",
        "Consistency across all students",
        "Didn't use"
    ])
    biggest_time_quality = col2.selectbox("Best time-to-quality:", ["Writing from scratch","ChatGPT/AI","Dropdown tool","Other","Didn't use"])
    time_saved = col3.selectbox("Time saved for 30 students:", ["No time saved","30min-1hr","1-2hrs","2-4hrs","4-6hrs","6-8hrs","8-12hrs","12-24hrs","24+hrs","Didn't use"])
    
    st.header("Open Feedback")
    open_feedback_ai = st.text_area("One thing AI does WRONG:", height=80)
    open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:", height=80)
    suggestions = st.text_area("Suggestions for improvement:", height=80)
    
    submitted = st.form_submit_button("Submit Survey")

# ============================
# 7. FORM SUBMISSION HANDLING
# ============================
if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Please select at least one method you've used")
    else:
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
            "character_accuracy_scratch": character_accuracy_scratch,
            "character_accuracy_ai": character_accuracy_ai,
            "character_accuracy_dropdown": character_accuracy_dropdown,
            "curriculum_alignment_scratch": curriculum_alignment_scratch,
            "curriculum_alignment_ai": curriculum_alignment_ai,
            "curriculum_alignment_dropdown": curriculum_alignment_dropdown,
            "stress_scratch": stress_scratch,
            "stress_ai": stress_ai,
            "stress_dropdown": stress_dropdown,
            "biggest_cognitive_relief": biggest_cognitive_relief,
            "biggest_time_quality": biggest_time_quality,
            "time_saved": time_saved,
            "open_feedback_ai": open_feedback_ai,
            "open_feedback_tool": open_feedback_tool,
            "suggestions": suggestions
        }
        success = persistence.save_submission(form_data)
        
        # Save CSV to buffer
        csv_buffer = io.StringIO()
        df_master = pd.read_csv(persistence.master_file)
        df_master.to_csv(csv_buffer, index=False)
        
        # Send email notification with CSV
        try:
            msg = EmailMessage()
            msg["From"] = EMAIL
            msg["To"] = EMAIL_RECEIVER
            msg["Subject"] = f"New Survey Submission: {form_data['submission_id']}"
            msg.set_content("A new survey submission was received. CSV attached.")
            msg.add_attachment(csv_buffer.getvalue(), filename="survey_data.csv", subtype="csv")
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL, EMAIL_PASSWORD)
                smtp.send_message(msg)
            st.success("Survey submitted and email sent successfully!")
        except Exception as e:
            st.warning(f"Saved locally, but email failed. Error: {str(e)[:100]}")
        
        st.session_state.submitted = True

# ============================
# 8. SUBMIT ANOTHER RESPONSE
# ============================
if st.session_state.submitted:
    if st.button("Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.last_submission = None
        st.experimental_rerun()
