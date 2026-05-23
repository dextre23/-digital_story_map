from PySide6.QtWidgets import QWidget

from app.ui.map_view import MapView


class MapWithSearchOverlay(QWidget):
    """Full-bleed map with no floating search overlay."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._map = MapView(self)

    @property
    def map_view(self) -> MapView:
        return self._map

    def apply_language(self, locale: str) -> None:
        self._map.apply_language(locale) if hasattr(self._map, 'apply_language') else None

    def set_entries(self, entries: list[dict], locale: str = "tr") -> None:
        self._map.set_entries(entries, locale)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._map.setGeometry(self.rect())
