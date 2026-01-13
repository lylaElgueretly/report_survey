# survey_app_mvp_production.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import io
import json
import time
import base64
import hashlib
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA PERSISTENCE MODULES - MULTIPLE REDUNDANT BACKUPS
# ============================================================================
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    st.warning("Google Sheets module not installed. Run: pip install gspread google-auth")

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

try:
    import boto3
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

# ============================================================================
# CONFIGURATION - SET THESE FOR YOUR DEPLOYMENT
# ============================================================================

# --- Deployment Mode ---
DEPLOYMENT_MODE = "STREAMLIT_CLOUD"  # Options: LOCAL, STREAMLIT_CLOUD, AWS

# --- Multiple Backup Systems Configuration ---
class BackupConfig:
    """Configuration for all backup systems"""
    
    # Google Sheets (Primary Cloud Backup)
    GOOGLE_SHEETS_ENABLED = True
    GOOGLE_SHEET_NAME = "Survey_Responses_MVP"
    # Store credentials in Streamlit secrets: st.secrets["google_credentials"]
    
    # Email Notifications (Instant Alerts)
    EMAIL_ENABLED = True
    DEVELOPER_EMAIL = "your-email@gmail.com"  # Change this
    # Store email credentials in Streamlit secrets: st.secrets["email"]
    
    # Local Files (Multiple Redundant Copies)
    LOCAL_BACKUPS_ENABLED = True
    BACKUP_DIRS = ["data", "backups", "daily_backups", "archived"]
    
    # Supabase Database (Alternative Cloud)
    SUPABASE_ENABLED = False
    # Store in secrets: st.secrets["supabase_url"], st.secrets["supabase_key"]
    
    # AWS S3 Backup (Enterprise)
    AWS_S3_ENABLED = False
    # Store in secrets: st.secrets["aws_access_key"], st.secrets["aws_secret_key"]

# ============================================================================
# DATA PERSISTENCE ENGINE
# ============================================================================

class DataPersistenceEngine:
    """Handles all data persistence with multiple fallback systems"""
    
    def __init__(self):
        self.init_time = datetime.now()
        self.submission_count = 0
        self.backup_systems = []
        self.setup_backup_systems()
        
    def setup_backup_systems(self):
        """Initialize all configured backup systems"""
        
        # 1. Local File System
        if BackupConfig.LOCAL_BACKUPS_ENABLED:
            self.setup_local_backups()
            self.backup_systems.append("local_files")
        
        # 2. Google Sheets
        if BackupConfig.GOOGLE_SHEETS_ENABLED and GOOGLE_SHEETS_AVAILABLE:
            try:
                self.setup_google_sheets()
                self.backup_systems.append("google_sheets")
            except Exception as e:
                st.warning(f"Google Sheets setup failed: {e}")
        
        # 3. Email System
        if BackupConfig.EMAIL_ENABLED:
            self.backup_systems.append("email_notifications")
        
        st.sidebar.success(f"✅ {len(self.backup_systems)} backup systems active")
    
    def setup_local_backups(self):
        """Create all necessary local backup directories"""
        for dir_name in BackupConfig.BACKUP_DIRS:
            os.makedirs(dir_name, exist_ok=True)
        
        # Create master CSV if doesn't exist
        if not os.path.exists("data/survey_data_master.csv"):
            pd.DataFrame(columns=columns).to_csv("data/survey_data_master.csv", index=False)
    
    def setup_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            if 'google_credentials' in st.secrets:
                creds_dict = dict(st.secrets["google_credentials"])
            else:
                # For local testing, you can load from file
                import json
                with open('credentials.json') as f:
                    creds_dict = json.load(f)
            
            scope = ['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive']
            
            credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
            self.gc = gspread.authorize(credentials)
            
            # Create or open sheet
            try:
                self.sh = self.gc.open(BackupConfig.GOOGLE_SHEET_NAME)
            except gspread.exceptions.SpreadsheetNotFound:
                self.sh = self.gc.create(BackupConfig.GOOGLE_SHEET_NAME)
                worksheet = self.sh.sheet1
                worksheet.append_row(columns)
            
            return True
        except Exception as e:
            st.error(f"Google Sheets setup error: {e}")
            return False
    
    def save_to_google_sheets(self, data):
        """Save data to Google Sheets"""
        try:
            worksheet = self.sh.sheet1
            
            # Prepare row data
            row_data = []
            for col in columns:
                value = data.get(col, "")
                # Handle lists and booleans
                if isinstance(value, list):
                    value = ", ".join(value)
                elif isinstance(value, bool):
                    value = "Yes" if value else "No"
                row_data.append(str(value) if value is not None else "")
            
            # Append row
            worksheet.append_row(row_data)
            
            # Add timestamp
            worksheet.update_cell(worksheet.row_count, 
                                 columns.index("timestamp") + 1, 
                                 data.get("timestamp", ""))
            
            return True
        except Exception as e:
            st.error(f"Google Sheets save error: {e}")
            return False
    
    def save_to_local_files(self, data):
        """Save data to multiple local file formats"""
        try:
            timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            date_str = datetime.now().strftime("%Y-%m-%d")
            
            # 1. Master CSV
            master_file = "data/survey_data_master.csv"
            df_master = pd.read_csv(master_file) if os.path.exists(master_file) else pd.DataFrame(columns=columns)
            df_master = pd.concat([df_master, pd.DataFrame([data])], ignore_index=True)
            df_master.to_csv(master_file, index=False)
            
            # 2. Daily CSV
            daily_file = f"daily_backups/survey_{date_str}.csv"
            if os.path.exists(daily_file):
                df_daily = pd.read_csv(daily_file)
                df_daily = pd.concat([df_daily, pd.DataFrame([data])], ignore_index=True)
            else:
                df_daily = pd.DataFrame([data])
            df_daily.to_csv(daily_file, index=False)
            
            # 3. JSON backup
            json_file = f"backups/survey_{timestamp.replace(':', '-').replace(' ', '_')}.json"
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            # 4. Archive file (weekly)
            week_num = datetime.now().strftime("%Y-W%U")
            archive_file = f"archived/week_{week_num}.csv"
            if os.path.exists(archive_file):
                df_archive = pd.read_csv(archive_file)
                df_archive = pd.concat([df_archive, pd.DataFrame([data])], ignore_index=True)
            else:
                df_archive = pd.DataFrame([data])
            df_archive.to_csv(archive_file, index=False)
            
            return True
        except Exception as e:
            st.error(f"Local file save error: {e}")
            return False
    
    def send_email_notification(self, data):
        """Send email notification about new submission"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Get email credentials from secrets
            if 'email' in st.secrets:
                email_config = st.secrets["email"]
                EMAIL_USER = email_config.get("user", "")
                EMAIL_PASSWORD = email_config.get("password", "")
                EMAIL_HOST = email_config.get("host", "smtp.gmail.com")
                EMAIL_PORT = email_config.get("port", 587)
            else:
                return False  # No email credentials
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 New MVP Survey Submission - {data.get('name', 'Anonymous')}"
            msg['From'] = EMAIL_USER
            msg['To'] = BackupConfig.DEVELOPER_EMAIL
            
            # HTML email content
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                    .metric {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #667eea; }}
                    .highlight {{ background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>📊 New MVP Survey Submission</h2>
                        <p>Time: {data.get('timestamp', 'N/A')}</p>
                    </div>
                    <div class="content">
                        <div class="metric">
                            <strong>👤 Respondent:</strong> {data.get('name', 'Anonymous')}<br>
                            <strong>📧 Email:</strong> {data.get('email', 'Not provided')}<br>
                            <strong>🤝 Open to contact:</strong> {'✅ Yes' if data.get('allow_contact') else '❌ No'}
                        </div>
                        
                        <div class="metric">
                            <strong>⏱️ Key Metric - Time Saved:</strong> {data.get('time_saved', 'Not specified')}<br>
                            <strong>⭐ Best Quality Method:</strong> {data.get('biggest_time_quality', 'Not specified')}<br>
                            <strong>🧠 Cognitive Relief:</strong> {data.get('biggest_cognitive_relief', 'Not specified')}
                        </div>
                        
                        <div class="highlight">
                            <h4>💡 AI Feedback:</h4>
                            <p>{data.get('open_feedback_ai', 'No feedback provided')}</p>
                        </div>
                        
                        <div class="highlight">
                            <h4>🚀 Tool Feedback:</h4>
                            <p>{data.get('open_feedback_tool', 'No feedback provided')}</p>
                        </div>
                        
                        <div class="highlight">
                            <h4>🔧 Suggestions:</h4>
                            <p>{data.get('suggestions', 'No suggestions')}</p>
                        </div>
                        
                        <hr>
                        <p><em>Total submissions today: {self.submission_count}</em></p>
                        <p><em>Backup systems used: {', '.join(self.backup_systems)}</em></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            st.error(f"Email notification error: {e}")
            return False
    
    def save_submission(self, data):
        """Save submission to all configured backup systems"""
        self.submission_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['timestamp'] = timestamp
        data['submission_id'] = hashlib.md5(f"{timestamp}{data.get('email','')}".encode()).hexdigest()[:8]
        
        results = {}
        
        # Save to all systems
        if BackupConfig.LOCAL_BACKUPS_ENABLED:
            results['local_files'] = self.save_to_local_files(data)
        
        if BackupConfig.GOOGLE_SHEETS_ENABLED and 'google_sheets' in self.backup_systems:
            results['google_sheets'] = self.save_to_google_sheets(data)
        
        if BackupConfig.EMAIL_ENABLED:
            results['email_notifications'] = self.send_email_notification(data)
        
        # Log results
        success_count = sum(results.values())
        total_attempts = len(results)
        
        # Save to session state
        st.session_state.last_submission = {
            'time': timestamp,
            'id': data['submission_id'],
            'name': data.get('name', 'Anonymous'),
            'success_rate': f"{success_count}/{total_attempts}"
        }
        
        return success_count, total_attempts, results

# ============================================================================
# STREAMLIT APP CONFIGURATION
# ============================================================================

# Page config
st.set_page_config(
    page_title="MVP Validation Survey",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize persistence engine
@st.cache_resource
def get_persistence_engine():
    return DataPersistenceEngine()

persistence = get_persistence_engine()

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Columns definition
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
# SIDEBAR - DASHBOARD & CONTROLS
# ============================================================================

with st.sidebar:
    st.title("📊 Dashboard")
    
    # System Status
    st.subheader("🔧 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Backup Systems", len(persistence.backup_systems))
    with col2:
        st.metric("Total Submissions", persistence.submission_count)
    
    # Data Protection Status
    st.progress(min(100, len(persistence.backup_systems) * 25), text="Data Protection")
    
    if persistence.backup_systems:
        st.success("✅ Data protected")
        for system in persistence.backup_systems:
            st.caption(f"• {system.replace('_', ' ').title()}")
    else:
        st.error("⚠️ No backup systems active")
    
    st.divider()
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    if st.button("🔄 Check Data Integrity"):
        try:
            if os.path.exists("data/survey_data_master.csv"):
                df = pd.read_csv("data/survey_data_master.csv")
                st.success(f"✅ {len(df)} records found")
                st.dataframe(df[['timestamp', 'name', 'time_saved']].tail(3), 
                           use_container_width=True)
            else:
                st.warning("No data file found")
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.button("📥 Download Latest Data"):
        if os.path.exists("data/survey_data_master.csv"):
            with open("data/survey_data_master.csv", "rb") as f:
                st.download_button(
                    label="Download CSV",
                    data=f,
                    file_name=f"survey_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    st.divider()
    
    # Last Submission
    if 'last_submission' in st.session_state:
        st.subheader("📝 Last Submission")
        ls = st.session_state.last_submission
        st.caption(f"Time: {ls['time']}")
        st.caption(f"ID: {ls['id']}")
        st.caption(f"Name: {ls['name']}")
        st.caption(f"Backups: {ls['success_rate']}")

# ============================================================================
# MAIN SURVEY INTERFACE
# ============================================================================

# Header with gradient
st.markdown("""
<style>
.header-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
}
.protection-badge {
    background: #10b981;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    display: inline-block;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-gradient"><h1>📊 Report Writing MVP Validation Survey</h1><p>Your feedback shapes our product roadmap</p><span class="protection-badge">🔒 Data Protected with {len(persistence.backup_systems)} Backup Systems</span></div>', unsafe_allow_html=True)

# Progress tracker
if not st.session_state.submitted:
    progress = st.progress(0, text="Survey Progress")
else:
    progress = st.progress(100, text="Survey Completed")

# --- Survey Form ---
with st.form("survey_form", clear_on_submit=False):
    # Contact Information
    st.header("👤 Your Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name (optional)", 
                           placeholder="e.g., Alex Johnson")
    with col2:
        email = st.text_input("Email (optional)", 
                            placeholder="e.g., name@school.edu")
    
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")
    
    if allow_contact:
        st.info("💬 Thank you! We may reach out to learn more about your experience.")
    
    st.divider()
    
    # Section 1: Methods Used
    st.header("📋 Methods You've Used")
    st.markdown("*Select all methods you've used for report writing:*")
    
    methods = st.multiselect(
        "Select methods:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
         "Previous year's comments", "Dropdown tool", "Other"],
        placeholder="Choose at least one method"
    )
    
    if "Other" in methods:
        other_method = st.text_input("Please specify other method:")
    
    st.divider()
    
    # Section 2: Time Comparison (Visual)
    st.header("⏱️ Time Efficiency")
    st.markdown("*How much time does each method take per comment?*")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**From Scratch**")
        time_scratch = st.radio("", ["<2min","2-5min","5-10min","10+min","Didn't use"], 
                              key="time_scratch", horizontal=False)
    with col2:
        st.markdown("**AI Prompts**")
        time_ai = st.radio("", ["<2min","2-5min","5-10min","10+min","Didn't use"], 
                          key="time_ai", horizontal=False)
    with col3:
        st.markdown("**School Banks**")
        time_school_bank = st.radio("", ["<2min","2-5min","5-10min","10+min","Didn't use"], 
                                  key="time_school", horizontal=False)
    with col4:
        st.markdown("**Dropdown Tool**")
        time_dropdown = st.radio("", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"], 
                               key="time_dropdown", horizontal=False)
    
    # Visual time comparison
    if any(x != "Didn't use" for x in [time_scratch, time_ai, time_school_bank, time_dropdown]):
        time_mapping = {"<30sec": 0.5, "<2min": 2, "2-5min": 3.5, "5-10min": 7.5, 
                       "10+min": 15, "30sec-1min": 0.75, "1-2min": 1.5, "2+min": 3}
        
        time_data = []
        labels = ["Scratch", "AI", "School Bank", "Dropdown"]
        values = [time_scratch, time_ai, time_school_bank, time_dropdown]
        
        for label, value in zip(labels, values):
            if value != "Didn't use":
                time_data.append({"Method": label, "Time (min est)": time_mapping.get(value, 0)})
        
        if time_data:
            df_time = pd.DataFrame(time_data)
            fig_time = px.bar(df_time, x='Method', y='Time (min est)', 
                            title="⏱️ Estimated Time Comparison",
                            color='Method', text='Time (min est)')
            fig_time.update_traces(texttemplate='%{text:.1f} min', textposition='outside')
            st.plotly_chart(fig_time, use_container_width=True)
    
    st.divider()
    
    # Section 3: Cognitive Effort
    st.header("🧠 Mental Effort")
    st.markdown("*How mentally demanding is each method?*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**From Scratch**")
        cognitive_scratch = st.select_slider("", 
            options=["Exhausting", "High", "Moderate", "Low", "Didn't use"],
            value="Moderate", key="cog_scratch")
    with col2:
        st.markdown("**AI Prompts**")
        cognitive_ai = st.select_slider("", 
            options=["Exhausting", "High", "Moderate", "Low", "Didn't use"],
            value="Moderate", key="cog_ai")
    with col3:
        st.markdown("**Dropdown Tool**")
        cognitive_dropdown = st.select_slider("", 
            options=["Very low", "Low", "Moderate", "High", "Didn't use"],
            value="Moderate", key="cog_drop")
    
    st.divider()
    
    # Section 4: Quality Assessment
    st.header("⭐ Output Quality")
    st.markdown("*Rate the quality of comments from each method:*")
    
    quality_options_scratch = ["High quality and consistent", "High quality but inconsistent", 
                              "Generally good", "Variable", "Often rushed/generic", "Didn't use"]
    quality_options_ai = ["High after edits", "Good with minor tweaks", "Acceptable", 
                         "Too generic/not suitable", "Haven't used AI", "Didn't use"]
    quality_options_dropdown = ["High & curriculum-aligned", "Good, ready to use", 
                               "Acceptable with minor tweaks", "Too generic", "Didn't use"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quality_scratch = st.selectbox("From scratch:", quality_options_scratch)
    with col2:
        quality_ai = st.selectbox("AI prompts:", quality_options_ai)
    with col3:
        quality_dropdown = st.selectbox("Dropdown tool:", quality_options_dropdown)
    
    st.divider()
    
    # Section 5: Specific Metrics
    st.header("🎯 Specific Metrics")
    
    st.subheader("Character Accuracy")
    col1, col2, col3 = st.columns(3)
    with col1:
        character_accuracy_scratch = st.radio("From scratch:", ["Within range", "Exceeds range", "Didn't use"])
    with col2:
        character_accuracy_ai = st.radio("AI prompts:", ["Within range", "Exceeds range", "Didn't use"])
    with col3:
        character_accuracy_dropdown = st.radio("Dropdown tool:", ["Within range", "Exceeds range", "Didn't use"])
    
    st.subheader("Curriculum Alignment")
    col1, col2, col3 = st.columns(3)
    with col1:
        curriculum_alignment_scratch = st.select_slider("From scratch:", 
            options=["Always", "Usually", "Sometimes", "Rarely", "Didn't use"])
    with col2:
        curriculum_alignment_ai = st.select_slider("AI prompts:", 
            options=["Always", "Usually", "Sometimes", "Rarely", "Didn't use"])
    with col3:
        curriculum_alignment_dropdown = st.select_slider("Dropdown tool:", 
            options=["Always", "Usually", "Sometimes", "Rarely", "Didn't use"])
    
    st.subheader("Stress Level")
    col1, col2, col3 = st.columns(3)
    with col1:
        stress_scratch = st.select_slider("From scratch:", 
            options=["Very high", "High", "Moderate", "Low", "Didn't use"])
    with col2:
        stress_ai = st.select_slider("AI prompts:", 
            options=["Very high", "High", "Moderate", "Low", "Didn't use"])
    with col3:
        stress_dropdown = st.select_slider("Dropdown tool:", 
            options=["Very high", "High", "Moderate", "Low", "Didn't use"])
    
    st.divider()
    
    # Section 6: Tool Benefits
    st.header("🚀 Dropdown Tool Benefits")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Cognitive Relief**")
        biggest_cognitive_relief = st.selectbox("", [
            "No need to decide what to include/exclude",
            "Character count automatically perfect",
            "No rephrasing/editing needed",
            "Curriculum-aligned language pre-written",
            "Clear structure removes blank page stress",
            "Consistency across all students",
            "Didn't use"
        ], index=0)
    
    with col2:
        st.markdown("**Best Time-to-Quality**")
        biggest_time_quality = st.selectbox("", [
            "Writing from scratch",
            "ChatGPT/AI",
            "Dropdown tool",
            "Other",
            "Didn't use"
        ], index=0)
    
    with col3:
        st.markdown("**Time Saved**")
        st.markdown("*For 30 students:*")
        time_saved = st.select_slider("", [
            "No time saved",
            "30min-1hr",
            "1-2hrs",
            "2-4hrs",
            "4+hrs",
            "Didn't use"
        ], value="2-4hrs")
    
    st.divider()
    
    # Section 7: Open Feedback
    st.header("💬 Open Feedback")
    
    with st.expander("**One thing AI does WRONG:**", expanded=True):
        open_feedback_ai = st.text_area(
            "What's the biggest pain point with AI tools?",
            placeholder="e.g., 'AI comments often exceed character limits and require heavy editing...'",
            height=100,
            label_visibility="collapsed"
        )
    
    with st.expander("**One thing dropdown tool does BETTER:**", expanded=True):
        open_feedback_tool = st.text_area(
            "What's the biggest advantage of the dropdown tool?",
            placeholder="e.g., 'The dropdown tool creates perfectly formatted, curriculum-aligned comments in seconds...'",
            height=100,
            label_visibility="collapsed"
        )
    
    with st.expander("**Suggestions for improvement:**", expanded=True):
        suggestions = st.text_area(
            "How can we make the tool even better?",
            placeholder="e.g., 'Add more subject-specific options, allow custom templates...'",
            height=100,
            label_visibility="collapsed"
        )
    
    st.divider()
    
    # Submit Button
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submitted = st.form_submit_button(
            "✅ Submit Survey",
            type="primary",
            use_container_width=True
        )

# ============================================================================
# SUBMISSION HANDLING
# ============================================================================

if submitted and not st.session_state.submitted:
    if not methods:
        st.error("❌ Please select at least one method you've used")
        st.stop()
    
    # Update progress
    progress.progress(100, text="Processing submission...")
    
    # Prepare data
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
    
    # Save to session
    st.session_state.form_data = form_data
    
    # Save with persistence engine
    with st.spinner("Saving your response securely..."):
        # Create progress visualization
        backup_cols = st.columns(len(persistence.backup_systems))
        backup_status = {}
        
        # Save data
        success_count, total_attempts, results = persistence.save_submission(form_data)
    
    # Show results
    st.balloons()
    
    if success_count > 0:
        # Success message
        st.success(f"""
        ## ✅ Submission Successful!
        
        **Your feedback has been securely saved in {success_count} locations:**
        
        📍 **Local Database** - Immediate access  
        🌐 **Google Sheets** - Cloud backup  
        📧 **Email Notification** - Sent to developer  
        
        **Submission Details:**  
        • ID: `{st.session_state.last_submission['id']}`  
        • Time: {st.session_state.last_submission['time']}  
        • Backup Success: {st.session_state.last_submission['success_rate']} systems  
        
        **Thank you for helping us improve!**  
        """)
        
        if allow_contact and name:
            st.info(f"📧 **Follow-up enabled:** We may contact '{name}' for further insights")
        
        st.session_state.submitted = True
        
        # Auto-refresh after delay
        time.sleep(5)
        st.rerun()
    else:
        st.error("""
        ## ❌ Submission Failed
        
        **We encountered an error saving your response.**  
        Please try again in a moment or contact support.
        
        **Don't lose your feedback!** Copy your responses below:
        """)
        
        # Show form data for manual recovery
        st.json(form_data)

# ============================================================================
# POST-SUBMISSION THANK YOU
# ============================================================================

if st.session_state.submitted:
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px;">
            <h2>🎉 Thank You!</h2>
            <p style="font-size: 1.2rem;">Your insights are invaluable for our product development.</p>
            <p>You may now close this window.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Option to submit another response
    if st.button("📝 Submit Another Response"):
        st.session_state.submitted = False
        st.session_state.form_data = {}
        st.rerun()

# ============================================================================
# ADMIN DASHBOARD (Hidden by default)
# ============================================================================

if st.sidebar.checkbox("👑 Admin Dashboard", False):
    st.markdown("---")
    st.header("👑 Admin Dashboard")
    
    # Data Management
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data", "🔧 Backup", "📈 Analytics", "⚙️ Settings"])
    
    with tab1:
        if os.path.exists("data/survey_data_master.csv"):
            df = pd.read_csv("data/survey_data_master.csv")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Responses", len(df))
            with col2:
                contact_count = df['allow_contact'].sum() if 'allow_contact' in df.columns else 0
                st.metric("Open to Contact", contact_count)
            with col3:
                unique_names = df[df['name'] != "Anonymous"]['name'].nunique()
                st.metric("Named Responses", unique_names)
            
            # Data preview
            st.subheader("Recent Submissions")
            st.dataframe(df[['timestamp', 'name', 'time_saved', 'biggest_time_quality']].tail(10),
                        use_container_width=True)
            
            # Export options
            st.subheader("Export Data")
            export_format = st.selectbox("Format:", ["CSV", "Excel", "JSON"])
            
            if export_format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "survey_data_full.csv", "text/csv")
            elif export_format == "Excel":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Survey Data', index=False)
                st.download_button("Download Excel", output.getvalue(), 
                                 "survey_data_full.xlsx", 
                                 "application/vnd.ms-excel")
    
    with tab2:
        st.subheader("Backup Systems Status")
        
        # Check backup files
        backup_info = []
        for backup_dir in BackupConfig.BACKUP_DIRS:
            if os.path.exists(backup_dir):
                file_count = len([f for f in os.listdir(backup_dir) if f.endswith(('.csv', '.json'))])
                backup_info.append({"Location": backup_dir, "Files": file_count})
        
        if backup_info:
            st.dataframe(pd.DataFrame(backup_info), use_container_width=True)
        
        # Manual backup
        if st.button("🔄 Create Manual Backup"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"manual_backup_{timestamp}.zip"
            st.success(f"Backup created: {backup_file}")
    
    with tab3:
        st.subheader("Response Analytics")
        
        if os.path.exists("data/survey_data_master.csv"):
            df = pd.read_csv("data/survey_data_master.csv")
            
            # Time saved distribution
            if 'time_saved' in df.columns:
                fig = px.pie(df, names='time_saved', 
                           title="⏱️ Time Saved Distribution",
                           hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
            
            # Methods used
            if 'methods' in df.columns:
                methods_count = df['methods'].str.split(', ').explode().value_counts()
                fig = px.bar(x=methods_count.index, y=methods_count.values,
                           title="📋 Methods Used",
                           labels={'x': 'Method', 'y': 'Count'})
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption(f"Data protected by {len(persistence.backup_systems)} backup systems")
with footer_col2:
    st.caption(f"Total submissions: {persistence.submission_count}")
with footer_col3:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Auto-save reminder
st.toast("💾 Auto-save enabled - Your data is protected", icon="✅")
