# survey_app_mvp.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CSV setup ---
csv_file = "survey_data.csv"

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
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

# --- Streamlit App ---
st.title("Report Writing MVP Survey")
st.write("""
**Purpose:** Collect teacher experience to validate the MVP, identify strengths, and guide improvements.
All responses are **anonymous**. Names are encoded for private follow-up only.
""")

# --- User Inputs ---
name = st.text_input("Your Name (optional, encoded for follow-up only)")

methods = st.multiselect(
    "Which methods have you used to write report comments?",
    ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", "Previous year's comments", "Dropdown tool", "Other"]
)

time_scratch = st.selectbox("Writing from scratch - Time per comment:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
time_ai = st.selectbox("ChatGPT/AI - Time per comment:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
time_school_bank = st.selectbox("School comment banks - Time per comment:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
time_dropdown = st.selectbox("Dropdown tool - Time per comment:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])

cognitive_scratch = st.selectbox("Writing from scratch - Mental effort:", ["Exhausting","High","Moderate","Low","Didn't use"])
cognitive_ai = st.selectbox("ChatGPT/AI - Mental effort:", ["Exhausting","High","Moderate","Low","Didn't use"])
cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", ["Very low","Low","Moderate","High","Didn't use"])

quality_scratch = st.selectbox("Writing from scratch - Quality:", ["High quality and consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic","Didn't use"])
quality_ai = st.selectbox("ChatGPT/AI - Quality:", ["High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI","Didn't use"])
quality_dropdown = st.selectbox("Dropdown tool - Quality:", ["High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic","Didn't use"])

character_accuracy_scratch = st.selectbox("Writing from scratch - Character count accuracy:", ["Within range","Exceeds range","Didn't use"])
character_accuracy_ai = st.selectbox("ChatGPT/AI - Character count accuracy:", ["Within range","Exceeds range","Didn't use"])
character_accuracy_dropdown = st.selectbox("Dropdown tool - Character count accuracy:", ["Within range","Exceeds range","Didn't use"])

curriculum_alignment_scratch = st.selectbox("Writing from scratch - Curriculum alignment:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
curriculum_alignment_ai = st.selectbox("ChatGPT/AI - Curriculum alignment:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
curriculum_alignment_dropdown = st.selectbox("Dropdown tool - Curriculum alignment:", ["Always","Usually","Sometimes","Rarely","Didn't use"])

stress_scratch = st.selectbox("Stress level - Writing from scratch:", ["Very high","High","Moderate","Low","Didn't use"])
stress_ai = st.selectbox("Stress level - ChatGPT/AI prompts:", ["Very high","High","Moderate","Low","Didn't use"])
stress_dropdown = st.selectbox("Stress level - Dropdown tool:", ["Very high","High","Moderate","Low","Didn't use"])

biggest_cognitive_relief = st.selectbox("Biggest cognitive relief from dropdown tool:", [
    "No need to decide what to include/exclude",
    "Character count automatically perfect",
    "No rephrasing/editing needed",
    "Curriculum-aligned language pre-written",
    "Clear structure removes blank page stress",
    "Consistency across all students",
    "Didn't use"
])

biggest_time_quality = st.selectbox("Best ratio of time-to-quality:", [
    "Writing from scratch",
    "ChatGPT/AI",
    "Dropdown tool",
    "Other",
    "Didn't use"
])

time_saved = st.selectbox("Time saved for 30 students vs previous method:", [
    "No time saved",
    "30min-1hr",
    "1-2hrs",
    "2-4hrs",
    "4+hrs",
    "Didn't use"
])

# Open feedback fields
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
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("Survey submitted! Thank you for your feedback.")

# --- Analysis ---
st.header("MVP Insights Dashboard")
df = pd.read_csv(csv_file)

# Quantitative charts
def create_chart(columns, title):
    temp = df[columns].melt(var_name="Method", value_name="Response")
    fig = px.histogram(temp, x="Method", color="Response", barmode="group", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Time Efficiency Comparison")
create_chart(["time_scratch","time_ai","time_school_bank","time_dropdown"], "Time per Comment")

st.subheader("Cognitive Load Comparison")
create_chart(["cognitive_scratch","cognitive_ai","cognitive_dropdown"], "Cognitive Effort")

st.subheader("Quality Comparison")
create_chart(["quality_scratch","quality_ai","quality_dropdown"], "Output Quality")

st.subheader("Stress Level Comparison")
create_chart(["stress_scratch","stress_ai","stress_dropdown"], "Stress Level")

st.subheader("Character Accuracy Comparison")
create_chart(["character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown"], "Character Accuracy")

st.subheader("Curriculum Alignment Comparison")
create_chart(["curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown"], "Curriculum Alignment")

# --- Qualitative Analysis ---
st.subheader("Qualitative Insights (MVP Evaluation)")

qualitative_comments = pd.concat([
    df[["open_feedback_ai"]].rename(columns={"open_feedback_ai":"Comment"}),
    df[["open_feedback_tool"]].rename(columns={"open_feedback_tool":"Comment"}),
    df[["suggestions"]].rename(columns={"suggestions":"Comment"})
], ignore_index=True)

# Classify simple strengths/limitations
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

st.write("**Value (what works well):**")
st.table(qualitative_comments[qualitative_comments["Category"]=="Value"].head(5))

st.write("**Limitations (pain points / areas to improve):**")
st.table(qualitative_comments[qualitative_comments["Category"]=="Limitation"].head(5))

# --- Download Excel ---
import io
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    # Quantitative
    df.to_excel(writer, sheet_name="Raw Survey Data", index=False)
    # Qualitative
    qualitative_comments.to_excel(writer, sheet_name="Qualitative Insights", index=False)
    writer.save()
    processed_data = output.getvalue()

st.download_button(
    label="Download Full MVP Survey Report (Excel)",
    data=processed_data,
    file_name="mvp_survey_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
