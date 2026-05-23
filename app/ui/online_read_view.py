import webbrowser

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t
from app.services.online_reader_service import OnlineReaderService


class OnlineReadView(QWidget):
    map_requested = Signal()

    def __init__(self, locale: str = "tr") -> None:
        super().__init__()
        self._locale = locale
        self._service = OnlineReaderService()
        self._current_book: dict | None = None
        self._book_data: dict[int, dict] | None = None

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
        self._hint.setObjectName("readerHint")

        srch = QHBoxLayout()
        srch.setSpacing(6)
        self._input = QLineEdit()
        self._input.setObjectName("readerSearchInput")
        self._input.returnPressed.connect(self._search)
        self._srch_btn = QPushButton()
        self._srch_btn.setObjectName("readerSearchBtn")
        self._srch_btn.clicked.connect(self._search)
        srch.addWidget(self._input)
        srch.addWidget(self._srch_btn)

        self._splitter = QSplitter(Qt.Orientation.Horizontal)

        self._list = QListWidget()
        self._list.setObjectName("readerResultsList")
        self._list.setMinimumWidth(260)
        self._list.itemClicked.connect(self._show_detail)
        self._splitter.addWidget(self._list)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(8, 0, 0, 0)
        rl.setSpacing(0)

        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setObjectName("readerScroll")

        self._detail = QWidget()
        dl = QVBoxLayout(self._detail)
        dl.setSpacing(8)

        self._cover = QLabel()
        self._cover.setObjectName("readerCover")
        self._cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._cover.setFixedHeight(200)
        dl.addWidget(self._cover)

        self._title_lbl = QLabel()
        self._title_lbl.setObjectName("readerDetailTitle")
        self._title_lbl.setWordWrap(True)
        dl.addWidget(self._title_lbl)

        self._author_lbl = QLabel()
        self._author_lbl.setObjectName("readerDetailAuthor")
        self._author_lbl.setWordWrap(True)
        dl.addWidget(self._author_lbl)

        self._meta_lbl = QLabel()
        self._meta_lbl.setObjectName("readerDetailMeta")
        self._meta_lbl.setWordWrap(True)
        dl.addWidget(self._meta_lbl)

        self._desc_lbl = QLabel()
        self._desc_lbl.setObjectName("readerDetailDesc")
        self._desc_lbl.setWordWrap(True)
        self._desc_lbl.setAlignment(Qt.AlignmentFlag.AlignTop)
        dl.addWidget(self._desc_lbl)

        self._read_btn = QPushButton()
        self._read_btn.setObjectName("readerReadBtn")
        self._read_btn.clicked.connect(self._open_read)
        self._read_btn.setVisible(False)
        dl.addWidget(self._read_btn)

        dl.addStretch()
        sc.setWidget(self._detail)
        rl.addWidget(sc)

        self._splitter.addWidget(right)
        self._splitter.setSizes([300, 800])

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        w2 = QWidget()
        wl = QVBoxLayout(w2)
        wl.setContentsMargins(24, 12, 24, 24)
        wl.setSpacing(8)
        wl.addWidget(self._hint)
        wl.addLayout(srch)
        wl.addWidget(self._splitter, stretch=1)
        layout.addWidget(w2, stretch=1)

        self.apply_language(locale)
        self._show_placeholder()

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        self._head.setText("\U0001F4DA  " + t(locale, "online_reader_title"))
        self._map_btn.setText(t(locale, "btn_map"))
        self._hint.setText(t(locale, "online_reader_hint"))
        self._srch_btn.setText(t(locale, "reader_search_btn"))
        self._read_btn.setText(t(locale, "reader_read_btn"))

    def _show_placeholder(self):
        self._cover.setText("\U0001F4DA")
        self._cover.setStyleSheet("color: #555; font-size: 48px; padding: 30px;")
        self._title_lbl.setText(t(self._locale, "reader_placeholder"))
        self._author_lbl.setText("")
        self._meta_lbl.setText("")
        self._desc_lbl.setText("")
        self._read_btn.setVisible(False)

    def _search(self):
        q = self._input.text().strip()
        if not q:
            return
        self._list.clear()
        self._current_book = None
        self._show_placeholder()
        self._title_lbl.setText("<i>Aranıyor…</i>")
        self._service.search(q, self._on_search_done, self._on_search_error)

    def _on_search_done(self, results: list):
        if not results:
            self._title_lbl.setText("<i>Sonuç bulunamadı.</i>")
            return
        self._book_data = {}
        for i, r in enumerate(results):
            label = f"{r['title']}\n{r['author']}"
            if r["year"]:
                label += f" ({r['year']})"
            it = QListWidgetItem(label)
            self._book_data[i] = r
            self._list.addItem(it)
        self._list.setCurrentRow(0)
        self._show_detail(self._list.item(0))

    def _on_search_error(self, msg: str):
        self._title_lbl.setText(f"<b style='color:#e55;'>Hata:</b> {msg}")

    def _show_detail(self, item: QListWidgetItem):
        row = self._list.row(item)
        data = self._book_data.get(row)
        if not data:
            return
        self._current_book = data
        self._cover.clear()
        self._cover.setStyleSheet("")
        self._cover.setFixedHeight(200)
        self._title_lbl.setText(f"<b>{data['title']}</b>")
        self._author_lbl.setText(f"<i>{data['author']}</i>")
        parts = []
        if data["year"]:
            parts.append(f"\U0001F4C5 {data['year']}")
        if data.get("isbn"):
            parts.append(f"\U0001F516 ISBN: {data['isbn']}")
        if data.get("olid"):
            parts.append(f"\U0001F4C4 OLID: {data['olid']}")
        self._meta_lbl.setText(" | ".join(parts) if parts else "")
        self._desc_lbl.setText("<i>Bilgiler yükleniyor…</i>")
        self._read_btn.setVisible(False)
        self._service.load_cover(data, self._on_cover_done)
        if data.get("key"):
            self._service.load_detail(data["key"], self._on_detail_done)
        self._read_btn.setVisible(bool(data.get("olid")))

    def _on_cover_done(self, pixmap):
        if pixmap is not None:
            self._cover.setPixmap(pixmap)
            self._cover.setFixedHeight(210)
        else:
            self._cover.setText("\U0001F4DA\nKapak yok")
            self._cover.setStyleSheet("color: #666; font-size: 16px; padding: 40px;")

    def _on_detail_done(self, info: dict):
        if info.get("desc"):
            subs = info.get("subjects", [])
            desc = info["desc"]
            if subs:
                desc += f"\n\n<b>Konular:</b> {', '.join(subs)}"
            self._desc_lbl.setText(desc)
        pub_parts = []
        if info.get("publishers"):
            pub_parts.append(f"Yayınevi: {', '.join(info['publishers'][:2])}")
        if info.get("pub_date"):
            pub_parts.append(f"Yayın: {info['pub_date']}")
        if info.get("pages"):
            pub_parts.append(f"{info['pages']} sayfa")
        if pub_parts:
            existing = self._meta_lbl.text()
            self._meta_lbl.setText(existing + "\n" + "\n".join(pub_parts))

    def _open_read(self):
        if not self._current_book:
            return
        olid = self._current_book.get("olid") or self._current_book.get("cover_ed")
        isbn = self._current_book.get("isbn")
        url = ""
        if olid:
            url = f"https://openlibrary.org/works/{olid}?mode=reader"
        elif isbn:
            url = f"https://openlibrary.org/isbn/{isbn}?mode=reader"
        if url:
            webbrowser.open(url)
