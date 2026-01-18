import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from ui.helpers import inject_global_styles

from ui.versemind_panel import render as versemind_render
from ui.timeline_panel import render as timeline
from ui.rule_editor import render as rules_render
from ui.validation_panel import render as validation
from ui.analytics_panel import render as analytics
from ui.debugger_panel import render as debugger
from ui.canon_panel import render as canon_render
from ui.paradox_panel import render as paradox
from ui.project_panel import render as project_render
from ui.truths_panel import render as truths_render
from ui.events_panel import render as events_render

def main():
    st.set_page_config(page_title="PURGE Console", layout="centered")
    inject_global_styles()

    st.markdown("## PURGE AI Console")
    st.caption("Internal research & narrative intelligence system")

    panel = st.sidebar.radio(
    "Tools",
        [
            "Project",
            "Rules",
            "Truths",
            "Events",
            "VerseMind",
            "Paradox",
            "Debugger",
            "Analytics",
            "Validation",
            "Canon",
            "Timeline"
        ],
    )


    if panel == "VerseMind":
        versemind_render()
    elif panel == "Timeline":
        timeline()
    elif panel == "Rules":
        rules_render()
    elif panel == "Validation":
        validation()
    elif panel == "Analytics":
        analytics()
    elif panel == "Debugger":
        debugger()
    elif panel == "Canon":
        canon_render()
    elif panel == "Paradox":
        paradox()
    elif panel == "Project":
        project_render()
    elif panel == "Truths":
        truths_render()
    elif panel == "Events":
        events_render()

if __name__ == "__main__":
    main()
