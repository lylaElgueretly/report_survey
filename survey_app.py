    # Section 7: Tool Benefits
    st.header("Dropdown Tool Benefits")
    
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
        time_saved = st.selectbox("Time saved for your class size:", [
            "No time saved",
            "30min-1hr",
            "1-2hrs",
            "2-4hrs",
            "4+hrs",
            "Custom hours (specify below)",
            "Didn't use"
        ])
    
    # Custom hours input - placed immediately after the dropdown
    if time_saved == "Custom hours (specify below)":
        # Add some visual separation
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <p style="margin: 0;"><strong>Please specify your custom time saved:</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        custom_col1, custom_col2 = st.columns([2, 1])
        with custom_col1:
            custom_hours_saved = st.number_input(
                "Approximate time saved (hours):",
                min_value=0.0,
                max_value=100.0,
                value=5.0,
                step=0.5,
                format="%.1f",
                label_visibility="collapsed",
                help="Enter hours saved (e.g., 4.5 = 4 hours 30 minutes)"
            )
        with custom_col2:
            # Add helper text
            st.markdown("###")
            st.caption("Example: 4.5 = 4½ hours")
    else:
        custom_hours_saved = None
    
    st.divider()
