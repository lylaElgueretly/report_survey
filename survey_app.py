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

# --- INSIGHTFUL Analysis Dashboard ---
st.markdown("---")
st.header("📈 MVP Insights Dashboard")

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 10:
    df = pd.read_csv(csv_file)
    
    # Remove duplicate rows
    initial_count = len(df)
    df = df.drop_duplicates(keep='first')
    duplicate_count = initial_count - len(df)
    
    total_responses = len(df)
    opt_in_count = df['allow_contact'].sum() if 'allow_contact' in df.columns else 0
    
    st.metric("📊 Unique Teacher Responses", total_responses, f"{opt_in_count} open to contact")
    
    if total_responses > 0:
        # --- QUANTITATIVE INSIGHTS ---
        st.subheader("📈 Quantitative Evidence")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            time_saved_4plus = (df['time_saved'] == '4+hrs').sum()
            time_saved_2plus = (df['time_saved'].isin(['2-4hrs', '4+hrs'])).sum()
            st.metric("⏱️ Time Saved", f"{time_saved_4plus}/{total_responses}", 
                     f"{time_saved_2plus} saved 2+ hrs")
        
        with col2:
            quality_high = (df['quality_dropdown'] == 'High & curriculum-aligned').sum()
            quality_good = (df['quality_dropdown'].isin(['High & curriculum-aligned', 'Good, ready to use'])).sum()
            st.metric("⭐ Output Quality", f"{quality_high}/{total_responses} High", 
                     f"{quality_good} Good+")
        
        with col3:
            cognitive_low = (df['cognitive_dropdown'] == 'Very low').sum()
            cognitive_vlow = (df['cognitive_dropdown'].isin(['Very low', 'Low'])).sum()
            st.metric("🧠 Mental Effort", f"{cognitive_low}/{total_responses} Very Low", 
                     f"{cognitive_vlow} Low+")
        
        with col4:
            alignment_always = (df['curriculum_alignment_dropdown'] == 'Always').sum()
            st.metric("🎯 Curriculum Alignment", f"{alignment_always}/{total_responses} Always", 
                     "Perfect alignment")
        
        # --- QUALITATIVE INSIGHTS WITH ANALYSIS ---
        st.subheader("🔍 Qualitative Insights")
        
        # Get UNIQUE feedback (remove duplicates)
        ai_feedback = df["open_feedback_ai"].dropna().unique().tolist()
        tool_feedback = df["open_feedback_tool"].dropna().unique().tolist()
        suggestions_list = df["suggestions"].dropna().unique().tolist()
        
        # Analyze dropdown tool value
        st.write("### 🎯 **Core Value for Scaling**")
        
        core_value_found = False
        if tool_feedback:
            # Check for core value phrases
            core_value_keywords = [
                "judgement", "turns into", "aligned comments", "curriculum", 
                "seconds", "few seconds", "fast", "quick", "saves"
            ]
            
            for feedback in tool_feedback:
                feedback_lower = str(feedback).lower()
                if any(keyword in feedback_lower for keyword in core_value_keywords):
                    core_value_found = True
                    st.success(f"""
                    **✅ Core Value Identified:**
                    *"{feedback}"*
                    
                    **What this means:** Teacher provides judgement → Tool creates curriculum-aligned comments instantly
                    """)
                    break
            
            if not core_value_found and tool_feedback:
                st.info(f"**General positive feedback:** {tool_feedback[0]}")
        else:
            st.info("No dropdown tool feedback yet")
        
        # Compare against AI
        st.write("### ⚡ **Comparison vs AI**")
        
        if ai_feedback:
            # Analyze AI pain points
            ai_pain_points = []
            for feedback in ai_feedback:
                feedback_lower = str(feedback).lower()
                if "character limit" in feedback_lower or "exceeds" in feedback_lower:
                    ai_pain_points.append("Character limit issues")
                if "tweaks" in feedback_lower or "edits" in feedback_lower:
                    ai_pain_points.append("Requires many edits")
                if "thinking" in feedback_lower or "mental" in feedback_lower:
                    ai_pain_points.append("Still requires cognitive effort")
            
            if ai_pain_points:
                st.warning(f"""
                **AI Limitations Found:**
                {', '.join(set(ai_pain_points))}
                
                **Our advantage:** These are problems our dropdown tool solves
                """)
            else:
                st.info(f"AI feedback: {ai_feedback[0]}")
        else:
            st.info("No AI comparison feedback yet")
        
        # Analyze suggestions
        st.write("### 🔧 **Improvement Opportunities**")
        
        if suggestions_list:
            # Group and categorize suggestions
            categorized_suggestions = {
                "UI/UX Improvements": [],
                "Feature Requests": [],
                "Bug Fixes": []
            }
            
            for suggestion in suggestions_list:
                suggestion_lower = str(suggestion).lower()
                
                if any(word in suggestion_lower for word in ["variant", "duplicate", "different"]):
                    categorized_suggestions["Feature Requests"].append("Add comment variants to avoid duplicates")
                
                if any(word in suggestion_lower for word in ["reverts", "default", "reset", "setting"]):
                    categorized_suggestions["UI/UX Improvements"].append("Remember user settings between comments")
                
                if any(word in suggestion_lower for word in ["select", "subject", "year", "every comment"]):
                    categorized_suggestions["UI/UX Improvements"].append("Save subject/year selections")
                
                if any(word in suggestion_lower for word in ["punctuation", "disappears", "typing"]):
                    categorized_suggestions["Bug Fixes"].append("Fix punctuation when editing comments")
            
            # Display categorized suggestions
            for category, items in categorized_suggestions.items():
                if items:
                    unique_items = list(set(items))  # Remove duplicates
                    st.info(f"**{category}:**")
                    for item in unique_items:
                        st.caption(f"• {item}")
        else:
            st.info("No suggestions yet")
        
        # --- SCALING ASSESSMENT ---
        st.subheader("🚀 **Scaling Readiness Assessment**")
        
        # Calculate evidence
        quantitative_evidence = 0
        if time_saved_4plus > 0:
            quantitative_evidence += 2
        if quality_high > 0:
            quantitative_evidence += 2
        if cognitive_low > 0:
            quantitative_evidence += 1
        
        qualitative_evidence = 1 if core_value_found else 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            if total_responses >= 3:
                if core_value_found and quantitative_evidence >= 3:
                    st.success("""
                    ### ✅ **STRONG CASE FOR SCALING**
                    
                    **Evidence:**
                    • Core value clearly demonstrated
                    • Strong quantitative metrics
                    • Clear advantage over AI
                    • Multiple teacher validations
                    
                    **Recommendation:** Scale with confidence
                    """)
                elif core_value_found:
                    st.warning("""
                    ### ⚠️ **PROMISING, NEEDS MORE VALIDATION**
                    
                    **Evidence:**
                    • Core value identified
                    • Some quantitative support
                    • Need more responses
                    
                    **Next:** Gather 2-3 more validations
                    """)
                else:
                    st.info("""
                    ### 🔍 **NEEDS MORE EVIDENCE**
                    
                    **Status:**
                    • Core value not clearly shown
                    • Need stronger feedback
                    
                    **Action:** Focus on demonstrating value
                    """)
            else:
                st.info(f"""
                ### 📊 **GATHERING DATA: {total_responses}/3 Teachers**
                
                **Current evidence:**
                • Core value: {'✅ Found' if core_value_found else '❓ Not yet'}
                • Time savings: {time_saved_4plus}/{total_responses} report 4+ hrs
                • Quality: {quality_high}/{total_responses} report High quality
                
                **Need:** {3 - total_responses} more unique teacher responses
                """)
        
        with col2:
            # Evidence summary
            evidence_data = {
                'Evidence Type': ['Core Value Found', '4+ Hours Saved', 
                                'High Quality', 'Low Cognitive Effort',
                                'AI Comparison', 'Total Teachers'],
                'Status': [
                    '✅ Yes' if core_value_found else '❓ No',
                    f'{time_saved_4plus}/{total_responses}',
                    f'{quality_high}/{total_responses}',
                    f'{cognitive_low}/{total_responses}',
                    '✅ Advantage' if ai_feedback else '❓ No data',
                    total_responses
                ]
            }
            
            st.dataframe(pd.DataFrame(evidence_data), hide_index=True, use_container_width=True)
        
        # Contact list
        if 'allow_contact' in df.columns and 'name' in df.columns:
            enthusiasts = df[(df['allow_contact'] == True) & (df['name'] != "Anonymous")]
            if not enthusiasts.empty:
                st.subheader("🌟 Enthusiasts Open to Contact")
                st.dataframe(enthusiasts[['name', 'email']].rename(
                    columns={'name': 'Name', 'email': 'Email'}), 
                    hide_index=True)
        
        # --- Download Report ---
        st.subheader("📥 Download Report")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Data", index=False)
            
            summary_data = {
                'Assessment Metric': ['Unique Teachers', 'Core Value Demonstrated',
                                    'Time Savings (4+ hrs)', 'High Quality Output',
                                    'Low Cognitive Effort', 'AI Limitations Found',
                                    'Scaling Readiness'],
                'Value': [total_responses,
                         'Yes' if core_value_found else 'No',
                         f'{time_saved_4plus}/{total_responses}',
                         f'{quality_high}/{total_responses}',
                         f'{cognitive_low}/{total_responses}',
                         len(ai_feedback),
                         'Strong' if core_value_found and time_saved_4plus > 0 else 'Needs More']
            }
            
            pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
            writer.close()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="📊 Download Analysis Report",
            data=output.getvalue(),
            file_name=f"mvp_scaling_assessment_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No survey data yet. Submit the first response to see insights!")

# --- Footer ---
st.markdown("---")
st.caption("🔒 Anonymous survey - One submission per person recommended")
