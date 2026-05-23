import webbrowser

import requests
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QSplitter,
    QWidget,
    QScrollArea,
)

from app.i18n import t

OPEN_LIBRARY_BASE = "https://openlibrary.org"
COVERS_BASE = "https://covers.openlibrary.org/b"


class SearchSignals(QObject):
    done = Signal(list, str)
    error = Signal(str)


class SearchWorker(QRunnable):
    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query
        self.signals = SearchSignals()

    def run(self) -> None:
        try:
            url = f"{OPEN_LIBRARY_BASE}/search.json?q={self.query}&limit=30"
            r = requests.get(url, timeout=12)
            r.raise_for_status()
            data = r.json()
            docs = data.get("docs", [])
            results = []
            for doc in docs:
                isbns = doc.get("isbn", [])
                key = doc.get("key", "")
                results.append({
                    "title": doc.get("title", "?"),
                    "author": ", ".join(doc.get("author_name", ["?"])),
                    "year": doc.get("first_publish_year", ""),
                    "isbn": str(isbns[0]) if isbns else "",
                    "key": key,
                    "olid": key.replace("/works/", "") if key else "",
                    "cover_i": doc.get("cover_i"),
                    "cover_ed": doc.get("cover_edition_key"),
                })
            self.signals.done.emit(results, "")
        except Exception as e:
            self.signals.error.emit(str(e))


class CoverSignals(QObject):
    done = Signal(object)


class CoverWorker(QRunnable):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self.signals = CoverSignals()

    def run(self) -> None:
        urls = []
        if self.data.get("cover_i"):
            urls.append(f"{COVERS_BASE}/id/{self.data['cover_i']}-L.jpg")
        if self.data.get("cover_ed"):
            urls.append(f"{COVERS_BASE}/olid/{self.data['cover_ed']}-L.jpg")
        if self.data.get("isbn"):
            urls.append(f"{COVERS_BASE}/isbn/{self.data['isbn']}-L.jpg")

        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    pm = QPixmap()
                    pm.loadFromData(resp.content)
                    if not pm.isNull():
                        pm = pm.scaled(140, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        self.signals.done.emit(pm)
                        return
            except Exception:
                continue
        self.signals.done.emit(None)


class DetailSignals(QObject):
    done = Signal(dict)


class DetailWorker(QRunnable):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key
        self.signals = DetailSignals()

    def run(self) -> None:
        result = {"desc": "", "publishers": [], "pub_date": "", "pages": "", "subjects": []}
        try:
            url = f"{OPEN_LIBRARY_BASE}{self.key}.json"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            wd = r.json()
            desc = wd.get("description", "")
            if isinstance(desc, dict):
                desc = desc.get("value", "")
            result["desc"] = desc[:1000] if desc else ""
            result["publishers"] = wd.get("publishers", [])
            result["pub_date"] = wd.get("first_publish_date") or wd.get("publish_date", "")
            result["pages"] = wd.get("number_of_pages", "")
            result["subjects"] = wd.get("subjects", [])[:6]
        except Exception:
            pass
        self.signals.done.emit(result)


class OnlineReaderDialog(QDialog):
    def __init__(self, parent=None, locale: str = "tr") -> None:
        super().__init__(parent)
        self._locale = locale
        self.setWindowTitle(t(self._locale, "online_reader_window"))
        self.resize(1100, 750)

        self._pool = QThreadPool.globalInstance()
        self._book_data: dict[int, dict] = {}
        self._current_book: dict | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        hdr = QLabel(t(self._locale, "online_reader_title"))
        hdr.setObjectName("readerTitle")
        layout.addWidget(hdr)

        hint = QLabel(t(self._locale, "online_reader_hint"))
        hint.setObjectName("readerHint")
        layout.addWidget(hint)

        srch = QHBoxLayout()
        srch.setSpacing(6)
        self._input = QLineEdit()
        self._input.setObjectName("readerSearchInput")
        self._input.setPlaceholderText("Kitap adı, yazar veya ISBN ara…")
        self._input.returnPressed.connect(self._search)
        btn = QPushButton(" Ara")
        btn.setObjectName("readerSearchBtn")
        btn.clicked.connect(self._search)
        srch.addWidget(self._input)
        srch.addWidget(btn)
        layout.addLayout(srch)

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

        self._read_btn = QPushButton("📖 Çevrimiçi Oku")
        self._read_btn.setObjectName("readerReadBtn")
        self._read_btn.clicked.connect(self._open_read)
        self._read_btn.setVisible(False)
        dl.addWidget(self._read_btn)

        dl.addStretch()
        sc.setWidget(self._detail)
        rl.addWidget(sc)

        self._splitter.addWidget(right)
        self._splitter.setSizes([300, 800])
        layout.addWidget(self._splitter, stretch=1)

        self._show_placeholder()

    def _show_placeholder(self):
        self._cover.setText("\U0001F4DA")
        self._cover.setStyleSheet("color: #555; font-size: 48px; padding: 30px;")
        self._title_lbl.setText("<i>Arama sonucunda bir kitap seçin</i>")
        self._author_lbl.setText("")
        self._meta_lbl.setText("")
        self._desc_lbl.setText("")
        self._read_btn.setVisible(False)

    def _search(self):
        q = self._input.text().strip()
        if not q:
            return
        self._list.clear()
        self._book_data.clear()
        self._current_book = None
        self._show_placeholder()
        self._title_lbl.setText("<i>Aranıyor…</i>")

        worker = SearchWorker(q)
        worker.signals.done.connect(self._on_search_done)
        worker.signals.error.connect(self._on_search_error)
        self._pool.start(worker)

    def _on_search_done(self, results: list, _msg: str):
        if not results:
            self._title_lbl.setText("<i>Sonuç bulunamadı.</i>")
            return

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
            parts.append(f"📅 {data['year']}")
        if data["isbn"]:
            parts.append(f"🔖 ISBN: {data['isbn']}")
        if data["olid"]:
            parts.append(f"📄 OLID: {data['olid']}")
        self._meta_lbl.setText(" | ".join(parts) if parts else "")

        self._desc_lbl.setText("<i>Bilgiler yükleniyor…</i>")
        self._read_btn.setVisible(False)

        worker_c = CoverWorker(data)
        worker_c.signals.done.connect(self._on_cover_done)
        self._pool.start(worker_c)

        if data.get("key"):
            worker_d = DetailWorker(data["key"])
            worker_d.signals.done.connect(self._on_detail_done)
            self._pool.start(worker_d)

        self._read_btn.setVisible(bool(data["olid"]))

    def _on_cover_done(self, pixmap):
        if pixmap is not None:
            self._cover.setPixmap(pixmap)
            self._cover.setFixedHeight(210)
        else:
            self._cover.setText("📚\nKapak yok")
            self._cover.setStyleSheet("color: #666; font-size: 16px; padding: 40px;")

    def _on_detail_done(self, info: dict):
        if info["desc"]:
            subs = info.get("subjects", [])
            desc = info["desc"]
            if subs:
                desc += f"\n\n<b>Konular:</b> {', '.join(subs)}"
            self._desc_lbl.setText(desc)

        pub_parts = []
        if info["publishers"]:
            pub_parts.append(f"Yayınevi: {', '.join(info['publishers'][:2])}")
        if info["pub_date"]:
            pub_parts.append(f"Yayın: {info['pub_date']}")
        if info["pages"]:
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
