# survey_app_mvp.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import hashlib
from datetime import datetime
import io

# --- CSV setup ---
csv_file = "survey_data.csv"

columns = [
    "name",
    "email",
    "allow_contact",
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
    "submission_hash",  # New column to prevent duplicates
    "timestamp"
]

# Create CSV if it doesn't exist
if not os.path.exists(csv_file):
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

# --- Streamlit App ---
st.title("📊 Report Writing MVP Survey")
st.markdown("---")

# --- SIMPLIFIED ANONYMITY DISCLAIMER ---
st.markdown("""
**🔒 Privacy Notice:** All responses are anonymous and aggregated. 
Names/emails are optional for follow-up only.
""")
st.markdown("---")

# --- Contact Information (Optional) ---
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Your Name (optional - for follow-up only)")
with col2:
    email = st.text_input("Email (optional - for product updates only)")

allow_contact = st.checkbox(
    "I'm open to follow-up contact about my experience (optional)",
    help="Check this if you're willing to participate in brief follow-up interviews or share your experience"
)

st.markdown("---")

# --- Survey Questions ---
st.write("""
### Survey Questions
**Purpose:** Collect teacher experience to validate the MVP, identify strengths, and guide improvements.
""")

methods = st.multiselect(
    "Which methods have you used to write report comments?",
    ["Writing from scratch", "ChatGPT/AI prompts", "School comment banks", "Previous year's comments", "Dropdown tool", "Other"]
)

# Time questions
col1, col2, col3, col4 = st.columns(4)
with col1:
    time_scratch = st.selectbox("From scratch - Time:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
with col2:
    time_ai = st.selectbox("AI prompts - Time:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
with col3:
    time_school_bank = st.selectbox("School banks - Time:", ["<2min","2-5min","5-10min","10+min","Didn't use"])
with col4:
    time_dropdown = st.selectbox("Dropdown tool - Time:", ["<30sec","30sec-1min","1-2min","2+min","Didn't use"])

# Cognitive effort
st.subheader("Mental Effort Comparison")
col1, col2, col3 = st.columns(3)
with col1:
    cognitive_scratch = st.selectbox("From scratch - Mental effort:", ["Exhausting","High","Moderate","Low","Didn't use"])
with col2:
    cognitive_ai = st.selectbox("AI prompts - Mental effort:", ["Exhausting","High","Moderate","Low","Didn't use"])
with col3:
    cognitive_dropdown = st.selectbox("Dropdown tool - Mental effort:", ["Very low","Low","Moderate","High","Didn't use"])

# Quality comparison
st.subheader("Output Quality Comparison")
col1, col2, col3 = st.columns(3)
with col1:
    quality_scratch = st.selectbox("From scratch - Quality:", ["High quality and consistent","High quality but inconsistent","Generally good","Variable","Often rushed/generic","Didn't use"])
with col2:
    quality_ai = st.selectbox("AI prompts - Quality:", ["High after edits","Good with minor tweaks","Acceptable","Too generic/not suitable","Haven't used AI","Didn't use"])
with col3:
    quality_dropdown = st.selectbox("Dropdown tool - Quality:", ["High & curriculum-aligned","Good, ready to use","Acceptable with minor tweaks","Too generic","Didn't use"])

# Character accuracy
st.subheader("Character Count Accuracy")
col1, col2, col3 = st.columns(3)
with col1:
    character_accuracy_scratch = st.selectbox("From scratch - Accuracy:", ["Within range","Exceeds range","Didn't use"])
with col2:
    character_accuracy_ai = st.selectbox("AI prompts - Accuracy:", ["Within range","Exceeds range","Didn't use"])
with col3:
    character_accuracy_dropdown = st.selectbox("Dropdown tool - Accuracy:", ["Within range","Exceeds range","Didn't use"])

# Curriculum alignment
st.subheader("Curriculum Alignment")
col1, col2, col3 = st.columns(3)
with col1:
    curriculum_alignment_scratch = st.selectbox("From scratch - Alignment:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
with col2:
    curriculum_alignment_ai = st.selectbox("AI prompts - Alignment:", ["Always","Usually","Sometimes","Rarely","Didn't use"])
with col3:
    curriculum_alignment_dropdown = st.selectbox("Dropdown tool - Alignment:", ["Always","Usually","Sometimes","Rarely","Didn't use"])

# Stress levels
st.subheader("Stress Level Comparison")
col1, col2, col3 = st.columns(3)
with col1:
    stress_scratch = st.selectbox("From scratch - Stress:", ["Very high","High","Moderate","Low","Didn't use"])
with col2:
    stress_ai = st.selectbox("AI prompts - Stress:", ["Very high","High","Moderate","Low","Didn't use"])
with col3:
    stress_dropdown = st.selectbox("Dropdown tool - Stress:", ["Very high","High","Moderate","Low","Didn't use"])

# Specific benefits
st.subheader("Specific Benefits of Dropdown Tool")
col1, col2, col3 = st.columns(3)
with col1:
    biggest_cognitive_relief = st.selectbox("Biggest cognitive relief:", [
        "No need to decide what to include/exclude",
        "Character count automatically perfect",
        "No rephrasing/editing needed",
        "Curriculum-aligned language pre-written",
        "Clear structure removes blank page stress",
        "Consistency across all students",
        "Didn't use"
    ])
with col2:
    biggest_time_quality = st.selectbox("Best time-to-quality ratio:", [
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
st.subheader("Qualitative Feedback")
st.markdown("*Please be specific - this helps us improve the tool*")

open_feedback_ai = st.text_area(
    "What's ONE specific thing AI does WRONG?",
    placeholder="e.g., 'Exceeds character limit', 'Requires too many edits', 'Too generic for our curriculum'"
)

open_feedback_tool = st.text_area(
    "What's the BIGGEST benefit of the dropdown tool?",
    placeholder="e.g., 'Saves decision-making time', 'Fast and accurate', 'Perfect curriculum alignment'"
)

suggestions = st.text_area(
    "What's ONE specific improvement that would make this tool better?",
    placeholder="e.g., 'Add comment variants', 'Fix the character limit issue', 'Save user preferences'"
)

st.markdown("---")

# --- Save to CSV with duplicate prevention ---
if st.button("✅ Submit Survey"):
    # Validate at least some methods selected
    if not methods:
        st.error("Please select at least one method you've used")
    else:
        # Create a hash to identify potential duplicates
        feedback_hash = hashlib.md5(
            f"{name}{email}{open_feedback_ai}{open_feedback_tool}{suggestions}".encode()
        ).hexdigest()
        
        df = pd.read_csv(csv_file)
        
        # Check for duplicates (same person submitting similar feedback)
        is_duplicate = False
        if 'submission_hash' in df.columns:
            is_duplicate = feedback_hash in df['submission_hash'].values
        
        if is_duplicate:
            st.warning("""
            ### ⚠️ Duplicate Submission Detected
            
            It looks like you've already submitted this survey. 
            
            **Please note:** Only one submission per person is allowed to ensure data accuracy.
            
            If you want to update your feedback, please contact us directly.
            """)
        else:
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
                "submission_hash": feedback_hash,
                "timestamp": timestamp
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(csv_file, index=False)
            
            # Thank you message
            st.success("""
            ### Thank you for your valuable feedback! 🎉
            
            **Your response has been recorded successfully.**
            
            **Next steps:**
            - We'll analyze all feedback to identify improvements
            - If you opted in for contact, we may reach out for a brief follow-up
            - Watch for product updates based on teacher feedback
            """)
            
            # Show what was saved
            if allow_contact and name:
                st.info(f"📧 *Note: You've opted in for follow-up contact as '{name}'*")
            else:
                st.info("🔒 *Your response is recorded anonymously*")

# --- Enhanced Analysis Dashboard ---
st.markdown("---")
st.header("📈 MVP Insights Dashboard")

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 10:
    df = pd.read_csv(csv_file)
    
    # FIXED: Handle missing columns gracefully
    duplicate_count = 0
    
    # Remove duplicates based on submission_hash if it exists
    if 'submission_hash' in df.columns:
        unique_df = df.drop_duplicates(subset=['submission_hash'], keep='first')
        duplicate_count = len(df) - len(unique_df)
        df = unique_df
    
    # Show response count (unique)
    total_unique_responses = len(df)
    opt_in_count = df['allow_contact'].sum() if 'allow_contact' in df.columns else 0
    
    st.metric("Total Unique Responses", total_unique_responses, 
              f"{opt_in_count} opted for contact")
    
    if duplicate_count > 0:
        st.caption(f"*({duplicate_count} duplicates removed)*")
    
    # Check if we have enough data
    if total_unique_responses < 1:
        st.info("Not enough unique data yet. Submit the first response to see insights!")
    else:
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
                        "Time Efficiency Comparison")
        with col2:
            create_chart(["cognitive_scratch","cognitive_ai","cognitive_dropdown"], 
                        "Cognitive Load Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            create_chart(["quality_scratch","quality_ai","quality_dropdown"], 
                        "Output Quality Comparison")
        with col2:
            create_chart(["stress_scratch","stress_ai","stress_dropdown"], 
                        "Stress Level Comparison")
        
        # --- ACCURATE QUALITATIVE ANALYSIS ---
        st.subheader("🔍 Qualitative Insights")
        
        # SEPARATE feedback types
        ai_feedback = df[["open_feedback_ai"]].rename(columns={"open_feedback_ai":"Comment"}).dropna()
        tool_feedback = df[["open_feedback_tool"]].rename(columns={"open_feedback_tool":"Comment"}).dropna()
        suggestions_feedback = df[["suggestions"]].rename(columns={"suggestions":"Comment"}).dropna()
        
        # Simple classification function
        def classify_tool_feedback(comment):
            """Classify dropdown tool feedback"""
            if pd.isna(comment) or str(comment).strip() == "":
                return "No feedback"
            
            comment_lower = str(comment).lower()
            
            # Core value detection
            if any(phrase in comment_lower for phrase in [
                "teacher does the judgement", "teacher makes the judgement", 
                "turns into aligned comments", "aligned comments", "curriculum aligned"
            ]):
                return "Core Value"
            
            # Issues
            if "character limit" in comment_lower or "exceeds" in comment_lower:
                return "Issue"
            
            return "Positive"
        
        # Apply classification
        tool_feedback["Category"] = tool_feedback["Comment"].apply(classify_tool_feedback)
        
        # Display analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Dropdown Tool Value**")
            core_value = tool_feedback[tool_feedback["Category"] == "Core Value"]
            if not core_value.empty:
                for idx, row in core_value.iterrows():
                    st.info(f"✓ {row['Comment'][:50]}...")
            else:
                st.info("No core value feedback yet")
        
        with col2:
            st.write("**AI Issues (Comparison)**")
            if not ai_feedback.empty:
                for idx, row in ai_feedback.iterrows():
                    st.warning(f"✗ {row['Comment'][:50]}...")
            else:
                st.info("No AI feedback yet")
        
        with col3:
            st.write("**Improvement Ideas**")
            if not suggestions_feedback.empty:
                # Get unique suggestions
                suggestions_list = suggestions_feedback['Comment'].unique()
                for suggestion in suggestions_list[:3]:  # Show first 3
                    st.caption(f"• {str(suggestion)[:40]}...")
            else:
                st.info("No suggestions yet")
        
        # --- SIMPLE SCALING ASSESSMENT ---
        st.subheader("🚀 Scaling Assessment")
        
        # Calculate metrics
        core_value_count = len(tool_feedback[tool_feedback["Category"] == "Core Value"])
        issue_count = len(tool_feedback[tool_feedback["Category"] == "Issue"])
        
        # Quantitative metrics
        time_saved_good = df['time_saved'].isin(['2-4hrs', '4+hrs']).any()
        quality_good = df['quality_dropdown'].isin(['High & curriculum-aligned', 'Good, ready to use']).any()
        cognitive_good = df['cognitive_dropdown'].isin(['Very low', 'Low']).any()
        
        # Simple decision logic
        if total_unique_responses >= 3:
            if core_value_count >= 2 and not time_saved_good and quality_good:
                st.success("**✅ Strong case for scaling**")
                st.write("Multiple teachers report core value with good metrics")
            elif core_value_count >= 1:
                st.warning("**⚠️ Promising but needs more validation**")
                st.write("Initial positive feedback, gather more responses")
            else:
                st.info("**🔍 Needs more positive feedback**")
                st.write("Focus on demonstrating core value")
        else:
            st.info(f"**📊 Gathering data: {total_unique_responses}/3 teachers**")
            st.write(f"Core value mentions: {core_value_count}")
            st.write(f"Time saved (2+ hrs): {'Yes' if time_saved_good else 'No'}")
            st.write(f"Quality good: {'Yes' if quality_good else 'No'}")
        
        # Contact list
        if 'allow_contact' in df.columns and 'name' in df.columns:
            enthusiasts = df[(df['allow_contact'] == True) & (df['name'] != "Anonymous")]
            if not enthusiasts.empty:
                st.subheader("🌟 Enthusiasts Open to Contact")
                contact_list = enthusiasts[['name', 'email']].copy()
                contact_list.columns = ['Name', 'Email']
                st.dataframe(contact_list, use_container_width=True, hide_index=True)
        
        # --- Download Report ---
        st.subheader("📥 Download Report")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # Data
            df.to_excel(writer, sheet_name="Data", index=False)
            
            # Summary
            summary_data = {
                'Metric': ['Unique Teachers', 'Core Value', 'AI Issues', 
                          'Time Saved (2+ hrs)', 'Quality Good', 'Cognitive Low',
                          'Assessment'],
                'Value': [total_unique_responses, core_value_count, len(ai_feedback),
                         'Yes' if time_saved_good else 'No',
                         'Yes' if quality_good else 'No',
                         'Yes' if cognitive_good else 'No',
                         'Promising' if core_value_count > 0 else 'Needs Work']
            }
            
            pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
            
            writer.close()
            processed_data = output.getvalue()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="📊 Download Analysis Report",
            data=processed_data,
            file_name=f"mvp_analysis_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No survey data yet. Submit the first response to see insights!")

# --- Footer ---
st.markdown("---")
st.caption("🔒 Responses are anonymous and aggregated. One submission per person.")
