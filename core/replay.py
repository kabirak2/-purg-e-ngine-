from copy import deepcopy


def replay_until(canon, log_id):
    new_canon = deepcopy(canon)
    new_canon.events = []
    new_canon.truths = {}
    new_canon.snapshots = []

    for entry in canon.event_log:
        if entry.get("log_id") == log_id:
            break

        if entry.get("commit", {}).get("written_to_canon"):
            payload = entry.get("payload")
            if payload and "act" in payload:
                new_canon.add_event(payload)

    return new_canon


# ------------------------------------------------------------
# UI ADAPTER (STRUCTURED OUTPUT ONLY)
# ------------------------------------------------------------

def replay_last(canon=None):
    """
    UI-facing adapter.
    Replays canon up to the most recent log entry.

    Returns a structured dict in ALL cases.
    """

    # ---- no canon ----
    if canon is None:
        return {
            "ok": False,
            "reason": "no_canon",
            "replayed_until": None,
            "event_count": 0,
            "truth_count": 0,
        }

    # ---- no event log ----
    if not hasattr(canon, "event_log") or not canon.event_log:
        return {
            "ok": False,
            "reason": "no_event_log",
            "replayed_until": None,
            "event_count": 0,
            "truth_count": 0,
        }

    last_log = canon.event_log[-1]
    log_id = last_log.get("log_id")

    # ---- invalid log ----
    if log_id is None:
        return {
            "ok": False,
            "reason": "invalid_log_entry",
            "replayed_until": None,
            "event_count": 0,
            "truth_count": 0,
        }

    # ---- successful replay ----
    new_canon = replay_until(canon, log_id)

    return {
        "ok": True,
        "reason": None,
        "replayed_until": log_id,
        "event_count": len(new_canon.events),
        "truth_count": len(new_canon.truths),
    }
