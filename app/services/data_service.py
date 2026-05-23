import json
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal

from app.config import CACHE_FILE
from app.models import BookEntry


class DataService(QObject):
    loaded = Signal(list, bool, str)
    failed = Signal(str)

    def __init__(self) -> None:
        super().__init__()

    def load_async(self, cache_file: Path = CACHE_FILE) -> None:
        try:
            if cache_file.exists():
                raw = json.loads(cache_file.read_text(encoding="utf-8"))
                entries = [BookEntry.from_dict(item).to_dict() for item in raw]
                self.loaded.emit(entries, True, "Cached data loaded.")
            else:
                self.failed.emit("No cached data available.")
        except (json.JSONDecodeError, OSError) as exc:
            self.failed.emit(f"Cache read error: {exc}")
