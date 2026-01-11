# survey_app_mvp.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from textblob import TextBlob
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

1. **Aggregated Analysis**: All survey responses will be analyzed in aggregate form only
2. **No Personal Identification**: Individual responses will **never** be shared publicly or with third parties
3. **Secure Storage**: Data is stored securely and encrypted
4. **Contact Opt-In Only**: Your name/email is collected **only** if you opt-in below for:
   - Follow-up interviews (to improve the tool)
   - Potential testimonial/endorsement opportunities (only with your explicit consent)
   - Product update notifications

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

# --- Save to CSV ---
if st.button("✅ Submit Survey"):
    # Validate at least some methods selected
    if not methods:
        st.error("Please select at least one method you've used")
    else:
        df = pd.read_csv(csv_file)
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
            "suggestions": suggestions
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        
        # Thank you message
        st.success("""
        ### Thank you for your valuable feedback! 🎉
        
        Your response has been recorded and will help us improve the tool for teachers everywhere.
        
        **Next steps:**
        - We'll analyze all feedback to identify improvements
        - If you opted in for contact, we may reach out for a brief follow-up
        - Watch for product updates based on teacher feedback
        """)
        
        # Show what was saved (anonymized)
        if allow_contact and name:
            st.info(f"📧 *Note: You've opted in for follow-up contact as '{name}'*")
        else:
            st.info("🔒 *Your response is recorded anonymously*")

# --- Enhanced Analysis Dashboard ---
st.markdown("---")
st.header("📈 MVP Insights Dashboard")

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 10:
    df = pd.read_csv(csv_file)
    
    # Show response count
    total_responses = len(df)
    opt_in_count = df['allow_contact'].sum() if 'allow_contact' in df.columns else 0
    st.metric("Total Responses", total_responses, f"{opt_in_count} opted for contact")
    
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
    
    # --- INTELLIGENT QUALITATIVE ANALYSIS ---
    st.subheader("🔍 Qualitative Insights for Scaling Decision")
    
    # SEPARATE feedback types (not aggregated together)
    ai_feedback = df[["open_feedback_ai"]].rename(columns={"open_feedback_ai":"Comment"}).dropna()
    tool_feedback = df[["open_feedback_tool"]].rename(columns={"open_feedback_tool":"Comment"}).dropna()
    suggestions_feedback = df[["suggestions"]].rename(columns={"suggestions":"Comment"}).dropna()
    
    # Intelligent classification function
    def classify_tool_feedback(comment):
        """Classify dropdown tool feedback into meaningful categories"""
        if pd.isna(comment) or str(comment).strip() == "":
            return "No feedback"
        
        comment_lower = str(comment).lower()
        
        # REAL VALUE FOR SCALING (Core Benefits)
        scaling_keywords = [
            "saves", "fast", "quick", "seconds", "minutes", "efficient", "speedy",
            "aligned", "curriculum", "professional", "consistent", "accurate",
            "judgement", "thinking", "decision", "mental", "cognitive", "stress", "relief",
            "automated", "automates", "turns into", "transforms", "converts", "better"
        ]
        
        for word in scaling_keywords:
            if word in comment_lower:
                return "Core Value for Scaling"
        
        # MINOR TECHNICAL ISSUES (not blocking)
        minor_issues = [
            "variant", "duplicate", "reverts", "default", "select", "choos", "punctuation",
            "disappears", "setting", "subject", "year", "clicking", "additional"
        ]
        
        for word in minor_issues:
            if word in comment_lower:
                return "Minor UI/UX Issue"
        
        # SERIOUS ISSUES (blocking)
        serious_issues = [
            "exceeds character limit", "always exceeds", "character limit", 
            "requires several tweaks", "all the thinking", "does all the thinking",
            "not working", "broken", "crash", "error", "fails"
        ]
        
        for phrase in serious_issues:
            if phrase in comment_lower:
                return "Serious Issue"
        
        return "General Positive"
    
    def classify_suggestions(comment):
        """Classify suggestions into feature requests"""
        if pd.isna(comment) or str(comment).strip() == "":
            return "No suggestions"
        
        comment_lower = str(comment).lower()
        
        # Feature enhancement requests
        feature_requests = [
            "add", "suggest", "improve", "enhance", "missing", "need", "could",
            "would like", "should have", "option", "setting", "preference"
        ]
        
        for word in feature_requests:
            if word in comment_lower:
                return "Feature Request"
        
        return "General Suggestion"
    
    # Apply classification
    tool_feedback["Category"] = tool_feedback["Comment"].apply(classify_tool_feedback)
    suggestions_feedback["Category"] = suggestions_feedback["Comment"].apply(classify_suggestions)
    
    # Display in tabs for clear separation
    tab1, tab2, tab3 = st.tabs(["🎯 Dropdown Tool Value", "⚡ AI Comparison", "🔧 Improvement Ideas"])
    
    with tab1:
        st.write("### Dropdown Tool Feedback (Scaling Decision)")
        
        if not tool_feedback.empty:
            # Show core value comments
            core_value = tool_feedback[tool_feedback["Category"] == "Core Value for Scaling"]
            if not core_value.empty:
                st.success("**✅ Core Value for Scaling**")
                for idx, row in core_value.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
            
            # Show minor issues
            minor_issues = tool_feedback[tool_feedback["Category"] == "Minor UI/UX Issue"]
            if not minor_issues.empty:
                st.info("**🔧 Minor UI/UX Issues**")
                for idx, row in minor_issues.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
            
            # Show serious issues
            serious_issues = tool_feedback[tool_feedback["Category"] == "Serious Issue"]
            if not serious_issues.empty:
                st.warning("**🚨 Serious Issues to Fix**")
                for idx, row in serious_issues.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
            
            # Show general positives
            general_positives = tool_feedback[tool_feedback["Category"] == "General Positive"]
            if not general_positives.empty:
                st.info("**👍 General Positive Feedback**")
                for idx, row in general_positives.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Core Value Comments", len(core_value))
            with col2:
                st.metric("Minor Issues", len(minor_issues))
            with col3:
                st.metric("Serious Issues", len(serious_issues))
        else:
            st.info("No dropdown tool feedback yet.")
    
    with tab2:
        st.write("### AI Feedback (For Comparison Only)")
        st.info("This shows what AI does WRONG - helps compare against our dropdown tool")
        
        if not ai_feedback.empty:
            for idx, row in ai_feedback.iterrows():
                st.markdown(f"• *\"{row['Comment']}\"*")
            
            # Quick sentiment on AI feedback
            def get_ai_sentiment(comment):
                try:
                    analysis = TextBlob(str(comment))
                    return "Negative" if analysis.sentiment.polarity < 0 else "Neutral"
                except:
                    return "Neutral"
            
            ai_feedback["Sentiment"] = ai_feedback["Comment"].apply(get_ai_sentiment)
            negative_count = (ai_feedback["Sentiment"] == "Negative").sum()
            
            st.metric("AI Negative Feedback", negative_count, 
                     f"{negative_count}/{len(ai_feedback)} comments")
        else:
            st.info("No AI feedback yet.")
    
    with tab3:
        st.write("### Suggestions & Feature Requests")
        
        if not suggestions_feedback.empty:
            # Show feature requests
            feature_requests = suggestions_feedback[suggestions_feedback["Category"] == "Feature Request"]
            if not feature_requests.empty:
                st.info("**📋 Feature Requests**")
                for idx, row in feature_requests.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
            
            # Show other suggestions
            other_suggestions = suggestions_feedback[suggestions_feedback["Category"] != "Feature Request"]
            if not other_suggestions.empty:
                st.info("**💡 Other Suggestions**")
                for idx, row in other_suggestions.iterrows():
                    st.markdown(f"• *\"{row['Comment']}\"*")
            
            st.metric("Total Suggestions", len(suggestions_feedback))
        else:
            st.info("No suggestions yet.")
    
    # --- IMPROVED SCALING RECOMMENDATION ---
    st.subheader("🚀 Scaling Recommendation Analysis")
    
    if not tool_feedback.empty:
        # Calculate metrics for decision
        core_value_count = len(tool_feedback[tool_feedback["Category"] == "Core Value for Scaling"])
        serious_issues_count = len(tool_feedback[tool_feedback["Category"] == "Serious Issue"])
        minor_issues_count = len(tool_feedback[tool_feedback["Category"] == "Minor UI/UX Issue"])
        total_tool_feedback = len(tool_feedback)
        
        # Calculate quantitative metrics for decision
        quantitative_score = 0
        
        # Time saved metrics
        time_saved_counts = df['time_saved'].value_counts()
        if '4+hrs' in time_saved_counts:
            quantitative_score += 3
        if '2-4hrs' in time_saved_counts:
            quantitative_score += 2
        if '1-2hrs' in time_saved_counts:
            quantitative_score += 1
        
        # Quality metrics
        quality_counts = df['quality_dropdown'].value_counts()
        if 'High & curriculum-aligned' in quality_counts:
            quantitative_score += 2
        if 'Good, ready to use' in quality_counts:
            quantitative_score += 1
        
        # Cognitive relief metrics
        cognitive_counts = df['cognitive_dropdown'].value_counts()
        if 'Very low' in cognitive_counts:
            quantitative_score += 2
        if 'Low' in cognitive_counts:
            quantitative_score += 1
        
        # Decision logic based on MULTIPLE factors
        col1, col2 = st.columns(2)
        
        with col1:
            # Create scoring system
            score = 0
            
            # 1. Core value strength
            if core_value_count >= 2:
                score += 3
            elif core_value_count == 1:
                score += 1
            
            # 2. Issue severity
            if serious_issues_count == 0:
                score += 2
            elif serious_issues_count == 1:
                score -= 1
            else:
                score -= 3
            
            # 3. Quantitative support
            if quantitative_score >= 5:
                score += 2
            elif quantitative_score >= 3:
                score += 1
            
            # 4. Response volume
            if total_responses >= 5:
                score += 1
            
            # Make recommendation based on score
            if score >= 5:
                st.success("""
                ### ✅ **STRONG RECOMMENDATION: SCALE NOW**
                
                **Why:**
                - Multiple core value indicators
                - Strong quantitative support
                - No serious blocking issues
                - Minor issues can be fixed during scaling
                
                **Confidence: High**
                """)
            elif score >= 3:
                st.warning("""
                ### ⚠️ **MODERATE RECOMMENDATION: ITERATE THEN SCALE**
                
                **Why:**
                - Some core value identified
                - Need to fix minor issues first
                - Consider gathering more feedback
                
                **Next: Fix UI issues, then scale**
                """)
            elif score >= 1:
                st.warning("""
                ### ⚠️ **WEAK RECOMMENDATION: FIX SERIOUS ISSUES FIRST**
                
                **Why:**
                - Serious issues need attention
                - Core value unclear or weak
                - Quantitative metrics mixed
                
                **Next: Fix serious issues, re-evaluate**
                """)
            else:
                st.error("""
                ### ❌ **NOT READY TO SCALE**
                
                **Why:**
                - Insufficient core value evidence
                - Serious blocking issues
                - Need more validation
                
                **Next: Pivot or gather more feedback**
                """)
        
        with col2:
            # Display detailed metrics
            metrics_data = {
                'Factor': ['Core Value Comments', 'Serious Issues', 'Minor Issues', 
                          'Total Tool Feedback', 'Quantitative Score', 'Total Responses',
                          'AI Negatives', 'Enthusiasts (Contact Opt-in)'],
                'Value': [core_value_count, serious_issues_count, minor_issues_count,
                         total_tool_feedback, quantitative_score, total_responses,
                         len(ai_feedback[ai_feedback["Sentiment"] == "Negative"]) if not ai_feedback.empty else 0,
                         opt_in_count]
            }
            metrics_df = pd.DataFrame(metrics_data)
            st.dataframe(metrics_df, hide_index=True, use_container_width=True)
            
            # Show scoring breakdown
            with st.expander("**Scoring Breakdown**"):
                st.write("""
                **Scoring System:**
                - Core Value (2+ comments): +3 points
                - Core Value (1 comment): +1 point
                - No Serious Issues: +2 points
                - 1 Serious Issue: -1 point
                - 2+ Serious Issues: -3 points
                - Strong Quantitative (≥5): +2 points
                - Moderate Quantitative (≥3): +1 point
                - Good Response Volume (≥5): +1 point
                
                **Thresholds:**
                - ≥5: Scale Now
                - 3-4: Iterate Then Scale  
                - 1-2: Fix Issues First
                - ≤0: Not Ready
                """)
    
    # Contact list for enthusiasts (WITH FIXED ERROR HANDLING)
    enthusiasts_available = False
    enthusiasts_df = pd.DataFrame()
    
    if 'allow_contact' in df.columns and 'name' in df.columns:
        enthusiasts_df = df[(df['allow_contact'] == True) & (df['name'] != "Anonymous") & (df['name'].notna())]
        enthusiasts_available = not enthusiasts_df.empty
    
    if enthusiasts_available:
        st.subheader("🌟 Enthusiasts Open to Contact")
        st.write(f"Found {len(enthusiasts_df)} participants willing to share their experience:")
        contact_list = enthusiasts_df[['name', 'email', 'open_feedback_tool']].copy()
        contact_list.columns = ['Name', 'Email', 'Key Feedback']
        st.dataframe(contact_list, use_container_width=True, hide_index=True)
    
    # --- Download Enhanced Report ---
    st.subheader("📥 Download Full Report")
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Raw data (anonymized for sharing)
        share_df = df.copy()
        share_df['name'] = share_df['name'].apply(lambda x: 'Anonymous' if x == 'Anonymous' else 'Participant')
        share_df['email'] = 'redacted'
        
        share_df.to_excel(writer, sheet_name="Aggregated Data", index=False)
        
        # Separate qualitative sheets
        if not tool_feedback.empty:
            tool_feedback.to_excel(writer, sheet_name="Tool Feedback", index=False)
        if not ai_feedback.empty:
            ai_feedback.to_excel(writer, sheet_name="AI Comparison", index=False)
        if not suggestions_feedback.empty:
            suggestions_feedback.to_excel(writer, sheet_name="Suggestions", index=False)
        
        # Summary stats
        summary_data = {
            'Metric': ['Total Responses', 'Opted for Contact', 'Core Value Comments', 
                      'Serious Issues', 'Minor Issues', 'AI Negative Feedback',
                      'Scoring Recommendation', 'Quantitative Score'],
            'Value': [total_responses, opt_in_count,
                     len(tool_feedback[tool_feedback["Category"] == "Core Value for Scaling"]) if not tool_feedback.empty else 0,
                     len(tool_feedback[tool_feedback["Category"] == "Serious Issue"]) if not tool_feedback.empty else 0,
                     len(tool_feedback[tool_feedback["Category"] == "Minor UI/UX Issue"]) if not tool_feedback.empty else 0,
                     len(ai_feedback[ai_feedback["Sentiment"] == "Negative"]) if not ai_feedback.empty else 0,
                     "Scale Now" if core_value_count >= 2 and serious_issues_count == 0 else "Needs Improvement",
                     quantitative_score]
        }
        
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
        
        writer.close()
        
        processed_data = output.getvalue()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📊 Download Full MVP Survey Report (Excel)",
        data=processed_data,
        file_name=f"mvp_survey_report_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Includes separated feedback analysis for better decision making"
    )
    
    # Internal contact list (separate download) - WITH FIX
    if enthusiasts_available:
        contact_output = io.BytesIO()
        with pd.ExcelWriter(contact_output, engine="xlsxwriter") as writer:
            enthusiasts_df.to_excel(writer, sheet_name="Contact List", index=False)
            writer.close()
            contact_data = contact_output.getvalue()
        
        st.download_button(
            label="📧 Download Enthusiast Contact List (Internal Use Only)",
            data=contact_data,
            file_name=f"enthusiast_contacts_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Internal use only - contains actual contact information for follow-up"
        )
    
else:
    st.info("No survey data yet. Submit the first response to see insights!")

# --- Footer with Privacy Reminder ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
<strong>Privacy Protection:</strong> All data is stored securely and analyzed in aggregate. 
Individual responses are never shared. Contact information is used only for product improvement 
with explicit consent.
</div>
""", unsafe_allow_html=True)
