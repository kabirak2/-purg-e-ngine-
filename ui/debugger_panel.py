import streamlit as st
from core.replay import replay_last
from core.runtime import get_canon


def render():
    st.markdown("### Debugger")
    st.caption("Replay and inspection")

    canon = get_canon()

    if st.button("Replay Last Commit"):
        result = replay_last(canon)

        # --------------------------------------------
        # Handle failure states
        # --------------------------------------------
        if not result.get("ok"):
            reason = result.get("reason")

            if reason == "no_canon":
                st.info("No canon state available to replay.")
            elif reason == "no_event_log":
                st.info("No events recorded yet.")
            elif reason == "invalid_log_entry":
                st.warning("Last event log entry is invalid.")
            else:
                st.warning("Replay failed for an unknown reason.")

            return

        # --------------------------------------------
        # Successful replay
        # --------------------------------------------
        st.success("Replay completed successfully")

        st.markdown("#### Replay summary")
        st.write(f"Replayed until log ID: `{result['replayed_until']}`")
        st.write(f"Events applied: **{result['event_count']}**")
        st.write(f"Truths derived: **{result['truth_count']}**")
        
        if isinstance(result, str):
            st.error(result)
            return

        if not result.get("ok"):
            ...

