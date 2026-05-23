from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t
from app.ui.search_utils import entry_city, filter_entries_for_suggest


class SearchView(QWidget):
    book_chosen = Signal(int)
    map_requested = Signal()

    def __init__(self, locale: str = "tr") -> None:
        super().__init__()
        self._locale = locale
        self._entries: list[dict] = []

        top = QWidget()
        top.setObjectName("whyReadTop")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(24, 16, 24, 12)

        self._head = QLabel()
        self._head.setObjectName("whyReadHead")

        self._map_btn = QPushButton()
        self._map_btn.setObjectName("whyReadMapBtn")
        self._map_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._map_btn.clicked.connect(self.map_requested.emit)

        top_layout.addWidget(self._head, stretch=1)
        top_layout.addWidget(self._map_btn)

        self._input = QLineEdit()
        self._input.setObjectName("sidebarSearchInput")
        self._input.textChanged.connect(self._on_text)
        self._input.returnPressed.connect(self._pick_first)
        self._input.setFocus()

        self._list = QListWidget()
        self._list.setObjectName("sidebarSearchList")
        self._list.itemClicked.connect(self._on_item_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        w2 = QWidget()
        wl = QVBoxLayout(w2)
        wl.setContentsMargins(24, 12, 24, 24)
        wl.setSpacing(10)
        wl.addWidget(self._input)
        wl.addWidget(self._list, stretch=1)
        layout.addWidget(w2, stretch=1)

        self.apply_language(locale)

    def set_entries(self, entries: list[dict]) -> None:
        self._entries = entries
        if not self._input.text().strip():
            self._show_suggestions()

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        self._head.setText("\U0001F50D  " + t(locale, "btn_search"))
        self._map_btn.setText(t(locale, "btn_map"))
        self._input.setPlaceholderText("\U0001F50D  " + t(locale, "search_placeholder"))

    def focus_search(self) -> None:
        self._input.setFocus()
        self._input.selectAll()

    def _show_suggestions(self) -> None:
        self._list.clear()
        for e in (self._entries or [])[:20]:
            city = entry_city(e)
            line = f"{e.get('title', '')}  \u2014  {e.get('author', '')}"
            if city:
                line += f"  \u00b7  {city}"
            it = QListWidgetItem(line)
            it.setData(Qt.ItemDataRole.UserRole, int(e.get("id", 0)))
            self._list.addItem(it)

    def _on_text(self, text: str) -> None:
        self._list.clear()
        if not text.strip():
            self._show_suggestions()
            return
        matches = filter_entries_for_suggest(self._entries, text, limit=20)
        if not matches:
            return
        for e in matches:
            city = entry_city(e)
            line = f"{e.get('title', '')}  \u2014  {e.get('author', '')}"
            if city:
                line += f"  \u00b7  {city}"
            it = QListWidgetItem(line)
            it.setData(Qt.ItemDataRole.UserRole, int(e.get("id", 0)))
            self._list.addItem(it)

    def _pick_first(self) -> None:
        if self._list.count() > 0:
            self._activate(self._list.item(0))

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        self._activate(item)

    def _activate(self, item: QListWidgetItem | None) -> None:
        if item is None:
            return
        bid = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(bid, int) and bid > 0:
            self.book_chosen.emit(bid)
