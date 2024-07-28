
from pathlib import Path


def get_project_root(search_marker):
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / search_marker).exists():
            return parent
    raise RuntimeError(f"Project root with marker '{search_marker}' not found")