import streamlit as st
from core.runtime import get_canon, save_project

def render():
    st.markdown("### Canon")
    st.caption("Current ground truth")

    canon = get_canon()
    st.json(canon.to_dict())
