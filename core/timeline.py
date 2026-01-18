from copy import deepcopy


def build_timeline(canon):
    """
    Replays events one by one and records canon + paradox state after each.
    Returns a list of timeline steps.
    """
    steps = []

    working = deepcopy(canon)
    working.events = []
    working.truths = {}
    working.event_log = []

    for idx, event in enumerate(canon.events):
        working.apply_event(event)

        paradoxes = working.detect_paradoxes()

        steps.append({
            "index": idx + 1,
            "event": event,
            "truths": dict(working.truths),
            "paradoxes": paradoxes,
        })

    return steps
