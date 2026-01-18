import streamlit as st
from core.analytics import get_metrics
from core.runtime import get_canon, save_project

def render():
    st.markdown("### Analytics")
    st.caption("Narrative metrics")

    canon = get_canon()
    metrics = get_metrics(canon)

    st.json(metrics)
