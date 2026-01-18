import streamlit as st
import json
from core.runtime import get_canon, save_project


def render():
    canon = get_canon()

    st.markdown("### Rules")
    st.caption("Narrative constraints and enforcement")

    st.divider()

    # ============================================================
    # ADD / EDIT RULE
    # ============================================================

    with st.expander("➕ Add new rule", expanded=True):
        rule_id = st.text_input(
            "Rule ID",
            placeholder="no_death_reversal",
            help="Stable identifier used internally"
        )

        rule_text = st.text_area(
            "Rule description",
            placeholder="Deaths are supposed to be irreversible",
        )

        severity = st.selectbox(
            "Severity",
            options=["soft", "medium", "hard"],
            index=2,
        )

        strength = st.slider(
            "Rule strength",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.05,
            help="Decay-sensitive enforcement strength"
        )

        st.markdown("##### Conditions")
        st.caption("All conditions must be true for the rule to apply")

        conditions = st.text_area(
            "Condition keys (one per line)",
            placeholder="character_is_alive\nwar_is_active",
            help="Truth keys that must all evaluate to true",
        )

        st.markdown("##### Constraint")
        st.caption("Optional structured constraint (advanced)")

        constraint_raw = st.text_area(
            "Constraint (JSON)",
            value="{}",
            help="Advanced constraint structure (leave empty if unused)",
        )

        if st.button("Add rule"):
            if not rule_id.strip():
                st.warning("Rule ID is required.")
                return

            try:
                constraint = (
                    {} if not constraint_raw.strip()
                    else json.loads(constraint_raw)
                )
            except Exception:
                st.error("Invalid JSON in constraint.")
                return

            rule = {
                "id": rule_id.strip(),
                "text": rule_text.strip(),
                "severity": severity,
                "conditions": {
                    "all": [
                        c.strip() for c in conditions.splitlines()
                        if c.strip()
                    ]
                },
                "constraint": constraint,
                "strength": strength,
                "overridden": False,
            }

            canon.add_rule(rule)
            save_project()

            st.success(f"Rule '{rule_id}' added and saved.")

    st.divider()

    # ============================================================
    # EXISTING RULES
    # ============================================================

    if not canon.rules:
        st.info("No rules defined yet.")
        return

    st.markdown("#### Existing rules")

    for idx, rule in enumerate(canon.rules):
        with st.expander(f"🧩 {rule.get('id', 'unnamed')}"):
            st.markdown("**Description**")
            st.write(rule.get("text", ""))

            st.caption(f"Severity: {rule.get('severity', 'unknown')}")
            st.caption(f"Strength: {rule.get('strength', 1.0)}")
            st.caption(f"Overridden: {rule.get('overridden', False)}")

            st.markdown("**Conditions (all)**")
            for c in rule.get("conditions", {}).get("all", []):
                st.code(c)

            st.markdown("**Constraint**")
            st.code(rule.get("constraint", {}), language="json")

            if st.button("Remove rule", key=f"remove_rule_{idx}"):
                canon.rules.pop(idx)
                save_project()
                st.success("Rule removed.")
                st.rerun()
