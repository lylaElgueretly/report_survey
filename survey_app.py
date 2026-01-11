# survey_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
import hashlib

# --- CSV file setup ---
csv_file = "survey_data.csv"
columns = [
    "name", "methods",
    "time_scratch","time_ai","time_school_bank","time_dropdown",
    "stress_scratch","stress_ai","stress_dropdown",
    "cognitive_scratch","cognitive_ai","cognitive_dropdown",
    "quality_scratch","quality_ai","quality_dropdown",
    "character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown",
    "curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown",
    "biggest_cognitive_relief","biggest_time_quality","time_saved",
    "open_feedback_ai","open_feedback_tool","suggestions"
]

if not os.path.exists(csv_file):
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

# --- Survey Form ---
st.title("Report Writing Methods - Teacher Experience Survey (MVP Feedback)")
st.write("""
This survey collects feedback on your experience using different methods for writing report comments.  
All responses are **anonymous**, names are encoded and used only for follow-up if you allow it.
""")

# Encode name for anonymity
name_raw = st.text_input("Your Name (optional, for follow-up):")
name = hashlib.sha256(name_raw.encode()).hexdigest() if name_raw else ""

# Methods used
methods = st.multiselect(
    "Which methods have you used to write report comments?",
    ["Writing from scratch","ChatGPT/AI prompts","School comment banks","Previous year's comments","Dropdown tool","Other"]
)

# Time per comment
time_options = ["<30sec","30sec-1min","1-2min","2-5min","5-10min","10+min","N/A"]
time_scratch = st.selectbox("Writing from scratch - Time per comment:", time_options)
time_ai = st.selectbox("ChatGPT/AI prompts - Time per comment:", time_options)
time_school_bank = st.selectbox("School comment banks - Time per comment:", time_options)
time_dropdown = st.selectbox("Dropdown tool - Time per comment:", time_options)

# Cognitive load
cognitive_options = ["Very low","Low","Moderate","High","Exhausting","N/A"]
cognitive_scratch = st.selectbox("Writing from scratch - Mental effort:", cognitive_options)
cognitive_ai = st.selectbox("ChatGPT/AI - Mental effort:", cognitive_options)
cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", cognitive_options)

# Quality
quality_options = ["High & consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic","Too generic/not suitable","Haven't used","N/A"]
quality_scratch = st.selectbox("Writing from scratch - Quality:", quality_options)
quality_ai = st.selectbox("ChatGPT/AI - Quality:", quality_options)
quality_dropdown = st.selectbox("Dropdown tool - Quality:", quality_options)

# Character accuracy
char_accuracy_options = ["Always within range","Usually within range","Often exceeds/under","Always wrong","N/A"]
character_accuracy_scratch = st.selectbox("Writing from scratch - Character count accuracy:", char_accuracy_options)
character_accuracy_ai = st.selectbox("ChatGPT/AI - Character count accuracy:", char_accuracy_options)
character_accuracy_dropdown = st.selectbox("Dropdown tool - Character count accuracy:", char_accuracy_options)

# Curriculum alignment
alignment_options = ["Always","Usually","Sometimes","Rarely","N/A"]
curriculum_alignment_scratch = st.selectbox("Writing from scratch - Curriculum alignment:", alignment_options)
curriculum_alignment_ai = st.selectbox("ChatGPT/AI - Curriculum alignment:", alignment_options)
curriculum_alignment_dropdown = st.selectbox("Dropdown tool - Curriculum alignment:", alignment_options)

# Stress
stress_options = ["Very high","High","Moderate","Low","N/A"]
stress_scratch = st.selectbox("Stress level - Writing from scratch:", stress_options)
stress_ai = st.selectbox("Stress level - ChatGPT/AI prompts:", stress_options)
stress_dropdown = st.selectbox("Stress level - Dropdown tool:", stress_options)

# Other comparisons
biggest_cognitive_relief = st.selectbox("Biggest cognitive relief from dropdown tool:", [
    "No need to decide what to include/exclude",
    "Character count automatically perfect",
    "No rephrasing/editing needed",
    "Curriculum-aligned language pre-written",
    "Clear structure removes blank page stress",
    "Consistency across all students"
])
biggest_time_quality = st.selectbox("Best ratio of time-to-quality:", ["Writing from scratch","ChatGPT/AI","Dropdown tool","Other"])
time_saved = st.selectbox("Time saved for 30 students vs previous method:", ["No time saved","30min-1hr","1-2hrs","2-4hrs","4+hrs","N/A"])

# Open feedback
open_feedback_ai = st.text_area("One thing ChatGPT/AI does WRONG:")
open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:")
suggestions = st.text_area("Any suggestions for improvement:")

# --- Save to CSV ---
if st.button("Submit Survey"):
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
    df = df.append(new_row, ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("Survey submitted! Thank you for your feedback.")

# --- Quantitative Charts ---
st.header("Quick Analysis of Responses")

df = pd.read_csv(csv_file)
if not df.empty:

    # Methods used
    st.subheader("Methods Used by Teachers")
    method_counts = pd.Series(','.join(df['methods']).split(',')).value_counts()
    fig_methods = px.bar(x=method_counts.index, y=method_counts.values, labels={'x':'Method','y':'Count'}, title="Methods Used")
    st.plotly_chart(fig_methods)

    # Time efficiency (dropdown)
    st.subheader("Time per Comment - Dropdown Tool")
    time_counts = df['time_dropdown'].value_counts()
    fig_time = px.bar(x=time_counts.index, y=time_counts.values, labels={'x':'Time','y':'Count'}, title="Dropdown Tool - Time per Comment")
    st.plotly_chart(fig_time)

# --- Qualitative Analysis ---
st.subheader("Qualitative Insights (MVP Evaluation)")

qualitative_comments = pd.concat([
    df[["open_feedback_ai"]].rename(columns={"open_feedback_ai":"Comment"}),
    df[["open_feedback_tool"]].rename(columns={"open_feedback_tool":"Comment"}),
    df[["suggestions"]].rename(columns={"suggestions":"Comment"})
], ignore_index=True)

strength_keywords = ["helpful", "fast", "saves", "consistent", "aligned", "structured", "reduces stress", "efficient", "accurate"]
limitation_keywords = ["tedious", "glitch", "exceeds", "slow", "extra work", "inconsistent", "manual", "error", "bug", "needs tweaks"]

def classify_comment(comment):
    comment_lower = str(comment).lower()
    for word in strength_keywords:
        if word in comment_lower:
            return "Value"
    for word in limitation_keywords:
        if word in comment_lower:
            return "Limitation"
    return "Neutral"

qualitative_comments["Category"] = qualitative_comments["Comment"].apply(classify_comment)

# Show as markdown with color
st.write("**Value / Strengths:**")
for _, row in qualitative_comments[qualitative_comments["Category"]=="Value"].iterrows():
    st.markdown(f"<span style='color:green'>- {row['Comment']}</span>", unsafe_allow_html=True)

st.write("**Limitations / Areas for Improvement:**")
for _, row in qualitative_comments[qualitative_comments["Category"]=="Limitation"].iterrows():
    st.markdown(f"<span style='color:red'>- {row['Comment']}</span>", unsafe_allow_html=True)

# --- Export Full Report ---
st.subheader("Download Full MVP Survey Report (Excel)")
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Raw Survey Data", index=False)
    qualitative_comments.to_excel(writer, sheet_name="Qualitative Insights", index=False)
processed_data = output.getvalue()

st.download_button(
    label="Download Report",
    data=processed_data,
    file_name="mvp_survey_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
