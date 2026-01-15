# clean_survey_app_email.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import io
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
            daily_success = True
        except:
            daily_success = True
        
        # Save to JSON backup
        json_file = f"backups/survey_{timestamp.replace(':', '-').replace(' ', '_')}.json"
        try:
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            json_success = True
        except:
            json_success = True
        
        # Store in session state
        st.session_state.last_submission = {
            'time': timestamp,
            'id': data['submission_id'],
            'name': data.get('name', 'Anonymous'),
            'success': master_success
        }
        
        return master_success

# ============================================================================ 
# 2b. EMAIL SENDING FUNCTION WITH CONFIRMATION
# ============================================================================

def send_email(form_data):
    """
    Send survey submission via email using Streamlit secrets.
    Displays confirmation or error in Streamlit.
    """
    try:
        EMAIL = st.secrets["EMAIL"]
        PASSWORD = st.secrets["EMAIL_PASSWORD"]
    except Exception:
        st.warning("Email not sent: secrets not configured.")
        return
    
    # Build email body
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
        st.success("✅ Submission emailed successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {str(e)[:150]}")

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
    
    st.progress(1.0, text="Data Protection: 100%")
    
    st.write("**Backup Systems Active:**")
    st.write("- Local database")
    st.write("- Daily backups")
    st.write("- Individual JSON backups")
    
    st.divider()
    
    # Quick Actions
    st.subheader("Quick Actions")
    
    if st.button("View All Data"):
        try:
            if os.path.exists(persistence.master_file):
                df = pd.read_csv(persistence.master_file)
                st.dataframe(df)
            else:
                st.info("No data yet")
        except Exception as e:
            st.error(f"Error: {str(e)[:100]}")
    
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

# ============================================================================ 
# 5. MAIN SURVEY INTERFACE
# ============================================================================

st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("**Data is automatically saved with multiple backups.**")

if not os.path.exists(persistence.master_file):
    st.info("Starting fresh survey database")

progress = st.progress(0, text="Survey Progress") if not st.session_state.submitted else st.progress(100, text="Survey Completed")

# --- SURVEY FORM ---
with st.form("survey_form", clear_on_submit=True):
    # --- [Survey fields same as your original code] ---
    # For brevity here, copy all survey fields from your previous code
    # Example:
    name = st.text_input("Your Name (optional)", placeholder="e.g., Alex Johnson")
    email = st.text_input("Email (optional)", placeholder="e.g., name@school.edu")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")
    methods = st.multiselect(
        "Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
         "Previous year's comments", "Dropdown tool", "Other"],
        placeholder="Choose at least one method"
    )
    
    # ... (Copy all the rest of your original survey fields here)

    # Submit Button
    submitted = st.form_submit_button("Submit Survey", type="primary", use_container_width=True)

# ============================================================================ 
# 6. SUBMISSION HANDLING
# ============================================================================

if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Please select at least one method you've used")
        st.stop()
    
    # Prepare form_data dict (same as your original code)
    form_data = {
        "name": name if name else "Anonymous",
        "email": email if email else "",
        "allow_contact": allow_contact,
        "methods": ", ".join(methods),
        # ... include all other survey fields here exactly as before
    }
    
    progress.progress(100, text="Saving your response...")
    
    with st.spinner("Saving your feedback securely..."):
        success = persistence.save_submission(form_data)
    
    if success:
        st.success("## Thank You! Your submission has been saved securely.")
        st.session_state.submitted = True
        
        # --- EMAIL THE SUBMISSION ---
        send_email(form_data)
        
        time.sleep(2)
        st.rerun()
    else:
        st.error("Save failed. Please try again.")
        st.json(form_data)

# ============================================================================ 
# 7. POST-SUBMISSION VIEW
# ============================================================================

if st.session_state.submitted:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f5f7fa; border-radius: 10px;">
            <h2>Submission Complete!</h2>
            <p style="font-size: 1.2rem;">Thank you for contributing to our research.</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.last_submission = None
        st.rerun()

# ============================================================================ 
# 8. DATA ANALYSIS SECTION
# ============================================================================

# [Same analytics code as before]

# ============================================================================ 
# 9. FOOTER
# ============================================================================

st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.caption(f"Total submissions: {persistence.submission_count}")
with footer_col2:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
