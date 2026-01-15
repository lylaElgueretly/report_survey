# clean_survey_app.py
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
    except Exception as e:
        st.warning("Email not sent: secrets not configured.")
        return
    
    body = "\n".join([f"{k}: {v}" for k, v in form_data.items()])
    
    msg = MIMEText(body)
    msg['Subject'] = f"New Survey
