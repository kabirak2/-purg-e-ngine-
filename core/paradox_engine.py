def detect_paradoxes(canon):
    paradoxes = []

    truths = canon.truths

    for rule in canon.rules:
        if rule.get("severity") != "hard":
            continue

        if rule.get("overridden", False):
            continue

        # ---------------- conditions ----------------
        conditions = rule.get("conditions", {}).get("all", [])
        if not all(truths.get(c) is True for c in conditions):
            continue

        # ---------------- constraint ----------------
        constraint = rule.get("constraint", {})
        forbidden = constraint.get("forbid_truth")

        if not forbidden:
            continue

        # normalize to list
        if isinstance(forbidden, str):
            forbidden = [forbidden]

        for truth_key in forbidden:
            if truths.get(truth_key) is True:
                paradoxes.append({
                    "rule_id": rule.get("id"),
                    "forbidden_truth": truth_key,
                    "severity": rule.get("severity"),
                    "message": (
                        f"Rule '{rule.get('id')}' forbids truth "
                        f"'{truth_key}', but it is True."
                    ),
                })



    return paradoxes
