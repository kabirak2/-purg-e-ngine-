import streamlit as st
from core.runtime import (
    open_project,
    save_project,
    save_project_as,
    reset_project,
    list_projects,
    get_store,
    get_canon,
)

def render():
    store = get_store()
    canon = get_canon()

    st.markdown("### Project")
    st.caption("Persistence, identity, and system control")

    st.divider()

    # ------------------------------------------------------------
    # Project selection
    # ------------------------------------------------------------

    if "selected_project" not in st.session_state:
        st.session_state.selected_project = ""

    available_projects = list_projects()

    selected_project = st.selectbox(
        "Select existing project",
        options=[""] + available_projects,
        index=(
            available_projects.index(store.active_project) + 1
            if store.active_project in available_projects
            else 0
        ),
        key="selected_project",
    )

    col_open, col_reset = st.columns(2)

    with col_open:
        if st.button("📂 Open project"):
            if not selected_project:
                st.warning("No project selected.")
            elif store.dirty:
                st.error("Unsaved changes detected. Save or reset before opening another project.")
            else:
                open_project(selected_project)
                st.success(f"Opened project: {selected_project}")

    with col_reset:
        if st.button("🗑 Reset project"):
            reset_project()
            st.success("In-memory project reset. Remember to save.")

    st.divider()

    # ------------------------------------------------------------
    # Active project display
    # ------------------------------------------------------------

    active = store.active_project or "(no project loaded)"
    dirty_flag = "  *unsaved*" if store.dirty else ""

    st.markdown("#### Active project")
    st.code(f"projects/{active}{dirty_flag}")

    st.divider()

    # ------------------------------------------------------------
    # Project metadata (CRITICAL FIX)
    # ------------------------------------------------------------

    st.markdown("#### Project metadata")
    st.caption("These values are stored inside canon.meta")

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input(
            "Story title",
            value=canon.meta.get("title", ""),
            placeholder="Neon Reapers",
        )

    with col2:
        author = st.text_input(
            "Author",
            value=canon.meta.get("author", ""),
            placeholder="Your name",
        )

    version = st.text_input(
        "Version",
        value=canon.meta.get("version", "0.1"),
        help="Internal or semantic version",
    )

    if st.button("💾 Save metadata"):
        canon.meta["title"] = title.strip()
        canon.meta["author"] = author.strip()
        canon.meta["version"] = version.strip()

        save_project()
        st.success("Project metadata saved.")

    st.divider()

    # ------------------------------------------------------------
    # Save / Save As
    # ------------------------------------------------------------

    col_save, col_save_as = st.columns(2)

    with col_save:
        if st.button("💾 Save project"):
            if not store.active_project:
                st.warning("No active project to save.")
            else:
                save_project()
                st.success("Project saved.")

    with col_save_as:
        new_name = st.text_input(
            "Save as (project name)",
            placeholder="my_project",
        )

        overwrite = st.checkbox("Overwrite if exists", value=False)

        if st.button("💾 Save as"):
            if not new_name.strip():
                st.warning("Please enter a project name.")
            else:
                try:
                    save_project_as(new_name.strip(), overwrite=overwrite)
                    st.success(f"Saved as {store.active_project}")
                except FileExistsError:
                    st.error("Project already exists. Enable overwrite to replace it.")

    if store.dirty:
        st.warning("This project has unsaved changes.")
