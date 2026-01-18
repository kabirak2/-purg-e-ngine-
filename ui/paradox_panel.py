import streamlit as st
from core.runtime import get_canon


def render():
    canon = get_canon()

    st.markdown("### Paradox Inspector")
    st.caption("Detected contradictions in canon state")

    paradoxes = canon.detect_paradoxes()

    if not paradoxes:
        st.success("No paradoxes detected.")
        return

    st.error(f"{len(paradoxes)} paradox(es) detected")

    for p in paradoxes:
        with st.expander(f"⚠️ {p['rule_id']}"):
            st.write(p["message"])
            st.caption(f"Severity: {p['severity']}")
