import streamlit as st
from core.runtime import get_canon, apply_event, save_project


def render():
    canon = get_canon()

    st.markdown("### Timeline")
    st.caption("Acts, events, and canon flow")

    # ------------------------------------------------------------
    # ADD ACT
    # ------------------------------------------------------------

    with st.expander("➕ Add Act"):
        act_id = st.number_input("Act number", min_value=0, step=1)
        act_label = st.text_input("Act label")

        if st.button("Add Act"):
            canon.acts.append({
                "id": int(act_id),
                "label": act_label or f"Act {act_id}",
            })
            save_project()
            st.success("Act added")
            st.rerun()

    st.divider()

    if not canon.acts:
        st.info("No acts defined yet.")
        return

    # ------------------------------------------------------------
    # ACT LOOP
    # ------------------------------------------------------------

    for act in sorted(canon.acts, key=lambda a: a["id"]):
        st.subheader(act["label"])

        # ---------------- events in this act ----------------
        act_events = [
            e for e in canon.events
            if e.get("act") == act["id"]
        ]

        if act_events:
            for e in act_events:
                st.markdown(f"• **{e.get('name', e.get('id', 'event'))}**")
        else:
            st.caption("No events in this act.")

        # ---------------- add event ----------------
        with st.expander("➕ Add event to this act"):
            name = st.text_input(
                "Event name",
                key=f"name_{act['id']}"
            )

            truth_key = st.text_input(
                "Truth key",
                key=f"truth_key_{act['id']}"
            )

            truth_value = st.checkbox(
                "Truth value = True",
                value=True,
                key=f"truth_val_{act['id']}"
            )

            if st.button("Add event", key=f"add_evt_{act['id']}"):
                event = {
                    "id": f"evt_{len(canon.events) + 1}",
                    "act": act["id"],
                    "name": name or f"Event {len(canon.events) + 1}",
                    "sets_truths": (
                        {truth_key: truth_value}
                        if truth_key else {}
                    ),
                }

                apply_event(event)
                st.success("Event added")
                st.rerun()

        # ---------------- canon flow after this act ----------------
        with st.expander("🧠 Canon state after this act"):
            truths_after = {}

            for e in canon.events:
                if e.get("act", 0) <= act["id"]:
                    truths_after.update(e.get("sets_truths", {}))

            st.json(truths_after)

        st.divider()
