# survey_app.py
import streamlit as st
import pandas as pd
import os

# --- SESSION STATE FOR SAFE RERUN ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.session_state.submitted:
    st.session_state.submitted = False
    st.experimental_rerun()

# CSV file path
csv_file = "survey_data.csv"

# Columns for Version A survey
columns = [
    "name",
    "methods",
    "time_scratch",
    "time_ai",
    "time_school_bank",
    "time_dropdown",
    "cognitive_scratch",
    "cognitive_ai",
    "cognitive_dropdown",
    "quality_scratch",
    "quality_ai",
    "quality_dropdown",
    "character_accuracy_scratch",
    "character_accuracy_ai",
    "character_accuracy_dropdown",
    "curriculum_alignment_scratch",
    "curriculum_alignment_ai",
    "curriculum_alignment_dropdown",
    "stress_scratch",
    "stress_ai",
    "stress_dropdown",
    "biggest_cognitive_relief",
    "biggest_time_quality",
    "time_saved",
    "open_feedback_ai",
    "open_feedback_tool",
    "suggestions",
]

# Create CSV if it doesn't exist
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)

# --- STREAMLIT SURVEY INTERFACE ---
st.title("Report Writing Methods - Teacher Experience Survey")
st.write("Quick Survey: How Do You Write Report Comments? (~5 minutes)")

# Teacher name
name = st.text_input("Your Name:")

# SECTION 1: Methods Used
methods = st.multiselect(
    "Which methods have you used to write report comments?",
    ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", "Previous year's comments", "This dropdown tool", "Other"]
)

# SECTION 2: Time Efficiency
time_scratch = st.selectbox(
    "Writing from scratch - Time per comment:",
    ["<2min","2-5min","5-10min","10+min","Did not use"]
)
time_ai = st.selectbox(
    "ChatGPT/AI prompts - Time per comment:",
    ["<2min","2-5min","5-10min","10+min","Did not use"]
)
time_school_bank = st.selectbox(
    "School comment banks - Time per comment:",
    ["<2min","2-5min","5-10min","10+min","Did not use"]
)
time_dropdown = st.selectbox(
    "This dropdown tool - Time per comment:",
    ["<30sec","30sec-1min","1-2min","2+min","Did not use"]
)

# SECTION 3: Cognitive Load
cognitive_scratch = st.selectbox("Writing from scratch - Mental effort:", ["Exhausting","High","Moderate","Low","Did not use"])
cognitive_ai = st.selectbox("ChatGPT/AI - Mental effort:", ["Exhausting","High","Moderate","Low","Did not use"])
cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", ["Very low","Low","Moderate","High","Did not use"])

# SECTION 4: Quality of Output
quality_scratch = st.selectbox(
    "Writing from scratch - Quality:",
    ["High & consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic","Did not use"]
)
quality_ai = st.selectbox(
    "ChatGPT/AI - Quality:",
    ["High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI","Did not use"]
)
quality_dropdown = st.selectbox(
    "Dropdown tool - Quality:",
    ["High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic","Did not use"]
)

# SECTION 5: Character & Curriculum Alignment
character_accuracy_scratch = st.selectbox(
    "Writing from scratch - Character count accuracy:",
    ["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"]
)
character_accuracy_ai = st.selectbox(
    "ChatGPT/AI - Character count accuracy:",
    ["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"]
)
character_accuracy_dropdown = st.selectbox(
    "Dropdown tool - Character count accuracy:",
    ["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"]
)

curriculum_alignment_scratch = st.selectbox(
    "Writing from scratch - Curriculum alignment:",
    ["Always","Usually","Sometimes","Rarely","Did not use"]
)
curriculum_alignment_ai = st.selectbox(
    "ChatGPT/AI - Curriculum alignment:",
    ["Always","Usually","Sometimes","Rarely","Did not use"]
)
curriculum_alignment_dropdown = st.selectbox(
    "Dropdown tool - Curriculum alignment:",
    ["Always","Usually","Sometimes","Rarely","Did not use"]
)

# SECTION 6: Stress Level
stress_scratch = st.selectbox("Stress level - Writing from scratch:", ["Very high","High","Moderate","Low","Did not use"])
stress_ai = st.selectbox("Stress level - ChatGPT/AI prompts:", ["Very high","High","Moderate","Low","Did not use"])
stress_dropdown = st.selectbox("Stress level - Dropdown tool:", ["Very high","High","Moderate","Low","Did not use"])

# SECTION 7: Other Comparisons
biggest_cognitive_relief = st.selectbox("Biggest cognitive relief from dropdown tool:", [
    "No need to decide what to include/exclude",
    "Character count automatically perfect",
    "No rephrasing/editing needed",
    "Curriculum-aligned language pre-written",
    "Clear structure removes blank page stress",
    "Consistency across all students"
])

biggest_time_quality = st.selectbox("Best ratio of time-to-quality:", [
    "Writing from scratch",
    "ChatGPT/AI",
    "Dropdown tool",
    "Other"
])

time_saved = st.selectbox("Time saved for 30 students vs previous method:", [
    "No time saved",
    "30min-1hr",
    "1-2hrs",
    "2-4hrs",
    "4+hrs"
])

# SECTION 8: Open Feedback
open_feedback_ai = st.text_area("One thing ChatGPT/AI does WRONG:")
open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:")
suggestions = st.text_area("Any suggestions for improvement:")

# --- SAVE TO CSV ---
if st.button("Submit Survey"):
    if name == "":
        st.warning("Please enter your name before submitting!")
    else:
        df = pd.read_csv(csv_file)
        new_row = {
            "name": name,
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
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success("Survey submitted! Thank you for your feedback.")
        st.session_state.submitted = True  # safe rerun

# --- BASIC CHARTS ---
st.header("Quick Analysis of Responses")
df = pd.read_csv(csv_file)

if not df.empty:
    st.subheader("Methods Used by Teachers")
    method_counts = pd.Series([m.strip() for m in ','.join(df['methods']).split(',')]).value_counts()
    st.bar_chart(method_counts)

    st.subheader("Time Efficiency (Dropdown Tool)")
    time_counts = df['time_dropdown'].value_counts()
    st.bar_chart(time_counts)
