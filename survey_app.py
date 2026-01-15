# survey_app.py
import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===============================
# 1. LOAD SECRETS
# ===============================
EMAIL = st.secrets["EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
EMAIL_RECEIVER = st.secrets.get("EMAIL_RECEIVER", EMAIL)  # optional: send to a different email

# ===============================
# 2. SETUP
# ===============================
st.set_page_config(
    page_title="Report Writing MVP Validation Survey",
    layout="wide"
)

# Make directories
os.makedirs("data", exist_ok=True)

# Master CSV file
MASTER_FILE = "data/survey_data_master.csv"

# Columns
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

# Initialize CSV if not exists
if not os.path.exists(MASTER_FILE):
    pd.DataFrame(columns=columns).to_csv(MASTER_FILE, index=False)

# ===============================
# 3. MAIN SURVEY
# ===============================
st.title("Report Writing MVP Validation Survey")
st.write("Your feedback helps improve our tool. All responses are anonymous unless you choose to share contact information.")
st.write("Data is automatically saved with multiple backups.")

with st.form("survey_form", clear_on_submit=True):
    # --- Contact Info ---
    st.header("Your Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name (optional)", placeholder="e.g., Alex Johnson")
    with col2:
        email = st.text_input("Email (optional)", placeholder="e.g., name@school.edu")
    allow_contact = st.checkbox("I'm open to follow-up interviews (optional)")

    st.divider()

    # --- Methods ---
    st.header("Methods Used")
    methods = st.multiselect(
        "Select all methods you've used for report writing:",
        ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks",
         "Previous year's comments", "Dropdown tool", "Other"]
    )

    st.divider()

    # --- Time Efficiency ---
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

    # --- Cognitive Effort ---
    st.header("Mental Effort")
    col1, col2, col3 = st.columns(3)
    with col1:
        cognitive_scratch = st.selectbox("From scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
    with col2:
        cognitive_ai = st.selectbox("AI prompts:", ["Exhausting","High","Moderate","Low","Didn't use"])
    with col3:
        cognitive_dropdown = st.selectbox("Dropdown tool:", ["Very low","Low","Moderate","High","Didn't use"])

    st.divider()

    # --- Quality ---
    st.header("Output Quality")
    col1, col2, col3 = st.columns(3)
    with col1:
        quality_scratch = st.selectbox("From scratch:", 
            ["High quality and consistent", "High quality but inconsistent", "Generally good", "Variable", "Often rushed/generic", "Didn't use"])
    with col2:
        quality_ai = st.selectbox("AI prompts:", 
            ["High after edits", "Good with minor tweaks", "Acceptable", "Too generic/not suitable", "Haven't used AI", "Didn't use"])
    with col3:
        quality_dropdown = st.selectbox("Dropdown tool:", 
            ["High & curriculum-aligned", "Good, ready to use", "Acceptable with minor tweaks", "Too generic", "Didn't use"])

    st.divider()

    # --- Character Accuracy ---
    st.header("Specific Metrics")
    st.subheader("Character Accuracy")
    col1, col2, col3 = st.columns(3)
    with col1:
        character_accuracy_scratch = st.radio("From scratch:", ["Within range", "Exceeds range", "Didn't use"])
    with col2:
        character_accuracy_ai = st.radio("AI prompts:", ["Within range", "Exceeds range", "Didn't use"])
    with col3:
        character_accuracy_dropdown = st.radio("Dropdown tool:", ["Within range", "Exceeds range", "Didn't use"])

    # --- Curriculum Alignment ---
    st.subheader("Curriculum Alignment")
    col1, col2, col3 = st.columns(3)
    with col1:
        curriculum_alignment_scratch = st.selectbox("From scratch:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
    with col2:
        curriculum_alignment_ai = st.selectbox("AI prompts:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
    with col3:
        curriculum_alignment_dropdown = st.selectbox("Dropdown tool:", ["Always","Usually","Sometimes","Rarely","Didn't use"])

    # --- Stress ---
    st.subheader("Stress Level")
    col1, col2, col3 = st.columns(3)
    with col1:
        stress_scratch = st.selectbox("From scratch:", ["Very high","High","Moderate","Low","Didn't use"])
    with col2:
        stress_ai = st.selectbox("AI prompts:", ["Very high","High","Moderate","Low","Didn't use"])
    with col3:
        stress_dropdown = st.selectbox("Dropdown tool:", ["Very high","High","Moderate","Low","Didn't use"])

    st.divider()

    # --- Tool Benefits ---
    st.header("Dropdown Tool Benefits")
    col1, col2, col3 = st.columns(3)
    with col1:
        biggest_cognitive_relief = st.selectbox("Cognitive relief:", [
            "No need to decide what to include/exclude",
            "Character count automatically perfect",
            "No rephrasing/editing needed",
            "Curriculum-aligned language pre-written",
            "Clear structure removes blank page stress",
            "Consistency across all students",
            "Didn't use"
        ])
    with col2:
        biggest_time_quality = st.selectbox("Best time-to-quality:", [
            "Writing from scratch",
            "ChatGPT/AI",
            "Dropdown tool",
            "Other",
            "Didn't use"
        ])
    with col3:
        time_saved = st.selectbox("Time saved for 30 students:", [
            "No time saved","30min-1hr","1-2hrs","2-4hrs","4-6hrs","6-8hrs","8-12hrs","12-24hrs","24+hrs","Didn't use"
        ])

    st.divider()

    # --- Open Feedback ---
    st.header("Open Feedback")
    open_feedback_ai = st.text_area("One thing AI does WRONG:", height=80)
    open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:", height=80)
    suggestions = st.text_area("Suggestions for improvement:", height=80)

    st.divider()

    submitted = st.form_submit_button("Submit Survey")

# ===============================
# 4. SUBMISSION HANDLING
# ===============================
if submitted:
    if not methods:
        st.error("Please select at least one method you used.")
        st.stop()

    # Collect data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submission_id = f"{int(time.time())}"
    data = {
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
        "suggestions": suggestions,
        "timestamp": timestamp
    }

    # Save locally
    df = pd.read_csv(MASTER_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(MASTER_FILE, index=False)
    st.success("✅ Successfully submitted and saved locally!")

    # ===============================
    # Send Email
    # ===============================
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = f"New Survey Submission {submission_id}"
        body = df.tail(1).to_csv(index=False)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        st.success(f"📧 Email sent to {EMAIL_RECEIVER}")
    except Exception as e:
        st.error(f"Email failed: {e}")
