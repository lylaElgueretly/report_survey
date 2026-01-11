# survey_app.py
import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# CSV file path
csv_file = "survey_data.csv"

# Survey columns
columns = [
    "name","methods",
    "time_scratch","time_ai","time_school_bank","time_dropdown",
    "cognitive_scratch","cognitive_ai","cognitive_dropdown",
    "quality_scratch","quality_ai","quality_dropdown",
    "character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown",
    "curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown",
    "stress_scratch","stress_ai","stress_dropdown",
    "biggest_cognitive_relief","biggest_time_quality","time_saved",
    "open_feedback_ai","open_feedback_tool","suggestions"
]

# Create CSV if missing
if not os.path.exists(csv_file):
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

# --- STREAMLIT SURVEY ---
st.title("Report Writing Methods - Teacher Experience Survey")
st.write("Quick Survey (~5 min)")

name = st.text_input("Your Name:")

methods = st.multiselect(
    "Which methods have you used to write report comments?",
    ["Writing from scratch","ChatGPT/AI prompts","School comment banks","Previous year's comments","This dropdown tool","Other"]
)

# Helper function for "Did not use" option
def options_with_skip(base_options):
    return base_options + ["Did not use"]

# SECTION: Time
time_scratch = st.selectbox("Writing from scratch - Time per comment:", options_with_skip(["<2min","2-5min","5-10min","10+min"]))
time_ai = st.selectbox("ChatGPT/AI prompts - Time per comment:", options_with_skip(["<2min","2-5min","5-10min","10+min"]))
time_school_bank = st.selectbox("School comment banks - Time per comment:", options_with_skip(["<2min","2-5min","5-10min","10+min"]))
time_dropdown = st.selectbox("Dropdown tool - Time per comment:", options_with_skip(["<30sec","30sec-1min","1-2min","2+min"]))

# SECTION: Cognitive Load
cognitive_scratch = st.selectbox("Writing from scratch - Mental effort:", options_with_skip(["Exhausting","High","Moderate","Low"]))
cognitive_ai = st.selectbox("ChatGPT/AI - Mental effort:", options_with_skip(["Exhausting","High","Moderate","Low"]))
cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", options_with_skip(["Very low","Low","Moderate","High"]))

# SECTION: Quality
quality_scratch = st.selectbox("Writing from scratch - Quality:", options_with_skip(["High & consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic"]))
quality_ai = st.selectbox("ChatGPT/AI - Quality:", options_with_skip(["High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI"]))
quality_dropdown = st.selectbox("Dropdown tool - Quality:", options_with_skip(["High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic"]))

# SECTION: Character Accuracy
character_accuracy_scratch = st.selectbox("Writing from scratch - Character count accuracy:", options_with_skip(["Always within range","Usually within range","Sometimes exceeds range","Exceeds range"]))
character_accuracy_ai = st.selectbox("ChatGPT/AI - Character count accuracy:", options_with_skip(["Always within range","Usually within range","Sometimes exceeds range","Exceeds range"]))
character_accuracy_dropdown = st.selectbox("Dropdown tool - Character count accuracy:", options_with_skip(["Always within range","Usually within range","Sometimes exceeds range","Exceeds range"]))

# SECTION: Curriculum Alignment
curriculum_alignment_scratch = st.selectbox("Writing from scratch - Curriculum alignment:", options_with_skip(["Always","Usually","Sometimes","Rarely"]))
curriculum_alignment_ai = st.selectbox("ChatGPT/AI - Curriculum alignment:", options_with_skip(["Always","Usually","Sometimes","Rarely"]))
curriculum_alignment_dropdown = st.selectbox("Dropdown tool - Curriculum alignment:", options_with_skip(["Always","Usually","Sometimes","Rarely"]))

# SECTION: Stress
stress_scratch = st.selectbox("Stress level - Writing from scratch:", options_with_skip(["Very high","High","Moderate","Low"]))
stress_ai = st.selectbox("Stress level - ChatGPT/AI prompts:", options_with_skip(["Very high","High","Moderate","Low"]))
stress_dropdown = st.selectbox("Stress level - Dropdown tool:", options_with_skip(["Very high","High","Moderate","Low"]))

# SECTION: Other
biggest_cognitive_relief = st.selectbox("Biggest cognitive relief from dropdown tool:", [
    "No need to decide what to include/exclude",
    "Character count automatically perfect",
    "No rephrasing/editing needed",
    "Curriculum-aligned language pre-written",
    "Clear structure removes blank page stress",
    "Consistency across all students"
])
biggest_time_quality = st.selectbox("Best ratio of time-to-quality:", ["Writing from scratch","ChatGPT/AI","Dropdown tool","Other"])
time_saved = st.selectbox("Time saved for 30 students vs previous method:", ["No time saved","30min-1hr","1-2hrs","2-4hrs","4+hrs"])

# SECTION: Qualitative
open_feedback_ai = st.text_area("One thing ChatGPT/AI does WRONG:")
open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:")
suggestions = st.text_area("Any suggestions for improvement:")

# --- SAVE TO CSV ---
if st.button("Submit Survey"):
    if not name:
        st.warning("Please enter your name!")
    else:
        df = pd.read_csv(csv_file)
        new_row = {
            "name": name,"methods": ", ".join(methods),
            "time_scratch": time_scratch,"time_ai": time_ai,"time_school_bank": time_school_bank,"time_dropdown": time_dropdown,
            "cognitive_scratch": cognitive_scratch,"cognitive_ai": cognitive_ai,"cognitive_dropdown": cognitive_dropdown,
            "quality_scratch": quality_scratch,"quality_ai": quality_ai,"quality_dropdown": quality_dropdown,
            "character_accuracy_scratch": character_accuracy_scratch,"character_accuracy_ai": character_accuracy_ai,"character_accuracy_dropdown": character_accuracy_dropdown,
            "curriculum_alignment_scratch": curriculum_alignment_scratch,"curriculum_alignment_ai": curriculum_alignment_ai,"curriculum_alignment_dropdown": curriculum_alignment_dropdown,
            "stress_scratch": stress_scratch,"stress_ai": stress_ai,"stress_dropdown": stress_dropdown,
            "biggest_cognitive_relief": biggest_cognitive_relief,"biggest_time_quality": biggest_time_quality,"time_saved": time_saved,
            "open_feedback_ai": open_feedback_ai,"open_feedback_tool": open_feedback_tool,"suggestions": suggestions
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success("Survey submitted! Thank you for your feedback.")
        st.session_state.submitted = True
        st.experimental_rerun()

# --- ANALYSIS & EXCEL EXPORT ---
st.header("Survey Analysis & Full Report")
df = pd.read_csv(csv_file)

if not df.empty:
    st.subheader("Interactive Charts")
    def create_chart(columns_list, title, order=None):
        temp = df[columns_list].melt(var_name="Method", value_name="Response")
        fig = px.histogram(temp, x="Method", color="Response", barmode="group", text_auto=True, category_orders={"Response": order})
        fig.update_layout(title=title, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    # Charts
    create_chart(["time_scratch","time_ai","time_school_bank","time_dropdown"], "Time per Comment", order=["<30sec","<2min","2-5min","5-10min","10+min","1-2min","2+min","Did not use"])
    create_chart(["cognitive_scratch","cognitive_ai","cognitive_dropdown"], "Cognitive Effort", order=["Very low","Low","Moderate","High","Exhausting","Did not use"])
    create_chart(["stress_scratch","stress_ai","stress_dropdown"], "Stress Level", order=["Low","Moderate","High","Very high","Did not use"])
    create_chart(["quality_scratch","quality_ai","quality_dropdown"], "Quality", order=["High & consistent","High quality but inconsistent","High & curriculum-aligned","Generally good","Good, ready to use","Acceptable","Acceptable with minor tweaks","Variable","Too generic","Too generic/not suitable","Haven't used AI","Did not use"])
    create_chart(["character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown"], "Character Accuracy", order=["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"])
    create_chart(["curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown"], "Curriculum Alignment", order=["Always","Usually","Sometimes","Rarely","Did not use"])

    # --- Excel Export ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Raw data
        df.to_excel(writer, sheet_name='Raw Data', index=False)

        # Summary sheet
        summary_data = {}
        for col in ["time_scratch","time_ai","time_school_bank","time_dropdown",
                    "cognitive_scratch","cognitive_ai","cognitive_dropdown",
                    "stress_scratch","stress_ai","stress_dropdown",
                    "quality_scratch","quality_ai","quality_dropdown",
                    "character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown",
                    "curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown"]:
            counts = df[col].value_counts(dropna=False)
            summary_data[col] = counts

        # Convert summary_data to DataFrame and save
        summary_df = pd.DataFrame({k:v for k,v in summary_data.items()})
        summary_df.to_excel(writer, sheet_name='Summary')

        # Qualitative responses
        df[["open_feedback_ai","open_feedback_tool","suggestions"]].to_excel(writer, sheet_name='Qualitative Responses', index=False)

    st.download_button("Download Full Survey Report (Excel)", data=output.getvalue(), file_name="full_survey_report.xlsx")
