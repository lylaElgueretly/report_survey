# survey_app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# =======================
# 1. Load Email Secrets
# =======================
EMAIL = st.secrets["EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

# =======================
# 2. Columns & Data Setup
# =======================
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

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
MASTER_FILE = os.path.join(DATA_DIR, "survey_data_master.csv")

if not os.path.exists(MASTER_FILE):
    pd.DataFrame(columns=columns).to_csv(MASTER_FILE, index=False)

# =======================
# 3. Streamlit App Config
# =======================
st.set_page_config(
    page_title="Report Writing MVP Survey",
    layout="wide"
)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# =======================
# 4. Survey Form
# =======================
st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("**Data is automatically saved with multiple backups.**")

with st.form("survey_form", clear_on_submit=True):
    # Contact Info
    st.header("Your Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name (optional)")
    with col2:
        email = st.text_input("Email (optional)")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")

    st.divider()
    
    # Methods Used
    st.header("Methods You've Used")
    methods = st.multiselect(
        "Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
         "Previous year's comments", "Dropdown tool", "Other"]
    )

    st.divider()

    # Time Efficiency
    st.header("Time Efficiency")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        time_scratch = st.selectbox("From scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    with col2:
        time_ai = st.selectbox("AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    with col3:
        time_school_bank = st.selectbox("School banks:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
    with col4:
        time_dropdown = st.selectbox("Dropdown tool:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])
    
    st.divider()

    # Cognitive Effort
    st.header("Mental Effort")
    col1, col2, col3 = st.columns(3)
    with col1:
        cognitive_scratch = st.selectbox("From scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
    with col2:
        cognitive_ai = st.selectbox("AI prompts:", ["Exhausting","High","Moderate","Low","Didn't use"])
    with col3:
        cognitive_dropdown = st.selectbox("Dropdown tool:", ["Very low","Low","Moderate","High","Didn't use"])

    st.divider()

    # Quality
    st.header("Output Quality")
    col1, col2, col3 = st.columns(3)
    with col1:
        quality_scratch = st.selectbox("From scratch:", ["High quality and consistent", "High quality but inconsistent", 
             "Generally good", "Variable", "Often rushed/generic", "Didn't use"])
    with col2:
        quality_ai = st.selectbox("AI prompts:", ["High after edits", "Good with minor tweaks", "Acceptable", 
             "Too generic/not suitable", "Haven't used AI", "Didn't use"])
    with col3:
        quality_dropdown = st.selectbox("Dropdown tool:", ["High & curriculum-aligned", "Good, ready to use", 
             "Acceptable with minor tweaks", "Too generic", "Didn't use"])

    st.divider()

    # Open Feedback
    st.header("Open Feedback")
    open_feedback_ai = st.text_area("One thing AI does WRONG:", height=80)
    open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:", height=80)
    suggestions = st.text_area("Suggestions for improvement:", height=80)

    st.divider()

    # Submit Button
    submitted = st.form_submit_button("Submit Survey")

# =======================
# 5. Submission Handling
# =======================
if submitted and not st.session_state.submitted:
    if not methods:
        st.error("Please select at least one method you've used")
        st.stop()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submission_id = f"{hash(timestamp + (email or '')) % 1000000:06d}"

    form_data = {
        "submission_id": submission_id,
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
        "suggestions": suggestions,
        "timestamp": timestamp
    }

    # Save locally
    try:
        df = pd.read_csv(MASTER_FILE)
        df = pd.concat([df, pd.DataFrame([form_data])], ignore_index=True)
        df.to_csv(MASTER_FILE, index=False)
        st.success("Saved locally successfully!")
    except Exception as e:
        st.error(f"Local save failed: {str(e)}")

    # Send email with CSV attached
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = f"New Survey Submission: {submission_id}"

        # Body
        body = f"New survey submitted by {form_data['name']} ({form_data['email']}) at {timestamp}"
        msg.attach(MIMEText(body, "plain"))

        # Attach CSV
        with open(MASTER_FILE, "rb") as f:
            part = MIMEApplication(f.read(), Name="survey_data_master.csv")
        part['Content-Disposition'] = 'attachment; filename="survey_data_master.csv"'
        msg.attach(part)

        # Connect and send
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Email failed: {str(e)}\nSaved locally, but email failed. Check secrets and internet.")

    st.session_state.submitted = True
