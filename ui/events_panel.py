import streamlit as st
import json
from core.runtime import get_canon, apply_event

    
def render():
    canon = get_canon()

    st.markdown("### Events")
    st.caption("Canon-changing actions")

    st.divider()

    # ============================================================
    # ADD EVENT
    # ============================================================

    with st.expander("➕ Add event", expanded=True):
        event_id = st.text_input(
            "Event ID",
            placeholder="evt_kael_revival"
        )

        act = st.text_input(
            "Act",
            placeholder="revival"
        )

        description = st.text_area(
            "Description",
            placeholder="Kael is brought back to life."
        )

        st.markdown("#### Truth mutations")
        st.caption("JSON object of truth changes")

        truth_json = st.text_area(
            "sets_truths",
            value="{\n  \"kael_comes_back_to_life\": true\n}",
        )

        if st.button("Apply event"):
            if not event_id or not act:
                st.warning("Event ID and Act are required.")
                return

            try:
                sets_truths = json.loads(truth_json)
                if not isinstance(sets_truths, dict):
                    raise ValueError
            except Exception:
                st.error("sets_truths must be valid JSON object.")
                return

            event = {
                "id": event_id,
                "act": act,
                "description": description,
                "sets_truths": sets_truths,
            }

            apply_event(event)
            st.success("Event applied to canon.")
            st.rerun()

    st.divider()

    # ============================================================
    # EVENT LOG
    # ============================================================

    st.markdown("#### Event log")

    if not canon.events:
        st.info("No events recorded yet.")
        return

    for evt in canon.events:
        with st.expander(evt.get("id", "unnamed_event")):
            st.json(evt)
