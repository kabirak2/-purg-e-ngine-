import streamlit as st
from core.runtime import get_canon, save_project


def render():
    canon = get_canon()

    st.markdown("### Truths")
    st.caption("Independent world facts")

    st.divider()

    # ------------------------------------------------------------
    # Add / update truth
    # ------------------------------------------------------------

    with st.expander("➕ Add or update truth", expanded=True):
        truth_key = st.text_input(
            "Truth key",
            placeholder="kael_is_alive",
            help="Stable identifier used by rules and events",
        )

        truth_value = st.selectbox(
            "Truth value",
            options=[True, False],
            index=0,
        )

        if st.button("Save truth"):
            if not truth_key.strip():
                st.warning("Truth key is required.")
            else:
                canon.truths[truth_key.strip()] = truth_value
                save_project()
                st.success(f"Truth '{truth_key}' saved.")

    st.divider()

    # ------------------------------------------------------------
    # Existing truths
    # ------------------------------------------------------------

    if not canon.truths:
        st.info("No truths defined yet.")
        return

    st.markdown("#### Existing truths")

    for key in sorted(canon.truths.keys()):
        col_key, col_val, col_del = st.columns([4, 2, 2])

        with col_key:
            st.code(key)

        with col_val:
            st.write(str(canon.truths[key]))

        with col_del:
            if st.button("Delete", key=f"delete_truth_{key}"):
                canon.truths.pop(key)
                save_project()
                st.success(f"Truth '{key}' deleted.")
                st.experimental_rerun()
