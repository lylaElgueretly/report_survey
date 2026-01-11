# survey_app.py
import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- SESSION STATE FOR SAFE RERUN ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# CSV file path
csv_file = "survey_data.csv"

# Columns for survey
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
    ["Writing from scratch","ChatGPT/AI prompts","School comment banks","Previous year's comments","This dropdown tool","Other"]
)

# SECTION 2: Time Efficiency
time_scratch = st.selectbox("Writing from scratch - Time per comment:", ["<2min","2-5min","5-10min","10+min","Did not use"])
time_ai = st.selectbox("ChatGPT/AI prompts - Time per comment:", ["<2min","2-5min","5-10min","10+min","Did not use"])
time_school_bank = st.selectbox("School comment banks - Time per comment:", ["<2min","2-5min","5-10min","10+min","Did not use"])
time_dropdown = st.selectbox("Dropdown tool - Time per comment:", ["<30sec","30sec-1min","1-2min","2+min","Did not use"])

# SECTION 3: Cognitive Load
cognitive_scratch = st.selectbox("Writing from scratch - Mental effort:", ["Exhausting","High","Moderate","Low","Did not use"])
cognitive_ai = st.selectbox("ChatGPT/AI - Mental effort:", ["Exhausting","High","Moderate","Low","Did not use"])
cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", ["Very low","Low","Moderate","High","Did not use"])

# SECTION 4: Quality of Output
quality_scratch = st.selectbox("Writing from scratch - Quality:", ["High & consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic","Did not use"])
quality_ai = st.selectbox("ChatGPT/AI - Quality:", ["High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI","Did not use"])
quality_dropdown = st.selectbox("Dropdown tool - Quality:", ["High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic","Did not use"])

# SECTION 5: Character & Curriculum Alignment
character_accuracy_scratch = st.selectbox("Writing from scratch - Character count accuracy:", ["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"])
character_accuracy_ai = st.selectbox("ChatGPT/AI - Character count accuracy:", ["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"])
character_accuracy_dropdown = st.selectbox("Dropdown tool - Character count accuracy:", ["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"])

curriculum_alignment_scratch = st.selectbox("Writing from scratch - Curriculum alignment:", ["Always","Usually","Sometimes","Rarely","Did not use"])
curriculum_alignment_ai = st.selectbox("ChatGPT/AI - Curriculum alignment:", ["Always","Usually","Sometimes","Rarely","Did not use"])
curriculum_alignment_dropdown = st.selectbox("Dropdown tool - Curriculum alignment:", ["Always","Usually","Sometimes","Rarely","Did not use"])

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
biggest_time_quality = st.selectbox("Best ratio of time-to-quality:", ["Writing from scratch","ChatGPT/AI","Dropdown tool","Other"])
time_saved = st.selectbox("Time saved for 30 students vs previous method:", ["No time saved","30min-1hr","1-2hrs","2-4hrs","4+hrs"])

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
        st.experimental_rerun()  # Reset form inputs

# --- ANALYSIS & CHARTS ---
st.header("Survey Analysis & Results")

df = pd.read_csv(csv_file)

if not df.empty:

    # --- Method Adoption Pie Chart ---
    st.subheader("Methods Used")
    method_series = pd.Series([m.strip() for m in ','.join(df['methods']).split(',')])
    method_counts = method_series.value_counts()
    fig_methods = px.pie(values=method_counts.values, names=method_counts.index, title="Methods Used by Teachers")
    st.plotly_chart(fig_methods, use_container_width=True)
    st.download_button(
        label="Download Methods Chart (HTML)",
        data=fig_methods.to_html(),
        file_name="methods_chart.html",
        mime="text/html"
    )

    # Helper function for grouped bar charts
    def plot_grouped_bar(df, metrics, title, order=None):
        temp = df[metrics].melt(var_name="Method", value_name="Response")
        if order:
            temp["Response"] = pd.Categorical(temp["Response"], categories=order, ordered=True)
        fig = px.histogram(temp, x="Method", color="Response", barmode="group",
                           text_auto=True, category_orders={"Response": order})
        fig.update_layout(title=title, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button(
            label=f"Download '{title}' Chart (HTML)",
            data=fig.to_html(),
            file_name=f"{title.replace(' ','_')}.html",
            mime="text/html"
        )

    # --- Charts for metrics ---
    plot_grouped_bar(df, ["time_scratch","time_ai","time_school_bank","time_dropdown"], "Time per Comment Comparison",
                     order=["<30sec","<2min","2-5min","5-10min","10+min","1-2min","2+min","Did not use"])
    plot_grouped_bar(df, ["cognitive_scratch","cognitive_ai","cognitive_dropdown"], "Cognitive Effort Comparison",
                     order=["Very low","Low","Moderate","High","Exhausting","Did not use"])
    plot_grouped_bar(df, ["stress_scratch","stress_ai","stress_dropdown"], "Stress Level Comparison",
                     order=["Low","Moderate","High","Very high","Did not use"])
    plot_grouped_bar(df, ["quality_scratch","quality_ai","quality_dropdown"], "Quality Comparison",
                     order=["High & consistent","High quality but inconsistent","High & curriculum-aligned","Generally good",
                            "Good, ready to use","Acceptable","Acceptable with minor tweaks","Variable","Too generic",
                            "Too generic/not suitable","Haven't used AI","Did not use"])
    plot_grouped_bar(df, ["character_accuracy_scratch","character_accuracy_ai","character_accuracy_dropdown"], "Character Accuracy",
                     order=["Always within range","Usually within range","Sometimes exceeds range","Exceeds range","Did not use"])
    plot_grouped_bar(df, ["curriculum_alignment_scratch","curriculum_alignment_ai","curriculum_alignment_dropdown"], "Curriculum Alignment",
                     order=["Always","Usually","Sometimes","Rarely","Did not use"])

    # --- Written Summary ---
    st.subheader("Written Summary / Interpretation")
    total_respondents = len(df)
    summary = f"Total respondents: {total_respondents}\n\n"

    # Method usage counts
    for method in ["Writing from scratch","ChatGPT/AI prompts","School comment banks","Dropdown tool"]:
        count_used = method_series.str.contains(method).sum()
        summary += f"{method}: used by {count_used} teacher(s), {total_respondents - count_used} did not use.\n"

    # Time efficiency summary
    summary += "\nTime per comment (dropdown tool):\n"
    time_counts = df['time_dropdown'].value_counts()
    for k,v in time_counts.items():
        summary += f"{k}: {v} teacher(s)\n"

    # Most common cognitive relief
    relief_counts = df['biggest_cognitive_relief'].value_counts()
    top_relief = relief_counts.idxmax()
    summary += f"\nMost reported cognitive relief from dropdown tool: {top_relief}\n"

    st.text_area("Survey Summary", value=summary, height=250)
