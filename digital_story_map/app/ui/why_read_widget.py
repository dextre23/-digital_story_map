from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.data.texts import TEXTS


class WhyReadWidget(QWidget):
    map_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("whyReadRoot")
        self._locale = "tr"

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
        scroll.setObjectName("whyReadScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        container.setObjectName("whyReadContainer")
        cards_layout = QVBoxLayout(container)
        cards_layout.setContentsMargins(24, 12, 24, 24)
        cards_layout.setSpacing(16)

        for item in TEXTS:
            card = QWidget()
            card.setObjectName("whyReadCard")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 16, 20, 16)
            card_layout.setSpacing(8)

            card_title = QLabel(item["title"])
            card_title.setObjectName("whyReadCardTitle")
            card_title.setWordWrap(True)

            card_body = QLabel(item["body"])
            card_body.setObjectName("whyReadCardBody")
            card_body.setWordWrap(True)

            card_layout.addWidget(card_title)
            card_layout.addWidget(card_body)
            cards_layout.addWidget(card)

        cards_layout.addStretch(1)
        scroll.setWidget(container)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top)
        layout.addWidget(scroll, stretch=1)

    def apply_language(self, locale: str) -> None:
        self._locale = locale
        from app.i18n import t

        self._head.setText("\U0001F4DA  " + t(locale, "btn_why_read"))
        self._map_btn.setText(t(locale, "btn_map"))
