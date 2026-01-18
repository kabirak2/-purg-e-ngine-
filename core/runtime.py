from core.project_store import ProjectStore

# ------------------------------------------------------------
# SINGLETON STORE (DO NOT DUPLICATE)
# ------------------------------------------------------------

_STORE = ProjectStore()


def get_store():
    return _STORE


def get_canon():
    return _STORE.canon


def open_project(filename: str):
    _STORE.open_project(filename)


def new_project(name: str):
    _STORE.new_project(name)


def save_project():
    _STORE.save()


def save_project_as(name: str, overwrite: bool = False):
    _STORE.save_as(name, overwrite=overwrite)


def reset_project():
    _STORE.reset_project()


def list_projects():
    return _STORE.list_projects()


def apply_event(event):
    """
    Apply an event and persist it.
    Requires an active project.
    """
    if not _STORE.active_project:
        raise RuntimeError("No active project to save")

    _STORE.canon.apply_event(event)
    _STORE.save()
