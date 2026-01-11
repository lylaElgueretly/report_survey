# survey_app.py
import streamlit as st
import pandas as pd
import os
from io import BytesIO
from textblob import TextBlob
import plotly.express as px
import hashlib

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- FILE PATHS ---
csv_file = "survey_data.csv"
lookup_file = "names_lookup.csv"

# --- SURVEY COLUMNS ---
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

# --- CREATE CSV FILE IF MISSING ---
if not os.path.exists(csv_file):
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

if not os.path.exists(lookup_file):
    pd.DataFrame(columns=["anon_id","name"]).to_csv(lookup_file, index=False)

# --- ANONYMITY DISCLAIMER ---
st.info("""
**Participant Anonymity Notice:**  
Your survey responses are anonymous and will be used only for analysis.  
Your name will be encoded and cannot be traced back publicly. Only the survey creator can decode it to request endorsements from willing participants.
""")

# --- NAME INPUT ---
name = st.text_input("Your Name (for endorsement purposes, will be anonymized in analysis):")

# --- ENCODE NAME ---
def encode_name(name_str):
    return hashlib.sha256(name_str.encode('utf-8')).hexdigest()[:10]  # short hash for anonymized ID

anon_id = encode_name(name) if name else ""

# --- SURVEY INPUTS ---
methods = st.multiselect(
    "Which methods have you used to write report comments?",
    ["Writing from scratch","ChatGPT/AI prompts","School comment banks","Previous year's comments","This dropdown tool","Other"]
)

def options_with_skip(base_options):
    return base_options + ["Did not use"]

# --- Time ---
time_scratch = st.selectbox("Writing from scratch - Time per comment:", options_with_skip(["<2min","2-5min","5-10min","10+min"]))
time_ai = st.selectbox("ChatGPT/AI prompts - Time per comment:", options_with_skip(["<2min","2-5min","5-10min","10+min"]))
time_school_bank = st.selectbox("School comment banks - Time per comment:", options_with_skip(["<2min","2-5min","5-10min","10+min"]))
time_dropdown = st.selectbox("Dropdown tool - Time per comment:", options_with_skip(["<30sec","30sec-1min","1-2min","2+min"]))

# --- Cognitive Load ---
cognitive_scratch = st.selectbox("Writing from scratch - Mental effort:", options_with_skip(["Exhausting","High","Moderate","Low"]))
cognitive_ai = st.selectbox("ChatGPT/AI - Mental effort:", options_with_skip(["Exhausting","High","Moderate","Low"]))
cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", options_with_skip(["Very low","Low","Moderate","High"]))

# --- Quality ---
quality_scratch = st.selectbox("Writing from scratch - Quality:", options_with_skip([
    "High & consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic"]))
quality_ai = st.selectbox("ChatGPT/AI - Quality:", options_with_skip([
    "High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI"]))
quality_dropdown = st.selectbox("Dropdown tool - Quality:", options_with_skip([
    "High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic"]))

# --- Character Accuracy ---
character_accuracy_scratch = st.selectbox("Writing from scratch - Character count accuracy:", options_with_skip([
    "Always within range","Usually within range","Sometimes exceeds range","Exceeds range"]))
character_accuracy_ai = st.selectbox("ChatGPT/AI - Character count accuracy:", options_with_skip([
    "Always within range","Usually within range","Sometimes exceeds range","Exceeds range"]))
character_accuracy_dropdown = st.selectbox("Dropdown tool - Character count accuracy:", options_with_skip([
    "Always within range","Usually within range","Sometimes exceeds range","Exceeds range"]))

# --- Curriculum Alignment ---
curriculum_alignment_scratch = st.selectbox("Writing from scratch - Curriculum alignment:", options_with_skip(["Always","Usually","Sometimes","Rarely"]))
curriculum_alignment_ai = st.selectbox("ChatGPT/AI - Curriculum alignment:", options_with_skip(["Always","Usually","Sometimes","Rarely"]))
curriculum_alignment_dropdown = st.selectbox("Dropdown tool - Curriculum alignment:", options_with_skip(["Always","Usually","Sometimes","Rarely"]))

# --- Stress ---
stress_scratch = st.selectbox("Stress level - Writing from scratch:", options_with_skip(["Very high","High","Moderate","Low"]))
stress_ai = st.selectbox("Stress level - ChatGPT/AI prompts:", options_with_skip(["Very high","High","Moderate","Low"]))
stress_dropdown = st.selectbox("Stress level - Dropdown tool:", options_with_skip(["Very high","High","Moderate","Low"]))

# --- Other ---
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

# --- Qualitative ---
open_feedback_ai = st.text_area("One thing ChatGPT/AI does WRONG:")
open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:")
suggestions = st.text_area("Any suggestions for improvement:")

# --- SUBMIT ---
if st.button("Submit Survey"):
    if not name:
        st.warning("Please enter your name!")
    else:
        df = pd.read_csv(csv_file)
        new_row = {
            "name": anon_id,
            "methods": ", ".join(methods),
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

        # Save name lookup privately
        lookup_df = pd.read_csv(lookup_file)
        if anon_id not in lookup_df["anon_id"].values:
            lookup_df = pd.concat([lookup_df, pd.DataFrame([{"anon_id": anon_id,"name": name}])], ignore_index=True)
            lookup_df.to_csv(lookup_file, index=False)

        st.success("Survey submitted! Thank you for your feedback.")
        st.session_state.submitted = True
        st.experimental_rerun()

# --- ANALYSIS & EXPORT ---
st.header("Survey Analysis & Full Report")
df = pd.read_csv(csv_file)

if not df.empty:
    # --- Quantitative Charts ---
    st.subheader("Quantitative Analysis")
    def create_chart(columns_list, title, order=None):
        temp = df[columns_list].melt(var_name="Method", value_name="Response")
        fig = px.histogram(temp, x="Method", color="Response", barmode="group", text_auto=True, category_orders={"Response": order})
        fig.update_layout(title=title, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

    create_chart(["time_scratch","time_ai","time_school_bank","time_dropdown"], "Time per Comment")
    create_chart(["cognitive_scratch","cognitive_ai","cognitive_dropdown"], "Cognitive Effort")
    create_chart(["stress_scratch","stress_ai","stress_dropdown"], "Stress Level")
    create_chart(["quality_scratch","quality_ai","quality_dropdown"], "Quality")
    create_chart(["character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown"], "Character Accuracy")
    create_chart(["curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown"], "Curriculum Alignment")

    # --- Qualitative Analysis ---
    st.subheader("Qualitative Analysis with Themes & Sentiment")
    themes_keywords = {
        "App Usability / UX Issues": ["click","reverts","select subject","last punctuation","typing","interface","layout","default"],
        "Cognitive Load / Effort": ["thinking","requires","tweaks","narrowing down","exceeds character","manual"],
        "Time Efficiency": ["seconds","quick","fast","saves time","few seconds"],
        "Other / Miscellaneous": []
    }

    qual_cols = ["open_feedback_ai","open_feedback_tool","suggestions"]
    qualitative_summary = []

    for col in qual_cols:
        responses = df[col].dropna().astype(str)
        themed_responses = {"Theme":[], "Sentiment":[]}
        for resp in responses:
            # Assign theme
            assigned = False
            for theme, keywords in themes_keywords.items():
                if any(word in resp.lower() for word in keywords):
                    themed_responses["Theme"].append(theme)
                    assigned = True
                    break
            if not assigned:
                themed_responses["Theme"].append("Other / Miscellaneous")
            # Sentiment
            sentiment = TextBlob(resp).sentiment.polarity
            if sentiment > 0.1:
                themed_responses["Sentiment"].append("Positive")
            elif sentiment < -0.1:
                themed_responses["Sentiment"].append("Negative")
            else:
                themed_responses["Sentiment"].append("Neutral")
        themed_df = pd.DataFrame(themed_responses)
        st.markdown(f"**{col.replace('_',' ').title()}:**")
        st.dataframe(themed_df.groupby("Theme")["Sentiment"].count().rename("Count"))
        fig = px.histogram(themed_df, x="Theme", color="Sentiment", barmode="stack", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        qualitative_summary.append(themed_df)

    # --- Excel Export ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        for i, col in enumerate(qual_cols):
            qualitative_summary[i].to_excel(writer, sheet_name=col[:30], index=False)
    st.download_button("Download Full Survey Report (Excel)", data=output.getvalue(), file_name="full_survey_report.xlsx")
