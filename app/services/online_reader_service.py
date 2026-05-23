import requests
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

OPEN_LIBRARY_BASE = "https://openlibrary.org"
COVERS_BASE = "https://covers.openlibrary.org/b"


class _SearchSignals(QObject):
    done = Signal(list, str)
    error = Signal(str)


class _SearchWorker(QRunnable):
    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query
        self.signals = _SearchSignals()

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


class _CoverSignals(QObject):
    done = Signal(object)


class _CoverWorker(QRunnable):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data
        self.signals = _CoverSignals()

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


class _DetailSignals(QObject):
    done = Signal(dict)


class _DetailWorker(QRunnable):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key
        self.signals = _DetailSignals()

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


class OnlineReaderService:
    def __init__(self) -> None:
        self._pool = QThreadPool.globalInstance()

    def search(self, query: str, on_done, on_error) -> None:
        worker = _SearchWorker(query)
        worker.signals.done.connect(on_done)
        worker.signals.error.connect(on_error)
        self._pool.start(worker)

    def load_cover(self, data: dict, on_done) -> None:
        worker = _CoverWorker(data)
        worker.signals.done.connect(on_done)
        self._pool.start(worker)

    def load_detail(self, key: str, on_done) -> None:
        worker = _DetailWorker(key)
        worker.signals.done.connect(on_done)
        self._pool.start(worker)
