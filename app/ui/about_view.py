import webbrowser

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t


class AboutView(QWidget):
    map_requested = Signal()

    def __init__(self, locale: str = "tr") -> None:
        super().__init__()
        self._locale = locale

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

        scroll = QScrollArea()
        scroll.setObjectName("readerScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(24, 12, 24, 24)
        cl.setSpacing(14)

        self._sub = QLabel()
        self._sub.setObjectName("aboutSub")

        self._body = QLabel()
        self._body.setObjectName("aboutBody")
        self._body.setTextFormat(Qt.TextFormat.RichText)
        self._body.setWordWrap(True)
        self._body.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._ts_title = QLabel()
        self._ts_title.setObjectName("aboutTechSpecTitle")
        self._ts_title.setWordWrap(True)

        self._ts = QLabel()
        self._ts.setObjectName("aboutTechSpec")
        self._ts.setTextFormat(Qt.TextFormat.RichText)
        self._ts.setWordWrap(True)
        self._ts.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._ig_label = QLabel("\U0001F4F8 Instagram")
        self._ig_label.setObjectName("instagramLabel")

        ig_users = [
            ("1w1_efe", "Efe Savaş"),
            ("gus.sasiru", "Efe Nazlıgül"),
            ("histyyy0616", "Hacı Boz"),
        ]
        self._ig_btns = []
        for username, name in ig_users:
            btn = QPushButton(f"\U0001F4F7  {name}  —  @{username}")
            btn.setObjectName("instagramBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, u=username: webbrowser.open(f"https://instagram.com/{u}"))
            self._ig_btns.append(btn)

        cl.addWidget(self._sub)
        cl.addWidget(self._body)
        cl.addSpacing(8)
        cl.addWidget(self._ts_title)
        cl.addWidget(self._ts)
        cl.addSpacing(16)
        cl.addWidget(self._ig_label)
        for btn in self._ig_btns:
            cl.addWidget(btn)
        cl.addStretch(1)

        scroll.setWidget(content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        layout.addWidget(scroll, stretch=1)

        self.apply_language(locale)

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        self._head.setText("\U00002139  " + t(locale, "about_head"))
        self._map_btn.setText(t(locale, "btn_map"))
        self._sub.setText(t(locale, "about_sub"))
        self._body.setText(str(t(locale, "about_body")))
        self._ts_title.setText(t(locale, "about_techspec_title"))
        self._ts.setText(str(t(locale, "about_techspec")))
