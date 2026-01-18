# ------------------------------------------------------------
# CONDITION EVALUATION
# ------------------------------------------------------------

def evaluate_condition(conditions, canon):
    """
    Evaluates rule conditions against canon truths.

    conditions schema:
    {
        "all": ["truth_key_1", "truth_key_2"]
    }

    Missing or empty conditions => always true
    """

    if not conditions:
        return True

    all_conditions = conditions.get("all", [])

    for truth_key in all_conditions:
        if canon.truths.get(truth_key) is not True:
            return False

    return True


# ------------------------------------------------------------
# RULE VALIDATION
# ------------------------------------------------------------

def validate_action(action, canon):
    """
    Validates a single action against canon rules.
    Returns blocked / warned rule lists.
    """

    blocked = []
    warned = []

    for rule in canon.rules:
        # ---------------- conditions ----------------
        conditions = rule.get("conditions", {})
        if not evaluate_condition(conditions, canon):
            continue

        constraint = rule.get("constraint", {})
        if not constraint:
            continue

        severity = rule.get("severity", "hard")

        # ---------------- forbid truth ----------------
        forbidden = constraint.get("forbid_truth")

        if forbidden:
            if isinstance(forbidden, str):
                forbidden = [forbidden]

            for truth_key in forbidden:
                if action.get("sets_truths", {}).get(truth_key) is True:
                    if severity == "hard":
                        blocked.append(rule)
                    else:
                        warned.append(rule)

    return {
        "blocked": blocked,
        "warned": warned,
    }


# ------------------------------------------------------------
# UI ADAPTER
# ------------------------------------------------------------

def validate_state(canon=None):
    """
    Performs a validation pass over all events in canon.
    """

    if canon is None:
        return {
            "status": "ok",
            "blocked": [],
            "warned": [],
            "message": "No canon state provided",
        }

    blocked = []
    warned = []

    for event in canon.events:
        result = validate_action(
            action=event,
            canon=canon,
        )

        blocked.extend(result["blocked"])
        warned.extend(result["warned"])

    status = "ok"
    if blocked:
        status = "blocked"
    elif warned:
        status = "warning"

    return {
        "status": status,
        "blocked": blocked,
        "warned": warned,
    }