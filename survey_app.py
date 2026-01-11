# survey_app_mvp.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import io

# --- CSV setup ---
csv_file = "survey_data.csv"

columns = [
    "name", "email", "allow_contact", "methods",
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

# Create CSV if it doesn't exist
if not os.path.exists(csv_file):
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

# --- Streamlit App ---
st.title("📊 Report Writing MVP Survey")

# --- Simple Privacy Notice ---
st.info("**🔒 Anonymous survey - Names/emails optional for follow-up only.**")
st.markdown("---")

# --- Contact Information ---
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Name (optional)")
with col2:
    email = st.text_input("Email (optional)")

allow_contact = st.checkbox("Open to follow-up contact (optional)")
st.markdown("---")

# --- Survey Questions ---
st.write("**Purpose:** Validate MVP and guide improvements.")

methods = st.multiselect(
    "Methods you've used:",
    ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", 
     "Previous year's comments", "Dropdown tool", "Other"]
)

# Time comparison
st.subheader("Time per Comment")
col1, col2, col3, col4 = st.columns(4)
with col1:
    time_scratch = st.selectbox("From scratch:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
with col2:
    time_ai = st.selectbox("AI prompts:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
with col3:
    time_school_bank = st.selectbox("School banks:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
with col4:
    time_dropdown = st.selectbox("Dropdown tool:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])

# Cognitive effort
st.subheader("Mental Effort")
col1, col2, col3 = st.columns(3)
with col1:
    cognitive_scratch = st.selectbox("From scratch:", ["Exhausting","High","Moderate","Low","Didn't use"])
with col2:
    cognitive_ai = st.selectbox("AI prompts:", ["Exhausting","High","Moderate","Low","Didn't use"])
with col3:
    cognitive_dropdown = st.selectbox("Dropdown tool:", ["Very low","Low","Moderate","High","Didn't use"])

# Quality
st.subheader("Output Quality")
col1, col2, col3 = st.columns(3)
with col1:
    quality_scratch = st.selectbox("From scratch:", ["High quality and consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic","Didn't use"])
with col2:
    quality_ai = st.selectbox("AI prompts:", ["High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI","Didn't use"])
with col3:
    quality_dropdown = st.selectbox("Dropdown tool:", ["High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic","Didn't use"])

# Character accuracy
st.subheader("Character Accuracy")
col1, col2, col3 = st.columns(3)
with col1:
    character_accuracy_scratch = st.selectbox("From scratch:", ["Within range","Exceeds range","Didn't use"])
with col2:
    character_accuracy_ai = st.selectbox("AI prompts:", ["Within range","Exceeds range","Didn't use"])
with col3:
    character_accuracy_dropdown = st.selectbox("Dropdown tool:", ["Within range","Exceeds range","Didn't use"])

# Curriculum alignment
st.subheader("Curriculum Alignment")
col1, col2, col3 = st.columns(3)
with col1:
    curriculum_alignment_scratch = st.selectbox("From scratch:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
with col2:
    curriculum_alignment_ai = st.selectbox("AI prompts:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
with col3:
    curriculum_alignment_dropdown = st.selectbox("Dropdown tool:", ["Always","Usually","Sometimes","Rarely","Didn't use"])

# Stress levels
st.subheader("Stress Level")
col1, col2, col3 = st.columns(3)
with col1:
    stress_scratch = st.selectbox("From scratch:", ["Very high","High","Moderate","Low","Didn't use"])
with col2:
    stress_ai = st.selectbox("AI prompts:", ["Very high","High","Moderate","Low","Didn't use"])
with col3:
    stress_dropdown = st.selectbox("Dropdown tool:", ["Very high","High","Moderate","Low","Didn't use"])

# Specific benefits
st.subheader("Dropdown Tool Benefits")
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
        "No time saved",
        "30min-1hr",
        "1-2hrs",
        "2-4hrs",
        "4+hrs",
        "Didn't use"
    ])

# Open feedback
st.subheader("Feedback")
open_feedback_ai = st.text_area("One thing AI does WRONG:")
open_feedback_tool = st.text_area("One thing dropdown tool does BETTER:")
suggestions = st.text_area("Suggestions for improvement:")

st.markdown("---")

# --- Save to CSV ---
if st.button("✅ Submit Survey"):
    if not methods:
        st.error("Please select at least one method")
    else:
        df = pd.read_csv(csv_file)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {
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
            "suggestions": suggestions,
            "timestamp": timestamp
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        
        st.success("✅ Thank you for your feedback!")
        if allow_contact and name:
            st.info(f"📧 Follow-up contact enabled for '{name}'")

# --- Analysis Dashboard ---
st.markdown("---")
st.header("📈 MVP Insights Dashboard")

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 10:
    df = pd.read_csv(csv_file)
    
    # Simple duplicate removal - check for identical rows
    initial_count = len(df)
    df = df.drop_duplicates(keep='first')
    duplicate_count = initial_count - len(df)
    
    total_responses = len(df)
    opt_in_count = df['allow_contact'].sum() if 'allow_contact' in df.columns else 0
    
    st.metric("Total Responses", total_responses, f"{opt_in_count} opted for contact")
    if duplicate_count > 0:
        st.caption(f"*({duplicate_count} duplicates removed)*")
    
    if total_responses > 0:
        # Quantitative charts
        def create_chart(columns, title):
            temp = df[columns].melt(var_name="Method", value_name="Response")
            temp['Method'] = temp['Method'].str.replace('_', ' ').str.title()
            fig = px.histogram(temp, x="Method", color="Response", barmode="group", 
                              text_auto=True, title=title, height=400)
            fig.update_layout(xaxis_title="Method", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            create_chart(["time_scratch","time_ai","time_school_bank","time_dropdown"], 
                        "Time Efficiency")
        with col2:
            create_chart(["cognitive_scratch","cognitive_ai","cognitive_dropdown"], 
                        "Mental Effort")
        
        # Qualitative analysis
        st.subheader("🔍 Qualitative Insights")
        
        # Collect feedback
        ai_feedback = df["open_feedback_ai"].dropna().tolist()
        tool_feedback = df["open_feedback_tool"].dropna().tolist()
        suggestions_list = df["suggestions"].dropna().tolist()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Dropdown Tool Value**")
            if tool_feedback:
                for feedback in tool_feedback[:3]:  # Show first 3
                    st.info(f"✓ {str(feedback)[:60]}...")
            else:
                st.info("No feedback yet")
        
        with col2:
            st.write("**AI Issues**")
            if ai_feedback:
                for feedback in ai_feedback[:3]:
                    st.warning(f"✗ {str(feedback)[:60]}...")
            else:
                st.info("No feedback yet")
        
        with col3:
            st.write("**Suggestions**")
            if suggestions_list:
                for suggestion in suggestions_list[:3]:
                    st.caption(f"• {str(suggestion)[:50]}...")
            else:
                st.info("No suggestions yet")
        
        # Simple scaling assessment
        st.subheader("🚀 Scaling Assessment")
        
        # Calculate metrics
        core_value_count = sum(1 for f in tool_feedback if any(word in str(f).lower() 
                            for word in ["aligned", "curriculum", "judgement", "turns into"]))
        
        time_saved_good = df['time_saved'].isin(['2-4hrs', '4+hrs']).sum()
        quality_good = df['quality_dropdown'].isin(['High & curriculum-aligned', 'Good, ready to use']).sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if total_responses >= 3:
                if core_value_count >= 2 and time_saved_good >= 2 and quality_good >= 2:
                    st.success("**✅ Strong case for scaling**")
                    st.write("Multiple validations with good metrics")
                elif core_value_count >= 1:
                    st.warning("**⚠️ Promising but needs more**")
                    st.write("Initial positive signals")
                else:
                    st.info("**🔍 Needs more validation**")
            else:
                st.info(f"**📊 Gathering data: {total_responses}/3 teachers**")
        
        with col2:
            metrics_data = {
                'Metric': ['Teachers', 'Core Value', 'Time Saved (2+ hrs)', 'Quality Good'],
                'Value': [total_responses, core_value_count, time_saved_good, quality_good]
            }
            st.dataframe(pd.DataFrame(metrics_data), hide_index=True)
        
        # Contact list
        if 'allow_contact' in df.columns and 'name' in df.columns:
            enthusiasts = df[(df['allow_contact'] == True) & (df['name'] != "Anonymous")]
            if not enthusiasts.empty:
                st.subheader("🌟 Enthusiasts Open to Contact")
                st.dataframe(enthusiasts[['name', 'email']], hide_index=True)
        
        # Download
        st.subheader("📥 Download Report")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Data", index=False)
            
            summary_data = {
                'Metric': ['Total Responses', 'Core Value Feedback', 'AI Issues Found',
                          'Time Saved (Good)', 'Quality (Good)', 'Assessment'],
                'Value': [total_responses, core_value_count, len(ai_feedback),
                         time_saved_good, quality_good,
                         'Strong' if core_value_count >= 2 else 'Needs More']
            }
            
            pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
            writer.close()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download Excel Report",
            data=output.getvalue(),
            file_name=f"mvp_report_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No survey data yet. Submit the first response to see insights!")

# --- Footer ---
st.markdown("---")
st.caption("🔒 Anonymous survey - One submission per person recommended")
