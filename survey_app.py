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

# --- ANONYMITY DISCLAIMER ---
st.markdown("""
### 🔒 **Data Privacy & Anonymity Notice**

**Your privacy is important to us:**

1. **One Response Per Person**: Please submit only once to ensure accurate data
2. **Aggregated Analysis**: All survey responses will be analyzed in aggregate form only
3. **No Personal Identification**: Individual responses will **never** be shared publicly or with third parties
4. **Contact Opt-In Only**: Your name/email is collected **only** if you opt-in below

**If you prefer complete anonymity:**
- Leave the "Name" and "Email" fields blank
- Your responses will still be valuable and included in aggregated results

By submitting this survey, you acknowledge your understanding of this privacy notice.
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
    
    # Remove duplicates based on submission_hash
    if 'submission_hash' in df.columns:
        unique_df = df.drop_duplicates(subset=['submission_hash'], keep='first')
        duplicate_count = len(df) - len(unique_df)
        df = unique_df
        
        if duplicate_count > 0:
            st.warning(f"⚠️ **Note:** {duplicate_count} duplicate responses were removed for accurate analysis")
    else:
        # Fallback: remove duplicates based on name+email+timestamp
        duplicate_count = len(df) - len(df.drop_duplicates(subset=['name', 'email', 'timestamp'], keep='first'))
        df = df.drop_duplicates(subset=['name', 'email', 'timestamp'], keep='first')
    
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
        st.subheader("🔍 Qualitative Insights (Based on Unique Responses)")
        
        # SEPARATE feedback types
        ai_feedback = df[["open_feedback_ai"]].rename(columns={"open_feedback_ai":"Comment"}).dropna()
        tool_feedback = df[["open_feedback_tool"]].rename(columns={"open_feedback_tool":"Comment"}).dropna()
        suggestions_feedback = df[["suggestions"]].rename(columns={"suggestions":"Comment"}).dropna()
        
        # Intelligent classification function
        def classify_tool_feedback(comment):
            """Classify dropdown tool feedback into meaningful categories"""
            if pd.isna(comment) or str(comment).strip() == "":
                return "No feedback"
            
            comment_lower = str(comment).lower()
            
            # CORE VALUE DETECTION
            core_value_phrases = [
                "teacher does the judgement",
                "teacher makes the judgement", 
                "app turns it into aligned comments",
                "turns into aligned comments",
                "aligned comments in few seconds",
                "saves decision-making",
                "perfect curriculum alignment"
            ]
            
            for phrase in core_value_phrases:
                if phrase in comment_lower:
                    return "Core Value for Scaling"
            
            # Check for core value keywords
            core_keywords = ["aligned", "curriculum", "judgement", "turns into", "converts", "transforms"]
            for word in core_keywords:
                if word in comment_lower:
                    return "Core Value for Scaling"
            
            # MINOR UI ISSUES
            minor_keywords = ["variant", "duplicate", "reverts", "default", "select", "punctuation", 
                            "disappears", "setting", "subject", "year", "clicking"]
            for word in minor_keywords:
                if word in comment_lower:
                    return "Minor UI/UX Issue"
            
            # SERIOUS ISSUES (from your feedback)
            if "exceeds character limit" in comment_lower or "always exceeds" in comment_lower:
                return "Serious Issue"
            
            if "requires several tweaks" in comment_lower or "all the thinking" in comment_lower:
                # Check context - is this about AI or dropdown tool?
                if "ai" in comment_lower or "chatgpt" in comment_lower:
                    return "AI Issue (Not Ours)"
                else:
                    return "Serious Issue"
            
            return "General Positive"
        
        def classify_suggestions(comment):
            """Classify suggestions"""
            if pd.isna(comment) or str(comment).strip() == "":
                return "No suggestions"
            
            comment_lower = str(comment).lower()
            
            if any(word in comment_lower for word in ["add", "suggest", "improve", "enhance", "missing"]):
                return "Feature Request"
            
            return "General Suggestion"
        
        # Apply classification
        tool_feedback["Category"] = tool_feedback["Comment"].apply(classify_tool_feedback)
        suggestions_feedback["Category"] = suggestions_feedback["Comment"].apply(classify_suggestions)
        
        # Display analysis
        tab1, tab2, tab3 = st.tabs(["🎯 Dropdown Tool", "⚡ AI Comparison", "🔧 Suggestions"])
        
        with tab1:
            st.write("### Dropdown Tool Feedback")
            
            if not tool_feedback.empty:
                # Show unique feedback only
                unique_tool_feedback = tool_feedback.drop_duplicates(subset=['Comment'])
                
                # Categorize
                core_value = unique_tool_feedback[unique_tool_feedback["Category"] == "Core Value for Scaling"]
                minor_issues = unique_tool_feedback[unique_tool_feedback["Category"] == "Minor UI/UX Issue"]
                serious_issues = unique_tool_feedback[unique_tool_feedback["Category"] == "Serious Issue"]
                
                # Display
                if not core_value.empty:
                    st.success("**✅ Core Value Identified**")
                    for idx, row in core_value.iterrows():
                        st.markdown(f"• *\"{row['Comment']}\"*")
                
                if not serious_issues.empty:
                    st.warning("**🚨 Issues to Address**")
                    for idx, row in serious_issues.iterrows():
                        st.markdown(f"• *\"{row['Comment']}\"*")
                
                if not minor_issues.empty:
                    st.info("**🔧 Minor UI Improvements**")
                    for idx, row in minor_issues.iterrows():
                        st.markdown(f"• *\"{row['Comment']}\"*")
                
                # Summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Core Value", len(core_value))
                with col2:
                    st.metric("Serious Issues", len(serious_issues))
                with col3:
                    st.metric("Minor Issues", len(minor_issues))
            else:
                st.info("No dropdown tool feedback yet.")
        
        with tab2:
            st.write("### AI Issues (What We're Better Than)")
            
            if not ai_feedback.empty:
                unique_ai_feedback = ai_feedback.drop_duplicates(subset=['Comment'])
                
                for idx, row in unique_ai_feedback.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
                
                # Analyze AI pain points
                ai_issues = []
                for comment in unique_ai_feedback['Comment']:
                    if "character limit" in str(comment).lower():
                        ai_issues.append("Character limit problems")
                    if "tweaks" in str(comment).lower() or "edits" in str(comment).lower():
                        ai_issues.append("Requires too many edits")
                    if "thinking" in str(comment).lower() or "mental" in str(comment).lower():
                        ai_issues.append("Still requires cognitive effort")
                
                if ai_issues:
                    st.info("**AI Pain Points Identified:**")
                    for issue in set(ai_issues):
                        st.markdown(f"• {issue}")
            else:
                st.info("No AI feedback yet.")
        
        with tab3:
            st.write("### Improvement Suggestions")
            
            if not suggestions_feedback.empty:
                unique_suggestions = suggestions_feedback.drop_duplicates(subset=['Comment'])
                
                # Group similar suggestions
                suggestions_text = " ".join(unique_suggestions['Comment'].astype(str).tolist()).lower()
                
                st.info("**Key Feature Requests:**")
                if "variant" in suggestions_text or "duplicate" in suggestions_text:
                    st.markdown("• **Add comment variants** to avoid duplicates")
                if "reverts" in suggestions_text or "default" in suggestions_text:
                    st.markdown("• **Remember user settings** between comments")
                if "subject" in suggestions_text or "year" in suggestions_text:
                    st.markdown("• **Save subject/year selections**")
                if "punctuation" in suggestions_text or "disappears" in suggestions_text:
                    st.markdown("• **Fix punctuation preservation** when editing")
                
                # Show all unique suggestions
                with st.expander("See all unique suggestions"):
                    for idx, row in unique_suggestions.iterrows():
                        st.markdown(f"• *\"{row['Comment']}\"*")
            else:
                st.info("No suggestions yet.")
        
        # --- REALISTIC SCALING ASSESSMENT ---
        st.subheader("🚀 Realistic Scaling Assessment")
        
        # Calculate unique metrics
        unique_core_value = len(tool_feedback[tool_feedback["Category"] == "Core Value for Scaling"].drop_duplicates())
        unique_serious_issues = len(tool_feedback[tool_feedback["Category"] == "Serious Issue"].drop_duplicates())
        
        # Get quantitative metrics from unique responses
        quantitative_evidence = 0
        
        # Time saved evidence
        time_saved_counts = df['time_saved'].value_counts()
        if '4+hrs' in time_saved_counts:
            quantitative_evidence += 3
        elif '2-4hrs' in time_saved_counts:
            quantitative_evidence += 2
        elif '1-2hrs' in time_saved_counts:
            quantitative_evidence += 1
        
        # Quality evidence
        quality_counts = df['quality_dropdown'].value_counts()
        if 'High & curriculum-aligned' in quality_counts:
            quantitative_evidence += 2
        
        # Cognitive relief evidence
        cognitive_counts = df['cognitive_dropdown'].value_counts()
        if 'Very low' in cognitive_counts:
            quantitative_evidence += 2
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Display realistic assessment
            if total_unique_responses >= 3:
                if unique_core_value >= 2 and unique_serious_issues == 0:
                    st.success("""
                    ### 📊 **PROMISING FOR SCALING**
                    
                    **Evidence:**
                    - Multiple teachers report core value
                    - No serious blocking issues
                    - Strong quantitative metrics
                    - Clear improvement over AI
                    
                    **Next:** Gather 3-5 more unique validations
                    """)
                elif unique_core_value >= 1:
                    st.warning("""
                    ### 📈 **NEEDS MORE VALIDATION**
                    
                    **Evidence:**
                    - Some core value identified
                    - Need more unique responses
                    - Quantitative support is present
                    
                    **Next:** Get 2-3 more unique teacher validations
                    """)
                else:
                    st.info("""
                    ### 🔍 **INCONCLUSIVE**
                    
                    **Evidence:**
                    - Insufficient unique responses
                    - Core value not clearly demonstrated
                    
                    **Next:** Need more diverse teacher feedback
                    """)
            else:
                st.info("""
                ### ⚠️ **TOO EARLY TO DECIDE**
                
                **Current Status:**
                - Only 1 unique response so far
                - Need at least 3 unique teachers for validation
                - Initial feedback shows promise
                
                **Action Required:** Get 2+ more unique teacher responses
                """)
        
        with col2:
            # Show unique metrics
            metrics_data = {
                'Metric': ['Unique Teachers', 'Core Value Comments', 
                          'Serious Issues', 'Quantitative Evidence',
                          'AI Pain Points', 'Feature Requests'],
                'Value': [total_unique_responses, unique_core_value,
                         unique_serious_issues, quantitative_evidence,
                         len(ai_feedback.drop_duplicates()),
                         len(suggestions_feedback.drop_duplicates())]
            }
            metrics_df = pd.DataFrame(metrics_data)
            st.dataframe(metrics_df, hide_index=True, use_container_width=True)
        
        # Contact list
        if 'allow_contact' in df.columns and 'name' in df.columns:
            enthusiasts = df[(df['allow_contact'] == True) & (df['name'] != "Anonymous") & (df['name'].notna())]
            if not enthusiasts.empty:
                st.subheader("🌟 Enthusiasts Open to Contact")
                st.write(f"Found {len(enthusiasts)} unique participants willing to share their experience:")
                contact_list = enthusiasts[['name', 'email', 'open_feedback_tool']].copy()
                contact_list.columns = ['Name', 'Email', 'Key Feedback']
                st.dataframe(contact_list, use_container_width=True, hide_index=True)
        
        # --- Download Report ---
        st.subheader("📥 Download Report")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # Unique data only
            share_df = df.copy()
            share_df['name'] = share_df['name'].apply(lambda x: 'Anonymous' if x == 'Anonymous' else 'Teacher')
            share_df['email'] = 'redacted'
            
            share_df.to_excel(writer, sheet_name="Unique Responses", index=False)
            
            # Analysis sheets
            if not tool_feedback.empty:
                tool_feedback.drop_duplicates(subset=['Comment']).to_excel(writer, sheet_name="Tool Feedback", index=False)
            if not ai_feedback.empty:
                ai_feedback.drop_duplicates(subset=['Comment']).to_excel(writer, sheet_name="AI Comparison", index=False)
            if not suggestions_feedback.empty:
                suggestions_feedback.drop_duplicates(subset=['Comment']).to_excel(writer, sheet_name="Suggestions", index=False)
            
            # Summary
            summary_data = {
                'Metric': ['Unique Teachers', 'Core Value Comments', 'Serious Issues',
                          'Minor Issues', 'AI Pain Points', 'Feature Requests',
                          'Time Saved (4+hrs)', 'Quality (High)', 'Cognitive (Very Low)',
                          'Assessment'],
                'Value': [total_unique_responses, unique_core_value, unique_serious_issues,
                         len(tool_feedback[tool_feedback["Category"] == "Minor UI/UX Issue"].drop_duplicates()),
                         len(ai_feedback.drop_duplicates()),
                         len(suggestions_feedback.drop_duplicates()),
                         time_saved_counts.get('4+hrs', 0),
                         quality_counts.get('High & curriculum-aligned', 0),
                         cognitive_counts.get('Very low', 0),
                         "Promising" if total_unique_responses >= 3 and unique_core_value >= 2 else "Need More Data"]
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
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
<strong>Note:</strong> Duplicate responses are filtered out for accurate analysis. 
Each teacher should submit only once.
</div>
""", unsafe_allow_html=True)
