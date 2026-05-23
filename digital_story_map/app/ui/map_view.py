from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from app.services.map_http_server import MapHttpServer
from app.services.map_service import build_map_html


class MapView(QWebEngineView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._entries: list[dict] = []
        self._locale: str = "tr"
        self._server = MapHttpServer.instance()
        self._server.ensure_running()

        s = self.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)

    def set_entries(self, entries: list[dict], locale: str = "tr") -> None:
        self._entries = entries
        self._locale = locale
        self._server.ensure_running()
        self._server.set_html(build_map_html(entries, locale))
        self.load(QUrl(self._server.url_with_cache_bust()))

    def fly_to_book(self, book_id: int) -> None:
        self.page().runJavaScript(
            f"if (typeof window.flyToBook === 'function') {{ window.flyToBook({book_id}); }}"
        )
