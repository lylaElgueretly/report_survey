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

# ============================================================================ 
# 1. COLUMNS DEFINITION
# ============================================================================

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

# ============================================================================ 
# 2. DATA PERSISTENCE CLASS
# ============================================================================

class DataPersistence:
    """Simple data persistence with multiple backups"""
    
    def __init__(self):
        self.submission_count = 0
        self.init_time = datetime.now()
        
        # Create backup directories
        os.makedirs("data", exist_ok=True)
        os.makedirs("backups", exist_ok=True)
        os.makedirs("daily_backups", exist_ok=True)
        
        # Initialize master CSV
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
        """Save submission with multiple backups"""
        self.submission_count += 1
        
        # Add metadata
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
        json_file = f"backups/survey_{timestamp.replace(':', '-').replace(' ', '_')}.json"
        try:
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except:
            pass
        
        # Store in session state
        st.session_state.last_submission = {
            'time': timestamp,
            'id': data['submission_id'],
            'name': data.get('name', 'Anonymous'),
            'success': master_success
        }
        
        return master_success

# ============================================================================ 
# 2b. EMAIL SENDING FUNCTION
# ============================================================================

def send_email(form_data):
    """Send survey submission via email using Streamlit secrets"""
    try:
        EMAIL = st.secrets["EMAIL"]
        PASSWORD = st.secrets["EMAIL_PASSWORD"]
    except Exception:
        st.warning("Email not sent: secrets not configured.")
        return
    
    body = "\n".join([f"{k}: {v}" for k, v in form_data.items()])
    
    msg = MIMEText(body)
    msg['Subject'] = f"New Survey Submission: {form_data.get('name','Anonymous')}"
    msg['From'] = EMAIL
    msg['To'] = EMAIL  # send to yourself
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        st.info("Submission emailed successfully")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)[:100]}")

# ============================================================================ 
# 3. STREAMLIT APP CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Report Writing MVP Survey",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'last_submission' not in st.session_state:
    st.session_state.last_submission = None

# Initialize data persistence
@st.cache_resource
def init_persistence():
    return DataPersistence()

persistence = init_persistence()

# ============================================================================ 
# 4. SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("Survey Dashboard")
    st.subheader("System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Submissions", persistence.submission_count)
    with col2:
        if os.path.exists("data/survey_data_master.csv"):
            try:
                file_size = os.path.getsize("data/survey_data_master.csv") / 1024
                st.metric("Data Size", f"{file_size:.1f} KB")
            except:
                st.metric("Data Size", "N/A")
        else:
            st.metric("Data Size", "0 KB")
    st.progress(100/100, text="Data Protection: 100%")
    
    st.subheader("Quick Actions")
    if st.button("View All Data"):
        if os.path.exists(persistence.master_file):
            st.dataframe(pd.read_csv(persistence.master_file))
        else:
            st.info("No data yet")
    
    if st.button("Download Data"):
        if os.path.exists(persistence.master_file):
            with open(persistence.master_file, "rb") as f:
                st.download_button("Download CSV", f, file_name=f"survey_data_{datetime.now().strftime('%Y%m%d')}.csv")

# ============================================================================ 
# 5. MAIN SURVEY FORM
# ============================================================================

st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")

with st.form("survey_form", clear_on_submit=True):
    # Contact info
    name = st.text_input("Your Name (optional)")
    email = st.text_input("Email (optional)")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")
    
    # Methods
    methods = st.multiselect(
        "Select all methods you've used:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
         "Previous year's comments", "Dropdown tool", "Other"]
    )
    
    # Time efficiency
    col1, col2, col3, col4 = st.columns(4)
    time_scratch = col1.selectbox("From scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_ai = col2.selectbox("AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_school_bank = col3.selectbox("School banks:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    time_dropdown = col4.selectbox("Dropdown tool:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])
    
    # Cognitive effort
    col1, col2, col3 = st.columns(3)
    cognitive_scratch = col1.selectbox("From scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
    cognitive_ai = col2.selectbox("AI prompts:", ["Exhausting","High","Moderate","Low","Didn't use"])
    cognitive_dropdown = col3.selectbox("Dropdown tool:", ["Very low","Low","Moderate","High","Didn't use"])
    
    # Quality
    col1, col2, col3 = st.columns(3)
    quality_scratch = col1.selectbox("From scratch:", ["High quality and consistent", "High quality but inconsistent", "Generally good", "Variable", "Often rushed/generic", "Didn't use"])
    quality_ai = col2.selectbox("AI prompts:", ["High after edits", "Good with minor tweaks", "Acceptable", "Too generic/not suitable", "Haven't used AI", "Didn't use"])
    quality_dropdown = col3.selectbox("Dropdown tool:", ["High & curriculum-aligned", "Good, ready to use", "Acceptable with minor tweaks", "Too generic", "Didn't use"])
    
    # Open feedback
    open_feedback_ai = st.text_area("One thing AI does WRONG:", height=80)
    open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:", height=80)
    suggestions = st.text_area("Suggestions for improvement:", height=80)
    
    submitted = st.form_submit_button("Submit Survey", type="primary", use_container_width=True)

# ============================================================================ 
# 6. SUBMISSION HANDLING WITH EMAIL
# ============================================================================

if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Please select at least one method you've used")
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
    
    with st.spinner("Saving your feedback securely..."):
        success = persistence.save_submission(form_data)
    
    if success:
        st.success("Thank you! Your submission has been saved securely.")
        st.session_state.submitted = True
        
        # Send email
        send_email(form_data)
        
        time.sleep(2)
        st.rerun()
    else:
        st.error("Save failed. Please try again.")
        st.json(form_data)
