import sqlite3
import streamlit as st

def init_post_study_db():
    conn = sqlite3.connect("survey_results.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_study_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soc_analyst_id INTEGER,
            expertise TEXT,
            sus_easy_use INTEGER,
            sus_clear_viz INTEGER,
            open_strategy TEXT,
            open_friction TEXT,
            open_trust TEXT,
            open_expertise TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_post_study(data):
    conn = sqlite3.connect("survey_results.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO post_study_feedback (
            soc_analyst_id, expertise, 
            sus_easy_use, sus_clear_viz,
            open_strategy, open_friction, open_trust, open_expertise
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

init_post_study_db()

st.title("Phase 3: Final Post-Study Feedback")
st.subheader("Retrospective System Evaluation")
st.markdown("---")

if "post_submitted" not in st.session_state:
    st.session_state.post_submitted = False

if not st.session_state.post_submitted:
    with st.form("post_study_form"):
        st.header("1. Analyst Profile Verification")
        col1, col2 = st.columns(2)
        with col1:
            soc_analyst_id = st.selectbox("Confirm Your SOC Analyst ID", list(range(1, 33)))
        with col2:
            expertise = st.selectbox("Confirm Your Expertise Cohort", ["Junior", "Senior"])
            
        st.markdown("---")
        likert_options = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}
        
        st.header("2. Overall System Usability")
        sus1 = st.radio("The XAI anomaly detection systems were overall easy to use and navigate.", list(likert_options.keys()), index=2, horizontal=True)
        sus2 = st.radio("The visual representations (temporal error, waterfall, and beeswarm plots) were clear and interpretable.", list(likert_options.keys()), index=2, horizontal=True)
        
        st.markdown("---")
        st.header("3. Diagnostic Strategy & Final Feedback")
        open_strategy = st.text_area("Describe your step-by-step process for determining if a flagged day was a True Positive versus a False Alarm. How did your strategy shift when SHAP plots were introduced?", height=120)
        open_friction = st.text_area("What was the most challenging or time-consuming bottleneck when triaging alerts using the Traditional Baseline (Design A)?", height=120)
        open_trust = st.text_area("Were there any scenarios where you disagreed with or felt confused by the feature attributions shown? How did you resolve that?", height=120)
        open_expertise = st.text_area("Did you feel you needed deep, specialized cybersecurity domain knowledge to interpret the alerts effectively when using the SHAP assisted layout (Design B)? Why?", height=120)
        
        submit_post = st.form_submit_button("Submit Final Post-Study Evaluation")
        
        if submit_post:
            payload = (
                int(soc_analyst_id), expertise,
                likert_options[sus1], likert_options[sus2],
                open_strategy, open_friction, open_trust, open_expertise
            )
            save_post_study(payload)
            st.session_state.post_submitted = True
            st.rerun()
else:
    st.success("Thank you! Your final post-study feedback has been securely recorded.")
    if st.button("Log Responses for a New Participant"):
        st.session_state.post_submitted = False
        st.rerun()