from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from app.i18n import t
from app.ui.search_utils import entry_city, entry_matches_query


class BookListDialog(QDialog):
    book_selected = Signal(int)

    def __init__(self, entries: list[dict], parent=None, locale: str = "tr") -> None:
        super().__init__(parent)
        self._locale = locale
        self._all_entries = sorted(entries, key=lambda e: str(e.get("title", "")).lower())
        self.setWindowTitle(t(self._locale, "book_list_window"))
        self.resize(560, 680)
        self.setModal(True)

        self._title = QLabel()
        self._title.setObjectName("bookListTitle")

        self._hint = QLabel()
        self._hint.setObjectName("aboutSub")
        self._hint.setWordWrap(True)

        self._search = QLineEdit()
        self._search.setObjectName("bookListSearch")
        self._search.setPlaceholderText("Kitap adi, yazar veya sehir ara...")
        self._search.textChanged.connect(self._filter)

        self._list = QListWidget()
        self._list.setAlternatingRowColors(True)
        self._list.itemDoubleClicked.connect(self._emit_and_close)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addWidget(self._title)
        layout.addWidget(self._hint)
        layout.addWidget(self._search)
        layout.addWidget(self._list, stretch=1)
        layout.addWidget(buttons)

        self._apply_texts()
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

    def _emit_and_close(self, item: QListWidgetItem) -> None:
        book_id = item.data(Qt.ItemDataRole.UserRole)
        self.book_selected.emit(book_id)
        self.accept()

    def _apply_texts(self) -> None:
        self.setWindowTitle(t(self._locale, "book_list_window"))
        self._title.setText(t(self._locale, "book_list_title"))
        self._hint.setText(t(self._locale, "book_list_hint"))
