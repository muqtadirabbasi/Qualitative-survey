import streamlit as st

# Define your multi-page layout routes
scenario_page = st.Page("scenario_form.py", title="1. Post-Scenario Logs", icon="📊")
post_study_page = st.Page("post_study_form.py", title="2. Final Post-Study Feedback", icon="📝")

# Initialize Navigation UI
pg = st.navigation([scenario_page, post_study_page])
st.sidebar.markdown("### User Study Navigation")
pg.run()
