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
from app.ui.search_utils import entry_city, entry_matches_query


class BookListView(QWidget):
    book_chosen = Signal(int)
    map_requested = Signal()

    def __init__(self, entries: list[dict] | None = None, locale: str = "tr") -> None:
        super().__init__()
        self._locale = locale
        self._all_entries = sorted(entries or [], key=lambda e: str(e.get("title", "")).lower())

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

        self._hint = QLabel()
        self._hint.setObjectName("aboutSub")
        self._hint.setWordWrap(True)

        self._search = QLineEdit()
        self._search.setObjectName("bookListSearch")
        self._search.textChanged.connect(self._filter)

        self._list = QListWidget()
        self._list.setAlternatingRowColors(True)
        self._list.itemDoubleClicked.connect(self._emit_and_fly)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        w2 = QWidget()
        wl = QVBoxLayout(w2)
        wl.setContentsMargins(24, 12, 24, 24)
        wl.setSpacing(10)
        wl.addWidget(self._hint)
        wl.addWidget(self._search)
        wl.addWidget(self._list, stretch=1)
        layout.addWidget(w2, stretch=1)

        self.apply_language(locale)
        self._populate_list(self._all_entries)

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        self._head.setText("\U0001F4D6  " + t(locale, "book_list_title"))
        self._map_btn.setText(t(locale, "btn_map"))
        self._hint.setText(t(locale, "book_list_hint"))

    def set_entries(self, entries: list[dict]) -> None:
        self._all_entries = sorted(entries, key=lambda e: str(e.get("title", "")).lower())
        self._populate_list(self._all_entries)

    def _populate_list(self, entries: list[dict]) -> None:
        self._list.clear()
        for e in entries:
            city = entry_city(e)
            line = f"{e.get('title', '')} \u2014 {e.get('author', '')}"
            if city:
                line += f"  ({city})"
            it = QListWidgetItem(line)
            it.setData(Qt.ItemDataRole.UserRole, int(e.get("id", 0)))
            self._list.addItem(it)

    def _filter(self, text: str) -> None:
        q = text.strip().lower()
        if not q:
            self._populate_list(self._all_entries)
            return
        filtered = [e for e in self._all_entries if entry_matches_query(e, q)]
        self._populate_list(filtered)

    def _emit_and_fly(self, item: QListWidgetItem) -> None:
        book_id = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(book_id, int) and book_id > 0:
            self.book_chosen.emit(book_id)
