from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t

LOCALES = [
    ("tr", "Türkçe"),
    ("en", "English"),
    ("de", "Deutsch"),
    ("es", "Español"),
    ("fr", "Français"),
    ("ja", "日本語"),
    ("ru", "Русский"),
    ("zh", "中文"),
    ("he", "עברית"),
    ("ky", "Кыргызча"),
]


class SidebarWidget(QWidget):
    book_catalog_requested = Signal()
    online_read_requested = Signal()
    about_requested = Signal()
    stats_requested = Signal()
    why_read_requested = Signal()
    search_requested = Signal()
    locale_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarRoot")
        self.setMinimumWidth(260)
        self.setMaximumWidth(320)
        self._locale = "tr"

        self._title = QLabel()
        self._title.setObjectName("sidebarTitle")

        self._tag = QLabel()
        self._tag.setObjectName("sidebarTag")
        self._tag.setWordWrap(True)

        locale_bar = QWidget()
        locale_bar.setObjectName("localeBar")
        loc_layout = QHBoxLayout(locale_bar)
        loc_layout.setContentsMargins(0, 0, 0, 0)
        loc_layout.setSpacing(6)

        self._loc_label = QLabel()
        self._loc_label.setObjectName("localeLabel")

        self._lang_combo = QComboBox()
        self._lang_combo.setObjectName("langCombo")
        for code, name in LOCALES:
            self._lang_combo.addItem(name, code)
        self._lang_combo.currentIndexChanged.connect(self._on_combo_change)

        loc_layout.addWidget(self._loc_label)
        loc_layout.addWidget(self._lang_combo, stretch=1)

        self.btn_search = QPushButton()
        self.btn_search.setObjectName("sidebarSearchBtn")
        self.btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_search.clicked.connect(self.search_requested.emit)

        self.btn_why_read = QPushButton()
        self.btn_why_read.setObjectName("sidebarWhyBtn")
        self.btn_why_read.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_why_read.clicked.connect(self.why_read_requested.emit)

        self.btn_books = QPushButton()
        self.btn_books.setObjectName("sidebarPrimaryBtn")
        self.btn_books.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_books.clicked.connect(self.book_catalog_requested.emit)

        self.btn_online_read = QPushButton()
        self.btn_online_read.setObjectName("sidebarReadBtn")
        self.btn_online_read.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_online_read.clicked.connect(self.online_read_requested.emit)

        self.btn_stats = QPushButton()
        self.btn_stats.setObjectName("sidebarStatsBtn")
        self.btn_stats.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stats.clicked.connect(self.stats_requested.emit)

        self.btn_about = QPushButton()
        self.btn_about.setObjectName("sidebarGhostBtn")
        self.btn_about.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_about.clicked.connect(self.about_requested.emit)

        self._footer = QLabel()
        self._footer.setObjectName("sidebarFooter")
        self._footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 18, 16, 16)
        layout.setSpacing(8)
        layout.addWidget(self._title)
        layout.addWidget(self._tag)
        layout.addWidget(locale_bar)
        layout.addSpacing(4)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_why_read)
        layout.addWidget(self.btn_books)
        layout.addWidget(self.btn_online_read)
        layout.addWidget(self.btn_stats)
        layout.addWidget(self.btn_about)
        layout.addStretch(1)
        layout.addWidget(self._footer)

        self.apply_language(self._locale)

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        self._title.setText(t(self._locale, "app_title"))
        self._tag.setText(t(self._locale, "sidebar_tag"))
        self._loc_label.setText(t(self._locale, "lang_label"))
        self.btn_search.setText("\U0001F50D  " + t(self._locale, "btn_search"))
        self.btn_why_read.setText("\U0001F4DA  " + t(self._locale, "btn_why_read"))
        self.btn_books.setText("\U0001F4D6  " + t(self._locale, "btn_books"))
        self.btn_online_read.setText("\U0001F4DA  " + t(self._locale, "btn_online_read"))
        self.btn_stats.setText("\U0001F4CA  " + t(self._locale, "btn_stats"))
        self.btn_about.setText("\U00002139  " + t(self._locale, "btn_about"))
        self._footer.setText(t(self._locale, "footer"))

    def set_entries(self, entries: list[dict]) -> None:
        pass

    def _apply_locale(self, code: str) -> None:
        self.apply_language(code)
        self.locale_changed.emit(code)

    def _on_combo_change(self, index: int) -> None:
        code = self._lang_combo.itemData(index)
        if code and code != self._locale:
            self._apply_locale(code)
