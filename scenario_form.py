import sqlite3
import streamlit as st

# ==========================================
# 1. DATABASE INITIALIZATION
# ==========================================
def init_db():
    conn = sqlite3.connect("survey_results.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qualitative_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soc_analyst_id INTEGER,
            suspicious_user_id TEXT,
            expertise TEXT,
            interface_type TEXT,
            q1_layout INTEGER,
            q2_confidence INTEGER,
            q3_intuitive INTEGER,
            q4_second_guess INTEGER,
            q5_baseline INTEGER,
            q6_shap_waterfall INTEGER,
            q7_shap_beeswarm INTEGER,
            q8_log_reduction INTEGER,
            q9_trust INTEGER,
            q10_cognitive_effort INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_responses(data):
    conn = sqlite3.connect("survey_results.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO qualitative_responses (
            soc_analyst_id, suspicious_user_id, expertise, interface_type,
            q1_layout, q2_confidence, q3_intuitive, q4_second_guess, q5_baseline,
            q6_shap_waterfall, q7_shap_beeswarm, q8_log_reduction, q9_trust, q10_cognitive_effort
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

# Initialize database on app launch
init_db()

# ==========================================
# 2. STREAMLIT INTERFACE CONFIGURATION
# ==========================================
st.set_page_config(page_title="XAI User Study: Post-Scenario Survey", layout="centered")

st.title("Qualitative Evaluation Protocol")
st.subheader("Post-Scenario Interface Assessment")
st.markdown("---")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Render Input Form Flow
if not st.session_state.submitted:
    
    st.header("1. Participant & Scenario Metadata")
    col1, col2 = st.columns(2)
    with col1:
        analyst_options = ["Select ID..."] + list(range(1, 33))
        soc_analyst_id = st.selectbox("SOC Analyst ID", analyst_options, index=0)
        expertise = st.selectbox("Expertise Cohort", ["Select Cohort...", "Junior", "Senior"], index=0)
    
    with col2:
        suspicious_user_options = ["Select User...", "User 93", "User 94", "User 17", "User 345", "User 400", "User 401", "User 102", "User 215"]
        suspicious_user_id = st.selectbox("Suspicious User Audited", suspicious_user_options, index=0)
        interface_type = st.selectbox("Evaluated Interface", ["Select Interface...", "Design_A", "Design_B"], index=0)
    
    st.markdown("---")
    
    # Core Question Evaluation Form
    with st.form("survey_form"):
        
        # Likert Mapping dictionary
        likert_options = {
            "Strongly Disagree": 1,
            "Disagree": 2,
            "Neutral": 3,
            "Agree": 4,
            "Strongly Agree": 5
        }
        
        # Core Usability Metrics (Both Designs A and B)
        st.header("2. System Usability & Interface Confidence")
        
        # index=None forces initial value to be completely unselected
        q1 = st.radio("The interface layout allowed me to locate critical anomaly data without feeling overwhelmed.", list(likert_options.keys()), index=None, horizontal=True)
        q2 = st.radio("I felt confident that my final triage classifications (True Positive vs. False Alarm) were accurate.", list(likert_options.keys()), index=None, horizontal=True)
        q3 = st.radio("Navigating the dashboard's panels felt intuitive and seamless.", list(likert_options.keys()), index=None, horizontal=True)
        q4 = st.radio("I found myself second-guessing my decisions while utilizing this dashboard.", list(likert_options.keys()), index=None, horizontal=True)
        q5 = st.radio("The temporal anomaly plot and baseline indicators provided a clear view of the user's historical behavior.", list(likert_options.keys()), index=None, horizontal=True)
        
        # XAI Specific Section 
        q6, q7, q8, q9, q10 = None, None, None, None, None
        
        if interface_type == "Design_B":
            st.markdown("---")
            st.header("3. Explainable AI (XAI) Utility Overlays")
            
            q6 = st.radio("The SHAP local waterfall plots provided clear, immediate justification for why an individual day was flagged.", list(likert_options.keys()), index=None, horizontal=True)
            q7 = st.radio("The global beeswarm plot effectively contextualized long-term, multi-day threat patterns.", list(likert_options.keys()), index=None, horizontal=True)
            st.caption("Note: Red blocks represent positive forces increasing anomaly vectors; Blue blocks pull scores down.")
            q8 = st.radio("The feature attribution plots allowed me to make accurate triage decisions without needing to meticulously inspect the raw system event logs.", list(likert_options.keys()), index=None, horizontal=True)
            q9 = st.radio("I trusted the feature importance vectors displayed by the XAI overlays.", list(likert_options.keys()), index=None, horizontal=True)
            q10 = st.radio("The SHAP visualizations reduced the mental effort required to correlate different system features.", list(likert_options.keys()), index=None, horizontal=True)

        st.markdown("---")
        
        # Form Submission Button
        submit_button = st.form_submit_button(label="Submit Scenario Responses")
        
        if submit_button:
            # --- INPUT CHECK VALIDATION LOGIC ---
            validation_errors = []
            
            if soc_analyst_id == "Select ID...":
                validation_errors.append("SOC Analyst ID selection is required.")
            if expertise == "Select Cohort...":
                validation_errors.append("Expertise Cohort selection is required.")
            if suspicious_user_id == "Select User...":
                validation_errors.append("Suspicious User selection is required.")
            if interface_type == "Select Interface...":
                validation_errors.append("Evaluated Interface selection is required.")
                
            # Check baseline questions
            if not all([q1, q2, q3, q4, q5]):
                validation_errors.append("Please answer all questions under Section 2 (Usability & Confidence).")
                
            # Check Design B specific questions
            if interface_type == "Design_B":
                if not all([q6, q7, q8, q9, q10]):
                    validation_errors.append("Please answer all questions under Section 3 (XAI Utility Overlays).")
            
            # Block submission if any checks fail
            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                payload = (
                    int(soc_analyst_id), suspicious_user_id, expertise, interface_type,
                    likert_options[q1], likert_options[q2], likert_options[q3], likert_options[q4], likert_options[q5],
                    likert_options[q6] if q6 else None,
                    likert_options[q7] if q7 else None,
                    likert_options[q8] if q8 else None,
                    likert_options[q9] if q9 else None,
                    likert_options[q10] if q10 else None
                )
                save_responses(payload)
                st.session_state.submitted = True
                st.rerun()

# Post-Submission Flow
else:
    st.success("Scenario feedback logged successfully!")
    
    if st.button("Proceed to Next Target Scenario"):
        st.session_state.submitted = False
        st.rerun()
        
    st.markdown("---")
    
    # Secure Administrative Panel
    with st.expander("🔑 Research Admin Data Extraction"):
        admin_password = st.text_input("Enter Admin Password to Download Data", type="password")
        
        if admin_password == "Waterloo_XAI_2026":
            try:
                with open("survey_results.db", "rb") as db_file:
                    st.download_button(
                        label="📥 Download survey_results.db",
                        data=db_file,
                        file_name="user_study_qualitative_backup.db",
                        mime="application/octet-stream"
                    )
                st.info("Download this backup at the end of your active evaluation blocks.")
            except FileNotFoundError:
                st.error("No records found in database yet.")
