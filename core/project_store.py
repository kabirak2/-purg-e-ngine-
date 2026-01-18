from typing import Optional
from core import filesystem
from core.canon import Canon


class ProjectStore:
    """
    In-memory authority for the currently loaded project.

    Responsibilities:
    - Track active project filename
    - Hold the active Canon instance
    - Track dirty state (unsaved changes)
    """

    def __init__(self):
        self.active_project: Optional[str] = None
        self.canon: Canon = Canon()
        self.dirty: bool = False

    # ------------------------------------------------------------------
    # Project lifecycle
    # ------------------------------------------------------------------

    def new_project(self, name: str):
        """
        Create a new empty project in memory.
        Does NOT save to disk.
        """
        if not name.endswith(".json"):
            name += ".json"

        self.active_project = name
        self.canon = Canon()
        self.canon.meta["title"] = name.replace(".json", "")
        self.dirty = True

    def open_project(self, filename: str):
        """
        Load an existing project from disk and replace memory.
        """
        data = filesystem.load_project(filename)

        canon = Canon()
        canon.load_from_dict(data)

        self.active_project = filename
        self.canon = canon
        self.dirty = False

    def reset_project(self):
        """
        Reset the current project in memory only.
        """
        self.canon = Canon()
        self.dirty = True

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self):
        """
        Save to the currently active project file.
        """
        if not self.active_project:
            raise RuntimeError("No active project to save")

        filesystem.save_project(
            self.active_project,
            self.canon.to_dict()
        )
        self.dirty = False

    def save_as(self, filename: str, overwrite: bool = False):
        """
        Save the current canon under a new filename.
        """
        if not filename.endswith(".json"):
            filename += ".json"

        if filesystem.project_exists(filename) and not overwrite:
            raise FileExistsError(filename)

        filesystem.save_project(
            filename,
            self.canon.to_dict()
        )

        self.active_project = filename
        self.dirty = False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def list_projects(self):
        """
        Return available projects for UI dropdown.
        """
        return filesystem.list_projects()

    def mark_dirty(self):
        """
        Mark project as having unsaved changes.
        """
        self.dirty = True
