from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t
from app.ui.about_view import AboutView
from app.ui.admin_dialog import AdminLoginDialog
from app.ui.book_list_view import BookListView
from app.ui.map_container import MapWithSearchOverlay
from app.ui.online_read_view import OnlineReadView
from app.ui.search_view import SearchView
from app.ui.sidebar import SidebarWidget
from app.ui.stats_view import StatsView
from app.ui.book_reader_widget import BookReaderWidget


class MainWindow(QMainWindow):
    def __init__(self, entries: list[dict] | None = None) -> None:
        super().__init__()
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setMinimumSize(1920, 1080)
        self.resize(1920, 1080)

        self.entries: list[dict] = entries or []
        self._locale: str = "tr"
        self._sidebar_visible = True
        self.setWindowTitle(t(self._locale, "app_title"))

        self.sidebar = SidebarWidget()

        self.map_stack = MapWithSearchOverlay()
        self.why_read = BookReaderWidget()
        self.search_view = SearchView(self._locale)
        self.book_list_view = BookListView(self.entries, self._locale)
        self.online_view = OnlineReadView(self._locale)
        self.stats_view = StatsView(self.entries, self._locale)
        self.about_view = AboutView(self._locale)
        self.sidebar.set_entries(self.entries)
        self.search_view.set_entries(self.entries)

        self._view_stack = QStackedWidget()
        self._view_stack.addWidget(self.map_stack)       # 0
        self._view_stack.addWidget(self.why_read)        # 1
        self._view_stack.addWidget(self.search_view)     # 2
        self._view_stack.addWidget(self.book_list_view)  # 3
        self._view_stack.addWidget(self.online_view)     # 4
        self._view_stack.addWidget(self.stats_view)      # 5
        self._view_stack.addWidget(self.about_view)      # 6
        self._view_stack.setCurrentIndex(0)

        self.sidebar.search_requested.connect(lambda: (self._switch_view(2), self.search_view.focus_search()))
        self.sidebar.why_read_requested.connect(lambda: self._switch_view(1))
        self.sidebar.book_catalog_requested.connect(lambda: self._switch_view(3))
        self.sidebar.online_read_requested.connect(lambda: self._switch_view(4))
        self.sidebar.stats_requested.connect(lambda: self._switch_view(5))
        self.sidebar.about_requested.connect(lambda: self._switch_view(6))
        self.sidebar.locale_changed.connect(self._on_locale_changed)

        self.why_read.map_requested.connect(lambda: self._switch_view(0))
        self.search_view.map_requested.connect(lambda: self._switch_view(0))
        self.search_view.book_chosen.connect(self._on_sidebar_book)
        self.book_list_view.map_requested.connect(lambda: self._switch_view(0))
        self.book_list_view.book_chosen.connect(self._on_sidebar_book)
        self.online_view.map_requested.connect(lambda: self._switch_view(0))
        self.stats_view.map_requested.connect(lambda: self._switch_view(0))
        self.about_view.map_requested.connect(lambda: self._switch_view(0))
        self._sidebar_width = 300
        self._toggle_btn = QPushButton("\u25C0")
        self._toggle_btn.setObjectName("sidebarToggleBtn")
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setFixedSize(28, 48)
        self._toggle_btn.clicked.connect(self._toggle_sidebar)

        view_wrapper = QWidget()
        view_wrapper.setObjectName("viewWrapper")
        vw_layout = QHBoxLayout(view_wrapper)
        vw_layout.setContentsMargins(0, 0, 0, 0)
        vw_layout.setSpacing(0)
        vw_layout.addWidget(self._toggle_btn)
        vw_layout.addWidget(self._view_stack, stretch=1)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(view_wrapper)
        self.splitter.setSizes([self._sidebar_width, 1000])
        self.splitter.splitterMoved.connect(self._on_splitter_moved)

        central = QWidget()
        central_layout = QHBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_layout.addWidget(self.splitter)

        self.setCentralWidget(central)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.map_stack.set_entries(self.entries, self._locale)

        n = len(self.entries)
        self.status.showMessage(
            t(self._locale, "status_loaded").format(n=n) if self.entries
            else t(self._locale, "status_load_error")
        )

        QShortcut(QKeySequence("Ctrl+Shift+A"), self, activated=self._open_admin_login)
        QShortcut(QKeySequence("Ctrl+B"), self, activated=self._toggle_sidebar)

    def _toggle_sidebar(self) -> None:
        self._sidebar_visible = not self._sidebar_visible
        sizes = self.splitter.sizes()
        if self._sidebar_visible:
            total = sizes[0] + sizes[1]
            self.splitter.setSizes([self._sidebar_width, total - self._sidebar_width])
            self._toggle_btn.setText("\u25C0")
            self._toggle_btn.setObjectName("sidebarToggleBtn")
        else:
            self._sidebar_width = sizes[0]
            self.splitter.setSizes([0, sizes[0] + sizes[1]])
            self._toggle_btn.setText("\u25B6")
            self._toggle_btn.setObjectName("sidebarToggleBtnClosed")
        self._toggle_btn.style().unpolish(self._toggle_btn)
        self._toggle_btn.style().polish(self._toggle_btn)

    def _on_splitter_moved(self, pos: int, index: int) -> None:
        sizes = self.splitter.sizes()
        if sizes[0] > 10:
            self._sidebar_visible = True
            self._sidebar_width = sizes[0]
            self._toggle_btn.setText("\u25C0")
            self._toggle_btn.setObjectName("sidebarToggleBtn")
        else:
            self._sidebar_visible = False
            self._toggle_btn.setText("\u25B6")
            self._toggle_btn.setObjectName("sidebarToggleBtnClosed")
        self._toggle_btn.style().unpolish(self._toggle_btn)
        self._toggle_btn.style().polish(self._toggle_btn)

    def _switch_view(self, index: int) -> None:
        self._view_stack.setCurrentIndex(index)

    def _on_sidebar_book(self, book_id: int) -> None:
        self._switch_view(0)
        self.map_stack.map_view.fly_to_book(book_id)

    def _on_locale_changed(self, locale: str) -> None:
        self._locale = locale
        self.setWindowTitle(t(self._locale, "app_title"))
        self.map_stack.set_entries(self.entries, self._locale)
        self.why_read.apply_language(locale)
        self.search_view.apply_language(locale)
        self.book_list_view.apply_language(locale)
        self.online_view.apply_language(locale)
        self.stats_view.apply_language(locale)
        self.about_view.apply_language(locale)
        n = len(self.entries)
        self.status.showMessage(
            t(locale, "status_loaded").format(n=n) if self.entries
            else t(locale, "status_load_error")
        )

    def _open_admin_login(self) -> None:
        dialog = AdminLoginDialog(self)
        if dialog.exec() and dialog.authenticated:
            QMessageBox.information(
                self,
                "Admin Vault",
                "Admin authentication successful.\nAdmin management tools will be enabled in next step.",
            )
