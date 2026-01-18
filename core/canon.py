from core.snapshot import take_snapshot
from core.integrity import compute_integrity
from core.dependency_graph import DependencyGraph
from core.rule_decay import decay_rules
from core.config import SAVE_POLICY
from core.paradox_engine import detect_paradoxes


class Canon:
    def __init__(self):
        # ---------------- CORE ----------------
        self.meta = {
            "title": "",
            "author": "",
            "version": "0.1",
        }

        self.truths = {}
        self.rules = []
        self.events = []

        # ---------------- TIMELINE ----------------
        self.acts = []

        # ---------------- STRUCTURE ----------------
        self.graph = DependencyGraph()   # ← FIX 1

        # ---------------- OPTIONAL ----------------
        self.event_log = []
        self.snapshots = []
        self.integrity = {}
        self.active_branch = "main"
        self.characters = {}
        self.fatigue = 0.0
        self.telemetry = {}

    # ---------------- RULES ----------------

    def add_rule(self, rule):
        rule.setdefault("strength", 1.0)
        rule.setdefault("overridden", False)
        self.rules.append(rule)

    # ---------------- EVENTS ----------------

    def add_event(self, event):
        self.events.append(event)

        # postconditions
        for t in event.get("postconditions", []):
            self.truths[t] = True

        # snapshots & integrity
        try:
            self.snapshots.append(
                take_snapshot(self, event.get("act", 0))
            )
            self.integrity = compute_integrity(self)
        except Exception:
            pass

        # rule decay
        try:
            decay_rules(self)
        except Exception:
            pass

        # dependency graph
        for dep in event.get("depends_on", []):
            self.graph.add_dependency(event["id"], dep)

    # ---------------- LOGGING ----------------

    def log_event(self, entry):
        entry["branch_id"] = self.active_branch
        self.event_log.append(entry)

    # ---------------- SERIALIZATION ----------------

    def to_dict(self):
        data = {
            "meta": self.meta,
            "truths": self.truths,
            "rules": self.rules,
            "events": self.events,
            "acts": self.acts,
        }

        if SAVE_POLICY.get("event_log"):
            data["event_log"] = self.event_log

        if SAVE_POLICY.get("snapshots"):
            data["snapshots"] = self.snapshots

        if SAVE_POLICY.get("integrity"):
            data["integrity"] = self.integrity

        if SAVE_POLICY.get("branches"):
            data["branch"] = self.active_branch

        if SAVE_POLICY.get("dependencies"):
            data["dependencies"] = self.graph.to_dict()

        if SAVE_POLICY.get("characters"):
            data["characters"] = self.characters

        if SAVE_POLICY.get("fatigue"):
            data["fatigue"] = self.fatigue

        if SAVE_POLICY.get("telemetry"):
            data["telemetry"] = self.telemetry

        return data

    def load_from_dict(self, data: dict):
        self.meta = data.get("meta", {})
        self.truths = data.get("truths", {})
        self.rules = data.get("rules", [])
        self.events = data.get("events", [])
        self.acts = data.get("acts", [])        # ← FIX 2

        self.event_log = data.get("event_log", [])
        self.snapshots = data.get("snapshots", [])
        self.integrity = data.get("integrity", {})
        self.active_branch = data.get("branch", "main")

        if "dependencies" in data:
            self.graph.from_dict(data["dependencies"])

        self.characters = data.get("characters", {})
        self.fatigue = data.get("fatigue", 0.0)
        self.telemetry = data.get("telemetry", {})

    # ---------------- PARADOX ----------------

    def detect_paradoxes(self):
        return detect_paradoxes(self)

    # ---------------- UI / RUNTIME ----------------

    def apply_event(self, event):
        self.events.append(event)

        for k, v in event.get("sets_truths", {}).items():
            self.truths[k] = v

        self.event_log.append({
            "log_id": f"log_{len(self.event_log)+1}",
            "commit": {"written_to_canon": True},
            "payload": event,
        })
