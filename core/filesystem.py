from pathlib import Path
import json
from typing import List

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# Public API (used by UI / project_store)
# -------------------------------------------------------------------

def list_projects() -> List[str]:
    """
    Return a sorted list of available project files.

    Only JSON files inside the projects directory are considered valid.
    """
    return sorted(p.name for p in PROJECTS_DIR.glob("*.json"))


def load_project(filename: str) -> dict:
    """
    Load a project from disk and return the canon dictionary.

    This performs NO validation or mutation.
    """
    path = PROJECTS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Project not found: {filename}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_project(filename: str, canon_dict: dict) -> None:
    """
    Save the given canon dictionary to disk.

    This function:
    - Does NOT invent filenames
    - Does NOT fork
    - Does NOT overwrite silently (UI must decide)
    - Does NOT validate canon logic
    """

    if not filename.endswith(".json"):
        raise ValueError("Project filename must end with .json")

    path = PROJECTS_DIR / filename

    safe_canon = _sanitize_canon(canon_dict)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(safe_canon, f, indent=2)


def project_exists(filename: str) -> bool:
    """
    Check whether a project file already exists.
    """
    return (PROJECTS_DIR / filename).exists()


# -------------------------------------------------------------------
# Internal helpers
# -------------------------------------------------------------------

def _sanitize_canon(canon_dict: dict) -> dict:
    """
    Defensive, non-destructive canon serialization.

    Only persists known stable fields.
    Optional systems are included if present.
    """

    safe = {
        "meta": canon_dict.get("meta", {}),
        "truths": canon_dict.get("truths", {}),
        "rules": canon_dict.get("rules", []),
        "events": canon_dict.get("events", []),
    }

    # Optional subsystems (never required)
    for key in (
        "event_log",
        "snapshots",
        "integrity",
        "branch",
        "dependencies",
        "characters",
        "fatigue",
        "telemetry",
    ):
        if key in canon_dict:
            safe[key] = canon_dict[key]

    return safe
