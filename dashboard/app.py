import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="NetSage AI Dashboard", layout="wide")

st.title("NetSage AI Troubleshooting Dashboard")
st.markdown("An AI-driven network diagnostic tool with deterministic rule checking and human-in-the-loop review.")

# Load Data
@st.cache_data
def load_data():
    cases_df = pd.read_csv('../data/cases/cases.csv') if os.path.exists('../data/cases/cases.csv') else pd.DataFrame()
    ai_df = pd.read_csv('../data/outputs/ai_results.csv') if os.path.exists('../data/outputs/ai_results.csv') else pd.DataFrame()
    review_df = pd.read_csv('../data/reviews/reviews.csv') if os.path.exists('../data/reviews/reviews.csv') else pd.DataFrame()
    rai_df = pd.read_csv('../data/reviews/responsible_ai_log.csv') if os.path.exists('../data/reviews/responsible_ai_log.csv') else pd.DataFrame()
    return cases_df, ai_df, review_df, rai_df

cases_df, ai_df, review_df, rai_df = load_data()

if cases_df.empty:
    st.error("No case data found. Please run batch generation.")
    st.stop()

# Dashboard Metrics
st.header("Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cases", len(cases_df))
col2.metric("Concept Areas", cases_df['concept_tag'].nunique() if 'concept_tag' in cases_df else 0)

high_sev = len(cases_df[cases_df['severity'] == 'High']) if 'severity' in cases_df else 0
col3.metric("High Severity Issues", high_sev)

accepted = len(review_df[review_df['human_decision'] == 'Accepted']) if not review_df.empty else 0
edited = len(review_df[review_df['human_decision'] == 'Edited']) if not review_df.empty else 0
rejected = len(review_df[review_df['human_decision'] == 'Rejected']) if not review_df.empty else 0
col4.metric("AI Accuracy (Accepted)", f"{accepted} / {len(review_df)}" if not review_df.empty else "N/A")
st.caption("AI results generated using Gemini where available. Cases processed using deterministic fallback are explicitly labelled DEMO FALLBACK. Review records must be validated by the project team before final submission.")

# Charts and Distributions
col1, col2 = st.columns(2)
with col1:
    st.subheader("Issue Types (Concepts)")
    if 'concept_tag' in cases_df:
        st.bar_chart(cases_df['concept_tag'].value_counts())

with col2:
    st.subheader("Human Review Decisions")
    if not review_df.empty:
        st.bar_chart(review_df['human_decision'].value_counts())

st.divider()

# Demo Workflow Section
st.header("Human-in-the-Loop Review Workflow")
st.markdown("Below is a review log containing human-review workflow records. Demonstration review records are clearly identified where applicable.")

if not rai_df.empty:
    edited_rejected = rai_df[rai_df['human_decision'].isin(['Edited', 'Rejected'])]
    st.dataframe(edited_rejected[['case_id', 'ai_diagnosis', 'human_decision', 'correction_reason']], width='stretch')
else:
    st.info("No Responsible AI log found.")

st.divider()

# Case Detail View
st.header("Case Detail Explorer")
case_id_list = cases_df['case_id'].tolist()
selected_case = st.selectbox("Select a Case ID to inspect:", case_id_list)

case_info = cases_df[cases_df['case_id'] == selected_case].iloc[0]
ai_info = ai_df[ai_df['case_id'] == selected_case].iloc[0] if (not ai_df.empty and selected_case in ai_df['case_id'].values) else None
rev_info = review_df[review_df['case_id'] == selected_case].iloc[0] if (not review_df.empty and selected_case in review_df['case_id'].values) else None

st.subheader(f"Case: {selected_case}")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Evidence")
    st.markdown(f"**Symptom:** {case_info.get('symptom', 'N/A')}")
    st.markdown(f"**Topology:** {case_info.get('topology_note', 'N/A')}")
    st.code(case_info.get('show_command_outputs', ''), language='text')

with col2:
    st.markdown("### 2. AI Diagnosis")
    if ai_info is not None:
        st.success(f"**Root Cause:** {ai_info.get('root_cause', 'N/A')}")
        st.info(f"**Confidence:** {ai_info.get('confidence', 'N/A')}")
        st.markdown(f"**Next Command:** `{ai_info.get('next_command', 'N/A')}`")
        st.markdown(f"**Verification:** `{ai_info.get('verification_command', 'N/A')}`")
    else:
        st.warning("No AI results found for this case.")
        
    st.markdown("### 3. Human Review & Fix")
    if rev_info is not None:
        decision = rev_info.get('human_decision', 'N/A')
        if decision == 'Accepted':
            st.success(f"Decision: **{decision}**")
        elif decision == 'Edited':
            st.warning(f"Decision: **{decision}**")
            st.markdown(f"**Correction:** {rev_info.get('human_correction', '')}")
        else:
            st.error(f"Decision: **{decision}**")
            st.markdown(f"**Correction:** {rev_info.get('human_correction', '')}")
    else:
        st.info("Pending Human Review")
