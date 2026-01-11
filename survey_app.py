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

# --- Color-coded qualitative table ---
def highlight_category(row):
    if row["Category"] == "Value":
        return ["background-color: #a8e6a3"]*2  # soft green
    elif row["Category"] == "Limitation":
        return ["background-color: #f4a2a2"]*2  # soft red
    else:
        return [""]*2

st.write("**Value (what works well):**")
st.dataframe(
    qualitative_comments[qualitative_comments["Category"]=="Value"].head(5).style.apply(highlight_category, axis=1)
)

st.write("**Limitations (pain points / areas to improve):**")
st.dataframe(
    qualitative_comments[qualitative_comments["Category"]=="Limitation"].head(5).style.apply(highlight_category, axis=1)
)

# --- Download Excel ---
import io
output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    # Quantitative
    df.to_excel(writer, sheet_name="Raw Survey Data", index=False)
    # Qualitative
    qualitative_comments.to_excel(writer, sheet_name="Qualitative Insights", index=False)
    # No writer.save() here — it's handled automatically
processed_data = output.getvalue()

st.download_button(
    label="Download Full MVP Survey Report (Excel)",
    data=processed_data,
    file_name="mvp_survey_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
