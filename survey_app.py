# survey_app_mvp.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from textblob import TextBlob

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
    
    # --- Enhanced Qualitative Analysis ---
    st.subheader("🔍 Advanced Qualitative Analysis")
    
    # Create qualitative dataframe
    qualitative_comments = pd.concat([
        df[["open_feedback_ai"]].rename(columns={"open_feedback_ai":"Comment"}),
        df[["open_feedback_tool"]].rename(columns={"open_feedback_tool":"Comment"}),
        df[["suggestions"]].rename(columns={"suggestions":"Comment"})
    ], ignore_index=True).dropna()
    
    # Enhanced classification function
    def classify_comment_advanced(comment):
        if pd.isna(comment) or str(comment).strip() == "":
            return "No feedback"
        
        comment_lower = str(comment).lower()
        categories = []
        
        # Comprehensive theme detection
        themes = {
            "Time Efficiency": ["fast", "quick", "seconds", "minutes", "saves time", "time saved", "efficient", "speedy"],
            "Cognitive Relief": ["thinking", "decision", "mental", "effort", "cognitive", "stress", "anxiety", "relief", "easy"],
            "Quality": ["quality", "aligned", "curriculum", "accurate", "consistent", "professional", "well-written"],
            "Technical Issues": ["bug", "glitch", "error", "disappears", "reverts", "reset", "default", "duplicate", "tweak", "adjust"],
            "Character Limit": ["exceeds", "character limit", "too long", "length", "count", "limit"],
            "Usability": ["select", "choose", "option", "setting", "preference", "interface", "user friendly"],
            "Feature Request": ["add", "suggest", "improve", "enhance", "missing", "need", "should", "could", "would like"],
            "Positive Comparison": ["better than", "prefer", "improved", "superior", "advantage", "love", "great", "excellent"],
            "Negative Comparison": ["worse than", "disadvantage", "rather use", "prefer other", "frustrating", "annoying"]
        }
        
        for theme, keywords in themes.items():
            for keyword in keywords:
                if keyword in comment_lower:
                    categories.append(theme)
                    break
        
        return ", ".join(set(categories)) if categories else "General Feedback"
    
    # Apply classification
    qualitative_comments["Themes"] = qualitative_comments["Comment"].apply(classify_comment_advanced)
    
    # Sentiment analysis
    def get_sentiment(text):
        if pd.isna(text) or str(text).strip() == "":
            return "Neutral", 0
        try:
            analysis = TextBlob(str(text))
            pol = analysis.sentiment.polarity
            if pol > 0.2:
                return "Positive", pol
            elif pol < -0.1:
                return "Negative", pol
            else:
                return "Neutral", pol
        except:
            return "Neutral", 0
    
    qualitative_comments[["Sentiment", "Polarity"]] = qualitative_comments["Comment"].apply(
        lambda x: pd.Series(get_sentiment(x))
    )
    
    # Priority scoring
    def calculate_priority_score(row):
        score = 0
        themes = str(row["Themes"]).lower()
        
        if "technical issues" in themes:
            score += 3
        if "character limit" in themes:
            score += 2
        if row["Sentiment"] == "Negative":
            score += 2
        if "feature request" in themes:
            score += 1
        
        return score
    
    qualitative_comments["Priority"] = qualitative_comments.apply(calculate_priority_score, axis=1)
    
    # Display qualitative insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Feedback Themes Analysis**")
        theme_counts = qualitative_comments["Themes"].str.split(", ").explode().value_counts()
        fig = px.bar(theme_counts.head(10), title="Top 10 Feedback Themes")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Sentiment Analysis**")
        sentiment_counts = qualitative_comments["Sentiment"].value_counts()
        fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, 
                     title="Overall Sentiment Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Priority Matrix
    st.subheader("🚨 Priority Improvement Matrix")
    priority_data = qualitative_comments.sort_values("Priority", ascending=False)
    
    tabs = st.tabs(["High Priority", "All Feedback"])
    
    with tabs[0]:
        high_priority = priority_data[priority_data["Priority"] >= 3]
        if not high_priority.empty:
            st.dataframe(
                high_priority[["Comment", "Themes", "Sentiment", "Priority"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No high-priority issues identified!")
    
    with tabs[1]:
        st.dataframe(
            priority_data[["Comment", "Themes", "Sentiment", "Priority"]],
            use_container_width=True,
            hide_index=True
        )
    
    # Contact list for enthusiasts
    if 'allow_contact' in df.columns and 'name' in df.columns:
        enthusiasts = df[(df['allow_contact'] == True) & (df['name'] != "Anonymous")]
        if not enthusiasts.empty:
            st.subheader("🌟 Enthusiasts Open to Contact")
            st.write(f"Found {len(enthusiasts)} participants willing to share their experience:")
            contact_list = enthusiasts[['name', 'email', 'open_feedback_tool']].copy()
            contact_list.columns = ['Name', 'Email', 'Key Feedback']
            st.dataframe(contact_list, use_container_width=True, hide_index=True)
    
    # --- Download Enhanced Report ---
    st.subheader("📥 Download Full Report")
    
    import io
    from datetime import datetime
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Raw data (anonymized for sharing)
        share_df = df.copy()
        share_df['name'] = share_df['name'].apply(lambda x: 'Anonymous' if x == 'Anonymous' else 'Participant')
        share_df['email'] = 'redacted'
        
        share_df.to_excel(writer, sheet_name="Aggregated Data", index=False)
        qualitative_comments.to_excel(writer, sheet_name="Qualitative Analysis", index=False)
        
        # Summary stats
        summary_data = {
            'Metric': ['Total Responses', 'Opted for Contact', 'Average Sentiment Score', 
                      'Most Common Theme', 'Top Priority Issue'],
            'Value': [total_responses, opt_in_count, 
                     qualitative_comments['Polarity'].mean(),
                     theme_counts.index[0] if len(theme_counts) > 0 else 'N/A',
                     priority_data.iloc[0]['Comment'][:50] + '...' if len(priority_data) > 0 else 'N/A']
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
        
        writer.save()
        processed_data = output.getvalue()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📊 Download Full MVP Survey Report (Excel)",
        data=processed_data,
        file_name=f"mvp_survey_report_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Includes aggregated data, qualitative analysis, and summary statistics"
    )
    
    # Internal contact list (separate download)
    if not enthusiasts.empty:
        contact_output = io.BytesIO()
        with pd.ExcelWriter(contact_output, engine="xlsxwriter") as writer:
            enthusiasts.to_excel(writer, sheet_name="Contact List", index=False)
            writer.save()
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
